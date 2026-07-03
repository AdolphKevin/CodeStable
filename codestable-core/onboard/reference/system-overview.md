# CodeStable System Overview
## Document map

- User model
- Shared playbooks
- Project knowledge layers
- Default loop
- Human gates

## User model

Users only need three lifecycle commands:

| Command | Responsibility |
|---|---|
| `cs-plan` | initialize/refresh, explore, audit-only ledger, route, design, context pack, minimality plan |
| `cs-do` | execute ready work, reuse existing code, record evidence and journal |
| `cs-review` | verify, check overbuild, finish task memory, sync durable facts |

## Shared playbooks

The runtime playbooks are package-level references, not discoverable Skills: collaboration, task-memory, minimality, onboard, explore, audit-only, feature, issue, refactor, roadmap, project-sync, and knowledge-sync.

## Project knowledge layers

- requirements: user/system capability facts;
- architecture: current structural facts;
- specs: scoped engineering standards;
- tasks: resumable context packs, audit ledgers, journals, and proof traces;
- roadmap: planning state;
- feature/issue/refactor: lifecycle artifacts;
- compound/attention: reusable decisions, learnings, tricks, explore records, and startup warnings.

## Default loop

```text
Orient -> Plan -> Do -> Review -> Sync -> Finish
```

Small safe work compresses the loop; risky backend prompt/schema/status/event chains may expand it with an audit-only file-level ledger before design or implementation.

## Human gates

Human approval is required for product/architecture tradeoffs, standard designs, risky or destructive changes, and merge/commit closure. AI proposes with evidence and implements within approved scope.
