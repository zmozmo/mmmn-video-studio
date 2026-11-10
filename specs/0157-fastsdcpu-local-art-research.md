# MMMN Research 0.15.7 — Real localhost image generation connector, NOT SHIPPED

Goal: create new scenic backgrounds on a 16GB Windows Intel CPU without paid API, but only at truly important story beats, preserving original narration and author-selected images.

- Candidate engine: [rupeshs/fastsdcpu](https://github.com/rupeshs/fastsdcpu) (MIT source code). Its locally running FastAPI service documents `POST /api/generate` returning one base64 JPEG and an error field. This implementation is based on inspected upstream code.
- Local bridge binds outbound **only** to http://127.0.0.1:PORT/api/generate; disables urllib proxies. Does not accept arbitrary remote IPs or URLs.
- Explicit author approval required before each candidate generation; no chapter or imported media is modified.
- One 512×512 JPEG, measured limits, verifies both JPEG magic and Pillow image decoding, unapproved SHA-256 sidecar and fresh collision-safe filenames.
- No silent model installation, private manuscript upload, cloud API, scene timing update, manual visual overwrite, or automatic image approval.
- Local FastSDCPU server itself by default can listen on 0.0.0.0 and may attempt remote model downloads if not cached. It MUST be configured securely and with cached offline weights separately; this bridge does not control the server's networking. Model license is a separate issue from MIT application source license.
- Unit CI exercises a synthetic local loopback HTTPServer **only**. This DOES NOT verify model inference, Intel i7-1185G7 performance, model size, real photo quality, user-facing application UI, or completed Windows release.
- Integrating the actual image engine into the user's 0.15.6 one-file installer requires a separate opted-in addon packaging, a model's specific license checks, and real local Windows CPU inference QA.
