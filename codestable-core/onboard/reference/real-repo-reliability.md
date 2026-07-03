# Real Repo Reliability Contract
## Document map

- Evidence levels
- Proof trace
- Bug fix contract
- Refactor contract
- Audit-only contract
- Review/doc-sweep contract

## Evidence levels

- L0: user intent only.
- L1: current docs or `.codestable` index.
- L2: current code/manifests/config/tests anchors.
- L3: executable command output or reproduction path.
- L4: before/after proof.

Use the highest level available. Do not close non-trivial code work below L3 unless the missing evidence is explicitly documented. Do not mark audit-only `已审完` unless every relevant module has L2 current code/config/test anchors.

## Proof trace

Non-trivial work stores compact proof in `tasks/YYYY-MM-DD-{slug}/proof.md`. The proof trace links the contract, before-change evidence, diff evidence, validation evidence, and writeback decisions.

## Bug fix contract

Start from symptom and reproduction. If reproduction is unavailable, record the exact no-repro rationale and substitute validation. Do not stack patches when a fix fails; return to analysis.

## Refactor contract

Refactor requires a behavior contract and equivalence proof path before editing. Behavior change routes to feature or issue.

## Audit-only contract

Audit-only backend reviews require a file-level ledger before fixes when the chain is cross-module and involves prompt, schema, status fields, or events. Every prompt/schema needs path, fields, caller, and downstream consumer. If any row is partial, final status is `Audit Status: 未审完`, and `cs-do` stays blocked.

## Review/doc-sweep contract

Review requires evidence, overbuild check, task finish, and writeback matrix. Doc-sweep treats documents as claims and maps them to current code or superseding sources before any mutation.
