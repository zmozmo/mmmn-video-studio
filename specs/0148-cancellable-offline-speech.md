# SDD 0148 — Cancellable Offline Speech Processing for Long Novels

**Date:** 2026-11-09 · **OS:** Windows 11 x64 · **Network:** no remote inference · **Android:** paused

## User story
A Myanmar novel may contain up to **90 minutes of narrator audio**. Offline local ASR can take much longer than the clip's runtime, especially on a 16 GB CPU laptop. The app must **not freeze** waiting for hours in a single HTTP request. It needs a visible job state, genuine Cancel operation, safe teardown of the FFmpeg/Whisper subprocess and no accidental overwriting of an already proofread SRT or the original narration.

## Changes to the actual native Windows app (0.14.8)
- New allowed localhost commands: `start_transcription_job`, `get_transcription_job_status`, `cancel_transcription_job`.
- Runs optional local FFmpeg extraction and whisper.cpp in **one background worker**, returning immediately to the UI. Avoids a blocking 24-hour local API request.
- Exposes truthful phases: queued, preparing 16 kHz audio, recognizing offline speech, review-ready, cancelled or failed. **No fake percentage estimate**.
- Windows UI polls status and offers **“⏹ အသံမှစာပြောင်းခြင်း ရပ်ရန်”** while recognizing. Cancelling stops the child process and *does not* continue into an unwanted auto-generated draft.
- A cancelled or failed job saves **no partial transcript**. User's previous corrected SRT, source audio and manually locked scene choices remain untouched.
- The app does not invoke a shell with ASR file paths. Limits job IDs, request parameters, concurrent workers, subprocess runtime and job-history memory.
- If a compatible multilingual CLI/model is absent, the existing `offline_speech_status` clearly says not ready; the app falls back to pause-based estimates, not an invented transcript.
- The original 0.14.5 duration-scaled full-HD verification and 0.14.6–0.14.7 visual rules, picture brief and all backup/security checks remain unchanged.

## Release gate
1. Apply audited Windows patches **0.14.1 → 0.14.8**, verifying patch refusal on unrecognized source versions.
2. Python syntax and JavaScript syntax checks; all existing full-suite tests.
3. Nine dedicated native speech job tests — quick success, real subprocess cancel/timeout, no concurrent worker, no partial SRT, malformed ID/source rejection, preserved optional-model semantics.
4. Real Windows installer Build A + Build B, Install A, in-place upgrade to B with original user data/snapshot hashes intact, MP4 and uninstall.
5. Publish **exact already-tested** Setup.exe bytes, not a rebuild. Then independently download and verify checksum, installed Edge UI Cancel button, authenticated API rejection of bogus speech IDs, backup/restore.
6. The previously published `0.14.7` 90-minute one-photo full-resolution render remains separately verified; do not claim current `0.14.8` 90-minute MP4 performance without a new published-EXE run.
7. A **real CLI/model QA** with public synthetic/test material is separate from the native unit and simulated SRT tests; it must not be called proof of actual Burmese-novel transcription accuracy.

## Still not done
- No compatible multilingual speech model or Whisper CLI is bundled in this ~65 MB native installer, so model setup remains optional and offline speech quality unverified.
- Published research indicates generic Whisper has poor Burmese accuracy; evaluate free Burmese-specific conformer or ONNX models with reproducible **native CPU** tests before adopting a large model or promising automated voice understanding.
- The owner's personal Windows laptop, actual long novel recording, external-drive backups and extended low-memory/thermal behavior remain untested.
- No automatic artwork generation or Google Drive download; important-scene-only picture brief still requires locally imported/created art.

Source: `.github/scripts/upgrade_windows_0148.py` · Tests: `tests/windows_speech_async_0148_test.py`
