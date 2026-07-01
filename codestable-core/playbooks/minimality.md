# Minimality playbook
## Document map

Use this map first, then open only the section needed:

- Purpose
- Ladder
- Safety floor
- Planning use
- Implementation use
- Review use
- Output fields
- Hard stops

## Purpose

CodeStable borrows Ponytail's senior-developer discipline: be lazy about unnecessary code, never lazy about reading, validation, security, accessibility, or data safety.

Owned by: `cs-plan`, `cs-do`, and `cs-review`.

## Ladder

After understanding the touched code path, stop at the first rung that works:

1. **Does this need to exist?** If not, skip or remove it.
2. **Already in this codebase?** Reuse existing helper, type, component, service, route, test pattern, or config.
3. **Standard library or platform feature?** Use language/runtime/browser/database/framework built-ins before custom code.
4. **Installed dependency already covers it?** Use it only if it is already part of the project and fits the task.
5. **One-line or one-home change?** Prefer the smallest change at the current responsibility boundary.
6. **Only then write new code**, limited to the requested behavior and nearest owning module.

The ladder runs after reading the relevant flow, not instead of reading it.

## Safety floor

Never cut these for minimality:

- trust-boundary validation;
- auth/permission checks;
- data loss or migration safety;
- error handling for user-visible or external I/O paths;
- accessibility for UI changes;
- tests or manual verification for non-trivial behavior.

## Planning use

`cs-plan` records the expected rung for fastforward and standard work:

```text
Minimality Plan: reuse | stdlib/platform | installed-dependency | one-home-change | new-minimal-code | no-op
Reuse targets: <paths or none>
Not doing: <explicit non-goals>
```

If the user asks for a large implementation but the first rung says the capability already exists, route to `explore.plan` or a no-op plan with evidence.

## Implementation use

`cs-do` must search for reuse before creating parallel abstractions. Add dependencies, new frameworks, caches, queues, plugin systems, config layers, or generic helpers only when the plan explicitly requires them or a user approves an escalation.

Implementation evidence includes:

- searched/reused paths;
- rung chosen;
- why earlier rungs did not apply;
- checks proving the small change works.

## Review use

`cs-review` checks for overbuild:

| Signal | Review action |
|---|---|
| new dependency | require plan/user approval and reason |
| new generic abstraction | require at least two real callers or approved design |
| broad file churn | compare against route scope |
| custom implementation of platform feature | ask why platform/stdlib was insufficient |
| missing safety check | block even if code is small |

## Output fields

Use these lines when relevant:

```text
Minimality: rung=<rung>; reuse=<paths or none>; added-abstraction=<none/path+reason>
Overbuild Check: pass | blocked | not-applicable
```

## Hard stops

- Writing speculative extension points.
- Adding dependencies for small local behavior.
- Copying an existing pattern instead of using it.
- Removing validation/security/accessibility to reduce lines.
