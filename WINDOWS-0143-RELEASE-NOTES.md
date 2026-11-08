# MMMN Video Studio Windows 0.14.3 — candidate until independent QA PASS

This is a Windows-only incremental hardening release built on the independently
verified 0.14.2 baseline. Android remains paused. No private manuscripts, images,
recordings, API secrets or cloud sync are included.

## Changes

- Reserve outstanding bytes from all active media imports at upload preflight,
  preventing independent WAV/image imports from overcommitting the same disk.
- Recheck disk headroom before **each** media chunk is written; if free space
  drops unexpectedly, reject the chunk before changing the partial file.
- Refuse pending-import metadata/partial symlinks before reading or writing.
- Add five unit tests for concurrent reservations, abort capacity recovery,
  low-space chunks, successful byte-exact imports and symlink overwrite refusal.
- Preserve verified full-media backup/restore, offline H.264/AAC rendering,
  all UI improvements, and the 0.14.2 published release as rollback.

**Release gate:** Must pass Windows A/B Build → Install → In-place Upgrade →
Real H.264/AAC MP4 Render → GUI → Backup/Restore → Uninstall, and a second
separate Windows runner testing the EXACT published setup.exe. Until then,
0.14.2 remains the approved latest release. User laptop not tested.
