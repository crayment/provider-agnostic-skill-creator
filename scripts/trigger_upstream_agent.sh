#!/usr/bin/env bash
# Launch a Cursor Cloud Agent to review upstream drift and open a PR when appropriate.
#
# Usage (scheduled job):
#   CURSOR_API_KEY=... bash scripts/trigger_upstream_agent.sh
#
# Requires upstream-drift-report.md in the working directory (repo root).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

REPORT="${REPO_ROOT}/upstream-drift-report.md"
PROMPT_TEMPLATE="${REPO_ROOT}/scripts/upstream_review_prompt.md"
API_BASE="${CURSOR_API_BASE:-https://api.cursor.com}"
REPO_URL="${UPSTREAM_REVIEW_REPO_URL:-https://github.com/crayment/provider-agnostic-skill-creator}"
REPO_SLUG="${UPSTREAM_REVIEW_REPO_SLUG:-crayment/provider-agnostic-skill-creator}"
STARTING_REF="${UPSTREAM_REVIEW_REF:-main}"
AGENT_NAME="${UPSTREAM_REVIEW_AGENT_NAME:-upstream skill-creator drift review}"
BRANCH_PREFIX="${UPSTREAM_REVIEW_BRANCH_PREFIX:-cursor/upstream-skill-creator-drift-review-}"

# Reuse an already-open drift-review PR instead of stacking a new one every
# time the scheduled job fires while a prior review is still unmerged.
EXISTING_PR_URL=""
if command -v gh >/dev/null 2>&1 && { [[ -n "${GH_TOKEN:-}" ]] || [[ -n "${GITHUB_TOKEN:-}" ]]; }; then
  EXISTING_PR_URL="$(
    gh pr list \
      --repo "$REPO_SLUG" \
      --state open \
      --json headRefName,url \
      --jq "[.[] | select(.headRefName | startswith(\"${BRANCH_PREFIX}\"))][0].url // \"\"" \
      2>/dev/null || true
  )"
fi

if [[ -n "$EXISTING_PR_URL" ]]; then
  echo "Found existing open drift-review PR: $EXISTING_PR_URL — will update it instead of opening a new one."
else
  echo "No existing open drift-review PR found — will open a new one."
fi

if [[ -z "${CURSOR_API_KEY:-}" ]]; then
  echo "ERROR: CURSOR_API_KEY is not set" >&2
  exit 1
fi

if [[ ! -f "$REPORT" ]]; then
  echo "ERROR: missing $REPORT — run check_upstream_drift.py first" >&2
  exit 1
fi

if [[ ! -f "$PROMPT_TEMPLATE" ]]; then
  echo "ERROR: missing $PROMPT_TEMPLATE" >&2
  exit 1
fi

export REPORT PROMPT_TEMPLATE API_BASE REPO_URL STARTING_REF AGENT_NAME EXISTING_PR_URL
export CURSOR_API_KEY

python3 - <<'PY'
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

report = Path(os.environ["REPORT"]).read_text()
template = Path(os.environ["PROMPT_TEMPLATE"]).read_text()
existing_pr_url = os.environ.get("EXISTING_PR_URL", "").strip()

if existing_pr_url:
    pr_mode_note = (
        f"An open drift-review PR already exists ({existing_pr_url}). You are "
        "resuming work on that same PR/branch — do not open a second PR."
    )
else:
    pr_mode_note = (
        "No open drift-review PR exists yet. `autoCreatePR` is enabled for "
        "this run — your branch should become a new pull request when you finish."
    )

prompt = template.replace("{{DRIFT_REPORT}}", report).replace(
    "{{PR_MODE_NOTE}}", pr_mode_note
)

api = os.environ["API_BASE"]
key = os.environ["CURSOR_API_KEY"].encode()
auth = "Basic " + base64.b64encode(key + b":").decode()

repo_entry = {"url": os.environ["REPO_URL"]}
payload = {
    "name": os.environ["AGENT_NAME"],
    "prompt": {"text": prompt},
    "repos": [repo_entry],
}

if existing_pr_url:
    # Push new commits straight to the existing PR's branch instead of
    # creating a sibling branch/PR for the same drift finding.
    repo_entry["prUrl"] = existing_pr_url
    payload["workOnCurrentBranch"] = True
else:
    repo_entry["startingRef"] = os.environ["STARTING_REF"]
    payload["autoCreatePR"] = True
    payload["skipReviewerRequest"] = True

data = json.dumps(payload).encode()
req = urllib.request.Request(
    api + "/v1/agents",
    data=data,
    headers={"Authorization": auth, "Content-Type": "application/json"},
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        created = json.load(resp)
except urllib.error.HTTPError as e:
    body = e.read().decode("utf-8", "replace")[:800]
    print(f"ERROR create HTTP {e.code}: {body}", file=sys.stderr)
    sys.exit(1)

agent = created.get("agent") or {}
aid = agent.get("id")
url = agent.get("url")
status = agent.get("status")

if not aid:
    print("ERROR: unexpected create response: " + json.dumps(created)[:500], file=sys.stderr)
    sys.exit(1)

print(f"Cloud Agent started: id={aid} status={status}")
if url:
    print(f"Dashboard: {url}")
PY

unset CURSOR_API_KEY
