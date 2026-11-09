# SDD 0147 — Offline Audio-First Major Scenes + Minimal Artwork Brief

**Status as of 2026-11-09:** Source implementation and unit tests PASS. Windows 0.14.7 installer/independent published-EXE QA in progress; do not claim final executable PASS until verified.

## Priority request

The narration of a Myanmar novel (normally no more than 90 minutes) should drive the visual plan, **without randomly rotating pictures**. Ordinary rain words, new people mentioned, and dialogue must not cause unnecessary switches. Only a major change in place, danger, dark atmosphere, reveal or confrontation can justify a different picture. Art creation should be required for only those major beats.

## Deliverables

1. **Important-scenes-only artwork checklist:** after Major-only Draft is saved, select **“🖼 အရေးကြီး Scene ပုံလိုအပ်ချက်သာ ထုတ်ရန်”**. The application downloads an **on-device Markdown** checklist containing only actual planned major visual beats. It reports linked local image assets, missing images and scene times. An internal 3,600-second render segment that repeats the same picture is **not a new required photo**. A filename and author-evidence excerpt help create consistent artwork externally.
2. **Optional Audio-first Smart Draft:** select **“🎧 အသံဖတ်ပြချက်နဲ့ အရေးကြီး Scene (Offline Model ရှိမှ)”**. Existing reviewed SRT always takes priority. Without SRT, if the user has separately installed **whisper.cpp CLI + multilingual ggml model**, the application explains potential time/accuracy cost and **asks for consent before** running fully local Burmese Speech-to-Text. It checks SRT timestamps. On failure/missing model, it falls back to the existing local FFmpeg pause analysis or clearly labelled manuscript estimates.
3. **No loss of manual work:** only on final confirm does the app save a draft with undo checkpoint; a newly recognized SRT is not persisted over existing corrected SRT before confirmation. Existing manual lock, image choice and project backup remain preserved.
4. **No cloud side effects:** no Google Drive sync, remote AI API, automatic picture download/generation, private novel uploads or background network activity. Any exported artwork checklist can include unpublished novel excerpts and should be kept private.

## Acceptance criteria / tests

- **12 photo-brief unit tests:** only major scenes, no extra photos from technical continuation, correct missing/linked media metadata, bad timeline rejected, author-evidence prompts and no invented image generation. [Unit tests PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42594598985).
- **21 conservative major scene tests** remain PASS, including 90/120-minute quiet narration and manual locks. [Earlier QA](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42555074044).
- Full 0.14.1→0.14.7 source patch chain, JS/Python syntax, 0144 and 0145 security/render regressions **PASS** in [0.14.7 source preflight](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42594925798).
- Native installer build, same-version in-place upgrade, independent public EXE Edge GUI import/click/export, backup and security still require separate 0.14.7 tests before marking complete.
- **Real Burmese ASR quality is not certified** by mock whisper.cpp tests; do not state that the app fully understands the spoken novel or guarantees word-level timing.

## Implementation

- `web/major-scene.mjs` — conservative major visual switches (existing).
- `web/major-artwork-brief.mjs` — only-important-artwork checklist (new).
- `tests/major-artwork-brief.test.mjs` — 12 unit tests (new).
- `.github/scripts/upgrade_windows_0147.py` — versioned Windows UI integration; preserves 0.14.6.
- `.github/workflows/windows-installer-upgrade-0147.yml` — actual Windows installer + upgrade QA.
- `.github/scripts/windows_published_release_acceptance_0147.py` — independent installer/Edge UI acceptance.
- `.github/scripts/windows_major_artwork_button_0147.py` — click/save/export local artwork brief.
