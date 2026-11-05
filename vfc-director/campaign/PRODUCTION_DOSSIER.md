# PRODUCTION DOSSIER — SEGA / Virtua Fighter Crossroads: Lionel Rafale
**Campaign launch:** 2026-10-29 · **Brief ingested:** 2026-11-04 · **Engine:** vfc-director 1.0.0
**Delivery mode:** MODE 1 — multi-file discrete (this environment writes independent files)
**Execution engine:** FFmpeg n9.0.2 (static, libx264 + libass + loudnorm + ebur128), driven by
`engine/` with byte-level verification at every gate.

> **Status in one line:** Phase 1 is complete and signed. Phase 2 is half-cleared — the **official
> logo is in hand and verified** (1600×847 RGBA, sha256 pinned, compositing at 5.57:1 worst-case
> contrast), while the **trailer itself is still refused at the network boundary** and the campaign
> forbids every substitute source. The full render chain (Phases 3–7) is built, executed and
> verified against a **synthetic fixture**, and will populate every remaining table the moment the
> official file is present. No timecode, dialogue line, or score in this dossier is invented.

---

## PHASE 1 — CAMPAIGN DECONSTRUCTION & COMPLIANCE GATEWAY

Source brief: `campaign/BRIEF_SOURCE.txt` (verbatim copy of the supplied document).
Machine-enforced subset: `engine/compliance.py`, canonical strings in `campaign/captions.json`.

| Parameter Category | Extracted Guideline Specification | Operational Boundary / Threshold | Enforcement Level |
|---|---|---|---|
| Mandatory Mentions (caption) | `A city you've never seen` / `A story you've never heard` / `A totally new Virtua Fighter` — exact, word for word, each on its own line | Verbatim string match; no shortening, no rewording | **Hard Gate** — `validate_caption()` fails the post |
| Mandatory Mentions (body) | `Experience a rich, cinematic single-player adventure with immersive narrative-driven gameplay, and the series' trademark thrilling VS battles!` + account tag immediately after | Verbatim sentence, tag as the last token of that line | **Hard Gate** |
| Account Tag | `@VFCROSSROADS` (TikTok + Instagram) · `@SEGA_West` (YouTube Shorts) | Exact handle per platform | **Hard Gate** |
| FTC Disclosure | `#Ad` / `#Advertisement` / `#Sponsored` — one required, on its own line, immediately after the tag line | Line index must equal tag line + 1 | **Hard Gate** |
| Optional approved copy | "A mysterious young martial artist named Lionel Rafale…" | May be added; required block must remain verbatim | Advisory |
| Prohibited content | Political, race/gender, NSFW, violent, racist/homophobic/sexual, controversy, rage-bait, hate-bait | Zero tolerance; instant ban on the protected categories | **Hard Gate** |
| Prohibited claims | False/made-up claims, stats, dates; exaggerated hooks; mislabeling a trailer as "gameplay" | Creative copy linted against `BANNED_CLAIM_PATTERNS` + "gameplay" mislabel check | **Hard Gate** |
| Audio restrictions | **No added music.** Only the audio from the official trailer. No AI voices/narration/clones | Engine renders exactly one audio stream, sourced from the trailer; `added_music`, `added_sfx`, `ai_voice` are hard-coded `false` in every plan | **Hard Gate** — `validate_delivery()` |
| Visual / Brand specs | Official logo on **every** clip | Logo PNG overlaid at (48, 292) inside the safe band, `eof_action=repeat` for full duration | **Hard Gate** |
| On-screen text | Required on every post; wording flexible; must describe only features actually in the clip | Hook + timed captions authored per clip from the verified shot list | **Hard Gate** |
| Duration bounds | Video must be **≥ 10 seconds** | `build_clip_plan()` raises below 10.0 s; QA re-verifies the encoded file | **Hard Gate** |
| Source whitelist | Footage **and** audio from the official content folder only | Single-source provenance; no stock, no memes, no third-party clips | **Hard Gate** |
| Language | English content only | Copy lint + English-only source | **Hard Gate** |
| Posting hygiene | ≥ 30 days live, visible likes, ≥ 0.20% engagement, ≥ 35% US+CA audience, ≤ 5 reposts, no paid promotion, no story boosting | Publishing constraints — recorded in `RUNBOOK.md` §Publishing | Operative |
| Watermark / page rule | No dedicated page needed; audience threshold may be met by page or post (OAuth-verified) | Account-level, outside render scope | Operative |

