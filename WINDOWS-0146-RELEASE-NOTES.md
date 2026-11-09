# MMMN Video Studio 0.14.6 — Conservative Major Scene Release

**Release date:** 2026-11-09 · **Windows 11 x64** · **Offline-first** · **Unsigned**

## What changed

The new **“🎬 အရေးကြီး Scene မှသာ ပုံပြောင်း (Auto Draft)”** button provides a calm, conservative background-image plan. It does not switch backgrounds for a single rain word, an ordinary dialogue turn or the mere appearance of a girl. It proposes an image change only when supported by clearer story evidence: arrival at a distinct setting, severe rain **together with** a dark oppressive atmosphere, a central revelation, or a major confrontation.

- **No slideshow timer:** No arbitrary maximum hold duration forces regular visual changes.
- **Visual continuity:** Existing image remains on screen when narration does not justify a major change.
- **Manual control:** Confirmed image choices, manual-timing locks and explicitly locked scenes are protected.
- **Render-safe:** A single picture may stay on screen for 90–120 minutes while the technical render timeline is segmented into scenes of no more than **3600 seconds each** (same picture across boundaries).
- **Local-only:** Uses the existing image library and image requirement IDs; no cloud upload or invented image files.
- **Narration timing:** Existing reviewed SRT is used when present; otherwise the native FFmpeg pause detector may suggest approximate boundaries. Scene durations remain consistent with the original recording timeline.
- **Review:** The draft is never automatically approved. Confirmation, preview, manual replace/lock and undo remain available.

## Important scope limitation

**This is explainable offline text-evidence planning, not complete Burmese semantic AI.** The app cannot guarantee that it understands every implicit plot event from a voice recording. The existing optional whisper.cpp transcription feature still requires a separately installed compatible offline model, accurate Myanmar speech recognition, and human proofreading. Without SRT, timings are only approximations/pause hints. Image generation and automatic Google Drive synchronization are **not** part of this release.

## Exact native installer

[**MMMN-Video-Studio-Setup-0.14.6.exe**](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0146/downloads/MMMN-Video-Studio-Setup-0.14.6.exe)

- **Size:** 64,837,468 bytes
- **SHA-256:** `b94b7e9a9f7e5dd373b38216dc2dcc7fa392bb56fd42b981f4f38c2d4a05814f`
- No developer tools, source ZIP, paid AI API or permanent internet connection required for normal local rendering.

## Verified QA

| Gate | Status | Evidence |
| --- | --- | --- |
| 21 major-scene tests: rain/character mentions, strong mood, location, locks, 90/120-minute unchanged-image bounds | **PASS** | [42555074044](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555074044) |
| Apply full source patch chain 0.14.1–0.14.6 and retained storage/render protections | **PASS** | [42555074115](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555074115) |
| Native Windows installer build, in-place upgrade, full regression suite and offline MP4 | **PASS** | [42555073944](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555073944) |
| Publish the exact tested Setup.exe (no post-QA rebuild) | **PASS** | [42555724317](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555724317) |
| Independently download/install public 0.14.6 Setup.exe, real Edge UI conservative scene module, data and full backup security | **PASS** | [42555752046](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555752046) |
| **Click actual Major-only Auto Draft button**: 4 narrative beats → 2 visual scenes, 320s preserved; save/reload durable in Edge | **PASS** | [42556697904](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42556697904) |

**Prior release continuity:** 0.14.5 passed full 90-minute/120-minute continuous Full HD H.264/AAC MP4 tests (162,000 / 216,000 frames), and a 60-distinct-image storyboard test. Windows 0.14.6 retains that renderer and its duration-dependent FFprobe verification, but the additional exact-0.14.6 **90-minute same-image** end-to-end render is tracked separately and must not be described as PASS until its run completes.

## Still not tested on owner's personal device

No installation or real-novel narration test has been performed on the owner's own Windows laptop. Windows SmartScreen can warn because the installer is **unsigned**. Long low-memory/thermal behavior, every codec variant, and real external-USB backup behavior are not guaranteed.

[Myanmar quick start](WINDOWS-QUICKSTART-MM.md) · [Release readiness](WINDOWS-RELEASE-READINESS.md) · [Requirements](specs/0146-major-scenes.md)
