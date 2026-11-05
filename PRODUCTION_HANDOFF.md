# VFC — LIONEL RAFALE | EXECUTIVE PRODUCTION HANDOFF
### SEGA / Virtua Fighter Crossroads · Clipping Culture programme · Launch 29 Oct 2026

**Run stamp:** 2026-11-05 · Engine v3.0.0-deterministic
**Delivery Mode:** **MODE 1 — MULTI-FILE DISCRETE ENVIRONMENT**
*(declared per §0.2: this runtime writes arbitrary independent files to disk, so discrete per-clip masters + standalone cover JPEGs are the correct architecture. No single-canvas container is needed; Mode 2 slice commands are therefore not applicable.)*

---

## ⛔ STATUS: PRODUCTION HALTED AT PHASE 2 — SOURCE FOOTAGE UNREACHABLE

Phases 1, 4.1, 5 (engine), 6 (harness) and 7.4 (distribution) are **complete**.
Phases 2→3 and the actual master renders are **blocked by a hard infrastructure
limit, not by a creative or engineering gap.**

**One action unblocks everything: attach the official Lionel Rafale trailer file
(`.mp4`) to this conversation.** It downloads, audits, cuts, renders and QA-passes
in a single command after that (see §8).

I will not fabricate timecodes, dialogue, or a "completed" render. Per Law 1 (Zero
Hallucination) and the Phase 2 Terminal Failure Protocol, the honest state of this
production is recorded below in full.

---

## PHASE 0 — RUNTIME PROBE

| Probe | Result |
|---|---|
| Multi-file write | **YES** → Mode 1 |
| FFmpeg | **ABSENT** at boot → resolved: static build extracted from `imageio-ffmpeg 0.8.1` wheel (ffmpeg n9.0.2, libx264, libass, ebur128, loudnorm, boxblur all present) |
| FFprobe | **ABSENT** → all stream telemetry is parsed from `ffmpeg -i` diagnostics (`pipeline/probe.py`); no field is ever guessed |
| Fonts | **ABSENT** (no fontconfig) → Montserrat + DejaVu vendored into `vendor/fonts/` |
| PIL / Pillow | ABSENT → installed; drives all typography |
| Outbound network | **STRICT ALLOWLIST** — `registry.npmjs.org`, `pypi.org`, `files.pythonhosted.org`, `github.com`, `codeload.github.com`, `api.github.com` only. Everything else returns HTTP `000`. |

That last row is the whole story of this run. **It is the blocker.**

---

## PHASE 1 — CAMPAIGN DECONSTRUCTION & COMPLIANCE GATEWAY ✅ COMPLETE

Full signed matrix: **[`docs/CCM.md`](docs/CCM.md)** — 20 binding constraints, all
Hard Gates, all encoded in `pipeline/campaign.py`.

**Gate check: PASS.** Every rule is locked and machine-enforced. Three caption blocks
(TikTok / Reels / Shorts) are generated and validated clean: [`docs/captions.md`](docs/captions.md).

Two real contradictions in the brief were found and resolved rather than ignored —
both are enforced in code:

1. **"gameplay" is both required and banned.** The verbatim-unalterable caption contains
   *"immersive narrative-driven gameplay"*; the brief separately bans mislabeling a
   trailer as gameplay. Resolution: caption wins (it cannot be edited); the mislabel ban
   is enforced on burned-in text only, via a separate `MISLABEL_TERMS` list.
2. **House playbook vs. campaign law.** The directive's template calls for trending tags,
   an appended engagement question and optional trending-sound pairing. This campaign
   bans all three. Campaign law wins; the engagement question and hashtags move to the
   pinned comment.

---

## PHASE 2 — ASSET ACQUISITION & INTEGRITY AUDIT ❌ BLOCKED

### 2.1 Acquisition audit trail (all four fallback rungs attempted)

