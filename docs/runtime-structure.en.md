# CodeStable Runtime Structure

After onboarding through `cs-plan`, a `.codestable/` directory is created at your project root. It is the aggregate root for all CodeStable artifacts and the only project workspace the three CodeStable entries read or write. Initialization, repair, and status checks are all handled through `cs-plan`; there is no separate onboard Skill.

```text
your-project/
├── .codestable/
│   ├── INDEX.md                           # project knowledge index
│   ├── requirements/                     # Requirement entities
│   │   ├── VISION.md                       # capability/requirements index
│   │   └── {slug}.md
│   ├── architecture/                     # Architecture entities
│   │   ├── ARCHITECTURE.md
│   │   └── {type}-{slug}.md
│   ├── roadmap/                          # Big-need planning
│   │   └── {slug}/
│   │       ├── {slug}-roadmap.md
│   │       ├── {slug}-items.yaml
│   │       └── drafts/
│   ├── features/                         # Feature flow
│   │   └── YYYY-MM-DD-{slug}/
│   │       ├── {slug}-brainstorm.md
│   │       ├── {slug}-design.md
│   │       ├── {slug}-checklist.yaml
│   │       └── {slug}-acceptance.md
│   ├── issues/                           # Issue flow
│   │   └── YYYY-MM-DD-{slug}/
│   │       ├── {slug}-report.md
│   │       ├── {slug}-analysis.md
│   │       └── {slug}-fix-note.md
│   ├── refactors/                        # Refactor flow
│   │   └── YYYY-MM-DD-{slug}/
│   │       ├── {slug}-scan.md
│   │       ├── {slug}-refactor-design.md
│   │       ├── {slug}-checklist.yaml
│   │       └── {slug}-apply-notes.md
│   ├── compound/                         # Searchable lessons / long-term rules / reusable prescriptions
│   │   ├── INDEX.md                       # durable knowledge index
│   │   └── YYYY-MM-DD-{doc_type}-{slug}.md
│   ├── tools/                            # Shared scripts
│   └── reference/                        # Shared references
│       ├── shared-conventions.md
│       ├── workflow-conventions.md
│       ├── system-overview.md
│       └── ...
```

## Explicit record entry

- Record architecture / requirements / roadmap state with `cs-review: record architecture/requirements/roadmap: ...`.
- Record decision / learning / trick / explore / attention with `cs-review: record decision/learning/trick/explore/attention: ...`; generic notes must be classified first.
- These operations route to `project-sync.manual` or `knowledge-sync.manual`; they still require a source/evidence and must not invent long-term facts.

## Key points

- All artifacts aggregate under `.codestable/`, so historical features, bugs, and decisions are easy to find.
- `requirements/` and `architecture/` are long-lived archives that only record current state.
- `roadmap/` is the planning layer for big-need breakdowns and interface contracts.
- `features/`, `issues/`, and `refactors/` use `YYYY-MM-DD-{slug}/` to bundle one unit of work.
- `compound/` stores searchable archive docs. learning, trick, decision, and explore are distinguished by `doc_type`.
- `attention.md` stores short reminders every CodeStable entry must know at startup.
- `.codestable/INDEX.md` is the project knowledge entry point for every Plan/Do/Review run; indexes contain summaries and links, while details live in architecture / requirements / roadmap / compound docs.
- `reference/` and `tools/` are copied by the onboard path in `cs-plan` from `codestable-core/onboard/`.

## Hard constraint

CodeStable runtime stores shared executor references in package-level `codestable-core/`, not in multiple Skill directories. Do not make one Skill depend on another Skill directory's reference files; shared rules live in exactly one `codestable-core/` file.

Cross-entry shared project facts go through the working project layer: `cs-plan` onboard releases `.codestable/INDEX.md` and `.codestable/reference/`, then all three entries read indexes before opening detailed docs.


## Maintenance entry ownership

- `.codestable/` initialization, repair, and reference/tools refresh: use `cs-plan` with `onboard.required` / `onboard.repair`.
- `.codestable/architecture/` and `.codestable/requirements/`: use `cs-review` with `project-sync.manual` or Project Sync after review.
- `.codestable/compound/`, `.codestable/attention.md`, guide/libdoc: use `cs-review` explicit records or Knowledge Sync after review.
- `cs-do` does not own long-lived documentation. It records execution evidence and hands closure to `cs-review`.


## Project knowledge index

Every CodeStable entry starts from `.codestable/INDEX.md` and `.codestable/attention.md`. Indexes point to detailed requirement, architecture, roadmap, and compound knowledge documents. `cs-review` updates both details and indexes when durable project facts change.
