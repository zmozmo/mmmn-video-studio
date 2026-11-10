# MMMN Windows 0.15.1 — Offline narration timing audit

## Why
An SRT may contain real matching Burmese words but only cover the opening
few seconds of a 90-minute novel, have misleading gaps or end prematurely.
The prior manuscript agreement guard alone cannot certify the timestamps.

## Requirements
- Pure local check; read-only; original voice and manually reviewed SRT stay unchanged.
- Audit the full imported narration duration against proposed SRT timing.
- Fail closed on reversed, overlapping, out-of-range, NaN and unreasonably long cues.
- Expose cue count, coverage, opening/trailing silence and longest missing span.
- Do not silently use incomplete automated SRT to decide picture change timing.
- Show summary from a dedicated UI action even when no SRT is present.
- Continue to require manuscript agreement and an explicit human choice before
  an SRT is even proposed to the major-scene draft.
- Manual timing locks and manually corrected SRT are not overwritten; no AI
  image generation, microphone upload, model downloads, telemetry or cloud calls.
- No probability, exact word alignment or semantic understanding is claimed.

## Acceptance
- Node regression tests cover short, long (5400s), gaps and malformed cues.
- Patched-source preflight checks the real UI button and fail-closed path.
- Native Windows release build, in-place upgrade, bundled FFmpeg render and
  installed published-EXE independent Edge QA must pass before publication.

SRT coverage is **not** semantic accuracy or word-level timing alignment.
