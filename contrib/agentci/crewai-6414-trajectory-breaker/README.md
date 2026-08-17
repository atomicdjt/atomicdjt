# CrewAI #6414 → AgentCI trajectory/resource-breaker corpus

**Reporter:** `atomicdjt` + ChatGPT (external agent)  
**Source provenance:** `crewAIInc/crewAI#6414`  
**AgentCI snapshot inspected:** `02d9536d1771dedab536cf38cec6ca2913240a5e`

## Falsifiable claim

A repeated, semantically equivalent trajectory with no observable progress must be blocked **before** the next external side effect, while a legitimate repeated action after observable state change must still be allowed.

This is a deliberately small provider-neutral corpus. It operationalizes the pre-dispatch boundary requested in the AgentCI invitation on CrewAI #6414 and incorporates `atomicdjt`'s earlier semantic-normalization proposal.

## Reproduce

Python 3.11+, standard library only:

```bash
python verify.py corpus.jsonl --self-test
```

Expected: top-level `verdict: PASS`, three corpus cases PASS, and five adversarial self-tests PASS.

## Cases

1. **`repeat-block-before-dispatch`** — same agent/tool, same normalized action, same progress, but different volatile request/trace identity. First attempt dispatches once; second is blocked and has **no** dispatch receipt.
2. **`progress-allows-repeat`** — same normalized action after an evidenced progress checkpoint. Both attempts remain allowed and each has a dispatch receipt.
3. **`material-change-allows`** — progress held constant while semantic arguments change. Canonical digest changes and both attempts remain allowed.

The adversarial self-test then deliberately manufactures:
- a false PASS with a second dispatch after the block;
- an over-aggressive false positive after legitimate progress;
- canonical-digest drift caused only by volatile identity;
- raw credential-like evidence leakage;
- non-append-only sequence evidence.

All five corruptions must be rejected.

## Normalization boundary

Fixture normalization version: `semnorm/v0.1`.

```text
raw args
→ schema-aware field classification
→ volatile-field exclusion
→ secret digest substitution
→ deterministic canonical semantics
→ SHA-256 trajectory action digest
```

Reference policy:
- `semantic`: `query`, `limit`
- `volatile`: `trace_id`, `request_id`
- `secret`: `api_key` → digest only
- `contextual`: progress/run identity stays outside the canonical action digest

## Evidence format

`corpus.jsonl` uses AgentCI's `agentci-trajectory-event/v0.1` shape: stable run/case identity, monotonic sequence, typed events, explicit detector decisions, dispatch receipts, and terminal reason.

The 15 reference events were separately validated against AgentCI's current `schemas/trajectory-event.schema.json`.

## Safety and truth boundary

This corpus is synthetic and side-effect-free: no network, no paid API calls, no real credentials, no CrewAI execution. Synthetic `dispatch_receipt_id` values model the evidence a real runtime adapter must bind to its actual execution seam.

Passing the corpus therefore **does not prove CrewAI currently intercepts every irreversible dispatch**. It defines the falsifiable provider-neutral contract that a real adapter can be tested against.

## Provenance

- CrewAI issue: https://github.com/crewAIInc/crewAI/issues/6414
- `atomicdjt` normalization proposal: https://github.com/crewAIInc/crewAI/issues/6414#issuecomment-5291787085
- AgentCI contribution invitation: https://github.com/crewAIInc/crewAI/issues/6414#issuecomment-5312734358
- AgentCI recognition contract: https://github.com/jinngimk-lang/agentci/blob/main/COMMUNITY.md
