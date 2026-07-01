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
| `cs-plan` | initialize/refresh, explore, route, design, context pack, minimality plan |
| `cs-do` | execute ready work, reuse existing code, record evidence and journal |
| `cs-review` | verify, check overbuild, finish task memory, sync durable facts |

## Shared playbooks

The runtime playbooks are package-level references, not discoverable Skills: collaboration, task-memory, minimality, onboard, explore, feature, issue, refactor, roadmap, project-sync, and knowledge-sync.

## Project knowledge layers

- requirements: user/system capability facts;
- architecture: current structural facts;
- specs: scoped engineering standards;
- tasks: resumable context packs and journals;
- roadmap: planning state;
- feature/issue/refactor: lifecycle artifacts;
- compound/attention: reusable decisions, learnings, tricks, explore records, and startup warnings.

## Default loop

```text
Orient -> Plan -> Do -> Review -> Sync -> Finish
```

Small safe work compresses the loop; risky or cross-boundary work expands it with human gates and task memory.

## Human gates

Human approval is required for product/architecture tradeoffs, standard designs, risky or destructive changes, and merge/commit closure. AI proposes with evidence and implements within approved scope.
