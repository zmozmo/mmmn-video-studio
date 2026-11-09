# MMMN Video Studio — Windows Offline-first

**Latest Windows release: 0.14.7 (unsigned; audio-first optional SRT + minimal image brief, hosted Windows QA PASS)** · 9 November 2026  
**Android: paused** · **Personal laptop: deliberately not tested**

## One-click Windows x64 Installer (direct EXE, no ZIP)

**[MMMN Video Studio 0.14.7 Windows setup.exe](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0147/downloads/MMMN-Video-Studio-Setup-0.14.7.exe)**

- Filename: `MMMN-Video-Studio-Setup-0.14.7.exe`
- Size: **64,839,519 bytes**
- SHA-256: `ca8b984722c6da971008a457c3d4b0dc734142edf0858d940f2c1bdb03c2f4cb`
- [Published direct executable and independent acceptance record](https://github.com/zmozmo/mmmn-video-studio/tree/windows-binaries-0147/downloads)

There is no requirement for VS Code, CMD, Python/Node.js installation, source ZIP or a paid video API to use the installed application. **Unsigned**: Windows SmartScreen may display an unknown-publisher warning; check the exact checksum. The user's actual Windows 11 laptop has not been tested yet.

## Features

- Local-first Burmese manuscript editor with scene-by-scene storyboard, image choices, manual scene locking and timing. Editing a manuscript **preserves** scene choices, manual locks and existing timing.
- Import your own WAV/MP3 audio narration, images and videos. Imports check available disk space at the beginning and **before each chunk**, reserve space for parallel imports, and reject unsafe symlink/media collisions.
- Render H.264/AAC MP4 using bundled FFmpeg, without external API/subscription: YouTube 16:9, TikTok/Shorts/Reels 9:16, Facebook 4:5 and square presets.
- Create **verified full-media local backups**, verify via SHA-256, restore after an accidental edit, open Project/Backup/MP4 folders directly in Windows Explorer and keep existing user files across in-place installer upgrades/uninstalls.
- New in **0.14.4**: unique exclusive project-save staging files with failure cleanup, project-recovery symlink protection, and collision-safe media finalization. Old trial labels and obsolete ZIP/CMD backup instructions corrected. Nine new regression tests.
- New in **0.14.5**: repair the hard-coded 180-second FFprobe full-frame verification timeout that prevented 90/120-minute video exports in 0.14.4. Frame-by-frame inspection stays enabled with a bounded duration-scaled check. The exact released 0.14.5 EXE produced a continuous **90-minute 1920×1080 H.264/AAC MP4 (162,000 frames)**; full local backup/restore and output SHA protection also passed on a disposable Windows runner.
- New in **0.14.7**: **🖼 Important-scenes-only artwork brief** exports a private local Markdown checklist of only significant scene pictures, excluding technical same-image encoder segments. **🎧 Audio-first Smart Draft** can optionally call a separately installed local whisper.cpp multilingual model to generate unapproved Myanmar SRT before major-scene planning; if unavailable, clearly falls back to pause/text-length estimates. The **installer does not bundle an ASR model or generate artwork**.
- New in **0.14.6**: **🎬 Major-only Auto Draft** suggests background changes only for major visual transitions, NOT each rain word, minor character entrance or dialogue. Keeps pictures stable, honors manual locks, uses existing SRT or approximate offline pause timing, and divides 90/120-minute visually unchanged passages into <=3600-second *technical* segments with the same photo. **Not a full Burmese semantic AI or automatic image generator.**

[မြန်မာလို Windows စတင်အသုံးပြုနည်း](WINDOWS-QUICKSTART-MM.md) · [0.14.7 release notes](WINDOWS-0147-RELEASE-NOTES.md) · [0.14.6 notes](WINDOWS-0146-RELEASE-NOTES.md) · [0.14.5 notes](WINDOWS-0145-RELEASE-NOTES.md) · [Release readiness](WINDOWS-RELEASE-READINESS.md) · [0.14.3 notes](WINDOWS-0143-RELEASE-NOTES.md)

## Exact native and independently downloaded Windows acceptance

| Gate | Outcome | Evidence |
| --- | --- | --- |
| **0.14.7 12 minimal-artwork + 21 major-scene tests** | **PASS** | [42594598985](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42594598985) |
| 0.14.7 Windows installer native Build, in-place upgrade, offline MP4 and data safety | **PASS** | [42595044624](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595044624) |
| 0.14.7 exact verified installer publication | **PASS** | [42595856442](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595856442) |
| 0.14.7 independently downloaded EXE, real Edge modules, storage, security, backup/restore and uninstall | **PASS** | [42595895083](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595895083) |
| **0.14.7 actual important-artwork Markdown export button** (only 2 of 4 narrative beats) | **PASS** | [42596100140](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42596100140) |
| 0.14.7 optional Audio-first native UI flow with **mock synthetic SRT** (real Burmese ASR NOT proven) | **PASS (mock)** | [42596129789](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42596129789) |
| **0.14.6 21 conservative Major Scene tests, manual-locks and 90/120m same-image bounds** | **PASS** | [42555074044](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555074044) |
| 0.14.6 complete patch chain, native Windows build/install/in-place upgrade and offline MP4 | **PASS** | [42555073944](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555073944) |
| Exact tested Windows 0.14.6 EXE publication | **PASS** | [42555724317](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555724317) |
| 0.14.6 published EXE independent Edge UI, real major-scene module, save, backup/security/uninstall | **PASS** | [42555752046](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555752046) |
| 0.14.6 actual Smart Scene UI button click, confirm, 4 narrative beats→2 major backgrounds, preserve 320s and save/reload | **PASS** | [42556697904](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42556697904) |
| **Exact released Windows 0.14.6 90-minute 1080p MP4**, one unchanged photo, 162,000 counted frames and original WAV SHA intact | **PASS** | [42555826576](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555826576) |
| Latest Windows 0.14.5 build, install, in-place upgrade, media and recovery | **PASS** | [Run 42498880529](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42498880529) |
| 0.14.5 exact byte-for-byte setup.exe publication | **PASS** | [Run 42499285203](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499285203) |
| 0.14.5 independent public-EXE install, UI, backup, security and uninstall | **PASS** | [Run 42499308041](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499308041) |
| **0.14.5 continuous 90-minute full-HD MP4, 162,000 frames, verified WAV and backup** | **PASS** | [90-minute job, Run 42499519584](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584) |
| **0.14.5 continuous 120-minute full-HD MP4, 216,000 frames, verified WAV and backup** | **PASS** | [120-minute job, Run 42499519584](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584) |
| 0.14.5: 60 different images, 59 dissolves, 15-minute 1080p MP4 and complete media snapshot | **PASS** | [Run 42499523807](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499523807) |
| Native Windows 0.14.4 Build A/B, install and in-place upgrade | **PASS** | [Run 42478959788](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42478959788) |
| Bundled offline FFmpeg MP4, real Edge UI and preserved project/media checksums | **PASS** | [Same native run](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42478959788) |
| Published the exact tested EXE, no binary rebuild | **PASS** | [Run 42479446166](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479446166) |
| Independent runner downloads public EXE, upgrades real 0.14.0, UI/backup/security/uninstall tests | **PASS** | [Run 42479467429](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479467429) |
| Additional 15-minute WAV streaming, full backup/restore and 3-chapter MP4 merge on installed public EXE | **PASS** | [Run 42491529466](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491529466) |
| All four FULL-quality platform MP4 presets on the exact installed published EXE | **PASS** | [Run 42491917768](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491917768) |
| Extended original EXE: 45-second 1080p ×2, cross-dissolve, cancel/retry, synthetic external-folder backup copy and recovery | **PASS** | [Run 42492649641](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42492649641) |
| Continuous 5-minute H.264/AAC 1080p MP4, 6 scenes and 9,000 checked frames | **PASS** | [Run 42493062578](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42493062578) |
| Continuous 15-minute H.264/AAC 1080p MP4, 6 scenes and 27,000 checked frames | **PASS** | [Run 42493702496](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42493702496) |

The older 0.14.4 native suite recorded **129 Python tests** plus JavaScript tests. Windows 0.14.5 adds seven length-aware full-frame verification regressions and retains atomic save/import regression coverage. The new published EXE passed **90-minute and 120-minute** real encoded H.264/AAC MP4 checks with 162,000 and 216,000 frames, plus 60 distinct storyboard pictures/59 fades. The original 0.14.4 publication remains available for history but has a known full-novel timeout bug.

The full native release check recorded **129 Python tests** along with the JavaScript suite. A separate published-binary long-form stress run imported **28,800,044 bytes** of synthetic WAV (15 minutes), verified full snapshot and recovery, and combined three two-second H.264/AAC chapters into an **180-frame, 6.023-second** MP4 while preserving all original chapter checksums. The separately downloaded published-EXE acceptance also passed. These tests certify the hosted Windows test environment and tested paths, **not every codec or PC, and not the owner's laptop**. The four export presets were checked with **one-second synthetic clips**, not hours of 1080p rendering.

## Backup and recovery

From the installed Windows app, open **Updates / Storage → Create + Verify Full Backup**. After verification, click **Open Backup Folder**; copy the **whole** `snapshot-...` folder to an external USB/different drive using Explorer. Keep `manifest.json`, `project-state.json` and `media/` together. Verify SHA-256 on the snapshot prior to restoration. A local same-disk backup alone will not protect against disk loss.

## Development and privacy

The `public-safe-windows-source.zip` stored in this public repo is a pinned audited baseline used **by CI only**; the user does not need to download it. Windows patch scripts apply sequentially (0.14.1 → 0.14.2 → 0.14.3 → 0.14.4 → 0.14.5 → 0.14.6 → 0.14.7) on disposable GitHub Windows runners. Any private manuscript, personal images, narration, backups, secrets and personal Google Drive links must **never** be added to this public repo.

- [0.14.6 conservative scene planner](web/major-scene.mjs) · [requirements](specs/0146-major-scenes.md) · [Windows UI patch](.github/scripts/upgrade_windows_0146.py)
- [0.14.5 long-video verification fix](.github/scripts/upgrade_windows_0145.py)
- [0.14.5 Windows installer and upgrade QA](.github/workflows/windows-installer-upgrade-0145.yml)
- [0.14.5 published-EXE 90/120-minute QA](.github/workflows/windows-novel-length-acceptance-0145.yml)
- [0.14.4 source hardening and regression tests](.github/scripts/upgrade_windows_0144.py)
- [0.14.4 Windows installer and upgrade tests](.github/workflows/windows-installer-upgrade-0144.yml)
- [Exact verified EXE publisher](.github/workflows/publish-windows-0144-binary-branch.yml)
- [Independent installed-public-binary QA](.github/workflows/windows-published-release-acceptance-0144.yml)

Because GitHub Release asset creation previously returned HTTP 403 for the available integration, the exact verified unsigned setup.exe is directly available from a **binary-only Git branch**. The older 0.14.0 GitHub Release is retained. This does not imply an installer code signature.

Local editing and rendering require no cloud connection or subscription. Automatic Google Drive sync and built-in model distribution are not included. Optional LOCAL Burmese speech-to-text integration exists only when a compatible user-supplied whisper.cpp CLI and multilingual model are installed; real Burmese ASR accuracy is unverified.
