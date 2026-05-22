# CodeStable Runtime Structure

After `/cs-onboard`, a `codestable/` directory appears at your project root. It is the aggregate root for all CodeStable artifacts and the only workspace each skill reads or writes at runtime.

```text
your-project/
├── codestable/
│   ├── requirements/                     # Requirement entities
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
│   ├── compound/                         # Knowledge sink
│   │   └── YYYY-MM-DD-{doc_type}-{slug}.md
│   ├── tools/                            # Shared scripts
│   └── reference/                        # Shared references
│       ├── shared-conventions.md
│       ├── system-overview.md
│       └── ...
└── AGENTS.md
```

## Key Points

- All artifacts aggregate under `codestable/`, so historical features, bugs, and decisions are easy to find.
- `requirements/` and `architecture/` are long-lived archives that only record current state.
- `roadmap/` is the planning layer for big-need breakdowns and interface contracts.
- `features/`, `issues/`, and `refactors/` use `YYYY-MM-DD-{slug}/` to bundle one unit of work.
- `compound/` is the single knowledge sink. learning, trick, decision, and explore are distinguished by the `doc_type` field.
- `reference/` is copied by `cs-onboard` from the skill package. To change shared conventions, edit `cs-onboard/reference/` templates.

## Hard Constraint

A skill is an independent install unit. At runtime, each skill can only see files inside its own package. References like `B-skill/reference/xxx.md` written in skill A's `SKILL.md` are unreachable at runtime.

Cross-skill shared references must go through the working project layer: `cs-onboard` copies them from the skill package to the project's `codestable/reference/`, and other skills read them via project-relative paths.
