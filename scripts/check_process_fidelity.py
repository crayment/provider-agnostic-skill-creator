#!/usr/bin/env python3
"""Static checks that fork SKILL.md preserves Anthropic eval-loop intent."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL = REPO_ROOT / ".agents/skills/provider-agnostic-skill-creator/SKILL.md"

REQUIRED_PHRASES = [
    "evals.json",
    "with_skill",
    "grading.json",
    "aggregate_benchmark",
    "generate_review",
    "feedback.json",
    "worker-contracts",
    "grader",
    "comparator",
    "run_loop",
    "description",
    "trigger",
    "parallel",
    "timing.json",
    "passed",
    "evidence",
]


def main() -> int:
    text = SKILL.read_text()
    missing = [p for p in REQUIRED_PHRASES if p not in text]
    if missing:
        print("Process fidelity check FAILED — missing concepts in SKILL.md:")
        for m in missing:
            print(f"  - {m}")
        return 1
    if not re.search(r"text.*passed.*evidence", text, re.I | re.S):
        print("WARN: grading.json field names (text/passed/evidence) not clearly documented")
    print("Process fidelity check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
