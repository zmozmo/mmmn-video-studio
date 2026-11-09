# MMMN Video Studio — Windows 0.14.6 Release Readiness

**Decision: GitHub-hosted Windows release gates PASS; ready for owner-controlled first-device acceptance.**  
Date: 9 November 2026 · Android paused · No download or local user-machine action has been performed by ChatGPT.

## Downloadable Windows release

- Direct, unsigned Windows x64 setup: https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0146/downloads/MMMN-Video-Studio-Setup-0.14.6.exe
- Filename: `MMMN-Video-Studio-Setup-0.14.6.exe`
- Size: **64,837,468 bytes**
- SHA-256: `b94b7e9a9f7e5dd373b38216dc2dcc7fa392bb56fd42b981f4f38c2d4a05814f`
- No source ZIP, Python, CMD, VS Code or paid API required for installation or core editing and MP4 export.

## Automated gates already passed

| Independent gate | GitHub run | Evidence |
| --- | --- | --- |
| 0.14.6: 21 conservative Major Scene tests + manual lock + 90/120min static photo bounds | [42555074044](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555074044) | PASS |
| 0.14.6: complete patch chain source preflight & preserved 0.14.4–0.14.5 regression tests | [42555074115](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555074115) | PASS |
| 0.14.6: built installer, real in-place upgrade, recovered original source/backup, offline MP4 | [42555073944](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555073944) | PASS |
| 0.14.6: published exact pretested installer bytes | [42555724317](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555724317) | PASS |
| 0.14.6: independent downloaded EXE; real Edge major scene UI, accurate no-change on rain/girl, change on severe dark storm, backup and security | [42555752046](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555752046) | PASS |
| Windows 0.14.5 source patch, native Build A/B, upgrade, original data safety, offline MP4 | [42498880529](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42498880529) | PASS |
| Windows 0.14.5 exact tested EXE published without rebuild | [42499285203](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499285203) | PASS |
| 0.14.5 downloaded public EXE independent upgrade/UI/backup/security/uninstall | [42499308041](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499308041) | PASS |
| **90-minute continuous Full HD MP4, 162,000 frames, intact source and recovery** | [42499519584](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584) — 90m job | PASS |
| **120-minute continuous Full HD MP4, 216,000 frames, intact source and recovery** | [42499519584](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584) — 120m job | PASS |
| 60 distinct pictures / 59 dissolves, 15-minute Full HD, 61-file recovery snapshot | [42499523807](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499523807) | PASS |
| Native Windows Build A/B → Install → Upgrade → Render → Uninstall | [42478959788](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42478959788) | PASS |
| Publish exact tested EXE bytes without rebuild | [42479446166](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479446166) | PASS |
| Real published EXE 0.14.0→0.14.4 upgrade, Edge UI, backup/restore, API security and uninstall | [42479467429](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479467429) | PASS |
| Exact published EXE: synthetic 15-minute streamed WAV, full backup/restore, 3-chapter MP4 merge | [42491529466](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491529466) | PASS |
| Exact published EXE: YouTube/TikTok/Facebook/Square full-resolution, 30fps H.264/AAC exports | [42491917768](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491917768) | PASS |
| Exact published EXE: 45s 1080p three-scene render twice, 9s dissolve, cancel and retry, simulated external-folder snapshot copy-back | [42492649641](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42492649641) | PASS |
| Exact published EXE: continuous 5-minute 1080p MP4, 9,000 frames | [42493062578](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42493062578) | PASS |
| Exact published EXE: continuous 15-minute 1080p MP4, 27,000 frames, prior MP4 preserved | [42493702496](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42493702496) | PASS |

The native build includes 129 Python tests plus the JavaScript suite. Long-form QA verified 28,800,044 WAV bytes and a 6.023-second / 180-frame chapter-concatenation output. These are distinct workloads. **A 15-minute recording import is not the same as a 15-minute video render.** All four platform presets were exercised with 1-second full-resolution synthetic exports, not an hour-long final MP4.

## Windows 0.14.6 Major Scene feature

The latest installed app includes a **Major-only Auto Draft** option, automatically combining small storyboard beats when there is no important visual shift, while protecting manually confirmed picture choices and timing. Source implementation: [offline conservative scene planner](web/major-scene.mjs). This is **not full Burmese semantic speech recognition**; it uses manuscript/SRT text evidence and optional FFmpeg pause hints. Manual Review remains required. For long quiet narration, technical FFmpeg segments can share one unchanged image, avoiding a fixed-interval slideshow and the native 3600-second per-scene limit.

**Additional pending release test:** one actual continuous **90-minute Full HD MP4 with the same unchanged background across two technical scenes**, on the exact published 0.14.6 EXE. [Live QA run 42555826576](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555826576) — record PASS only after final success. Previously 90-minute and 120-minute full-HD H.264/AAC exports were verified on the immediately preceding **0.14.5** release.

## Actual novel-length acceptance target (owner clarification, 2026-11-08)

The complete narrated MMMN novel lasts **no more than 90 minutes**. A six-to-eight-hour video was an incorrect assumption and is **not a release requirement**.

- **Primary real-novel target:** one complete 90-minute 1920×1080 H.264/AAC MP4, 30fps / **162,000 video frames**. Chapter-by-chapter MP4 production and combining must remain optional.
- **Safety headroom:** test **120 minutes** (216,000 video frames) to allow introduction/outro, audio pauses and future changes; this is a resilience goal, not a new user requirement.
- **Acceptance checks:** full video/audio duration, actual decoded frame count, output integrity, original narration and prior MP4 unchanged, progress/cancel/retry, available disk space, backup/restore and recovery after interruption.
- **Currently verified:** continuous **90-minute Full HD MP4, 162,000 frames**, exact published Windows **0.14.5** EXE ([90-minute QA PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584)); media and full snapshot SHA-256 intact.
- **Verified:** 120-minute optional headroom (**216,000 frames**), 60-distinct-scene storyboard and 59 dissolves, all on independently installed Windows 0.14.5 public EXE.
- **Not yet verified:** the owner's own Windows 11 laptop, real novel narration/photos, and full variety of third-party media codecs.

## Conditions still not verified

- User's actual Windows 11 HP laptop hardware and Windows security warnings: **not tested**.
- Long duration output up to 120 minutes **passed on hosted Windows**, but low-memory/low-battery behavior on the user's personal laptop remains untested.
- Full variety of customer-supplied audio/image/video codecs and damaged real files: **not exhaustively tested**.
- Installer is **unsigned**. SmartScreen may display an unknown publisher warning; adding a genuine code signature requires a recognized signing solution.
- Full backup is local by default. The user must copy a verified complete snapshot directory to another physical drive to withstand disk loss.
- No automatic Google Drive sync or guaranteed Burmese transcription model. The core editor and bundled FFmpeg renderer work offline.

## First-device acceptance when the owner chooses to test

No development environment required. Keep source files private. Launch the exact verified installer from the direct link and check basic UI, a **synthetic/non-sensitive** manuscript, one short WAV, a scene image, an offline MP4 and the verified backup location. For real novels, confirm an independent external-drive backup first. Never upload original unpublished manuscripts, personal voice recordings, account credentials or photo collections to this public GitHub repository.

**Release status: verified Windows 0.14.6 native build and independent public binary/GUI checks. The extra single-picture 90-minute native export has a separately tracked acceptance test. Owner device acceptance still pending.**
