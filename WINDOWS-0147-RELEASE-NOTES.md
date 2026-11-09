# MMMN Video Studio Windows 0.14.7 — Audio-First and Important-Pictures-Only

**Date:** 9 November 2026 · **Windows 11 x64** · **Offline-first** · **Unsigned setup**

## Exact released installer

[Download MMMN Video Studio Setup 0.14.7.exe](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0147/downloads/MMMN-Video-Studio-Setup-0.14.7.exe)

- File: `MMMN-Video-Studio-Setup-0.14.7.exe`
- Size: **64,839,519 bytes**
- SHA-256: `ca8b984722c6da971008a457c3d4b0dc734142edf0858d940f2c1bdb03c2f4cb`
- No developer environment (VS Code, Python, Node.js or a source ZIP) or paid AI API needed for normal operation.
- Unsigned, so Windows SmartScreen may show an unknown publisher warning.

## New in 0.14.7

### 1. Important-scene-only image creation brief

**“🖼 အရေးကြီး Scene ပုံလိုအပ်ချက်သာ ထုတ်ရန်”** exports a **local Markdown** checklist from the saved conservative major-scene timeline. It lists only the actual major visible image beats, with their narration timestamps and existing/missing local image assignments. Ordinary rain mentions, minor character introductions and internal 3,600-second same-picture renderer boundaries are **not** extra image requests.

This is a plan for the author's own images, not an automatic image generator. No files are sent to Google Drive or any remote server. The local checklist can contain private excerpts from the novel; do not publish it.

### 2. Optional narration-first major-scene draft

**“🎧 အသံဖတ်ပြချက်နဲ့ အရေးကြီး Scene (Offline Model ရှိမှ)”** keeps an existing reviewed SRT when present. Otherwise, if separately installed **whisper.cpp** and a multilingual ggml model are available, the app **asks for consent** before running local Burmese speech-to-text and checking SRT timestamp structure. If no model is available or the speech step fails, the app transparently falls back to FFmpeg offline narration-pause estimates or text-length estimates.

The user must still check Burmese transcription accuracy and the timing/picture choices. **No speech model or whisper.cpp CLI is bundled with the installer**, and real Burmese speech recognition accuracy has NOT been certified. This is an integration feature, not guaranteed end-to-end audio understanding.

### 3. 0.14.6 protections unchanged

Conservative major-scene image choices, manual image/time locks, chapter audio duration, original audio SHA, FFmpeg offline H.264/AAC MP4, verified local Backup/Restore, local API security, and in-place Windows upgrade remain in place.

## Verified tests

| Test | Result | Evidence |
| --- | --- | --- |
| 12 artwork brief tests + 21 conservative major scene tests | **PASS** | [42594598985](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42594598985) |
| Apply entire 0.14.1–0.14.7 patch chain; retained video/storage tests | **PASS** | [42594925798](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42594925798) |
| Build, install, in-place upgrade, original media/data safety, actual offline MP4 | **PASS** | [42595044624](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595044624) |
| Publish exact pretested unsigned EXE bytes | **PASS** | [42595856442](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595856442) |
| Independently download published EXE; real Edge UI, backup, restore, security and uninstall | **PASS** | [42595895083](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595895083) |
| Click important-photo button, download 2-beat local brief, preserve entire audio timeline and project | **PASS** | [42596100140](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42596100140) |
| Click Audio-first button, simulate LOCAL whisper recognition with 40 synthetic SRT cues, save/reload | **PASS (synthetic stub)** | [42596129789](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42596129789) |

The immediately preceding **0.14.6** exact installer also encoded a **90-minute one-unchanged-background 1920×1080 H.264/AAC MP4 with 162,000 counted frames**, preserving the original synthetic narration SHA. [Actual 0.14.6 90-minute QA PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555826576). The video engine is retained in 0.14.7. A separate 90-minute full encode **of the 0.14.7 binary** has not been performed, so do not conflate the prior release's stress result with this version.

## Remaining acceptance / limitations

- **User's own Windows 11 HP laptop has not been tested.** Hosted CI performance does not predict that machine's time, thermal behavior, or available disk.
- Real Myanmar ASR from a real narration using a real, installed local model **not validated**. SRT timestamps and semantics require human review.
- The application **does not automatically generate artwork or auto-fetch pictures from Google Drive**. Local images or generated assets must be supplied/imported.
- Any user recordings/manuscripts, backup snapshots and generated art should remain private; the public GitHub code and CI used only synthetic media.

[မြန်မာလို အသုံးပြုနည်း](WINDOWS-QUICKSTART-MM.md) · [Release readiness](WINDOWS-RELEASE-READINESS.md) · [0147 SDD](specs/0147-audio-major-artwork.md)
