# CodeStable Manual Operations

Use `cs-plan` for onboard/refresh/explore/planning, `cs-do` for ready execution, and `cs-review` for verification, project sync, doc-sweep, task finish, scoped specs, and durable knowledge records.

Common operations:

- `cs-plan: initialize CodeStable for this repo` creates code-informed indexes plus `specs/INDEX.md` and `tasks/INDEX.md`.
- `cs-plan: refresh .codestable from current implementation` refreshes inventory and indexes without deleting docs.
- `cs-review: record specs: <confirmed engineering standard and evidence>` updates scoped specs.
- Non-trivial work uses `.codestable/tasks/YYYY-MM-DD-{slug}/context-pack.md`, `journal.md`, and `proof.md`.
- Doc-sweep is audit first, mutation only after explicit approval.
