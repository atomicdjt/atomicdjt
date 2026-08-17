#!/usr/bin/env python3
"""Minimal deterministic oracle for CrewAI #6414 / AgentCI trajectory breaker."""
from __future__ import annotations
import argparse, copy, json, re
from collections import defaultdict
from pathlib import Path

SV = "agentci-trajectory-event/v0.1"
NV = "semnorm/v0.1"
CASES = {"repeat-block-before-dispatch", "progress-allows-repeat", "material-change-allows"}
KINDS = {"message","tool_call","tool_result","checkpoint","artifact","error"}
STATUSES = {"started","ok","failed","blocked"}
CRED = (re.compile(r"^sk-[\w-]+$"), re.compile(r"^Bearer\s+\S+$", re.I),
        re.compile(r"^gh[pousr]_[\w-]+$", re.I))

class CorpusError(ValueError): pass
def fail(msg): raise CorpusError(msg)

def load(path):
    out=[]
    for n,line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(),1):
        if not line.strip(): continue
        try: e=json.loads(line)
        except json.JSONDecodeError as x: fail(f"line {n}: invalid JSON: {x}")
        if not isinstance(e,dict): fail(f"line {n}: event must be object")
        out.append(e)
    if not out: fail("empty corpus")
    return out

def scalars(v):
    if isinstance(v,dict):
        for x in v.values(): yield from scalars(x)
    elif isinstance(v,list):
        for x in v: yield from scalars(x)
    else: yield v

def base(events):
    groups=defaultdict(list); runs=set()
    for i,e in enumerate(events):
        req={"schema_version","run_id","case_id","seq","kind"}
        if req-e.keys(): fail(f"event {i}: missing {sorted(req-e.keys())}")
        if e["schema_version"]!=SV: fail(f"event {i}: wrong schema_version")
        if not isinstance(e["run_id"],str) or not e["run_id"]: fail(f"event {i}: bad run_id")
        if not isinstance(e["case_id"],str) or not e["case_id"]: fail(f"event {i}: bad case_id")
        if not isinstance(e["seq"],int) or e["seq"]<0: fail(f"event {i}: bad seq")
        if e["kind"] not in KINDS: fail(f"event {i}: bad kind")
        if "status" in e and e["status"] not in STATUSES: fail(f"event {i}: bad status")
        for x in scalars(e):
            if isinstance(x,str) and any(p.match(x) for p in CRED):
                fail(f"event {i}: raw credential-like value leaked")
        runs.add(e["run_id"]); groups[e["case_id"]].append(e)
    if len(runs)!=1: fail("run_id drift")
    if set(groups)!=CASES: fail(f"case set mismatch: {sorted(groups)}")
    for cid,evs in groups.items():
        if [e["seq"] for e in evs] != list(range(len(evs))):
            fail(f"{cid}: trajectory is not append-only/contiguous")
    return groups

def calls(evs):
    out=[e for e in evs if e["kind"]=="tool_call"]
    need={"attempt_id","agent","tool","normalization_version","canonical_args_sha256",
          "canonical_semantics","decision","progress_digest","volatile_fingerprint",
          "volatile_fields_ignored","secret_digests"}
    for e in out:
        m=e.get("metadata",{})
        if need-m.keys(): fail(f"{e['case_id']}: incomplete tool_call metadata")
        if m["normalization_version"]!=NV: fail(f"{e['case_id']}: normalization version drift")
        if m["decision"] not in {"allow","block"}: fail(f"{e['case_id']}: bad decision")
        if m["tool"]!=e.get("name"): fail(f"{e['case_id']}: tool identity mismatch")
        if not {"trace_id","request_id"} <= set(m["volatile_fields_ignored"]):
            fail(f"{e['case_id']}: volatile-field classification missing")
        h=m["canonical_args_sha256"]
        if not isinstance(h,str) or len(h)!=64:
            fail(f"{e['case_id']}: bad canonical digest")
        try: int(h,16)
        except ValueError: fail(f"{e['case_id']}: non-hex canonical digest")
        if not m["secret_digests"] or any(
            not isinstance(v,str) or not v.startswith("sha256:")
            for v in m["secret_digests"].values()):
            fail(f"{e['case_id']}: secrets must be digest-only")
    return out

def receipts(evs):
    r=defaultdict(list)
    for e in evs:
        if e["kind"]!="tool_result": continue
        m=e.get("metadata",{})
        if not m.get("attempt_id") or not m.get("dispatch_receipt_id"):
            fail(f"{e['case_id']}: unbound dispatch receipt")
        if m.get("external_side_effect") is not True:
            fail(f"{e['case_id']}: tool_result is not explicit side-effect evidence")
        r[m["attempt_id"]].append(e)
    return r

def exact_one(r,attempt,where):
    if len(r.get(attempt,[]))!=1: fail(f"{where}: allowed attempt needs exactly one dispatch receipt")

