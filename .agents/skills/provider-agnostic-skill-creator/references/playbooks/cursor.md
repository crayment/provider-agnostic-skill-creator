# Playbook: Cursor

Thin notes for the non-substitutable Cursor gaps in the skill-creator loop.
Shared roles, prompts, and paths live in
[worker-contracts.md](../worker-contracts.md).

## Before parallel evals

Load the environment's current orchestration skills before spawning:

- `cursor-subagents` for spawn, resume, ownership, and autonomy conventions
- `agent-teams-cursor-v2` for roster, parallel work, relay, and handoff

Those skills define the API mechanics. This playbook does not duplicate Task
parameters. Use the executor and grader contracts, and launch every with-skill
and baseline executor in the same orchestration turn.

## Timing and token gaps

Worker completion notifications may omit `total_tokens`. Process each
completion immediately:

- write reported duration or measured wall time to `timing.json`
- set `timing_source` to `worker_notification` or `wall_clock`
- leave `total_tokens` null when unavailable
- retain `metrics.json` `output_chars` as an explicitly labeled size proxy

Do not skip timing merely because tokens are unavailable.

## Description optimization gap

The bundled `run_eval.py` and `run_loop.py` use real `claude -p` trigger
events. Cursor does not currently provide an equivalent verified injection and
trigger signal in this repository.

Use the Claude Code playbook for the automated optimization loop, or run a
manual, explicitly labeled Cursor experiment. Do not replace invocation
evidence with an orchestrator's yes/no guess.

## Viewer

```bash
python eval-viewer/generate_review.py <workspace>/iteration-N \
  --skill-name "<name>" \
  --benchmark <workspace>/iteration-N/benchmark.json
```

Use `--static <output.html>` when the environment has no display. The static
viewer downloads `feedback.json`; copy it into the iteration directory.

## Packaging

```bash
python -m scripts.package_skill /path/to/skill-folder
```

Return the generated `.skill` path when no file-presentation tool is
available.
