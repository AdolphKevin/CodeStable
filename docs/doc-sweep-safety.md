# Doc-sweep safety

Doc-sweep reduces documentation entropy without letting old docs drag the project away from current code.

## Invocation

```text
cs-review：做文档熵减，范围是 auth 模块，先出报告不要删除。
```

## Two-phase model

1. **Audit**: refresh/read code inventory, build doc inventory, map claims to evidence, and write a report.
2. **Mutation**: archive/delete/rewrite only after explicit user approval with exact paths and rollback note.

## Evidence priority

1. Current code/manifests/tests/config.
2. Current `.codestable/INDEX.md` and scoped indexes.
3. Newer accepted design/acceptance/fix-note/apply-notes.
4. Older docs being evaluated.

## Claim mapping

Each durable claim should be mapped to one of:

```text
code-anchor | current-index | newer-accepted-doc | user-source | no-current-evidence
```

`no-current-evidence` means `unverified`, not stale.

## Default outcome

Write a report under:

```text
.codestable/doc-sweeps/YYYY-MM-DD-{slug}/index.md
```

Classify candidates as `current`, `unverified`, `conflicts-with-code`, `superseded-by`, or `archive-candidate`.

## Deletion gate

Do not delete by default. Deletion requires explicit user confirmation, a file-by-file list, strong supersession/archive evidence, no current index pointing to that file as authoritative, and a rollback note.
