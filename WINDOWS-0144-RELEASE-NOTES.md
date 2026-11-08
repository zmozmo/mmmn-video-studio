# MMMN Video Studio Windows 0.14.4 — Verified atomic-storage release

**Release date:** 2026-11-08 · **Platform:** Windows x64, unsigned · **Android:** paused

## Improved project and media safety

- Every manuscript/project save now uses a **unique exclusive temporary file** rather than a predictable `project-state.pending.json` name. If the final replace fails, the temporary file is removed and the original project remains intact.
- Detect and refuse symlinked project metadata, previous and older recovery copies before writing, preventing unrelated files from being overwritten by recovery copy operations.
- Reject symlinked import metadata during chunk upload and finalization; reject a symlinked partial media file before checksum and finalization.
- Finalized media uses a Windows destination-collision-refusing rename instead of `os.replace` so a newly appeared existing media file cannot be silently overwritten.
- Windows UI displays the correct release version and "Windows Offline Installer" instead of old "Trial" labels. The backup instructions explain how to use the built-in Open Backup Folder button and copy the entire verified snapshot to an external drive, **without any ZIP/CMD requirement**.

**9 new atomic-storage/UI regression tests**. All 0.14.3 media capacity guards, 0.14.2 disk-free indicators, 0.14.1 manuscript scene/timing preservation and the built-in offline FFmpeg renderer remain intact.

## Full release evidence

1. [Native Windows Build → Install → Upgrade → MP4 Render → Uninstall PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42478959788). 129 Python tests; existing JavaScript suite, FFmpeg H.264/AAC export, real Edge UI and project/media SHA-256/uninstall preservation.
2. [Publish exact tested setup.exe bytes PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479446166). No rebuild after native validation.
3. [Independent downloaded-executable Windows QA PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479467429). Separate runner downloads the public EXE, verifies SHA-256, installs previous real 0.14.0, creates synthetic project/WAV/image/backup, upgrades 0.14.4, checks unchanged legacy hashes, tests real Edge UI, save/reload, full backup and restore, corrupt-backup refusal, missing/forged local API token rejection, offline core flow and uninstall.

**Published installer:** `MMMN-Video-Studio-Setup-0.14.4.exe`  
**Size:** 64,855,430 bytes  
**SHA-256:** `db57d26241c19c9a2629f959245fa0ecb74c86d5a9bbfe04df8031cfe5da6830`

[Direct public verified executable](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0144/downloads/MMMN-Video-Studio-Setup-0.14.4.exe) · [Independent QA receipt](https://github.com/zmozmo/mmmn-video-studio/blob/windows-binaries-0144/downloads/WINDOWS-0144-ACCEPTANCE-VERIFIED.txt)

## Additional published-installer long-form QA

[Independent long-form WAV and three-chapter merge — PASS, Run 42491529466](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491529466). The already published 0.14.4 EXE was downloaded unchanged and installed on a disposable Windows runner. A synthetic **15-minute WAV (28,800,044 bytes)** was imported in SHA-256-verified chunks; a full backup was verified and restored with original bytes and manuscript intact; three two-second H.264/AAC chapters were encoded with packaged FFmpeg and combined into one **6.023-second, 180-frame** full-book MP4 without altering the originals. This establishes the tested streaming and merge path, not hours-long MP4 encoding on the owner's laptop.

## All platform presets: independent full-quality export QA

[Published Windows EXE four-format export — PASS, Run 42491917768](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491917768). With a synthetic 1-second WAV and PNG, the exact installed 0.14.4 EXE rendered and FFprobe-validated **YouTube 1920×1080**, **TikTok/Shorts 1080×1920**, **Facebook 1080×1350**, and **Square 1080×1080**. Every file was H.264 video / AAC audio at **30 fps (30 frames)**. The same run independently repeated the 15-minute WAV import/backup/restore and three-chapter MP4 merge. These tests validate all four output paths at full resolution, not hours of 1080p encoding.

## Limitations

Windows native and published-binary acceptance tests passed on GitHub-hosted disposable Windows machines only. The user's own laptop was not tested or touched. Installer is unsigned and may raise SmartScreen warning. The app requires no paid AI API, subscription or online server to edit and render locally; there is no automatic Google Drive sync, external-drive backup copy, or mandatory Burmese transcription model. The user should separately copy a verified full backup to an external drive. No private real manuscripts, voice recordings or images were published.
