# Retry-safety companion: local verification receipt

Verified on October 17, 2026 using Python 3.13.5, standard library only.

Command:

```bash
python verify.py
```

Result: **10 tests passed**, 0 failures, 0 errors (local synthetic model).

Source integrity, SHA-256 of exact locally tested files:

- `verify.py`: `0f902c4a69f27ce0558ed22a2eb3d2886be2761f5f4ffa1283e2d3b7d3f6c118`
- `README.md`: `ed85f21cd8b8b2de63c94f1a9b4548c2eacaa7877277556a48814c99a0ac66fa`

The tests cover a known pre-dispatch failure and authorized retry; committed effect with lost response and readback; unknown commit with no reconciliation capability; remote-enforced idempotency; concurrent duplicate attempts; distinct authorized operations with equal arguments; revoked authority; payload drift; permit reuse; and restart with SQLite claim preservation, unique retry-attempt identity, and subsequent reconciliation.

**Boundaries:** This receipt is for the local code model. It is **not** an assertion that CrewAI currently enforces the behavior, that GitHub CI ran the tests, or that any real remote provider ensures exactly-once effects. The remote effect counter and read-after-write/idempotency capabilities are simulations. The pre-dispatch hook inspection is confined to inspected paths; no claim of universal coverage is made.

Upstream discussion: https://github.com/crewAIInc/crewAI/issues/6414#issuecomment-6242448169

Previously frozen AgentCI #121 corpus remains untouched at `967aaa5242850087be4b91e4fe8655042e18203c`.
