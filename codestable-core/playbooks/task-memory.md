# Task memory playbook
## Document map

Use this map first, then open only the section needed:

- Purpose
- Task capsule
- When to create one
- Context pack rules
- Audit ledger rules
- Proof trace rules
- Journal rules
- Finish rules
- Output fields
- Hard stops

## Purpose

CodeStable borrows Trellis' task-centered memory: every non-trivial unit of work should carry a small, reviewable context pack and journal so the next AI session does not start from scratch.

Owned by: `cs-plan` creates or refreshes; `cs-do` appends evidence; `cs-review` finishes and promotes durable learnings.

## Task capsule

A task capsule links the lifecycle artifact to the code/document facts used for this task:

```text
.codestable/tasks/YYYY-MM-DD-{slug}/
├── task.md          # goal, non-goals, owner decisions, linked feature/issue/refactor/roadmap
├── context-pack.md  # curated links, not a dump
├── audit-ledger.md  # optional audit-only file-level backend ledger
├── journal.md       # session-to-session progress and blockers
├── proof.md         # contract, before/after evidence, checks, writeback
└── status.yaml      # planned | ready | in-progress | review | done | blocked
```

Feature/issue/refactor/roadmap artifacts remain the canonical lifecycle artifacts. The task capsule is the cross-session memory and context injection layer.

## When to create one

Create or refresh a task capsule for:

- standard feature / issue / refactor / roadmap work;
- fastforward work expected to span sessions;
- doc-sweep or knowledge-refresh work with many documents;
- audit-only backend chain reviews that produce a file-level ledger;
- any task where the next session would otherwise need to reconstruct context.

Do not create one for `intro.only`, `onboard.status`, a one-turn code explanation, or a trivial fastforward completed immediately.

## Context pack rules

`context-pack.md` is curated. It contains:

- user goal and non-goals;
- linked lifecycle artifact paths;
- relevant architecture / requirements / compound / roadmap links;
- current code anchors and tests;
- owner decisions and open questions;
- minimality/reuse targets;
- forbidden paths or changes;
- completed audit ledger path and audit status when audit-only was required.

Do not paste whole files. Link paths and short summaries; open detail docs only when the current step needs them.

## Audit ledger rules

`audit-ledger.md` is allowed only for `audit-only.backend-ledger` or a task that explicitly requires a completed audit before execution. It records file-level findings and must use the minimum ledger fields from `audit-only.md`.

Rules:

- Do not paste full source files; cite paths, functions, fields, callers, consumers, and short evidence notes.
- The ledger must state `Audit Status: 已审完` or `Audit Status: 未审完`.
- A ledger with any `审计状态: partial` row cannot make the task ready for `cs-do`.
- Risks stay as findings until a later `cs-do` run implements a bounded fix item.

## Proof trace rules

`proof.md` records the evidence required to trust a real-repo change. Create it for standard tasks, bug fixes, risky refactors, and doc-sweeps. Keep it compact and update it as evidence changes.

Minimum fields: contract, before-change evidence, change evidence, validation evidence, knowledge freshness, and uncovered risk. See `reliability.md`.

## Journal rules

`journal.md` is append-only per session or meaningful step:

```markdown
## YYYY-MM-DD HH:MM — cs-do
- Did: ...
- Evidence: ...
- Checks: ...
- Blockers / decisions needed: ...
- Next suggested route: ...
```

Do not rewrite earlier journal entries except to fix a factual typo with a dated correction.

## Finish rules

During `cs-review`, finish means:

1. Verify the diff/artifact/checks.
2. Update task `status.yaml`.
3. Add a final journal entry.
4. Promote only durable facts to architecture/requirements/compound/attention/roadmap.
5. Keep ephemeral debugging notes in the task journal, not global docs.

## Output fields

Public entries include these lines when a task capsule is relevant:

```text
Task Memory: none | create:<path> | update:<path> | finish:<path>
Context Pack: <path or none>
Proof Trace: none | create:<path> | update:<path> | finish:<path>
Audit Ledger: not-applicable | missing | inline | create:<path> | update:<path> | read:<path> | complete:<path> | partial:<path>
Journal: <path or none>
```

## Hard stops

- Treating task memory as another place to dump full files.
- Promoting ephemeral attempts into durable architecture/requirements.
- Continuing a task without reading its context pack when it exists.
- Implementing audit-required work without reading a completed audit ledger.
- Marking a task done while review evidence is missing.
- Skipping proof trace for non-trivial code or doc-sweep work.
