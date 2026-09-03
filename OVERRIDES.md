# Intentional fork deltas

Files listed here are **not** expected to match upstream byte-for-byte. CI
(`scripts/check_upstream_drift.py`) treats them separately from
`UPSTREAM_PIN.json` → `vendor_identical`.

See `UPSTREAM_PIN.json` for the machine-readable list and pinned upstream commit.

When the upstream skill-creator tree changes a file we patched, the scheduled
job opens an agent review — do not blindly overwrite our fork with upstream.
Marketplace-only commits on `main` are not skill-creator drift.