| # | Rung | Target | Result |
|---|---|---|---|
| 1 | Direct HTTPS GET | `https://f.io/V0QTpG9W` | **302 → resolved.** It is a **Frame.io** share, not a file host. Resolved project: *"SEGA - Virtua Fighter Crossroads"*, owner *Evan Stanfield*, 1 folder. Share ID `5cb2f221-b950-4a63-b0d0-c25530ba5a3e`, root folder `55cafaa1-af3f-44bd-a900-e2e5b12fc74a` |
| 2 | Dropbox mutation (`?dl=1` / `dl.dropboxusercontent.com`) | — | **N/A** — not a Dropbox URL |
| 3 | Google Drive extraction (`gdown` / `/d/{id}/`) | — | **N/A** — not a Drive URL |
| 4 | YouTube/streaming whitelist (`yt-dlp`) | — | **N/A** — not a streaming URL |
| 5 | Frame.io share API enumeration | `/v4/shares/{id}`, `/v2/shares/{id}` | **404** — Frame.io exposes no public unauthenticated route for this share. The share is a JS single-page app; its asset manifest is delivered by an authenticated GraphQL/browser session, not a static document |
| 6 | Binary egress | `api.frame.io` from the runtime | **HTTP 000** — host not on the sandbox allowlist. Even with a signed download URL in hand, **no video bytes can enter this environment** |

### 2.2 Why rung 6 is terminal

Frame.io asset downloads are CDN-signed URLs on hosts outside the allowlist. There is
no proxy, no `yt-dlp`, no browser, and no permitted egress path that returns binary
media. This is not a retry-able failure; it is an environment boundary.

### 2.3 Phase 2 inventory table — as measured

| Asset ID | Filename | Format/Codec | Resolution | Frame Rate | Duration (s) | Audio Tracks | Ingestion Integrity |
|---|---|---|---|---|---|---|---|
| RAW-01 | *unresolved — Frame.io share contains no publicly enumerable file name* | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | **FAILED_OFFLINE** |
| RAW-02 | *not acquired* | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | **FAILED_OFFLINE** |
| LOGO-01 | `snake_logo_w.png` | PNG / RGBA | 1600×847 | N/A | N/A | N/A | **VERIFIED_ORIGINAL** — alpha intact, content bbox (94,103)→(1510,744), brand accent `#A84828` sampled from 48,553 opaque pixels |

**Total usable raw footage: 0.00 s.** Gate check: **FAIL** (0 continuous seconds of
licensed source). Phases 3, 5, 6 and the Phase 7 manifest cannot legitimately proceed.

---

## PHASE 3 — FOOTAGE ANALYSIS & MOMENT SCORING ⏸ NOT STARTED

Requires RAW-01. Nothing here can be honestly produced without it — any table I wrote
would be invented dialogue with invented timecodes, which Law 1 forbids.

The scorer is specified and ready (weights as mandated): `H 25% · E 20% · C 15% ·
P 15% · V 15% · L 10%`, targeting 8–12 candidate moments, with full transcription,
speech-velocity flags >175 WPM, and the Semantic Climax filter (drop throat-clearing;
keep counter-intuitive truth / conflict / result / catharsis).

**Anti-cannibalization mandate is pre-committed** so the two clips cannot converge:
Clip 1 attacks the **character-reveal** angle (identity/reveal, fast and declarative);
Clip 2 attacks the **rivalry/battle** angle (conflict/status, tension-and-payoff pacing).
Different psychological lever, different rhythm — no shared hook, no shared payoff.

---

## PHASE 4 — ARCHITECTURE & HOOK SHOOTOUT 🟡 PARTIAL (4.1 COMPLETE)

### 4.1 Hook suites — 30 candidates, 100% CCM-screened ✅

Full table: **[`docs/hooks.md`](docs/hooks.md)** (generated by `python -m pipeline.hooks`).
Three angles matching the brief's own approved on-screen directions, 10 hooks each,
spanning five archetypes.

Two decisions worth the director's attention:

