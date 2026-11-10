# MMMN Video Studio 0.15.4 — Optional Offline Burmese CPU ASR Support

**10 November 2026** · Windows 11 x64 · unsigned setup, no paid API, Android paused.

**[Download published exact 0.15.4 Windows Studio setup.exe](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0154/downloads/MMMN-Video-Studio-Setup-0.15.4.exe)**

- Windows Studio setup: 64,832,335 bytes
- SHA-256: 318d7d37addd1fec3be226460ac198baecf31cd018bd0d0d984de8351abaf1c9
- A Burmese model add-on is a **separate optional package**, not inside this approximately 65 MB Windows Studio setup. Its one-click Windows CPU installer is under real packaging QA, and is NOT yet approved for distribution.

## New support in installed Studio

- Detect a complete local Burmese-language CPU Conformer add-on installed under the user's local Studio data folder and prefer it to the optional generic whisper.cpp fallback.
- Keep existing asynchronous narration transcription jobs, cancel, local FFmpeg, privacy, unchanged original recordings, reviewed SRT and protected visual scenes.
- Generated Burmese speech subtitles remain tentative; validate manuscript evidence, whole-recording timing coverage, unique scene cues and obtain explicit human consent before changing any major-scene draft.
- If no add-on is present, video editing and full-HD MP4 export remain available, and prior compatible Whisper fallback remains optional.

## Evidence

| Real QA | Status | Evidence |
| --- | --- | --- |
| Public licensed real Burmese speech, 108.24 s stitched from 6 clips, segmented model-generated local SRT | PASS | [CPU model E2E](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42762225771) |
| Full synthetic source patch chain + 9 backend addon tests | PASS | [Preflight](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42763027545) |
| Native Windows build/upgrade/MP4/154 Python tests/data SHA/uninstall | PASS | [Native Windows](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42763027222) |
| Publish byte-identical unsigned Windows Studio setup | PASS | [Publisher](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42763651702) |
| Independent exact downloaded Studio setup, Edge, media, security and uninstall | PASS | [Independent Windows](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42763681555) |
| Independently built one-click local Burmese CPU Model Add-on and real installed Windows model inference | IN PROGRESS | [Addon QA](https://github.com/zmozmo/mmmn-video-studio/actions/workflows/windows-burmese-offline-model-pack-0154.yml) |
| 90-minute 1080p full MP4 from exact published 0.15.4 EXE | IN PROGRESS | [Long MP4 QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42763681451) |

## Still unverified

- A real human's long Burmese novel speech on the owner's 16 GB Windows laptop, model memory/duration and accurate word-by-word timestamp alignment.
- Add-on installation is not complete until dedicated real Windows CPU model QA and cross-package integration pass.
- Autonomous offline AI image creation, fully semantic major-scene interpretation, Google Drive private media syncing, Windows code signing and Android app.

**No private manuscript, audio or personal photos are included in the public source or CI.**
