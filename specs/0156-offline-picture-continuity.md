# 0.15.6 — Existing-image continuity, never blank novel video after a major beat

Problem: a major beat with no imported image choice may render a black/blank background despite a verified prior local picture; a technical 3600-second encoder split must never change pictures.

- Read-only audit first; optional explicit user confirmation for only the safe candidates.
- Only continue an image verified as already imported and nativeStored, correct image MIME, with a known asset ID.
- A missing opening image cannot be fabricated; existing missing/non-native metadata must not be silently replaced.
- A manually locked blank is intentionally left blank and blocks propagation of older pictures.
- A 3600+ second technical continuation can retain the prior picture, but a conflicting explicit new image on the technical segment causes fail-closed diagnostics, not a silent rewrite.
- Never add new scene boundaries, alter timings, voice, SRT, picture files, photos manually assigned to new scenes, or confirmed locks.
- Every continued picture remains marked 'same-imported-picture-review'. No new artwork generated; offline only.

Requires Node unit QA, full pinned Windows source patch, real native install/upgrade/MP4/backup/uninstall, independent released EXE + Edge click before calling a public release fully verified.
