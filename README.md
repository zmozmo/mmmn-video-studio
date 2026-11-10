# MMMN Video Studio Windows 0.15.1 — exact verified unsigned executable

- Setup file: downloads/MMMN-Video-Studio-Setup-0.15.1.exe
- Size: 64,831,959 bytes
- SHA-256: 4c0df19cbc6259577a7152c5a008ed990d461ee5ff9a7cdbe73284075f32869b
- [Windows Native Install/Upgrade/MP4/Backup QA — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42751977489)
- [Exact tested binary publication — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42752627042)
- [Independent public-binary Edge, 3 ASR timing scenarios, storage/security/uninstall — PASS](https://github.com/zmozmo/mmmn-video-studio/actions/runs/42752668531)

0.15.1 adds a read-only narration-vs-SRT coverage audit button. It rejects matching but truncated generated subtitles before they drive major-scene timing; also rejects grossly wrong Burmese SRT. Correctly matching SRT still requires manual review, and original audio/SRT and manual image locks are protected.

**No Burmese speech model is bundled; no automatic AI picture generation or private Google Drive synchronization is provided.** Normal Windows usage requires no VS Code or paid subscription. The unsigned installer may show SmartScreen warnings. These checks were on disposable Windows runners, not the owner's actual laptop.

[Release notes](https://github.com/zmozmo/mmmn-video-studio/blob/main/WINDOWS-0151-RELEASE-NOTES.md)
