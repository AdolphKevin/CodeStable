# Scoped Specs Contract
## Document map

- Purpose
- Read rules
- Write rules
- Freshness

## Purpose

Scoped specs are compact engineering standards that should be injected only when relevant: build/test commands, code style, API conventions, UI patterns, data rules, security constraints, and repo-specific workflows.

## Read rules

Start from `.codestable/specs/INDEX.md`; open a specific spec only when the current route touches that scope.

## Write rules

`cs-review` may add or update a scoped spec when a rule is confirmed by current code, tests, CI, README, or explicit owner decision. Do not infer team preference from one accidental file.

## Freshness

Specs can become stale. When code contradicts a spec, mark it as `needs-review` or route to doc-sweep; do not silently rewrite the spec without evidence.
