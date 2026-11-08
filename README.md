# MMMN Video Studio — Windows (Offline-first)

**Latest Windows update:** **0.14.1 (verified unsigned installer)**, published **8 November 2026**, independently tested against the prior 0.14.0 installation.

### Download the actual Windows installer

**[MMMN-Video-Studio-Setup-0.14.1.exe — Direct download](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0141/downloads/MMMN-Video-Studio-Setup-0.14.1.exe)**

File size: 64,821,111 bytes. SHA-256:

```text
d9966b888f7e46fb0bdbcf16626e32e2de99f1cc134521b3e2300b59b04fd861
```

[Verified 0.14.1 installer download branch](https://github.com/zmozmo/mmmn-video-studio/tree/windows-binaries-0141/downloads) • [Native Windows Install/Upgrade/Render/Uninstall PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42448702717) • [Independent real 0.14.0→0.14.1 upgrade / GUI / WAV / backup / restore PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42449367102)

**What's new in 0.14.1:** Fixes the manuscript-save bug that could erase storyboard scenes, timing, manual locks and chosen artwork. Adds one-click Windows Explorer buttons to open the user's Backup, Project and MP4 Export folders. [Read the Windows 0.14.1 release notes](WINDOWS-0141-RELEASE-NOTES.md).

**GitHub release API note:** The verified 0.14.1 EXE is currently published as a **direct downloadable file** in a public-safe Git branch, not as a GitHub Release asset, because the latter returned a GitHub integration 403. It does not require downloading or extracting a ZIP. The previous 0.14.0 GitHub Release remains available at [v0.14.0](https://github.com/zmozmo/mmmn-video-studio/releases/tag/v0.14.0).

You **do not need to extract a ZIP, use VS Code, or run build scripts**. Download the EXE, close any old copy of the studio, and run the installer for the same Windows user account. For upgrades, run the newer installer without first uninstalling the previous version. For important projects, make a separate copy of your saved media and backups before upgrading.

The installer is **unsigned**. Windows SmartScreen may warn about an unknown publisher. Only use the release asset linked above and verify its SHA-256 if authenticity is in doubt.

### Intended workflow

1. Open the installed Windows app. It launches a local browser UI on **127.0.0.1**.
2. Import your own Myanmar novel/manuscript (TXT) or edit a local chapter copy; provide your self-recorded narration (WAV/MP3 or a video with audio).
3. Import scene photos, review the storyboard and align picture changes to narration timing.
4. Export H.264/AAC MP4 using YouTube 16:9, TikTok/Shorts/Reels 9:16, Facebook 4:5, or square presets.
5. Save a **native full backup** and copy it to an external drive for independent protection. The app does not upload user content to an online service.

**Important:** The public installer contains **synthetic demonstration chapters only**, not any private MMMN manuscript, personal character images, Drive IDs or recordings. Import your own materials locally. The app does not automatically gain ChatGPT's Google Drive permissions or synchronize files from Google Drive.

### Verification and limitations

- The Windows GitHub-hosted runner **compiled the 0.14.1 installer**, installed a base version, upgraded it in place, rendered H.264 + AAC video, opened the real Edge UI, checked project/media SHA-256 hashes and verified uninstall retained test data. [Full CI evidence](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42448702717).
- The setup EXE on the release page is the **same verified installer bytes**, not an untested rebuild.
- A separate, independent workflow **PASSED** after downloading the public 0.14.1 installer directly, installing the actual 0.14.0 first, upgrading to 0.14.1, verifying that seven project/media/backup file hashes remain unchanged, opening the real Edge editor, saving/reloading chapter edits without deleting the existing storyboard, importing WAV narration, completing a full backup and SHA-256 verification, actually restoring it, testing local folder access and proving no outbound requests. [Independent acceptance PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42449367102).
- This is an **unsigned Windows release**, not a code-signed release or a guarantee that every laptop/codec/project will work. The user's Windows 11 device has not yet been tested.
- Rendering is CPU-based and longer, high-resolution videos may take time, RAM and disk space.
- Burmese automatic speech transcription requires separately installed **offline speech models** and is not an always-ready built-in feature. Your own narration audio import/export is independent of speech transcription.
- Android development is on hold.

### Public repository and safety

This public repository is **public-safe only**. The `public-safe-windows-source.zip` archive contains synthetic demonstration data and exists for reproducible Windows CI builds; it is **not** necessary for end users. Do not commit original Myanmar manuscripts, private project backups, recordings, unpublished images, personal Drive URLs, passwords or tokens.

The Windows app uses a local HTTP UI and local filesystem data; no subscription/API key is required for normal editing or rendering. The provided installer includes FFmpeg needed by the tested local encoder. If you want a fully independent disaster-recovery copy, copy your backups to an external drive.

### Developer links

- [Windows installer upgrade laboratory](.github/workflows/windows-installer-upgrade-lab.yml)
- [Verified direct release publishing](.github/workflows/publish-verified-windows-setup.yml)
- [Independent published release acceptance](.github/workflows/windows-published-release-acceptance.yml)
- [Promotion to stable only after published-download QA](.github/workflows/promote-published-windows-stable.yml)
