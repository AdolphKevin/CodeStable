# Audit-only backend ledger playbook
## Document map

Use this map first, then open only the section needed for the current route:

- Purpose
- Trigger conditions
- Placement in `cs-plan`
- Read-only boundary
- Scope discovery
- File-level audit ledger
- Prompt and schema traceability
- Completion status
- Prioritized fix plan
- Handoff rules
- Output fields
- Hard stops

## Purpose

`audit-only.backend-ledger` is a `cs-plan` route for high-risk backend chains where a normal scoped plan is not safe enough. It performs a read-only, file-level audit before design or implementation and produces an audit ledger that makes every relevant module, prompt, schema, state field, and event flow traceable.

Owned by: `cs-plan` routes and performs the audit; `cs-do` blocks execution when a required completed ledger is missing; `cs-review` may later preserve durable findings only through normal Project Sync / Knowledge Sync evidence rules.

## Trigger conditions

Enable audit-only only when at least one condition is true:

1. The user explicitly says `audit-only` or asks to enter audit-only mode.
2. The requested backend chain crosses multiple modules and cannot be safely planned from a few local anchors.
3. The request involves prompt definitions, schema contracts, state fields, event flow, queues, workers, LLM orchestration, or generated/validated payloads across boundaries.
4. A fix is requested but evidence is too weak for `feature.standard.design`, `issue.standard.report-analysis`, or `refactor.standard.scan-design` to produce a safe plan.

Do **not** enable audit-only by default. Ordinary `cs-plan` remains scoped planning. A small local route, single-file bug, or ordinary code explanation should stay on the normal feature / issue / refactor / explore path unless the user explicitly asks for `audit-only`.

## Placement in `cs-plan`

Audit-only sits after startup/onboard routing and before feature / issue / refactor / roadmap design:

```text
cs-plan route judgment
  -> if heavy audit trigger matches: audit-only.backend-ledger
  -> read-only scan
  -> file-level audit ledger
  -> Audit Status: 已审完 | 未审完
  -> prioritized fix plan
  -> only then may a later ready task proceed to cs-do
```

If the ledger is missing, incomplete, or not marked `已审完`, do not move into `cs-do` and do not claim that the full backend chain has been reviewed.

## Read-only boundary

Audit-only may read files, inspect manifests/configs/tests, run safe read-only commands, and record findings. It must not change source code, migrations, generated assets, package manifests, tests, or runtime configuration.

Allowed writes are limited to audit records when the user asked for a persistent artifact or the task needs cross-session memory, for example:

```text
.codestable/tasks/YYYY-MM-DD-{slug}/audit-ledger.md
.codestable/tasks/YYYY-MM-DD-{slug}/context-pack.md
.codestable/tasks/YYYY-MM-DD-{slug}/journal.md
```

Those records must contain findings and evidence only. They must not smuggle in implementation patches or mutate product / architecture facts as if they were accepted current state.

## Scope discovery

Do not audit by keyword search alone. Build a topology of the relevant backend chain from multiple anchors:

1. Start from user-facing or system entrypoints: HTTP routes, RPC handlers, CLIs, webhooks, scheduled jobs, workers, queue consumers, event subscribers, and tests that exercise the chain.
2. Follow calls through controllers, services, orchestration layers, repositories, adapters, validators, prompt registries/templates, schema/model definitions, state machines, event emitters, and downstream consumers.
3. Include configuration and manifests that register routes, events, workers, prompt providers, schemas, feature flags, or environment-dependent behavior.
4. For each discovered module, record why it is in scope. Stop only when upstream inputs and downstream consumers for prompt/schema/state/event dependencies are accounted for.
5. If time, access, generated-code size, missing dependencies, or dynamic dispatch prevents full enumeration, mark the affected modules `partial` and the overall audit `未审完`.

## File-level audit ledger

The required output is a file-level ledger. Use this minimum shape for every relevant file or module:

```text
文件:
职责:
入口:
出口:
事件:
Prompt:
Schema:
状态字段:
调用方:
下游消费方:
风险:
审计状态: done | partial
```

