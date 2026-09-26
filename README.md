<div align="center">

<img src="./assets/profile-hero.svg" alt="David Turner — systems, verification, and AI-assisted engineering" width="100%" />

<br />

<a href="https://ai-project-portfolio-portfolio-hub.vercel.app/"><img src="https://img.shields.io/badge/PORTFOLIO-LIVE-0ea5e9?style=for-the-badge&logo=vercel&logoColor=white" alt="Portfolio" /></a>
<a href="https://www.linkedin.com/in/david-turner-6052491a2"><img src="https://img.shields.io/badge/LINKEDIN-DAVID%20TURNER-2563eb?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="https://github.com/atomicdjt"><img src="https://img.shields.io/badge/GITHUB-ATOMICDJT-111827?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
<a href="mailto:davidelsey9513@gmail.com"><img src="https://img.shields.io/badge/EMAIL-CONTACT-7c3aed?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>

</div>

## Engineering profile

I build **inspectable software systems** and contribute correctness, security, and performance improvements to established open-source codebases. My work emphasizes **explicit assumptions, reproducible verification, provenance, failure boundaries, and claims that stay inside the evidence**.

The strongest external proof is upstream review: **5 merged contributions across Grid Dynamics Rosetta and super-productivity**, including an **O(n²) → O(n)** improvement in a security-critical matcher that reviewers independently reproduced and differentially checked at scale.

<img src="./assets/evidence-dashboard.svg" alt="Engineering evidence dashboard" width="100%" />

### Technical focus

<p>
  <img src="https://img.shields.io/badge/Verification-Evidence%20First-0284c7?style=flat-square" alt="Verification" />
  <img src="https://img.shields.io/badge/Provenance-Traceable-2563eb?style=flat-square" alt="Provenance" />
  <img src="https://img.shields.io/badge/Local--First-Inspectable-7c3aed?style=flat-square" alt="Local-first" />
  <img src="https://img.shields.io/badge/Agent%20Interoperability-ATIF%201.7-4f46e5?style=flat-square" alt="ATIF 1.7" />
  <img src="https://img.shields.io/badge/Open%20Source-Upstream%20Review-0891b2?style=flat-square" alt="Open source" />
</p>

I tend to work where software needs more than a plausible demo: **state integrity, evidence chains, normalization, differential testing, deterministic simulation, explicit limitations, and reviewable technical decisions**.

## Featured systems

<table>
<tr>
<td width="50%" valign="top">

### Agent Session Bridge

Provider-neutral trajectory portability for coding agents using **ATIF v1.7**, with explicit fidelity/loss accounting, Claude Code normalization, OpenInference projection, and boundaries around what portable trajectories cannot preserve.

**Stack:** Python 3.11+, Pydantic, pytest, mypy, Ruff, OpenTelemetry/OpenInference

