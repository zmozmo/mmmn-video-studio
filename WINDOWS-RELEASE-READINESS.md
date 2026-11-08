# MMMN Video Studio — Windows 0.14.5 Release Readiness

**Decision: GitHub-hosted Windows release gates PASS; ready for owner-controlled first-device acceptance.**  
Date: 8 November 2026 · Android paused · No download or local user-machine action has been performed by ChatGPT.

## Downloadable Windows release

- Direct, unsigned Windows x64 setup: https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0145/downloads/MMMN-Video-Studio-Setup-0.14.5.exe
- Filename: `MMMN-Video-Studio-Setup-0.14.5.exe`
- Size: **64,844,005 bytes**
- SHA-256: `3afb835da0c14c7b3da761e07b479c15a3956ee97efb771b450467d2f529f274`
- No source ZIP, Python, CMD, VS Code or paid API required for installation or core editing and MP4 export.

## Automated gates already passed

| Independent gate | GitHub run | Evidence |
| --- | --- | --- |
| Windows 0.14.5 source patch, native Build A/B, upgrade, original data safety, offline MP4 | [42498880529](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42498880529) | PASS |
| Windows 0.14.5 exact tested EXE published without rebuild | [42499285203](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499285203) | PASS |
| 0.14.5 downloaded public EXE independent upgrade/UI/backup/security/uninstall | [42499308041](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499308041) | PASS |
| **90-minute continuous Full HD MP4, 162,000 frames, intact source and recovery** | [42499519584](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584) — 90m job | PASS |
| Native Windows Build A/B → Install → Upgrade → Render → Uninstall | [42478959788](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42478959788) | PASS |
| Publish exact tested EXE bytes without rebuild | [42479446166](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479446166) | PASS |
| Real published EXE 0.14.0→0.14.4 upgrade, Edge UI, backup/restore, API security and uninstall | [42479467429](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479467429) | PASS |
| Exact published EXE: synthetic 15-minute streamed WAV, full backup/restore, 3-chapter MP4 merge | [42491529466](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491529466) | PASS |
| Exact published EXE: YouTube/TikTok/Facebook/Square full-resolution, 30fps H.264/AAC exports | [42491917768](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491917768) | PASS |
| Exact published EXE: 45s 1080p three-scene render twice, 9s dissolve, cancel and retry, simulated external-folder snapshot copy-back | [42492649641](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42492649641) | PASS |
| Exact published EXE: continuous 5-minute 1080p MP4, 9,000 frames | [42493062578](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42493062578) | PASS |
| Exact published EXE: continuous 15-minute 1080p MP4, 27,000 frames, prior MP4 preserved | [42493702496](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42493702496) | PASS |

The native build includes 129 Python tests plus the JavaScript suite. Long-form QA verified 28,800,044 WAV bytes and a 6.023-second / 180-frame chapter-concatenation output. These are distinct workloads. **A 15-minute recording import is not the same as a 15-minute video render.** All four platform presets were exercised with 1-second full-resolution synthetic exports, not an hour-long final MP4.

## Actual novel-length acceptance target (owner clarification, 2026-11-08)

The complete narrated MMMN novel lasts **no more than 90 minutes**. A six-to-eight-hour video was an incorrect assumption and is **not a release requirement**.

- **Primary real-novel target:** one complete 90-minute 1920×1080 H.264/AAC MP4, 30fps / **162,000 video frames**. Chapter-by-chapter MP4 production and combining must remain optional.
- **Safety headroom:** test **120 minutes** (216,000 video frames) to allow introduction/outro, audio pauses and future changes; this is a resilience goal, not a new user requirement.
- **Acceptance checks:** full video/audio duration, actual decoded frame count, output integrity, original narration and prior MP4 unchanged, progress/cancel/retry, available disk space, backup/restore and recovery after interruption.
- **Currently verified:** continuous **90-minute Full HD MP4, 162,000 frames**, exact published Windows **0.14.5** EXE ([90-minute QA PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584)); media and full snapshot SHA-256 intact.
- **Not yet verified:** 120-minute optional headroom and the owner's personal Windows 11 laptop. Do not claim these have passed before separate confirmation.

## Conditions still not verified

- User's actual Windows 11 HP laptop hardware and Windows security warnings: **not tested**.
- Over-90-minute optional output and low-memory/low-battery behavior on the user's personal Windows laptop: **not fully tested**.
- Full variety of customer-supplied audio/image/video codecs and damaged real files: **not exhaustively tested**.
- Installer is **unsigned**. SmartScreen may display an unknown publisher warning; adding a genuine code signature requires a recognized signing solution.
- Full backup is local by default. The user must copy a verified complete snapshot directory to another physical drive to withstand disk loss.
- No automatic Google Drive sync or guaranteed Burmese transcription model. The core editor and bundled FFmpeg renderer work offline.

## First-device acceptance when the owner chooses to test

No development environment required. Keep source files private. Launch the exact verified installer from the direct link and check basic UI, a **synthetic/non-sensitive** manuscript, one short WAV, a scene image, an offline MP4 and the verified backup location. For real novels, confirm an independent external-drive backup first. Never upload original unpublished manuscripts, personal voice recordings, account credentials or photo collections to this public GitHub repository.

**Release status: verified hosted-Windows build; owner device acceptance still pending.**
