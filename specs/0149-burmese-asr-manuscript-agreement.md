# SDD 0149 — Burmese Speech-to-Manuscript Agreement Guard

**Windows app:** MMMN Video Studio 0.14.9 · **Scope:** offline, local-only.

## User requirement

Change the background only when the narration actually reaches a **major** dramatic/setting change. Do not change images on every keyword, ordinary rain, mention of a girl, incidental action, or arbitrary 20/60-second timer.

The previously verified 0.14.6–0.14.8 Smart Scene planner takes a timestamped SRT as possible audio evidence; the local multilingual Whisper.cpp base model gave **100% observed character error** on one public Burmese audio sample even though it returned a syntactically valid SRT. Invalid content must never silently drive a storyboard.

## Design and safeguards

1. Accept the user-supplied **original manuscript** as read-only comparison evidence.
2. After optional local ASR returns timestamped SRT, perform `assessBurmeseTranscript(originalEvidence, cues)` (local deterministic Myanmar-script seven-codepoint sequence comparison).
3. **If unsupported or insufficient:** do NOT import the bad generated cues into the project or use them for photo timing. Explain that the transcript does not match the actual story, preserve original narration/manual edits and fall back to clearly labelled local silence or text estimates. User can import a corrected SRT.
4. **If supported:** a human must still review words and timestamps. Never auto-approve pictures or certify Burmese word-level alignment.
5. Existing edited or imported SRT always takes precedence. Do not replace it automatically.
6. Keep 0.14.8 nonblocking cancellable offline speech worker, safe child cleanup, local authenticated API, backup, 90-minute MP4 support, original asset SHA and manual lock protection.
7. No model/API/download, telemetry, source disclosure or cloud call in the agreement module.

## Test cases

- Matching Burmese passage has enough diverse evidence to permit a **reviewable proposal**, not automatic approval.
- Unrelated Burmese output with valid SRT timestamps is rejected.
- English-only output, empty/truncated text, excessively long text, and repetitive short phrases do not pass.
- Mixed unrelated cues cannot pass on one matching phrase alone.
- SRT/manuscript inputs are not mutated.
- In a separate *real installed Windows Edge* test, click Audio-first, use synthetic bad versus matching SRT responses, and verify only the matching SRT persists after native save/reload.

## Evidence and limitations

- [13 deterministic manuscript-match tests and inherited 33 storyboard/photo tests — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42628226679)
- [0.14.9 source patch chain + inherited audio cancellation/backup tests — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42629403329)
- [0.14.9 Windows build, old-to-new installer upgrade, real local MP4 — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42629403389)
- [0.14.9 exact tested installer publication — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42630331371)
- [Actual installed Edge rejection of incorrect SRT **and** acceptance of matching review-only SRT, verified native project reload — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42647519009).
- [Exact public 0.14.9 Setup.exe independent Windows install/upgrade, Edge UI, backup/security, uninstall, and two-case speech acceptance — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42647941174).
- [Real public Burmese sample with official Whisper.cpp ggml-base: **100% observed character error** (single clip)](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42601243930).
- [Burmese-specific 23.8M CPU Conformer model publisher's public sample: **0% observed character error**, 2.9s CPU; research only, NOT bundled](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42630539897).

**Not complete:** True 90-minute Myanmar novel semantic comprehension, scene word alignment, a production-ready integrated Burmese-specific CPU inference runtime, independent multi-speaker ASR accuracy testing, owner Windows laptop acceptance, and software code signing. Do not advertise these as completed.
