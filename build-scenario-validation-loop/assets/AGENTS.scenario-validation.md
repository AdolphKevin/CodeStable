# Scenario Validation Boundary

- Treat Scenario runner output as execution evidence, not as the final quality verdict.
- When Codex performs Scenario validation, inspect the complete expected/actual result, sanitized
  trace, business actions, state or persistence evidence, metrics, manifest, triage, cleanup, and
  relevant debug logs required by the local contract.
- Write the final review in the artifact root using the repository's strict schema and bind it to
  the exact reviewed evidence. A run without a valid review cannot be reported as Codex-reviewed.
- Keep the reviewer outside production and ordinary test runtimes. A dedicated acceptance-only
  reviewer launcher is allowed only when the repository explicitly defines and tests an isolated,
  fail-closed boundary.
- Keep execution status and review status separate. Do not stitch passing cases across different
  source, configuration, suite, fixture, or model snapshots.
- Redact secrets, credentials, private identities, and unnecessary raw user content from artifacts
  and reviews.
