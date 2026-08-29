# provider-agnostic-skill-creator

A cross-platform fork of [Anthropic's official skill-creator](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) eval harness, redesigned so the **skill instructions stay provider-neutral** and platform specifics live in **playbooks**.

## Philosophy vs "harness adapter" forks

Many forks wrap one agent product's Task API directly inside `SKILL.md` — Cursor params here, Claude tool names there. That works for one IDE but rots quickly and duplicates orchestration logic across repos.

This project inverts that:

| Layer | What it contains |
|-------|------------------|
| **SKILL.md (~90% neutral)** | Eval loop, schemas, improvement guidance, pointers to contracts |
| **`references/worker-contracts.md`** | Executor, grader, comparator roles; paths; artifact schemas |
| **`references/playbooks/`** | Only non-substitutable platform mechanics (CLI triggers, notification timing, known gaps) |
| **`scripts/`** | Deterministic tooling — aggregation, HTML viewer, `claude -p` trigger evals |

Before spawning workers, the orchestrator loads **its environment's subagent orchestration skill** (e.g. Cursor's `agent-teams-cursor-v2` + `cursor-subagents`, Claude Code's delegation conventions). The harness should work out of the box anywhere that honors the worker contracts.

Claude Code is a first-class target — not a legacy path — via `references/playbooks/claude-code.md` and the upstream `run_loop` / `run_eval` scripts.

## Install

Clone and link the skill per your agent's skill install convention:

```bash
git clone https://github.com/crayment/provider-agnostic-skill-creator.git
# Example: symlink into .agents/skills/
ln -s "$(pwd)/provider-agnostic-skill-creator/.agents/skills/skill-creator" \
  ~/.agents/skills/skill-creator
```

Or copy `.agents/skills/skill-creator/` into your skills directory.

**Requirements:** Python 3.10+ for harness scripts. Subagent-capable agent environment recommended for the full parallel eval loop. PyYAML optional for `quick_validate.py`.

## Quick start

1. Activate the `skill-creator` skill in your agent.
2. Draft a skill and `evals/evals.json`.
3. Follow the eval loop in `SKILL.md` — spawn executors per `references/worker-contracts.md`.
4. Read your platform playbook if needed:
   - [Claude Code](.agents/skills/skill-creator/references/playbooks/claude-code.md)
   - [Cursor](.agents/skills/skill-creator/references/playbooks/cursor.md)

## Repository layout

```
.agents/skills/skill-creator/   # Agent Skills spec skill package
├── SKILL.md
├── agents/                     # Grader, comparator, analyzer prompts
├── references/
│   ├── worker-contracts.md     # Platform-neutral worker roles
│   ├── schemas.md
│   └── playbooks/
├── scripts/                    # aggregate_benchmark, run_loop, run_eval, …
├── eval-viewer/                # HTML review UI
└── assets/
IMPLEMENTATION.md               # Stubs and roadmap
LICENSE                         # Apache-2.0 (upstream)
NOTICE                          # Anthropic attribution
```

## License

Apache License 2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE). Derived from Anthropic's skill-creator plugin; see NOTICE for attribution.

## Related

- [Agent Skills specification](https://agentskills.io/specification)
- Upstream: Anthropic `claude-plugins-official` / `skill-creator` plugin
