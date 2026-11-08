# MMMN Video Studio Windows 0.14.4 — Verified unsigned EXE

[Direct Windows x64 Setup 0.14.4](downloads/MMMN-Video-Studio-Setup-0.14.4.exe) · 64,855,430 bytes

SHA-256: `db57d26241c19c9a2629f959245fa0ecb74c86d5a9bbfe04df8031cfe5da6830`

- [Checksum file](downloads/MMMN-Video-Studio-Setup-0.14.4.exe.sha256)
- [Native installer release evidence](downloads/RELEASE-EVIDENCE-VERIFIED.json)
- [Independent public executable acceptance receipt](downloads/WINDOWS-0144-ACCEPTANCE-VERIFIED.txt)

**PASS** [Windows Build → Install → Upgrade → Render → Uninstall](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42478959788) · **PASS** [exact binary publication](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479446166) · **PASS** [independent downloaded Windows setup.exe QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42479467429).

0.14.4 adds atomic manuscript save staging and recovery symlink protection, import metadata/partial symlink rejection, safe Windows destination collision semantics, updated offline UI and full backup Explorer guidance. This repository branch contains only public-safe files and the unsigned EXE. User manuscript/recording/image data is never uploaded.

**Additional [long-form published EXE test PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491529466):** 15-minute WAV (28,800,044 bytes) streamed with per-chunk integrity, full backup/restore, and 3 H.264/AAC two-second chapters combined to one 180-frame, 6.023-second MP4. [QA addendum](downloads/WINDOWS-0144-LONGFORM-VERIFIED.txt).

**All four full-quality MP4 export presets PASS:** [Independent public EXE Windows QA 42491917768](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42491917768): YouTube 1920×1080, TikTok 1080×1920, Facebook 1080×1350, Square 1080×1080; H.264/AAC, 30fps, each one-second synthetic clip. [Complete QA addendum](downloads/WINDOWS-0144-LONGFORM-VERIFIED.txt).

**Final [extended native published-binary stress QA PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42492649641):** 45 seconds of actual 1080p video at 30fps, same export twice, 9s 1080p dissolve, cancel/retry, simulated USB-style backup copy/loss/restore with SHA-256. [Full receipt](downloads/WINDOWS-0144-LONGFORM-VERIFIED.txt).

**[Five-minute full-HD MP4 exported and independently inspected — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42493062578).** 300.000s, 1920×1080, six scenes, 30fps / **9,000 frames**, H.264/AAC; hosted Windows runner encoded in **45.9s**. This is not an owner-laptop performance estimate.

**[15-minute Full HD MP4 — Windows Runner PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42493702496):** exact already-published EXE encoded an uninterrupted 900-second, six-scene 1920×1080 H.264/AAC video, 30fps / **27,000 verified frames**. Encoder time 132 seconds on that runner; not a performance estimate for the owner's laptop. Earlier 5-minute MP4 SHA stayed unchanged. [Long-form receipt](downloads/WINDOWS-0144-LONGFORM-VERIFIED.txt).

**Windows SmartScreen may warn (unsigned).** Owner's actual laptop remains untested, Android paused. No mandatory subscription or cloud API.
