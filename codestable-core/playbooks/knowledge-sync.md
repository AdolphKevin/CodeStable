# Knowledge Sync playbook
## Document map

Use this map first, then open only the section needed for the current route:

- Principle
- Target map
- Compound frontmatter
- Manual record mode
- Deduplication and intent routing
- Generic note handling
- Attention rules
- Learning rules
- Trick rules
- Decision rules
- Explore rules
- Guide rules
- Libdoc rules
- Project Sync coordination
- Index maintenance contract
- Hard stops


This is the authoritative runtime reference for durable knowledge synchronization after review or explicit manual recording. It covers attention, learning, tricks, decisions, explore docs, guide docs, and library docs. Generic `note` is intentionally not a runtime target; route durable content to the most specific target.

## Principle

Most changes should not create durable knowledge. `no-sync` is an intentional precision decision, not a skipped task.

Write knowledge only when the information will likely help future humans or AI sessions avoid mistakes, reuse a pattern, understand a decision, or use a public interface. Ephemeral attempts stay in task journal.

## Target map

| Target | Path | Write when |
|---|---|---|
| attention | `.codestable/attention.md` | Every CodeStable run must know a short hard constraint |
| learning | `.codestable/compound/YYYY-MM-DD-learning-{slug}.md` | Pitfall or knowledge with future reuse value |
| trick | `.codestable/compound/YYYY-MM-DD-trick-{slug}.md` | Reusable project-specific technique/pattern/workaround |
| decision | `.codestable/compound/YYYY-MM-DD-decision-{slug}.md` | Durable tradeoff or technical/product choice was made |
| explore | `.codestable/compound/YYYY-MM-DD-explore-{slug}.md` | Evidence-backed answer to “how does this work?” worth preserving |
| guide | project docs / `.codestable/guides/` by convention | User/dev-facing documented behavior changed |
| libdoc | `.codestable/libdoc/` by convention | Internal/external library usage/API needs durable local docs |

## Compound frontmatter

```yaml
doc_type: learning | trick | decision | explore
status: current
summary: "..."
tags: []
source: "feature | issue | refactor | review | manual"
```

Each doc type may add fields, but shared fields should stay consistent with `.codestable/reference/shared-conventions.md`.

## Manual record mode

`knowledge-sync.manual` is allowed when the user explicitly asks to record durable knowledge such as decision, learning, trick, explore, attention, guide, or libdoc. It does not require a code diff, but it does require at least one source:

- user explicitly states the decision/fact/lesson;
- a finished task journal contains a durable lesson confirmed by review;
- code anchors or docs support the claim;
- the current conversation contains a concrete investigation result;
- a reviewed feature/issue/refactor produced the knowledge.

Manual record should still deduplicate against existing compound docs, task journals, and attention. If the content has no future reuse value, report `Project Sync: no-sync` instead of writing a document.

## Deduplication and intent routing

Before writing durable knowledge:

1. Search existing compound docs, task memory, attention, guides, and libdoc for overlap.
2. Decide whether to update an existing doc, create a new doc, or skip.
3. Keep one doc focused on one durable point.
4. Ask for user review when the entry asserts a decision or changes reader-facing docs.
5. Ensure the title and tags make it discoverable later.

## Generic note handling

Do not create a generic note document type or generic-note compound file for knowledge sync. When a user asks for a generic project remark, classify it first:

- mandatory startup constraint -> attention;
- reusable pitfall or lesson -> learning;
- repeatable project technique -> trick;
- durable tradeoff or choice -> decision;
- evidence-backed code understanding -> explore;
- reader-facing usage/API information -> guide or libdoc.

If it does not fit one of these targets, ask one clarifying question or report `Project Sync: no-sync`.

## Attention rules

Good attention items are short, mandatory, and repeatedly relevant.

Good:

```text
All CodeStable workflows must run `pnpm test -- --runInBand` because this repo has shared test database state.
```

