# MMMN Video Studio — Windows Offline-first

**Latest verified Windows version: 0.14.2 (unsigned)** · 8 November 2026  
**Android development: paused**

## Windows setup.exe — direct download, no ZIP

**[Download MMMN Video Studio 0.14.2 for Windows x64](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0142/downloads/MMMN-Video-Studio-Setup-0.14.2.exe)**

- Size: **64,819,122 bytes** (~64.8 MB)
- SHA-256: `80da4ce34f88aea685d33989b16c4749a58a2e5b50178280a93bcfcfab217692`
- [Public downloadable installer, checksum and independent QA record](https://github.com/zmozmo/mmmn-video-studio/tree/windows-binaries-0142/downloads)

**This is not a source ZIP.** No VS Code, Python setup, Node.js installation, command-line build, or external video API subscription is required to install and use its core offline editor and FFmpeg renderer.

**Unsigned:** Windows SmartScreen may report an unknown publisher. Obtain only the original linked binary; a byte-for-byte SHA-256 check can verify the download. The user's actual Windows 11 laptop has **not** been tested, although the independent hosted Windows tests passed.

## What's new

**0.14.2** — Media imports now check the recording/image/video size against the actual drive's free space and keep at least 128 MiB extra capacity. Low-space imports are rejected before creating a partial file, existing media IDs and symlink destinations cannot be overwritten, and free disk space is shown in the app. Five new regression tests cover these situations. [Full notes](WINDOWS-0142-RELEASE-NOTES.md).

**0.14.1** — Saving corrected Myanmar manuscript text no longer deletes existing storyboard scenes, image choices, timing and manual locks. The app also has one-click Windows Explorer buttons to open its Project, Full Backups, and MP4 Exports folders. [Previous update](WINDOWS-0141-RELEASE-NOTES.md).

## Real Windows verification

- **[Native Windows 0.14.2 Build — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42471534266):** source audits and 143 JavaScript / 115 Python tests, real installer Build A/B, native install, in-place upgrade, bundled FFmpeg H.264/AAC video, real Edge editor, original project/media hash comparison, and uninstall data preservation.
- **[Independent downloaded 0.14.2 EXE Acceptance — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42472031214):** separately download the actual published executable; install earlier 0.14.0; create WAV, scene image, manuscript and full backup; install 0.14.2 without uninstalling; confirm seven original SHA-256 hashes and pre-upgrade metadata. Test actual Edge browser edits and scene retention, free-space display, WAV import, completed and verified full backup, actual restore, Explorer folder allowlisting, and no external network requests during the tested core flow.
- **[Independent 0.14.2 QA receipt](https://github.com/zmozmo/mmmn-video-studio/blob/windows-binaries-0142/downloads/WINDOWS-0142-ACCEPTANCE-VERIFIED.txt)** documents the exact tested executable hash and evidence.

Installer bytes were **not rebuilt after validation**. No personal user manuscripts, unpublished photographs or recordings were published. All public QA uses synthetic example content.

## How the app works

1. Install the Windows x64 application in your normal Windows user account; upgrading over 0.14.0 or 0.14.1 should not require uninstalling first. Make an external-drive backup before important upgrades.
2. Open MMMN Video Studio; it runs a local UI bound to **127.0.0.1** in your browser.
3. Import your own Burmese chapter/manuscript and self-recorded WAV/MP3 narration. Add scene artwork and align the visual timeline to audio.
4. Export H.264/AAC MP4, using 16:9 YouTube, 9:16 Shorts/TikTok/Reels, 4:5 Facebook, or square presets.
5. Create and SHA-256 verify a full local backup, then **copy that backup to a different drive** for disaster recovery.

**Scope limitations:** There is no automatic Google Drive sync and no mandatory preinstalled Myanmar transcription model. The app requires no online API for normal local editing and encoding. Offline editing tests do not certify every media codec, very large audiobook, or an individual device. It remains an unsigned installer; Android is not currently being developed.

## Repository structure and security

The versioned `public-safe-windows-source.zip` archive is kept for reproducible CI, **not** as a required user download. Keep personal scripts, voice recordings, original images, backups, account tokens and Google Drive URLs out of this public GitHub repository.

- [0.14.2 Windows build](.github/workflows/windows-installer-upgrade-0142.yml)
- [0.14.2 direct binary publish](.github/workflows/publish-windows-0142-binary-branch.yml)
- [0.14.2 independently downloaded Windows acceptance](.github/workflows/windows-published-release-acceptance-0142.yml)

The older **0.14.0 stable release** is retained at [GitHub Releases](https://github.com/zmozmo/mmmn-video-studio/releases/tag/v0.14.0). The more recent 0.14.2 direct executable is stored in a public-safe binary-only Git branch because GitHub Release creation returned HTTP 403 for the available integration.
