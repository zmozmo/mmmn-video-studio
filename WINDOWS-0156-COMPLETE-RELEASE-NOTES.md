# MMMN Video Studio Complete 0.15.6 — Stable image continuity and Burmese Offline AI

**10 November 2026** · Windows 11 x64 · current-user installer · unsigned · offline-first.

**[Download exact independently verified Complete Setup.exe](https://github.com/zmozmo/mmmn-video-studio/releases/download/mmmn-complete-0.15.6/MMMN-Video-Studio-Complete-0.15.6.exe)**

- Name: `MMMN-Video-Studio-Complete-0.15.6.exe`
- Size: **429,187,874 bytes**
- SHA-256: `41a71126e8957e4732fe75036fbca6cf22fa5a263068e93ed61379f8d7984e7d`
- Includes exact released **Studio 0.15.6** and independently verified Burmese **CPU Model 0.15.4**; no paid API or additional model installer.
- Source and binary lineages are SHA-pinned. Private manuscripts/audio are not uploaded.

## New in 0.15.6

- **🎞️ Missing-image continuity button**: a reviewer can reuse an EXISTING native-imported photo at a subsequent unassigned important scene, avoiding a blank new visual while preserving the underlying storyboard timing.
- An author-selected alternate image, a manually locked blank, or a missing/unverified source photo is NEVER silently replaced. Disagreement on technical same-image encoder splits fails closed.
- No random photo rotation when ordinary rain, a character entrance or dialogue is mentioned. Changes to major setting, pivotal reveal or truly altered atmosphere remain rare.
- The existing model outputs private locally recognized Burmese subtitles, but not reliable word-level synchronized 90-minute transcription.
- No automatic picture drawing/generation or private Google Drive sync is claimed.

## Verified real Windows QA

| Check | Result | Workflow |
|---|---|---|
| Conservative image-continuity guard with 90-minute same-photo tests | PASS | [Unit](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42783068247) |
| Full source patch chain and fail-closed guards | PASS | [Preflight](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42783068284) |
| Studio install, native in-place upgrade, FFmpeg, 154 Python tests, backups, SHA integrity, uninstall | PASS | [Native](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42783068949) |
| Public Studio EXE installed on fresh Windows, real Microsoft Edge photo continuity clicked, original PNG/SRT preserved | PASS (retry) | [Independent Studio](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42784019444) |
| 3 independent Windows runners, 24 saved manuscripts each, 4 reloads each; 72 native saves, no HTTP 400 | PASS | [Native Save Stress](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42785509349) |
| Complete ONE EXE with Studio + installed genuine CPU model, real public Burmese voice-to-SRT and source integrity | PASS | [Native Complete](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42784472878) |
| Exact published one-file EXE independently downloaded, verified, installed, private voice-to-SRT produced offline, safely uninstalled | PASS | [Independent Complete](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42785504940) |
| Published 0.15.6 full 90-minute unchanged-background video | IN PROGRESS at doc update | [Full-HD](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42784019592) |

A first independent Studio run experienced a native save HTTP 400 and the next run passed. The follow-up three-run repeated save stress passed; this reduces concern but cannot prove zero intermittent problems on every machine. The stress runner now records diagnostics if a reload fails.

## Not yet certified

- 90-minute *actual author Burmese speech* lexical accuracy, speaker/word-level alignment or fully automatic perfect scene placement. Tests include short real Burmese public audio and deterministic 90-minute segments, not the owner's private author recording.
- Automatic creation of new illustrated backgrounds on this 16GB Intel laptop.
- Android release, one-click personal laptop acceptance, signed Windows publisher, Google Drive auto sync.

[မြန်မာလိုအသုံးပြုနည်း](WINDOWS-QUICKSTART-MM.md) · [Technical notes](specs/0156-offline-picture-continuity.md) · [Source](README.md)