Bad:

```text
The auth module is complicated and should be handled carefully.
```

Long explanations belong in learning/explore, not attention.

## Learning rules

Use learning for pitfalls or reusable knowledge.

Common tracks:

- Pitfall: trigger, symptom, root cause, fix, prevention.
- Knowledge: concept, when it matters, project-specific interpretation, examples.

Do not store transient debugging noise. Prefer one lesson per document.

## Trick rules

Use trick for reusable “how to do X here” patterns.

Minimum sections:

- Applicable scenario.
- Method.
- Why it works.
- Example.
- When not to use it.
- Known pitfalls.
- Related docs/code anchors.

A trick requires code investigation or concrete project evidence; do not write generic advice.

## Decision rules

Use decision when a durable choice was made among alternatives.

Minimum sections:

- Background.
- Decision.
- Rationale.
- Alternatives considered.
- Consequences.
- Related docs and affected workflows.

Do not create a decision for a preference that has not actually been decided.

## Explore rules

Use explore when investigation answered a question worth preserving.

Minimum sections:

- Question and scope.
- Short answer.
- Key evidence.
- Detailed explanation.
- Unknowns.
- Follow-up suggestions.
- Related docs/code anchors.

An explore doc must be evidence-backed. If it is just speculation, keep it in the conversation.

## Guide rules

Guide docs are reader-facing. Update when public commands, setup paths, component props, SDK/API methods, user flows, or documented behavior changed.

Typical developer guide sections:

- Overview.
- Prerequisites.
- Quick start.
- Core concepts.
- API/reference.
- Common scenarios.
- Known limitations.
- Related docs.

Typical user guide sections:

- Feature overview.
- Preconditions.
- How to use.
- Expected results.
- Troubleshooting.
- Limitations.

Do not update guide docs for invisible internal refactors.

## Libdoc rules

Use libdoc when local library usage needs durable docs.

Typical files:

- `manifest.yaml` for entry inventory.
- One entry document per library/package/module concept.

Entry sections:

- Overview.
- API reference.
- Basic usage.
- Typical scenarios.
- Pitfalls and version constraints.
- Related entries.
- Source extraction checklist when generated from code.

## Project Sync coordination

`cs-review` owns the unified matrix. The knowledge-sync playbook handles compound/attention/guide/libdoc entries when the matrix says yes or when `knowledge-sync.manual` is routed explicitly. It should report paths updated and reasons for skipped candidates.

## Index maintenance contract

Knowledge Sync writes small durable knowledge entries. Keep lookup paths fresh:

- Update the authoritative detail doc first. Update the corresponding index in the same turn.
- Writing learning / trick / decision / explore must update `.codestable/compound/INDEX.md` with topic, trigger, summary, status, and detail link.
- Writing or changing a high-impact decision may also update `.codestable/INDEX.md` if it affects project-level planning or architecture navigation.
- Writing `attention.md` may update `.codestable/INDEX.md` only when the startup warning changes the project-wide working contract.
- Do not duplicate long explanations inside indexes; link to the compound doc.
- If the entry supersedes another compound doc, mark both the old doc and `compound/INDEX.md` in the same turn.

Report index work as:

```text
Index Sync: compound-index=<yes/no>, root=<yes/no>, reason=<short reason>
```

## Task-memory promotion

When closing a task, promote only durable, reusable conclusions from `tasks/*/journal.md` into compound/attention/specs. Keep failed commands, temporary debugging, and local progress notes in the task journal. If a journal item is not clearly reusable, leave it there.

## Hard stops

- Writing durable knowledge without reuse value.
- Writing a decision that the user has not actually made.
- Writing an explore doc without evidence from code/docs/conversation.
- Creating duplicate docs instead of updating an existing one.
- Putting long explanations into attention.
- Writing generic programming advice with no project evidence.
- Updating guide/libdoc for changes invisible to readers.
