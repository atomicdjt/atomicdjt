# Current work and evidence index

Contribution, open-PR, and publication status checked October 23, 2026. Older project descriptions retain their repository-specific validation dates. This index connects David Turner's public software, accepted external contributions, technical writing, and current local development. Repository source and contribution records are authoritative for the linked claims. A public source repository, a released package, and a deployed demonstration describe different stages of delivery.

## Start here: external evidence and published work

1. **[Nine merged upstream contributions](../writing/external-validation-upstream-review.md):** seven Rosetta changes and two super-productivity fixes. Rosetta #359 is included; its specific review and limits are documented.
2. **[ResearchOps Community publication](https://medium.com/researchops-community/when-research-evidence-stops-surviving-product-decisions-183579089904?postPublishedType=approve-in-publication):** an article accepted and published on Medium on October 22, 2026.
3. **[AgentMeasure contribution](../writing/agentmeasure-inference-boundary.md):** public attribution in DR-005 and an included synthetic conformance fixture.
4. **[Trajectory Fidelity Bridge](https://github.com/atomicdjt/trajectory-fidelity-bridge):** an owned, published Python tool with explicit transformation and loss boundaries.
5. **[Portfolio Hub](https://ai-project-portfolio-portfolio-hub.vercel.app/):** working applications, source links, and review paths.

## Recent verified work (October 16–23, 2026)

GitHub search found **23 authored PRs merged** in this UTC window: 20 in repositories I own and three in other repositories. This is an activity count, not a measure of external endorsement.

- **ResearchOps publication:** [When Research Evidence Stops Surviving Product Decisions](https://medium.com/researchops-community/when-research-evidence-stops-surviving-product-decisions-183579089904?postPublishedType=approve-in-publication) was accepted and published by the ResearchOps Community on Medium on October 22.
- **CrewAI reliability work:** profile-repository PRs [#40](https://github.com/atomicdjt/atomicdjt/pull/40), [#41](https://github.com/atomicdjt/atomicdjt/pull/41), and [#42](https://github.com/atomicdjt/atomicdjt/pull/42), plus recovery-fixture [#1](https://github.com/atomicdjt/crewai-stripe-recovery-fixture/pull/1) and [#2](https://github.com/atomicdjt/crewai-stripe-recovery-fixture/pull/2), add a CrewAI-version-pinned dispatch harness, fault-injected HTTP/SQLite tests, recovery ownership, and evidence safeguards. Fixture #1 reports 20/20 deterministic tests passing on its final head. The independent Patient Agent run cited in that PR was on an earlier pinned head. This work is not an upstream CrewAI patch, a live Stripe test, or an exactly-once guarantee.
- **External repository acceptance:** [Rosetta #359](https://github.com/griddynamics/rosetta/pull/359) merged after maintainer review and is part of the nine-PR upstream record above. [OpenWorldRPG #252](https://github.com/TateParker/OpenWorldRPGUnreal/pull/252) and [#253](https://github.com/TateParker/OpenWorldRPGUnreal/pull/253) were separately merged in a collaborator's repository. #252 reports a UE 5.8.4 build and three focused tests; the PR records the remaining test limits.
- **Other merged repository work:** [Validation Ledger #49](https://github.com/atomicdjt/validation-ledger/pull/49) resolved the production DOMPurify advisory set; [Trajectory Fidelity Bridge #46](https://github.com/atomicdjt/trajectory-fidelity-bridge/pull/46) removed an obsolete Ruff suppression; [QuoteForge #33](https://github.com/atomicdjt/quoteforge-local/pull/33) and [#37](https://github.com/atomicdjt/quoteforge-local/pull/37) addressed dependency and Node 22 type compatibility; [Cosmic Atlas #9](https://github.com/atomicdjt/cosmic-atlas-scientific/pull/9) added a source-backed reviewer guide. Profile and portfolio PRs #39–46 and #169–173 refreshed evidence, attribution, and reviewer navigation.

## Attribution corrections and pending third-party work

**Verified 20 October 2026:** The [canonical attribution/disposition register](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/discovery/external-corroboration.md#attribution-and-disposition-reconciliation--verified-20-october-2026) separates credited work from proposals, independent reports, and other people's results.

- **Not my publication, sign-off, or test run:** the [SCITT/Zenodo report](https://github.com/atomicdjt/AI-Project-Portfolio/issues/144) does not establish my authorship or independent final verification. The October report sign-off and reported digests were supplied by `babyblueviper1`, who also owns the [Vaara #590](https://github.com/vaaraio/vaara/issues/590) conformance result. The separate [delete-the-rule conformance test](https://github.com/babyblueviper1/invinoveritas/commit/be141e8d501d61486fb7a363bee507312ef61162) credits `Rul1an`, not me.
- **Not merged or adopted:** [OpenClaw #125740](https://github.com/openclaw/openclaw/pull/125740) closed without merge; [AgentCI #121](https://github.com/jinngimk-lang/agentci/issues/121) remains `UNVERIFIED / reproducible-candidate`. Neither is counted as a merged external contribution.
- **Directory submissions still open:** [LocalFirstWeb #102](https://github.com/mylofi/localfirstweb.dev/pull/102), [Awesome BYOK #12](https://github.com/yatsyk/awesome-byok-apps/pull/12), and [Awesome Browser-Based Tools #7](https://github.com/ZihangDong/awesome-browser-based-tools/pull/7) are unmerged PRs, not published listings or evidence of usage.
- **Retained legitimate credits:** nine `atomicdjt`-authored merged upstream PRs and the expressly attributed [AgentMeasure reviewer/fixture contribution](../writing/agentmeasure-inference-boundary.md); no authorship of its entire specification or claim of broader adoption.

## Maintained systems

| Work | Source / public surface | Scope and current delivery state |
| --- | --- | --- |
| Trajectory Fidelity Bridge | [Source](https://github.com/atomicdjt/trajectory-fidelity-bridge) · [PyPI](https://pypi.org/project/atomicdjt-trajectory-fidelity-bridge/) | Claude Code JSONL to ATIF v1.7, fidelity accounting, heuristic redaction, and historical observability projection. Interchange does not provide native session resumption. |
| Validation Ledger | [Source](https://github.com/atomicdjt/validation-ledger) · [Demo](https://validation-ledger.vercel.app/) | Local decision governance linking sources, evidence, claims, counterevidence, hypotheses, and decisions. Scores are inspectable heuristics. |
| WeaveStudio | [Source](https://github.com/atomicdjt/weavestudio) · [Demo](https://weavestudio-nine.vercel.app/) | Local workflow composition, source lineage, human review, snapshots, and portable handoffs. Public source is proprietary and provided for evaluation. |
| BuildWorld AI | [Source](https://github.com/atomicdjt/buildworld-ai) · [Demo](https://buildworld-ai-v01-improvements.vercel.app/) | Deterministic graph simulation, cascades, sensitivity, and scenario reports under declared heuristic models. Source visibility uses a portfolio license. |
| Cosmic Atlas Scientific | [Source](https://github.com/atomicdjt/cosmic-atlas-scientific) · [Tagged releases](https://github.com/atomicdjt/cosmic-atlas-scientific/releases) | Main contains v6 scientific-engine work: JPL Horizons/DE441 states, propagation, Lambert exploration, and local HEALPix catalogs. The latest formal release remains v5.1.0. |
| AI Project Portfolio | [Source](https://github.com/atomicdjt/AI-Project-Portfolio) · [Project index](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/PROJECT_INDEX.md) | Eleven configured application workspaces plus supporting case studies and legacy artifacts. The index distinguishes source authority, local services, and deployment boundaries. |
| QuoteForge Local | [Public demonstration](https://quoteforge-local.vercel.app/) | Commercial quote-calculator package with private authoritative source. Packaging and availability do not establish purchases or revenue. |

## Breadth inside the portfolio

The monorepo's configured applications are Portfolio Hub, Astra, Nexus Play, LayerForge Studio, ProcessHarbor, FocusForge, VariantVision Pro, RedactReady Pro, the BuildWorld review copy, RedactReady, and ScamShield AI. BuildWorld's standalone repository is authoritative. Astra and Nexus Play have local service requirements.

Supporting work includes GardenGrid, Mnemosyne, Amino Acid Research Workbench, HearthLink, AI Knowledge Operations Toolkit, Ecology of Consciousness, IHOS, and FrameEcho. Their [project index](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/PROJECT_INDEX.md) and [deployment map](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/deployment-and-previews.md) describe which are maintained applications, research frameworks, concepts, manual deployments, or preserved static demos.

## Work in review

**Status checked October 23, 2026. Ten open PRs are in repositories I own:**

- [CrewAI recovery fixture #3](https://github.com/atomicdjt/crewai-stripe-recovery-fixture/pull/3) — credential-gated Stripe test-mode smoke; live test workflow was skipped because no test secret was configured.
- [Validation Ledger #51](https://github.com/atomicdjt/validation-ledger/pull/51) — development-dependency advisory follow-up; [#47](https://github.com/atomicdjt/validation-ledger/pull/47) — reproducible governance review docs; [#38](https://github.com/atomicdjt/validation-ledger/pull/38) — mixed-evidence demo seed.
- [Trajectory Fidelity Bridge #44](https://github.com/atomicdjt/trajectory-fidelity-bridge/pull/44) — independent converter-review path; [#43](https://github.com/atomicdjt/trajectory-fidelity-bridge/pull/43) — test-only Claude tool-result null/error boundary coverage.
- [WeaveStudio #67](https://github.com/atomicdjt/weavestudio/pull/67) — reviewer workflow docs; [#65](https://github.com/atomicdjt/weavestudio/pull/65) — workspace/deliverable safety changes; [#64](https://github.com/atomicdjt/weavestudio/pull/64) — approval-content attestations.
- [QuoteForge Local #38](https://github.com/atomicdjt/quoteforge-local/pull/38) — purchase/delivery audit and buyer-prospect research; it does not report a completed real purchase or paid order.

These are proposed branch changes, not accepted contributions or canonical releases. The separate [directory submissions](#attribution-corrections-and-pending-third-party-work) remain unmerged and are tracked above.

## Current local development

These are ongoing local projects whose source has not been published to my GitHub account. The summaries are development status, with no public release or independent reproduction claim.

| Work | Current scope |
| --- | --- |
| Aether Browser | An Electron desktop browser prototype exploring browsing, agent execution, permission boundaries, and workflow tools. |
| Autonomous Computational Discovery Lab (ACDL) | A local scientific workbench for bounded materials and molecular calculations, job records, provenance, and replay bundles. Its declared models do not establish experimental accuracy or wet-lab confirmation. |
| RMA Relay | A warranty and service-resolution prototype exploring how voice-agent claims can be checked against evidence before becoming recorded facts. Live service success is a separate validation step. |
| Synchronizing-automata research note | A revised finite computational study with recorded results for 203 parameter values. It does not prove the general conjecture; no public preprint identifier is available at this check. |

## Writing and contribution boundaries

The [profile writing directory](../writing/) is the canonical source for GitHub-hosted technical articles. [When Research Evidence Stops Surviving Product Decisions](https://medium.com/researchops-community/when-research-evidence-stops-surviving-product-decisions-183579089904?postPublishedType=approve-in-publication) was accepted and published in the ResearchOps Community on Medium on October 22, 2026; this index links to the publisher's canonical page rather than duplicating the article. Public forks retain upstream branding and serve contribution work; they are not presented as original systems. Private correspondence and editorial invitations are not used as public endorsements. Broader writing and research drafts remain separate from accepted publications.

This is an AI-assisted body of work. I direct requirements, scope, acceptance criteria, verification expectations, and public claims, and take responsibility for the material I publish.
