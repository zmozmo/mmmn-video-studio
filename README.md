# MMMN Video Studio — Offline-first Windows Video Studio

**Latest verified Windows version: 0.14.3 (unsigned)** · 8 November 2026
**Android development: paused** · **User laptop: not tested**

## Direct Windows setup.exe — no ZIP, development tools or subscription needed

[MMMN Video Studio 0.14.3 Windows x64 Installer](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0143/downloads/MMMN-Video-Studio-Setup-0.14.3.exe)

- Filename: `MMMN-Video-Studio-Setup-0.14.3.exe`
- Size: **64,840,856 bytes**
- SHA-256: `4c4de4daad56d292e7b697a004f74ffb374ddb7a79916c317f0d2e250d30c3ed`
- [Published binary-only branch and QA receipt](https://github.com/zmozmo/mmmn-video-studio/tree/windows-binaries-0143/downloads)

This executable is **unsigned** and may show Windows SmartScreen's "unknown publisher" prompt. No one needs VS Code, CMD, Python, Node.js or a ZIP extraction to install this version. The owner's personal laptop is deliberately **not tested yet**.

## What's new in 0.14.3

- Multiple simultaneous media imports reserve their **remaining declared bytes**. The server rejects a second oversized upload **before** the partial file is created, rather than overcommitting the same disk capacity.
- Every imported media chunk checks current free space against the import's disk reserve before writing, so disk pressure from another app cannot silently exhaust the recording drive.
- Pending-import metadata and partial symlinks are refused; correct WAV bytes and SHA-256 are preserved.
- Five new storage regression tests. Existing Windows 0.14.2 and 0.14.1 enhancements remain: free-disk display, manuscript edits preserving all scene choices/timing/locks, one-click Explorer folders for backups, projects and MP4 exports.

[Full 0.14.3 release notes](WINDOWS-0143-RELEASE-NOTES.md) · [0.14.2 release notes](WINDOWS-0142-RELEASE-NOTES.md)

## Exact release evidence

- **[Real Windows Build, Install, Upgrade, MP4 Render and Uninstall — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42475358558)**. Includes 143 JavaScript and 120 Python tests; two NSIS builds; actual installed Windows executables; in-place upgrade without uninstall; real FFmpeg H.264/AAC MP4; Edge UI; byte-exact project/media hash preservation and uninstall preservation.
- **[Publish the EXACT tested setup.exe bytes — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42475837823)**. Published executable matches the successful native Windows evidence, not a subsequent unverified rebuild.
- **[Independent published-binary Windows QA — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42475858282)**. A separate runner downloaded the public installer, verified its SHA-256, installed real 0.14.0, created synthetic manuscript/media/full-backup data, upgraded to 0.14.3, verified original hashes, exercised real Edge UI, WAV import, save/reload, SHA-256 full backup and restore, tampered-backup detection, missing/forged API token rejection, offline core flow, folder allowlisting and uninstall.

**These results prove the tested release flow on GitHub-hosted Windows runners, not every media format, hardware configuration, or the owner's own Windows 11 device.** The app remains unsigned. Never install a binary whose checksum differs from the value above.

## How it works

1. Install the x64 Windows app. Upgrades from verified older releases are designed to preserve data; keep a full backup on a separate drive first.
2. Open the local UI in the default browser. It is bound to `127.0.0.1` and uses a protected localhost API.
3. Import a Burmese manuscript, your own WAV/MP3 narration, and images/video for each scene. Adjust scene durations and storyboard layout manually.
4. Render bundled offline FFmpeg H.264/AAC MP4 for YouTube (16:9), Shorts/TikTok/Reels (9:16), Facebook (4:5), or square videos.
5. Create a full-media backup, verify its SHA-256, and **copy the entire snapshot directory to a different drive** for disaster recovery.

The app does not require an external video AI API, cloud subscription or internet access for core offline editing and rendering. Optional Google Drive auto-sync is **not included**. No mandatory preinstalled Myanmar speech recognition model is provided. Rendering large video projects still depends on device CPU, RAM and available disk space.

## Repository and privacy

The reproducible `public-safe-windows-source.zip` is a pinned, privacy-audited source baseline for GitHub CI—not a user download. CI applies verified Windows 0.14.1, 0.14.2 and 0.14.3 incremental source patches **in sequence** before compiling. Keep personal manuscripts, narration, artwork, backups, tokens, Google Drive links and identity data **out of this public repo**.

- [Windows 0.14.3 patch and five regression tests](.github/scripts/upgrade_windows_0143.py)
- [Windows 0.14.3 native build and upgrade workflow](.github/workflows/windows-installer-upgrade-0143.yml)
- [Publish only if Windows build PASS](.github/workflows/publish-windows-0143-binary-branch.yml)
- [Independent published-executable QA workflow](.github/workflows/windows-published-release-acceptance-0143.yml)

GitHub Release creation was previously blocked by HTTP 403 in the available integration. The verified newer installer is published as a **direct EXE in the binary-only Git branch**; the separate older `v0.14.0` GitHub Release remains available. The direct EXE is not a signed GitHub Releases asset.
