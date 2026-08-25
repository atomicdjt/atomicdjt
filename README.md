# David Turner

**Independent Applied-AI & Workflow Builder**

I build local-first tools, deterministic AI-assisted workflows, and technical systems with an emphasis on **inspectability, reproducibility, human review, and honest failure boundaries**.

**[Portfolio](https://ai-project-portfolio-portfolio-hub.vercel.app/) · [Writing](writing/your-ai-agent-finished-the-task.md) · [LinkedIn](https://www.linkedin.com/in/david-turner-6052491a2) · [Email](mailto:davidelsey9513@gmail.com)**

## Start here

| Project | What it demonstrates | Try / inspect |
| --- | --- | --- |
| **[Validation Ledger](https://ai-project-portfolio-portfolio-hub.vercel.app/projects/validation-ledger)** | Local-first customer evidence → hypothesis → decision traceability, explicit counterevidence, inspectable scoring | [Source](https://github.com/atomicdjt/validation-ledger) · [Live demo](https://validation-ledger.vercel.app/) · [Challenge the evidence model](https://github.com/atomicdjt/validation-ledger/issues/10) |
| **[Agent Session Bridge](https://ai-project-portfolio-portfolio-hub.vercel.app/projects/agent-session-bridge)** | ATIF v1.7 coding-agent trajectory interchange, namespaced fidelity/loss accounting, Claude Code normalization, explicit target-resumption boundaries | [Source](https://github.com/atomicdjt/agent-session-bridge) · [Contributor issues](https://github.com/atomicdjt/agent-session-bridge/issues) |
| **[BuildWorld AI](https://ai-project-portfolio-portfolio-hub.vercel.app/projects/buildworld-ai)** | Deterministic graph simulation, cascades, reproducibility metadata, stability heuristics | [Source](https://github.com/atomicdjt/buildworld-ai) · [Live demo](https://buildworld-ai-v01-improvements.vercel.app/) · [Challenge the visualization/model boundary](https://github.com/atomicdjt/buildworld-ai/issues/16) |
| **[WeaveStudio](https://ai-project-portfolio-portfolio-hub.vercel.app/projects/weavestudio)** | Local-first visual workflows, claim-to-source provenance, human review gates, portable project exports | [Source](https://github.com/atomicdjt/weavestudio) · [Live demo](https://weavestudio-nine.vercel.app/) · [Candid feedback](https://github.com/atomicdjt/weavestudio/issues/21) |

Commercial work also includes **[QuoteForge Local](https://quoteforge-local.vercel.app/)**, a white-label quote-calculator package for agencies and local-service implementers.

## Featured writing

- **[Your AI Agent Finished the Task. What Did It Actually Prove?](writing/your-ai-agent-finished-the-task.md)** — a practical framework for separating artifact, behavioral, state/provenance, boundary, and independent evidence when AI agents do technical work. The article uses concrete cases where a green or apparently complete state was still narrower than the claim that mattered.

---

## External technical validation

I contribute focused fixes and technical analysis upstream when the work intersects with established projects. These are public evidence artifacts, **not blanket endorsements**.

### Merged upstream

- **[Grid Dynamics Rosetta PR #299](https://github.com/griddynamics/rosetta/pull/299)** — expanded a dangerous-action guard to catch equivalent `git branch` force-delete forms while preserving safe commands. A maintainer independently stress-tested the change with a hand-built matrix, randomized differential fuzzing, real Git execution, the repository test suite, and mutation testing before approving and merging it.
- **[Rosetta PR #319](https://github.com/griddynamics/rosetta/pull/319)** — hardened dataset lookup ambiguity and removed obsolete authorization behavior after review showed the originally targeted `team` policy was dead code. Requested code/documentation corrections were addressed, the final head was re-verified and approved, and the PR merged upstream on August 24, 2026.
- **[Rosetta PR #320](https://github.com/griddynamics/rosetta/pull/320)** — removed a quadratic dangerous-command matcher path. A maintainer independently pressure-tested the change across millions of inputs, reproduced the performance improvement, requested targeted regressions/invariant comments, then re-verified and approved the corrected head before merge on August 24, 2026.
- **[Rosetta PR #322](https://github.com/griddynamics/rosetta/pull/322)** — added focused CLI regression coverage for dataset-name resolution. After review identified two test-fixture gaps, both were corrected and mutation-checked; the contribution was approved and merged on August 24, 2026.
- **[Super Productivity PR #9619](https://github.com/super-productivity/super-productivity/pull/9619)** — keeps section-visible task ordering synchronized with persistent Move Up/Down/To Top/To Bottom actions using the existing reducer architecture. The contribution was merged upstream on August 21, 2026.

### Reviewed but not merged

- **[OpenClaw PR #125740](https://github.com/openclaw/openclaw/pull/125740)** — addressed Skill Workshop routing-description provenance across persistence, revise/apply behavior, legacy migration, and bounded public/model output. Repository-side automated review found no contributor-facing correctness defect while reserving a compatibility-policy decision for maintainers. The PR was closed on August 20, 2026 without merge or recorded human approval, so I do not present it as accepted upstream.

### External reuse, critique, and collaboration

My public corroboration record separates stronger and weaker signals rather than collapsing them into one “validation” bucket. Examples include:

- an external contributor implementing a falsification technique I proposed in their own conformance suite after it exposed vacuous invariants;
- substantive source-level validation and continued technical discussion in CrewAI;
- owner/contributor architectural follow-up in LangGraph, Kimi CLI, and other agent-development threads;
- preliminary local-first curation review of WeaveStudio;
- specialist graph-visualization critique of BuildWorld AI with permission to attribute the feedback publicly.

**[Review the conservative external-corroboration record](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/discovery/external-corroboration.md)**

---

## What the portfolio demonstrates

- **Problem framing** — explicit users, constraints, non-goals, acceptance criteria, and failure boundaries before implementation.
- **Systems thinking** — dependencies, state transitions, bottlenecks, reversibility, provenance, and evidence boundaries.
- **Applied-AI judgment** — deterministic logic where determinism is useful; optional model assistance where it adds value; human review where generated output could mislead.
- **QA / verification** — regression tests, adversarial cases, reproducible issue reports, CI evidence, accessibility checks, and release gates.
- **Technical operations** — audit records, runbooks, source authority, deployment provenance, exports, SOPs, and implementation documentation.
- **Product execution** — concept → implementation → validation → deployment → critique → iteration.
- **Claim discipline** — clear distinctions between implemented, tested, deployed, experimental, externally reviewed, pending, and independently adopted behavior.

## Core tools and methods

**Technologies:** React · TypeScript · Vite · Next.js · Python · Pydantic · IndexedDB · localStorage · Zod · Vitest · Playwright · Canvas/SVG

**Methods:** local-first design · deterministic workflows · structured exports · CI verification · regression testing · technical documentation · human-in-the-loop AI · provenance/loss accounting

---

## AI-assisted authorship

This is an **AI-assisted portfolio**. I direct product strategy, requirements, workflow design, scope boundaries, acceptance criteria, verification expectations, source authority, and public claims. AI systems assist with implementation, research, debugging, testing, and drafting; I review, revise, reject, validate, and take responsibility for what is published.

Supporting evidence:

- **[Portfolio evidence dossier](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/PORTFOLIO_EVIDENCE.md)**
- **[Technical decisions](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/TECHNICAL_DECISIONS.md)**
- **[Recruiter brief](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/RECRUITER_BRIEF.md)**
- **[External corroboration](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/discovery/external-corroboration.md)**

Commercial availability does not imply verified revenue, customers, active users, purchases, or completed acquisitions. Deterministic scores are heuristics rather than certified predictions. Local-first storage is not automatically encrypted, durable, synchronized, or compliant.

---

## I prefer criticism to generic praise

If you work in software, product discovery, developer tools, technical operations, research, AI-agent infrastructure, or local-first systems, the most useful feedback is specific:

- what breaks;
- what is confusing;
- which assumption is wrong;
- where a model creates false confidence;
- what you would remove;
- or what would stop you from using the work in practice.

Follow the public work here on GitHub or start with the [five-minute portfolio review path](https://ai-project-portfolio-portfolio-hub.vercel.app/review).