- **"Forbidden Secret" is disqualified.** Implying a secret the campaign has not
  disclosed *is* an exaggerated hook — a Hard Gate violation. It is replaced by
  **CURIOSITY GAP**, which asks a question the footage genuinely answers.
- **Every hook is evidence-gated.** The brief requires that on-screen text only mention
  features actually in the clip. So each hook carries a `requires` flag
  (`reveal` / `cielo` / `battle` / `city` / `story`); the plan validator refuses to burn
  a hook whose evidence is not present in that specific clip.

**Scroll-Stop picks (pending footage confirmation):**
· Clip 1 (reveal) → **"CIELO HAS COMPETITION"** — alternates: `A NEW RIVAL`, `WHO IS RAFALE?`
· Clip 2 (rivalry) → **"OUTCLASSED IN THE STREET"** — alternates: `RAFALE VS CIELO`, `TWO FIGHTERS, ONE CITY`

### 4.2 Framing shootout — decision rule locked, verdict pending footage ⏸

The trailer is 16:9. A 9:16 full-bleed crop discards **68% of frame width**; a 3:4 crop
discards 58%. Per §1.6, if the 9:16 crop would truncate >25% of essential subject action,
the deliverable escalates to **3:4 Modern Aesthetic**. Both treatments are already
implemented and QA-clean (see Phase 5), so the verdict is a one-flag switch after a
10-second subject-loss audit on the real frames — not a rebuild.

### 4.3 Beat sheets ⏸

`| Timestamp | Source & Framing | Camera & Scale | Spatial Typography | SFX | Retention Trigger |`
requires real timecodes. The **retention architecture** is locked and footage-independent:

- `0.00–1.20s` Sensory Blitz — 2–4 micro-cuts (0.15–0.25s) of peak-action glimpses
- `1.20s` Deceleration Slam — cut all chaos, land a stable high-clarity close-up
- `1.50s →` Pattern interrupt every 1.5–2.2s (angle cut / 115% punch-in / text pop)
- `80–92%` Payoff delivery
- `100%` Frictionless loop — final syllable and camera vector match Frame 0

**SFX note:** the directive's multi-candidate SFX auditioning (§1.7) is **vetoed by CCM**.
"Use only the audio from the official trailer" is a Hard Gate. Result: zero added SFX,
zero music bed, zero ducking targets — trailer stem only, cleaned and normalised.

---

## PHASE 5 — MASTER COMPOSITING & RENDERING ✅ ENGINE BUILT · ⏸ MASTERS PENDING

The engine is real, working, and validated. Four modules:

| Module | Function |
|---|---|
| `pipeline/probe.py` | ffmpeg-based integrity probe (replaces missing ffprobe) |
| `pipeline/graphics.py` | PIL spatial-typography compositor: glass pills, feathered outlines, letter-tracking, logo watermark + drop shadow, `[STEP nn/nn]` badges |
| `pipeline/render.py` | Temporal assembly → kinetic reframe (9:16 crop / 3:4 rounded glass card) → colour harmonisation → overlay stack → **2-pass EBU R128** → H.264 High L4.2 CRF18 +faststart |
| `pipeline/qa.py` | Phase 6 adversarial auditor |

**Design choices that matter on delivery:**

- **Text never enters the filtergraph.** Captions are rendered as PIL overlay plates and
  flipped by `enable='between(t,a,b)'`. The §1.3 escaping invariant is satisfied *by
  construction* — there is no string that can terminate an FFmpeg script.
- **Safe-zone compliance is analytic, not visual.** Every plate reports its pixel bbox;
  QA asserts clearance arithmetically against top 260 / bottom 420 / right 140.
  This already caught **9 real violations** in the first build (logo pinned 6px into top
  chrome; caption pills 73px into the right rail; two pills 32px into the bottom rail).
  All fixed by clamping the layout budget, then re-rendered and re-audited.
- **Brand accent is sampled from the official logo at runtime** (`#A84828`), never
  hardcoded — no palette drift from the brand mark.
