# Skill feedback (runtime friction)

After using provider-agnostic-skill-creator, if something **non-routine** misled
you, leave feedback here. Do not edit the skill.

Follows the [meta-skill-feedback](https://github.com/crayment/meta-skill-feedback)
convention (`feedback/*.md` open queue, `feedback/resolved/` after review).

**This folder is not `feedback.json`.** The eval loop's `feedback.json` holds a
human's review of one iteration's outputs and lives in the eval workspace. This
folder holds agent notes about *this skill's* instructions and harness.

**Public repo:** notes are committed and visible. Keep them generic — no company
or customer names, private skill names or eval prompts, internal hostnames,
workspace paths, model account details, or tokens. Describe the skill-under-test
by shape ("a CLI helper with three evals"). Use a generic machine label
(`local`, `ci-runner`) in the heading, or omit it.

## Before you write

1. Skim open `feedback/*.md` (not README, not `resolved/`).
2. **Same issue already open?** Add a **+1** under **Votes** and a short entry under **Agent comments** on that file.
3. **New issue?** Create one timestamped file — see format below.

## When to write

This skill owns **the eval loop, the worker contracts, the playbooks, and the
harness scripts**, so write here for:

- A worker contract in `references/worker-contracts.md` left an executor, grader, or comparator unsure what to write or where
- A playbook in `references/playbooks/` was wrong or silent for your platform — spawn, timing capture, CLI trigger path
- `aggregate_benchmark`, `generate_review.py`, `run_loop`, `run_eval`, `package_skill`, or `quick_validate` failed, or needed a layout or flag the skill did not mention
- The workspace layout (`iteration-N/eval-<name>/with_skill/...`) did not match what a script expected
- Packaging picked up files that should not ship, such as a target skill's `feedback/` notes
- Description optimization or blind comparison could not run as written in your environment
- Skip routine iterations where the loop ran as written

## Not feedback

| Situation | Where |
|-----------|--------|
| A human's verdict on an iteration's outputs | the workspace `feedback.json` |
| The skill under test misled its executors | that skill's `feedback/`, or its eval results |
| Spawning, resuming, or orchestrating workers on your platform | your environment's orchestration skill or issue tracker |
| Upstream skill-creator changed a vendored file | the scheduled upstream-sync job and its review PR — note here only if this skill's instructions misled you |
| A bug in a vendored upstream script | the upstream skill-creator repo; note here if the fork should work around it |

## Filename (new issues only)

`YYYY-MM-DDTHHMM-<short-slug>.md` — timestamp required; lowercase hyphens in slug.

## New issue — body

# YYYY-MM-DD — <id> · <role> · <machine>

## Context
The platform, which stage of the loop, and the skill-under-test's shape.

## What happened
The contract, playbook, or script, what you expected, what happened, the workaround you used.

## Suggestion (optional)
Smallest skill change that would help. Do not apply it yourself.

## Votes

- **YYYY-MM-DDTHHMM** — <id> · opened

## Agent comments

_(none yet)_

## Same issue again — append only

**Votes:** `- **YYYY-MM-DDTHHMM** — <id> · +1`

**Agent comments:** `### YYYY-MM-DDTHHMM — <id>` then one short paragraph.

## Rules

- One topic per file · duplicates are +1 votes, not new files · no secrets or private eval data · reviewer moves handled notes to `resolved/`
