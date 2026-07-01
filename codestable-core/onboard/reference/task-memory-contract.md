# Task Memory Contract
## Document map

- Purpose
- Task capsule layout
- Context pack
- Journal
- Finish

## Purpose

Task memory keeps non-trivial work resumable across AI sessions. It is a curated context pack and journal, not a replacement for feature/issue/refactor/roadmap artifacts.

## Task capsule layout

```text
.codestable/tasks/YYYY-MM-DD-{slug}/
├── task.md
├── context-pack.md
├── journal.md
├── proof.md
└── status.yaml
```

## Context pack

Include only high-signal links and short summaries: user goal, non-goals, owner decisions, related project facts, code anchors, tests, reuse targets, and forbidden changes.

## Proof trace

`proof.md` stores the real-repo evidence needed to trust the work: contract, before-change evidence, change evidence, validation evidence, writeback matrix, and uncovered risk. It is required for non-trivial bug fixes, refactors, feature work, and doc-sweeps.

## Journal

Append progress, evidence, checks, blockers, and next route. Do not rewrite past entries except dated corrections.

## Finish

`cs-review` finishes a task by verifying work, updating status, finishing proof trace, adding final journal, and promoting only durable facts to architecture/requirements/compound/attention/roadmap.
