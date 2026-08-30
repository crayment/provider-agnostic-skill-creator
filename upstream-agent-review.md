# Upstream agent review — provider-agnostic-skill-creator

**Review date:** 2026-08-30  
**Reviewer:** Cloud drift agent (`cursor/upstream-skill-creator-drift-review-29bb`)  
**Drift report:** [upstream-drift-report.md](./upstream-drift-report.md)

## Executive summary

**Recommendation: pin bump only — no file merges.**

Upstream `main` advanced (`0620a687ddd5` → `ed404106fcd8`), but the
`plugins/skill-creator/skills/skill-creator` subtree is **byte-identical** at
both commits. A full tree diff and per-file hash comparison confirm zero upstream
changes to any vendor or fork-patched path in this pin window.

| Category | Status | Action |
|----------|--------|--------|
| Vendor-identical files (13) | Already match upstream latest | None |
| Fork patches (5) | Unchanged upstream since pin; local deltas intentional | Keep fork; no merge |
| SKILL.md eval-loop process | No upstream additions in this window | None |
| `UPSTREAM_PIN.json` | Stale commit field | **Bump to `ed404106fcd8`** |

The scheduled drift job correctly detected branch movement and flagged fork
patches for review. Those files did not actually change upstream — the script
marks all fork patches whenever `main` moves. This review closes that cycle with
a metadata-only update.

## Verification method

1. Read `UPSTREAM_PIN.json`, `COMPARISON.md`, and the generated drift report.
2. Cloned [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) at `main` (`ed404106fcd8`).
3. Compared upstream `0620a687` vs `ed404106` for the skill path — **empty diff** (18 files, identical trees).
4. Hashed all 13 `vendor_identical` paths locally vs upstream latest — all match.
5. Diffed each `fork_patch` locally vs upstream latest — only intentional fork deltas (documented below).
6. Ran `scripts/check_process_fidelity.py` — passed.

## File-by-file recommendations

### Vendor-identical files — no action

All paths already match upstream `ed404106fcd8`:

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

| File | Upstream delta (0620→ed404) | Local vs upstream latest | Recommendation |
|------|----------------------------|---------------------------|----------------|
| `SKILL.md` | None | Provider-neutral orchestration; worker contracts; no Claude.ai/Cowork sections; complete eval loop with Step 0 orchestration preamble | **Keep fork.** No new upstream eval-loop steps to absorb. |
| `references/schemas.md` | None | Adds `tokens_source` field docs for proxy token reporting | **Keep fork.** Documents aggregation behavior upstream lacks. |
| `scripts/__init__.py` | None | Comment-only package marker for `python -m scripts.*` | **Keep fork.** |
| `scripts/aggregate_benchmark.py` | None | Direct + nested `run-N` layouts; config ordering; inferred run counts; token proxy notes | **Keep fork.** Fixes upstream layout mismatch documented in `COMPARISON.md`. |
| `eval-viewer/generate_review.py` | None | `find_ancestor_file()` for metadata above nested runs | **Keep fork.** Pairs with aggregate_benchmark layout support. |

### Fork-only files — no action

| File | Recommendation |
|------|----------------|
| `references/worker-contracts.md` | ✓ Keep (fork-only) |
| `references/playbooks/claude-code.md` | ✓ Keep (fork-only) |
| `references/playbooks/cursor.md` | ✓ Keep (fork-only) |

## SKILL.md process check

Compared section structure and required eval-loop concepts against upstream
`SKILL.md` at `ed404106fcd8`:

- **Continuous eval sequence** — preserved (Steps 0–5; “do not stop mid-loop”).
- **Parallel with-skill + baseline** — preserved with platform qualification.
- **Pipeline:** evals → metadata → outputs → timing → grader → aggregate → analyst → viewer → feedback → improve → scale-up → package.
- **Grader-first grading** — preserved; scripts support, not replace, grader.
- **Description optimization track** — trigger queries, HTML review, 60/40 holdout, three runs, held-out selection — all present.
- **Packaging** — unconditional final step restored.

Upstream did not add or reorder eval-loop steps in this pin window. Provider-neutral constraints (no Task API params, thin playbooks) remain satisfied.

## Proposed `UPSTREAM_PIN.json` update

```json
"commit": "ed404106fcd80ba98ecb7c851e531dcb626d13b7"
```

Applied in this PR. No changes to `vendor_identical`, `fork_patches`, or
`fork_only` lists.

## Deferred items

None for this drift cycle. Re-run review when upstream next modifies files under
`plugins/skill-creator/skills/skill-creator/`.

**Optional CI improvement (not in scope):** teach `check_upstream_drift.py` to
diff fork patches against the pinned commit instead of flagging all patches
whenever `main` moves — would reduce false-positive agent runs like this one.
