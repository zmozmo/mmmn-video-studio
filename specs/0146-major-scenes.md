# SDD 0146 — Conservative Major-Scene Auto Draft (Windows Offline)

**Status:** Source module, 21 unit tests, Windows installer and independently installed Edge UI **PASS**. The additional 90-minute unchanged-picture actual-video test is separately tracked.

## User story

For one narrated Myanmar novel (up to **90 minutes**, optionally 120 minutes headroom), **do not rotate background pictures on every noun, keyword, action or character mention**. The narrator's illustrations should mostly remain calm and stable, changing only at a clear major setting transition, a transformed atmosphere (heavy rain **and** a dark, oppressive dusk/night), a central revelation, significant confrontation or an author-marked visual beat.

Example: ordinary **“မိုးရွာတယ်”** must NOT change the picture. **“မိုးအရမ်းသည်းပြီး ညနေမှောင်မိုက်လာတယ်”** is a possible strong mood transition. **“မိန်းကလေးတစ်ယောက်ပေါ်လာတယ်”** alone must NOT change the picture.

## Current technical scope

- A new **Major-only Auto Draft** button uses the existing real Windows `makeOfflineDraft` engine, story image requirements, local image filenames, SRT evidence if present, and optional offline FFmpeg narration-pause hints.
- Pure `web/major-scene.mjs` groups adjacent timeline scenes *without changing the audio duration*. It starts with the current background and keeps it by default. Major transitions are accepted only with **multiple corroborating textual cues**, not a lone keyword.
- **75-second minimum hold** before another suggested picture switch by default. **No arbitrary maximum duration** forces a visible picture change. If native FFmpeg requires a new technical scene after **3600 seconds**, the exact same background image is reused with no new visual beat. Separate counts for image changes and technical render segments. Author-marked critical beats may override after a minimum safe interval.
- **Do not alter existing manual-confirmed images, visual locks, manually fixed scene start or duration.**
- Use only existing imported images and established image-requirement IDs. Never pretend to generate an image. All new proposals remain **unapproved / subject to review**; preview, manual replace, lock and undo are available.
- An existing SRT or model-generated transcript (if separately available) provides *potential* narration timestamps, but transcription must be proofread. Without SRT, local FFmpeg pauses or manuscript-length estimates are only approximate.
- Saving a new draft requires explicit confirmation and an undo checkpoint. No cloud upload, no original novel/audio rewrite or Google Drive modification.

## Important truthfulness boundary

This deterministic conservative selector is **not a trained Burmese semantic model** and **does not transcribe narration on its own**. It cannot reliably interpret every symbolic or implicit plot turn. A complete automatic “listen → understand the novel → change only the correct picture exactly when spoken” feature still needs a reliable **offline Burmese ASR model**, timestamp alignment, better semantic classification, and real-novel QA. The app must never claim those capabilities until demonstrated.

## Acceptance tests

1. Rain alone, mention of a woman, dialogue turn → **keep current background**.
2. Severe rain + dusk turning dark → **one mood-shift proposal**.
3. Arrival at a clearly different location → **one location proposal**.
4. Brief new-character appearance → **no proposal**.
5. Central revelation, severe confrontation → **major proposal**.
6. No forced image switch on a long quiet stretch; no slideshow-like fixed-interval switching.
7. Existing confirmed picture, fixed timing, locked scene → unchanged.
8. Original scene objects, total narration duration, and timeline continuity remain intact.
9. Missing pictures remain missing; never assign an invented image ID.
10. SRT or audio pauses must be labelled evidence/estimates, not claim verified speech-level understanding.
11. Native UI integration and offline import are covered by Windows 0.14.6 install/upgrade/security tests before publishing a new EXE.

## Release acceptance evidence

- 21 deterministic behavioral tests: [PASS 42555074044](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555074044).
- All incremental source patches applied cleanly: [PASS 42555074115](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555074115).
- Native Windows 0.14.6 install/upgrade/FFmpeg: [PASS 42555073944](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555073944).
- Exact public EXE UI: [PASS 42555752046](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555752046).
- Extended 90-minute one-visible-image export: [42555826576 — **PASS**](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555826576). The published installer encoded a 5,400-second H.264/AAC Full HD MP4 with 162,000 frames, one unchanged visible photo and original synthetic WAV SHA preserved.

## Source locations

- `web/major-scene.mjs` — deterministic conservative scene selector.
- `tests/major-scene.test.mjs` — **21** focused tests (including uninterrupted 90/120-minute same-photo output and native 3600-second scene limit).
- `.github/scripts/upgrade_windows_0146.py` — versioned Windows UI integration.
- Existing `web/auto-edit.mjs`, `web/core.mjs`, pause analyzer, local media importer and renderer remain responsible for draft assets, timing and MP4 export.
