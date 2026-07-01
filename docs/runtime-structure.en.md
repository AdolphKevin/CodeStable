# CodeStable Runtime Structure

After onboarding through `cs-plan`, the project root contains `.codestable/`, the aggregate workspace for CodeStable artifacts and durable project knowledge.

```text
.codestable/
├── INDEX.md
├── attention.md
├── requirements/VISION.md
├── architecture/ARCHITECTURE.md
├── roadmap/
├── features/
├── issues/
├── refactors/
├── doc-sweeps/
├── compound/INDEX.md
├── tools/
│   ├── scan-project.py
│   └── scan-codestable-docs.py
└── reference/
    ├── project-knowledge-contract.md
    ├── code-inventory.json
    ├── code-inventory.md
    ├── shared-conventions.md
    ├── workflow-conventions.md
    └── system-overview.md
```

`INDEX.md` is the first project-knowledge entry point. `code-inventory.*` maps the current implementation and is refreshed by onboard, refresh, and doc-sweep. Long-term facts are written by `cs-review`, with index sync.

Shared discipline lives in package-level `codestable-core/playbooks/*.md`, not in discoverable Skills.
