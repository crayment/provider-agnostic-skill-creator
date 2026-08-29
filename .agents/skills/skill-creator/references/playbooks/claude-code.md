# Playbook: Claude Code

Platform-specific mechanics for running the skill-creator harness in Claude Code.

Load this playbook when the orchestrator runs in Claude Code and needs CLI automation, description optimization, or packaging integration.

## Subagent orchestration

Claude Code provides subagents via its Task/delegation tools. Before spawning executor or grader workers:

1. Use Claude Code's team/delegation conventions (parallel Task spawn when available).
2. Put full executor contract from `references/worker-contracts.md` in each child prompt.
3. Skills are not auto-loaded in children — instruct workers to read required skill files explicitly.

## Parallel eval execution

Spawn **all** with-skill and baseline executors in the **same turn** so runs finish together.

When each Task completes, the notification may include `total_tokens` and `duration_ms`. Write these to `{run_dir}/timing.json` immediately — they are not persisted elsewhere.

## Description optimization (`run_loop`)

Trigger evals use the Claude CLI subprocess, not LLM simulation:

```bash
cd <project-with-.claude>   # run_eval discovers project root via .claude/
python -m scripts.run_loop \
  --eval-set <workspace>/trigger-eval.json \
  --skill-path <path-to-skill-under-test> \
  --model <model-id-from-session> \
  --max-iterations 5 \
  --verbose
```

`run_eval.py` creates a temporary command file under `.claude/commands/` and runs `claude -p` with stream-json to detect skill triggering. Requires `claude` on PATH and appropriate auth.

Flags (see `python -m scripts.run_loop --help`):

- `--max-iterations` — optimization rounds
- `--holdout` — train/test split fraction (default 0.4)
- `--runs-per-query` — repetitions per query for trigger rate stability

While running, tail stderr/log output for progress updates.

## Individual trigger eval

```bash
python -m scripts.run_eval \
  --eval-set <json> \
  --skill-path <path> \
  --model <model-id> \
  --output <results.json>
```

## Packaging and present_files

Package:

```bash
python -m scripts.package_skill <path/to/skill-folder> [output-dir]
```

If the `present_files` tool is available, package then present the `.skill` file to the user. Skip if the tool is unavailable.

## Validation

```bash
python -m scripts.quick_validate <skill-directory>
```

Requires PyYAML (`pip install pyyaml`) for frontmatter validation.

## Headless / Cowork

- Use `eval-viewer/generate_review.py --static <path.html>` when no browser/display.
- Feedback downloads as `feedback.json`; copy into the workspace iteration directory.
- Description optimization works headless (CLI-based).
- Subagents available — full parallel eval loop applies.

## Claude.ai (no subagents)

When subagents are unavailable:

- Run eval prompts sequentially yourself (weaker independence; human review compensates).
- Skip baseline runs and quantitative benchmarking.
- Skip blind comparison and description optimization (needs `claude -p`).
- Packaging and static HTML viewer still work.

## Notification timing

Process Task completion notifications as they arrive — do not batch timing capture. Each notification is the only source for that run's token/duration data.
