# Onboard playbook
## Document map

Open only the section needed:

- Purpose
- Routes
- Code-aware initialization contract
- Required project scan
- Files created or refreshed
- Route procedures
- Existing `.codestable/` migration
- Output protocol
- Hard stops

## Purpose

Onboard is not a skeleton-only bootstrap. Its job is to make `.codestable/` immediately useful for the current repository by grounding the first project index in actual code, manifests, tests, config, and README evidence.

Owned by: `cs-plan`.

## Routes

| Route | Use when | Writes |
|---|---|---|
| `onboard.required` | `.codestable/` is missing | Full code-aware initialization |
| `onboard.repair` | Skeleton exists but required files/tools/reference are missing or still empty templates | Missing assets + code-aware fill for empty placeholders |
| `onboard.refresh-knowledge` | User asks to reorganize/refresh `.codestable` from current implementation | Refresh inventory and indexes; mark stale candidates; no deletion |
| `onboard.status` | User only asks for status and skeleton is complete | No writes |

## Code-aware initialization contract

A successful `onboard.required` must create more than empty files:

1. Build a code inventory from the current repo.
2. Read high-signal sources: `README*`, package/build manifests, app entrypoints, route/API files, database/schema files, config files, tests.
3. Generate `.codestable/INDEX.md` with observed stack, entrypoints, module map, commands, and links.
4. Generate `.codestable/architecture/ARCHITECTURE.md` as an observed architecture index with code anchors and confidence.
5. Generate `.codestable/requirements/VISION.md` as an inferred capability index; label unconfirmed product intent as `inferred-needs-owner-confirmation`.
6. Generate `.codestable/attention.md` with only operational facts observed from manifests/config/tests; do not invent project owner preferences.
7. Copy runtime reference/tools from the package.

Use this confidence vocabulary:

- `observed`: confirmed by code/manifests/tests.
- `documented`: stated by README/docs but not verified in code.
- `inferred`: likely from filenames/routes/UI but not confirmed.
- `unknown`: not enough evidence.

## Required project scan

After creating `.codestable/tools/`, run or emulate:

```bash
python .codestable/tools/scan-project.py --root . --json .codestable/reference/code-inventory.json --markdown .codestable/reference/code-inventory.md
```

If Python is unavailable, manually produce the same two artifacts with equivalent content. Always exclude `.git/`, `node_modules/`, build outputs, virtualenvs, cache directories, and `.codestable/` itself from code inventory.

Inventory must include:

- detected package manager / language / framework hints;
- manifests and important config files;
- source directories and likely app entrypoints;
- tests and validation commands;
- API/route/schema/data-model hints when detectable;
- candidate modules with file counts and representative anchors.

## Files created or refreshed

Required directories:

```text
.codestable/
├── INDEX.md
├── attention.md
├── requirements/
│   └── VISION.md
├── architecture/
│   └── ARCHITECTURE.md
├── roadmap/
├── features/
├── issues/
├── refactors/
├── doc-sweeps/
├── compound/
│   └── INDEX.md
├── reference/
│   ├── project-knowledge-contract.md
│   ├── code-inventory.json
│   └── code-inventory.md
└── tools/
```

`reference/` and `tools/` are package-managed and may be refreshed from `codestable-core/onboard/`. User-maintained project docs are not overwritten blindly.

## Route procedures

### `onboard.required`

1. Create required directories.
2. Copy package-managed `codestable-core/onboard/reference/` to `.codestable/reference/` and `codestable-core/onboard/tools/` to `.codestable/tools/`.
3. Generate code inventory.
4. Create code-informed `INDEX.md`, `ARCHITECTURE.md`, `VISION.md`, `compound/INDEX.md`, and `attention.md` using `codestable-core/onboard/reference.md` templates.
5. Report observed facts, unknowns, and owner-confirmation candidates.

### `onboard.repair`

1. Copy/refresh package-managed reference/tools.
2. Create missing required files.
3. If an index is empty or still says `骨架（待填充）` / `skeleton`, refresh it from current code inventory.
4. Do not overwrite non-empty user-maintained documents; instead add a “refresh suggestion” section or report conflict.

### `onboard.refresh-knowledge`

1. Refresh code inventory.
2. Re-read `INDEX.md`, `ARCHITECTURE.md`, `VISION.md`, `compound/INDEX.md`, `attention.md`.
3. Update index summaries that are clearly stale based on current code anchors.
4. Mark stale/conflicting facts as `needs-review` or `stale-candidate`; do not delete old documents.
5. If broad rewrites would be needed, write a refresh report and ask the user before changing large docs.

Suggested report path:

```text
.codestable/doc-sweeps/YYYY-MM-DD-code-knowledge-refresh/index.md
```

### `onboard.status`

No writes. Report:

- required files present/missing;
- code inventory freshness;
- whether indexes appear code-informed or still placeholders;
- detected risks and next command.

## Existing `.codestable/` migration

When old project docs exist, use this rule:

- Package-managed reference/tools can be refreshed.
- User-maintained architecture/requirements/compound/roadmap docs are never deleted during onboard.
- If current code conflicts with existing docs, mark conflict and route cleanup to `cs-review：做文档熵减`.

## Output protocol

```text
Route: onboard.required | onboard.repair | onboard.refresh-knowledge | onboard.status
Playbook: codestable-core/playbooks/onboard.md#<section>
Read: <README/manifests/source dirs/tests/config/docs>
Evidence: <inventory path + key anchors>
Write-intent: <created/refreshed paths or none>
Project Knowledge State: code-informed | partial | skeleton-only | blocked
Unknowns: <facts requiring owner confirmation>
Next: do | review | ask-user | stop
```

## Hard stops

- Do not claim architecture facts without code/manifests/docs evidence.
- Do not delete or move user-maintained docs during onboard.
- Do not fill requirements as current product truth when only inferred from filenames; mark inferred.
- Do not begin feature/bug/refactor work as a side effect of onboard.
- Do not leave `.codestable/INDEX.md` as a generic skeleton when the repository has code to inspect.
