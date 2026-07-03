# CodeStable Manual Operations

Use `cs-plan` for onboard/refresh/explore/audit-only/planning, `cs-do` for ready execution, and `cs-review` for verification, project sync, doc-sweep, task finish, scoped specs, and durable knowledge records.

Common operations:

- `cs-plan: initialize CodeStable for this repo` creates code-informed indexes plus `specs/INDEX.md` and `tasks/INDEX.md`.
- `cs-plan: refresh .codestable from current implementation` refreshes inventory and indexes without deleting docs.
- `cs-review: record specs: <confirmed engineering standard and evidence>` updates scoped specs.
- `cs-plan: audit-only, audit the backend prompt/schema/status/event chain before changing source` produces a file-level ledger, exact `Audit Status: complete/incomplete` equivalent (`已审完/未审完`), and a prioritized fix plan.
- Non-trivial work uses `.codestable/tasks/YYYY-MM-DD-{slug}/context-pack.md`, optional `audit-ledger.md`, `journal.md`, and `proof.md`.
- Doc-sweep is audit first, mutation only after explicit approval.

Audit-only is read-only for source code. It is enabled only by explicit `audit-only` or high-risk backend chains where prompt/schema/state/event evidence is too weak for safe scoped planning. A partial ledger blocks `cs-do`.
