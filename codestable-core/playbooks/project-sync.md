# Project Sync playbook
## Document map

Use this map first, then open only the section needed:

- Writeback matrix
- Manual sync mode
- Target responsibilities
- Startup checklist
- Architecture rules
- Requirements rules
- Roadmap rules
- Doc-sweep rules
- Claim matrix format
- Scoped specs and task memory
- Audit rules
- Historical integrity
- Output protocol
- Index maintenance contract
- Hard stops

## Writeback matrix

Every review emits:

```text
architecture=<yes/no>, requirements=<yes/no>, roadmap=<yes/no>, compound=<yes/no>, attention=<yes/no>, guides-or-libdoc=<yes/no>, specs=<yes/no>, task-memory=<yes/no>, doc-sweep=<yes/no>
```

`yes` requires a concrete signal and evidence. `no` is valid and often preferred.

## Manual sync mode

`project-sync.manual` is allowed when the user explicitly asks to record or update architecture, requirements, roadmap state, or audit output. It does not require a current code diff, but it does require a traceable source:

- user explicitly states a current fact or decision;
- code anchors confirm the claim;
- existing design/analysis/roadmap/docs support the change;
- an issue, meeting note, or prompt excerpt is provided;
- a reviewed diff already proved the change.

Doc entropy cleanup uses `project-sync.doc-sweep`, not generic manual sync.

Manual sync must not silently execute feature work or write future ideas as current architecture. If a claim is proposed rather than current, mark it as draft/proposed or route to `cs-plan`.

## Target responsibilities

| Target | Write when | Do not write when |
|---|---|---|
| Architecture | Current module boundary, public API, data/state shape, config format, main flow, dependency relation changed; or manual sync records a sourced current architecture fact | local bug, variable rename, internal helper extraction, UI copy, unsourced future idea |
| Requirements | User-visible capability, business rule, success criteria, or capability boundary changed; or manual sync records a sourced business rule | implementation bug fixed without requirement change, internal implementation detail |
| Roadmap | Roadmap item status/scope/dependency/blocker changed; or manual sync updates planning state explicitly | independent small task not tied to roadmap |
| Specs | Confirmed engineering convention, test command, API/UI/data/security rule, or workflow standard changed | single accidental local style or unconfirmed preference |
| Task memory | Non-trivial task is accepted/blocked/done or needs resumable journal/context updates | one-turn explanation or trivial completed fastforward |
| Doc-sweep | User explicitly asks cleanup, entropy reduction, outdated-doc scan, or a confirmed anchor fully absorbs/supersedes old docs | normal feature/bug/refactor review |
| Audit | User asks for audit or release gate requires systematic scan | local review closure |

## Startup checklist

1. Read `.codestable/INDEX.md`, `.codestable/attention.md`, and `.codestable/reference/project-knowledge-contract.md`.
2. Determine mode:
   - ordinary review sync: read review output, diff summary, verification evidence, and Writeback Matrix;
   - manual sync: read the explicit user request, target docs, and stated evidence/source;
   - doc-sweep: refresh/read code inventory, then inspect relevant docs and indexes.
3. Read the relevant index first (`requirements/VISION.md`, `architecture/ARCHITECTURE.md`, `specs/INDEX.md`, `tasks/INDEX.md`, roadmap main doc, or `compound/INDEX.md`), then only linked docs needed for this sync.
4. For ordinary review sync, confirm behavior/code has passed review. For manual sync, confirm the user supplied a traceable source or code/doc anchor.
5. Check dirty files and exclude unrelated changes.

## Architecture rules

Architecture docs record current structural facts, not wish lists. A good update includes status, terminology, structure and interactions, data/state ownership, decisions, constraints, code anchors, related docs, and change log.

Quality checks:

- Can each claim be backed by current code, accepted design, or verified diff?
- Does it describe stable structure rather than one-off implementation notes?
- Are old conflicting current facts updated or marked outdated instead of left ambiguous?
- Are future ideas kept out of architecture unless clearly marked as non-current?

## Requirements rules

Requirements docs describe what users or the system now need/provide, not how implementation happens internally.

A requirement update should include capability, why it exists, current behavior, success criteria, boundaries, non-goals, failure modes, and source evidence.

Allowed “no requirement” case: a change may be implementation-only or UI-only without durable requirement impact. Do not invent requirements for every change.

## Roadmap rules

Roadmap sync changes planning state, not current architecture facts.

Rules:

- Feature item starts as `planned`, moves to `in-progress` when execution starts, and becomes `done` only after acceptance.
- Blockers and scope changes must be explicit.
- A child feature closure may update roadmap status without changing requirements/architecture.
- Do not collapse large roadmap items into a single giant feature design.

## Doc-sweep rules

Doc-sweep is code-grounded lifecycle maintenance, not deletion by default and not old-doc majority voting.

### Required evidence order

1. Current code/manifests/tests/config.
2. Current `.codestable/INDEX.md` and target indexes.
3. Newer accepted design/acceptance/fix-note/apply-notes.
4. Older docs being evaluated.

