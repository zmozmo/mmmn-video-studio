# MMMN Video Studio 0.14.8 — Cancellable Offline Speech for Long Novels

**Date:** 2026-11-09 · **Windows 11 x64** · **Offline-first** · **Unsigned installer** · **Android paused**

## Exact released Setup.exe

[Download MMMN-Video-Studio-Setup-0.14.8.exe](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0148/downloads/MMMN-Video-Studio-Setup-0.14.8.exe)

- **File size:** 64,824,609 bytes
- **SHA-256:** `7af13007a0c608688ede3dcfa9c3aa4f984949406e5993ceb710362979e8b42b`
- No new end-user requirement for Python, VS Code or paid video rendering API.

## Improved in 0.14.8

**Offline Audio-first Draft no longer waits on a single blocking local request** when optional local Whisper.cpp model is installed. The app starts a background job, shows an honest phase (preparing audio, recognizing, review ready), offers **⏹ အသံမှစာပြောင်းခြင်း ရပ်ရန်**, polls local job status and lets the user cancel without waiting for a 24-hour command timeout. Child FFmpeg/Whisper processes are terminated on cancellation/timeout.

- Finished SRT is still a **human-review-required draft**. A partial failed or cancelled transcription is **not persisted**; a corrected existing SRT is never silently replaced.
- Only one active speech job is permitted; IDs and requests are validated in a strict authenticated localhost API allowlist.
- Original voice media, existing chapter/scenes, manually locked pictures, verified local snapshots and other prior user data remain protected.
- The earlier **Major-only Scene Draft** rule remains: ordinary rain/character mention does not rotate photos. The **Important Pictures Only** Markdown brief also remains.
- The prior 0.14.5+ FFmpeg full-frame verification, offline H.264/AAC output and chapter joining remain.

## Confirmed acceptance

| Windows gate | Result | Evidence |
| --- | --- | --- |
| Apply source patches 0.14.1–0.14.8, speech worker/cancel regressions, source safety | **PASS** | [42600341890](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42600341890) |
| Native Windows Build A/B, install → in-place upgrade → identical data/snapshot hashes → offline MP4 → uninstall | **PASS** | [42600341966](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42600341966) |
| Publish EXACT tested bytes to binary-only branch, no rebuilt EXE | **PASS** | [42601107418](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42601107418) |
| Independent new Windows runner downloads checksum-matched EXE, real Edge cancel control, rejects invalid speech API IDs, audio import, backup and security | **PASS** | [42601142040](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42601142040) |
| Optional real Whisper.cpp + multilingual base model + short public Burmese audio, local Async API (no mocks) | **In independent QA** | [42601243930](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42601243930) |
| 90-minute full-HD one-background clip on exact public 0.14.7 release, all 162,000 frames | **In independent QA** | [42598420189](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42598420189) |

## What is not yet finished

- **No Whisper.cpp CLI/model bundled in the 0.14.8 Setup.exe.** A compatible model must be installed separately to use real ASR; ordinary offline editing/video export needs no model.
- **Burmese speech recognition accuracy** is not certified. Small/default generic Whisper models may produce poor Burmese transcripts. Independently evaluate a Burmese-specialized lightweight model before claiming automatic, word-accurate voice understanding.
- Full novel manuscript-to-spoken-word alignment may require reviewing original text and SRT before auto scene timing. The current audio-pause/SRT fallback only provides estimates.
- The owner's own laptop, genuine recorded novel, external-drive recovery, battery/heat and all foreign codecs have not been tested.
- No background image generator or Google Drive automatic image fetch. The app produces a minimal image-request brief based on major scenes.
- Installer is unsigned; Windows SmartScreen can warn.

[မြန်မာလို စတင်အသုံးပြုနည်း](WINDOWS-QUICKSTART-MM.md) · [0.14.8 technical SDD](specs/0148-cancellable-offline-speech.md)
