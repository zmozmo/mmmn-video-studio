# ASR 0152 — Public independent-source CPU benchmark

This optional research workflow measures the Apache-2.0 Burmese Conformer
model freococo/myanmar_asr against up to six publicly licensed Google FLEURS
Burmese my_mm test clips (CC BY 4.0). It computes a proper character error
rate on short third-party-source recordings, instead of trusting one
publisher-provided three-second sample.

CAVEAT: FLEURS may overlap the model's training data; proof of
training-disjoint evaluation is NOT available. A recorded benchmark result
does not certify exact timestamp alignment, long novels or real-author voice.

The research runner uses only public audio, no private manuscripts, no
private voice, no model binaries added to the Windows installer and no
automatic changes to user assets. Model inference is CPU-only on an
ephemeral Linux host. Actual Windows integration requires further work.

## Measured first public-source run — 10 Nov 2026

**[Reproducible hosted CPU research — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42752466377)**

- 6 publicly available FLEURS Burmese my_mm *test* clips, with no private author audio.
- Observed aggregate normalized Myanmar character error: **13.6% CER** across these six clips.
- Individual observed CERs: 0.0%, 10.4%, 3.1%, 12.9%, 19.7%, and 30.5%.
- CPU inference of each short clip: approximately 1.8–1.9 seconds on one hosted Ubuntu runner.
- This research validates inference and short-audio accuracy only; it does not establish exact speech timestamps, multi-hour processing speed, independent train/test exclusion, or Windows app integration.
- The model's published 9.42% **syllable** error metric uses a different measure and sample set, so it is not directly comparable to the 13.6% observed character error here.

**Decision:** Keep Burmese-specific model as an optional offline integration candidate; do not enable automatic unreviewed chapter scene timing yet.