- **Audio:** the CCM-legal single source passes `highpass=80`, then a genuine two-pass
  loudnorm (measure → apply measured values → verify with ebur128).

### 5.1 Engine proof — `out/PREVIS_*.mp4`

Because no campaign footage exists, the engine was validated end-to-end on a generated
16:9 test plate (`pipeline/smoke_test.py`). **These are PREVIS files. They are not
campaign deliverables and must never be posted.** They exist to prove every code path
executes: 9:16 full-bleed and 3:4 rounded-glass-card both render, watermark, caption,
grade, master and pass QA.

---

## PHASE 6 — ADVERSARIAL QA 🟡 HARNESS PASSES · ⏸ MASTERS UNAUDITABLE

Measured on the previs renders (real numbers, real files):

| Metric Evaluated | Strict Threshold | 9:16 previs | 3:4 previs | Status |
|---|---|---|---|---|
| Canvas dimensions | exact | 1080×1920 | 1080×1440 | **PASS** |
| Duration floor | ≥10.0s | 12.0s | 12.0s | **PASS** |
| Integrated loudness | −14.0 ±0.5 LUFS | **−14.1 LUFS** | **−14.1 LUFS** | **PASS** |
| True peak | ≤ −1.0 dBTP | **−9.7 dBTP** | −9.7 dBTP | **PASS** |
| Pixel format | yuv420p | yuv420p | yuv420p | **PASS** |
| Audio stream present | ≥1 | 1 | 1 | **PASS** |
| Black frames | 0 | 0 | 0 | **PASS** |
| Safe-zone clearance | 0 violations | 0 | 0 | **PASS** |
| On-screen text present | ≥1 burst | 4 | 4 | **PASS** |
| Campaign text compliance | 0 violations | 0 | 0 | **PASS** |

Diagnostic frames (Frame 0 / 1.0s / 50% / 85% / end) are extracted to `out/qa_frames/`
on every run. **These scores do not transfer to the masters** — the Hook Stop-Rate,
Temporal Pacing and Caption Syllable-Sync rows in the Phase 6 scorecard require real
dialogue and cannot be scored against a test pattern.

---

## PHASE 7 — DELIVERABLES

### 7.1 Asset manifest

| Deliverable | Filename | Status |
|---|---|---|
| Clip 1 master | `VFC_RAW01_MASTER_9x16.mp4` *(or `_3x4`)* | ⏸ **PENDING** — blocked on RAW-01 |
| Clip 2 master | `VFC_RAW02_MASTER_9x16.mp4` | ⏸ **PENDING** |
| Cover 1 | `VFC_RAW01_COVER.jpg` | ⏸ **PENDING** |
| Cover 2 | `VFC_RAW02_COVER.jpg` | ⏸ **PENDING** |
| Engine proof | `out/PREVIS_pipeline_9x16.mp4`, `out/PREVIS_pipeline_3x4.mp4` | ✅ **DELIVERED** (not for posting) |
| Locked captions | `docs/captions.md` | ✅ **DELIVERED** |
| Hook suites | `docs/hooks.md` | ✅ **DELIVERED** |
| Compliance matrix | `docs/CCM.md` | ✅ **DELIVERED** |

### 7.2 Source provenance & beat log ⏸ Pending RAW-01.

### 7.3 Typography & alternates ✅

- Active hook (Clip 1): **CIELO HAS COMPETITION** · alternates: `A NEW RIVAL` / `WHO IS RAFALE?`
- Active hook (Clip 2): **OUTCLASSED IN THE STREET** · alternates: `RAFALE VS CIELO` / `TWO FIGHTERS, ONE CITY`
- Type system: Montserrat ExtraBold, uppercase, `size = 8.2% canvas width`, tracking +2,
  3px feathered `#000` outline over a `rgba(15,15,15,0.75)` glass pill with a `#A84828`
  accent spine. Max 4 words per burst (≤220 WPM reading density).

### 7.4 Social distribution metadata ✅ COMPLETE

Exact blocks (generated, validated): **[`docs/captions.md`](docs/captions.md)**

