# MMMN Video Studio 0.14.9 — Burmese Narration Safety and Major Scenes

**Windows 11 x64 · offline-first · unsigned installer · Android paused**

[**Windows Setup.exe (0.14.9)**](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0149/downloads/MMMN-Video-Studio-Setup-0.14.9.exe)

- Exact size: **64,824,927 bytes**
- SHA-256: `28d3f9b9d886986eeb3ebb8f908b22206e6debe22179c767f4ec733ca9d6ee1b`
- Python, Node, VS Code, subscriptions and online video APIs not required for normal use.

## New safety protection

0.14.9 adds an **offline Burmese narration-to-manuscript agreement guard**. Optional Whisper.cpp can return perfectly formatted SRT timings with **incorrect Burmese words**. Before these generated cues drive picture switches, the app compares their Myanmar-script sequences with the user's **existing local manuscript**.

- If clearly unrelated or insufficient, the SRT **is not imported or used for automatic picture timing**. Existing manually reviewed SRT and scene edits remain intact. Timing falls back to clearly labelled local audio pauses or manuscript estimates.
- If sufficient manuscript overlap exists, the output is **only proposed for human review**, never automatically certified correct.
- **Rain mentions, incidental character appearances and dialogue** still do not trigger unwanted picture switches. Major atmosphere, location and story turns can receive a proposed picture change.
- Retains **0.14.8 cancellable local transcription**, original media integrity, manual scene locks, 90-minute video engine and local SHA-verified backup/restore.
- Local image brief still lists **only significant illustrated scenes**; it does not generate or fetch pictures.

This is a deterministic conservative mismatch detector, **not a model that understands Burmese novels or certifies accurate speech-to-text**.

## Completed real Windows acceptance

| Gate | Status | Evidence |
| --- | --- | --- |
| Burmese manuscript overlap guard + retained storyboard regressions | **PASS** | [42628226679](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42628226679) |
| Full pinned 0.14.1–0.14.9 patched source preflight | **PASS** | [42629403329](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42629403329) |
| Native Windows installer build, 0.14.0 upgrade, original audio and backup integrity, offline MP4 | **PASS** | [42629403389](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42629403389) |
| Publish **exact** QA-tested EXE, no rebuilt bytes | **PASS** | [42630331371](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42630331371) |
| Actual published EXE in a fresh hosted Windows runner: real Edge UI, media import, save/reload, full backup/restore, API security and uninstall | **PASS** | [42647941174](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42647941174) |
| Real installed Edge Audio-first button: reject **wrong** Burmese synthetic SRT and accept matching SRT only for human review, persist/reload safely | **PASS** | [42647519009](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42647519009) |
| 0.14.7 exact public EXE: continuous **90-minute 1080p** MP4 (162,000 full frames) with one unchanged background | **PASS** | [42598420189](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42598420189) |

**Long video caveat:** The last 90-minute exact-binary render above used **0.14.7**, not a fresh 0.14.9 90-minute run. The same renderer protections are retained and short offline MP4 build acceptance passed in 0.14.9, but a separate full 90-minute render of the new version is not claimed.

## Real Burmese ASR research (not bundled)

A generic multilingual Whisper.cpp ggml-base produced **100% observed Burmese character error on one public sample**: [42601243930](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42601243930). A Burmese-specific CPU research model achieved **0% observed character error on its publisher-supplied ~3.13-second sample** with ~2.9-second CPU inference on one hosted machine: [42630539897](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42630539897). **Neither single-clip result predicts real-novel accuracy**; the dedicated model is **not integrated into the installer**. No personal voice or unpublished manuscript was used.

## Limitations and next acceptance

- No tested fully automatic `90-minute Burmese audio → accurate aligned transcript → semantically perfect major-only photos` pipeline yet.
- The owner's real Windows laptop, actual novel/voice/photos and thermal/storage conditions have not been tested.
- No automatic private Google Drive photo synchronization or built-in image generation.
- Installer unsigned; Windows SmartScreen may warn.
- The user must review scene timing/word recognition and decide whether suggested pictures match the story.

[မြန်မာလို စတင်အသုံးပြုနည်း](WINDOWS-QUICKSTART-MM.md) · [Technical requirements](specs/0149-burmese-asr-manuscript-agreement.md) · [Release readiness](WINDOWS-RELEASE-READINESS.md)
