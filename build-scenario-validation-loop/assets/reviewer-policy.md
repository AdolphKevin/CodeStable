# Scenario Evidence Review Policy

Review one completed and frozen Scenario run. Apply the accepted SOP and case expectations without
adding or weakening criteria.

## Required input

- scenario source and user-visible expected outcomes;
- final run manifest and source/config/suite identities;
- complete expected/actual transcript or request/response evidence;
- sanitized trace, business actions, state/commit or persistence evidence;
- typed metrics, triage, cleanup, and relevant debug logs.

Return `BLOCKED` when required evidence is missing, mismatched, mutable, or insufficient.

## Procedure

1. Verify artifact integrity and run identity.
2. Inspect every required case and turn.
3. Compare actual language, actions, state, and exact values with the expected outcome.
4. Record each blocking deviation at its earliest authority boundary with evidence references and a
   narrow recommended fix boundary.
5. Keep non-blocking observations separate.
6. Bind the output to the exact reviewed artifact hashes.

## Verdicts

- `PASS`: the run is complete and has no blocking finding.
- `FAIL`: at least one observed contract, semantic, action, state, safety, or integrity failure
  exists.
- `BLOCKED`: the reviewer cannot decide reliably from the available evidence.

Do not call the evaluated service, modify evidence, recompute deterministic metrics, copy secrets,
or infer success from the runner summary alone.
