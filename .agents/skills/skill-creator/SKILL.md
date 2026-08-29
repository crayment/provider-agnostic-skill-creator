---
name: skill-creator
description: >-
  Create new skills, modify and improve existing skills, and measure skill
  performance. Use when users want to create a skill from scratch, edit or
  optimize an existing skill, run evals to test a skill, benchmark skill
  performance with variance analysis, or optimize a skill's description for
  better triggering accuracy.
license: Apache-2.0
compatibility: Python 3.10+ for harness scripts; subagent-capable agent environment recommended for full eval loop
metadata:
  upstream: anthropic-claude-plugins-official/skill-creator
  version: "0.1.0"
---

# Skill Creator

A skill for creating new skills and iteratively improving them through an eval loop.

## Before you orchestrate workers

This skill describes **what** each worker must do and **where** artifacts go. It does **not** hardcode platform-specific spawn APIs (Cursor Task params, Claude Code tool names, etc.).

Before spawning any worker:

1. Load **your environment's subagent orchestration skill** (however your product documents team delegation).
2. Read `references/worker-contracts.md` for roles, inputs, outputs, and directory layout.
3. If you need platform-specific mechanics (parallel spawn, timing capture, CLI triggers), read the matching playbook under `references/playbooks/`.

Most harnesses with subagents should work out of the box if they follow the contracts plus their local orchestration skill.

## High-level loop

```
Draft skill → evals.json → parallel with-skill + baseline workers
  → grader → aggregate_benchmark → HTML viewer → human feedback
  → improve skill → (optional) description optimization → (optional) blind comparison
```

Your job is to figure out where the user is in this loop and help them progress. If they want to skip formal evals and iterate conversationally, that is fine.

## Communicating with the user

Users range from terminal-comfortable developers to people new to coding jargon. Match their level. Briefly explain terms like "JSON" or "assertion" when context suggests they may be unfamiliar.

---

## Creating a skill

### Capture intent

Understand what the user wants the skill to do. If the current conversation already contains a workflow to capture, extract tools, steps, corrections, and I/O formats from history first; ask the user to confirm gaps.

1. What should this skill enable the agent to do?
2. When should it trigger?
3. What is the expected output format?
4. Should we set up test cases? Objective outputs (file transforms, extraction, codegen) benefit from evals; subjective outputs (tone, design) often do not. Suggest a default; let the user decide.

### Interview and research

Ask about edge cases, formats, examples, success criteria, and dependencies before writing test prompts. Use available research tools in parallel when helpful.

### Write SKILL.md

