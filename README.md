# MMMN Video Studio 0.15.5 — exact verified unsigned Windows setup

- **File:** downloads/MMMN-Video-Studio-Setup-0.15.5.exe
- **Bytes:** 64,849,752
- **SHA-256:** `82a46db961713db2a38fdd9bad998cd351e7a87f9bb548329161a2885816f63a`
- [Full native Windows install/upgrade/MP4/154 Python tests, backup and uninstall PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42765624705)
- [Exact byte-identical public installer publication PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42766327090)
- [Independent real Windows/Edge QA with actual imported photo matched to one major scene, no source media/locked scene modifications PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42766360083)

Version 0.15.5 can propose already-imported local picture files for existing important scenes from their filename and tags, **only with explicit user confirmation**. It never fetches artwork, creates new images, changes the original audio, accepts subtitles silently or adds extra photo transitions for ordinary rain or dialogue.

The Windows application is offline-first and needs no separate Python, Node or paid API. An optional Burmese CPU ASR model pack is separately built and **must not be considered ready until the independent installed-Studio/model integration QA and package release pass**. Scene-to-word speech time alignment is not certified.

Installer is **unsigned** and may warn under Windows SmartScreen. It has been tested on disposable Windows runners, NOT yet on the owner's own computer.

[Complete release notes](https://github.com/zmozmo/mmmn-video-studio/blob/main/WINDOWS-0155-RELEASE-NOTES.md)
