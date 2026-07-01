# Doc-sweep safety

Doc-sweep reduces documentation entropy without letting old docs drag the project away from current code.

## Invocation

```text
cs-review：做文档熵减，范围是 auth 模块，先出报告不要删除。
```

## Evidence priority

1. Current code/manifests/tests/config.
2. Current `.codestable/INDEX.md` and target indexes.
3. Newer accepted design/acceptance/fix-note/apply-notes.
4. Older docs being evaluated.

## Default outcome

Write a report under:

```text
.codestable/doc-sweeps/YYYY-MM-DD-{slug}/index.md
```

Classify candidates as `current`, `unverified`, `conflicts-with-code`, `superseded-by`, or `archive-candidate`.

## Deletion gate

Do not delete by default. Deletion requires explicit user confirmation, a file-by-file list, strong supersession/archive evidence, and no current index pointing to that file as authoritative.
