# MMMN Video Studio 0.14.2 — Windows offline storage-safety update

**Target:** Windows 11 x64 and Windows-only workflow. Android remains paused.

This is an update on the verified 0.14.1 installer, not a change to the user's private original manuscripts.

## Included

- **Prevent disk exhaustion on media import:** Before accepting an imported WAV/MP3/video/image file, the Windows server checks free space on the actual drive storing the project. The recording's declared size **plus at least 128 MiB of headroom** must fit, otherwise the operation is refused before creating a partial import.
- **Protect existing recordings:** Preexisting media IDs and symbolic link destinations are not silently overwritten. Finalization also rejects collisions with existing media.
- **Disk headroom visible in the app:** The Updates / Storage screen displays available disk space in GiB so the user can keep enough room for full-media backups and MP4 exports.
- **Five regression tests:** Insufficient disk refusal with no partial file, reserve behavior on tiny imports, byte-for-byte WAV import SHA-256, collision rejection for symbolic links, and correct free-space accounting.
- **Retain 0.14.1 improvements:** Editing a novel manuscript must not erase scenes, photos, manual locks or timing; Windows Explorer buttons open only approved local folders; verified backup and restore remain available.

## Release gating

The new build is **not approved** until a real hosted Windows runner passes: complete JavaScript and Python tests, low-disk regression, bundled FFmpeg, native NSIS setup.exe build, Windows base install, in-place upgrade, H.264/AAC MP4 export, Edge UI, full backup/restore, original project/media SHA-256 preservation, and uninstall preservation.

After a complete native build succeeds, the exact tested setup.exe bytes are published directly without a source ZIP. A separate Windows runner independently downloads the **published executable**, installs actual 0.14.0 first, upgrades to the new version, checks original project/media hashes, exercises real Edge UI, validates the disk headroom display, WAV import, snapshot verification, restore, and no external network requests.

The unsigned installer may trigger Windows SmartScreen. **The user's personal Windows 11 laptop has not yet been tested**. No real personal media or original manuscripts are included in the public source or installer. Keep a backup on a separate drive before any important upgrade.

[Windows build and tests](.github/workflows/windows-installer-upgrade-0142.yml) · [Independent published binary acceptance](.github/workflows/windows-published-release-acceptance-0142.yml).
