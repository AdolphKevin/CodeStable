# CodeStable Shared Conventions
## Document map

- Runtime directory
- Naming rules
- Metadata rules
- Roadmap ↔ feature protocol
- Knowledge types
- Index rules

## Runtime directory

```text
.codestable/
├── INDEX.md
├── attention.md
├── requirements/
├── architecture/
├── specs/
├── tasks/
├── roadmap/
├── features/
├── issues/
├── refactors/
├── doc-sweeps/
├── compound/
├── tools/
└── reference/
```

## Naming rules

- Features/issues/refactors: `YYYY-MM-DD-{slug}/`.
- Roadmaps: `roadmap/{slug}/`.
- Requirements: `requirements/{slug}.md`; index is `requirements/VISION.md`.
- Architecture: `architecture/{type}-{slug}.md`; index is `architecture/ARCHITECTURE.md`.
- Compound: `compound/YYYY-MM-DD-{doc_type}-{slug}.md` where `doc_type` is `learning`, `trick`, `decision`, or `explore`.
- Tasks: `tasks/YYYY-MM-DD-{slug}/` with `task.md`, `context-pack.md`, optional `audit-ledger.md`, `proof.md`, `journal.md`, and `status.yaml`.
- Scoped specs: `specs/{scope}.md`; index is `specs/INDEX.md`.

## Metadata rules

Use frontmatter only when it helps search or lifecycle state. Prefer stable fields: `doc_type`, `status`, `summary`, `tags`, `source`, `updated`, `roadmap`, `roadmap_item`, `lifecycle`, `audit_status`, `supersedes`, `superseded_by`.

Do not invent a generic `note` type. Classify durable knowledge as attention, decision, learning, trick, explore, guide, libdoc, requirement, architecture, or spec.

## Roadmap ↔ feature protocol

Roadmap item statuses:

```text
planned -> in-progress -> done
planned -> dropped
```

- `cs-plan` creates roadmap and child item plan.
- `cs-do` may mark a linked item `in-progress` when implementation begins.
- `cs-review` alone marks items `done` after acceptance or records blockers.

## Knowledge types

| Type | Use when |
|---|---|
| `attention` | every CodeStable run must know a short hard constraint |
| `decision` | a durable choice was made by the owner or accepted review |
| `learning` | a reusable failure mode, debugging path, or lesson was discovered |
| `trick` | a repeatable implementation recipe exists |
| `explore` | a read-only investigation answered a question worth future lookup |
| `spec` | confirmed engineering standard affects future implementation/review |

## Index rules

Detail first, scoped index second, root index last. Never add an index entry that points to a missing detail doc. If a detail doc changes but index remains accurate, report `Index Sync: no-change`.
