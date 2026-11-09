# MMMN Video Studio — Windows 0.14.7 Offline Release

**Windows 11 x64 · Unsigned setup.exe · Android paused**

[**MMMN-Video-Studio-Setup-0.14.7.exe**](downloads/MMMN-Video-Studio-Setup-0.14.7.exe) — **64,839,519 bytes**

- SHA-256: `ca8b984722c6da971008a457c3d4b0dc734142edf0858d940f2c1bdb03c2f4cb`
- [Checksum file](downloads/MMMN-Video-Studio-Setup-0.14.7.exe.sha256)
- [Exact Windows build evidence](downloads/RELEASE-EVIDENCE-VERIFIED.json)
- [Full independent QA receipt](downloads/WINDOWS-0147-ACCEPTANCE-VERIFIED.txt)

## Verified exact published installer

| Gate | Result |
| --- | --- |
| Native Windows 0.14.7 build and in-place upgrade, data protection and FFmpeg | [PASS 42595044624](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595044624) |
| Publish pretested EXE bytes without rebuilding | [PASS 42595856442](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595856442) |
| Independent download/install, real Edge GUI, backup/restore, security, uninstall | [PASS 42595895083](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42595895083) |
| Real Edge click: four narrative beats → two important visual scenes; local Markdown picture brief downloaded | [PASS 42596100140](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42596100140) |
| Real Edge Audio-first button with **synthetic/mock local SRT** (not true Burmese recognition accuracy) | [PASS 42596129789](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42596129789) |
| 12 important-artwork + 21 conservative major scene unit tests | [PASS 42594598985](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42594598985) |

**New:** Generate only-important-scene photo checklists; no new art requests for ordinary rain/character mentions or silent encoder segments. Optional offline audio-first Smart Scene works if **you separately supply whisper.cpp CLI and a multilingual speech model**. Existing SRT/pause estimates remain available.

**Not bundled:** whisper.cpp executable, Burmese ASR model, offline image generation, Google Drive sync, code signing. The optional Audio-first flow was tested with a mock local SRT; real Burmese speech accuracy is unverified.

**Earlier full-novel proof:** The actual 0.14.6 Windows EXE successfully produced one continuous 90-minute 1920×1080 H.264/AAC MP4 with **one unchanged background**, 162,000 frames and preserved synthetic WAV. [PASS 42555826576](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555826576). This 90-minute encode was **not repeated on 0.14.7**.

Real owner's laptop has not been used or tested, and this is an **unsigned** build. Only synthetic media was used in GitHub Actions. Original private novels, voice recordings and photos do not belong in this public repository.

[မြန်မာလို စတင်အသုံးပြုနည်း](https://github.com/zmozmo/mmmn-video-studio/blob/main/WINDOWS-QUICKSTART-MM.md) · [0.14.7 release notes](https://github.com/zmozmo/mmmn-video-studio/blob/main/WINDOWS-0147-RELEASE-NOTES.md)
