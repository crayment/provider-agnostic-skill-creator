#!/usr/bin/env python3
"""Compare local skill-creator fork against pinned and latest upstream."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def git_dir_commit(repo: Path) -> str:
    return (
        subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True)
        .strip()
    )


def clone_upstream(url: str, branch: str, dest: Path) -> None:
    subprocess.check_call(
        [
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            branch,
            url,
            str(dest),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pin-file",
        type=Path,
        default=REPO_ROOT / "UPSTREAM_PIN.json",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=REPO_ROOT / "upstream-drift-report.md",
    )
    parser.add_argument(
        "--github-output",
        type=Path,
        help="Append GITHUB_OUTPUT key=value pairs when upstream drift detected",
    )
    args = parser.parse_args()

    pin = json.loads(args.pin_file.read_text())
    canonical = pin["canonical"]
    local_root = REPO_ROOT / pin["local_skill_path"]
    upstream_url = f"https://github.com/{canonical['repo']}.git"
    skill_rel = canonical["skill_path"]
    pinned_commit = canonical["commit"]

    with tempfile.TemporaryDirectory() as tmp:
        upstream = Path(tmp) / "upstream"
        clone_upstream(upstream_url, canonical["branch"], upstream)
        latest_commit = git_dir_commit(upstream)
        upstream_skill = upstream / skill_rel

        lines: list[str] = [
            "# Upstream drift report",
            "",
            f"- **Canonical upstream:** [{canonical['repo']}]({canonical['url']})",
            f"- **Pinned commit:** `{pinned_commit[:12]}`",
            f"- **Latest `{canonical['branch']}`:** `{latest_commit[:12]}`",
            "",
        ]

        upstream_moved = pinned_commit != latest_commit
        if upstream_moved:
            lines.append(
                f"⚠️ Upstream `{canonical['branch']}` has moved since pin "
                f"(`{pinned_commit[:12]}` → `{latest_commit[:12]}`)."
            )
            lines.append("")
        else:
            lines.append("✓ Pinned commit matches latest upstream branch tip.")
            lines.append("")

        vendor_stale: list[str] = []
        lines.append("## Vendor-identical files (must match upstream latest)")
        lines.append("")
        for rel in pin["vendor_identical"]:
            local = local_root / rel
            remote = upstream_skill / rel
            if not local.is_file():
                lines.append(f"- ❌ **missing locally:** `{rel}`")
                vendor_stale.append(rel)
                continue
            if not remote.is_file():
                lines.append(f"- ❌ **removed upstream:** `{rel}`")
                vendor_stale.append(rel)
                continue
            lh, rh = sha256(local), sha256(remote)
            if lh == rh:
                lines.append(f"- ✓ `{rel}`")
            else:
                lines.append(f"- ❌ **drift:** `{rel}` (local ≠ upstream latest)")
                vendor_stale.append(rel)
        lines.append("")

        patched_upstream_changed: list[str] = []
        lines.append("## Fork patches (upstream file changed since pin)")
        lines.append("")
        for entry in pin["fork_patches"]:
            rel = entry["path"]
            remote = upstream_skill / rel
            if not remote.is_file():
                lines.append(f"- ⚠️ `{rel}` — gone upstream; review required")
                patched_upstream_changed.append(rel)
                continue
            # Shallow clone only has latest; note if we are behind pin era
            if upstream_moved:
                lines.append(
                    f"- 🔍 `{rel}` — upstream tip moved; agent should diff "
                    f"({entry['reason']})"
                )
                patched_upstream_changed.append(rel)
            else:
                lines.append(f"- ✓ `{rel}` — no upstream tip movement")
        lines.append("")

        needs_agent = upstream_moved or bool(vendor_stale) or bool(
            patched_upstream_changed
        )
        needs_attention = upstream_moved or bool(vendor_stale)

        lines.append("## Summary")
        lines.append("")
        if not needs_attention:
            lines.append("No action required — vendor files match upstream latest.")
        else:
            lines.append(
                "Action recommended: review upstream changes and bump "
                "`UPSTREAM_PIN.json` after merge."
            )
            if vendor_stale:
                lines.append("")
                lines.append("Stale vendor files:")
                for rel in vendor_stale:
                    lines.append(f"- `{rel}`")

        report_text = "\n".join(lines) + "\n"
        args.report.write_text(report_text)
        print(report_text)

        if args.github_output:
            with args.github_output.open("a") as fh:
                fh.write(f"upstream_moved={'true' if upstream_moved else 'false'}\n")
                fh.write(f"needs_agent={'true' if needs_agent else 'false'}\n")
                fh.write(f"needs_attention={'true' if needs_attention else 'false'}\n")
                fh.write(f"upstream_latest={latest_commit}\n")
                fh.write(f"report_path={args.report}\n")

        return 1 if needs_attention else 0


if __name__ == "__main__":
    sys.exit(main())
