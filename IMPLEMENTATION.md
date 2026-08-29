# Implementation status

Stubs, gaps, and planned work for provider-agnostic-skill-creator v0.1.0.

## Done (v0.1.0)

- [x] Provider-neutral `SKILL.md` eval loop
- [x] `references/worker-contracts.md` — executor, grader, analyzer, comparator contracts
- [x] Playbooks: `claude-code.md`, `cursor.md`
- [x] Upstream scripts copied: `aggregate_benchmark`, `run_eval`, `run_loop`, `improve_description`, `generate_report`, `package_skill`, `quick_validate`, `utils`
- [x] Upstream agents: `grader.md`, `comparator.md`, `analyzer.md`
- [x] Upstream eval viewer: `generate_review.py`, `viewer.html`, `assets/eval_review.html`
- [x] Schemas reference from upstream

## Stubbed / TODO

### Harness runner CLI (`scripts/runner.py`) — **not yet implemented**

Planned thin CLI for unavoidable automation only:

```bash
# Proposed interface (stub)
python -m scripts.runner aggregate <iteration-dir> --skill-name foo
python -m scripts.runner viewer <iteration-dir> --static out.html
python -m scripts.runner validate <skill-dir>
```

Today: invoke submodules directly (`python -m scripts.aggregate_benchmark`, `python eval-viewer/generate_review.py`).

**TODO:** Add `runner.py` subcommands that delegate to existing scripts with stable flags; no LLM trigger simulation.

### Cursor `cursor-agent` headless executor — **documented gap**

`references/playbooks/cursor.md` notes experimental headless runs. No verified CLI contract checked in.

**TODO:** Spike cursor-agent flags for executor workers; add playbook section or `scripts/cursor_exec.sh` if stable.

### Token capture on Cursor — **honest gap**

Worker contract allows null `total_tokens`. Aggregation should tolerate missing token stats.

**TODO:** Verify `aggregate_benchmark.py` handles absent tokens gracefully; add test fixture.

### Playbooks for other providers — **future**

- OpenAI Codex / other CLIs — add only when non-substitutable automation exists
- Generic "no subagents" fallback — partially covered in claude-code playbook (Claude.ai section)

### CI / packaging — **future**

**TODO:** GitHub Action: validate skill frontmatter, smoke-test `aggregate_benchmark` on fixture workspace.

### Test fixtures — **future**

**TODO:** Minimal `fixtures/sample-workspace/iteration-1/` with grading.json files for aggregation + viewer smoke tests.

### `scripts/__init__.py`

**TODO:** Add empty `__init__.py` if `python -m scripts.*` fails in some environments (verify).

## Architecture decisions (log)

1. **Contracts over adapters** — SKILL.md never names Cursor Task params or Claude tool names.
2. **Playbooks are thin** — Cursor playbook points to Cody's subagent skills rather than duplicating them.
3. **Scripts stay CLI-bound** — `run_eval` / `run_loop` require real `claude -p`; not replaced by orchestrator YES/NO guessing.
4. **Skill path** — `.agents/skills/skill-creator/` per Agent Skills spec and Cody install conventions.
5. **Upstream compatibility** — artifact schemas unchanged so viewer and aggregation work with existing iteration directories.

## Contributing

When adding a playbook:

1. Confirm the behavior cannot live in the user's orchestration skill.
2. Keep SKILL.md neutral — link to the playbook instead.
3. Extend `worker-contracts.md` only when the artifact contract changes for all platforms.
