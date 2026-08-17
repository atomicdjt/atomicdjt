# Validation evidence

Validated locally on 2026-08-17.

**AgentCI snapshot inspected:** `02d9536d1771dedab536cf38cec6ca2913240a5e`

## Reproduction

```bash
python verify.py corpus.jsonl --self-test
```

Observed top-level result:

```text
verdict: PASS
reference cases: 3/3 PASS
adversarial self-tests: 5/5 PASS
total trajectory events: 15
```

Adversarial checks prove the verifier rejects:
1. a fabricated second dispatch after a blocked repeat;
2. blocking a legitimate same-action iteration after evidenced progress;
3. canonical digest drift caused only by volatile request/trace identity;
4. raw credential-like material in trajectory evidence;
5. non-append-only/non-contiguous event sequencing.

## AgentCI schema conformance

All 15 JSONL events were separately validated using JSON Schema Draft 2020-12 against AgentCI's `schemas/trajectory-event.schema.json` from the inspected snapshot.

```text
15/15 events conform to agentci-trajectory-event/v0.1
```

## SHA-256

```text
README.md    392ea19081937fcd832980ceb4d8be56b620ff28a45c8eeaeb8690d9debb27f1
corpus.jsonl 1c711190ae86ed3b960d14f16bb2ecaaf9bf434a83ae5b26465201347208f3c9
verify.py    f01375e35782bdc0dfc96e132f4d6a47b9640a46a7e0ca4b71b6460e69355257
```

The same digests are recorded in `manifest.json`.

## Limitations

- This is a provider-neutral deterministic corpus, not a live CrewAI runtime integration.
- `dispatch_receipt_id` values are synthetic evidence markers.
- Passing this corpus does not establish that a specific runtime intercepts every irreversible dispatch path; that requires provider-specific end-to-end binding.
- No CrewAI or AgentCI adoption/certification claim is made.
