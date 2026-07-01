# Issue playbook
## Document map

Use this map first, then open only the section needed for the current route:

- Route map
- Artifact layout
- Report discipline
- Analysis discipline
- Quickfix discipline
- Task memory for investigations
- Fix implementation discipline
- Debug escalation
- Fix-note minimum
- Reproduction gate
- Verification checklist
- Anti-regression reflection
- Minimality checkpoints
- Project Sync boundary
- Hard stops

## Route map

| Route | Use when | Output |
|---|---|---|
| `issue.quickfix.plan` | Root cause and fix boundary are already clear | compact plan / fix boundary |
| `issue.quickfix.do` | Clear root cause, small scoped patch | code diff + fix-note or final fix summary |
| `issue.standard.report-analysis` | Root cause is unknown, reproduction is unstable, or impact is broad | report + analysis; no code changes |
| `issue.standard.fix` | Analysis is confirmed or user selected a fix option | scoped fix + validation evidence |
| `issue.fix-verify` | Fix is ready for closure | fix-note completion + regression evidence |

## Artifact layout

```text
.codestable/issues/YYYY-MM-DD-{slug}/
├── {slug}-report.md
├── {slug}-analysis.md
└── {slug}-fix-note.md
```

Quickfix may skip full report/analysis but still needs a compact fix-note or final output with the same evidence.

## Report discipline

A report captures the observed failure without inventing the cause.

Minimum questions:

1. What is the visible symptom?
2. How can it be reproduced, or what observed signal replaces reproduction?
3. What is expected vs actual behavior?
4. What environment, version, command, browser, data, tenant, or entry point matters?
5. What is the severity and affected scope?

Include logs, screenshots, failing tests, timestamps, request IDs, or user-provided evidence when available. Unknowns are allowed; do not fill them with guesses.

## Analysis discipline

Analysis is for finding the root cause and fix options, not for changing code.

Five steps:

1. Locate the failing path and relevant code owners.
2. Reconstruct the failure path from input to observed symptom.
3. Confirm root cause with evidence, or state remaining uncertainty.
4. Evaluate impact surface: other callers, data variants, regression risks.
5. Present fix options, tradeoffs, recommended option, and verification plan.

Stop if the evidence contradicts the initial hypothesis. Do not continue into implementation on an unconfirmed root cause unless the user explicitly chooses an experiment.

## Quickfix discipline

Quickfix is allowed only when the root cause is concrete and scoped, for example a known guard condition, parser edge case, config typo, or obvious null/empty handling bug.

Required compact output:

- Symptom and affected scope.
- Known root cause or evidence-backed hypothesis.
- Intended fix location and forbidden scope.
- Verification command or manual reproduction path.
- Fix-note path or final fix summary.

Quickfix is not a permission to skip evidence or broaden the diff.

## Task memory for investigations

Create a task capsule when the investigation spans sessions, has multiple hypotheses, or touches many modules. The context pack links reproduction evidence, failing path, candidate owners, relevant requirements/architecture, and open questions. The journal records hypothesis changes so later sessions do not repeat failed attempts.

## Fix implementation discipline

During fixing:

- Modify the common root cause, not only the visible caller.
- Search for sibling callers and duplicated logic before patching.
- Keep the diff minimal and inside the confirmed scope.
- Do not mix in refactor, feature behavior, formatting churn, dependency upgrades, or unrelated cleanup.
- Avoid suppression, empty catch blocks, type casts, debug logs, retries, or broad fallbacks as the “fix” unless they are the actual confirmed behavior.
- If the fix does not work, escalate to analysis or log collection rather than stacking patches.

## Debug escalation

When evidence is insufficient, ask for the smallest useful signal: exact command, failing input, log snippet, request/trace ID, screenshot, or reproduction branch. Instrumentation must be temporary, scoped, and removed or documented before closure.

## Fix-note minimum

A fix-note or final summary must include:

- Root cause.
- Actual adopted solution.
- Files touched.
- Verification result: failing path before / passing path after when possible.
- Regression risk and uncovered areas.
- Project Sync result.
- Proof trace path when task memory exists.

## Reproduction gate

Before `issue.quickfix.do` or `issue.standard.fix`, require one of:

- failing test or command output;
- deterministic manual reproduction path;
- production/user evidence such as log, request ID, screenshot, or exact input;
- explicit no-repro rationale plus a targeted validation plan.

If none exists, route to `blocked.missing-reproduction` or `issue.standard.report-analysis`. Do not implement from a vague symptom.

## Verification checklist

At review time, verify at least one:

- Original reproduction no longer fails.
- Regression test fails before and passes after, or a new test covers the root cause.
- Related callers were checked.
- Manual path includes input, action, expected, and observed result.
- If checks cannot run, state why and provide substitute evidence.

## Anti-regression reflection

Spend a brief reflection when any signal appears: recurring bug, second fix attempt, unclear cross-layer contract, missing tests, hidden data assumption, or production incident. Only durable, reusable lessons go to knowledge-sync.

## Minimality checkpoints

Apply `minimality.md`: fix the smallest shared root cause, avoid caller-by-caller patches, avoid new abstractions/dependencies, and keep safety checks. A tiny patch with missing validation is still blocked.

## Project Sync boundary

Most bug fixes do not update architecture or requirements. Sync only when the fix changes public behavior, data format, config semantics, user-visible capability boundary, or long-lived project rule.

## Hard stops

- Coding before root cause is known on a non-trivial issue.
- Coding a bug fix without reproduction evidence or a no-repro rationale.
- Continuing after the root-cause hypothesis fails.
- Expanding bug fix into refactor or feature work.
- Claiming verification with no command, reproduction, or substitute evidence.
- Rewriting report/analysis after the fact to hide the actual investigation path.
