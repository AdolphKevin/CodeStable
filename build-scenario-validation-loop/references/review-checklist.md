# Review Checklist

## Contents

1. Integrity preflight
2. Evidence reading order
3. Semantic and business judgment
4. Findings and observations
5. Verdict and binding
6. Reporting

## 1. Integrity preflight

Before judging quality:

- resolve one explicit artifact root or Evidence Pack;
- verify it is complete and frozen using the project validator;
- verify run ID, source/config/suite/model/runtime identities and budgets as required;
- verify no source or suite drift invalidated the run;
- verify cleanup, isolation, and execution completion evidence;
- verify required files exist and hashes match;
- verify reviewer inputs exclude secrets and forbidden Oracle data;
- for a comparison, verify every required arm, scenario, and repetition is present exactly once.

If required evidence is missing, corrupted, mutable, or mismatched, use the project's unavailable
verdict (`BLOCKED`, `needs_review`, or equivalent). Do not guess.

## 2. Evidence reading order

Read in this order unless local policy says otherwise:

1. scenario/SOP/Oracle and reviewer policy;
2. start and final manifest plus source/config/suite identities;
3. triage, execution summaries, and cleanup/isolation results;
4. complete expected/actual transcript or API request/response evidence;
5. sanitized trace, provider calls, business actions, effects, and commits;
6. before/after persistence and state versions;
7. typed metrics, latency, token, cost, retry, and budget evidence;
8. relevant debug errors and external worker results;
9. existing deterministic assertion results;
10. review schema and required evidence-reference shape.

Read every relevant turn/case. Sample only if the accepted policy explicitly authorizes sampling.

## 3. Semantic and business judgment

For dialogue Agents, ask for each turn:

- Did the system understand every independent request?
- Did it preserve relevant context across turns and languages?
- Did it ask only for actually missing information?
- Did it wait for required confirmation?
- Does every claimed success/failure/unknown state match authoritative action and commit evidence?
- Are exact values, cards, links, and identifiers bound to authoritative data?
- Did it invent policy, eligibility, human work, timing, or future action?
- Did it expose sensitive or private values?

For stateful services, ask for each case:

- Was the input identity and source trusted?
- Did the model/service choose the correct operation?
- Do response and before/after state match the Oracle?
- Are retry, idempotency, transaction, isolation, deletion, and expiry semantics correct?
- Did the Worker receive any Oracle, score, rubric, or reviewer information?

For comparative evals:

- Accept runner-owned objective metrics as immutable after verifying evidence integrity.
- Judge only the qualitative dimensions assigned by policy.
- Cite paired evidence for each preference or adoption statement.
- Keep unknown cost, token, coverage, or reliability as insufficient evidence.

Judge meaning, not keywords. Equivalent expressions across languages can pass. Fluent prose cannot
override contradictory action/state evidence.

## 4. Findings and observations

For each blocking problem, record:

- suite/case/turn or pair identity;
- the earliest authority boundary where behavior diverged;
- concise root cause;
- exact evidence references and hashes;
- the narrow recommended fix boundary.

Use an observation only when the deviation does not authorize a false business fact, alter an
effect/state, hide an independent request, violate safety/privacy, or cross another project-defined
hard boundary. Never downgrade a blocking problem to preserve a pass.

Keep environment/fixture/runner failures distinct from product semantic failures. A safe response to
a broken fixture may still be semantically correct, while the overall run remains unavailable.

## 5. Verdict and binding

Use the local verdict vocabulary. If none exists, use:

- `PASS`: execution is acceptable, all required evidence is present, and there is no blocking
  finding;
- `FAIL`: at least one observed contract, safety, semantic, action, state, or evidence-integrity
  failure exists;
- `BLOCKED`: evidence or environment is insufficient to decide credibly.

Bind every reviewed artifact required by policy. Prefer repository-relative paths and lowercase
SHA-256. Reject path traversal and absolute references outside the frozen root. Validate the final
review with the project tool and, when useful, the bundled `verify_review_bindings.py`.

Do not revise a frozen review in place to represent a new source, policy, schema, or evidence set.
Create a new run or review output.

## 6. Reporting

Always report two independent results:

```text
execution status: <runner/pack result>
review status: <Codex/project verdict>
```

Also report the run ID, artifact root, scale, blocking findings, non-blocking observations,
verification command, and material limitations. A local/focused pass must be labeled local/focused;
it cannot approve the full release.
