# Upstream agent review — provider-agnostic-skill-creator

**Review date:** 2026-09-01  
**Reviewer:** Cloud drift agent (`cursor/upstream-skill-creator-drift-review-9c5b`)  
**Drift report:** scheduled job output (summarized below; CI artifact, not committed)

## Executive summary

**Recommendation: pin bump only — no file merges.**

Upstream `main` advanced (`ed404106fcd8` → `4b909c3492b3`), but the
`plugins/skill-creator/skills/skill-creator` subtree is **byte-identical** at
both commits. A full tree diff and per-file hash comparison confirm zero upstream
changes to any vendor or fork-patched path in this pin window.

The sole intervening commit is [`4b909c3`](https://github.com/anthropics/claude-plugins-official/commit/4b909c3492b350cdc42160ffe4b135e6f5c1db12)
(`bump(activecampaign): 964b2f9f → 0ff85872`, #5722), which edits
`.claude-plugin/marketplace.json` only.

| Category | Status | Action |
|----------|--------|--------|
| Vendor-identical files (13) | Already match upstream latest | None |
| Fork patches (5) | Unchanged upstream since pin; local deltas intentional | Keep fork; no merge |
| SKILL.md eval-loop process | No upstream additions in this window | None |
| `UPSTREAM_PIN.json` | Stale commit field | **Bump to `4b909c3492b3`** |

The scheduled drift job correctly detected branch movement and flagged fork
patches for review. Those files did not actually change upstream — the script
marks all fork patches whenever `main` moves. This review closes that cycle with
a metadata-only update so the next cron run is green until skill-creator itself
changes.

## Drift report summary

From the scheduled job (`ed404106fcd8` pin vs `4b909c3492b3` tip):

- **Canonical upstream:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator/skills/skill-creator)
- **Vendor-identical files (13):** all already matched upstream latest ✓
- **Fork patches (5):** flagged 🔍 because the tip moved; agent diff shows **no upstream file changes**
- **Action recommended by the job:** review and bump `UPSTREAM_PIN.json` after merge — applied here as a pin-only bump (nothing to merge)

## Verification method

1. Read `UPSTREAM_PIN.json`, `COMPARISON.md`, `OVERRIDES.md`, and the attached drift report.
2. Cloned [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) and fetched `main` (`4b909c3492b350cdc42160ffe4b135e6f5c1db12`).
3. Compared upstream `ed404106fcd8` vs `4b909c3492b3` for the skill path — **empty diff** (18 files, identical trees).
4. Hashed all 13 `vendor_identical` paths locally vs upstream latest — all match.
5. Confirmed each `fork_patch` is unchanged between the two upstream commits; local vs latest still shows only intentional fork deltas.
6. Ran `scripts/check_process_fidelity.py` — passed.

## File-by-file recommendations

### Vendor-identical files — no action

All paths already match upstream `4b909c3492b3` (same bytes as `ed404106fcd8`):

| File | Recommendation |
|------|----------------|
| `LICENSE.txt` | ✓ Keep (matches upstream) |
| `agents/analyzer.md` | ✓ Keep |
| `agents/comparator.md` | ✓ Keep |
| `agents/grader.md` | ✓ Keep |
| `assets/eval_review.html` | ✓ Keep |
| `eval-viewer/viewer.html` | ✓ Keep |
| `scripts/generate_report.py` | ✓ Keep |
| `scripts/improve_description.py` | ✓ Keep |
| `scripts/package_skill.py` | ✓ Keep |
| `scripts/quick_validate.py` | ✓ Keep |
| `scripts/run_eval.py` | ✓ Keep |
| `scripts/run_loop.py` | ✓ Keep |
| `scripts/utils.py` | ✓ Keep |

### Fork patches — keep local; defer upstream verbatim merge

Upstream content for these files did **not** change between the old pin and
latest `main`. Local versions remain ahead of upstream with documented fork
intent (see `UPSTREAM_PIN.json` → `fork_patches` and `COMPARISON.md`).

| File | Upstream delta (ed404→4b909) | Local vs upstream latest | Recommendation |
|------|------------------------------|---------------------------|----------------|
| `SKILL.md` | None | Provider-neutral orchestration; worker contracts; no Task API params; complete eval loop with Step 0 orchestration preamble | **Keep fork.** No new upstream eval-loop steps to absorb. |
| `references/schemas.md` | None | Documents benchmark layout variants and `tokens_source` for repeated-run workspaces | **Keep fork.** Documents aggregation behavior upstream lacks. |
| `scripts/__init__.py` | None | Comment-only package marker for `python -m scripts.*` | **Keep fork.** |
| `scripts/aggregate_benchmark.py` | None | Direct + nested `run-N` layouts; config ordering; inferred run counts; token proxy notes | **Keep fork.** Fixes upstream layout mismatch documented in `COMPARISON.md`. |
| `eval-viewer/generate_review.py` | None | Static export and ancestor metadata discovery for nested runs | **Keep fork.** Pairs with aggregate_benchmark layout support. |

### Fork-only files — no action

| File | Recommendation |
|------|----------------|
| `references/worker-contracts.md` | ✓ Keep (fork-only) |
| `references/playbooks/claude-code.md` | ✓ Keep (fork-only) |
| `references/playbooks/cursor.md` | ✓ Keep (fork-only) |

## SKILL.md process check

Compared required eval-loop concepts against upstream `SKILL.md` at
`4b909c3492b3` (identical to the previous pin):

- **Continuous eval sequence** — preserved (Steps 0–5; “do not stop mid-loop”).
- **Parallel with-skill + baseline** — preserved with platform qualification.
- **Pipeline:** evals → metadata → outputs → timing → grader → aggregate → analyst → viewer → feedback → improve → scale-up → package.
- **Grader-first grading** — preserved; scripts support, not replace, grader.
- **Description optimization track** — trigger queries, HTML review, 60/40 holdout, three runs, held-out selection — all present.
- **Packaging** — unconditional final step.

Upstream did not add or reorder eval-loop steps in this pin window. Provider-neutral constraints (no Task API params, thin playbooks) remain satisfied.

## Proposed `UPSTREAM_PIN.json` update

```json
"commit": "4b909c3492b350cdc42160ffe4b135e6f5c1db12"
```

Applied in this PR. No changes to `vendor_identical`, `fork_patches`, or
`fork_only` lists.

## Deferred items

- **All skill-file merges** — nothing to merge; skill-creator subtree is unchanged.
- **Fork patches** — keep local deltas; re-diff when upstream next modifies those paths.
- **Closed upstream PR [anthropics/claude-plugins-official#5709](https://github.com/anthropics/claude-plugins-official/pull/5709)** (`fix(skill-creator): measure skill triggers reliably on Windows`) is **not on `main`**. Watch only; do not merge from a closed unmerged PR.

**Optional CI improvement (not in this PR):** teach `check_upstream_drift.py` to
diff fork patches against the pinned commit (or restrict the tip comparison to
the skill subtree) instead of flagging all patches whenever `main` moves — would
reduce false-positive agent runs like this one (marketplace-only bumps).
