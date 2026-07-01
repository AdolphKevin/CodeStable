# Design synthesis
## Document map

- CodeStable core philosophy
- Trellis-inspired parts
- Ponytail-inspired parts
- What CodeStable intentionally does differently

## CodeStable core philosophy

CodeStable keeps the original principle: orchestrate software lifecycle entities, not autonomous agent roles. The durable center is the project knowledge tree: requirements, architecture, roadmap, features, issues, refactors, compound knowledge, scoped specs, and task memory.

The human remains the owner of product intent, architecture tradeoffs, risk tolerance, destructive doc cleanup, and merge/commit decisions. AI is the fast reader, implementer, verifier, and evidence recorder.

## Trellis-inspired parts

- Repo-persisted standards: `.codestable/specs/INDEX.md` and scoped spec docs.
- Task-centered context: `.codestable/tasks/YYYY-MM-DD-{slug}/context-pack.md`, `journal.md`, and `proof.md`.
- Finish loop: `cs-review` verifies work, closes task memory, and promotes durable learnings into project knowledge.
- Platform portability: public entries are regular Skills; project memory lives in the repo.

## Ponytail-inspired parts

- Minimality ladder in `codestable-core/playbooks/minimality.md`.
- Plan output includes `Minimality Plan`.
- Do output includes `Minimality` and reuse evidence.
- Review output includes `Overbuild Check`.
- Safety floor prevents minimality from cutting validation, security, accessibility, or data-safety checks.

## What CodeStable intentionally does differently

- It keeps only three lifecycle entry points, instead of many workflow commands.
- It separates read-only exploration from durable knowledge recording.
- It makes doc-sweep audit-first and code-grounded; destructive cleanup requires explicit human approval.
- It treats generated code inventory as evidence map, not product truth.
