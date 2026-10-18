# CrewAI #6414: real-dispatch and ambiguous-commit conformance harness

A minimal **application-owned** guarded custom tool with an actual localhost HTTP service, distinct remote and local SQLite journals, deterministic injected network faults, and a small test that traverses CrewAI's `execute_tool_and_check_finality` entrypoint. This is an independent reference harness, **not** a patch to CrewAI core or proof of an unreported CrewAI defect.

CrewAI version under test: **1.15.28**, pinned in the GitHub Actions workflow. Code was inspected at [crewAIInc/crewAI `9112709`](https://github.com/crewAIInc/crewAI/tree/911270929444ffc385e725e15976821ea503ddc2) (2026-10-18). The tool entrypoint, `CrewStructuredTool.from_function`, `AgentAction`, legacy pre-tool hooks, and hook dispatcher are real CrewAI APIs. A scripted `AgentAction` avoids LLM nondeterminism: **this exercises CrewAI's synchronous tool execution boundary, not an end-to-end Crew/agent kickoff or all native tool-call paths.**

## Run

```bash
# Dependency-free reference tests, Python 3.11+
python -m unittest discover -s research/crewai_effect_boundary -p test_boundary.py -v

# Actual CrewAI tool-dispatch integration (Python 3.11 recommended)
python -m pip install crewai==1.15.28
python -m unittest discover -s research/crewai_effect_boundary -p test_crewai_integration.py -v
```

CI installs CrewAI and explicitly verifies it imports. Without CrewAI the four integration cases are `SKIPPED`; **a local run of just the nine reference tests must not be described as real CrewAI runtime verification**.

## Invariants and expected results

| Stimulus | Expected conclusion |
|---|---|
| New operation + valid receipt | `COMMITTED`, one remote POST |
| Remote commits then drops response | First attempt `UNKNOWN`; later correlated positive status readback `COMMITTED` |
| HTTP 500 *after* commit | `UNKNOWN` until correlated status receipt |
| No reliable status or idempotency | `UNKNOWN` persists on restart; no second POST |
| Provider replies `404 NOT_FOUND` with unverified consistency | Remains `UNKNOWN`, no automatic redispatch |
| Concurrent same operation | At most one remote POST from the guarded wrapper |
| Same operation ID with different payload | Refused; never treated as an authorized retry |
| Same payload but different operation ID | Two deliberately distinct operations |
| CrewAI pre-tool hook returns `False` | CrewAI blocks the dispatch |
| CrewAI pre-tool hook raises ordinary exception | Framework fails open as designed; the **guarded tool** remains responsible for effect safety |

## Scope, non-claims, and gaps

- The simulated provider uses real localhost HTTP calls and commits effects to **its own SQLite database**; it is *not* Stripe, not a production provider, and not a distributed consistency proof. Faults occur deliberately after the remote effect commits.
- The client journal uses `BEGIN IMMEDIATE` for atomic first-claim arbitration. There is no distributed lock or claim expiry, and no automatic redispatch after uncertainty. Status `NOT_FOUND` does not establish a safe retry.
- The positive receipt is a **test-provider assertion**. Production verification needs provider authentication, immutable operation linkage, a documented status consistency/finality contract, and a carefully bounded idempotency retention policy.
- The reference tool expects the **calling application** to supply a durable logical operation ID and valid authorization. It does not mint authority permits, prove multi-process exactly-once delivery, handle provider retries outside this wrapper, or offer an operator recovery workflow.
- Normal CrewAI hook exceptions fail open, as documented in `crewai/hooks/dispatch.py`. That behavior is **not** classified as an upstream defect here. High-assurance checks belong within the guarded execution boundary, or must explicitly use CrewAI's blocking mechanism.
- Workload execution uses a deterministic `AgentAction` (no LLM, money movement, third-party APIs or external credentials). A future integration may test CrewAI native parallel calls and the full agent lifecycle separately.

## Contributing upstream

Only propose a CrewAI core change after one concrete regression demonstrates incorrect behavior at a supported execution seam. Until then, this PR is a reproducible reference integration, with links to [CrewAI issue #6414](https://github.com/crewAIInc/crewAI/issues/6414), the [AgentCI #121 corpus](https://github.com/jinngimk-lang/agentci/issues/121), and [atomicdjt PR #40](https://github.com/atomicdjt/atomicdjt/pull/40). It does **not** modify the previously pinned AgentCI corpus.
