# MMMN Video Studio (Windows-only)

**Status:** Windows x64 installer is under real GitHub Actions verification. Do not regard source-only tests as a Windows release.

- `public-safe-windows-source.zip`: audited source bundle with synthetic demo content only; no private manuscripts or user media.
- `.github/workflows/windows-installer-upgrade-lab.yml`: on Windows runner verifies source archive SHA256, runs JavaScript/Python, builds NSIS `setup.exe` with packaged FFmpeg, installs version A, upgrades in place to version B, verifies offline MP4 and project/media hashes, uninstalls, and publishes the exact tested unsigned installer only after all steps pass.
- View build state under **Actions**; download the verified installer artifact only on a successful run.

Android work is paused. The app is offline-first and the narrator provides their own audio.
