# CodeStable Core References

This directory is a package-level support library, not a discoverable Skill. It contains the single authoritative executor references and onboard assets used by `cs-plan`, `cs-do`, and `cs-review`.

## Maintenance rules

- Do not copy `feature.md`, `issue.md`, `refactor.md`, or `roadmap.md` into individual Skill directories.
- Entry Skills should reference these files by package-relative path, for example `../codestable-core/references/executors/feature.md`.
- Onboard copies `codestable-core/onboard/reference/` and `codestable-core/onboard/tools/` into the target project as `.codestable/reference/` and `.codestable/tools/`.
- This directory must not contain `SKILL.md`; it must not participate in Skill discovery.
