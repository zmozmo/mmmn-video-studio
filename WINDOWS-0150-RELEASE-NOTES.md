# MMMN Video Studio 0.15.0 — Offline Burmese SRT Chronology Protection

**Released: 10 November 2026** · Windows 11 x64 · unsigned executable · Android paused.

**[Download official exact tested Setup.exe](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0150/downloads/MMMN-Video-Studio-Setup-0.15.0.exe)**

- File: `MMMN-Video-Studio-Setup-0.15.0.exe`
- Size: **64,836,579 bytes**
- SHA-256: `ce60a9c9e8f40caf68c5d2d0573e966e875bc75a7099e15c10dd3525508b66b3`
- Python/Node/VS Code are **not needed** to install or run. No online video generation service is used.

## Changes

- Strictly reject malformed, negative, backwards, overlapping or non-finite generated SRT cue times.
- Cross-check speech cues against original local manuscript; require substantial per-cue agreement and plausible narrative ordering rather than aggregate word overlap alone.
- Do not exaggerate evidence by concatenating the same chapter story and generated scene excerpts.
- Even a matching transcript requires a separate explicit choice before its timing is used for **draft-only** major-scene proposals.
- Preserve original narration, previously corrected SRT, manually locked artwork/timings, project state and SHA-verified backup/restore.
- Avoid changing backgrounds for small events such as ordinary rain or passing characters. Keep long visually unchanged stretches on one image.

## Verified Windows QA

| Gate | Result | Evidence |
| --- | --- | --- |
| Deterministic Burmese SRT and major-scene regression tests | PASS | [Unit QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42749464444) |
| Full source preflight | PASS | [Preflight](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42749464270) |
| Actual Windows Installer, upgrade, MP4, backup, 145 Python tests, uninstall | PASS | [Native QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42749464288) |
| Exact tested binary publication | PASS | [Publish QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42750121344) |
| Independently downloaded public EXE and real Windows/Edge/data QA | PASS | [Independent QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42750156953) |
| 90-minute full-HD MP4 on 0.15.0 exact published EXE | IN PROGRESS | [Long-form QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42750156838) |

## Important limitations

**The Windows setup does not bundle a Burmese speech recognition model.** A separately configured compatible offline whisper.cpp CLI/model is necessary for optional ASR. Observed character error for generic Whisper Base on one public Burmese clip was 100%; another Burmese-specific research candidate matched its own author's sample but is not validated on independent long-form narration or built into the installer.

Agreement of text with the manuscript does not prove spoken words are correctly aligned at exact timestamps. Major-only picture proposals still require proofreading/review. The app does not auto-generate pictures or fetch private Google Drive images. The user's actual Windows laptop has not been tested; unsigned installers may trigger SmartScreen. Do not put private manuscript or recordings on public GitHub.

[Myanmar quickstart](WINDOWS-QUICKSTART-MM.md) · [technical requirements](specs/0150-burmese-srt-chronology.md)
