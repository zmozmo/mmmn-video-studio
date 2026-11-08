# MMMN Video Studio — Windows 0.14.4 Release Readiness

**Decision: GitHub-hosted Windows release gates PASS; ready for owner-controlled first-device acceptance.**  
Date: 8 November 2026 · Android paused · No download or local user-machine action has been performed by ChatGPT.

## Downloadable Windows release

- Direct, unsigned Windows x64 setup: https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0144/downloads/MMMN-Video-Studio-Setup-0.14.4.exe
- Filename: `MMMN-Video-Studio-Setup-0.14.4.exe`
- Size: **64,855,430 bytes**
- SHA-256: `db57d26241c19c9a2629f959245fa0ecb74c86d5a9bbfe04df8031cfe5da6830`
- No source ZIP, Python, CMD, VS Code or paid API required for installation or core editing and MP4 export.

## Automated gates already passed

| Independent gate | GitHub run | Evidence |
| --- | --- | --- |
| Native Windows Build A/B → Install → Upgrade → Render → Uninstall | [42478959788](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42478959788) | PASS |
| Publish exact tested EXE bytes without rebuild | [42479446166](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479446166) | PASS |
| Real published EXE 0.14.0→0.14.4 upgrade, Edge UI, backup/restore, API security and uninstall | [42479467429](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479467429) | PASS |
| Exact published EXE: synthetic 15-minute streamed WAV, full backup/restore, 3-chapter MP4 merge | [42491529466](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491529466) | PASS |
| Exact published EXE: YouTube/TikTok/Facebook/Square full-resolution, 30fps H.264/AAC exports | [42491917768](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491917768) | PASS |
| Exact published EXE: 45s 1080p three-scene render twice, 9s dissolve, cancel and retry, simulated external-folder snapshot copy-back | [42492649641](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42492649641) | PASS |

The native build includes 129 Python tests plus the JavaScript suite. Long-form QA verified 28,800,044 WAV bytes and a 6.023-second / 180-frame chapter-concatenation output. These are distinct workloads. **A 15-minute recording import is not the same as a 15-minute video render.** All four platform presets were exercised with 1-second full-resolution synthetic exports, not an hour-long final MP4.

## Conditions still not verified

- User's actual Windows 11 HP laptop hardware and Windows security warnings: **not tested**.
- Very long (hour-scale) encoded H.264/AAC chapter exports and low-memory/low-battery behavior on the user's laptop: **not tested**.
- Full variety of customer-supplied audio/image/video codecs and damaged real files: **not exhaustively tested**.
- Installer is **unsigned**. SmartScreen may display an unknown publisher warning; adding a genuine code signature requires a recognized signing solution.
- Full backup is local by default. The user must copy a verified complete snapshot directory to another physical drive to withstand disk loss.
- No automatic Google Drive sync or guaranteed Burmese transcription model. The core editor and bundled FFmpeg renderer work offline.

## First-device acceptance when the owner chooses to test

No development environment required. Keep source files private. Launch the exact verified installer from the direct link and check basic UI, a **synthetic/non-sensitive** manuscript, one short WAV, a scene image, an offline MP4 and the verified backup location. For real novels, confirm an independent external-drive backup first. Never upload original unpublished manuscripts, personal voice recordings, account credentials or photo collections to this public GitHub repository.

**Release status: verified hosted-Windows build; owner device acceptance still pending.**
