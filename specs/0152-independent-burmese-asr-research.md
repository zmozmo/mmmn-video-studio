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
