# CodeStable Runtime Structure

After `cs-plan` onboarding, the project contains `.codestable/`, a human/AI shared software lifecycle knowledge base.

```text
.codestable/
├── INDEX.md
├── attention.md
├── requirements/VISION.md
├── architecture/ARCHITECTURE.md
├── specs/INDEX.md
├── tasks/INDEX.md
├── tasks/YYYY-MM-DD-{slug}/
│   ├── task.md
│   ├── context-pack.md
│   ├── audit-ledger.md   # optional audit-only file-level ledger
│   ├── journal.md
│   ├── proof.md
│   └── status.yaml
├── roadmap/
├── features/
├── issues/
├── refactors/
├── doc-sweeps/
├── compound/INDEX.md
├── tools/
└── reference/
    ├── project-knowledge-contract.md
    ├── human-ai-collaboration.md
    ├── task-memory-contract.md
    ├── minimality-ladder.md
    ├── specs-contract.md
    ├── code-inventory.json
    └── code-inventory.md
```

`specs/` stores scoped engineering standards. `tasks/` stores resumable task capsules, optional audit ledgers, journals, and proof traces. `cs-review` owns durable writeback and index freshness.
