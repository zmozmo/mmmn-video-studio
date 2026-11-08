# MMMN Video Studio — Windows 0.14.5 Verified Release

**Windows 11 x64 · offline-first · unsigned installer · Android paused**

[**MMMN-Video-Studio-Setup-0.14.5.exe**](downloads/MMMN-Video-Studio-Setup-0.14.5.exe) — **64,844,005 bytes**

SHA-256: `3afb835da0c14c7b3da761e07b479c15a3956ee97efb771b450467d2f529f274`

[SHA256 checksum file](downloads/MMMN-Video-Studio-Setup-0.14.5.exe.sha256) · [Native release evidence](downloads/RELEASE-EVIDENCE-VERIFIED.json) · [Full Windows acceptance receipt](downloads/WINDOWS-0145-ACCEPTANCE-VERIFIED.txt)

## Verified exact released EXE — all gates PASS

| Gate | GitHub Windows verification |
| --- | --- |
| Build two installers, real install / in-place upgrade / offline MP4, preserved app data / uninstall | [42498880529 — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42498880529) |
| Publish exact pretested EXE bytes, unchanged | [42499285203 — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499285203) |
| Independent download, 0.14.0 → 0.14.5 install/upgrade, Edge UI, backup/restore, localhost API security | [42499308041 — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499308041) |
| One **90-minute 1920×1080 H.264/AAC 30fps MP4**, **162,000 verified frames**, intact narration/backup | [42499519584, 90m job — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584) |
| One **120-minute Full HD MP4**, **216,000 verified frames**, intact narration/backup | [42499519584, 120m job — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584) |
| 60 distinct generated images, 59 cross-dissolves, one **15-minute Full HD MP4**, 27,000 verified frames, 61-file backup | [42499523807 — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499523807) |

## Fixed in 0.14.5

The previous **0.14.4** installer had a fixed 180-second timeout in its final FFprobe frame-count verification. Actual 90/120-minute exports failed after the encoding phase despite reaching final checks. Windows 0.14.5 scales the allowed verification time with the duration while **still checking every decoded video frame** and preserving all 0.14.4 atomic-save and media-import security protections.

All media in the above tests was synthesized on disposable GitHub-hosted Windows machines. Original unpublished manuscripts, real narration, photographs and private user data were **never included**.

**Limitations:** The owner's own Windows 11 laptop has not been tested. Hardware performance will differ. The installer is **unsigned** and Windows SmartScreen may warn. Backup copies are local until separately transferred and verified on another physical drive. No mandatory paid service or cloud video API.

[Main source and Burmese installation guide](https://github.com/zmozmo/mmmn-video-studio/blob/main/WINDOWS-QUICKSTART-MM.md)
