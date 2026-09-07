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
STARTING_REF="${UPSTREAM_REVIEW_REF:-main}"
# ⚡ = GitHub Actions (not 🤖 — that prefix is Mini LaunchAgent wakes).
AGENT_NAME="${UPSTREAM_REVIEW_AGENT_NAME:-⚡ provider-agnostic-skill-creator}"

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

export REPORT PROMPT_TEMPLATE API_BASE REPO_URL STARTING_REF AGENT_NAME
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
prompt = template.replace("{{DRIFT_REPORT}}", report)

api = os.environ["API_BASE"]
key = os.environ["CURSOR_API_KEY"].encode()
auth = "Basic " + base64.b64encode(key + b":").decode()

payload = {
    "name": os.environ["AGENT_NAME"],
    "prompt": {"text": prompt},
    "repos": [
        {
            "url": os.environ["REPO_URL"],
            "startingRef": os.environ["STARTING_REF"],
        }
    ],
    "autoCreatePR": True,
    "skipReviewerRequest": True,
}

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
