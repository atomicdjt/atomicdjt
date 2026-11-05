# Engineering case: custom weekdays in the Super Productivity Local REST API

[PR #11273](https://github.com/super-productivity/super-productivity/pull/11273), authored by `atomicdjt`, was merged by maintainer `johannesjo` on November 5, 2026 at 19:19:39 UTC. It corrects how the Local REST API interprets partial custom weekday selections for recurring tasks. [Issue #11262](https://github.com/super-productivity/super-productivity/issues/11262) describes the reported problem.

## Problem and architecture

A client creating a Wednesday-only custom weekly schedule could get Monday through Friday because the request was combined with a default repeat configuration that had those weekdays selected. The API route builds a repeat configuration from defaults or an existing configuration and the supplied custom fields; the resulting selection affects recurring-task generation. An integration relying on the requested schedule could therefore create tasks on unintended days.

## Root cause and design

The underlying problem was treating a partial weekday selection as ordinary field-by-field overrides over a base containing selected days. The [merged change](https://github.com/super-productivity/super-productivity/pull/11273/files) detects whether a `CUSTOM` request supplies any weekday. If it does, the route overlays an all-false weekday set before applying the supplied values. Thus supplied days define the complete selection. For a PATCH with no weekday fields, existing weekdays remain; for a create without them, defaults remain. The implementation rejects an explicitly empty weekly selection, and non-custom preset handling is unchanged.

The alternative of clearing defaults for every explicit weekly create would change previously valid requests that specify no weekday. Review identified that compatibility regression. Restricting replacement to requests that name a weekday addresses the reported defect while retaining the omitted-field behavior. This decision is grounded in the [review discussion](https://github.com/super-productivity/super-productivity/pull/11273#issuecomment-6518707549), not a claim that every alternative was evaluated.

## Regression coverage and review

The PR adds Jasmine cases for Wednesday-only creation, empty selection rejection, replacing weekdays through PATCH, preserving weekdays when changing only the repeat interval, and preserving creation defaults with an explicit or omitted weekly cycle. The [diff](https://github.com/super-productivity/super-productivity/pull/11273/files) includes the implementation, route tests, and API documentation.

A review comment posted under the maintainer account identified the default-preservation regression and requested documentation of PATCH replacement semantics. The comment labels itself an automated Claude Code review pass. Subsequent commits preserved omitted defaults, added tests, and updated the API documentation. The [follow-up](https://github.com/super-productivity/super-productivity/pull/11273#issuecomment-6666060130), also labeled an automated pass, reported the two points resolved and stated that the reviewer did not run the tests personally. The maintainer subsequently merged the PR.

The PR's final-head [CI run](https://github.com/super-productivity/super-productivity/actions/runs/41776303136) reports successful unit tests, lint, build and E2E jobs. This account relies on the recorded GitHub checks; it does not claim a fresh local run for this case study. Some separate sync E2E jobs were skipped by their workflow.

## Outcome and limits

The merged code defines partial custom weekday input as a complete selection, while preserving the prior defaults or existing selection when no weekday is supplied. The merge and CI support the scoped change; they do not establish how many users encountered it, independent production measurements, or the absence of other scheduling defects. AI assistance was used in preparing the contribution and review; authorship, review provenance and merge are distinguishable in the linked record.

The general lesson is to test both **explicit replacement** and **omission** when a partial API payload is combined with defaults. A fix for one payload can silently break compatibility for another that produces the same effective configuration.
