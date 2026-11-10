# Research 0153 — Truly local 90-minute Burmese narration segmentation

Experimental optional CPU ASR adapter, NOT built into any Windows setup.exe.

- Input: already-local audio and already-local freococo/myanmar_asr model folder (Apache-2.0).
- Processing: ffprobe checks original duration; FFmpeg detects pauses and generates nonoverlapping 7–28s chunks; one CPU model instance handles the chunks.
- Output: private local REVIEW-ONLY SRT with *segment-level approximate* times. Does NOT certify individual word timing.
- Max 90 minutes. Supports dry-run segmentation without importing the model.
- Absolutely no automatic speech-model downloads, network calls, public GitHub audio uploads or source media edits.
- Never overwrite a pre-existing corrected SRT. Failed transcription cannot produce a complete final SRT.
- Validation is deterministic; no actual full-novel author speech has been tested. Model Python/PyTorch runtime is NOT bundled in the Windows EXE.
- Model-output quality must pass existing 0.15.1 manuscript agreement and full-voice coverage gates before scene review.

TODO before installing in the end-user app: CPU/RAM/time benchmark on Windows 11 16GB, real long Burmese recordings from diverse authors with explicit local consent, robust cancel/progress, streaming model architecture and safe one-click optional model setup.
