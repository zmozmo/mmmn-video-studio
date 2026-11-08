# MMMN Video Studio — Windows (Offline-first)

**Latest Windows release candidate:** **0.14.0 RC1**, published **8 November 2026**.

### Download the actual Windows installer

**[MMMN-Video-Studio-Setup-0.14.0.exe — Direct download](https://github.com/zmozmo/mmmn-video-studio/releases/download/v0.14.0-rc.1/MMMN-Video-Studio-Setup-0.14.0.exe)**

File size: 64,823,394 bytes. SHA-256:

```text
d1b1908cd078d140713f923c33ccb5c2d4c8abe2f4042cfef982a3aaa21c462f
```

[Release page](https://github.com/zmozmo/mmmn-video-studio/releases/tag/v0.14.0-rc.1) • [Verified Windows CI #10](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42442410316) • [Independent published-release acceptance tests](https://github.com/zmozmo/mmmn-video-studio/actions/workflows/windows-published-release-acceptance.yml)

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

- The Windows GitHub-hosted runner **compiled the installer**, installed the base version, upgraded it in place, rendered H.264 + AAC video, opened the real Edge UI, checked project/media SHA-256 hashes and verified uninstall retained test data. [Full CI evidence](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42442410316).
- The setup EXE on the release page is the **same verified installer bytes**, not an untested rebuild.
- A separate, independent workflow checks the **published download** by installing it on another clean Windows runner and exercising actual editor interactions.
- This is an **unsigned release candidate**, not a code-signed production release or a guarantee that every laptop/codec/project will work. The user's Windows 11 device has not yet been tested.
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
