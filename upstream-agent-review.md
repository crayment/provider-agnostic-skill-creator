# Upstream agent review

Review date: 2026-09-05

- **Canonical upstream:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator/skills/skill-creator) `plugins/skill-creator/skills/skill-creator`
- **Pinned commit:** `0120fb83da5d7cdaa52dd11979690f2dc5f76052` (2026-09-02, recorded by #6)
- **Latest `main` reviewed:** `85cce0381e7860082641b59d961a2b8c368b8b79` (2026-09-05)
- **Skill-creator tree SHA (both commits):** `98a510d1cfef9f82c3b1eec200229ca68725e613` — unchanged

Compare: https://github.com/anthropics/claude-plugins-official/compare/0120fb83da5d7cdaa52dd11979690f2dc5f76052...85cce0381e7860082641b59d961a2b8c368b8b79

## Executive summary

**No action on skill files. Pin bump only.** Upstream `main` moved again since #6 merged, but `plugins/skill-creator/skills/skill-creator` is still byte-identical — confirmed by `git rev-parse HEAD:plugins/skill-creator/skills/skill-creator` at latest `main`, which still returns `98a510d1cfef9f82c3b1eec200229ca68725e613`, the same tree SHA #6 pinned.

This PR closes out the backlog of drift-review PRs (#4, #5, #7, #8) that accumulated because the pre-#6 detector treated any marketplace `main` movement as skill-creator drift and because the trigger workflow never checked for an already-open review PR before spawning another one.

**This PR**

- Bumps `UPSTREAM_PIN.json` commit to the latest verified tip (`85cce0381e78…`); `skill_tree` is unchanged.
- Updates this review doc.
- Fixes `scripts/trigger_upstream_agent.sh` to check for an existing open drift-review PR (branch prefix `cursor/upstream-skill-creator-drift-review-`) before triggering a new Cloud Agent. If one is open, the agent is pointed at it via `prUrl` + `workOnCurrentBranch: true` and pushes to that same branch instead of opening a sibling PR.
- Adds `pull-requests: read` to the `upstream-sync.yml` workflow permissions and passes `GH_TOKEN` so the trigger script can query `gh pr list`.
- Updates `scripts/upstream_review_prompt.md` so the agent prompt states whether it's opening a new PR or updating an existing one, and to refresh (not append to) `upstream-agent-review.md` when reusing a PR.

**Not merged:** no copies of vendor files, no edits to fork patches, no `SKILL.md` process changes — none are needed.

## Why five PRs piled up (background, now resolved)

1. **Detection was too coarse** (fixed by #6, already merged): the old script compared the whole upstream repo HEAD, so unrelated marketplace-plugin bumps (Salesforce, Carta, ActiveCampaign, etc.) looked like skill-creator drift every day.
2. **No dedupe on trigger** (fixed by this PR): even with accurate detection, if real drift were ever detected on two consecutive days before a human merged the first PR, the workflow would have opened a second, redundant PR. It now reuses the open one.

With both fixes in place, a new PR should only appear when the `plugins/skill-creator/skills/skill-creator` tree SHA actually changes upstream, and there will only ever be one open drift-review PR at a time.

## File-by-file recommendations

No copies or merges — every file is unchanged from #6's last verified state.

| Path | Status |
|---|---|
| `LICENSE.txt`, `agents/*.md`, `assets/eval_review.html`, `eval-viewer/viewer.html`, `scripts/generate_report.py`, `scripts/improve_description.py`, `scripts/package_skill.py`, `scripts/quick_validate.py`, `scripts/run_eval.py`, `scripts/run_loop.py`, `scripts/utils.py` | Vendor-identical, still match upstream latest |
| `SKILL.md`, `references/schemas.md`, `scripts/__init__.py`, `scripts/aggregate_benchmark.py`, `eval-viewer/generate_review.py` | Fork patches, upstream unchanged since pin — keep fork |
| `references/worker-contracts.md`, `references/playbooks/claude-code.md`, `references/playbooks/cursor.md` | Fork-only, no upstream counterpart |

## Proposed `UPSTREAM_PIN.json` bump

Applied in this PR:

```json
"commit": "85cce0381e7860082641b59d961a2b8c368b8b79"
```

`skill_tree`, `branch`, `repo`, `skill_path`, `vendor_identical`, `fork_patches`, and `fork_only` are unchanged.

## Follow-up (not in this PR)

None required. The next drift review PR should only appear if the skill-creator tree itself changes upstream.
