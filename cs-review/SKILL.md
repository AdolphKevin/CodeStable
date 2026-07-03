---
name: cs-review
description: "CodeStable public entry for verification and knowledge freshness: acceptance, fix/refactor verification, doc-sweep, project sync, task finish, and durable learning promotion."
---

# cs-review

## Document map

- Runtime playbook map
- Startup scan
- Fixed output protocol
- User intent table
- Review and sync rules
- Doc-sweep rules
- Human gate rules
- Hard stops

`cs-review` is the public **Review / Sync / Closure** entry. It verifies that work is complete, prevents overbuild and stale documentation, finishes task memory, and promotes only durable facts into project knowledge.

Shared rules live in `../codestable-core/playbooks/`; they are auditable references, not hidden Skills.

## Runtime playbook map

| Concern | Runtime authority |
|---|---|
| Human gates / destructive approval | `../codestable-core/playbooks/collaboration.md` |
| Task finish / journal | `../codestable-core/playbooks/task-memory.md` |
| Minimality / overbuild review | `../codestable-core/playbooks/minimality.md` |
| Real-repo reliability gates | `../codestable-core/playbooks/reliability.md` |
| Feature / issue / refactor verification | `../codestable-core/playbooks/{feature,issue,refactor}.md` |
| Audit ledger evidence when reviewing audit-required work | `../codestable-core/playbooks/audit-only.md` |
| Roadmap closure and status | `../codestable-core/playbooks/roadmap.md` + `../codestable-core/playbooks/project-sync.md` |
| Architecture / requirements / roadmap / doc-sweep | `../codestable-core/playbooks/project-sync.md` |
| Decisions / learnings / tricks / explore / attention / guide / libdoc | `../codestable-core/playbooks/knowledge-sync.md` |

## Startup scan

1. Ensure `.codestable/INDEX.md` exists. If missing, stop with `Next: plan`.
2. Read `.codestable/INDEX.md`, `.codestable/attention.md`, `.codestable/reference/project-knowledge-contract.md`, and any relevant `.codestable/tasks/*/context-pack.md` or `audit-ledger.md`.
3. If the user asks to record architecture, requirements, roadmap, decision, learning, trick, explore, attention, guide, or libdoc, use manual sync with a traceable source.
4. If the user asks for 文档熵减 / doc-sweep / 清理过时文档, use `project-sync.doc-sweep` and refresh/read code inventory first.
5. Otherwise review current diff, lifecycle artifacts, task journal, checks, and related code.
6. Distinguish current-scope changes from unrelated dirty files.

## Fixed output protocol

Every response ends with:

```text
Route: <route-id>
Playbook: <codestable-core/playbooks/*.md#section or none>
Reason: <review conclusion and evidence summary>
Human Gate: none | owner-confirmation | design-approval | risk-approval | merge-approval
Owner decision: <known decision, pending question, or not-applicable>
Read: <artifact/diff/check/doc/code/task paths>
Evidence: <tests, diff, code anchors, user source, inventory, doc claim mapping>
Evidence Level: L0 | L1 | L2 | L3 | L4
Reliability Gate: pass | blocked:<reason> | not-applicable
Proof Trace: none | update:<path> | finish:<path>
Audit Ledger: not-applicable | missing | inline | create:<path> | update:<path> | read:<path> | complete:<path> | partial:<path>
Audit Status: not-applicable | 已审完 | 未审完
Overbuild Check: pass | blocked | not-applicable
Task Memory: none | update:<path> | finish:<path>
Write-intent: <actual or proposed doc updates>
Claim Matrix: <not-applicable | path -> claim -> current anchor/status>
Checks: <commands/manual paths; manual sync may be not-applicable + source>
Writeback Matrix: architecture=<yes/no>, requirements=<yes/no>, roadmap=<yes/no>, compound=<yes/no>, attention=<yes/no>, guides-or-libdoc=<yes/no>, specs=<yes/no>, task-memory=<yes/no>, doc-sweep=<yes/no>
Index Sync: root=<yes/no>, architecture-index=<yes/no>, requirements-index=<yes/no>, compound-index=<yes/no>, roadmap-index=<yes/no>, specs-index=<yes/no>, task-index=<yes/no>, doc-sweep-index=<yes/no>
Next: commit | do | plan | ask-user | stop
```

Legal `route-id` values:

```text
feature.acceptance
issue.fix-verify
refactor.apply-verify
project-sync.manual
project-sync.doc-sweep
knowledge-sync.manual
review.status-only
review.blocked-unrelated-dirty-files
review.blocked-insufficient-evidence
review.blocked-overbuild
review.blocked-weak-evidence
```

## User intent table

| User says | Route | Target |
|---|---|---|
| `cs-review：验收这个 feature` | `feature.acceptance` | Compare design/checklist/context pack/diff/checks |
| `cs-review：验证 bug 修复` | `issue.fix-verify` | Verify report/analysis/fix-note and reproduction path |
| `cs-review：检查这次重构是否等价` | `refactor.apply-verify` | Prove behavior equivalence |
| `cs-review：记录 architecture/requirements/roadmap：...` | `project-sync.manual` | Write current project facts or planning state with source |
| `cs-review：做文档熵减 / 清理过时文档 / doc-sweep` | `project-sync.doc-sweep` | Code-grounded claim classification report; no deletion by default |
| `cs-review：记录 decision/learning/trick/explore/attention/guide/libdoc：...` | `knowledge-sync.manual` | Durable reusable knowledge with source or code anchor |
| Evidence below required level for closure or mutation | `review.blocked-weak-evidence` | Stop with missing evidence list and next route |

Generic `note` is not a durable type. Classify it or ask.

## Review and sync rules

- Verification first, writeback second. Do not use documentation updates to hide incomplete work.
- Detail doc first, scoped index second, root index last.
- Finish task memory by updating task status/journal/proof trace before promoting durable facts.
- Run the overbuild check: dependencies, abstractions, broad churn, custom platform replacements, missing safety checks.
- If the diff implements audit-required backend work, verify it references a completed audit ledger and a bounded fix item from that ledger.
- Use `no-sync` when no durable fact changed.

## Doc-sweep rules

Doc-sweep is a two-step operation:

1. **Audit**: refresh/read code inventory, map each document claim to current code anchors / current index / newer doc / unknown, and write a report with a `Claim Matrix`.
2. **Mutation**: archive/delete/rewrite only after explicit user approval with exact path list and rollback note.

Classifications are only `current`, `unverified`, `conflicts-with-code`, `superseded-by`, and `archive-candidate`. Unknown is not stale.

## Human gate rules

Use `risk-approval` before destructive doc changes, migrations, broad rewrites, security-sensitive decisions, or roadmap closure with ambiguity. Use `merge-approval` before commit/close operations. Manual sync requires user source, reviewed diff, code anchor, or existing doc anchor.

## Hard stops

- Review without verification evidence.
- Reviewing audit-required backend work without a completed audit ledger.
- Closing tasks without finishing the proof trace when one exists.
- Manual sync without traceable source.
- Doc-sweep based only on old docs.
- Marking task done while checks or owner gates are pending.
- Writing future plans as current architecture.
- Deleting or archiving docs without explicit confirmation.