[Source](https://github.com/atomicdjt/agent-session-bridge) · [Issues](https://github.com/atomicdjt/agent-session-bridge/issues)

</td>
<td width="50%" valign="top">

### Validation Ledger

A local-first workspace for evidence → hypothesis → decision traceability, explicit counterevidence, inspectable scoring, and differential checks against an independent oracle.

**Stack:** TypeScript, React, Dexie/IndexedDB, Vitest, Playwright, axe-core

[Source](https://github.com/atomicdjt/validation-ledger) · [Live demo](https://validation-ledger.vercel.app/)

</td>
</tr>
<tr>
<td width="50%" valign="top">

### WeaveStudio

Local-first visual workflows with claim-to-source provenance, human review gates, portable exports, browser verification, and buyer-package validation.

**Stack:** TypeScript, React, XYFlow, Vitest, Playwright, jsPDF

[Source](https://github.com/atomicdjt/weavestudio) · [Live demo](https://weavestudio-nine.vercel.app/)

</td>
<td width="50%" valign="top">

### BuildWorld AI

Deterministic graph simulation for cascade analysis, sensitivity, reproducibility metadata, stability heuristics, and exportable scenario reports.

**Stack:** TypeScript, React, Vitest, Playwright, Vite

[Source](https://github.com/atomicdjt/buildworld-ai) · [Live demo](https://buildworld-ai-v01-improvements.vercel.app/)

</td>
</tr>
</table>

## Upstream engineering

| PR | Project | Change | External result |
| --- | --- | --- | --- |
| [#320](https://github.com/griddynamics/rosetta/pull/320) | Grid Dynamics Rosetta | Replaced quadratic backtracking in the dangerous-command matcher | **Merged** after independent equivalence, scaling, and mutation checks |
| [#319](https://github.com/griddynamics/rosetta/pull/319) | Grid Dynamics Rosetta | Removed unreachable team-authorization behavior and hardened dataset lookup | **Merged** after substantive review and correction |
| [#322](https://github.com/griddynamics/rosetta/pull/322) | Grid Dynamics Rosetta | Added CLI regression coverage for dataset-name resolution branches | **Merged** after fixture gaps were found and corrected |
| [#299](https://github.com/griddynamics/rosetta/pull/299) | Grid Dynamics Rosetta | Extended a dangerous-action guard to equivalent force-delete forms | **Merged** |
| [#9619](https://github.com/johannesjo/super-productivity/pull/9619) | super-productivity | Kept visible task order synchronized with persistent movement actions | **Merged** |

**Why Rosetta #320 is the clearest proof point:** a reviewer independently checked equivalence across roughly **5.5 million inputs**, then re-verified the corrected head across **1.6+ million differential cases** after review changes. The review also reproduced the O(n²) → O(n) scaling and mutation-checked the verification harness.

[Read the external validation case study →](writing/external-validation-upstream-review.md)

> Transparency note: [OpenClaw #125740](https://github.com/openclaw/openclaw/pull/125740) was closed without merge or recorded human approval. I do not present it as accepted upstream work.

## How I work

<img src="./assets/verification-workflow.svg" alt="Verification-oriented engineering workflow" width="100%" />

The recurring pattern is simple: define what must remain true, make the smallest defensible change, build checks that can falsify the claim, invite review, and narrow the final claim to what survives.

## Tooling represented in the work

<p>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=111827" alt="React" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite" />
  <img src="https://img.shields.io/badge/Vitest-6E9F18?style=for-the-badge&logo=vitest&logoColor=white" alt="Vitest" />
  <img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright" />
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic" />
  <img src="https://img.shields.io/badge/OpenTelemetry-000000?style=for-the-badge&logo=opentelemetry&logoColor=white" alt="OpenTelemetry" />
</p>

## Selected technical writing

| Piece | Focus |
| --- | --- |
| [External validation: what upstream review actually established](writing/external-validation-upstream-review.md) | A compact evidence record for merged Rosetta and super-productivity contributions |
| [From Claude Code JSONL to ATIF v1.7: what actually survives an agent handoff?](writing/from-claude-code-jsonl-to-atif-v1-7.md) | Trajectory portability, fidelity/loss accounting, and the boundary between interchange and native session resumption |
| [Your AI agent finished the task. What did it actually prove?](writing/your-ai-agent-finished-the-task.md) | Artifact, behavioral, provenance, boundary, and independent evidence |
| [Pull request descriptions that survive review](writing/pull-request-descriptions-that-survive-review.md) | PR structure designed to make assumptions, verification, and limitations inspectable |

## AI-assisted authorship

This is an **AI-assisted portfolio**. I direct product strategy, requirements, scope boundaries, acceptance criteria, verification expectations, and public claims. AI systems assist with implementation, research, debugging, testing, and drafting; I review, revise, reject, validate, and take responsibility for what is published.

Commercial availability does not imply verified revenue, customers, active users, or completed acquisitions. Deterministic scores are heuristics, not certified predictions. Local-first storage is not automatically encrypted, durable, synchronized, or compliant.

## Criticism is useful when it is specific

If you find a broken assumption, weak verification step, misleading claim, confusing interface, or a simpler design, **open an issue**. Specific technical criticism is more valuable than generic praise.

<div align="center">

### Explore the work

[**Portfolio**](https://ai-project-portfolio-portfolio-hub.vercel.app/) · [**Repositories**](https://github.com/atomicdjt?tab=repositories) · [**Writing**](writing/) · [**LinkedIn**](https://www.linkedin.com/in/david-turner-6052491a2) · [**Email**](mailto:davidelsey9513@gmail.com)

<sub>Built around a simple rule: make the evidence easier to inspect than the claim is to repeat.</sub>

</div>