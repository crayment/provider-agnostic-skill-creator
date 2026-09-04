# Upstream skill-creator drift review

Review date: 2026-09-04
Reviewer: Cursor Cloud Agent (`cursor/upstream-skill-creator-drift-review-b58c`)
Canonical upstream: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator/skills/skill-creator)
Skill path: `plugins/skill-creator/skills/skill-creator`

| | Commit | Date | Subject |
|---|---|---|---|
| **Pinned** | `ed404106fcd80ba98ecb7c851e531dcb626d13b7` | 2026-08-28 | Add scandit-sdk plugin (#5634) |
| **Latest `main`** | `1dd995193ba20bba51ca6c681aa8d3398dbd80a2` | 2026-09-04 | Merge PR #5785 `bump(carta-crm): f54736df → cf7e25ef` |

Method: cloned latest `main`, fetched the pinned commit, and compared git blobs for every file listed in `UPSTREAM_PIN.json`. Local vendor files were also `cmp`'d against latest upstream.

## Executive summary

**No skill-tree merge. Bump the pin.**

Upstream `main` moved (`ed404106fcd8` → `1dd995193ba2`), which is why the scheduled drift job asked for a review. The only commit in that range is an unrelated marketplace bump (`carta-crm`). **Zero files under `plugins/skill-creator/` changed.** Every `vendor_identical` file already matches latest upstream. Every `fork_patches` blob is identical at pin and tip, so there is nothing to merge and nothing to defer.

This is not a process-fidelity event. Anthropic did not add, remove, or reorder eval-loop steps. The fork's provider-neutral `SKILL.md`, layout patches, and playbooks stay as they are.

**Changed in this PR**

- `UPSTREAM_PIN.json` commit → `1dd995193ba20bba51ca6c681aa8d3398dbd80a2` (review complete; skill tree unchanged)
- This review document

**Deferred / not changed**

- All vendor-identical files (already in sync)
- All fork-patched files (upstream content unchanged; keep local patches)
- Fork-only files (`references/worker-contracts.md`, playbooks)

## Drift report summary

The scheduled job produced:

- Vendor-identical: all 13 files ✓ against latest `main`
- Fork patches: flagged 🔍 only because the checker treats *any* tip movement as “agent should diff,” not because those blobs changed
- Action recommended: review and bump `UPSTREAM_PIN.json` after merge

That 🔍 signal is a shallow-clone limitation in `scripts/check_upstream_drift.py`: it clones latest `main` only, so it cannot tell whether a patched path actually drifted. Blob comparison against the pin shows they did not.

## `SKILL.md` process check

Upstream `SKILL.md` blob `65b3a402dbd09b8e83f9d637c6b553875189085c` is unchanged between pin and tip (485 lines).

No new eval-loop steps. No dropped steps to restore. The fork's provider-neutral orchestration (contracts + thin playbooks, no Task API params in `SKILL.md`) remains the correct overlay on the same upstream process.

## File-by-file recommendations

### Vendor-identical (copy verbatim if they drift)

All already match latest upstream. **No copies.**

| Path | Pin vs latest | Local vs latest | Action |
|---|---|---|---|
| `LICENSE.txt` | unchanged | identical | none |
| `agents/analyzer.md` | unchanged | identical | none |
| `agents/comparator.md` | unchanged | identical | none |
| `agents/grader.md` | unchanged | identical | none |
| `assets/eval_review.html` | unchanged | identical | none |
| `eval-viewer/viewer.html` | unchanged | identical | none |
| `scripts/generate_report.py` | unchanged | identical | none |
| `scripts/improve_description.py` | unchanged | identical | none |
| `scripts/package_skill.py` | unchanged | identical | none |
| `scripts/quick_validate.py` | unchanged | identical | none |
| `scripts/run_eval.py` | unchanged | identical | none |
| `scripts/run_loop.py` | unchanged | identical | none |
| `scripts/utils.py` | unchanged | identical | none |

### Fork patches (merge thoughtfully; do not overwrite)

Upstream blobs are **identical** at pin and latest. Local files still differ from upstream for the documented fork reasons. **Keep local. Do not overwrite.**

| Path | Upstream pin blob | Upstream tip blob | Local intent | Action |
|---|---|---|---|---|
| `SKILL.md` | `65b3a402…` | same | Provider-neutral orchestration; playbooks and worker contracts | keep fork |
| `references/schemas.md` | `b6eeaa2d…` | same | Documented benchmark layout variants for repeated-run workspaces | keep fork |
| `scripts/__init__.py` | `e69de29b…` (empty file) | same | Package marker comment for `python -m scripts.*` | keep fork |
| `scripts/aggregate_benchmark.py` | `3e66e8c1…` | same | Direct and repeated-run benchmark directory layouts | keep fork |
| `eval-viewer/generate_review.py` | `7fa59786…` | same | Static export and nested `run-N` metadata lookup | keep fork |

### Fork-only (not in upstream)

No upstream counterpart. Unchanged by this tip.

- `references/worker-contracts.md`
- `references/playbooks/claude-code.md`
- `references/playbooks/cursor.md`

### New or removed upstream skill files

None. `git diff --name-status ed404106fcd8..1dd995193ba2 -- plugins/skill-creator` is empty.

## Proposed `UPSTREAM_PIN.json` bump

Applied in this PR:

```json
"commit": "1dd995193ba20bba51ca6c681aa8d3398dbd80a2"
```

`branch`, `repo`, `skill_path`, `vendor_identical`, and `fork_patches` are unchanged.

Bumping the pin after an empty skill-tree review stops the daily job from failing and re-spawning agents for the same unrelated marketplace commit.

## Follow-up (not in this PR)

`scripts/check_upstream_drift.py` could fetch the pinned commit and only flag `fork_patches` when that path's blob actually changed. That would avoid agent reviews for unrelated `main` motion. Out of scope for this sync.
