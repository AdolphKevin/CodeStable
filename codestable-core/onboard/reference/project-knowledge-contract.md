# CodeStable 项目知识索引契约
## Document map

Use this map first, then open only the section needed:

- Read contract for every CodeStable entry
- Index files and detail files
- Plan-time read path
- Do-time read path
- Review-time writeback path
- Freshness and drift rules

## Read contract for every CodeStable entry

Every `cs-plan`, `cs-do`, and `cs-review` run starts with:

1. Read `.codestable/INDEX.md`.
2. Read `.codestable/attention.md`.
3. Read this file when index/update behavior matters.
4. Use index files to decide which detailed documents to open.

Do not full-scan `.codestable/architecture/`, `.codestable/requirements/`, or `.codestable/compound/` unless the user asks for an audit/doc-sweep.

## Index files and detail files

| Layer | Index | Detail files |
|---|---|---|
| Requirements | `.codestable/requirements/VISION.md` | `.codestable/requirements/{slug}.md` |
| Architecture | `.codestable/architecture/ARCHITECTURE.md` | `.codestable/architecture/{type}-{slug}.md` or grouped subdirs |
| Roadmap | `.codestable/roadmap/{slug}/{slug}-roadmap.md` | `{slug}-items.yaml`, child feature docs |
| Compound | `.codestable/compound/INDEX.md` | `.codestable/compound/YYYY-MM-DD-{doc_type}-{slug}.md` |
| Attention | `.codestable/attention.md` | optional links to compound / architecture docs |

Indexes contain summaries and links, not long explanations. Detailed documents contain durable facts, evidence, and change notes.

## Plan-time read path

`cs-plan` should:

1. Read `.codestable/INDEX.md` and `.codestable/attention.md`.
2. Identify the likely route.
3. Read only the relevant index layer: requirements, architecture, compound, or roadmap.
4. Open detailed docs only when an index entry names a module, capability, decision, pitfall, or roadmap item that may constrain the plan.
5. Mention conflicts or outdated knowledge in `Reason` and route to `ask-user` when the current source of truth is ambiguous.

## Do-time read path

`cs-do` should:

1. Read the current feature/issue/refactor artifact first.
2. Read `.codestable/INDEX.md` and `.codestable/attention.md`.
3. Use indexes to open only the detailed docs that constrain implementation.
4. If code evidence contradicts an index, do not silently fix docs during implementation; finish or stop and leave Project Sync for `cs-review`.

## Review-time writeback path

`cs-review` owns durable knowledge freshness:

1. Verify the change or manual source.
2. Update detailed current-fact docs first.
3. Update the corresponding index in the same turn.
4. Update `.codestable/INDEX.md` when a new major capability/module/decision/roadmap appears, is renamed, or becomes outdated.
5. Report `Index Sync` with yes/no for root, architecture, requirements, compound, and roadmap indexes.

If an index would only duplicate unchanged text, write `Index Sync: no-change` and explain why.

## Freshness and drift rules

- Do not let an index point to a missing or superseded detail file without marking it.
- Do not update an index without updating or verifying the linked detail file.
- Do not write future plans as current architecture.
- Do not use generic notes; classify durable knowledge as attention, decision, learning, trick, explore, guide, or libdoc.
- Prefer small index entries with strong links over large summaries that will drift.
