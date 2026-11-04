# PHASE 2 — ACQUISITION LOG (human-readable)

Machine record: `PHASE2_ACQUISITION_LOG.json` (written by `engine/assets.py`)
Probe time: 2026-11-04T23:52:16Z

## Supplied link
```
https://f.io/V0QTpG9W
  └─ resolves (readable as text) →
     https://next.frame.io/share/5cb2f221-b950-4a63-b0d0-c25530ba5a3e/55cafaa1-af3f-44bd-a900-e2e5b12fc74a
     Frame.io project: "SEGA - Virtua Fighter Crossroads" — created by Evan Stanfield
```

## Cascade results

| # | Method | Endpoint | Result |
|---|---|---|---|
| 1 | Direct HTTPS GET | `https://f.io/V0QTpG9W` | `URLError: TLS/SSL connection has been closed (EOF) (_ssl.c:992)` — egress blocked |
| 2 | Dropbox mutation | `dl.dropboxusercontent.com` (control probe) | `SSL_ERROR_SYSCALL` — host unreachable from this image |
| 3 | Google Drive extraction | n/a | no Drive file ID in the brief |
| 4 | yt-dlp | n/a | brief supplies a Frame.io share, not a stream URL; `yt-dlp` absent |
| 5 | Terminal failure protocol | — | **FAILED_OFFLINE**, logged with the real error string |

## Why the engine stops instead of substituting

The brief is explicit:

> USE ONLY THE OFFICIAL CONTENT FOLDER
> Footage or audio from any other source will be rejected.

and

> ❌ Footage or audio not from the official content folder

Any workaround — a reupload, a mirror, a "close enough" clip — violates a hard gate and falsifies
provenance. Per the terminal-failure protocol the engine records the failure, keeps every remaining
gate intact, and waits for the authorised file rather than inventing footage.

## How to clear this in one step

**Option A — upload here (no egress needed):** attach the official trailer MP4 (and the logo PNG if
available) to the conversation. They land in the session workspace; then:

```bash
cd vfc-director
python3 -m engine.cli analyze campaign/assets_raw/<TRAILER>.mp4 \
        --out build/<TRAILER>_analysis.json
```

**Option B — run where Frame.io is reachable:**

```bash
cd vfc-director
python3 -m engine.cli acquire https://f.io/V0QTpG9W \
        --outdir campaign/assets_raw --name VFC_LIONEL_TRAILER.mp4
```

`acquire` writes the same evidence trail, and on success probes the downloaded file (codec,
resolution, fps, duration, audio, SHA-256) so the Phase 2 integrity table fills itself with verified
values instead of guesses.
