# Playbook: Cursor

Thin platform notes for running the skill-creator harness in Cursor IDE agents.

## Subagent orchestration (required reading)

Before spawning workers, load:

1. **`cursor-subagents`** — spawn/resume mechanics, full-power defaults, ownership rules
2. **`agent-teams-cursor-v2`** — frame → assign → warm up → align → build → handoff; one roster

These skills replace hardcoded Task API parameters in the main skill-creator SKILL.md. Follow their roster, relay, and parallel-warmup patterns when coordinating executor and grader workers.

### Spawning executor workers

Use the worker contract prompts from `references/worker-contracts.md`. Typical Cursor settings (adjust per task, do not treat as universal law):

- `subagent_type: "generalPurpose"` for executors and graders
- `run_in_background: true` when launching the full parallel eval batch
- `environment: "local"` unless cloud isolation is explicitly needed

First prompt to each child should state role, slice, done-when criteria, and paths — children start with clean context.

### Parallel batch

Launch all with-skill **and** baseline executors in the same orchestration turn (`run_in_background: true` for each), matching upstream harness timing.

## Honest gaps

| Capability | Cursor status | Workaround |
|------------|---------------|------------|
| Token counts in Task completion | **Not consistently exposed** to parent agent | Record `duration_ms` if available; leave `total_tokens` null; note in benchmark metadata |
| `run_loop` / description optimization | Requires **`claude -p` CLI** | Use Claude Code playbook on a machine with CLI, or stub/manual description iteration |
| `present_files` | Cursor-specific / unavailable | Use `package_skill.py`; tell user the output path |
| Timing notification shape | May differ from Claude Code Task API | Capture whatever completion metadata exists; document in `timing.json` |

## Optional: headless investigation

Experimental: `cursor-agent` CLI for non-interactive runs may suit CI-style executor workers. Not required for the default harness — subagents in IDE are the primary path.

TODO: document stable CLI flags once cursor-agent headless contract is verified (see IMPLEMENTATION.md).

## Resume and roster

Track child agent IDs on the orchestrator roster. Only the spawning agent may resume a child. Use relay for cross-slice questions per agent-teams-cursor-v2.

## Viewer

Same as other platforms:

```bash
python eval-viewer/generate_review.py <workspace>/iteration-N \
  --skill-name "<name>" \
  --benchmark <workspace>/iteration-N/benchmark.json
```

Use `--static` in remote/cloud environments without a local browser.

## My Machines / Cloud Agents

Cloud agents on a Mac (My Machines) are a **separate system** from IDE subagents — see Cody's `running-agents` pattern doc. Use My Machines when Cody needs phone-visible runs or local tool access outside the current chat; use IDE subagents for parallel eval executors in-session.

Do not conflate Cloud Agent API follow-ups with Task resume IDs.
