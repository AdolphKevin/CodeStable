# Feature workflow reference
## Document map

Use this map first, then open only the section needed for the current route:

- Route map
- Artifact layout
- Brainstorm discipline
- Fastforward discipline
- Standard design discipline
- Checklist discipline
- Implementation discipline
- Acceptance discipline
- Roadmap handoff
- Project Sync candidates
- Hard stops

## Route map

| Route | Use when | Runtime artifact |
|---|---|---|
| `feature.brainstorm` | Intent is real but success criteria, non-goals, options, or ownership are unclear | optional `{slug}-brainstorm.md` |
| `feature.fastforward.plan` | Small, local, low-risk user-visible change with clear bounds | usually no directory; optional `{slug}-ff-note.md` after do |
| `feature.fastforward.do` | The fastforward boundary is already clear and implementation is safe | code diff + validation evidence |
| `feature.standard.design` | Cross-module, public API, data model, permissions, billing, security, migration, or design tradeoff exists | `{slug}-design.md`; after approval `{slug}-checklist.yaml` |
| `feature.standard.implement` | Approved design and checklist exist | checklist evidence updates |
| `feature.acceptance` | Implementation is ready for review | `{slug}-acceptance.md` or compact acceptance summary |

## Artifact layout

```text
.codestable/features/YYYY-MM-DD-{slug}/
├── {slug}-brainstorm.md   # optional discovery artifact
├── {slug}-design.md       # standard flow only
├── {slug}-checklist.yaml  # standard flow after design approval
├── {slug}-acceptance.md   # standard review / closure
└── {slug}-ff-note.md      # fastforward flow; mutually exclusive with standard docs unless explicitly upgraded
```

## Brainstorm discipline

Use brainstorm when the user is exploring, not when the task is already implementable. Keep it conversational but evidence-aware.

Minimum sections:

- What the user wants and why.
- Options discussed and current preference.
- Decisions already made.
- Open questions and next step.
- Whether this should become feature fastforward, feature standard, roadmap, issue, refactor, or no-op.

Do not turn every discussion into durable docs. Create a brainstorm artifact only when it will help future planning or when the user asks to preserve the exploration.

## Fastforward discipline

Fastforward is the default for small, clear feature work. It is not “no process”; it compresses process into bounded implementation and explicit evidence.

Fastforward is allowed only when all are true:

- No public API, data model, permissions, billing, security, migration, or configuration contract changes.
- No unresolved option requires user decision.
- The change fits existing component/service/type/test patterns.
- Validation can be done with a small command or explicit manual path.
- The diff can stay scoped to the requested behavior.

Before writing code, check:

- Where should this live in the existing structure?
- Is there an existing helper/type/component/service/test to reuse?
- Can the behavior be added without a new abstraction, dependency, plugin mechanism, cache, queue, or configuration layer?
- Are we patching symptoms instead of changing the right boundary?
- Are unrelated dirty files present?

Fastforward final output must include goal, non-goals, changed scope, verification evidence, and intentionally-not-done items. Write `{slug}-ff-note.md` only when it improves future traceability.

## Standard design discipline

Use standard design when the feature changes durable project facts or has meaningful uncertainty.

Design minimum sections:

- Problem / user outcome.
- Success criteria and acceptance contract.
- Non-goals.
- Terminology and orchestration: current behavior → proposed behavior.
- Existing evidence: code, architecture, requirements, decisions, roadmap item.
- Proposed interface / data / behavior contract.
- Implementation outline and affected modules.
- Risks, rollback, and uninstall/removal path.
- Verification plan.
- Open questions and user decisions.

Rules:

- Do not decide unresolved product or architecture tradeoffs on behalf of the user.
- Write objectives and constraints so they can be verified.
- Every feature should be removable or reversible in principle.
- Do not generate checklist or write code until the design is approved or the user explicitly combines phases.

## Checklist discipline

A feature checklist is an execution plan, not a file-by-file script.

Rules:

- 4–8 steps for normal work.
- Each step has a separately verifiable exit signal.
- Steps should describe behavior increments, safety nets, or integration points.
- Do not encode exact file:line targets unless the design truly requires them.
- `steps[].evidence` is written by implementation.
- `checks[].status` is updated by review / acceptance, not during implementation.

## Implementation discipline

During `feature.standard.implement`:

- Execute the current checklist step only.
- Preserve design terminology.
- Do not add design concepts, data flows, or abstractions not present in the approved design.
- Stop when implementation reveals a design gap, public contract change, or new user choice.
- Update evidence after each completed step: what changed, how it was verified, and remaining risk.

Implementation self-check:

- Files touched are inside the intended scope.
- No unrequested dependency or framework layer was added.
- No patch branches were added to hide a deeper mismatch.
- Tests or manual paths cover the user-visible contract.
- New logic has a nearby home consistent with project patterns.

## Acceptance discipline

Acceptance compares the final diff against the approved goal, non-goals, design contract, checklist evidence, and roadmap item when present.

Acceptance should record:

- What was delivered.
- How it was verified.
- Which acceptance checks passed or failed.
- Any accepted deviation from the original design.
- Project Sync candidates.

Do not rewrite the approved design to match what happened. If implementation diverged, write that divergence into acceptance.

## Roadmap handoff

When a feature originates from a roadmap item:

- Design frontmatter records `roadmap` and `roadmap_item`.
- The item moves from `planned` to `in-progress` when implementation begins.
- After acceptance, review/project-sync updates the item to `done`; if closure is blocked, it records the blocker in roadmap notes/status without inventing item statuses outside the roadmap schema.
- Roadmap closure does not imply architecture/requirements changes unless current facts changed.

## Project Sync candidates

Feature closure must always provide the matrix:

```text
architecture=<yes/no>, requirements=<yes/no>, roadmap=<yes/no>, compound=<yes/no>, attention=<yes/no>, guides-or-libdoc=<yes/no>
```

Most fastforward work is `no-sync`. Standard features often update requirements and sometimes architecture. Write durable docs only when there is a concrete signal.

## Hard stops

- Starting feature work without reading `.codestable/attention.md` when it exists.
- Upgrading a small task into roadmap/design just to create records.
- Implementing before design approval when standard design is required.
- Quietly changing API, data, permissions, security, or migration scope during implementation.
- Rewriting historical design/checklist/acceptance to hide actual sequence.
