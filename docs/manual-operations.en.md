# CodeStable Manual Operations

## Entry choice

| Operation | Entry | Why |
|---|---|---|
| Initialize, repair, or refresh `.codestable/` | `cs-plan` | Build a code-informed project knowledge index before lifecycle work |
| Read-only code exploration | `cs-plan` | Explore is analysis, not durable knowledge by itself |
| Plan feature / bug / refactor / roadmap | `cs-plan` | Requires routing and scope judgment |
| Execute ready work | `cs-do` | Only implement within confirmed boundaries |
| Review, close, and write back docs | `cs-review` | Review owns durable knowledge freshness |
| Documentation entropy reduction | `cs-review` | Requires current-code evidence and deletion gates |
| Record architecture / requirements / roadmap | `cs-review` | Project Sync manual mode |
| Record decision / learning / trick / explore / attention / guide / libdoc | `cs-review` | Knowledge Sync manual mode; no generic `note` type |

## Onboard and refresh

```text
cs-plan: initialize CodeStable for this repo.
cs-plan: refresh .codestable from the current implementation.
cs-plan: check and repair CodeStable initialization.
```

Routes:

```text
onboard.required
onboard.repair
onboard.refresh-knowledge
onboard.status
```

Initialization is not skeleton-only. It should generate code inventory and code-informed `INDEX.md`, `architecture/ARCHITECTURE.md`, `requirements/VISION.md`, `compound/INDEX.md`, and `attention.md`. Unconfirmed product intent must be labeled `inferred` or `unknown`.

## Explore

```text
cs-plan: explore the auth login flow without changing code.
```

Explore is read-only and does not write `.codestable/compound/`. To persist useful findings:

```text
cs-review: record explore: <finding and evidence>
```

## Record durable facts

```text
cs-review: record architecture: <current fact + code anchor>
cs-review: record requirements: <capability + success criteria + boundary>
cs-review: record decision: <decision + context + tradeoff + consequence>
cs-review: record learning/trick/attention: <content + evidence>
```

Manual records require a source: user decision, code anchor, existing accepted artifact, or reviewed diff.

## Doc-sweep

```text
cs-review: run doc-sweep for auth; report first, do not delete.
```

Route:

```text
project-sync.doc-sweep
```

Rules:

- Refresh/read `reference/code-inventory.*` first.
- Map document claims to current code anchors, current indexes, or newer accepted docs.
- Write a sweep report by default.
- Do not delete files unless the user explicitly confirms a file-by-file deletion list with sufficient evidence.
