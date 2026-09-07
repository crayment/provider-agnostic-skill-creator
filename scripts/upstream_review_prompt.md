You are reviewing upstream drift for **provider-agnostic-skill-creator**.

## Context

This repo is an **unofficial, provider-neutral port** of Anthropic's open-source
[skill-creator](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator/skills/skill-creator).

Pinned upstream metadata lives in `UPSTREAM_PIN.json`. A scheduled drift job
produced `upstream-drift-report.md` (attached below).

{{PR_MODE_NOTE}}

## Your task

1. Read `upstream-drift-report.md`, `UPSTREAM_PIN.json`, and `COMPARISON.md`.
2. If upstream moved, fetch the upstream skill tree at latest main and compare:
   - **vendor_identical** files — copy upstream changes verbatim when safe.
   - **fork_patches** files — merge upstream edits thoughtfully; never blind overwrite.
   - **SKILL.md process** — did Anthropic add/change eval-loop steps we dropped?
3. Write `upstream-agent-review.md` in the repo root with:
   - Executive summary (merge now / defer / no action)
   - File-by-file recommendations
   - Proposed `UPSTREAM_PIN.json` commit bump when merges are done
4. **Land your changes on a pull request** (required when drift needs attention):
   - **Stale vendor_identical only:** verbatim upstream copies, pin bump,
     short review doc. Title like `chore: sync vendor files from upstream skill-creator`.
   - **fork_patches also changed:** safe vendor merges plus documented
     manual merges for patched files; do not silently overwrite fork intent.
   - **Upstream moved but nothing to merge yet:** just `upstream-agent-review.md`
     explaining defer/no-action, plus the pin bump.
   - If you are updating an **existing** drift-review PR (see PR mode note above),
     replace/update `upstream-agent-review.md` rather than leaving stale prior-day
     findings alongside new ones — this PR should always reflect the latest review.
5. PR body must link the drift report summary and list what you changed vs deferred.

## Constraints

- Preserve provider-neutral orchestration (no Task API params in SKILL.md).
- Keep playbooks thin.
- Do not reference private skill names.
- Do not merge your own PR — leave it open for human review.

## Drift report

```markdown
{{DRIFT_REPORT}}
```
