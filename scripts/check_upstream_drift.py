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


def git_rev_parse(repo: Path, spec: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", spec],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return None


def git_dir_commit(repo: Path) -> str:
    commit = git_rev_parse(repo, "HEAD")
    if not commit:
        raise RuntimeError(f"could not resolve HEAD in {repo}")
    return commit


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
    pinned_skill_tree = canonical.get("skill_tree")

    with tempfile.TemporaryDirectory() as tmp:
        upstream = Path(tmp) / "upstream"
        clone_upstream(upstream_url, canonical["branch"], upstream)
        latest_commit = git_dir_commit(upstream)
        latest_skill_tree = git_rev_parse(upstream, f"HEAD:{skill_rel}")
        upstream_skill = upstream / skill_rel

        repo_moved = pinned_commit != latest_commit
        if pinned_skill_tree and latest_skill_tree:
            skill_tree_moved = pinned_skill_tree != latest_skill_tree
        else:
            # Old pins without skill_tree cannot distinguish marketplace HEAD
            # movement from skill-creator edits; fall back to repo HEAD.
            skill_tree_moved = repo_moved

        lines: list[str] = [
            "# Upstream drift report",
            "",
            f"- **Canonical upstream:** [{canonical['repo']}]({canonical['url']})",
            f"- **Pinned commit:** `{pinned_commit[:12]}`",
            f"- **Latest `{canonical['branch']}`:** `{latest_commit[:12]}`",
        ]
        if pinned_skill_tree:
            lines.append(f"- **Pinned skill tree:** `{pinned_skill_tree[:12]}`")
        if latest_skill_tree:
            lines.append(f"- **Latest skill tree:** `{latest_skill_tree[:12]}`")
        lines.append("")

        if skill_tree_moved:
            lines.append(
                f"⚠️ Upstream skill-creator tree has moved since pin "
                f"(`{(pinned_skill_tree or pinned_commit)[:12]}` → "
                f"`{(latest_skill_tree or latest_commit)[:12]}`)."
            )
            lines.append("")
        elif repo_moved:
            lines.append(
                f"✓ Skill-creator tree unchanged "
                f"(`{(latest_skill_tree or pinned_skill_tree or 'unknown')[:12]}`) "
                f"even though `{canonical['branch']}` moved "
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
            if skill_tree_moved:
                lines.append(
                    f"- 🔍 `{rel}` — skill-creator tree moved; agent should diff "
                    f"({entry['reason']})"
                )
                patched_upstream_changed.append(rel)
            else:
                lines.append(f"- ✓ `{rel}` — skill-creator tree unchanged")
        lines.append("")

        needs_agent = skill_tree_moved or bool(vendor_stale) or bool(
            patched_upstream_changed
        )
        needs_attention = skill_tree_moved or bool(vendor_stale)

        lines.append("## Summary")
        lines.append("")
        if not needs_attention:
            if repo_moved and not skill_tree_moved:
                lines.append(
                    "No action required — vendor files match upstream latest "
                    "and the skill-creator tree is unchanged."
                )
            else:
                lines.append(
                    "No action required — vendor files match upstream latest."
                )
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
                fh.write(f"upstream_moved={'true' if skill_tree_moved else 'false'}\n")
                fh.write(f"repo_moved={'true' if repo_moved else 'false'}\n")
                fh.write(f"skill_tree_moved={'true' if skill_tree_moved else 'false'}\n")
                fh.write(f"needs_agent={'true' if needs_agent else 'false'}\n")
                fh.write(f"needs_attention={'true' if needs_attention else 'false'}\n")
                fh.write(f"upstream_latest={latest_commit}\n")
                if latest_skill_tree:
                    fh.write(f"upstream_skill_tree={latest_skill_tree}\n")
                fh.write(f"report_path={args.report}\n")

        return 1 if needs_attention else 0


if __name__ == "__main__":
    sys.exit(main())
