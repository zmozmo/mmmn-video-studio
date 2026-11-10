# MMMN Video Studio Complete Windows one-file installer — 0.15.5

One optional, unsigned setup.exe combines the **exact, separately verified**
MMMN Video Studio 0.15.5 and Burmese Offline CPU Model Pack 0.15.4. Both
source installers are checksum pinned. No download or paid service is needed
at actual installation time. Existing separately downloadable installs
remain available as an alternative.

This is a wrapper around their published EXEs, not an independently rebuilt
application. It needs no admin permissions, Node, Python or source ZIP.

## Mandatory acceptance
- Build one Windows NSIS complete installer.
- Install just that executable in a disposable Windows user account.
- Prove actual independent files: app, FFmpeg, model CLI and pinned Conformer
  weights. Running app self-test must pass.
- Route a real publicly licensed Burmese sample through the *actual
  installed app*, with *actual installed model weights/runtime* to a private
  review-only local SRT, leaving original audio/project/locks intact.
- Full 90-minute prerecorded novel speech accuracy is NOT certified.
- No automatic AI picture generation, private Drive sync or Android runtime.
- Uninstallers remove only binaries, never author manuscript/audio/assets.
- Public release requires binary SHA identical to the one that passed
  full native acceptance; independent *publicly released* EXE QA recommended.

The complete installer is not deemed published until GitHub Actions native
Windows tests and a published release asset are independently verified.
