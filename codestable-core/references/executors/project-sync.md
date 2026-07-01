# Project Sync reference
## Document map

Use this map first, then open only the section needed for the current route:

- Writeback matrix
- Manual sync mode
- Target responsibilities
- Startup checklist
- Architecture rules
- Requirements rules
- Roadmap rules
- Doc-sweep rules
- Audit rules
- Historical integrity
- Output protocol
- Index maintenance contract
- Hard stops

## Writeback matrix

Every review emits:

```text
architecture=<yes/no>, requirements=<yes/no>, roadmap=<yes/no>, compound=<yes/no>, attention=<yes/no>, guides-or-libdoc=<yes/no>
```

`yes` requires a concrete signal and evidence. `no` is valid and often preferred.

## Manual sync mode

`project-sync.manual` is allowed when the user explicitly asks to record or update architecture, requirements, roadmap state, doc-sweep, or audit output. It does not require a current code diff, but it does require a traceable source:

- user explicitly states a current fact or decision;
- code anchors confirm the claim;
- existing design/analysis/roadmap/docs support the change;
- an issue, meeting note, or prompt excerpt is provided;
- a reviewed diff already proved the change.

Manual sync must not be used to silently execute feature work or to write future ideas as current architecture. If the claim is proposed rather than current, mark it as draft/proposed or route to `cs-plan`.

## Target responsibilities

| Target | Write when | Do not write when |
|---|---|---|
| Architecture | Current module boundary, public API, data/state shape, config format, main flow, dependency relation changed; or manual sync records a sourced current architecture fact | local bug, variable rename, internal helper extraction, UI copy, unsourced future idea |
| Requirements | User-visible capability, business rule, success criteria, or capability boundary changed; or manual sync records a sourced business rule | implementation bug fixed without requirement change, internal implementation detail |
| Roadmap | Roadmap item status/scope/dependency/blocker changed; or manual sync updates planning state explicitly | independent small task not tied to roadmap |
| Doc-sweep | User explicitly asks cleanup, or a confirmed anchor fully absorbs/supersedes old specs | normal feature/bug/refactor review |
| Audit | User asks for audit or release gate requires systematic scan | local review closure |



## Startup checklist

1. Read `.codestable/INDEX.md`, `.codestable/attention.md`, and `.codestable/reference/project-knowledge-contract.md`.
2. Determine mode:
   - ordinary review sync: read review output, diff summary, verification evidence, and Writeback Matrix;
   - manual sync: read the explicit user request, target docs, and stated evidence/source.
3. Read the relevant index first (`requirements/VISION.md`, `architecture/ARCHITECTURE.md`, roadmap main doc, or `compound/INDEX.md`), then only the linked current docs needed for this sync; avoid full-document rewrites.
4. For ordinary review sync, confirm behavior/code has passed review. For manual sync, confirm the user supplied a traceable source or code/doc anchor.
5. Check dirty files and exclude unrelated changes.

## Architecture rules

Architecture docs record current structural facts, not wish lists.

A good architecture update includes:

- Status/frontmatter that indicates current/backfill/update as appropriate.
- Terminology and audience.
- Structure and interactions.
- Data/state ownership.
- Key decisions and constraints.
- Code anchors.
- Known boundaries and edge cases.
- Related docs and change log for updates.

Quality checks:

- Can each claim be backed by current code, accepted design, or verified diff?
- Does it describe stable structure rather than one-off implementation notes?
- Are old conflicting current facts updated or marked outdated instead of left ambiguous?
- Are future ideas kept out of architecture unless clearly marked as non-current?

## Requirements rules

Requirements docs describe what users or the system now need/provide, not how implementation happens internally.

A requirement update should include:

- User story or capability statement.
- Why the capability exists.
- Current behavior / success criteria.
- Boundaries, non-goals, and failure modes.
- Relevant acceptance evidence or source feature.
- Status: draft/current/outdated when the repo convention supports it.

Allowed “no requirement” case: a feature may be implementation-only or UI-only without durable requirement impact. Do not invent requirements for every change.

## Roadmap rules

Roadmap sync changes planning state, not current architecture facts.

Rules:

- Feature item starts as `planned`, moves to `in-progress` when execution starts, and becomes `done` only after acceptance.
- Blockers and scope changes must be explicit.
- A child feature closure may update roadmap status without changing requirements/architecture.
- Do not collapse large roadmap items into a single giant feature design.

## Doc-sweep rules

Doc-sweep is cleanup by lifecycle marking, not deletion by default.

Workflow:

1. Determine mode and scope.
2. Build a document inventory.
3. Group candidates by topic / anchor.
4. Mark lifecycle states such as current, absorbed, superseded, outdated, or archive-candidate.
5. Ask for user review before broad changes.
6. Produce a sweep report.

Do not perform doc-sweep as a side effect of normal review.

## Audit rules

Audit is proactive maintenance and must not silently enter the current feature scope.

Audit output separates:

- Confirmed issue.
- Risk.
- Observation.
- False positive / dismissed candidate.

Each finding should include evidence, impact, suggested action, and confidence/severity. Common dimensions: correctness, security, performance, reliability, maintainability, test coverage, docs drift.

## Historical integrity

- Do not rewrite approved design, analysis, or roadmap history to make the final state look inevitable.
- Put execution deviations in acceptance/fix-note/apply-notes.
- Put current fact changes in architecture/requirements.
- Put planning state changes in roadmap.

## Output protocol

```text
Project Sync: updated | no-sync | blocked
Mode: ordinary-review | manual
Updated: <paths or none>
Index Sync: <root/index paths updated, no-change, or blocked>
Reason: <yes/no decision for each target>
Evidence: <diff/tests/docs read, or manual source/code anchors>
Next: commit | review | ask-user | stop
```

## Index maintenance contract

Project Sync updates durable project facts. Every durable write must keep indexes fresh:

| Durable write | Required index check |
|---|---|
| New/changed architecture detail | Update `architecture/ARCHITECTURE.md`; update `.codestable/INDEX.md` if a major module/boundary changed |
| New/changed requirement detail | Update `requirements/VISION.md`; update `.codestable/INDEX.md` if a major capability changed |
| Roadmap item/status change | Update roadmap main doc and items yaml; update `.codestable/INDEX.md` if roadmap visibility changed |
| Doc-sweep/audit result that marks docs absorbed/superseded | Update affected indexes or mark stale links |

Rules:

- Update the authoritative detail doc first. Update the corresponding index in the same turn.
- Detail first, index second. Never add an index entry that points to a missing detail doc.
- Index entries should be short: topic, current status, one-line summary, link, last updated.
- If the detail changed but index text remains accurate, report `Index Sync: no-change` with the reason.
- `cs-review` output must include `Index Sync` whenever Project Sync writes or explicitly decides not to write.

## Hard stops

- Ordinary review sync without verification evidence for the underlying change.
- Manual sync without a traceable source, user decision, or code/doc anchor.
- Broad rewrite of long-lived docs without a concrete sync signal.
- Future plan written as current architecture.
- Implementation details written as requirements.
- Unrelated dirty files included in sync.
