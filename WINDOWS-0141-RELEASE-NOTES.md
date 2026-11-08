# MMMN Video Studio — Windows 0.14.1 Update

**Windows-only. Android development remains paused.** This file documents the updated public-safe source and reviewed Windows upgrade procedure; it does not contain private novels, audio recordings, or user media.

## Improvements

- **Preserve storyboard on chapter-text edits.** Correcting a typo in the local Myanmar manuscript no longer silently discards existing scene durations, image choices, split/merge work, and manual locks. The editor marks alignment for re-review, because new text can make old timings stale.
- **One-click Windows Explorer access.** Open the actual Backup, Project Data, and exported MP4 folders from inside the installed app. No source ZIP, command prompt, VS Code, or Explorer path copy/paste is required.
- **Safer offline recovery workflow.** The app continues creating SHA-256-verified full-media backups and can restore them; users can open the snapshots folder and copy a complete backup to an external drive. Merely storing it on the same disk does NOT protect against disk failure.
- **Real release-to-release upgrade gate.** The independent Windows acceptance run must install the published 0.14.0 EXE, create a synthetic novel, WAV, image and backup via its actual localhost API, then upgrade to 0.14.1. It rejects any change in SHA-256 of the original project and media, requires previous backup verification, and checks pre-upgrade metadata checkpoint.
- **Installed-app GUI acceptance.** Real Edge browser tests verify editor startup, text persistence and scene-retention, WAV import, completed full backup, SHA-256 backup verification, GUI restore with original audio bytes, only whitelisted folder-opening actions, and no external requests.
- **Version consistency.** The source release metadata and Windows NSIS setup version are updated together.

## Compatibility

Run the newer setup.exe as the same Windows user who installed 0.14.0, with MMMN Video Studio closed. The install directory may be overwritten in place; saved user projects, imported recordings, exports, and snapshots live in a separate per-user directory and must be preserved. Make an independent external backup before an important upgrade.

The studio remains CPU-based and uses FFmpeg to render H.264/AAC MP4. No subscription or cloud API key is required for its local editor/export. Automatic Google Drive synchronization, prepackaged Myanmar speech-recognition models, Android APK and code signing are **not** included in this Windows maintenance update.

The release is **unsigned**: Windows SmartScreen may warn about an unknown publisher. Use only the direct installer in the verified [GitHub Releases](https://github.com/zmozmo/mmmn-video-studio/releases) page. Windows hosted-runner tests do not substitute for the user's own laptop acceptance.
