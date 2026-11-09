# MMMN Video Studio — Windows 0.14.7 Release Readiness

**Decision: GitHub-hosted Windows release gates PASS; ready for owner-controlled first-device acceptance.**  
Date: 9 November 2026 · Android paused · No download or local user-machine action has been performed by ChatGPT.

## Downloadable Windows release

- Direct, unsigned Windows x64 setup: https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0147/downloads/MMMN-Video-Studio-Setup-0.14.7.exe
- Filename: `MMMN-Video-Studio-Setup-0.14.7.exe`
- Size: **64,839,519 bytes**
- SHA-256: `ca8b984722c6da971008a457c3d4b0dc734142edf0858d940f2c1bdb03c2f4cb`
- No source ZIP, Python, CMD, VS Code or paid API required for installation or core editing and MP4 export.

## Automated gates already passed

| Independent gate | GitHub run | Evidence |
| --- | --- | --- |
| 0.14.7 12 important-photo brief / 21 conservative-major-scene tests | [42594598985](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42594598985) | PASS |
| 0.14.7 full pinned source patch chain and original storage/renderer tests | [42594925798](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42594925798) | PASS |
| 0.14.7 Windows native installer build/install/in-place upgrade/offline MP4 | [42595044624](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595044624) | PASS |
| 0.14.7 publish exact pretested EXE bytes | [42595856442](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595856442) | PASS |
| 0.14.7 independent released EXE Edge UI, security, full backup/recovery and uninstall | [42595895083](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595895083) | PASS |
| **0.14.7 actual local artwork-brief download of ONLY two important scenes** | [42596100140](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42596100140) | PASS |
| 0.14.7 audio-first UI flow with **synthetic mock** local model SRT (not real ASR quality) | [42596129789](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42596129789) | PASS (mock) |
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

## Windows 0.14.7 Important-Artwork and Optional Narration-First

- The main release includes a **local-only Markdown creation brief** listing only the significant picture beats from the reviewed major-only storyboard. A 90-minute one-picture video does not require extra pictures for internal 3,600-second technical encoder segments.
- The Audio-first button may use **a compatible, separately installed** whisper.cpp CLI + multilingual model, with user consent, to propose Myanmar SRT. If unavailable, the app uses its existing offline pause/estimated timing. This install **does NOT include an ASR model** and **real Burmese recognition quality remains unverified**.
- Rejected or unapproved drafts do not overwrite original narration/media. Image sourcing/generation and Google Drive auto sync are not provided.
- The 0.14.7 Windows installer is built/independently tested, but its final **90-minute full MP4** has not been separately rerun; the exact 0.14.6 installer passed that long-form same-image test [here](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555826576).

## Windows 0.14.6 Major Scene feature

The latest installed app includes a **Major-only Auto Draft** option, automatically combining small storyboard beats when there is no important visual shift, while protecting manually confirmed picture choices and timing. Source implementation: [offline conservative scene planner](web/major-scene.mjs). This is **not full Burmese semantic speech recognition**; it uses manuscript/SRT text evidence and optional FFmpeg pause hints. Manual Review remains required. For long quiet narration, technical FFmpeg segments can share one unchanged image, avoiding a fixed-interval slideshow and the native 3600-second per-scene limit.

**Additional acceptance PASS:** exact published 0.14.6 installer downloaded, checksum-verified and run on hosted Windows. It produced a continuous **90-minute 1920×1080 H.264/AAC MP4 with one unchanged visible background**, exactly **162,000 counted video frames** and original synthetic WAV SHA preserved. Internally two 3,600/1,800-second technical render segments shared the same picture. [Full Windows 0.14.6 acceptance run 42555826576 — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555826576). Previously 120-minute Full HD output on 0.14.5 also PASSed; 120-minute one-picture behavior is covered by unit tests in 0.14.6, not a separate 120-minute real video encode.

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

**Release status: Windows 0.14.7 native installer, independent public binary/GUI, minimal photo brief and optional synthetic transcription UI all PASS. The exact 0.14.6 release proved a 90-minute unchanged-background MP4; no separate 90-minute full encode was performed on 0.14.7. Owner laptop acceptance and real Burmese ASR quality remain pending.**
