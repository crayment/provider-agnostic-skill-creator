# Skill Creator Fork Comparison

Review date: 2026-08-29

## Scope and method

This review compares:

1. [Anthropic's skill-creator](https://github.com/anthropics/claude-plugins-official/tree/ed404106fcd80ba98ecb7c851e531dcb626d13b7/plugins/skill-creator/skills/skill-creator)
   at upstream `main` commit `ed404106fcd80ba98ecb7c851e531dcb626d13b7`
   and the installed local tree supplied for this review.
2. Greenfield `provider-agnostic-skill-creator` at pre-review commit
   `2ba6fbd` (the canonical target).
3. Refactored `skill-creator-harness` at commit `8ae1251` on
   `refactor/provider-agnostic`.

Statuses and scores below describe those reviewed commits, before the fixes
listed near the end of this document. “Identical” means byte-identical to the
corresponding upstream file. Intent scores measure preservation of Anthropic's
process, not textual similarity:

- **5/5** — preserves the complete upstream purpose and sequencing
- **4/5** — preserves the process with a small omission or integration issue
- **3/5** — useful adaptation with a material fidelity risk
- **1–2/5** — conflicts with, or cannot reliably implement, upstream intent

## Executive verdict

The greenfield fork is the better canonical foundation. It makes the correct
architectural cut: a provider-neutral `SKILL.md`, shared worker contracts,
thin playbooks, and unchanged Claude Code automation. The refactor preserves
more of Anthropic's prose and adds more CLI surface, but some of that surface
is not behaviorally equivalent to upstream trigger evaluation.

Before this review, the refactor was slightly stronger as a process checklist
and in Cursor gap documentation. Greenfield was stronger in neutrality,
Claude Code correctness, and restraint. After the fixes in this review,
greenfield combines the useful documentation from refactor with stricter
Anthropic intent fidelity.

| Dimension | Greenfield (pre-fix) | Refactor | Verdict |
|---|---|---|---|
| Provider neutrality | **Strong**: 289-line neutral workflow; mechanics delegated to contracts/playbooks | Mixed: 510-line `SKILL.md` retains large Claude.ai/Cowork sections; scripts add provider profiles | **Greenfield** |
| Anthropic process fidelity | Strong but over-compressed in description optimization, scale-up, and final packaging | Strongest textual/process preservation; all major stages remain | **Refactor narrowly pre-fix; fixed greenfield now strongest** |
| Claude Code support | Exact upstream `run_eval`/`run_loop`, plus dedicated playbook | First-class and preflighted, but `run_eval` broadens matching beyond the unique injected command and can false-positive | **Greenfield** |
| Cursor orchestration docs | Correct delegation idea, but playbook duplicated Task parameters and unrelated My Machines detail | Thinner playbook, honest token/trigger gaps, clearer fallback | **Refactor pre-fix; best parts merged into greenfield** |
| Script completeness | Exact proven upstream suite; no speculative adapter | Broader surface (`harness.py`, orchestrator batch, experimental Cursor parser, requirements file) | **Refactor for breadth; greenfield for reliable behavior** |

## Anthropic intent fidelity checklist

“Fix needed?” refers to the canonical greenfield fork as reviewed at
`2ba6fbd`. Every identified fix is applied in the current canonical tree.

| Upstream intent | Present in greenfield? | Present in refactor? | Fix needed? |
|-----------------|------------------------|----------------------|-------------|
| Continuous eval sequence (don't stop mid-loop) | **Yes**, stated as continuous, but the summary compressed stages | **Yes**, near-verbatim | **Yes** — full order restored in summary |
| Parallel with-skill + baseline same turn | **Yes**, with an honest platform-support qualification | **Yes**, explicit same-turn rule | No |
| evals.json → eval_metadata → outputs → timing → grading → benchmark → viewer → feedback → improve | **Yes in body**, incomplete in the high-level diagram | **Yes** | **Yes** — diagram and contracts now name every stage |
| Draft assertions while runs in progress | **Yes** | **Yes** | No |
| Grader agent first (not scripts-only) | **Mostly** — grader worker named, but script relationship was implicit | **Yes** — grader worker named; programmatic checks retained | **Yes** — canonical now says scripts support, never replace, the grader |
| grading.json uses text/passed/evidence | **Yes**, exact | **Yes**, exact | No |
| aggregate_benchmark before viewer | **Yes** | **Yes** | No |
| Analyst pass after aggregate | **Yes** | **Yes** | No |
| Blind comparison optional (comparator.md) | **Yes** | **Yes** | No |
| Description optimization track (trigger queries, eval review HTML, run_loop) | **Partial** — all three existed, but holdout/repetition/review constraints were compressed | **Yes**, including provider alternatives | **Yes** — restored query, review, 60/40, three-run, and held-out-selection details |
| Pushy description guidance | **Yes**, shortened | **Yes**, upstream example retained | **Yes** — canonical wording now makes implicit-use contexts explicit |
| Progressive disclosure / references pattern | **Yes**, and structurally strongest | **Yes**, but the 510-line body exceeds its own ideal | No |
| Package skill at end | **Partial** — packaging was conditional and omitted scale-up immediately before it | **Yes**, near-verbatim | **Yes** — final package step is unconditional |
| Generalize improvements (anti-overfit) | **Yes** | **Yes**, near-verbatim | No |

Additional upstream intent checked:

- The final small eval set should be expanded and rerun at larger scale.
  Refactor retained this; greenfield had dropped it. It is restored.
- A programmatic assertion should use a deterministic check, but a complete
  grader pass still interprets all evidence. The canonical wording now makes
  this ordering unambiguous.
- Trigger queries should be substantive and realistic. The canonical
  description track now restores that constraint.
- The user reviews the trigger eval set before optimization. The canonical
  track now explicitly blocks optimization on an unreviewed set.

## Upstream file-by-file inventory

### Core instructions, prompts, schemas, and assets

| Upstream path | Upstream intent | Greenfield status / intent fidelity | Refactor status / intent fidelity |
|---|---|---|---|
| `SKILL.md` | Defines skill authoring and the complete continuous eval/improve/package loop | **Adapted — 4/5.** Excellent neutral structure and progressive disclosure; compressed scale-up, grader/script ordering, description-loop mechanics, and unconditional packaging | **Adapted — 4.5/5.** Retains nearly all process prose and adds orchestration pointers; at 510 lines it weakens progressive disclosure and keeps more provider-specific body content |
| `LICENSE.txt` | Preserves Apache-2.0 licensing for upstream material | **Identical — 5/5.** No process effect; attribution preserved | **Identical — 5/5** |
| `agents/grader.md` | Requires evidence-based grading, claim checking, eval critique, metrics/timing, and exact grading schema | **Identical — 5/5** | **Identical — 5/5** |
| `agents/comparator.md` | Defines blind A/B output comparison without skill identity leakage | **Identical — 5/5** | **Identical — 5/5** |
| `agents/analyzer.md` | Defines both post-hoc comparison analysis and the post-aggregate benchmark analyst pass | **Identical — 5/5** | **Identical — 5/5** |
| `references/schemas.md` | Defines eval, grading, metrics, timing, benchmark, comparison, and analysis fields consumed by tools | **Identical — 5/5** | **Identical — 5/5** |
| `assets/eval_review.html` | Lets a user review/edit/export description trigger queries before optimization | **Identical — 5/5** | **Identical — 5/5** |
| `eval-viewer/viewer.html` | Presents qualitative outputs, grades, benchmark statistics, and feedback UI | **Identical — 5/5** | **Identical — 5/5** |
| `eval-viewer/generate_review.py` | Discovers outputs, builds static/live review UI, and persists feedback | **Identical — 4/5.** Preserves upstream, including an inherited inability to find eval metadata above nested `run-N` layouts | **Identical — 4/5.** Same inherited mismatch |

### Scripts

| Upstream path | Upstream behavior | Greenfield status / intent fidelity | Refactor status / intent fidelity |
|---|---|---|---|
| `scripts/__init__.py` | Empty package marker | **Adapted — 5/5.** Comment-only package marker | **Adapted — 5/5.** Different comment only |
| `scripts/aggregate_benchmark.py` | Reads graded runs and emits benchmark JSON/Markdown before viewer launch | **Identical — 4/5.** Preserves code, including inherited conflict: script required nested `run-N`, while upstream `SKILL.md` directs a direct run directory; config sorting could also put a baseline first | **Identical — 4/5.** Same conflict |
| `scripts/generate_report.py` | Builds HTML history for description optimization iterations | **Identical — 5/5** | **Identical — 5/5** |
| `scripts/improve_description.py` | Uses Claude to propose a better description from train failures and history | **Identical — 5/5** | **Identical — 5/5** |
| `scripts/package_skill.py` | Validates and packages the finished skill | **Identical — 5/5** | **Identical — 5/5** |
| `scripts/quick_validate.py` | Validates frontmatter and Agent Skills metadata constraints | **Identical — 5/5.** Dependency documented in README but not declared in a requirements file | **Identical — 5/5.** Dependency declared in root `requirements.txt` |
| `scripts/run_eval.py` | Injects a uniquely named ephemeral Claude command, runs real `claude -p` queries in parallel, and detects actual Skill/Read events | **Identical — 5/5.** Highest Claude Code behavioral fidelity | **Adapted — 3/5.** Retains Claude path and adds Cursor/orchestrator modes, but also accepts the non-unique base `skill_name` in stream matching, increasing false positives; experimental Cursor detection is broad string matching |
| `scripts/run_loop.py` | Stratified train/test split, repeated trigger eval, train-only improvements, held-out best selection, live/final report | **Identical — 5/5** | **Adapted — 4/5.** Claude loop remains, with useful preflight; Cursor is rejected honestly, but exposed `--mode orchestrator` cannot complete the automated improve loop |
| `scripts/utils.py` | Parses skill frontmatter for optimization scripts | **Identical — 5/5** | **Identical — 5/5** |

No upstream file is absent from either fork.

## Added-file inventory

These paths do not exist in Anthropic's skill directory. Scores indicate
whether the addition reinforces or risks upstream process intent.

### Skill-package additions

| Added path | Greenfield status / intent score | Refactor status / intent score | Intent assessment |
|---|---|---|---|
| `references/worker-contracts.md` | **Added — 4/5** | **Added — 4/5** | Both correctly separate worker roles/artifacts from spawn syntax. Refactor was stronger on same-turn wording and no-worker fallback; those parts are now merged into canonical. Greenfield avoids an under-specified trigger-worker contract. |
| `references/playbooks/claude-code.md` | **Added — 4/5** | **Added — 4/5** | Both keep Claude Code first-class. Greenfield had one incorrect `run_eval --output` example; fixed to stdout redirection. Refactor adds useful preflight notes but depends on its modified scripts. |
| `references/playbooks/cursor.md` | **Added — 3/5** | **Added — 4/5** | Greenfield correctly named Cody's orchestration skills but duplicated API parameters and unrelated My Machines detail. Refactor was thinner and clearer about timing and trigger gaps. Canonical now adopts the thin structure without its speculative trigger batch. |
| `references/cursor-agent-trigger-eval.md` | **Not added — 5/5** | **Added — 2/5** | Honest experimental documentation, but the implementation is not equivalent to upstream: concurrent temporary skills share a workspace and stream detection is substring-based. Useful research note, not canonical behavior. |
| `references/harness-profiles.md` | **Not added — 5/5** | **Added — 4/5** | A deprecated-name index only. Harmless, but unnecessary in the canonical architecture. |
| `scripts/harness.py` | **Not added — 5/5** | **Added — 3/5** | Capability inventory and preflight are useful, but provider API descriptions belong in playbooks/orchestration skills. Its Cursor auth check also differs from `run_eval`'s check, and claimed trigger support rests on experimental parsing. Not merged. |

### Repository-root additions

| Added path | Greenfield status / intent score | Refactor status / intent score | Intent assessment |
|---|---|---|---|
| `README.md` | **Added — 5/5** | **Added — 4/5** | Both explain installation and architecture. Greenfield better matches the canonical repository name and clearly states contracts-over-adapters. |
| `IMPLEMENTATION.md` | **Added — 3/5** | **Added — 4/5** | Greenfield documented decisions but contained stale TODOs (`__init__.py` already existed) and unverified aggregation claims. Refactor was more current. Canonical is now corrected and records merge/rejection decisions. |
| `CHANGELOG.md` | **Not added — 5/5** | **Added — 5/5** | Useful refactor history; not necessary to preserve Anthropic process. |
| `requirements.txt` | **Missing pre-fix — 4/5; added by this review** | **Added — 5/5** with `PyYAML>=6.0` | Useful because `quick_validate.py` imports PyYAML. Canonical now declares current `PyYAML>=6.0.3`. |
| `LICENSE` | **Added — 5/5** | **Added — 5/5** | Root copy of Apache-2.0 license; complements preserved package `LICENSE.txt`. |
| `NOTICE` | **Added — 5/5** | **Added — 5/5** | Both attribute Anthropic. Greenfield's file maps derived directories in more detail. |
| `.gitignore` | **Added — 5/5** | **Added — 5/5** | Both ignore Python/build artifacts. Greenfield also ignores local environments; refactor ignores generated workspaces. No process risk. |

## Detailed script comparison

### `run_eval.py`

Upstream tests real triggering, not whether another model thinks a skill
*would* trigger. It creates a unique temporary command, exposes its
description to Claude Code, runs the raw user query, and watches Skill/Read
tool events for that unique identifier. Greenfield preserves this exactly.

Refactor adds three concepts:

1. A Claude Code runner selected by `--harness`. This is mostly a wrapper
   around upstream behavior.
2. A Cursor headless runner. It creates temporary `.agents/skills` entries and
   searches serialized stream events for path/name plus broad marker words.
   That is best-effort evidence, not upstream-equivalent structured detection.
3. An orchestrator job batch. Each worker receives the skill path and
   description under test. That prompt can itself cause the worker to read the
   skill, contaminating the trigger measurement. The contract says not to
   guess, but it does not define a reliable ambient-discovery isolation
   protocol.

The refactor also changed Claude event detection from the unique injected
command name to “unique name **or base skill name**” in partial streams and
Read paths. A common base name may appear for unrelated reasons, weakening the
control that upstream's unique suffix provides. This change was not merged.

### `run_loop.py`

Greenfield is byte-identical to upstream: stratified holdout, three runs per
query by default, parallel train/test evaluation, train-only proposal context,
held-out best selection, and live/final reports.

Refactor retains that loop and adds useful harness preflight. It correctly
raises for Cursor because `improve_description.py` still requires
`claude -p`. However, accepting a generic `--mode` in the public parser
suggests orchestrator mode can participate in the automated loop; in practice
the function rejects the emitted job batch. The honest hard error is better
than fake optimization, but the added interface is not complete.

### `aggregate_benchmark.py` and viewer integration

Both reviewed forks copied upstream exactly, including an integration bug:

- `SKILL.md` and the viewer support a direct run such as
  `eval-name/with_skill/outputs/`.
- `aggregate_benchmark.py` only accepted
  `eval-name/with_skill/run-N/grading.json`.
- The viewer only searched the run and one parent for `eval_metadata.json`, so
  a nested `run-N` could lose its prompt and eval ID.
- Alphabetical configuration discovery could place `old_skill` or
  `without_skill` before `with_skill`, reversing the meaning of delta.
- `runs_per_configuration` was hardcoded to 3.

The canonical fix supports both layouts, searches ancestors for eval metadata,
orders with-skill before baseline, carries `eval_name`, infers run counts, and
labels `output_chars` when token counts are unavailable. This intentionally
changes bytes to fulfill upstream's documented process.

### Other scripts and utilities

`generate_report.py`, `improve_description.py`, `package_skill.py`,
`quick_validate.py`, and `utils.py` are identical in both forks. Their
behavior therefore matches upstream. Refactor's only additional dependency
support is `requirements.txt`; that useful addition is now in canonical.

## Fixes applied to the canonical repository

1. Restored the complete process order and “do not stop mid-loop” constraint
   in `SKILL.md`.
2. Made same-turn paired execution, immediate timing, grader-first evaluation,
   aggregation, analyst pass, viewer, feedback, iteration, scale-up, and final
   packaging explicit.
3. Restored description-optimization safeguards: pushy descriptions,
   realistic balanced queries, human HTML review, substantive trigger tasks,
   60/40 holdout, three runs, and held-out model selection.
4. Merged refactor's stronger no-worker fallback and same-turn language into
   `worker-contracts.md`.
5. Rewrote the Cursor playbook as a thin gap document with no Task API
   parameters or unrelated Cloud/My Machines material.
6. Fixed the Claude Code playbook's nonexistent `run_eval --output` flag.
7. Reconciled direct and repeated-run layouts across aggregation and viewer,
   and made token proxies explicit.
8. Added a current PyYAML requirements declaration and linked this audit from
   README/implementation docs.

## Items for Cody's decision

1. **Repository consolidation:** Treat
   `provider-agnostic-skill-creator` as canonical and mark
   `skill-creator-harness` / `refactor/provider-agnostic` as superseded, or
   retain the latter explicitly as an experimental Cursor headless lab.
   Maintaining both as peer implementations will invite drift.
2. **Cursor trigger research:** Decide whether experimental
   `cursor-agent` trigger detection belongs in a separate research branch.
   It should not enter canonical until Cursor exposes a stable skill discovery
   and invocation signal with isolated per-query workspaces.
3. **Repository rename:** No rename is needed for the canonical repository;
   `provider-agnostic-skill-creator` accurately describes the architecture.
   If the old harness repository remains, its README should point to the
   canonical project.
