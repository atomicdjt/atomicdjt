# From Claude Code JSONL to ATIF v1.7: What Actually Survives an Agent Handoff?

Coding agents accumulate more state than a chat transcript suggests. A long session can contain user and agent messages, structured tool calls, tool observations, timestamps, provider metadata, workspace context, and records that exist only because one specific runtime needs them.

When that history has to move somewhere else, a prose summary is convenient—but it quietly answers the wrong question. It asks, “What seems important enough to retell?” rather than, “What state was actually preserved, what was transformed, and what was lost?”

That distinction is the reason I built **Agent Session Bridge**.

**[Canonical project overview](https://ai-project-portfolio-portfolio-hub.vercel.app/projects/agent-session-bridge) · [Source](https://github.com/atomicdjt/agent-session-bridge) · [ATIF specification](https://github.com/harbor-framework/harbor/blob/main/rfcs/0001-trajectory-format.md)**

Agent Session Bridge is an MIT-licensed reference implementation that converts supported coding-agent transcripts into the public **Agent Trajectory Interchange Format (ATIF) v1.7**. It does not define a competing interchange standard. Its narrower job is to handle provider-specific parsing, expose conversion fidelity, apply best-effort redaction, and build target-specific mappings without pretending that every target can resume imported history as native state.

## The important boundary: trajectory portability is not session resumption

It is tempting to treat these as the same capability:

```text
source session → portable representation → target session
```

But the last arrow is not guaranteed.

ATIF can give us a structured portable trajectory. It does not define another product's internal conversation database, authorization model, workspace binding, tool-execution policy, or an API for creating resumable historical sessions.

That means there are at least three different claims worth separating:

1. **The source transcript can be parsed.**
2. **The parsed history can be represented faithfully enough in a portable trajectory.**
3. **A target product can ingest that trajectory as native resumable state.**

Agent Session Bridge currently supports the first two for its documented Claude Code subset. For Antigravity, it can produce a reference mapping to an observed derived-log shape, but it does **not** claim native historical-session rehydration because there is no supported ingestion boundary for that operation.

That negative result is useful. It prevents “I generated a target-shaped JSON file” from being upgraded into “the target can resume this session.”

## What survives from the supported Claude Code path

The current Claude Code adapter maps supported source records into an ATIF trajectory and preserves or normalizes several important categories.

### Messages and roles

Supported user and agent text becomes ATIF steps with the corresponding source role and message content.

The point is not to make every provider's event model look identical. The point is to preserve the state for which a defensible mapping exists.

### Timestamps

When the source supplies supported timestamps, they are carried into the trajectory rather than replaced with conversion time.

Conversion provenance is recorded separately. That distinction matters: “when this event happened” and “when I transformed this file” are different facts.

### Tool calls

Supported tool invocations become structured ATIF `tool_calls` with their identifiers, names, and JSON arguments.

Keeping calls structured is much more useful than flattening them into prose such as “the agent ran a command.” A downstream consumer can still inspect which call produced which result.

### Tool results become observations

Claude Code can place `tool_result` content in a later user-side record. ASB normalizes that result into an ATIF observation attached to the originating tool call through `source_call_id`.

This is a transformation, not byte-for-byte preservation, so ASB records it as such.

That distinction is central to the design. A conversion can be semantically useful without being structurally identical to its source. The honest claim is “normalized with an explicit rule,” not “unchanged.”

### Session and agent metadata

Where the source provides a session identifier or source-agent version, those can be represented in the corresponding ATIF trajectory/agent fields.

Provider identity can live in ATIF extension metadata rather than requiring a new proprietary core schema.

## What does not become ATIF core state

A portable format should not be forced to absorb every provider-specific concept.

Agent Session Bridge keeps its own conversion metadata under a single namespace:

```text
extra.agent_session_bridge
```

That extension is currently used for things such as:

- conversion provenance;
- source preservation counts;
- unsupported source-record counts;
- unsupported source-block counts;
- orphaned tool-result counts;
- transformation notes;
- source-derived workspace metadata where appropriate.

Consumers that only care about the ATIF trajectory can ignore this namespace. Consumers that care about how trustworthy the conversion is can inspect it.

That is preferable to quietly smuggling ASB-specific concepts into ATIF core fields.

## Fidelity should be inspectable, not implied

Interchange systems can fail in a particularly dangerous way: they can produce valid output while silently discarding information.

A valid JSON document tells you that the output matches a schema. It does not tell you that the source survived the conversion intact.

ASB therefore treats fidelity accounting as a first-class conversion concern.

For example, a conversion report can distinguish between:

- source records that were preserved;
- tool calls that were preserved;
- observations that were correlated successfully;
- records or blocks that were unsupported;
- tool results that could not be correlated;
- explicit structural transformations.

This does not magically prove perfect fidelity. It makes the claim falsifiable.

If an adapter says it preserved four source records and omitted two unsupported blocks, a reviewer has something concrete to inspect. “Conversion succeeded” is much weaker evidence.

## Why unsupported information should stay unsupported

One of the easiest mistakes in interoperability work is to invent a representation because the target format has no evidenced equivalent.

The current Antigravity reference mapper illustrates the boundary. If an ATIF system message has no evidenced representation in the observed derived-log shape, ASB reports the omission instead of manufacturing a target record type.

That is less convenient than pretending everything mapped perfectly. It is also more useful.

An interoperability layer should not create semantic certainty that neither source nor target supplied.

## Redaction is a safeguard, not a guarantee

Coding-agent transcripts can contain credentials, filesystem paths, private source, personal information, or proprietary context.

ASB includes heuristic secret redaction before export. The word **heuristic** matters.

A redacted trajectory still requires human review before publication or transfer into an environment with a different trust boundary. Redaction should reduce obvious exposure risk, not be treated as proof that a transcript is safe to disclose.

The same applies to workspace metadata. For example, redacted output deliberately avoids carrying a workspace current-working-directory value that could expose local path information.

## Historical observability has another truth boundary

Agent Session Bridge also includes an optional downstream projection from ATIF into OpenTelemetry/OpenInference-style observability.

That creates another opportunity to overclaim.

A historical transcript can establish that an event occurred and may preserve a source timestamp. It does not necessarily contain the same timing information that would have been measured by live runtime instrumentation.

So the observability path is described as a **historical structural projection**, not original runtime telemetry.

Where independent completion timing is unavailable, the projection should not invent measured duration. Provenance about where a timestamp came from is more important than producing a visually satisfying trace.

That principle generalizes beyond observability: missing evidence should stay missing.

## The migration from ASEF was intentionally breaking

The first Agent Session Bridge prototype used a project-specific schema called ASEF. Version 0.2 deliberately replaced that output with ATIF rather than trying to establish another canonical ecosystem format.

Old `*.asef.json` files are not ATIF documents and should not be renamed to look like them. The supported migration is to regenerate an ATIF trajectory from the original source transcript and inspect the resulting fidelity report.

This matters for authority as well as engineering. Interoperability becomes harder when every tool invents a “universal” schema. When a public format already covers the portable trajectory layer, an adapter project can add value by implementing, testing, and challenging that format instead of competing with it unnecessarily.

## A useful handoff test

For any proposed coding-agent handoff, I now think the most useful review is to ask four separate questions:

### 1. What source state was observed?

List the actual source structures. Do not begin with what the target happens to support.

### 2. What was preserved versus transformed?

A tool result moved from a provider-specific user block into a call-correlated ATIF observation is transformed but still potentially faithful. Label that transformation.

### 3. What was lost or unsupported?

Make omissions countable and visible. Do not collapse them into a generic success state.

### 4. What can the target genuinely ingest?

A target-shaped export is not evidence of native import. Look for a documented, supported ingestion boundary before claiming resumption.

Those four questions produce a much more defensible statement than “the agents are interoperable.”

## What I want challenged

The most valuable next step for Agent Session Bridge is not generic promotion. It is falsification.

Useful critiques include:

- a Claude Code source construct the current adapter incorrectly classifies as preserved;
- a tool-result correlation case that produces misleading ATIF;
- provider state that should be considered portable but is currently treated as noise;
- a target with a documented historical import boundary that would make a real native-resumption adapter possible;
- a conformance fixture that exposes a fidelity claim that passes today but should fail;
- observability behavior that makes a historical projection look like measured runtime truth.

The project maintains its current mapping and boundary documentation in the source repository:

- [ATIF interchange and ASB extension profile](https://github.com/atomicdjt/agent-session-bridge/blob/main/docs/FORMAT.md)
- [Architecture](https://github.com/atomicdjt/agent-session-bridge/blob/main/docs/ARCHITECTURE.md)
- [Observability notes](https://github.com/atomicdjt/agent-session-bridge/blob/main/docs/OBSERVABILITY.md)
- [Historical observability write-up](https://github.com/atomicdjt/agent-session-bridge/blob/main/docs/HISTORICAL_OBSERVABILITY_WRITEUP.md)
- [Open contributor issues](https://github.com/atomicdjt/agent-session-bridge/issues)

The broader principle is simple: **portability claims should be proportional to the evidence retained during conversion.**

If a field survived, show how. If it changed shape, document the transform. If it was lost, say so. If the target cannot ingest it, stop at the boundary rather than inventing a success state.