If old docs conflict with current code and no current index/doc resolves it, code wins for classification, but the result is `conflicts-with-code` or `needs-review`, not automatic rewrite.

### Workflow

1. **Scope**: define anchor area, e.g. `auth`, `billing`, `router`, `database`, or “entire `.codestable`”.
2. **Refresh inventory**: run/read `.codestable/tools/scan-project.py` output.
3. **Build document inventory**: list relevant `.codestable/**/*.md|yaml|yml`, excluding `.codestable/reference/` and `.codestable/tools/` unless user explicitly audits runtime assets.
4. **Extract claims**: for each candidate, list durable claims: modules, APIs, data shapes, commands, rules, status.
5. **Map claims to anchors**: current code anchor, current index, newer doc, or no evidence.
6. **Classify**:
   - `current`: supported by current code/index/newer accepted doc.
   - `unverified`: no current evidence found.
   - `conflicts-with-code`: current code contradicts the claim.
   - `superseded-by`: a newer accepted doc explicitly replaces it.
   - `archive-candidate`: safe to archive after user confirmation.
7. **Write report**: `.codestable/doc-sweeps/YYYY-MM-DD-{slug}/index.md` with candidate table, evidence, and recommended actions.
8. **Apply only safe lifecycle changes**: update indexes or add status markers when evidence is strong. Do not delete by default.

### Claim matrix format

Every doc-sweep report includes a claim matrix. Minimum columns:

| Document | Claim | Claimed status/date | Current anchor | Anchor type | Classification | Recommended action |
|---|---|---|---|---|---|---|

Current anchors must be one of: code path/line or symbol, manifest/config, test, generated code inventory entry, current index, newer accepted lifecycle artifact, or explicit owner source.

If a claim has no anchor, classify as `unverified`. If current code contradicts it, classify as `conflicts-with-code`. Only `superseded-by` or `archive-candidate` can be proposed for archive/delete, and only after the deletion gate.

### Deletion gate

Deletion requires all of the following:

- user explicitly asks to delete/archive now;
- every file is listed by path before deletion;
- each file has `superseded-by` or `archive-candidate` evidence;
- no current index points to it as authoritative;
- output includes rollback note.

Otherwise ask for confirmation or stop after report.

## Scoped specs and task memory

Update `specs/INDEX.md` or a scoped spec only when a convention is confirmed by current code, tests, CI, README, or explicit owner decision. Do not infer permanent standards from one accidental file.

Finish or update task memory when closing non-trivial work: status first, final journal second, durable knowledge promotion third. Ephemeral debug notes remain in task journal.

## Audit rules

Audit is proactive maintenance and must not silently enter current feature scope. Findings separate confirmed issue, risk, observation, and false positive/dismissed candidate. Each finding includes evidence, impact, suggested action, confidence, and severity.

## Historical integrity

- Do not rewrite approved design, analysis, or roadmap history to make the final state look inevitable.
- Put execution deviations in acceptance/fix-note/apply-notes.
- Put current fact changes in architecture/requirements.
- Put planning state changes in roadmap.
- Put stale-doc lifecycle findings in doc-sweep reports or indexes, not by mutating old artifacts into a fake history.

## Output protocol

```text
Project Sync: updated | no-sync | blocked
Mode: ordinary-review | manual | doc-sweep
Updated: <paths or none>
Index Sync: <root/specs/tasks/index paths updated, no-change, or blocked>
Reason: <yes/no decision for each target>
Evidence: <diff/tests/docs read, manual source, code anchors, inventory path>
Doc-sweep Classification: <counts by current/unverified/conflicts/superseded/archive-candidate or not-applicable>
Claim Matrix: <path or inline table summary>
Next: commit | review | ask-user | stop
```

## Index maintenance contract

Project Sync updates durable project facts. Every durable write must keep indexes fresh:

| Durable write | Required index check |
|---|---|
| New/changed architecture detail | Update `architecture/ARCHITECTURE.md`; update `.codestable/INDEX.md` if a major module/boundary changed |
| New/changed requirement detail | Update `requirements/VISION.md`; update `.codestable/INDEX.md` if a major capability changed |
| Roadmap item/status change | Update roadmap main doc and items yaml; update `.codestable/INDEX.md` if roadmap visibility changed |
| New/changed scoped spec | Update `specs/INDEX.md`; update `.codestable/INDEX.md` only if top-level standards summary changed |
| Task status/finish | Update `tasks/INDEX.md`; update root index only for high-visibility active work changes |
| Doc-sweep result | Update affected indexes or mark stale links; update `.codestable/INDEX.md` only if top-level links/status changed |

Rules: detail first, index second. Never add an index entry that points to a missing detail doc. If detail changed but index text remains accurate, report `Index Sync: no-change` with reason.

## Hard stops

- Ordinary review sync without verification evidence for the underlying change.
- Manual sync without a traceable source, user decision, or code/doc anchor.
- Doc-sweep without code inventory/current anchors.
- Broad deletion or rewrite of docs without explicit confirmation.
- Future plan written as current architecture.
- Implementation details written as requirements.
- Unrelated dirty files included in sync.
