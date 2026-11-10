# MMMN Video Studio Windows 0.15.0 — exact verified unsigned installer

- File: `downloads/MMMN-Video-Studio-Setup-0.15.0.exe`
- Size: **64,836,579 bytes**
- SHA-256: `ce60a9c9e8f40caf68c5d2d0573e966e875bc75a7099e15c10dd3525508b66b3`
- [Native Windows build, install, upgrade, MP4 and preservation QA — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42749464288)
- [Exact-binary publication without rebuilding — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42750121344)
- [Independent public EXE download, Edge UI, original media, backup and uninstall QA — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42750156953)

This release adds a stricter **offline Burmese narration/SRT agreement guard** (chronology, timestamp order and per-cue evidence) and explicit consent before using model-generated timing for an editable draft. It preserves manual locks and original files, but **does not include a Burmese ASR model or automatic image generation**. Real Burmese ASR word-level accuracy over long novels has not been proven.

Windows installer is **unsigned**. SmartScreen may warn. Only disposable hosted Windows QA machines were tested, not the owner's real laptop. No private narration, manuscript or photos are included in this public binary branch.

See the [full 0.15.0 release notes](https://github.com/zmozmo/mmmn-video-studio/blob/main/WINDOWS-0150-RELEASE-NOTES.md) for limitations.
