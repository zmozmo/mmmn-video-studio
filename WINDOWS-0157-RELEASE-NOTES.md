# Windows 0.15.7 — Important-scene artwork review queue

Status: **SOURCE QA PASS; native Windows installer & public binary acceptance pending**.

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

The previously independently verified **0.15.6 Complete** remains the recommended released one-file Windows installation until 0.15.7 has independently passed published binary testing.

Unfinished: local CPU model inference with real art-generation weights/quality, user's 16GB Intel laptop performance, exact word-level 90-minute Myanmar voice ASR, direct private Google Drive, and Android installer. Do not describe the review queue as automatic image generation.
