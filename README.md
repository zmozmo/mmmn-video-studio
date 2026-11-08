# MMMN Video Studio — Windows Offline-first

**Latest verified Windows release: 0.14.4 (unsigned)** · 8 November 2026  
**Android: paused** · **Personal laptop: deliberately not tested**

## One-click Windows x64 Installer (direct EXE, no ZIP)

**[MMMN Video Studio 0.14.4 Windows setup.exe](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0144/downloads/MMMN-Video-Studio-Setup-0.14.4.exe)**

- Filename: `MMMN-Video-Studio-Setup-0.14.4.exe`
- Size: **64,855,430 bytes**
- SHA-256: `db57d26241c19c9a2629f959245fa0ecb74c86d5a9bbfe04df8031cfe5da6830`
- [Published direct executable and independent acceptance record](https://github.com/zmozmo/mmmn-video-studio/tree/windows-binaries-0144/downloads)

There is no requirement for VS Code, CMD, Python/Node.js installation, source ZIP or a paid video API to use the installed application. **Unsigned**: Windows SmartScreen may display an unknown-publisher warning; check the exact checksum. The user's actual Windows 11 laptop has not been tested yet.

## Features

- Local-first Burmese manuscript editor with scene-by-scene storyboard, image choices, manual scene locking and timing. Editing a manuscript **preserves** scene choices, manual locks and existing timing.
- Import your own WAV/MP3 audio narration, images and videos. Imports check available disk space at the beginning and **before each chunk**, reserve space for parallel imports, and reject unsafe symlink/media collisions.
- Render H.264/AAC MP4 using bundled FFmpeg, without external API/subscription: YouTube 16:9, TikTok/Shorts/Reels 9:16, Facebook 4:5 and square presets.
- Create **verified full-media local backups**, verify via SHA-256, restore after an accidental edit, open Project/Backup/MP4 folders directly in Windows Explorer and keep existing user files across in-place installer upgrades/uninstalls.
- New in **0.14.4**: unique exclusive project-save staging files with failure cleanup, project-recovery symlink protection, and collision-safe media finalization. Old trial labels and obsolete ZIP/CMD backup instructions corrected. Nine new regression tests.

[Full 0.14.4 release notes](WINDOWS-0144-RELEASE-NOTES.md) · [0.14.3 notes](WINDOWS-0143-RELEASE-NOTES.md)

## Exact native and independently downloaded Windows acceptance

| Gate | Outcome | Evidence |
| --- | --- | --- |
| Native Windows 0.14.4 Build A/B, install and in-place upgrade | **PASS** | [Run 42478959788](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42478959788) |
| Bundled offline FFmpeg MP4, real Edge UI and preserved project/media checksums | **PASS** | [Same native run](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42478959788) |
| Published the exact tested EXE, no binary rebuild | **PASS** | [Run 42479446166](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479446166) |
| Independent runner downloads public EXE, upgrades real 0.14.0, UI/backup/security/uninstall tests | **PASS** | [Run 42479467429](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479467429) |
| Additional 15-minute WAV streaming, full backup/restore and 3-chapter MP4 merge on installed public EXE | **PASS** | [Run 42491529466](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491529466) |
| All four FULL-quality platform MP4 presets on the exact installed published EXE | **PASS** | [Run 42491917768](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491917768) |

The full native release check recorded **129 Python tests** along with the JavaScript suite. A separate published-binary long-form stress run imported **28,800,044 bytes** of synthetic WAV (15 minutes), verified full snapshot and recovery, and combined three two-second H.264/AAC chapters into an **180-frame, 6.023-second** MP4 while preserving all original chapter checksums. The separately downloaded published-EXE acceptance also passed. These tests certify the hosted Windows test environment and tested paths, **not every codec or PC, and not the owner's laptop**. The four export presets were checked with **one-second synthetic clips**, not hours of 1080p rendering.

## Backup and recovery

From the installed Windows app, open **Updates / Storage → Create + Verify Full Backup**. After verification, click **Open Backup Folder**; copy the **whole** `snapshot-...` folder to an external USB/different drive using Explorer. Keep `manifest.json`, `project-state.json` and `media/` together. Verify SHA-256 on the snapshot prior to restoration. A local same-disk backup alone will not protect against disk loss.

## Development and privacy

The `public-safe-windows-source.zip` stored in this public repo is a pinned audited baseline used **by CI only**; the user does not need to download it. Windows patch scripts apply sequentially (0.14.1 → 0.14.2 → 0.14.3 → 0.14.4) on disposable GitHub Windows runners. Any private manuscript, personal images, narration, backups, secrets and personal Google Drive links must **never** be added to this public repo.

- [0.14.4 source hardening and regression tests](.github/scripts/upgrade_windows_0144.py)
- [0.14.4 Windows installer and upgrade tests](.github/workflows/windows-installer-upgrade-0144.yml)
- [Exact verified EXE publisher](.github/workflows/publish-windows-0144-binary-branch.yml)
- [Independent installed-public-binary QA](.github/workflows/windows-published-release-acceptance-0144.yml)

Because GitHub Release asset creation previously returned HTTP 403 for the available integration, the exact verified unsigned setup.exe is directly available from a **binary-only Git branch**. The older 0.14.0 GitHub Release is retained. This does not imply an installer code signature.

Local editing and rendering require no cloud connection or subscription. Automatic Google Drive sync and model-based Burmese transcription are not included.
