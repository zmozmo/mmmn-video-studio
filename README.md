# MMMN Video Studio 0.14.6 — Windows Offline Installer

**Windows 11 x64 · Offline-first · Unsigned installer · Android paused**

[**MMMN-Video-Studio-Setup-0.14.6.exe**](downloads/MMMN-Video-Studio-Setup-0.14.6.exe)

- **Size:** 64,837,468 bytes
- **SHA-256:** `b94b7e9a9f7e5dd373b38216dc2dcc7fa392bb56fd42b981f4f38c2d4a05814f`
- [Original SHA256 manifest](downloads/MMMN-Video-Studio-Setup-0.14.6.exe.sha256)
- [Windows build evidence](downloads/RELEASE-EVIDENCE-VERIFIED.json)

## Verified independent Windows tests

| Test | Result |
| --- | --- |
| Native Windows 0.14.6 build/upgrade, local voice/photos and backup integrity | [**PASS**](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555073944) |
| Publish exact native-tested EXE bytes (no rebuild) | [**PASS**](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555724317) |
| Independent real Windows install of published EXE, Edge GUI, Local API security, Backup/Restore, uninstall | [**PASS**](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555752046) |
| Conservative scene model: 21 regressions, rain/girl does not switch image, severe dark storm does, manual locks | [**PASS**](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555074044) |
| Installed Edge UI actually imports and runs Smart Scene module | [**PASS**](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555752046) |

**New:** The **Major-only Auto Draft** button only proposes picture changes for major setting, atmosphere or story turning points. Ordinary rain or a character mention should keep the current image. It preserves manual locks. In long quiet narration, the same photo can continue across internal 3600-second renderer-safe segments, not forced slideshow cuts.

**Limitations:** This is a deterministic offline *reviewable suggestion* system, not guaranteed full Burmese semantic AI/audio understanding, and it does not create new photographs or automatically connect to Google Drive. Compatible offline ASR model and transcript proofreading may be needed for better word-level timing.

**Prior video-engine evidence:** Windows **0.14.5** actually encoded continuous 90 and 120-minute 1080p H.264/AAC videos with all frames and backups verified. [Run 42499519584](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42499519584). Windows 0.14.6 retains the same encoder. Its extra one-picture 90-minute end-to-end test is [tracked separately](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555826576).

The owner's physical laptop has not been tested. The executable is **not code-signed**; Windows SmartScreen may warn. All test media was synthetic; never upload unpublished manuscripts, original voice or other private content to public GitHub.

[မြန်မာလို စတင်အသုံးပြုနည်း](https://github.com/zmozmo/mmmn-video-studio/blob/main/WINDOWS-QUICKSTART-MM.md) · [0.14.6 Release Notes](https://github.com/zmozmo/mmmn-video-studio/blob/main/WINDOWS-0146-RELEASE-NOTES.md)
