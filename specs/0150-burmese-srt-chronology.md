# SDD 0150 — Safer offline Burmese narration timeline

**Status:** implementation candidate, NOT published or accepted until Windows CI and independent installed EXE QA pass.

The 0.14.9 manuscript overlap gate could still accept valid words in a reversed story order, malformed timestamps, or a small set of matching cues among unrelated generated text.

## Requirements
- Entirely local and deterministic. No cloud model, personal content telemetry or automatic image downloads.
- Preserve original narration SHA, manuscript, corrected SRT, manual scene locks, backups and 90-minute render paths.
- Reject malformed/overlapping/reversed/negative/non-finite SRT timings.
- Demand sufficient Burmese evidence in each auditable cue and adequate coverage across the generated transcript.
- Reject major backward jumps in the narration's manuscript order, with safe fallback to pause/text draft.
- Compare first to the original chapter manuscript (not repeatedly concatenated scene derivatives).
- Matching is **NOT** recognition accuracy. Require an explicit user's draft-use choice before proposed ASR timings can influence scene planning.
- A declined or unsupported SRT must not be saved, overwrite reviewed subtitles, or drive picture switches.
- Major-only art switching remains conservative; rain words / minor arrivals alone do not imply new pictures.

## QA
- Node agreement legacy and chronology regression suites.
- Full pinned source patch 0.14.1–0.15.0 and local security tests.
- Real Windows installer, 0.14.0-to-0.15.0 upgrade, Edge and offline render QA.
- Publish EXACT tested setup binary; independently reinstall, test Edge, verify backup/security/uninstall.
- Real Burmese ASR novel-wide accuracy **NOT** certified, and any future external CPU model integration must be benchmarked on multiple independent clips first.
