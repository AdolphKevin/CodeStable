# CodeStable Project Knowledge Contract
## Document map

- Knowledge layers
- Startup read contract
- Scoped specs
- Task memory
- Code inventory
- Plan contract
- Do contract
- Review/writeback contract
- Audit-only contract
- Doc-sweep contract
- Freshness rules

## Knowledge layers

Keep facts close to their authority:

```text
.codestable/INDEX.md                    # root summaries and links only
.codestable/attention.md                # short always-read warnings
.codestable/specs/INDEX.md              # scoped engineering standards index
.codestable/tasks/INDEX.md              # resumable task capsules index
.codestable/reference/code-inventory.*  # generated current implementation map
.codestable/architecture/               # current structural facts with code anchors
.codestable/requirements/               # current capability / business facts
.codestable/roadmap/                    # planning state
.codestable/compound/                   # decisions, learnings, tricks, explore records
.codestable/doc-sweeps/                 # code-grounded doc lifecycle reports
```

Root and scoped indexes are navigation aids. Detail docs own facts.

## Startup read contract

Every CodeStable entry starts with:

1. `.codestable/INDEX.md`
2. `.codestable/attention.md`
3. `.codestable/reference/project-knowledge-contract.md`
4. `.codestable/reference/real-repo-reliability.md`
5. relevant `.codestable/tasks/*/context-pack.md`, `audit-ledger.md`, and `proof.md` when resuming work
6. `.codestable/specs/INDEX.md` when implementing/reviewing code style, commands, API, UI, data, or security conventions
7. `.codestable/reference/code-inventory.md` when implementation map, onboard, refresh, or doc-sweep matters
8. specific architecture / requirements / compound / roadmap docs only after an index says they are relevant

Do not full-scan all knowledge folders unless the user asks for audit, doc-sweep, or refresh. Audit-only backend chain reviews are explicit exceptions and must still be topology-scoped to the relevant chain.

## Scoped specs

Scoped specs are high-signal rules shared by humans and AI. Examples: test commands, API conventions, UI accessibility expectations, schema migration rules, naming, or module ownership. `cs-plan` and `cs-do` read them selectively; `cs-review` keeps them fresh.

## Task memory

Task capsules make non-trivial work resumable:

```text
.codestable/tasks/YYYY-MM-DD-{slug}/task.md
.codestable/tasks/YYYY-MM-DD-{slug}/context-pack.md
.codestable/tasks/YYYY-MM-DD-{slug}/audit-ledger.md   # optional audit-only output
.codestable/tasks/YYYY-MM-DD-{slug}/journal.md
.codestable/tasks/YYYY-MM-DD-{slug}/proof.md
.codestable/tasks/YYYY-MM-DD-{slug}/status.yaml
```

Feature/issue/refactor/roadmap artifacts remain canonical lifecycle records. Task memory is the curated context and session journal.

## Code inventory

`code-inventory.json` and `code-inventory.md` are generated maps to current code anchors. They are not product truth.

Refresh inventory when onboarding, refreshing knowledge, doing doc-sweep, seeing stale indexes, or after major framework/directory/test setup changes.

## Plan contract

`cs-plan` must:

- read root index + attention;
- use code inventory or targeted code reads when facts are missing or suspect;
- route to `onboard.refresh-knowledge` when `.codestable` is placeholder-heavy or stale;
- route to `audit-only.backend-ledger` before design or implementation when a backend chain is high-risk across prompt/schema/status/event boundaries;
- create/update task context packs, audit ledgers, and proof traces for non-trivial work;
- identify human gates and minimality plan;
- avoid durable fact writes except onboard/refresh artifacts.

## Do contract

`cs-do` must:

- read current plan/artifact plus root index + attention;
- read task context pack, completed audit ledger, and proof trace when present;
- block audit-required work when the ledger is missing, partial, or lacks `Audit Status: 已审完`;
- read scoped specs and project facts that constrain the implementation;
- apply the minimality ladder before new code;
- prefer current code over stale docs while reporting conflicts;
- leave durable knowledge freshness to `cs-review`.

## Review/writeback contract

`cs-review` owns durable freshness:

1. Verify code/diff/checks or manual source.
2. Run overbuild/minimality review when code changed.
3. Finish task memory and proof trace when present.
4. Write/update concrete detail doc first.
5. Update scoped index.
6. Update `.codestable/INDEX.md` only when top-level summary/link/status changed.
7. Output `Writeback Matrix` and `Index Sync`.

## Audit-only contract

Audit-only is a `cs-plan` reliability escalation, not a default scan. Use it when the user explicitly says `audit-only`, or when a backend chain crosses modules and involves prompt/schema/status/event flow or weak evidence before a fix.

It must output a file-level ledger with: file, responsibility, entry, exit, events, prompts, schemas, state fields, callers, downstream consumers, risks, and `审计状态: done | partial`.

Every prompt and schema must include path, fields, caller, and downstream consumer. The final status is exactly `Audit Status: 已审完` or `Audit Status: 未审完`; a partial ledger cannot authorize `cs-do`.

## Doc-sweep contract

Doc-sweep is code-grounded lifecycle maintenance:

- refresh/read code inventory first;
- compare document claims against current code anchors, current indexes, and newer docs;
- write a sweep report by default;
- classify stale docs instead of deleting them;
- require explicit confirmation for archive/delete/rewrite operations.

## Freshness rules

- Prefer current code/manifests/tests over old docs for implementation facts.
- Prefer accepted review artifacts over draft plans.
- Mark unverified or conflicting facts; do not silently rewrite history.
- Every durable fact needs a source path, code anchor, user decision, or review proof trace.
- Every stale finding needs evidence and a recommended action.
