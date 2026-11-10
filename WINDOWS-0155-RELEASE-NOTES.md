# MMMN Video Studio 0.15.5 — Conservative Local Important-Scene Picture Suggestions

**10 November 2026** · Windows 11 x64 · unsigned offline-first, Android paused.

**[Exact QA-verified Windows 0.15.5 Setup.exe](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0155/downloads/MMMN-Video-Studio-Setup-0.15.5.exe)**

- Size: 64,849,752 bytes
- SHA-256: 82a46db961713db2a38fdd9bad998cd351e7a87f9bb548329161a2885816f63a

## New visible feature

- Import local original photos into the private on-disk Studio library. The new major-only picture match button uses **names and tags** to suggest a matching already-imported photo at an existing important scene boundary.
- Nothing is downloaded, scraped or AI-generated, and mere rain/brief character mention does not create a new background.
- Conflicting labels are left unresolved. The user must confirm proposals; even then image status remains **review-required**, never marked manually approved.
- Original narrator audio, imported photo files, accepted subtitle cues and manual time/photo locks are untouched. No visible image boundary is added; renderer-only 3600s technical continuations keep the same picture.
- This does NOT perform automatic AI visual recognition or create images.

## Evidence

| Validation | Result | GitHub Actions |
| --- | --- | --- |
| New local image match regression tests (incl. must already be imported), scene and artwork tests | PASS | [Unit tests](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42765625141) |
| Full pinned 0.14.1→0.15.5 Windows source patch and UI witnesses | PASS | [Source Preflight](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42765624706) |
| Native Windows installer, in-place upgrade, FFmpeg MP4, 154 Python tests, data retention and uninstall | PASS | [Native Windows](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42765624705) |
| Published byte-identical checked Windows unsigned installer | PASS | [Publisher](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42766327090) |
| Independent public EXE download, Edge, actual imported local PNG match, manual confirmation, unchanged original photo SHA and SRT, persistence and uninstall | PASS | [Independent Windows + Edge](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42766360083) |
| Same-background exact 90-minute Full-HD MP4 using released 0.15.5 installer | IN PROGRESS | [Long Video](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42766359981) |

## Optional real Burmese CPU Model

- The Windows application contains optional offline Burmese CPU model routing, but the heavy model is **not bundled** in this 64 MB Studio installer.
- A separate optional model pack 0.15.4 passed native Windows install/real public-speech inference and remains subject to independent installed Studio+model end-to-end QA before any public download.
- No real author's private 90-minute Burmese narration has been independently assessed. Model subtitles are segment-level estimates, not exact word alignment. Human approval is mandatory.

**Still outside this release:** full automated high-quality offline image generation, full novel semantic video understanding, automatic Google Drive private manuscript sync, digital code signing and Android build.

[မြန်မာလိုစတင်အသုံးပြုနည်း](WINDOWS-QUICKSTART-MM.md) · [Photo matching specification](specs/0155-offline-important-scene-image-labels.md)
