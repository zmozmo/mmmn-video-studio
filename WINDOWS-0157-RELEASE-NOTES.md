# Windows 0.15.7 — Important-scene artwork review queue

Status: **RELEASED — Windows Native + independent public one-click Complete 0.15.7 QA PASS**.

The Studio's new Burmese timeline action **🎨 အရေးကြီး Scene ပုံလိုအပ်ချက် စစ်ရန်** exports a local private Markdown report about missing pictures at important scene boundaries.

- Keeps ordinary rain, minor character entrances, dialogue, and technical same-photo 3600s encoder continuations on the existing picture.
- Shows missing important-scene artwork only; at most 12 proposals per chapter in ordinary use, 24 maximum in the underlying library.
- Does not replace original image selections, manually locked blank scenes, SRT, original recorded voice, timeline boundaries or backups.
- Does NOT download/generate any image or call an external AI/model service.
- The research-only FastSDCPU 0.15.7 loopback bridge may create unapproved local image previews ONLY after explicit author consent, but it is not yet installed in this Windows release. It now refuses redirecting private scene prompts away from 127.0.0.1.
- Scene-based prompts include unpublished manuscript fragments. Never put them on public GitHub or send them to a hosted model.

Verified evidence:
- [Source preflight PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42791641124)
- [Private major-only candidate queue CI PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42790870264)
- [Localhost bridge redirect privacy regression PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42790647600)
- [Native Windows 0.15.7 Installer/Upgrade QA (check status)](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42791641398)

**Latest independently verified one-file Windows installation: [Complete 0.15.7](https://github.com/zmozmo/mmmn-video-studio/releases/download/mmmn-complete-0.15.7/MMMN-Video-Studio-Complete-0.15.7.exe)**. File 429,190,822 bytes; SHA-256 `537eb7f1b943f8f686fd75fe0e99497197534e97f7eb35c04d0ae175d7573ad5`.

- [Native Windows Studio 0.15.7 upgrade and MP4 safety PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42791641398).
- [Independent exact Studio 0.15.7 public EXE real Edge local image queue/no modifications QA PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42792616245).
- [Complete 0.15.7 ONE setup installs Studio and the Burmese CPU model, REAL speech-to-SRT PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42792792099).
- [Independent COMPLETE 0.15.7 public setup/download SHA verification, install, local Burmese speech and uninstall QA PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42793480635).

Unfinished: local CPU model inference with real art-generation weights/quality, user's 16GB Intel laptop performance, exact word-level 90-minute Myanmar voice ASR, direct private Google Drive, and Android installer. Do not describe the review queue as automatic image generation.
