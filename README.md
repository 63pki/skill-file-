# VFC — Lionel Rafale · Short-Form Production Engine

Deterministic render + QA pipeline for the SEGA *Virtua Fighter Crossroads* clipping
campaign (Lionel Rafale trailer). Campaign compliance is not documentation here — it is
executable code that refuses to render an out-of-spec clip.

**Read [`PRODUCTION_HANDOFF.md`](PRODUCTION_HANDOFF.md) first.** Production is halted at
Phase 2: the official content folder is a Frame.io share and this sandbox's network is
allowlisted, so no source video can be downloaded. Attach the trailer `.mp4` to unblock.

## Quick start

```bash
pip install -r requirements.txt          # pillow (+ imageio-ffmpeg if no system ffmpeg)

# 0. inspect the campaign rules / regenerate validated caption blocks
python -m pipeline.campaign

# 1. Phase 2 — audit an asset (no ffprobe needed)
python -m pipeline.probe assets/raw/lionel_rafale_trailer.mp4

# 2. Phase 5+6 — render a master, then audit it and print the scorecard
python -m pipeline.run \
  --src assets/raw/lionel_rafale_trailer.mp4 \
  --plan plans/clip1.json \
  --aspect 9:16 --mode crop \
  --out out/VFC_RAW01_MASTER_9x16.mp4

# 3. engine self-test (produces PREVIS files — never for posting)
python -m pipeline.smoke_test
```

## What it enforces

| Gate | Where |
|---|---|
| Verbatim caption + correct tag per platform + `#Ad` on its own line | `campaign.validate_caption()` |
| No hype / false claims / banned terms in burned-in text | `campaign.validate_onscreen_text()` |
| Trailer never labeled "gameplay" (but the required copy may say it) | `MISLABEL_TERMS`, screen-only |
| ≤4 words per caption burst | density ceiling in validator |
| Logo on every frame, 302px, top-centre at y=272 | `graphics.logo_plate()` |
| Top 260 / bottom 420 / right 140 px platform clearance | analytic bbox audit in `qa.py` |
| ≥10s runtime, 1080×1920 or 1080×1440, yuv420p | `qa.py` |
| −14.0 ±0.5 LUFS integrated, ≤ −1.0 dBTP | true two-pass loudnorm + ebur128 verify |
| Trailer audio only — no music, no SFX, no AI voice | renderer has no second audio input by design |

`pipeline.run` exits after writing `<out>.qa.json`. There is no skip-the-audit flag.

## Layout

```
pipeline/      campaign.py · probe.py · graphics.py ◆ render.py · qa.py · run.py · hooks.py · smoke_test.py
docs/          CCM.md (signed Phase 1 matrix) · captions.md · hooks.md
plans/         edit-plan schema + example
assets/brand/  official logo (the only licensed asset currently reachable)
assets/raw/    ← drop the trailer here
vendor/fonts/  Montserrat + DejaVu, vendored because the host has no fontconfig
out/           PREVIS engine proof + QA JSON (posting-blocked)
```
