# Worker contracts

Platform-neutral roles and artifact layout for the skill-creator eval harness.

Orchestrators spawn workers through **their environment's subagent API** (see playbooks). These contracts define what each worker receives and must produce so grading, aggregation, and the HTML viewer work unchanged.

The required order is: metadata → parallel executors → outputs and timing →
grader → aggregate → analyst → viewer → feedback → improvement.

## Workspace layout

```
<skill-name>-workspace/
├── skill-snapshot/          # Optional: frozen baseline skill when improving
├── iteration-1/
│   ├── benchmark.json
│   ├── benchmark.md
│   ├── feedback.json
│   └── <eval-name>/
│       ├── eval_metadata.json
│       ├── with_skill/
│       │   ├── outputs/       # Task deliverables
│       │   │   ├── metrics.json
│       │   │   └── user_notes.md   # Optional executor uncertainties
│       │   ├── transcript.md
│       │   ├── timing.json
│       │   └── grading.json
│       └── without_skill/     # Or old_skill/ when improving
│           └── (same structure)
└── iteration-2/
    └── ...
```

Legacy names `without_skill` and `with_skill` are required for the benchmark viewer's configuration grouping. When improving an existing skill, baseline runs may live under `old_skill/` instead of `without_skill/` — aggregation accepts both.

For variance measurement, a configuration may contain `run-1/`, `run-2/`, …
directories, each with the same run structure. The aggregation and viewer tools
also accept the direct single-run layout shown above.

## Orchestrator responsibilities

1. Load the environment's subagent orchestration skill before spawning.
2. When parallel workers are available, launch every with-skill and baseline
   executor for the iteration in one orchestration turn. Do not run one side
   first and return later for the other.
3. Write `eval_metadata.json` before or when runs start.
4. Capture timing from worker completion notifications into each run's `timing.json`.
5. After executors finish, use grader workers (grade inline only when workers
   are unavailable).
6. Run `scripts.aggregate_benchmark`, append analyzer notes, launch `eval-viewer/generate_review.py`.
7. Maintain a roster of worker IDs if the platform supports resume (orchestrator-only relay).

---

## Executor worker

**Purpose:** Complete the eval prompt as an independent agent, with or without the skill.

### Inputs (orchestrator provides in prompt)

| Field | Description |
|-------|-------------|
| `task_prompt` | The eval prompt text |
| `skill_path` | Path to skill directory, or `null` for baseline |
| `input_files` | List of paths copied or referenced for this eval |
| `output_dir` | Absolute path ending in `.../outputs/` |
| `transcript_path` | Where to write execution log |
| `deliverables` | What files matter for review (human-readable) |

### Required outputs

| Artifact | Location | Notes |
|----------|----------|-------|
| Task outputs | `{run_dir}/outputs/` | Files the user cares about |
| Transcript | `{run_dir}/transcript.md` | Steps, tools, reasoning summary |
| Metrics | `{run_dir}/outputs/metrics.json` | Tool counts, errors, output size — see schemas |
| User notes | `{run_dir}/outputs/user_notes.md` | Optional: uncertainties, workarounds |
| Timing | `{run_dir}/timing.json` | Orchestrator may write from platform notification |

### Executor prompt template (conceptual)

```
You are an executor worker — not the orchestrator.

Role: Complete the task independently.
Skill: Read SKILL.md at <skill_path> if provided; otherwise use general capabilities only.
Task: <task_prompt>
Inputs: <input_files or none>
Save deliverables to: <output_dir>
Write transcript to: <transcript_path>
Write metrics.json to outputs/ per references/schemas.md.

Do not grade yourself. Do not modify the skill under test unless the eval explicitly requires it.
```

### Baseline selection

| Scenario | Baseline directory | Skill given to baseline worker |
|----------|-------------------|--------------------------------|
| New skill | `without_skill/` | None |
| Improve skill | `old_skill/` | Snapshot at `workspace/skill-snapshot/` |

---

## Grader worker

**Purpose:** Evaluate assertions against transcript and outputs.

### Inputs

| Field | Description |
|-------|-------------|
| `expectations` | List of assertion strings |
| `transcript_path` | Executor transcript |
| `outputs_dir` | Executor outputs directory |
| `grading_output_path` | Usually `{run_dir}/grading.json` |

### Instructions

Read `agents/grader.md` in this skill package.

The grader remains the primary evaluator. For assertions that can be checked
programmatically, run a deterministic script and cite its output as evidence;
do not substitute scripts for the complete grader pass.

### Required output

`grading.json` with `expectations[]` using exactly `text`, `passed`, `evidence`, plus `summary` — see `references/schemas.md`.

---

## Benchmark analyzer (orchestrator or worker)

**Purpose:** Add freeform `notes` to `benchmark.json` after aggregation.

Read `agents/analyzer.md` section "Analyzing Benchmark Results". Output: JSON array of observation strings merged into `benchmark.json` `notes` field.

---

## Blind comparator worker

**Purpose:** Pick winner between two outputs without knowing which skill produced them.

### Inputs

| Field | Description |
|-------|-------------|
| `output_a_path` | Directory or file |
| `output_b_path` | Directory or file |
| `eval_prompt` | Original task |
| `expectations` | Optional assertion list |
| `output_path` | Where to write comparison JSON |

Read `agents/comparator.md`. Output schema: `references/schemas.md` (`comparison.json`).

---

## Post-hoc analyzer worker

**Purpose:** After blind comparison, explain why the winner won and suggest skill improvements.

Read `agents/analyzer.md` (post-hoc section). Inputs: winner/loser skill paths, transcripts, comparison result. Output: `analysis.json` per schema.

---

## eval_metadata.json (per eval directory)

Written by orchestrator:

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

Assertions populate after drafting (Step 2 of eval run).

---

## Fallback when child workers are unavailable

Run prompts sequentially as a non-independent sanity check. Skip baselines,
quantitative benchmarking, and blind comparison because the same agent has
seen both the skill and the eval design. Use the static viewer or inline human
review, and label the limitation explicitly.

---

## feedback.json (per iteration)

Produced by HTML viewer when user submits reviews:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "...", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Only `with_skill` runs typically receive improvement feedback; baseline runs inform benchmarks.

---

## Contract compatibility checklist

Harness adapters should verify:

- [ ] Executor writes `outputs/`, `transcript.md`, `outputs/metrics.json`
- [ ] Grader writes `grading.json` with correct field names
- [ ] Config dirs named `with_skill` and `without_skill` (or `old_skill`)
- [ ] `aggregate_benchmark` input path points at iteration directory
- [ ] Viewer receives `--benchmark` path with schema-compliant JSON
