# Refactor playbook
## Document map

Use this map first, then open only the section needed for the current route:

- Route map
- Artifact layout
- Refusal and reroute checks
- Fastforward discipline
- Equivalence gate
- Task memory for risky refactors
- Standard scan discipline
- Method library summary
- Design discipline
- Apply discipline
- Minimality checkpoints
- Equivalence evidence options
- Project Sync boundary
- Hard stops

## Route map

| Route | Use when | Output |
|---|---|---|
| `refactor.fastforward.plan` | Single function/component/module, low risk, behavior equivalence easy to prove | compact plan |
| `refactor.fastforward.do` | Local safe change with tests or manual equivalence path | diff + equivalence evidence |
| `refactor.standard.scan-design` | Cross-module, high-risk, weak test coverage, unclear equivalence, or many candidates | scan + design/checklist |
| `refactor.standard.apply` | Approved refactor design and checklist exist | staged apply + evidence |
| `refactor.apply-verify` | Refactor is ready for closure | apply-notes / review summary |

## Artifact layout

```text
.codestable/refactors/YYYY-MM-DD-{slug}/
├── {slug}-scan.md
├── {slug}-refactor-design.md
├── {slug}-checklist.yaml
└── {slug}-apply-notes.md
```

Fastforward refactor normally creates no directory. Standard refactor creates artifacts only after scan/design is justified.

## Refusal and reroute checks

Before scan or implementation, run these checks in order:

1. Does the request require a high-risk backend prompt/schema/status/event chain audit before safe design? If yes, route to `audit-only.backend-ledger` first.
2. Does the request include behavior change? If yes, reroute to feature or issue.
3. Is there enough test or manual evidence to prove equivalence? If no, plan safety net first.
4. Is the scope cross-module or owner-spanning? If yes, use standard scan/design.
5. Are all candidates style preferences only? If yes, refuse or ask for a concrete maintainability goal.
6. Is the target generated, vendored, third-party, or intentionally frozen code? If yes, refuse or ask for scope change.
7. Is the scan scope too broad for one reviewable change? If yes, narrow it.
8. After scan, is there a real improvement with evidence? If no, stop with no-op result.

A refusal is a valid refactor outcome when it prevents unsafe churn.

## Fastforward discipline

Allowed examples: extract a small helper, inline an unnecessary wrapper, rename a local concept, split a local component, remove duplicate branches, simplify a conditional, or isolate a tiny pure function.

Required evidence:

- Existing test suite, targeted test, snapshot/golden output, API response comparison, manual UI path, or explicit uncovered-risk statement.
- One-sentence equivalence claim: what behavior should remain unchanged.

Do not add abstractions “for later.” Do not change formatting broadly unless the task is formatting.

## Equivalence gate

Before `refactor.fastforward.do` or `refactor.standard.apply`, require an equivalence proof path:

- existing tests that cover the behavior;
- characterization test added before the refactor;
- snapshot/golden output comparison;
- API response or CLI output comparison;
- manual path with expected/observed result;
- explicit uncovered-risk statement accepted by the owner.

If the proof path is missing, route to `blocked.missing-equivalence-proof`. Do not refactor on style preference alone.

## Task memory for risky refactors

Create a task capsule for standard refactors and multi-session fastforward refactors. The context pack links current behavior contract, equivalence evidence, affected callers, owner decisions, and forbidden behavior changes.

## Standard scan discipline

A scan identifies concrete, evidence-backed refactor candidates.

Scan item fields:

- ID and one-line title.
- Location and affected callers.
- Problem stated as an observable maintenance or risk issue, not just an adjective.
- Suggested method.
- Behavior-equivalence evidence needed.
- Risk and estimated size.
- User selection marker when multiple candidates exist.

Hard constraints:

- One item does one thing.
- Do not list taste-only items.
- Do not list the same location in too many unrelated items.
- Every item maps to a method or a clear local cleanup pattern.
- The summary distinguishes must-do, optional, and no-op.

## Method library summary

Choose boring, known refactor methods before inventing custom architecture:

- Behavior-equivalent migration: parallel change, strangler fig, branch by abstraction, characterization test.
- Code-level: extract function, inline function, extract variable, move function, decompose conditional, guard clauses, introduce parameter object only when repeated parameter groups are real.
- Structure: component split, container/presenter split, composable/custom hook extraction, module boundary cleanup.
- Performance/async: memoization, batching, lazy loading, N+1 elimination, index/cache, cancellation, virtualization.

Use performance methods only when there is a real performance signal and equivalence risk is understood.

## Design discipline

A refactor design must include:

- Scope and non-goals.
- Current behavior contract.
- Dependencies and preconditions.
- Execution order.
- Method choices.
- Risk and rollback.
- Equivalence verification plan.
- Explicit statement that no user-visible behavior should change.

## Apply discipline

- Apply in small, reviewable steps.
- Introduce tests or characterization before risky moves.
- Redirect one caller at a time when behavior risk exists.
- Remove old paths after new paths are verified.
- Update checklist evidence after each step.
- Stop immediately when behavior changes or requirements emerge.

## Minimality checkpoints

Refactor minimality means removing or simplifying real maintenance risk, not creating architecture for its own sake. Apply `minimality.md` before adding an abstraction; require real callers, real duplication, or a real boundary.

## Equivalence evidence options

- Unit/integration tests before and after.
- Snapshot or golden output comparison.
- CLI/API response equivalence.
- Manual UI path showing the same visible behavior.
- Static type/lint checks plus explicit uncovered behavior risk.

## Project Sync boundary

Pure internal cleanup is usually `no-sync`. Update architecture only when accepted refactor changes module boundaries, dependencies, configuration shape, public extension points, or main data/control flow.

## Hard stops

- Mixing behavior change with refactor.
- Applying broad formatting churn together with semantic refactor.
- Adding compatibility shims without removal plan.
- Introducing a new abstraction that does not remove real duplication or isolate a real boundary.
- Claiming equivalence without evidence.
- Refactoring a high-risk backend prompt/schema/status/event chain before a required completed audit ledger exists.