def verify(events):
    g=base(events); results=[]
    # Breaker: same semantics + no progress + different volatile IDs => second must block pre-dispatch.
    ev=g["repeat-block-before-dispatch"]; c=calls(ev); r=receipts(ev)
    if len(c)!=2: fail("repeat: expected two calls")
    a,b=(x["metadata"] for x in c)
    if a["canonical_args_sha256"]!=b["canonical_args_sha256"]: fail("repeat: volatile-only difference changed digest")
    if a["canonical_semantics"]!=b["canonical_semantics"]: fail("repeat: semantic drift")
    if a["progress_digest"]!=b["progress_digest"]: fail("repeat: progress drift")
    if a["volatile_fingerprint"]==b["volatile_fingerprint"]: fail("repeat: volatile control did not vary")
    if (a["decision"],b["decision"])!=("allow","block"): fail("repeat: detector must allow then block")
    exact_one(r,a["attempt_id"],"repeat")
    if r.get(b["attempt_id"]): fail("repeat: blocked attempt dispatched")
    terminal=[e for e in ev if e["kind"]=="error" and e.get("status")=="blocked"]
    if len(terminal)!=1 or terminal[0].get("metadata",{}).get("terminal_reason")!="trajectory_repeat_blocked":
        fail("repeat: missing terminal blocked reason")
    if terminal[0]["metadata"].get("external_side_effects_observed")!=1:
        fail("repeat: side-effect count proves extra dispatch")
    results.append({"case":"repeat-block-before-dispatch","verdict":"PASS","dispatch_receipts":1})
    # Negative control: same action after evidenced progress is legitimate.
    ev=g["progress-allows-repeat"]; c=calls(ev); r=receipts(ev)
    if len(c)!=2: fail("progress: expected two calls")
    a,b=(x["metadata"] for x in c)
    if a["canonical_args_sha256"]!=b["canonical_args_sha256"]: fail("progress: action digest changed")
    if a["progress_digest"]==b["progress_digest"]: fail("progress: no progress evidence")
    if (a["decision"],b["decision"])!=("allow","allow"): fail("progress: legitimate iteration was blocked")
    exact_one(r,a["attempt_id"],"progress"); exact_one(r,b["attempt_id"],"progress")
    if not any(e["kind"]=="checkpoint" and e.get("metadata",{}).get("progress_digest")==b["progress_digest"] for e in ev):
        fail("progress: changed state lacks checkpoint evidence")
    results.append({"case":"progress-allows-repeat","verdict":"PASS","dispatch_receipts":2})
    # Normalization control: material semantic change must not collide.
    ev=g["material-change-allows"]; c=calls(ev); r=receipts(ev)
    if len(c)!=2: fail("change: expected two calls")
    a,b=(x["metadata"] for x in c)
    if a["canonical_args_sha256"]==b["canonical_args_sha256"]: fail("change: material actions collided")
    if a["progress_digest"]!=b["progress_digest"]: fail("change: progress must stay constant")
    if (a["decision"],b["decision"])!=("allow","allow"): fail("change: material change was blocked")
    exact_one(r,a["attempt_id"],"change"); exact_one(r,b["attempt_id"],"change")
    results.append({"case":"material-change-allows","verdict":"PASS","dispatch_receipts":2})
    return {"verdict":"PASS","schema_version":SV,"normalization_version":NV,
            "total_events":len(events),"cases":results}

def expect_fail(events,needle):
    try: verify(events)
    except CorpusError as e:
        if needle not in str(e): fail(f"self-test expected {needle!r}, got {e!r}")
        return
    fail(f"self-test expected failure containing {needle!r}")

def self_test(reference):
    checks=[]
    # 1: false PASS — fabricated dispatch after the blocked attempt.
    x=copy.deepcopy(reference)
    block=[e for e in x if e["case_id"]=="repeat-block-before-dispatch"]
    i=x.index(block[-1])
    x.insert(i,{"schema_version":SV,"run_id":block[0]["run_id"],"case_id":"repeat-block-before-dispatch",
                "seq":3,"kind":"tool_result","name":"search_web","status":"ok",
                "metadata":{"attempt_id":"repeat-2","dispatch_receipt_id":"dispatch:repeat-2",
                            "external_side_effect":True,"external_side_effect_index":2}})
    n=0
    for e in x:
        if e["case_id"]=="repeat-block-before-dispatch": e["seq"],n=n,n+1
    expect_fail(x,"blocked attempt dispatched"); checks.append("false-pass-second-dispatch")
    # 2: false positive — block a legitimate same-action iteration after progress.
    x=copy.deepcopy(reference)
    c=[e for e in x if e["case_id"]=="progress-allows-repeat" and e["kind"]=="tool_call"][1]
    c["metadata"]["decision"]="block"; c["status"]="blocked"
    expect_fail(x,"legitimate iteration was blocked"); checks.append("false-positive-progress")
    # 3: volatile-only IDs must not alter action identity.
    x=copy.deepcopy(reference)
    c=[e for e in x if e["case_id"]=="repeat-block-before-dispatch" and e["kind"]=="tool_call"][1]
    c["metadata"]["canonical_args_sha256"]="f"*64
    expect_fail(x,"volatile-only difference changed digest"); checks.append("volatile-normalization")
    # 4: raw secret-like values must never land in evidence.
    x=copy.deepcopy(reference); x[0]["metadata"]["debug_raw_secret"]="sk-test-do-not-emit"
    expect_fail(x,"raw credential-like value leaked"); checks.append("secret-leak")
    # 5: evidence is append-only/ordered.
    x=copy.deepcopy(reference)
    c=[e for e in x if e["case_id"]=="material-change-allows"]; c[2]["seq"]=1
    expect_fail(x,"not append-only/contiguous"); checks.append("sequence-integrity")
    return {"verdict":"PASS","self_tests":checks,"count":len(checks)}

def main(argv=None):
    p=argparse.ArgumentParser()
    p.add_argument("corpus",nargs="?",default="corpus.jsonl")
    p.add_argument("--self-test",action="store_true")
    p.add_argument("--json",action="store_true")
    a=p.parse_args(argv)
    try:
        events=load(a.corpus); result=verify(events)
        if a.self_test: result["adversarial_self_test"]=self_test(events)
    except (OSError,CorpusError) as e:
        print(json.dumps({"verdict":"FAIL","error":str(e)},sort_keys=True) if a.json else f"FAIL: {e}")
        return 1
    print(json.dumps(result,sort_keys=True) if a.json else json.dumps(result,indent=2,sort_keys=True))
    return 0

if __name__=="__main__": raise SystemExit(main())