**Conflict resolution logged.** The engine's default sound-design layer (auditioned SFX beds,
impacts, risers) is **disabled** for this campaign: §AUDIO of the brief bans all added audio and the
hard gate outranks the engine's stylistic defaults. Music beds, AI narration and TTS are likewise
off. The master therefore carries the trailer's own mix, mastered only for loudness.

**Gate check — SIGNED.** All Phase 1 rules are locked into code, not prose. `engine.compliance`
refuses to mark a delivery complete while any hard gate is open, and `dev/smoke_test.py` proves the
refusals fire (reworded caption, missing `#Ad`, wrong-platform tag, hype claim, sub-10 s window).

---

## PHASE 2 — ASSET ACQUISITION & INTEGRITY AUDIT

### 2.1 What the campaign supplied
| Item | Value | Resolution |
|---|---|---|
| Content folder | `https://f.io/V0QTpG9W` | Redirects to Frame.io share `next.frame.io/share/5cb2f221-b950-4a63-b0d0-c25530ba5a3e` — project **"SEGA - Virtua Fighter Crossroads"**, created by *Evan Stanfield*, containing the official Lionel Rafale trailer + logo |
| Logo file | "Download the official logo (PNG)" — inside the same folder | Not separately addressable without the folder |
| Captions | `campaign/captions.json` | Extracted verbatim ✔ |

### 2.2 Acquisition cascade — actual results
Full machine log: `campaign/PHASE2_ACQUISITION_LOG.json`.

| Step | Method | Result |
|---|---|---|
| 1 | Direct HTTPS GET `https://f.io/V0QTpG9W` | `URLError: TLS/SSL connection has been closed (EOF)` — egress blocked at the sandbox boundary |
| 2 | Dropbox mutation (`?dl=1`, `dl.dropboxusercontent.com`) | Not applicable — the link is not Dropbox; direct probe to `dl.dropboxusercontent.com` also returns `SSL_ERROR_SYSCALL` |
| 3 | Google Drive extraction | Not applicable — no Drive file ID in the supplied link |
| 4 | YouTube / streaming whitelist (`yt-dlp`) | Not applicable — the campaign supplied a Frame.io share, not a stream URL; `yt-dlp` is not installed in this image |
| 5 | **Terminal failure protocol** | `FAILED_OFFLINE` recorded with the real error string. Not substituted, not simulated |

**Why this cannot be worked around:** the campaign states *"USE ONLY THE OFFICIAL CONTENT FOLDER.
Footage or audio from any other source will be rejected."* Sourcing the trailer anywhere else would
violate a hard gate and misrepresent provenance, so the engine stops here rather than improvise
footage. The iframe share page is readable as text (title/creator confirmed above), but the media
binaries are behind the blocked host.

### 2.3 Integrity table
| Asset ID | Filename | Format/Codec | Resolution | Frame Rate | Duration | Audio | Ingestion Integrity |
|---|---|---|---|---|---|---|---|
| RAW-01 | *(pending)* `VFC_LIONEL_TRAILER.mp4` | — | — | — | — | — | **FAILED_OFFLINE** |
| RAW-02 | `VFC_OFFICIAL_LOGO.png` | PNG / RGBA (straight alpha) | 1600×847 | n/a (still) | n/a | none | **VERIFIED_ORIGINAL** · 129,408 B · sha256 `34b571be…54cf` · alpha 57.5 % fully transparent |

