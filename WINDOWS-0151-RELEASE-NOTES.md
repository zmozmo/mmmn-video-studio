# MMMN Video Studio 0.15.1 — Offline Full-Narration SRT Timing Audit

Released: 10 November 2026. Windows 11 x64, unsigned, offline-first. Android paused.

**[Download exact tested 0.15.1 Windows setup.exe](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0151/downloads/MMMN-Video-Studio-Setup-0.15.1.exe)**

File size: 64,831,959 bytes. SHA-256: 4c0df19cbc6259577a7152c5a008ed990d461ee5ff9a7cdbe73284075f32869b

## Added in 0.15.1

- Read-only local narration/SRT timing audit: coverage percentage, beginning and trailing gaps and the longest gap.
- An actual timeline button in Edge for viewing that audit without editing the original voice, manuscript or reviewed SRT.
- Reject matching Burmese ASR text if its SRT only covers a small part of the narration.
- Preserve 0.15.0 narration sequence, word overlap, human-consent guards and conservative major-only artwork decisions.
- All processing and video rendering remain local; the installer still does not include an offline Burmese ASR model.

## Windows QA evidence

| Gate | Status | Evidence |
| --- | --- | --- |
| Full patch chain + narration timing and storyboard tests | PASS | [Fast QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42751977290) |
| Native Windows 145 Python tests, real installed upgrade/MP4/backup/uninstall | PASS | [Native QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42751977489) |
| Exact tested binary publication | PASS | [Publisher](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42752627042) |
| Independent downloaded public EXE, real Edge, media, backup, security, uninstall | PASS | [Independent QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42752668531) |
| Real Edge rejects wrong Burmese, rejects matching but truncated SRT, and accepts complete matching SRT for human review only | PASS (3 mocked SRT cases) | [Installed Edge QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42752668531) |
| Exact released EXE 90-minute full-HD one-unchanged-picture render | IN PROGRESS | [Long video QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42752668322) |

## ASR Research — Not Bundled

Six public FLEURS Burmese short clips gave 13.6% aggregate observed character error on an Apache-2.0 Burmese-specific CPU model. Clip errors were 0% to 30.5%. [Research QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42752466377). Training-data overlap is not excluded; long-novel accuracy and time alignment remain unproven.

**Not yet built:** fully autonomous long Burmese narration comprehension, built-in AI image generation, private Google Drive artwork sync, a packaged optional Myanmar ASR model and real-user laptop acceptance. Original narration and manuscript are private and must not be uploaded to this public GitHub repository.

[မြန်မာလိုစတင်အသုံးပြုနည်း](WINDOWS-QUICKSTART-MM.md) · [Requirements](specs/0151-narration-timing-audit.md)
