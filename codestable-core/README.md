# CodeStable Core Playbooks

`codestable-core/` 是 CodeStable runtime 的共享工程纪律库，不是可发现 Skill。这里的文件只给 `cs-plan` / `cs-do` / `cs-review` 读取，宿主不会因为这里有规则就多发现一个技能。

## Why playbooks

v6 开始把共享工程纪律统一建模为 **playbook**：

- 明确支持哪些 route；
- 明确由哪个入口拥有写权限；
- 明确输入、证据、禁止事项和输出；
- 便于调试时直接定位到单一权威文件。

## Debugging contract

三个入口的输出都包含：

```text
Route: ...
Playbook: codestable-core/playbooks/<name>.md#<section>
Evidence: ...
Next: ...
```

当效果不满意时，优先调对应 playbook 的 route 小节。

## Maintenance rules

- Do not copy playbooks into individual Skill directories.
- Entry Skills reference playbooks by package-relative path, for example `../codestable-core/playbooks/feature.md`.
- Onboard copies `codestable-core/onboard/reference/` and `codestable-core/onboard/tools/` into the target project as `.codestable/reference/` and `.codestable/tools/`.
- This directory must not contain `SKILL.md`; it must not participate in Skill discovery.
