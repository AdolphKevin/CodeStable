# Human-AI Collaboration Contract
## Document map

- Ownership
- Gates
- Evidence
- History

## Ownership

The human owns product intent, architectural tradeoffs, destructive changes, risk tolerance, and merge/commit approval. AI owns reading code, proposing options, implementing scoped work, running checks, and recording evidence.

## Gates

Use gates when a task changes durable direction:

- `owner-confirmation`: unclear product or architecture decision.
- `design-approval`: standard feature/refactor/roadmap design.
- `risk-approval`: migration, deletion, security-sensitive or broad rewrite.
- `merge-approval`: commit, close roadmap, archive/delete docs.

## Evidence

Every durable claim needs at least one of: code anchor, test/check output, user decision, current doc anchor, or reviewed diff.

## History

Approved designs and analyses are history. Do not rewrite them to match implementation. Record accepted divergences in acceptance, fix-note, apply-notes, or a dated addendum.
