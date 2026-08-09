# Core Contract

## Contents

1. Shared six-layer architecture
2. Validation shapes
3. Review topologies
4. Setup blueprint
5. Required tests
6. Anti-patterns

## 1. Shared six-layer architecture

### Layer 1: Business truth

Choose one accepted source of truth: SOP, product requirement, quality standard, or frozen Oracle.
Record who owns it and which behavior is explicitly out of scope. A model-generated scenario is a
draft until the business boundary is reviewed.

### Layer 2: Executable scenario

Give each suite, case, and turn a stable identity. Model input should look like real input. For open
language output, describe expected meaning and forbidden commitments without fixing one sentence.
Keep deterministic contracts in typed tests unless the project's scenario schema explicitly owns
them.

### Layer 3: Production-shaped execution

Enter through the same service or orchestration boundary used by the product. Preserve normal
authorization, state, transaction, effect, provider, retry, and concurrency boundaries. A fake may
stand in for an external system only at its accepted integration boundary; it must not replace the
reasoning or business implementation under test.

### Layer 4: Immutable evidence

Use a unique run ID and a new output directory. Bind source, configuration, suite, fixture, runtime,
and model identities as appropriate. Record execution status separately from quality. A complete
dialogue artifact normally includes expected/actual transcript, sanitized trace, business actions,
state or commit evidence, metrics, manifest, triage, cleanup, and relevant debug logs. A stateful
service or comparison experiment may use a sealed Evidence Pack instead.

### Layer 5: Independent review

Give the reviewer a frozen, verified evidence set and a strict policy. Require evidence citations
for substantive conclusions. Bind the review to exact hashes. The reviewer may apply semantic
judgment but must not recalculate runner-owned objective metrics, mutate evidence, call the system
under evaluation, or invent release authority.

### Layer 6: Durable regression

Record the earliest failed authority boundary, root cause, evidence, and allowed fix scope. After a
fix, rerun the target case, affected set, and full set required by the project. Store stable rules in
scenarios, deterministic tests, docs, and project knowledge.

## 2. Validation shapes

### Dialogue Agent

Use when quality depends on natural-language understanding and real business actions. The decisive
comparison is user input + expected meaning + actual reply + authoritative action/state evidence.
Execution success cannot prove semantic completeness.

### Stateful AI service

Use when quality is primarily observable through API results and persistence. Keep Worker inputs
free of Oracle, score, pass/fail, rubric, or reviewer policy. Freeze raw requests/responses,
before/after state, model/source timing, idempotency, and isolation proof.

### Comparative evaluation

Use when two or more arms are compared. Freeze identical scenario identities, repetitions, budgets,
model/tool configuration, order-balancing method, and objective metrics. Let deterministic code own
counts, latency, cost, and assertion results. Limit Codex to policy-delegated qualitative assessment
and adoption advice.

## 3. Review topologies

### Development review

Use when a developer deliberately asks Codex to validate a run. The runner never calls the reviewer.
Codex reads the run in the development workflow, writes a review into the artifact root, and then
runs a local validator. Application runtime code never imports, launches, waits for, or consumes the
reviewer.

### Isolated review launcher

Use only when the repository deliberately implements an acceptance-only judging mechanism. Keep it
in a separate package/process from the runner and product. Before launch:

- verify a complete frozen pack;
- copy only required evidence, policy, schema, runtime, and isolated authentication;
- use an explicit reviewer model;
- remove evaluated-system, provider, database, and unrelated credentials;
- prove the filesystem sandbox can read allowed files, cannot read siblings, cannot alter frozen
  evidence, and can write only the designated output tree;
- fail closed as unavailable if any boundary is missing.

Preserve the raw model output and let the launcher own provenance, pack digests, model identity,
tool identity, timestamps, and terminal sealing.

## 4. Setup blueprint

Create repository-native equivalents of the following only when absent:

```text
scenario schema and examples
runner and focused/full entry points
artifact writer and run manifest
triage and cleanup evidence
reviewer policy and strict review schema
review validator and tamper tests
project rule describing the boundary
```

Required design decisions:

1. What is the production-shaped entry?
2. What may be simulated, and at which provider boundary?
3. Which facts are deterministic assertions versus semantic expectations?
4. How are cases isolated across run, conversation, database, queue, and effect state?
5. Which files prove a run is complete?
6. How is source/config/suite drift detected?
7. Who writes the review and who validates it?
8. What does each verdict mean?
9. Which data must be redacted before logging or review?
10. Which focused and full runs establish acceptance?

When adapting an existing system, make the new contract a hard cut. Update all consumers and delete
the obsolete path after validation; do not keep adapters, fallback, or dual review formats.

## 5. Required tests

At minimum, test:

- strict scenario parsing and duplicate identities;
- real production entry selection;
- unique run/artifact roots and no overwrite;
- source/config/suite drift invalidation;
- cleanup and isolation failure classification;
- transcript/trace/action/state/metric completeness;
- secret and sensitive-data redaction;
- review schema validation;
- artifact hash mismatch and path traversal rejection;
- verdict consistency, including blocking finding versus pass;
- reviewer unavailable behavior for isolated launchers;
- one end-to-end fixture run that creates and verifies a complete review.

Run one representative real Scenario after deterministic tests. Do not call a fixture-only run proof
of real-model or production readiness.

## 6. Anti-patterns

- Embedding expected answers or Oracle data in Worker/model input.
- Grading by keyword, regex, or exact localized sentence.
- Looking only at final text while ignoring actions and persistence.
- Treating a trace status or provenance identity as semantic correctness.
- Recomputing or changing deterministic metrics during review.
- Reviewing a live, changing artifact directory.
- Copying a later review into an earlier run or rehashing a mismatched review.
- Using a focused pass as a full release conclusion.
- Running an unconstrained reviewer after an isolation failure.
- Adding a second runner/reviewer instead of updating the accepted path.
