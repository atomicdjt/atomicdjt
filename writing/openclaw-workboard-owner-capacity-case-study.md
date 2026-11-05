# Engineering case: OpenClaw Workboard owner capacity after completed executions

**Disposition:** [atomicdjt-authored PR #187880](https://github.com/openclaw/openclaw/pull/187880), merged into `openclaw/openclaw` on October 29, 2026 at 22:00:17 UTC. Maintainer [merge confirmation](https://github.com/openclaw/openclaw/pull/187880#issuecomment-6509310231) cites `f421bd20a6`.

## User-visible failure

Workboard limits concurrent task dispatch by owner. A card can be *completed* while its persisted historical execution is still marked `running`. Before the change, the slot-occupancy predicate evaluated `card.execution?.status === "running"` without excluding `card.status === "done"`. A historical execution could therefore occupy an owner's live concurrency slot, causing ready work in another board to remain undispatched.

## Narrow change and invariant

The shared SQL owner-capacity predicate is used by dispatcher selection and atomic SQLite admission. It now requires that the card is not `done` before evaluating active claims, running card status, or a running execution. It **does not delete or rewrite historical executions**.

| Scenario | Required behavior |
| --- | --- |
| `done` card with historical `running` execution | Does **not** consume a slot; next eligible ready card can dispatch |
| Nonterminal card with a `running` execution | Still consumes a slot |
| Nonterminal card with a valid live claim | Still consumes a slot |
| Archived or reclaimable state | Existing exclusion/reclamation rules remain in force |

The accepted PR changed two files with 15 additions and 19 deletions. The regression exercises completed-vs-nonterminal execution conditions against the SQLite Workboard persistence path. [See patch and commits](https://github.com/openclaw/openclaw/pull/187880/files).

## Verification and independent challenge

1. Inspect the [merged PR diff](https://github.com/openclaw/openclaw/pull/187880/files) and its base/head history for the exact predicate and test cases.
2. Check the [automated review](https://github.com/openclaw/openclaw/pull/187880#issuecomment-6507693727), which initially required maintainer review.
3. Read [maintainer `obviyus`'s independent integration account](https://github.com/openclaw/openclaw/pull/187880#issuecomment-6508868833): it describes isolated Docker builds of a real Gateway with Workboard, SQLite worker, local deterministic Chat Completions provider and base-vs-candidate dispatch comparison.
4. Confirm [the maintainer's merge statement](https://github.com/openclaw/openclaw/pull/187880#issuecomment-6509310231) and matching merged PR state.

The maintainer reported two base/candidate repetitions using synthetic legacy records and a deterministic local provider. The base started no affected workers; the candidate started and completed one in each repetition. The maintainer also reported 56 passing focused tests and an intended base failure. These are **upstream-recorded results**, not a fresh reproduction by this case study. It is not a claim that this case study independently reran their environment. Exact historical reproduction requires pinned commits, dependencies and disposable state. Running an arbitrary current `main` checkout is not equivalent.

## Expected effect for a user

A worker's stale history on a completed card no longer prevents dispatch of another eligible task merely because the historical execution field remained `running`. The old execution record remains available for inspection.

## Limits and professional relevance

This confirms one accepted and tested change in the Workboard dispatch path. It does not prove a measured fleet-wide throughput increase, the absence of unrelated scheduler defects, production adoption of a particular release, or employment/endorsement by OpenClaw maintainers.

**Competencies represented:** root-cause analysis across persisted state and scheduling policy, minimal production change, regression-case design, preservation of historical data, and constructive external code review.

**AI assistance:** AI-assisted development and review were used. The contributor is responsible for the submitted code, evidence boundaries, and communication; upstream GitHub records determine what was authored, tested, reviewed, and merged.
