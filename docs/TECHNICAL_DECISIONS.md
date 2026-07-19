# Technical Decisions and Engineering Judgment

This document explains selected architecture decisions, alternatives, tradeoffs, and evidence boundaries. It is designed for technical interviews and serious portfolio review.

## BuildWorld AI: deterministic systems simulation

### Problem

Create a visual environment where a reviewer can model connected systems, run scenarios, inspect bottlenecks and cascades, compare interventions, and export understandable reports without requiring a paid AI service.

### Decision 1: represent systems as typed graphs

**Choice:** Nodes represent assets, populations, resources, facilities, or process stages. Edges represent flow, dependency, mobility, transmission, predation, or resource transfer.

**Why:** Graphs make structure explicit. They allow the same interaction model to support traffic, supply chains, power systems, ecosystems, warehouses, population spread, and emergency resource networks.

**Alternative considered:** A separate data model and UI for every domain.

**Tradeoff:** A common graph abstraction improves reuse and comparison but necessarily simplifies domain-specific reality. The product therefore presents educational heuristics rather than certified predictions.

### Decision 2: use deterministic engines instead of an LLM as the analytical core

**Choice:** Simulation ticks, SSI scoring, cascade analysis, optimization suggestions, and explanatory insights are generated from explicit local logic.

**Why:**

- identical inputs can be reproduced;
- reports can record model version, seed, and input fingerprint;
- the product works without credentials or usage charges;
- findings are easier to test and explain;
- provider availability cannot silently change the core result.

**Alternative considered:** Send the graph to a large language model and ask for analysis.

**Tradeoff:** Deterministic logic is more bounded and requires explicit model design. It does not provide the breadth or linguistic flexibility of a general LLM, but it is more defensible for reproducible portfolio evidence.

### Decision 3: separate simulation modules by responsibility

The architecture isolates:

- tick execution and bounded history;
- cascade stress experiments;
- SSI component scoring;
- ranked intervention suggestions;
- deterministic explanations;
- report generation;
- import/export validation;
- built-in templates.

**Why:** Pure modules can be tested independently and reused by UI, reports, or a future service layer.

**Alternative considered:** Keep all logic inside React components.

**Tradeoff:** More files and types create up-front structure, but reduce coupling and make behavioral testing practical.

### Decision 4: use local-first persistence

**Choice:** Project JSON is stored in browser local storage and can be exported/imported.

**Why:** It avoids unnecessary accounts, servers, secret management, and external data transfer for an educational application.

**Tradeoff:** Browser storage is not encrypted, is not durable across device loss or cleared browser data, and does not support collaboration. The product states those boundaries rather than presenting local storage as enterprise persistence.

### Decision 5: bound the engine to educational graph sizes

**Choice:** The current design targets dozens of nodes and hundreds of ticks, with bounded history.

**Why:** This keeps a static browser application responsive and understandable.

**Future threshold:** Larger graphs should move tick execution to a Web Worker and virtualize rendering rather than simply increasing limits in the main thread.

### Verification

The standalone repository documents:

```text
npm run lint
npm run typecheck
npm run test
npm run build
```

Vitest covers simulation behavior, SSI scoring, cascade analysis, optimizer output, reporting, and import/export validation. Passing tests demonstrate the specified implementation behavior; they do not establish real-world predictive validity.

## ProcessHarbor: deterministic operations workflow with an optional service boundary

### Problem

Operations knowledge is often fragmented across notes, policies, tickets, onboarding material, and undocumented practice. A useful tool must structure that material without pretending generated drafts are authoritative records.

### Decision 1: make the default workflow deterministic and local

The public workflow can transform sample or user-provided notes into SOPs, onboarding checklists, knowledge-base drafts, gap findings, version records, audit activity, and exports without requiring an external AI provider.

**Why:** Reviewers can inspect the complete workflow without secrets, account setup, provider cost, or nondeterministic output.

### Decision 2: design optional AI as a guarded adapter

The reference service layer uses typed contracts, Zod validation, role-aware checks, strict structured output, rate limiting, and deterministic fallback.

**Why:** Provider output is treated as untrusted input. It must satisfy the product schema before saving.

**Boundary:** Server routes and provider-backed behavior are not described as live until functions, configuration, validation, fallback, and security controls are verified on a preview environment.

### Decision 3: include a production migration path without claiming production completion

The source includes a Postgres-compatible schema and route contracts for organizations, users, documents, versions, training items, knowledge articles, gaps, and audit events.

**Why:** This demonstrates an architectural path beyond the demo while keeping the public claim accurate: the current browser experience is local, and the service repository is a reference implementation.

## WeaveStudio: portable human-reviewed workflow product

### Key decisions

- **Portable JSON projects:** avoids lock-in and supports backup, restore, and transfer.
- **Snapshots plus undo/redo:** supports reversible editing rather than destructive automation.
- **Consent-gated provider actions:** external requests happen only when the user initiates them.
- **Volatile API-key handling:** provider keys remain in tab memory and are excluded from exports.
- **Review-before-apply:** AI output is proposed rather than silently committed.
- **Buyer documentation:** architecture, maintenance, feature reality, transfer checklist, and operating plan are treated as part of the product.

## QuoteForge Local: productized implementation rather than managed SaaS

### Key decisions

- **Template-driven calculators:** one typed engine can support multiple service categories.
- **Embeddable route and WordPress wrapper:** meets buyers where they already deploy client sites.
- **Clear infrastructure boundary:** browser demo storage is separated from optional real lead delivery.
- **Private source with public proof:** protects commercial assets while exposing enough documentation for evaluation.
- **Explicit non-goals:** not presented as a CRM, invoicing system, scheduling platform, or guaranteed lead-generation service.

## Cross-project operating principles

1. Prefer deterministic behavior where reproducibility matters.
2. Keep external AI optional and visible.
3. Treat generated output as a draft requiring review.
4. Preserve user portability through export and restore.
5. Separate implemented behavior from roadmap architecture.
6. Document the weakest important boundary, not only the strongest feature.
7. Use tests and builds as evidence of execution, not as proof of security or real-world correctness.
