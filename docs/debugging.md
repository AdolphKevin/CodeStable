# Debugging CodeStable behavior

## What to inspect

Every `cs-plan`, `cs-do`, and `cs-review` response should include:

```text
Route: ...
Playbook: codestable-core/playbooks/<name>.md#<section>
Evidence: ...
```

## Debug loop

1. **Wrong entry**: user called the wrong public command. Fix README/manual examples or user prompt.
2. **Wrong route**: edit the route table in `cs-plan/SKILL.md`, `cs-do/SKILL.md`, or `cs-review/SKILL.md`.
3. **Right route, wrong action**: edit the named playbook section.
4. **Insufficient evidence**: strengthen that playbook's evidence requirements or hard stops.
5. **Doc drift**: inspect `codestable-core/playbooks/project-sync.md`, especially manual sync and doc-sweep rules.
6. **Onboard too generic**: inspect `codestable-core/playbooks/onboard.md` and `codestable-core/onboard/reference.md` templates.

## Route ownership

| Concern | Where to edit |
|---|---|
| When a prompt should route to feature/issue/refactor/roadmap | `cs-plan/SKILL.md` |
| What a feature/issue/refactor flow actually does | `codestable-core/playbooks/feature.md`, `issue.md`, `refactor.md` |
| Code-aware onboarding | `codestable-core/playbooks/onboard.md` and `codestable-core/onboard/tools/scan-project.py` |
| Doc-sweep drift | `codestable-core/playbooks/project-sync.md#doc-sweep-rules` |
| Long-term knowledge records | `codestable-core/playbooks/knowledge-sync.md` |

Do not add new discoverable Skills just to patch behavior; prefer route table + playbook edits first.
