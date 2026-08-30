# Implementation status

Current architecture and known gaps for `provider-agnostic-skill-creator`.

## Implemented

- Provider-neutral `SKILL.md` with the complete Anthropic eval loop
- Worker contracts for executors, graders, benchmark analysis, and blind comparison
- Thin Claude Code and Cursor playbooks
- Upstream grader, comparator, analyzer, description optimization, packaging,
  schemas, templates, and viewer assets
- Claude Code trigger evaluation and description optimization through the
  upstream `claude -p` scripts
- Python package marker for `python -m scripts.*`
- PyYAML dependency declaration for `quick_validate.py`
- Upstream drift tracking: pin in `UPSTREAM_PIN.json`, daily scheduled diff via
  [`.github/workflows/upstream-sync.yml`](.github/workflows/upstream-sync.yml)
  (cron sandbox — not CI on every push), Cloud Agent opens a PR on drift via
  `scripts/trigger_upstream_agent.sh`

## 2026-08-29 fidelity review fixes

See [COMPARISON.md](COMPARISON.md) for the complete audit.

- Restored the full continuous sequence in `SKILL.md`: metadata, same-turn
  paired executors, outputs, timing, grader, aggregate, analyst, viewer,
  feedback, improvement, larger-scale rerun, and packaging.
- Made grader-first evaluation explicit. Deterministic assertion scripts
  support the grader; they do not replace it.
- Restored description-optimization details: pushy descriptions, realistic
  positive and near-miss queries, human eval-set review, 60/40 holdout,
  repeated trigger runs, and held-out selection.
- Kept Cursor spawn API parameters out of both `SKILL.md` and its thin
  playbook; the playbook points to the environment's orchestration skills.
- Corrected the Claude Code `run_eval` example: the script writes JSON to
  stdout and has no `--output` flag.
- Updated `aggregate_benchmark.py` to accept the direct layout documented by
  upstream as well as repeated `run-N` layouts, preserve with-skill/baseline
  ordering, carry eval names, infer run counts, and label token proxies.
- Updated the viewer to find eval metadata for nested repeated-run layouts.

## Deliberately not merged from the refactor fork

- `scripts/harness.py` and experimental Cursor headless trigger parsing:
  no stable Cursor skill-injection/trigger signal has been demonstrated.
- Orchestrator-generated trigger jobs: handing the tested skill path to a
  worker can itself induce a read, so it is not equivalent to observing
  organic triggering.
- Provider API parameter blocks: the environment's orchestration skill is the
  source of truth for those mechanics.

## Known gaps

- Cursor completion notifications may not include token counts. Aggregation
  labels `output_chars` when it must use that proxy.
- Automated description optimization remains Claude Code-first because
  `run_eval.py` and `improve_description.py` rely on real `claude -p` events.
- No CI fixture currently exercises aggregation and static viewer generation.
- Upstream drift job fails when vendor-identical files diverge or upstream
  moves; a Cloud Agent opens a PR with merge guidance (human review required).
- Additional provider playbooks should be added only for non-substitutable
  mechanics, not generic worker spawning.

## Architecture decisions

1. **Contracts over adapters** — `SKILL.md` defines roles and artifacts, not
   Task API parameters or product-specific tool names.
2. **Thin playbooks** — platform docs cover only timing, CLI, viewer, and
   packaging gaps.
3. **Real trigger evidence** — description evals do not use an LLM's yes/no
   guess as a substitute for invocation events.
4. **Claude Code remains first-class** — upstream `run_eval` and `run_loop`
   behavior is retained with a dedicated playbook.
5. **Intent over byte identity** — copied files stay unchanged unless a
   concrete integration mismatch prevents Anthropic's documented loop.

## Contributing

When adding a playbook:

1. Confirm the behavior cannot live in the environment's orchestration skill.
2. Keep `SKILL.md` neutral and link to the playbook.
3. Extend worker contracts only when the artifact contract changes everywhere.
