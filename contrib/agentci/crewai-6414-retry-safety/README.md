# CrewAI #6414: retry, side-effect, and idempotency companion fixture

A **separate, synthetic** regression model for the question raised in [CrewAI #6414](https://github.com/crewAIInc/crewAI/issues/6414#issuecomment-6228790433). It extends the test *ideas* in [AgentCI #121](https://github.com/jinngimk-lang/agentci/issues/121) without editing the previously published immutable corpus or its manifests.

## Core contract

Do not confuse three distinct identities:

- **Logical `operation_id`**: minted once by the application, before first dispatch; reused by retry attempts. A payload digest binds it to the same action. Two intentional operations with identical payloads receive different IDs.
- **`attempt_id`**: distinguishes each local attempt.
- **`authorization_permit_id`**: distinct, single-use per permitted attempt; the harness tests permit replay rejection. Real policy decisions and permit issuance must be implemented by an external authority.

A trajectory hash does **not** establish remote commit status. A new authorization permit does **not** establish that retrying an unknown effect is safe. A local `ToolUsageStartedEvent` does **not** prove the effect crossed the real dispatch boundary.

## Run

Requires Python 3.11+; **standard library only**:

```bash
python verify.py
```

Expected: **10 tests passed**, including pre-dispatch failure, committed effect/response loss, unknown outcome without recovery support, replay under remote idempotency, concurrent claim, distinct operations with identical inputs, revoked authority, changed payload, replayed permit, and SQLite restart/reconciliation.

## Evidence and scope

The executable uses a transactional SQLite claim ledger and a simulated remote-effect counter. It reopens the ledger to simulate process restart, and threads race for an identical operation claim. No real CrewAI execution, API calls, money movement, network connection, or hosted-service fault injection occurs.

The mock remote service models either a **reliable read-after-write status lookup** or a **server-enforced idempotency contract**. Neither capability can safely be assumed for arbitrary tools. An `UNKNOWN` outcome with neither capability fails closed, possibly sacrificing liveness.

This is a **local reference contract**, not an AgentCI `agentci-trajectory-event/v0.1` ingestion artifact, a proven CrewAI adapter, an exactly-once distributed execution guarantee, or independently verified upstream compatibility. A real adapter must bind the operation key to the external provider, durably record the operation and permit before dispatch, propagate the same key on retries, handle cancellation/restart/concurrency across processes, and independently establish any remote reconciliation/idempotency guarantees.

## Relevant code

CrewAI current default-branch `ToolCallHookContext` exposes mutable tool inputs and agent/task/crew context but no documented durable operation identity: [`hooks/tool_hooks.py`](https://github.com/crewAIInc/crewAI/blob/main/lib/crewai/src/crewai/hooks/tool_hooks.py). The inspected native path emits `ToolUsageStartedEvent` before running tool pre-hooks: [`agents/agent_executor.py`](https://github.com/crewAIInc/crewAI/blob/main/lib/crewai/src/crewai/agents/agent_executor.py). These are observed implementation details, not assertions of exhaustive integration across all CrewAI execution paths.

## Relationship to immutable provenance

The original [AgentCI #121 artifact](https://github.com/atomicdjt/atomicdjt/tree/967aaa5242850087be4b91e4fe8655042e18203c/contrib/agentci/crewai-6414-trajectory-breaker) remains unchanged at commit `967aaa5242850087be4b91e4fe8655042e18203c`. This independent companion uses new files and does not change its prior test outputs or claims.