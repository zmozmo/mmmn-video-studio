# Windows 0.14.3 — Verified Concurrent-Import and Disk Safety

**Verified unsigned Windows x64 release — 8 November 2026.** Android paused. User laptop not tested.

Based on independently verified 0.14.2, this update adds:
- Import capacity accounting that reserves outstanding bytes from all active imports, preventing concurrent operations from overcommitting free space.
- Pre-chunk free-space checking to preserve headroom if other apps consume disk during an upload.
- Reject pending metadata and media-partial symlinks instead of following them.
- Five regression tests: concurrent overcommit rejection, abort freeing the reservation, low-space chunk rejection without writing, byte-for-byte successful WAV finalization, and symlink overwrite refusal.
- Full compatibility with previous manuscript edit preservation, native Full Backup/Restore, UI storage display, and offline FFmpeg H.264/AAC rendering.

## Verified native release chain

1. [Native Windows build and installer-lab PASS — Run 42475358558](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42475358558): source privacy and regression tests; 120 Python tests and 143 JavaScript tests; native NSIS Build A/B, install, upgrade, MP4 render, real Edge UI, recovery, project/media hashes and uninstall.
2. [Published exact verified EXE PASS — Run 42475837823](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42475837823): released the tested bytes, no rebuild.
3. [Independent published EXE acceptance PASS — Run 42475858282](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42475858282): a separate Windows runner downloaded the actual published binary; confirmed SHA-256; installed 0.14.0 then upgraded to 0.14.3; tested UI, WAV import, full backup/restore, tampered backup refusal, unauthorized API writes, and uninstall.

**Installer:** `MMMN-Video-Studio-Setup-0.14.3.exe` · **64,840,856 bytes**
**SHA-256:** `4c4de4daad56d292e7b697a004f74ffb374ddb7a79916c317f0d2e250d30c3ed`

[Direct executable and release verification receipt](https://github.com/zmozmo/mmmn-video-studio/tree/windows-binaries-0143/downloads)

Scope: free offline-first Windows x64, no mandatory API/subscription. The application is not code-signed. The runner tests do not constitute proof on the user's own laptop, all media codecs or all long-form projects. Personal novels/audio/images were never published.
