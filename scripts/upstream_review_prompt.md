You are reviewing upstream drift for **provider-agnostic-skill-creator**.

## Context

This repo is an **unofficial, provider-neutral port** of Anthropic's open-source
[skill-creator](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator/skills/skill-creator).

Pinned upstream metadata lives in `UPSTREAM_PIN.json`. A deterministic CI job
produced `upstream-drift-report.md` (attached below).

## Your task

1. Read `upstream-drift-report.md` and `COMPARISON.md` (Anthropic intent checklist).
2. If upstream moved, fetch the upstream skill tree at latest main and compare:
   - **vendor_identical** files — should we merge upstream changes verbatim?
   - **fork_patches** files — what upstream edits need thoughtful merges?
   - **SKILL.md process** — did Anthropic add/change eval-loop steps we dropped?
3. Produce a markdown report in the repo root: `upstream-agent-review.md` with:
   - Executive summary (merge now / defer / no action)
   - File-by-file recommendations
   - Proposed `UPSTREAM_PIN.json` commit bump if merges are done
4. **Do not open a PR or push** unless the drift report shows stale vendor_identical
   files that are safe verbatim merges — then one PR with clear commits is OK.

## Constraints

- Preserve provider-neutral orchestration (no Task API params in SKILL.md).
- Keep playbooks thin.
- Do not reference private skill names.

## Drift report

```markdown
{{DRIFT_REPORT}}
```
