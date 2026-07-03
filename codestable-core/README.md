# CodeStable Core Playbooks

`codestable-core/` is the shared engineering discipline library for CodeStable runtime. It is **not** a discoverable Skill and must not contain `SKILL.md`.

## Current design

The runtime makes lifecycle workflow explicit as auditable playbooks:

```text
playbooks/collaboration.md   # human ownership and gates
playbooks/task-memory.md     # task capsule, context pack, journal, proof trace
playbooks/minimality.md      # minimal implementation ladder and overbuild checks
playbooks/onboard.md         # code-aware initialization and refresh
playbooks/explore.md         # read-only exploration
playbooks/audit-only.md      # high-risk backend audit ledger before fixes
playbooks/feature.md
playbooks/issue.md
playbooks/refactor.md
playbooks/roadmap.md
playbooks/project-sync.md
playbooks/knowledge-sync.md
```

## Debugging contract

The public entries emit:

```text
Route: ...
Playbook: codestable-core/playbooks/<name>.md#<section>
Human Gate: ...
Evidence: ...
Task Memory: ...
Proof Trace: ...
Audit Ledger / Audit Status: ...
Minimality Plan / Minimality / Overbuild Check: ...
Next: ...
```

When behavior is bad, debug in this order: route, human gate, evidence, audit ledger status, context pack, minimality rung, review/writeback.

## Maintenance rules

- Do not copy playbooks into individual Skill directories.
- Do not reintroduce internal `SKILL.md` files for lifecycle phases.
- Onboard copies `codestable-core/onboard/reference/` and `codestable-core/onboard/tools/` into the target project as `.codestable/reference/` and `.codestable/tools/`.
- Runtime packages must not include eval harness files.


## Real-repo reliability

`playbooks/reliability.md` defines evidence levels, proof traces, bug/refactor gates, audit-only completion rules, and doc-sweep claim mapping. Public entries surface those fields in their final protocol so route quality can be debugged.