Per the [Agent Skills specification](https://agentskills.io/specification):

- **name**: Skill identifier (kebab-case, matches directory name)
- **description**: Primary triggering mechanism — what it does **and** when to use it. Descriptions tend to undertrigger; be slightly pushy about relevant contexts.
- **compatibility**: Only if the skill has real environment requirements

See the skill writing guide below and `references/schemas.md` for eval data structures.

### Skill writing guide

#### Anatomy

```
skill-name/
├── SKILL.md
├── scripts/      # Deterministic automation
├── references/   # Docs loaded on demand
└── assets/       # Templates, static resources
```

#### Progressive disclosure

1. **Metadata** (name + description) — always in context
2. **SKILL.md body** — when skill triggers (<500 lines ideal)
3. **Bundled resources** — as needed

Keep SKILL.md focused; move detail to `references/` with clear pointers.

#### Principle of lack of surprise

Skills must not contain malware or content that surprises the user relative to the stated purpose.

#### Writing patterns

Prefer imperative instructions. Explain **why** behind non-obvious steps. Avoid overfit MUST/NEVER blocks when reasoning works better.

### Test cases

After drafting the skill, propose 2–3 realistic user prompts. Save to `evals/evals.json` (prompts only at first; assertions come while runs execute):

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema.

---

## Running and evaluating test cases

This section is one continuous sequence. Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Organize by iteration (`iteration-1/`, `iteration-2/`, …) and eval directories (`eval-<name>/`). Create directories as you go.

### Step 0: Load orchestration + contracts

Load your environment's subagent orchestration skill. Read `references/worker-contracts.md`.

Spawn **executor workers** (with-skill and baseline) in parallel — all in the same orchestration turn when your platform supports it.

### Step 1: Spawn executor runs

For each eval, launch two executor workers:

| Worker | Role | Baseline when creating new skill | Baseline when improving existing skill |
|--------|------|----------------------------------|----------------------------------------|
| With-skill | Run task with skill available | Current draft skill path | Current iteration skill path |
| Baseline | Run same prompt without skill advantage | No skill (`without_skill/`) | Prior version snapshot (`old_skill/`) |

Each worker must write artifacts per `references/worker-contracts.md` (outputs, transcript, metrics, timing).

Write `eval_metadata.json` per eval directory (assertions may start empty). Use descriptive eval names, not only `eval-0`.

### Step 2: Draft assertions while runs execute

Do not idle. Draft objectively verifiable assertions; explain them to the user. Subjective quality is better reviewed qualitatively in the HTML viewer.

Update `eval_metadata.json` and `evals/evals.json` when assertions are ready.

### Step 3: Capture timing when workers complete

When your platform reports token/duration data on worker completion, write `timing.json` immediately — see `references/worker-contracts.md` and `references/schemas.md`. This data may not be recoverable later.

If your platform does not expose tokens (see `references/playbooks/cursor.md`), record what you have and note the gap in benchmark metadata.

### Step 4: Grade, aggregate, analyze, launch viewer

Once all executor runs finish:

1. **Grade** — spawn a grader worker (or grade inline) using `agents/grader.md`. Save `grading.json` per run. The `expectations` array must use fields `text`, `passed`, and `evidence`.

2. **Aggregate** — from this skill's directory:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   Produces `benchmark.json` and `benchmark.md`. See `references/schemas.md` for exact field names.

3. **Analyze** — read benchmark data; surface patterns per `agents/analyzer.md` (benchmark notes section). Append notes to `benchmark.json`.

4. **Launch viewer**:
   ```bash
   python eval-viewer/generate_review.py <workspace>/iteration-N \
     --skill-name "<name>" \
     --benchmark <workspace>/iteration-N/benchmark.json
   ```
   For iteration 2+, pass `--previous-workspace <workspace>/iteration-<N-1>`.
   Headless environments: use `--static <output_path>` instead of a server.

5. **Tell the user** to review Outputs and Benchmark tabs; feedback saves to `feedback.json`.

### Step 5: Read feedback

When the user is done, read `feedback.json`. Empty feedback means acceptable. Focus improvements on cases with specific complaints.

---

## Improving the skill

### How to think about improvements

1. **Generalize** — evals are a few examples; the skill must work broadly.
2. **Keep the prompt lean** — read transcripts, not just outputs.
3. **Explain why** — help the model reason, not just obey caps-lock rules.
4. **Bundle repeated work** — if every run reinvents the same script, add it to `scripts/`.

### Iteration loop

1. Apply improvements to the skill
2. Rerun all evals into `iteration-<N+1>/` with baselines
3. Launch viewer with `--previous-workspace`
4. Wait for user review
5. Repeat until satisfied, feedback is empty, or progress stalls

---

## Advanced: blind comparison

Optional rigor when comparing two skill versions. Read `agents/comparator.md` and `agents/analyzer.md` (post-hoc section). Requires independent comparator workers and transcripts for both sides.

---

## Description optimization

The `description` frontmatter field drives skill triggering. After the skill content stabilizes, offer to optimize it.

### Step 1: Generate trigger eval queries

Create ~20 queries (mix of should-trigger and should-not-trigger). Save as JSON array:

```json
[
  {"query": "realistic user prompt", "should_trigger": true},
  {"query": "near-miss prompt", "should_trigger": false}
]
```

Favor realistic, detailed prompts and tricky near-miss negatives — not obviously irrelevant negatives.

### Step 2: Review with user

Use `assets/eval_review.html`: replace placeholders, open in browser, user exports edited set.

### Step 3: Run optimization loop

This requires a CLI trigger path (typically Claude Code — see `references/playbooks/claude-code.md`):

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id> \
  --max-iterations 5 \
  --verbose
```

Report progress while it runs. Output includes `best_description` selected on held-out test score.

### Step 4: Apply result

Update SKILL.md frontmatter; show before/after and scores.

---

## Packaging

If your environment supports skill packaging:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

See `references/playbooks/claude-code.md` for `present_files` integration when available.

---

## Reference files

| Path | Purpose |
|------|---------|
| `references/worker-contracts.md` | Executor, grader, comparator roles and artifact paths |
| `references/schemas.md` | JSON schemas for eval artifacts |
| `references/playbooks/claude-code.md` | Claude Code CLI, run_loop, notifications |
| `references/playbooks/cursor.md` | Cursor subagent teams; known gaps |
| `agents/grader.md` | Assertion grading |
| `agents/comparator.md` | Blind A/B comparison |
| `agents/analyzer.md` | Benchmark notes and post-hoc analysis |

---

## Core loop (summary)

- Draft or edit the skill
- Run with-skill and baseline executors on test prompts
- Grade, aggregate, show results in the HTML viewer
- Improve from human feedback
- Optionally optimize description and run blind comparisons
- Package when done
