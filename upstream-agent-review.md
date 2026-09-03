# Upstream agent review

Review date: 2026-09-03

- **Canonical upstream:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator/skills/skill-creator) `plugins/skill-creator/skills/skill-creator`
- **Pinned commit:** `ed404106fcd80ba98ecb7c851e531dcb626d13b7` (2026-08-28)
- **Latest `main` reviewed:** `0120fb83da5d7cdaa52dd11979690f2dc5f76052` (2026-09-02)
- **Skill-creator tree SHA (both commits):** `98a510d1cfef9f82c3b1eec200229ca68725e613`

Compare: https://github.com/anthropics/claude-plugins-official/compare/ed404106fcd80ba98ecb7c851e531dcb626d13b7...0120fb83da5d7cdaa52dd11979690f2dc5f76052

## Executive summary

**No action on skill files.** Upstream `main` moved (`ed404106fcd8` → `0120fb83da5d`, 117 commits) but **none of those commits touch skill-creator**. The skill directory tree is byte-identical at the pin and at latest `main`. All `vendor_identical` files already match. Fork-patched files have no upstream edits to merge. Anthropic did not add or change eval-loop steps.

The scheduled drift job flagged this because it treated any marketplace HEAD movement as skill-creator drift. GitHub compare for this window lists 31 files: `.claude-plugin/marketplace.json`, plus `claude-security` and `frontend-design` plugin updates. Nothing under `plugins/skill-creator/skills/skill-creator`.

**This PR**

- Records the review (this file).
- Bumps `UPSTREAM_PIN.json` to the reviewed SHA and records the skill-creator tree SHA.
- Gates future drift alerts on that tree SHA so unrelated marketplace commits do not launch another review.

**Not merged:** no copies of vendor files, no edits to fork patches, no `SKILL.md` process changes.

Sibling open PRs covering the same pin window or an earlier marketplace-only tip: #5 (same `0120fb83da5d` review plus this detector change) and #4 (earlier `4b909c3492b3` pin-only bump). This run independently re-verified the current tip.

## Drift report recap

The scheduled job reported:

- Vendor-identical files: all ✓ (local already equals upstream latest).
- Fork patches: all 🔍 because `main` moved — the checker cannot see pin-era blobs from a shallow clone of latest, so it asked an agent to diff.

Agent verification (blob IDs at both SHAs, plus GitHub compare):

| Path | Blob at pin | Blob at latest | Verdict |
|------|-------------|----------------|---------|
| Entire skill tree | `98a510d1cfef` | `98a510d1cfef` | Unchanged |
| Last commit touching the skill path | `ed404106fcd8` | `ed404106fcd8` | Still the pin |

## File-by-file recommendations

### Vendor-identical (must match upstream latest)

No copies. Each file is already byte-identical to upstream latest.

| Path | Recommendation |
|------|----------------|
| `LICENSE.txt` | Keep — already matches |
| `agents/analyzer.md` | Keep — already matches |
| `agents/comparator.md` | Keep — already matches |
| `agents/grader.md` | Keep — already matches |
| `assets/eval_review.html` | Keep — already matches |
| `eval-viewer/viewer.html` | Keep — already matches |
| `scripts/generate_report.py` | Keep — already matches |
| `scripts/improve_description.py` | Keep — already matches |
| `scripts/package_skill.py` | Keep — already matches |
| `scripts/quick_validate.py` | Keep — already matches |
| `scripts/run_eval.py` | Keep — already matches |
| `scripts/run_loop.py` | Keep — already matches |
| `scripts/utils.py` | Keep — already matches |

No files were added or removed in the upstream skill directory.

### Fork patches (do not overwrite)

Upstream content of each patched file is unchanged since the pin. Keep the fork versions.

| Path | Fork intent | Upstream since pin | Recommendation |
|------|-------------|--------------------|----------------|
| `SKILL.md` | Provider-neutral orchestration; playbooks and worker contracts | Unchanged (blob `65b3a402dbd0`) | Keep fork. No new eval-loop steps to port. |
| `references/schemas.md` | Documented benchmark layout variants for repeated-run workspaces | Unchanged | Keep fork |
| `scripts/__init__.py` | Comment-only package marker for `python -m scripts.*` (upstream is an empty blob) | Unchanged (empty blob `e69de29bb2d1`) | Keep fork comment |
| `scripts/aggregate_benchmark.py` | Direct and repeated-run benchmark layouts | Unchanged | Keep fork |
| `eval-viewer/generate_review.py` | Static export and ancestor metadata lookup for nested `run-N` layouts | Unchanged | Keep fork |

### Fork-only (not in upstream)

`references/worker-contracts.md` and `references/playbooks/{claude-code,cursor}.md` have no upstream counterpart. No merge possible.

## SKILL.md process check

Upstream `SKILL.md` at latest `main` is the same blob as at the pin. Anthropic did not add, remove, or reorder eval-loop steps.

The upstream sequence remains:

1. Spawn with-skill and baseline in the same turn; write `eval_metadata.json`
2. Draft assertions while runs execute
3. Capture `timing.json` on completion
4. Grade (`text` / `passed` / `evidence`) → `aggregate_benchmark` → analyst notes → `generate_review.py` viewer
5. Read `feedback.json`; iterate; expand the eval set; optionally `run_loop` description optimization; `package_skill`

This fork still covers that sequence in provider-neutral form (see `COMPARISON.md`). Nothing new was dropped because nothing new landed. Claude.ai / Cowork body sections remain intentionally out of `SKILL.md` (playbooks).

## Proposed `UPSTREAM_PIN.json` bump

Applied in this PR:

```json
"commit": "0120fb83da5d7cdaa52dd11979690f2dc5f76052",
"skill_tree": "98a510d1cfef9f82c3b1eec200229ca68725e613"
```

`skill_tree` is `git rev-parse <commit>:plugins/skill-creator/skills/skill-creator`. Future drift jobs compare this tree, not marketplace HEAD.

## Changed vs deferred

| Item | Action |
|------|--------|
| Vendor-identical skill files | **Deferred / none** — already match; nothing to copy |
| Fork-patched skill files | **Deferred / none** — no upstream edits |
| Eval-loop steps in `SKILL.md` | **Deferred / none** — upstream process unchanged |
| `UPSTREAM_PIN.json` commit + `skill_tree` | **Changed** — record the reviewed SHA |
| `scripts/check_upstream_drift.py` | **Changed** — alert only when the skill tree or vendor files actually diverge |
| This review document | **Changed** |

## Follow-up (not in this PR)

None required for skill-creator content. If Anthropic later edits the skill tree, the next scheduled job should open a content merge review.
