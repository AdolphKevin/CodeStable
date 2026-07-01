# Human-AI collaboration playbook
## Document map

Use this map first, then open only the section needed:

- Purpose
- Collaboration model
- Human gates
- AI responsibilities
- Output fields
- Hard stops

## Purpose

CodeStable coordinates the **software lifecycle**, not a team of autonomous agents. The human remains the product/architecture owner; AI accelerates discovery, implementation, verification, and knowledge maintenance.

Owned by: all three public entries.

## Collaboration model

| Actor | Owns | Must not delegate silently |
|---|---|---|
| Human | product intent, tradeoff approval, risk tolerance, merge/commit decision | business priority, architecture direction, security posture, destructive doc cleanup |
| AI | code reading, option discovery, smallest viable implementation, checks, evidence capture, draft docs | current project facts without evidence, irreversible changes, future roadmap commitments |

Every significant step must answer:

```text
What did the human decide?
What did the code prove?
What remains uncertain?
```

## Human gates

Use a gate whenever the task would change durable direction or destroy information.

| Gate | Required when | Allowed output |
|---|---|---|
| `owner-confirmation` | product intent, success criteria, pricing, permissions, security, data retention, public API, or roadmap priority is unclear | options + recommendation; no implementation |
| `design-approval` | standard feature/refactor/roadmap design is needed | design artifact; `Next: ask-user` or `Next: do` only if user already approved |
| `risk-approval` | migration, deletion, broad rewrite, security-sensitive change, or destructive doc-sweep is requested | scoped proposal + rollback path |
| `merge-approval` | committing, tagging, closing roadmap, or deleting/archive docs | verification summary + exact paths |

Fastforward work may run without a gate only when the change is local, reversible, tested or manually verifiable, and does not change durable product/architecture facts.

## AI responsibilities

- Ask the smallest number of questions needed to unblock the next step.
- Present tradeoffs with code/document evidence, not generic pros/cons.
- Keep history honest: approved plans stay as history; divergences go into acceptance/fix/apply notes.
- Separate current facts from proposed future work.
- Stop when evidence contradicts a plan instead of editing the plan to fit the diff.

## Output fields

Public entries include a `Human Gate` line in non-trivial cases:

```text
Human Gate: none | owner-confirmation | design-approval | risk-approval | merge-approval
Owner decision: <known decision, pending question, or not-applicable>
```

For simple fastforward tasks, `Human Gate: none` is acceptable when the reason explains why.

## Hard stops

- Inventing product requirements or architecture decisions.
- Deleting or archiving docs without explicit path-by-path approval.
- Treating a generated code inventory as user-approved product truth.
- Hiding uncertainty by rewriting historical artifacts.
