# Upstream agent review — provider-agnostic-skill-creator

**Review date:** 2026-08-30  
**Drift window (from scheduled report):** `0620a687ddd5` → `ed404106fcd8`  
**Canonical upstream:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator/skills/skill-creator)

## Executive summary

**Recommendation: no action — defer merges; pin already at latest.**

Upstream `main` moved one commit since the drift report’s old pin (`0620a687ddd5` → `ed404106fcd8`), but that commit only updates `.claude-plugin/marketplace.json` (scandit-sdk plugin promotion). **Zero files under `plugins/skill-creator/skills/skill-creator/` changed** in that range (verified by per-file SHA-256 comparison at both commits).

| Category | Status |
|----------|--------|
| Vendor-identical files | All 13 match upstream latest |
| Fork patches | Upstream unchanged in drift window; local intentional deltas preserved |
| SKILL.md eval-loop process | No new upstream steps in this window; fork retains full loop per `COMPARISON.md` |
| Pin bump | **Already at** `ed404106fcd80ba98ecb7c851e531dcb626d13b7` in `UPSTREAM_PIN.json` |

No verbatim copies or manual merges are required for this drift cycle.

---

## Upstream commit analysis

| Commit | Message | Skill-creator impact |
|--------|---------|----------------------|
| `ed404106fcd8` | Add scandit-sdk plugin (community → official promotion) (#5634) | None — only `marketplace.json` |
| `0620a687ddd5` | (previous pin in drift report) | Baseline for comparison |

The skill-creator subtree has not changed since at least `2a40fd2` (skill-creator sync from anthropics/skills, #1523).

---

## Vendor-identical files

All files listed in `UPSTREAM_PIN.json` → `vendor_identical` are byte-identical to upstream at `ed404106fcd8`:

- `LICENSE.txt`
- `agents/analyzer.md`, `agents/comparator.md`, `agents/grader.md`
- `assets/eval_review.html`
- `eval-viewer/viewer.html`
- `scripts/generate_report.py`, `scripts/improve_description.py`, `scripts/package_skill.py`, `scripts/quick_validate.py`, `scripts/run_eval.py`, `scripts/run_loop.py`, `scripts/utils.py`

**Action:** none.

---

## Fork patches (file-by-file)

Upstream content for these paths is **unchanged** between `0620a687ddd5` and `ed404106fcd8`. Local diffs are intentional fork adaptations documented in `COMPARISON.md` and `OVERRIDES.md`. Do **not** blind-overwrite.

### `SKILL.md`

| | |
|---|---|
| **Upstream delta in window** | None |
| **Local fork intent** | Provider-neutral orchestration; worker contracts + thin playbooks; no Task API params |
| **Eval-loop fidelity** | Fork preserves continuous loop, same-turn parallel executors, grader-first grading, aggregate → analyst → viewer, scale-up, description optimization safeguards, unconditional packaging (see `COMPARISON.md` checklist) |
| **Upstream-only sections not ported** | Claude.ai-specific, Cowork-specific, and verbose subagent spawn templates — deliberately replaced by `references/worker-contracts.md` and `references/playbooks/*` |
| **Action** | **Keep local.** Re-diff on next upstream skill-creator commit only. |

### `references/schemas.md`

| | |
|---|---|
| **Upstream delta in window** | None |
| **Local fork intent** | Documents `tokens_source` and `output_chars_proxy` for platforms without token notifications |
| **Action** | **Keep local.** |

### `scripts/__init__.py`

| | |
|---|---|
| **Upstream delta in window** | None (upstream has no file; fork adds package marker) |
| **Local fork intent** | Enables `python -m scripts.*` invocations |
| **Action** | **Keep local.** |

### `scripts/aggregate_benchmark.py`

| | |
|---|---|
| **Upstream delta in window** | None |
| **Local fork intent** | Direct single-run + repeated-run layouts; config ordering (`with_skill` before baseline); inferred run counts; token proxy labeling |
| **Action** | **Keep local.** Fixes upstream layout mismatch noted in `COMPARISON.md`. |

### `eval-viewer/generate_review.py`

| | |
|---|---|
| **Upstream delta in window** | None |
| **Local fork intent** | Ancestor walk for `eval_metadata.json` in nested `run-N` layouts |
| **Action** | **Keep local.** |

---

## Fork-only files (unchanged)

These paths are not in upstream; no drift review needed:

- `references/worker-contracts.md`
- `references/playbooks/claude-code.md`
- `references/playbooks/cursor.md`

---

## Proposed `UPSTREAM_PIN.json` commit

After this review (no merges required):

```json
"commit": "ed404106fcd80ba98ecb7c851e531dcb626d13b7"
```

This matches upstream `main` tip as of review date. **No file edit required** — the repository pin is already current.

---

## What changed in this PR

- Added this review document (`upstream-agent-review.md`).
- Regenerated `upstream-drift-report.md` (pin now matches tip → “no action required”).
- **No skill file changes** — upstream skill-creator subtree did not move in the drift window.

## Deferred

- Monitor future upstream commits that touch `plugins/skill-creator/skills/skill-creator/`; the next real skill-creator change will require a full fork-patch diff per `OVERRIDES.md`.
- If upstream adds new eval-loop steps in `SKILL.md`, merge them into the provider-neutral body and worker contracts rather than copying Claude Code spawn blocks verbatim.
