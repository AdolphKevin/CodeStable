# explore playbook

`explore.plan` 是一次**定向代码探索**，由 `cs-plan` 直接执行。它不是独立 Skill，也不是长期知识写回；长期沉淀只在用户后续通过 `cs-review：记录 explore 结论：...` 时发生。

## When to use

Use this route when the user asks to understand code without asking for a code change, for example:

- “这个模块怎么实现？”
- “先摸一下这段代码。”
- “解释一下请求从哪里进来。”
- “帮我找这段逻辑相关文件。”

Do not route to `explore.plan` when the user asks to implement, fix, refactor, or decide a product direction. Those should become feature / issue / refactor / roadmap routes.

## Execution steps

1. State the exploration question in one sentence.
2. Read `.codestable/attention.md` if present.
3. Search only the likely code paths first: filenames, symbols, routes, tests, API handlers, config.
4. Read enough files to support an answer; avoid whole-repo wandering.
5. Produce an evidence-backed map: entry points, main flow, key data structures, side effects, tests, and uncertainties.
6. Recommend the next CodeStable route only when useful: feature, issue, refactor, roadmap, or stop.

## Write rules

Default: **no file writes**.

`cs-plan` must not create `.codestable/compound/*-explore-*.md` during `explore.plan`. Exploration is a read activity; durable knowledge persistence belongs to `cs-review` using a user-visible “记录 explore 结论” request.

When the user asks to save the exploration, or the result is clearly future-reusable, `cs-plan` should output a `Long-term record candidate` with:

- the proposed target type: `explore`;
- evidence paths / symbols / tests;
- facts separated from hypotheses;
- why the conclusion is reusable;
- a suggested next command: `cs-review：记录 explore 结论：...`.

This keeps exploration execution and durable knowledge writeback separate.

## Output shape

```text
Route: explore.plan
Playbook: codestable-core/playbooks/explore.md#execution-steps
Reason: <why this is code exploration, not feature/issue/refactor>
Read: <paths/symbols inspected>
Evidence: <paths/symbols/tests that support the answer>
Write-intent: none
Long-term record candidate: <none | explore record candidate for cs-review>
Next: stop | review | plan
```

Then include:

```text
Question: <the question explored>
Evidence map:
- <path>: <what it proves>
Flow summary: <concise explanation>
Uncertainties: <unknowns or paths not checked>
Long-term record candidate: <none | evidence summary suitable for `cs-review：记录 explore 结论：...`>
Recommended next route: <none or CodeStable route>
```

## Hard stops

- Do not change code during exploration.
- Do not create feature/issue/refactor artifacts unless the user asks to continue into that workflow.
- Do not write long-term compound entries from `cs-plan`; hand durable explore persistence to a later `cs-review：记录 explore 结论：...` request.
- Do not treat long-term knowledge writeback as the implementation of exploration; it is only a later persistence decision.
