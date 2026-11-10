# MMMN Burmese Offline AI Speech Model Pack — Windows 0.15.4

**Status: RELEASED after Windows native model tests and independent installed Studio-to-model QA.**

## Two files; no coding or ZIP replacements needed

1. [Main Video Studio 0.15.5 setup.exe](https://raw.githubusercontent.com/zmozmo/mmmn-video-studio/windows-binaries-0155/downloads/MMMN-Video-Studio-Setup-0.15.5.exe) — 64,849,752 bytes; SHA-256 `82a46db961713db2a38fdd9bad998cd351e7a87f9bb548329161a2885816f63a`.
2. [Optional Burmese Offline CPU AI Model Pack 0.15.4 setup.exe](https://github.com/zmozmo/mmmn-video-studio/releases/download/burmese-asr-addon-0.15.4/MMMN-Burmese-ASR-Offline-Addon-0.15.4.exe) — **364,228,875 bytes**; SHA-256 `af81e68f3971d6374bffa0987f547e716606e6cf46a45c72b9cf6274729dadeb`.

Install the Studio first and Model Pack second, as normal current-user Windows EXEs. The user does not need PyTorch, Python, Node, VS Code, a source ZIP or a subscription. The heavy model is a separate component to keep the main editor small and allow offline editing without speech recognition.

## Using your own narration offline

Import your Myanmar manuscript and the original narration audio. Start **🎧 အသံဖတ်ပြချက်နဲ့ အရေးကြီး Scene** on the chapter storyboard. With the add-on installed, the existing cancellable offline worker invokes the Burmese-specific CPU Conformer and produces a local *draft SRT*. The app checks manuscript matching and full original narration coverage before the SRT may even be proposed. Human proofreading/confirmation is always required. Original audio, manually accepted SRT, image selections and timing locks are never deliberately overwritten.

Use **🎬 အရေးကြီး Scene မှသာ ပုံပြောင်း** to make conservative major-only scene proposals; plain rain, dialogue or a minor entrance are not a reason to rotate photos. Then use **🧭 အရေးကြီး Scene / SRT အချိန်တိုက်စစ်ချက်** and **🖼️ အရေးကြီး Scene အတွက် ရှိပြီးပုံများ စစ်ရွေးရန်** to verify approximate timing and match already imported native photos. These actions do not invent or download images. For missing artwork, export the local private picture brief and provide your own photos.

## Independent proof

- [Public 108.24-second Burmese six-clip CPU speech → local SRT PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42762225771).
- [Windows native model pack install + real Burmese recognition PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42766366243).
- [Independent Windows installs actual published Studio + actual local CPU model, real public speech, local SRT, preserved voice/project/locks PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42767034087).
- [Publisher verified exact installer file SHA from independently successful model+Studio E2E before release PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42767194551).

## Limitations

- The Burmese model is not perfect: an earlier six-public-clip test found 13.6% aggregate character error, with per-clip errors up to 30.5%; public test samples may overlap training data.
- This is chunk-level SRT timing, **not word-accurate forced alignment**. The user's own 90-minute Burmese novel, exact model memory, speed and real-world scene timing on the owner's laptop still need private local acceptance.
- No automatic model training, unlimited AI image generation, unpublished novel uploads, Google Drive auto-sync, Windows code signing or Android Studio runtime.
- Installer is unsigned. Validate the exact SHA-256; never disable Windows security globally. Allow enough free disk space for extraction, model installation, multimedia assets and MP4 encoding.

### Third-party model

The CPU model is [freococo/myanmar_asr](https://huggingface.co/freococo/myanmar_asr), Apache-2.0 licensed. The bundled open-source Python/PyTorch dependencies have their own upstream licences. Attribution is included with the installer and GitHub release. No personal audio is used in public build/QA.
