# AgentMeasure: an attributed inference boundary and a synthetic fixture

Checked October 15, 2026 against the public repository.

AgentMeasure records my contribution to a specific question in agent observability: what can a client-side trace actually establish about a tool result reaching a model?

The distinction is between a framework serializing a result into a request and that result reaching provider inference. A client can record the former. Establishing the latter needs evidence from beyond that client observation point. The same discipline applies to availability and influence: observing a value in context does not by itself establish that the value changed a model's behavior.

## Public attribution

[DR-005 — Evidence-Calibrated Consumption Claims](https://github.com/roy-tong/AgentMeasure/blob/main/design-rationale/DR-005-evidence-calibrated-consumption-claims.md) names David Turner (@atomicdjt) as an external reviewer for independent four-rung convergence and the provider-inference boundary. The document also identifies other reviewers and their distinct contributions. My attribution was recorded in [commit 82968db](https://github.com/roy-tong/AgentMeasure/commit/82968db8c19ffa4d9e6fc2a4aeda6fdcbaf088d3).

That is evidence that the external project incorporated and credited this scoped technical input. It does not establish authorship of the whole rationale or specification, formal standards-body adoption, or endorsement of my other projects.

## A contribution with an inspectable artifact

The project's [inference-boundary aggregation-replay fixture](https://github.com/roy-tong/AgentMeasure/tree/main/conformance/evidence/inference-boundary-aggregation-replay) is attributed to me in its README. It describes a provider-reported count whose source pointer resolves to two equally plausible candidates: a measured counter and a replayed cache record with the same window and count.

The expected behavior is to preserve the unresolved measurement basis. The fixture distinguishes the observed provider output, the derived ambiguity, and an inference the evidence cannot settle. Its forbid list rejects confidently labeling the count as measured or selecting a default basis.

This is a **synthetic conformance fixture**. It is an inspectable example of the boundary and expected handling, rather than a capture of real provider behavior. The public repository establishes the artifact's inclusion and attribution; it does not establish adoption by external users or every consumer's conformance.

## Why it belongs beside the software work

Trajectory Fidelity Bridge reports what a transcript conversion preserves or loses. Validation Ledger keeps conclusions traceable to source evidence. WeaveStudio records claim lineage and review state. This AgentMeasure contribution applies the same question to telemetry: which part of a conclusion does the observable record support?

AI assisted with analysis and drafting in my broader workflow. I directed the scope, reviewed the distinctions and fixture, and take responsibility for the published description of my contribution.
