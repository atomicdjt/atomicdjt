# Pull Request Descriptions That Survive Review

*A structure extracted from a maintainer-verified fix to a security-critical regex matcher, and why each heading exists.*

**Published:** August 25, 2026
**Author:** David Turner

## Abstract

[Grid Dynamics Rosetta PR #320](https://github.com/griddynamics/rosetta/pull/320) removed quadratic backtracking from a `PreToolUse` dangerous-command matcher. A maintainer re-verified it independently across roughly 5.5 million inputs across two rounds and merged it. That outcome had less to do with the fix being clever and more to do with the description making the fix cheap to review. This is the structure, why each section exists, and what it would have cost the reviewer if a section had been missing.

---

Most PR descriptions answer one question: *what changed?* A description that survives adversarial review has to answer a different, harder set: *why is this the right change, what did you check, what could still be wrong, and how bad is it if you're wrong?*

The structure below is not a template I designed in the abstract. It is what the #320 description actually contained, in order, reconstructed after the fact because the maintainer's response showed exactly which parts of it did work.

### Summary

One or two sentences, no hedging. State what changed and where. A reviewer deciding whether to spend the next ten minutes on your diff makes that call here.

### Root cause

Not "the regex was slow" — the actual mechanism. In #320: an unbounded lookahead re-scanned from every candidate match position, so pathological input produced O(n²) rescans. Naming the mechanism, not the symptom, is what lets a reviewer verify your fix addresses the cause rather than a correlate of it.

### Structural solution

What you changed and, critically, what you *didn't* change and why. #320 kept both lookaheads unbounded — bounding either would have broken a passing test on line 84 that specifically requires matching 75,000 characters after `branch`. Stating that tradeoff up front means the reviewer's first instinct ("why not just bound the window?") is answered before they ask it.

### Security / behavioral implications

If the code sits in a security-critical path, say so explicitly and quantify the failure mode in both directions. #320's description stated plainly: a false negative could permit an unreviewed destructive branch deletion; a pathological matcher could delay every Bash tool call. Both directions matter — reviewers of security code are trained to ask "what happens when this fails," and pre-answering it changes the shape of the review.

### Validation

This is the section that did the most work in #320. Not "I tested it" — the actual method: differential testing against the previous matcher (seeded fuzz cases plus exhaustive enumeration over bounded alphabets), a harness that was itself mutation-checked before being trusted, and reported counts with zero divergence in both directions. A mutation-checked harness matters because a differential test that can't detect a deliberately broken implementation isn't evidence of anything. State the seed. State the count. State that you checked the checker.

### Tests

What's pinned by name, not just "added tests." The maintainer's first review round found a gap here directly — a whitespace variant that no existing test exercised — because the validation section made it easy to see what *hadn't* been differentially tested yet (behavioral edge cases around cross-line matching, as opposed to raw throughput).

### Performance impact

A before/after table with concrete numbers at multiple scales, not "faster." #320 reported 8.8/35.4/138.9/552.2 ms before against 0.08/0.16/0.33/0.66 ms after at 1k/2k/4k/8k repetitions, plus a flakiness check (15/15 runs) on the regression assertion. A reviewer with those numbers doesn't have to re-run your benchmark to trust the shape of the claim.

### Risk / blast radius

Quantify who is affected and how, not just "low risk." Every `PreToolUse` hook invocation running through this matcher was in scope; that's worth stating even when the change is narrow, because it tells the reviewer how much attention the change actually warrants.

### Compatibility

What existing behavior is preserved, explicitly, not left to inference from the diff.

### Limitations

The section most descriptions skip and the one that did the most credibility work here. #320 stated plainly: Windows couldn't run the hooks package's Unix shell steps, so pre-commit ran in an isolated WSL worktree; CodeQL was unavailable locally and remained a remote-only check; the performance numbers were local medians, not cross-runner guarantees. None of those weakened the PR. Naming them meant the maintainer's own follow-up testing was confirmatory rather than a search for gaps you'd hidden.

---

## What this isn't

Not every PR needs every heading. A one-line typo fix does not need a performance table. The structure exists to make a *reviewer's* job cheap on changes where the cost of being wrong is high — security paths, performance-sensitive code, anything with a blast radius bigger than the diff suggests. Forcing all ten sections onto a trivial change is the same mistake as skipping them on a load-bearing one: it optimizes for the appearance of rigor instead of the actual amount needed.

[`agent-session-bridge/.github/PULL_REQUEST_TEMPLATE.md`](https://github.com/atomicdjt/agent-session-bridge/blob/main/.github/PULL_REQUEST_TEMPLATE.md) and [`validation-ledger/.github/PULL_REQUEST_TEMPLATE.md`](https://github.com/atomicdjt/validation-ledger/blob/main/.github/PULL_REQUEST_TEMPLATE.md) encode this structure as a checklist a contributor can delete sections from, not a form they're required to fill out completely.
