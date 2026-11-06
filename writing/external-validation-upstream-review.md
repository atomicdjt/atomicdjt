# External Validation: What Upstream Review Actually Established

**Current verified count as of November 5, 2026: 16 authored pull requests merged in four external repositories** — ten Rosetta, three Super Productivity, one OpenClaw, and two OpenWorldRPGUnreal. [Super Productivity #11273](https://github.com/super-productivity/super-productivity/pull/11273) is the November 5 addition. The dated November 4 table below remains a historical 15-PR snapshot; the added PR and current count are recorded here without rewriting that snapshot. This count includes only PRs authored by `atomicdjt` with GitHub's merged state and excludes self-owned repositories, open or closed-unmerged submissions, and comments on pull requests authored by others.

Self-directed projects show what I can build. Upstream review shows what happens when somebody else controls acceptance.

Checked November 4, 2026 against the GitHub pull-request records. This note records **15 authored merged pull requests in external repositories**: ten in Grid Dynamics' Rosetta, two in super-productivity, one in OpenClaw, and two in a collaborator's OpenWorldRPGUnreal repository. Each link below identifies a specific accepted change, not endorsement of unrelated work.

The claim is deliberately narrow. A merged pull request is evidence that a specific contribution survived an external project's review process. It is not a blanket endorsement of my portfolio, seniority, or every technical judgment I make.

**November 5 update:** [Super Productivity #11273](https://github.com/super-productivity/super-productivity/pull/11273) subsequently merged; see the [weekday API case study](super-productivity-weekday-api-case-study.md). The count and table below are retained as the November 4 snapshot.

## The record

| Contribution | Scope | External result |
| --- | --- | --- |
| [Rosetta #299](https://github.com/griddynamics/rosetta/pull/299) | Dangerous-action guard correctness | Merged upstream after focused regression work |
| [Rosetta #319](https://github.com/griddynamics/rosetta/pull/319) | Dataset lookup ambiguity + removal of dead authorization surface | Revised through human review, approved, merged |
| [Rosetta #320](https://github.com/griddynamics/rosetta/pull/320) | Security-critical matcher performance/correctness | Independently differential-tested, revised, approved, merged |
| [Rosetta #322](https://github.com/griddynamics/rosetta/pull/322) | Dataset-name resolution regression coverage | Review gaps corrected, mutation-checked, merged |
| [super-productivity #9619](https://github.com/super-productivity/super-productivity/pull/9619) | Section-visible task ordering | Regression fix merged upstream |
| [Rosetta #338](https://github.com/griddynamics/rosetta/pull/338) | Configurable command-evaluator timeout and descendant-process termination | Merged September 29, 2026 |
| [Rosetta #339](https://github.com/griddynamics/rosetta/pull/339) | MultiEdit review-marker source restricted to newly written content | Merged September 29, 2026 |
| [Rosetta #359](https://github.com/griddynamics/rosetta/pull/359) | Equal-size binary-change detection during publish | Merged October 19, 2026 |
| [super-productivity #10126](https://github.com/super-productivity/super-productivity/pull/10126) | Schedule day panel preserves the user's scroll position after initialization | Merged September 25, 2026 |
| [Rosetta #377](https://github.com/griddynamics/rosetta/pull/377) | Reject empty domain input before destructive generation cleanup | Maintainer-approved, merged October 29, 2026 |
| [Rosetta #378](https://github.com/griddynamics/rosetta/pull/378) | Reject duplicate case agent IDs before trial matrix construction | Maintainer-approved, merged October 29, 2026 |
| [Rosetta #379](https://github.com/griddynamics/rosetta/pull/379) | Nonzero CLI parse exit status when polling deadline expires with pending documents | Maintainer-approved, merged October 29, 2026 |
| [OpenClaw #187880](https://github.com/openclaw/openclaw/pull/187880) | Exclude completed Workboard cards from active owner-slot occupancy | Maintainer-confirmed, merged October 29, 2026 |
| [OpenWorldRPGUnreal #252](https://github.com/TateParker/OpenWorldRPGUnreal/pull/252) | Extend combat and movement test level | Merged October 21, 2026; source PR documents validation bounds |
| [OpenWorldRPGUnreal #253](https://github.com/TateParker/OpenWorldRPGUnreal/pull/253) | Publish issue #248 asset verification manifest | Merged October 21, 2026 |

The 15-count excludes pull requests merged in my own repositories and excludes external proposals still open or closed without merge. [Rosetta #359](https://github.com/griddynamics/rosetta/pull/359) is included. GitHub's [merged external contribution search](https://github.com/search?q=is%3Apr+is%3Amerged+author%3Aatomicdjt+-user%3Aatomicdjt&type=pullrequests) offers an independent cross-check; check individual PR pages for authorship and exact dispositions.

## Case 1: Rosetta #320 - performance improvement under adversarial review

The problem was a dangerous-command matcher whose repeated suffix scanning produced quadratic behavior on adversarial input. The proposed change restructured candidate discovery around separator-bounded segments while preserving the existing delete/force predicates.

The important part is not merely that the patch was merged. The reviewer independently stress-tested the equivalence claim rather than relying on my test report.

During the first review, the reviewer:

- compared the old and new matcher across roughly 5.5 million generated and adversarial inputs with zero observed behavioral divergence;
- independently reproduced the scaling change from quadratic growth to approximately linear growth;
- mutation-checked the performance/equivalence harness;
- identified two missing regression boundaries: cross-line `git branch` forms and a same-segment later-candidate case; and
- requested comments documenting why the optimization remains sound only while the relevant lookahead windows remain unbounded to the segment end.

I added the requested cases and invariants rather than broadening the patch.

On the final head, the reviewer independently ran another 1.6+ million differential cases, mutation-checked both failure directions, reproduced the scaling improvement, and approved the contribution. The PR was then merged upstream.

Evidence: [PR #320 and review history](https://github.com/griddynamics/rosetta/pull/320).

## Case 2: Rosetta #319 - the review changed the problem, not just the code

PR #319 is useful evidence for a different reason. The original issue pointed toward hardening a team-authorization path. During review, the maintainer established that the path could not execute in the current product surface.

The right response was therefore not to defend the original implementation. I removed the dead authorization machinery and kept the live-path `DatasetLookup` collision hardening that the reviewer identified as the valuable part of the work.

The contribution then went through another documentation-focused review. I made the requested surgical corrections, including restoring live invitation guidance, removing only false product claims, and recording the deleted authorization pattern in the change log.

The final review re-ran the MCP/CLI suites and type checks, confirmed the stale authorization surface was gone, verified the live dataset-lookup path, approved the result, and the PR was merged.

This is stronger evidence to me than an unchallenged merge: the final contribution became materially different because outside review falsified part of the initial premise.

Evidence: [PR #319 and review history](https://github.com/griddynamics/rosetta/pull/319).

## Later reliability fixes

Rosetta #338 added a configurable deadline to command evaluation. The accepted implementation terminates the process tree when a shell command hangs and returns a normal failed evaluation. Its review history documents how hosted Ubuntu exposed descendant processes surviving the initial timeout approach. Rosetta #339 narrowed the `Rosetta-AI-reviewed` override to `new_string`, closing the case where a marker in old text or an unrelated property could authorize a MultiEdit write.

Super-productivity #10126 removed the periodic effect that re-scrolled the schedule day panel as the current-time row advanced. It retained the initial scroll and current-time display. This is a small, accepted usability repair; its merge does not imply the independent differential-verification evidence recorded for Rosetta #320.

## Case 3: OpenClaw #187880 — a completed card must not consume live worker capacity

A Workboard card marked `done` could retain an execution marked `running` from its history. The owner-slot occupancy predicate then counted that completed card as active, preventing a ready card belonging to the same owner on another board from dispatching. [PR #187880](https://github.com/openclaw/openclaw/pull/187880), authored by `atomicdjt`, changes the predicate so completed cards do not consume live owner capacity while nonterminal running work still does.

The change was limited to two files (15 additions, 19 deletions). Tests distinguish a completed historical execution from a nonterminal running execution and other active claims. In the PR discussion, maintainer `obviyus` supplied a built Gateway / real Workboard differential account using isolated SQLite state and a deterministic local provider, then confirmed the merge in `f421bd20a6` on October 29. These are upstream review records, not a claim that I ran the maintainer's environment or that all production deployments have been observed. [Reproduction and caveats](openclaw-workboard-owner-capacity-case-study.md).

## Collaboration that is **not** counted as an authored merge

[Rosetta #397](https://github.com/griddynamics/rosetta/pull/397) was authored by `xyrolle` to address the publishing-path defect intentionally left outside my merged [#379](https://github.com/griddynamics/rosetta/pull/379). I reviewed scope and versioning in its discussion; that collaboration is distinct from implementation authorship. [Home Assistant frontend #55484](https://github.com/home-assistant/frontend/pull/55484) and [Bitwarden clients #24289](https://github.com/bitwarden/clients/pull/24289) remain submitted, not accepted, at this check.

## What I take from the record

The recurring pattern across these contributions is not "I wrote code and CI was green." It is:

1. isolate a concrete failure mode;
2. make a narrowly scoped change;
3. add tests that can fail for the right reason;
4. expose the reasoning and verification in the pull request;
5. accept external correction when the evidence changes the problem; and
6. keep the final public claim no broader than what the merge and review actually establish.

That is the same discipline I try to apply to independent product work: explicit boundaries, reproducible checks, and claims that can survive someone else's scrutiny.

## What this does not prove

These merges do not establish broad product adoption, customer traction, employment by the upstream organizations, or senior-engineering tenure. They establish something narrower and more useful for evaluating my work: external repositories reviewed specific contributions closely enough to challenge them, request changes, independently reproduce key claims, and ultimately merge them.

## AI-assisted workflow disclosure

AI systems assisted with repository analysis, implementation, testing, debugging, and drafting on parts of this work. I directed scope, reviewed the resulting changes, responded to maintainer feedback, checked the evidence boundaries, and take responsibility for the submitted and published claims.
