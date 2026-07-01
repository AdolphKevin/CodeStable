# CodeStable Explicit Operations Manual

## Document map

- Entry selection
- Onboard
- Explore
- Manual architecture / requirements / roadmap records
- Manual decision / learning / trick / explore / attention records
- Project knowledge freshness

This runtime exposes only three CodeStable entries: `cs-plan`, `cs-do`, and `cs-review`. Onboarding, exploration, architecture sync, and decision records are explicit intents routed through those entries, not separate Skills.

## Entry selection

| Operation | Entry | Reason |
|---|---|---|
| Initialize, repair, or inspect `.codestable/` | `cs-plan` | Onboarding is the precondition for the lifecycle |
| Explore code without editing | `cs-plan` | Exploration is read-only investigation, not durable knowledge by default |
| Plan feature / bug / refactor / roadmap | `cs-plan` | Requires routing and scope control |
| Execute ready work | `cs-do` | Only executes work with clear boundaries |
| Review, close state, sync docs | `cs-review` | Review owns final Project Sync writeback |
| Manually record architecture / requirements / roadmap state | `cs-review` | This is explicit Project Sync |
| Manually record decision / learning / trick / explore / attention / guide / libdoc | `cs-review` | This is explicit Knowledge Sync |

## Onboard

Recommended invocation:

```text
cs-plan: initialize CodeStable and create the .codestable skeleton for this repo.
```

Routes:

```text
Route: onboard.required   # no .codestable/
Route: onboard.repair     # skeleton exists but required pieces are missing
Route: onboard.status     # skeleton is complete; report status only
```

Onboarding creates or repairs the CodeStable runtime skeleton. It must not modify business code.

## Explore

Recommended invocation:

```text
cs-plan: explore the auth login flow without editing code; list key files, call chain, and unknowns.
```

Route:

```text
Route: explore.plan
```

Exploration is read-only and does not write files by default. Persist the result later with `cs-review` only when it has durable reuse value.

## Manual architecture record

Recommended invocation:

```text
cs-review: record architecture: OrderService owns writes and OrderQuery owns read projections; evidence: src/order/*.
```

Route:

```text
Route: project-sync.manual
Writeback Matrix: architecture=yes, requirements=no, roadmap=no, compound=no, attention=no, guides-or-libdoc=no
```

Architecture records require a source: explicit user statement, code anchors, existing docs, or reviewed diff. Future plans must not be written as current architecture.

## Manual requirement record

```text
cs-review: record requirements: free users can export at most 3 reports per day; show an upgrade prompt afterwards.
```

Route:

```text
Route: project-sync.manual
Writeback Matrix: requirements=yes, architecture=no, roadmap=no, compound=no, attention=no, guides-or-libdoc=no
```

Record user-visible capability, success criteria, boundaries, and failure modes. Do not turn implementation details into requirements.

## Manual decision record

```text
cs-review: record decision: use Postgres row locks instead of Redis for job state for now because deployment complexity is lower and current throughput is sufficient.
```

Route:

```text
Route: knowledge-sync.manual
Writeback Matrix: compound=yes, architecture=<yes/no>, requirements=no, roadmap=<yes/no>, attention=no, guides-or-libdoc=no
```

A decision needs context, the decision, rationale, alternatives, and consequences. If it changes current architecture facts, update architecture too.

## Manual knowledge records

```text
cs-review: record learning: The billing reconciliation entrypoint is src/billing/reconcile.ts; context is in issue #123.
cs-review: record attention: tests must use pnpm test -- --runInBand because the shared test DB is stateful.
cs-review: record learning: Vitest mock order affects authClient initialization; see src/auth/__tests__/login.test.ts.
cs-review: record trick: when adding admin list pages, reuse useServerTable instead of reimplementing pagination state.
cs-review: record explore: persist the billing webhook idempotency investigation as a searchable explanation.
```

If the user only gives a generic project remark, classify it as attention, learning, trick, decision, explore, guide, or libdoc first. If it cannot be classified, ask before writing.

Route:

```text
Route: knowledge-sync.manual
```

Only record knowledge that future agents or humans will reuse. Do not persist transient debugging noise or generic advice without project evidence.

## Do not invoke removed stage Skills

```text
cs-onboard: initialize the project
cs-decide: record a decision
cs-arch: update architecture
```

These old stage-style Skills are not part of the runtime package. Express the intent through `cs-plan` or `cs-review` instead.


Generic `note` is not a write target. Classify it as attention, learning, trick, decision, explore, guide, or libdoc before writing.

## Project knowledge index maintenance

Onboard creates `.codestable/INDEX.md`, `requirements/VISION.md`, `architecture/ARCHITECTURE.md`, and `compound/INDEX.md`.

- `cs-plan` reads indexes and attention first, then opens detailed docs only when needed.
- `cs-do` uses current ready artifacts plus indexed project constraints; it does not casually rewrite long-lived facts.
- `cs-review` owns freshness: after writing durable detail docs, it updates the relevant indexes and reports `Index Sync`.
