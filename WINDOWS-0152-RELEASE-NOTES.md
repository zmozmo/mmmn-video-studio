# MMMN Video Studio 0.15.2 — Important Scene/SRT evidence review

**Released 10 November 2026** · Windows 11 x64 · unsigned, offline video rendering, Android paused.

**[Exact tested Windows 0.15.2 Setup.exe](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0152/downloads/MMMN-Video-Studio-Setup-0.15.2.exe)**

- Installer bytes: **64,853,687**
- SHA-256: d7196122d31402eac27e71b659b4a55015609f83bad376356ffda4916a122c74
- No VS Code, Python, Node.js, paid API or source ZIP required for ordinary app use.

## Added in 0.15.2

- A real clickable Burmese major-scene vs SRT timing evidence button in the Windows Edge UI.
- Generates a private local Markdown listening/review report for only important visible scenes.
- Uses full-narration SRT coverage and original Myanmar manuscript agreement gates first.
- Unique short matching passages can suggest one SRT cue start to listen to; this is NOT verified word alignment or author approval.
- Duplicate passages, insufficient speech, truncated/incorrect SRT produce no suggested cue.
- No original audio, corrected subtitles, manually locked scene, picture, project data, or backup is changed.
- Existing conservative storyboard keeps ordinary rain/dialogue/character entrances on the same image.

## Evidence

| Windows QA | Result | Run |
| --- | --- | --- |
| Major SRT scene matching and old regressions | PASS | [Unit QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42755522208) |
| Full source patch chain and real UI actions verified | PASS | [Preflight](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42755522551) |
| Native Windows install/upgrade/FFmpeg/145 Python tests, data and backup, uninstall | PASS | [Native QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42755522222) |
| Published EXACT tested unsigned installer | PASS | [Publish](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42756195741) |
| Separate real Windows download, upgraded install, Edge 3 mocked speech cases + PRIVATE report download with no project mutation, security/uninstall | PASS | [Independent QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42756225248) |
| Entire 90-minute unchanged-background 1080p MP4 from exact published 0.15.2 EXE | IN PROGRESS | [Longform](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42756225385) |

## Still not in the installer

- Accurate word-level alignment of a 90-minute Burmese novel has NOT been demonstrated.
- No bundled local Burmese ASR neural model. The separately developed 0.15.3 long narration chunker is RESEARCH ONLY and still needs a packaged CPU model/runtime and real author voice evaluation.
- No automatic new background image generation or direct Google Drive sync.
- Signed Windows installer, owner laptop acceptance and Android app not complete.

**Privacy:** the local scene report can include UNPUBLISHED manuscript snippets. Do not publish it on GitHub. The public QA uses synthetic text/audio only.

[မြန်မာလိုအသုံးပြုနည်း](WINDOWS-QUICKSTART-MM.md) · [0.15.2 engineering spec](specs/0152-important-scene-srt-evidence.md)