- **TikTok** — the locked caption + `@VFCROSSROADS` + `#Ad`. *No additional hashtags, no
  appended question* (would alter the verbatim caption).
- **Instagram Reels** — identical block; line breaks already mirror the required stanza
  layout. Audio pairing recommendation: **none** — trending-sound pairing is prohibited.
- **YouTube Shorts** — same block with `@SEGA_West`, plus title
  `Virtua Fighter Crossroads: Lionel Rafale Trailer` (48 chars, under the 60-char CTR ceiling).

**Engagement tactics, relocated to stay compliant:**
- **Pinned comment (TikTok/Reels):** *"A new fighter just walked into Vilasapara. Who do
  you want to see him fight next? 👀"* — this is where the hook question and any tags live,
  never in the caption.
- **No CTA stickers over burned-in text** — keep the bottom 420px free.
- **Schedule:** 2 posts ≥24h apart, different angles (reveal, then rivalry), so neither
  cannibalises the other's cold-start distribution.

### 7.5 Executive directorial brief ✅

**Algorithmic thesis.** Short-form retention is won in the first 1.2 seconds and again at
the loop seam. The mandated architecture exploits both: a sensory blitz of 0.15–0.25s
micro-cuts converts a scroll into a pause before the viewer can form the judgement
"advertisement"; the 1.20s deceleration slam then pays that pause off with one clean,
legible image. From there, a pattern interrupt every 1.5–2.2s sits just inside the human
attention-decay window. The loop is engineered, not hoped for: the final syllable and
camera vector are matched to Frame 0 so the replay is seamless and the video accrues
watch-time *above* 100% — the single strongest signal these three feeds rank on.

**Platform audio strategy.** There is only one legal option here, and it is also the
right one: the trailer stem, mastered to −14 LUFS / −1 dBTP, plays standalone. Do **not**
blend it under a trending sound — that both violates the campaign and destroys the
trailer mix. The upside is consistency: identical audio across TikTok, Reels and Shorts
means the mixdown is tuned once.

**Compliance as a distribution asset.** The clip is engineered to survive audit: logo
present in every frame, safe zones clear, `#Ad` on its own line, caption byte-exact, no
added audio. Rejections in clipping programmes are overwhelmingly clerical — missing
logo, altered caption, hidden disclosure — not creative. Every one of those failure modes
is now a machine check that fails the render before it reaches a feed.

---

## 8. THE SINGLE COMMAND THAT FINISHES THIS

Drop the official trailer in as `assets/raw/lionel_rafale_trailer.mp4`, then:

```bash
pip install -r requirements.txt          # pillow
python -m pipeline.probe assets/raw/lionel_rafale_trailer.mp4   # Phase 2 audit

# Phase 3 (transcribe + score) → Phase 4 (beat sheet) → Phase 5/6:
python -m pipeline.run \
  --src assets/raw/lionel_rafale_trailer.mp4 \
  --plan plans/clip1.json \
  --aspect 9:16 --mode crop \
  --out out/VFC_RAW01_MASTER_9x16.mp4
```

`pipeline.run` renders, then audits, then prints the Phase 6 scorecard and writes
`*.qa.json`. A non-passing score means rebuild — there is no override flag.

---

### Repository map

```
pipeline/
  campaign.py    CCM constants + hard-gate validators   ← single source of truth
  probe.py       media integrity probe (ffprobe replacement)
  graphics.py    PIL typography / watermark / badges
  render.py      compositing + 2-pass audio master
  qa.py          Phase 6 adversarial auditor
  run.py         orchestrator: render → audit → scorecard
  hooks.py       30-hook generator + evidence gating
  smoke_test.py  previs engine validation
docs/
  CCM.md         signed Phase 1 compliance matrix
  captions.md    locked, validated caption blocks
  hooks.md       screened hook suites
assets/brand/    official logo
vendor/fonts/    Montserrat, DejaVu (vendored — no fontconfig needed)
```