These rows are left blank **by design**. Filling them with plausible values is exactly the
fabrication the campaign (and the directive's anti-hallucination law) forbids. `engine/probe.py`
populates the entire table automatically from `ffmpeg` on the real file — the synthetic fixture in
§2.4 shows the exact output shape.

### 2.4 Chain validation on a clearly-labelled synthetic fixture
To prove the chain executes before real footage arrives, a synthetic 1920×1080 / 15.0 s fixture
(`build/fixture_16x9.mp4`, three moving plates, pulsed 55 Hz bed) was pushed through the identical
pipeline. **It is not campaign footage and cannot be shipped.**

| Asset ID | Filename | Format/Codec | Resolution | Frame Rate | Duration | Audio Tracks | Ingestion Integrity |
|---|---|---|---|---|---|---|---|
| SYN-00 | fixture_16x9.mp4 | H.264 / AAC | 1920×1080 | 30.0 | 15.000 s | Stereo 48 kHz | SYNTHETIC_TEST_FIXTURE (non-shippable) |

The official logo has since been supplied directly by the campaign owner and is now installed at
`campaign/assets_raw/VFC_OFFICIAL_LOGO.png` (tracked, so renders are reproducible). It is a true
RGBA file with genuine transparency — corners at alpha 0, 57.5 % of pixels fully transparent — so it
composites without a black box. A soft dark plate (`SCRIM_ALPHA 158/255`) is generated under it,
and the watermark's legibility is now a measured gate rather than an opinion:

| Sample | Plate luminance | Contrast vs white | Verdict |
|---|---|---|---|
| t = 0.24 s (brightest plate) | 0.1384 | **5.57 : 1** | pass (≥ 4.5) |
| t = 3.00 s | 0.1377 | 5.59 : 1 | pass |
| t = 6.00 s | 0.0058 | 18.83 : 1 | pass |
| t = 9.00 s | 0.0665 | 9.01 : 1 | pass |
| t = 11.76 s | 0.0754 | 8.37 : 1 | pass |

**Gate check:** raw-duration confirmed by decoding (450 frames). Final renders cut directly from the
original file at CRF 18 — no intermediate transcode exists anywhere in the graph.

---

## PHASE 3 — FOOTAGE ANALYSIS & MOMENT SCORING

Status: **AWAITING_SOURCE.** The analysis pass itself is implemented and measured, not sketched:

| Measurement | Implementation | Verified on fixture |
|---|---|---|
| Shot boundaries | `select='gt(scene,0.30)',metadata=print` (real frame differences) | 3 cuts detected across 3 plates |
| Audio onsets / transients | 16 kHz decode → 512-pt STFT → positive spectral flux → adaptive peak pick, 80 ms collapse | transients + tempo estimate produced |
| Dynamic range / band split | RMS envelope (10 ms hop), sub/low/mid/high energy shares | produced |
| Saliency centroid (x,y) per frame | 6 fps decode at 192×108, gradient-magnitude centroid | produced, drives pan keyframes |
| Sharpness / exposure | gradient energy + mean luma per sampled frame | produced, drives cover selection |
| Framing shootout | saliency-energy retention inside each candidate crop window | 9:16 keeps 31.6% of the horizontal field by geometry; retention measured per frame |

**Moment scoring (weights H25/E20/C15/P15/V15/L10) cannot be populated without the transcript and
the pictures.** The scoring engine is a deterministic table applied to the verified shot list; the
six vectors will be scored from the real trailer in one pass — `python3 -m engine.cli analyze …`
followed by the candidate log — the moment the file lands. Any number written here today would be
invented.

---

## PHASE 4 — BLUEPRINT & FRAMING SHOOTOUT

**Framing decision is computed, not assumed.** For a 16:9 master, a full-height 9:16 crop keeps
`0.5625 / 1.7778 = 31.6%` of the horizontal field — measured, not estimated. The engine then sums
the gradient energy that survives each candidate window:

- `9x16_full_bleed` — retention ≥ 0.75 (subject truncation < 25%) → **lock 9:16**
- otherwise `3x4_glass_card` only if it gains ≥ 0.05 retention
- otherwise `9x16_punch_pan`, which follows the subject instead of cropping blind

On the synthetic fixture the audit returned `3x4_glass_card` (9:16 retention 0.378 vs 3:4 0.521,
delta +0.143) and the master rendered with the blurred-plate glass card — the decision path is live.

Hook candidates and the second-by-second beat sheet are authored in `campaign/HOOK_BANK.md`, where
every hook is a factual claim tied to a content condition that must be visually confirmed in the
clip before it may be burned in.

---

## PHASE 5 — COMPOSITING, KEYFRAMING & RENDERING

Executed end-to-end on the fixture (identical code path to the real deliverable):

- Eased pan: cubic ease-in-out keyframes compiled to a single FFmpeg crop expression, snapped to
  even pixels for YUV420p validity (verified: every keyframe `x % 2 == 0`).
- Reframing: 9:16 full-bleed / 3:4 glass card with blurred, brightness-damped mirrored plate
  (`boxblur=30:5`, `eq=brightness=-0.35`) / 9:16 punch-pan with an evaluated scale ramp.
- Typography: libass, font-fit measured against the actual `DejaVuSans-Bold.ttf` (a 19-character
  caps hook measured 997 px at 76 px, ratio 0.69 — the old character-count fitter overflowed the
  canvas and was replaced), glass-dark outline for >4.5:1 contrast, spatial anchors in the
  collarbone zone and upper-centre, 1–4 words per burst, 220 WPM ceiling enforced.
- Logo: top-left at (48, 286), 220×116 from the real 1600×847 file, on a generated 158/255 scrim,
  `eof_action=repeat` for the full duration.
- Audio: source only → `highpass=f=80` → two-pass `loudnorm`.
- Encode: H.264 High 4.2, yuv420p, CRF 18, `+faststart`, AAC 192 kbps / 48 kHz.

**Measured on the fixture master:** 10.000 s, 300 frames, 1080×1920, yuv420p, H.264 High, faststart,
**−14.0 LUFS** integrated, **−5.4 dBTP**, one audio stream, zero black frames, zero stuck freezes,
worst-case watermark contrast **5.57 : 1**.

---

## PHASE 6 — ADVERSARIAL QA SCORECARD

Automated telemetry is real. Human-judgement rows are **explicitly marked**, never scored by the
machine (`qa.scorecard()` returns `requires_human_signoff` with the exported evidence frame).

| Metric Evaluated | Strict Threshold | Fixture Master (measured) | Real Clip 1 | Real Clip 2 | Status |
|---|---|---|---|---|---|
| Hook Stop-Rate Viability | ≥ 9.0 / 10.0 | *requires human sign-off* — frame 0 exported | — | — | PENDING (asset blocked) |
| Temporal Pacing & Rhythm | ≥ 9.0 / 10.0 | *requires human sign-off* — 50%/85% frames exported | — | — | PENDING (asset blocked) |
| Caption Precision & Safe Zone | 10.0 / 10.0 | **10.0** — anchors inside safe band, ≤220 WPM, pixel-fit verified | — | — | PASS (mechanism proven) |
| Audio Engineering & Loudness | ≥ 9.5 / 10.0 @ −14 LUFS | **10.0** — −14.0 LUFS, −5.4 dBTP, single source stream | — | — | PASS (mechanism proven) |
| Campaign Compliance Matrix | 10.0 / 10.0 | **10.0** — 16/16 mechanical gates | — | — | PASS (mechanism proven) |
| Logo legibility (WCAG) | ≥ 4.5 : 1 | **5.57 : 1** worst case, real logo | — | — | PASS (official logo verified) |
| Syllable-sync / caption accuracy | 0 drift | *requires transcription or human* — not fabricated | — | — | PENDING |

Fixture suite: **53 / 53 checks pass** (`dev/SMOKE_RESULTS.json`).

---

## PHASE 7 — DELIVERABLES

| Deliverable | Path | State |
|---|---|---|
| Clip 1 master (9:16 or 3:4) | `build/<CLIP_ID>/<CLIP_ID>_MASTER_1080x1920.mp4` | Awaiting source |
| Clip 2 master | same, separate `clip_id` | Awaiting source |
| Cover frame 1 / 2 | `<CLIP_ID>_COVER.jpg` at the sharpest, best-exposed real frame | Awaiting source |
| Captions (3 platforms, validated) | `build/<CLIP_ID>/captions/caption_*.txt` | **Ready and validated** |
| Delivery manifest (SHA-256, QA, gates) | `build/<CLIP_ID>/DELIVERY_MANIFEST.json` | Generated automatically |
| Dual-nest canvas + lossless slice commands | `python3 -m engine.cli slice --canvas …` | Available if a single-canvas env is used |

**Single blocker:** the official trailer MP4. The logo is already installed and gated; supply the
trailer (upload it here, or run `campaign/RUNBOOK.md` where Frame.io is reachable) and everything
downstream is one command.
