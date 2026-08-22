# David Turner

**Independent Applied-AI & Workflow Builder**

I build local-first tools, deterministic AI-assisted workflows, and technical systems with an emphasis on **inspectability, reproducibility, human review, and honest failure boundaries**.

**[Portfolio](https://ai-project-portfolio-portfolio-hub.vercel.app/) · [LinkedIn](https://www.linkedin.com/in/david-turner-6052491a2) · [Email](mailto:davidelsey9513@gmail.com)**

## Start here

| Project | What it demonstrates | Try / inspect |
| --- | --- | --- |
| **[Validation Ledger](https://github.com/atomicdjt/validation-ledger)** | Local-first customer evidence → hypothesis → decision traceability, explicit counterevidence, inspectable scoring | [Live demo](https://validation-ledger.vercel.app/) · [Challenge the evidence model](https://github.com/atomicdjt/validation-ledger/issues/10) |
| **[Agent Session Bridge](https://github.com/atomicdjt/agent-session-bridge)** | Provider-neutral coding-agent session exchange, ASEF canonicalization, fidelity/loss accounting, Claude Code import | [Repository](https://github.com/atomicdjt/agent-session-bridge) · [Contributor issues](https://github.com/atomicdjt/agent-session-bridge/issues) |
| **[BuildWorld AI](https://github.com/atomicdjt/buildworld-ai)** | Deterministic graph simulation, cascades, reproducibility metadata, stability heuristics | [Live demo](https://buildworld-ai-v01-improvements.vercel.app/) · [Challenge the visualization/model boundary](https://github.com/atomicdjt/buildworld-ai/issues/16) |
| **[WeaveStudio](https://github.com/atomicdjt/weavestudio)** | Local-first visual workflows, claim-to-source provenance, human review gates, portable project exports | [Live demo](https://weavestudio-nine.vercel.app/) · [Candid feedback](https://github.com/atomicdjt/weavestudio/issues/21) |

Commercial work also includes **[QuoteForge Local](https://quoteforge-local.vercel.app/)**, a white-label quote-calculator package for agencies and local-service implementers.

---

## External technical validation

I contribute focused fixes and technical analysis upstream when the work intersects with established projects. These are public evidence artifacts, **not blanket endorsements**.

### Merged upstream

- **[Grid Dynamics Rosetta PR #299](https://github.com/griddynamics/rosetta/pull/299)** — expanded a dangerous-action guard to catch equivalent `git branch` force-delete forms while preserving safe commands. A maintainer independently stress-tested the change with a hand-built matrix, randomized differential fuzzing, real Git execution, the repository test suite, and mutation testing before approving and merging it.

### Independently pressure-tested / under review

- **[Rosetta PR #319](https://github.com/griddynamics/rosetta/pull/319)** — dataset lookup ambiguity hardening plus authorization cleanup. Independent review reproduced validation, ran multiple refutation attempts, validated the live-path ambiguity fix, and requested a legitimate scope correction to remove obsolete authorization behavior.
- **[Rosetta PR #320](https://github.com/griddynamics/rosetta/pull/320)** — removes a quadratic dangerous-command matcher path. Independent review compared millions of generated inputs with zero divergence and reproduced the O(n²) → approximately linear performance improvement before requesting additional cross-line coverage/comments.
- **[OpenClaw PR #125740](https://github.com/openclaw/openclaw/pull/125740)** — repairs Skill Workshop routing-description provenance across persistence, revise/apply behavior, legacy migration, and bounded public/model output. Repository-side review found no contributor-facing correctness defect while reserving a compatibility-policy decision for maintainers.
- **[Super Productivity PR #9619](https://github.com/super-productivity/super-productivity/pull/9619)** — keeps section task ordering consistent with persistent move actions using the existing reducer architecture.

### External reuse, critique, and collaboration

My public corroboration record also separates stronger and weaker signals rather than collapsing them into one “validation” bucket. Examples include:

- an external contributor implementing a falsification technique I proposed in their own conformance suite after it exposed vacuous invariants;
- substantive source-level validation and continued technical discussion in CrewAI;
- owner/contributor architectural follow-up in LangGraph, Kimi CLI, and other agent-development threads;
- preliminary local-first curation review of WeaveStudio;
- specialist graph-visualization critique of BuildWorld AI with permission to attribute the feedback publicly.

**[Review the conservative external-corroboration record](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/external-corroboration.md)**

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
- **[External corroboration](https://github.com/atomicdjt/AI-Project-Portfolio/blob/main/docs/external-corroboration.md)**

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
