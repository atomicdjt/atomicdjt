# Engineering proof cases: reproduce the claim, not just the demo

These case studies are review guides for two bounded results. They do not turn external PR comments into employment endorsements, turn local mocks into provider assurances, or substitute CI status for independent assessment. Source and review records are linked so a reader can challenge the claims.

## Case 1: Rosetta #320 — a performance fix that required a security-equivalence argument

**Problem.** A `git branch` deletion guard repeatedly scanned overlapping, separator-free suffixes. An adversarial long command caused approximately quadratic evaluation time before a tool call could proceed. Optimizing a security guard also creates a false-negative risk: flags from separate command segments must not combine, and legitimate force-delete spellings must remain protected.

**Change.** [Merged Rosetta PR #320](https://github.com/griddynamics/rosetta/pull/320), authored by `atomicdjt`, selected the first line-local `git branch` candidate per separator-bounded segment while preserving the original existential delete/force lookaheads. Cross-line whitespace handling was retained separately. This does not replace the matcher with a complete shell parser.

**Falsification strategy.** The old and optimized regexes were independently compiled and differentially tested; mutation probes deliberately removed cross-line recognition or truncated a necessary lookahead to verify that focused cases would fail. An upstream reviewer requested missing cross-line and same-segment later-candidate regressions; they were added before approval.

| Evidence | Reported result | Boundary |
| --- | --- | --- |
| [Submitted PR validation](https://github.com/griddynamics/rosetta/pull/320) | 3,000,000 seeded differential sequences and 12 explicit cases; zero observed divergences | Sample-based equivalence, **not** a proof for all shell input |
| [Independent reviewer history](https://github.com/griddynamics/rosetta/pull/320) | Approximately 5.5 million initial differential cases and 1.6+ million final-head checks; scaling and mutation probes | Reviewer-run evidence under tested configurations |
| [Local performance series](https://github.com/griddynamics/rosetta/pull/320) | 8,000 candidates: median 1,689.46 ms before vs. 1.59 ms after | Local Node/Linux results, not universal runner latency |
| [Merge disposition](https://github.com/griddynamics/rosetta/pull/320) | Reviewed, revised, approved, merged August 24, 2026 | Specific merged upstream change, not portfolio-wide certification |

### Reproduce from the merged project

Use a **disposable directory and no valuable Git branches**; the test suite checks a dangerous-action detector and its simulated command handling. The upstream repo owns the tests and may evolve after the cited merge.

```bash
git clone https://github.com/griddynamics/rosetta.git
cd rosetta/src/hooks
npm ci
npm run check
npm test
```

Inspect [the actual matcher source](https://github.com/griddynamics/rosetta/blob/main/src/hooks/src/hooks/dangerous-actions/patterns.ts) and [its dedicated regression file](https://github.com/griddynamics/rosetta/blob/main/src/hooks/tests/git-branch-delete.test.ts). For a historical reproduction rather than a current-main smoke test, inspect the [merged PR's commit range](https://github.com/griddynamics/rosetta/pull/320/commits) and run the equivalent commands at the exact target revision. **These commands are a reproduction path, not a claim that this documentation edit reran upstream tests.**

**Failure modes worth challenging:** cross-line `git\s+branch` variants; candidate order within a segment; flag isolation across `;`, `&&`, `|`, CR/LF; and pathological inputs with many benign candidates.

## Case 2: Recovery after an ambiguous tool side-effect

**Problem.** An agent/tool call can time out or lose its HTTP response **after** the provider performed the side effect. Treating the missing response as a proven failure and blindly retrying can cause additional effects. Treating it as proven success fabricates evidence.

**Owned reference implementation.** [crewai-stripe-recovery-fixture](https://github.com/atomicdjt/crewai-stripe-recovery-fixture) records application-owned operation IDs and payload binding in SQLite, keeps provider observations append-only, and preserves `UNKNOWN` until correlated evidence allows a narrower state. The provider in its standard test suite is a **fake**, not Stripe. It does not modify CrewAI core.

### Reproduce the current main-branch fixture

```bash
git clone https://github.com/atomicdjt/crewai-stripe-recovery-fixture.git
cd crewai-stripe-recovery-fixture
python -m unittest discover -s tests -v
```

[Inspect the test source](https://github.com/atomicdjt/crewai-stripe-recovery-fixture/blob/main/tests/test_recovery.py) and [journal implementation](https://github.com/atomicdjt/crewai-stripe-recovery-fixture/blob/main/operation_journal.py). The tests cover a lost-create response, idempotency-key reuse within a configured window, inconclusive retrieval, mismatched provider correlation, post-dispatch crash/restart, conservative migration, and a claim-safe custom tool result.

| Observation | Expected classification | Important negative control |
| --- | --- | --- |
| Fake provider accepted create but response was lost | `UNKNOWN` until authoritative recovery | Do not assert the provider did nothing |
| Correlated provider reference, amount/currency, and operation metadata | `INTENT_CREATED` (unconfirmed resource) | Do not call this a charge or payment completion |
| Inconclusive or mismatched provider response | Remain `UNKNOWN`, retain raw evidence | Do not promote an untrusted reference |
| Retry past a modeled idempotency retention window | Refuse create retry | Do not invent a safe provider-side replay |

**Independent scrutiny and active work.** The [CrewAI #6414 discussion](https://github.com/crewAIInc/crewAI/issues/6414) includes independent review of the recovery boundary. The [fixture's PR #1](https://github.com/atomicdjt/crewai-stripe-recovery-fixture/pull/1) proposes additional retry-owner fencing and stale-evidence protections, with its own CI and tests; **it is not merged into main at this checkpoint**. A reviewer should compare branch head and CI evidence rather than assuming the proposal is part of the standard fixture.

**Not proved:** live Stripe test-mode or production behavior, payment confirmation, a CrewAI framework defect, remote authoritative reconciliation, prevention of all simultaneous physical HTTP requests after lease expiry, or distributed exactly-once semantics.

## Evaluation protocol

1. Pin the exact revision and distinguish `main`, open PR head, and published release.
2. Identify a falsifiable property and a negative case that would catch its violation.
3. Execute the documented commands in an isolated environment; save command, version, exit code, and run URL.
4. Verify that the result supports **only** the stated assertion.
5. Record failures and reviewer objections; do not silently broaden the claim.

See also [all nine merged upstream contributions](external-validation-upstream-review.md) and [the attribution/acceptance correction ledger](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/discovery/external-corroboration.md).

**AI-assisted workflow:** AI helped with review and drafting. The contributor directed the scope, revised work after maintainer feedback, and owns the submitted claims; the primary GitHub record remains the source for authorship, merge, and reviewer provenance.
