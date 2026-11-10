# Research 0.15.7 — Major-only private artwork generation queue

This is pure offline JS planning, not an image generator and not the Windows app.
It refuses ordinary weather, minor entrances or dialogue as fresh picture beats.
Only already-proposed major changes and missing, unprotected images can become
human-reviewed generator prompts. 12 candidates per chapter by default and
24 maximum; technical same-photo renderer continuations are ignored.
Manual locks, assigned but unavailable media, existing pictures and scene
timing are left untouched. No network request, model download, generated
image or automatic approval is made by the queue.

The local FastSDCPU bridge separately creates unapproved JPEG previews only
with explicit author action. It must stay bound to IPv4 loopback, and be tested
on the intended Windows Intel hardware with an offline-cached, licensed model.
The actual end-user UI/add-on integration remains incomplete.
