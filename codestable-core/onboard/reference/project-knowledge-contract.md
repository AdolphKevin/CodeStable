# CodeStable 项目知识索引契约
## Document map

Use this map first, then open only the section needed:

- Knowledge layers
- Startup read contract
- Code inventory contract
- Plan contract
- Do contract
- Review/writeback contract
- Doc-sweep contract
- Freshness rules

## Knowledge layers

Project knowledge is layered. Keep facts close to their authority:

```text
.codestable/INDEX.md                 # root index, summaries and links only
.codestable/attention.md             # short always-read warnings
.codestable/reference/code-inventory.* # current repo implementation inventory
.codestable/architecture/            # current structural facts with code anchors
.codestable/requirements/            # current user/system capability facts
.codestable/roadmap/                 # planning state
.codestable/compound/                # decisions, learnings, tricks, explore records
.codestable/doc-sweeps/              # doc lifecycle reports
```

`INDEX.md` points to where facts live; it must not become a dumping ground.

## Startup read contract

Every CodeStable entry starts with:

1. `.codestable/INDEX.md`
2. `.codestable/attention.md`
3. `.codestable/reference/project-knowledge-contract.md`
4. `.codestable/reference/code-inventory.md` only when route/context requires current implementation map
5. Specific architecture / requirements / compound / roadmap docs only after the index says they are relevant

Do not full-scan `.codestable/architecture/`, `.codestable/requirements/`, or `.codestable/compound/` unless the user asks for audit/doc-sweep/refresh.

## Code inventory contract

`code-inventory.json` and `code-inventory.md` are generated during onboard and refresh. They are not product truth; they are a map to current code anchors.

Refresh inventory when:

- onboarding a repo for the first time;
- user says “根据当前实现重新整理 .codestable”;
- doc-sweep is requested;
- route/debug output suggests indexes are stale;
- a major directory/framework/test setup changed.

Inventory updates are safe because they are generated facts. Architecture/requirements updates still need careful evidence and index sync.

## Plan contract

`cs-plan` must:

- read root index + attention before planning;
- use code inventory or targeted code reads when project facts are missing or suspect;
- route to `onboard.refresh-knowledge` when `.codestable` is placeholder-heavy or stale;
- output `Playbook` and `Evidence` so route decisions are debuggable;
- avoid writing durable facts except through onboard initialization/refresh artifacts.

## Do contract

`cs-do` must:

- read current plan/artifact plus root index + attention;
- read only the specific project facts that constrain implementation;
- prefer current code over stale docs when executing, but report conflicts;
- not opportunistically rewrite architecture/requirements/compound docs;
- leave durable knowledge freshness to `cs-review`.

## Review/writeback contract

`cs-review` owns durable knowledge freshness:

1. Verify code/diff/checks or manual source.
2. Write/update the concrete detail doc first.
3. Update the corresponding index.
4. Update `.codestable/INDEX.md` only when top-level summary/link/status changed.
5. Output `Writeback Matrix` and `Index Sync`.

## Doc-sweep contract

Doc-sweep is code-grounded lifecycle maintenance:

- refresh/read code inventory first;
- compare document claims against current code anchors and current indexes;
- write a sweep report by default;
- classify stale docs instead of deleting them;
- require explicit confirmation for deletion/archive operations.

## Freshness rules

- Prefer current code/manifests/tests over old docs for factual claims.
- Prefer accepted review artifacts over draft plans.
- Mark unverified or conflicting facts; do not silently rewrite history.
- Every new durable fact needs a source path, code anchor, or user decision.
- Every stale finding needs an evidence path and a recommended action.