Rules:

- `文件` uses a concrete path or clearly named generated/runtime module.
- `职责` says what this module owns and what it does not own.
- `入口` names functions, routes, handlers, jobs, consumers, tests, or config registrations that enter the module.
- `出口` names returned payloads, DB writes, external calls, emitted events, prompt invocations, schema validations, or state transitions.
- `事件` includes inbound and outbound events, queues, webhooks, scheduler triggers, or `none observed` with evidence.
- `Prompt` and `Schema` must follow the traceability rules below.
- `状态字段` lists persisted, in-memory, task/session, lifecycle, queue, retry, idempotency, feature-flag, or workflow status fields touched by the module.
- `调用方` and `下游消费方` must be concrete paths/functions when known; otherwise mark `unknown` and explain why.
- `风险` records findings only. Do not fix them in audit-only.
- `审计状态` is `partial` whenever the file was inferred but not fully inspected, dynamic references remain unresolved, tests/configs are missing, or any caller/consumer is unknown.

## Prompt and schema traceability

Every prompt and schema found in the audited chain must be enumerated with:

```text
路径: <file path>
字段: <template variables / payload fields / validation fields / model columns>
调用方: <path:function, route, worker, test, or config registration>
下游消费方: <LLM/tool/output parser, service, DB, event consumer, API response, UI, or unknown>
```

If a module has no prompt or schema involvement, write `none observed` plus the evidence used to decide that. Do not leave the field blank.

## Completion status

At the end of the audit, state one of the following exactly:

```text
Audit Status: 已审完
Audit Status: 未审完
```

Use `已审完` only when every relevant module in the discovered chain has a ledger entry, every entry is `审计状态: done`, and every prompt/schema has a path, fields, caller, and downstream consumer.

Use `未审完` when any ledger entry is `partial`, any related module was not opened, dynamic dispatch or generated code was not resolved, or prompt/schema/state/event consumers remain unknown. When `未审完`, list the missing scope and do not say the full backend chain is complete.

## Prioritized fix plan

After the ledger and status, provide a prioritized fix plan. It is still planning, not implementation.

Use priority buckets:

```text
P0: correctness / data loss / security / irreversible state / prompt-schema mismatch that can corrupt outputs
P1: integration bugs, missing validation, broken event consumers, retry/idempotency risks
P2: observability, cleanup, refactor, documentation, test coverage gaps
```

Each fix item should cite the ledger entries it comes from, name the smallest safe next route, and state whether user approval is needed. If the audit is `未审完`, mark the fix plan `provisional` and block execution until the missing ledger scope is completed.

## Handoff rules

- `cs-plan` may propose `Next: do` only when `Audit Status: 已审完`, the fix plan identifies a bounded first change, required human gates are satisfied, and verification criteria are named.
- If `Audit Status: 未审完`, use `Next: stop` or `Next: ask-user`; do not route to `cs-do`.
- `cs-do` must stop with `blocked.missing-audit-ledger` when the task/request requires audit-only but no completed ledger is present.
- A completed ledger is not implementation approval by itself. Public API, security, data, migration, or owner tradeoffs still use the normal human gates.

## Output fields

For `audit-only.backend-ledger`, include these fields in addition to the normal `cs-plan` footer:

```text
Audit Ledger: not-applicable | missing | inline | create:<path> | update:<path> | read:<path> | complete:<path> | partial:<path>
Audit Status: 已审完 | 未审完
Audit Scope: <backend chain and module count, or missing scope>
Fix Plan: prioritized | provisional | none
```

## Hard stops

- Starting code changes before a required audit ledger exists.
- Claiming “已审完” with any `partial` ledger row or unknown prompt/schema consumer.
- Auditing only keyword hits while ignoring route registrations, workers, events, configs, or downstream consumers.
- Omitting prompt/schema path, fields, caller, or downstream consumer.
- Treating risk notes as fixes.
- Enabling full-chain audit by default for small scoped tasks.
