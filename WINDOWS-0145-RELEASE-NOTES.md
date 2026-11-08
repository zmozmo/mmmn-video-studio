# MMMN Video Studio Windows 0.14.5 — Long-Novel Reliability Release

**Date:** 2026-11-08 · **Windows x64** · **Offline-first** · **Unsigned installer** · **Android paused**

## Why this release was necessary

The original 0.14.4 published EXE successfully imported 90- and 120-minute WAV files, generated the MP4 stream and reached the final verification stage. However, FFprobe decoding and counting **all** video frames exceeded the old hard-coded **180-second** process timeout, so the application safely rejected the output instead of publishing a possibly unverified file.

Evidence: [0.14.4 90/120-minute timeout run](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42497822087).

## Actual fix

The 0.14.5 patch replaces the fixed 180-second final full-frame verification timeout with a duration-proportional, bounded window. **It does not remove** FFprobe, frame counting, duration validation, codec validation, temporary-file safety, cancellation or source-file protection. All 0.14.4 atomic save/import protections remain.

[0.14.5 source fix and regression tests](.github/scripts/upgrade_windows_0145.py).

## Exact published Windows setup.exe

- [MMMN Video Studio 0.14.5 Setup.exe](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0145/downloads/MMMN-Video-Studio-Setup-0.14.5.exe)
- Exact file size: **64,844,005 bytes**
- SHA-256: `3afb835da0c14c7b3da761e07b479c15a3956ee97efb771b450467d2f529f274`
- No mandatory internet connection, paid AI API, Python, Node.js or VS Code for end users.

## Verified Windows acceptance

| Gate | Result | GitHub Windows evidence |
| --- | --- | --- |
| Native 0.14.5 build, A→B in-place upgrade, original data preserved, offline MP4 | PASS | [42498880529](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42498880529) |
| Publish exact already-tested unsigned installer bytes | PASS | [42499285203](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499285203) |
| Download published EXE, install/upgrade, real Edge UI, backup, API security, uninstall | PASS | [42499308041](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499308041) |
| **90-minute continuous 1920×1080 H.264/AAC MP4**, 30fps / **162,000 verified frames**, SHA-preserved backup/restore | PASS | [90m job in 42499519584](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584) |

The actual 90-minute MP4 contained **5,400.000 seconds**, and the GitHub-hosted Windows test recorded **641.9 seconds** for the export operation. This is not a speed benchmark for the owner's personal computer. All test source images, WAV and manuscript are synthetic.

The owner's complete novel narration is specified as **no longer than 90 minutes**. A two-hour export and a 60-distinct-image, 59-dissolve storyboard export are additional resilience checks, not prerequisites to changing the narration's actual stated duration. Their final 0.14.5 results must be confirmed separately.

## Limitations and first-device acceptance

The user's own Windows 11 laptop has not been accessed or tested. This unsigned executable may display SmartScreen unknown-publisher warnings. A full local backup does not protect against physical drive loss until a verified, complete snapshot is copied to another drive. The app does not automatically sync Google Drive or guarantee Burmese speech recognition without an offline model.

Older 0.14.4 setup.exe should **not** be used for a single 90-minute export because of its known 180-second verification timeout. Use the checksum-matched **0.14.5** release instead.

[မြန်မာလို စတင်အသုံးပြုနည်း](WINDOWS-QUICKSTART-MM.md) · [Release readiness and pending tests](WINDOWS-RELEASE-READINESS.md)
