# Intentional fork deltas

Files listed here are **not** expected to match upstream byte-for-byte. CI
(`scripts/check_upstream_drift.py`) treats them separately from
`UPSTREAM_PIN.json` → `vendor_identical`.

See `UPSTREAM_PIN.json` for the machine-readable list and pinned upstream commit.

When upstream changes a file we patched, CI opens an agent review — do not
blindly overwrite our fork with upstream.
