# Windows 0.14.4 — Atomic Project Saves and Safer Media Finalization

**Windows-only**; Android paused; no AI API/subscription or personal user media in public CI.

- Project saves use random exclusive temporary files (instead of predictable `project-state.pending.json`) and clean up if atomic replacement fails. Preserve existing previous/older recovery copies and refuse recovery symlink destinations before writing.
- Imported audio/image/video finalization rejects symlink partials and metadata; Windows rename rejects a target that appears after collision preflight instead of overwriting it.
- Actual Windows UI shows the current version, eliminates misleading trial status, and documents the one-click Open Backup Folder + external-drive copy workflow without any ZIP or command prompt.
- Nine regression tests cover saved manuscript recovery, predictable temporary-file collision, failed replace cleanup, recovery symlink rejection, exact audio checksum, partial/metadata symlink refusal, and current UI copy.

## Release policy

0.14.3 stays verified while this candidate is tested. Require two real NSIS installer builds, install and in-place upgrade, H.264/AAC MP4 render, real Windows Edge UI, full backup/restore, byte-identical user project/media, uninstall preservation, exact-binary publication, and independent published-EXE Windows QA before promoting 0.14.4. Unsigned and never tested on the user's own laptop unless explicitly authorized.
