# Upstream skill-creator drift review

Review date: 2026-09-05  
Reviewer: Cloud Agent (scheduled drift job)  
Canonical upstream: [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator/skills/skill-creator)  
Skill path: `plugins/skill-creator/skills/skill-creator`

| | Commit |
|---|---|
| Pinned | `ed404106fcd80ba98ecb7c851e531dcb626d13b7` (`ed40410`) |
| Latest `main` | `85cce0381e7860082641b59d961a2b8c368b8b79` (`85cce03`) |
| Latest tip subject | Merge pull request #5822 from anthropics/jordan/raise-bump-cap |

Method: sparse-clone of the upstream repo at the pin and at `origin/main`; SHA-256 of every skill-tree file; `git log pin..tip -- plugins/skill-creator`.

---

## Executive summary

**No action on skill files. Pin bump only.**

Upstream `main` moved (`ed40410` → `85cce03`, 249 monorepo commits), but **zero of those commits touch `plugins/skill-creator`**. The skill-creator file set is identical at the pin and at latest `main` (same 18 files; no adds, no deletes). Every `vendor_identical` file already matches latest. Every `fork_patches` file is unchanged upstream, so the fork deltas stay as documented in `COMPARISON.md` / `OVERRIDES.md`.

Anthropic did **not** add or change eval-loop steps in `SKILL.md`. There is nothing to merge, defer, or overwrite.

The scheduled drift job flags all `fork_patches` whenever the **repo** tip moves (shallow clone cannot diff against the pin). That is why this review fired. Bumping `UPSTREAM_PIN.json` to `85cce0381e78…` records that we audited this tip and stops the same no-op review from launching every day.

---

## Drift report (from the scheduled job)

The job attached this summary (vendor checks are correct; fork-patch “🔍” lines are tip-movement, not file diffs):

- Canonical: anthropics/claude-plugins-official `plugins/skill-creator/skills/skill-creator`
- Pinned: `ed404106fcd8` → latest `main`: `85cce0381e78`
- Vendor-identical: all 13 files ✓ match latest
- Fork patches: all five listed as “upstream tip moved; agent should diff”
- Recommendation: review and bump the pin after merge

---

## File-by-file recommendations

### Vendor-identical (must match latest) — no copy needed

| Path | Pin vs latest | Local vs latest | Action |
|---|---|---|---|
| `LICENSE.txt` | identical | identical | none |
| `agents/analyzer.md` | identical | identical | none |
| `agents/comparator.md` | identical | identical | none |
| `agents/grader.md` | identical | identical | none |
| `assets/eval_review.html` | identical | identical | none |
| `eval-viewer/viewer.html` | identical | identical | none |
| `scripts/generate_report.py` | identical | identical | none |
| `scripts/improve_description.py` | identical | identical | none |
| `scripts/package_skill.py` | identical | identical | none |
| `scripts/quick_validate.py` | identical | identical | none |
| `scripts/run_eval.py` | identical | identical | none |
| `scripts/run_loop.py` | identical | identical | none |
| `scripts/utils.py` | identical | identical | none |

### Fork patches — upstream file did not change

These still differ from upstream **by our documented fork intent**. Upstream itself did not edit them between the pin and `85cce03`. Do not overwrite.

| Path | Fork reason | Pin vs latest | Recommendation |
|---|---|---|---|
| `SKILL.md` | Provider-neutral orchestration; playbooks and worker contracts | identical | **Keep fork.** No new upstream process steps. |
| `references/schemas.md` | Documented benchmark layout variants for repeated-run workspaces | identical | **Keep fork.** |
| `scripts/__init__.py` | Package marker for `python -m scripts.*` (upstream is empty) | identical | **Keep fork.** |
| `scripts/aggregate_benchmark.py` | Direct + repeated-run benchmark layouts | identical | **Keep fork.** |
| `eval-viewer/generate_review.py` | Static export + ancestor metadata for nested `run-N` layouts | identical | **Keep fork.** |

### Fork-only (not in upstream)

`references/worker-contracts.md`, `references/playbooks/claude-code.md`, `references/playbooks/cursor.md` — no upstream counterpart. No action.

### SKILL.md process check

Compared upstream `SKILL.md` at pin vs `85cce03`: **byte-identical**. Anthropic did not add, remove, or reorder eval-loop steps (draft → `evals.json` / `eval_metadata.json` → parallel with-skill + baseline → timing → grader → `aggregate_benchmark` → analyst → HTML viewer → feedback → improve → optional description/`run_loop` and blind compare → package).

Our fork still carries the 2026-08-29 fidelity restorations from `COMPARISON.md` (continuous sequence, grader-first, holdout/repetition for description opt, scale-up before package) and still keeps spawn APIs out of `SKILL.md`. Nothing from this tip needs to be pulled in.

---

## What this PR changes vs defers

**Changed**

- `UPSTREAM_PIN.json` `canonical.commit` → `85cce0381e7860082641b59d961a2b8c368b8b79` (this review’s close-out).
- This review document.

**Deferred / not done (correctly)**

- No verbatim vendor copies (already current).
- No merge into any `fork_patches` file (upstream did not edit them).
- No playbook or worker-contract edits.
- No Task API / provider-specific parameters in `SKILL.md`.

**Follow-up (not in this PR)**

- `scripts/check_upstream_drift.py` treats any monorepo tip move as “diff every fork patch.” A later change could fetch the pin-era blobs (or compare file hashes at pin vs tip) so a skill-tree-unchanged move does not launch an agent. Until then, a pin bump after a no-op review is the right close-out.

---

## Proposed `UPSTREAM_PIN.json` bump

Applied in this PR:

```json
"commit": "85cce0381e7860082641b59d961a2b8c368b8b79"
```

All other pin fields (`repo`, `branch`, `skill_path`, `url`, `vendor_identical`, `fork_patches`, `fork_only`) stay the same.
