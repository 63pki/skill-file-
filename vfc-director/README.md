# vfc-director

A deterministic short-form video engine, built for the **SEGA / Virtua Fighter Crossroads: Lionel
Rafale** clipping campaign. It is not a prompt template — it decodes real files, measures them, and
refuses to ship anything that breaks a campaign hard gate.

```
engine/     ff.py probe/measure · analyze.py decoded-pixel & decoded-audio analysis
            plan.py render contract · render.py ASS typography + reframing + mastering
            qa.py adversarial audit · compliance.py campaign gates · assets.py acquisition
            cli.py doctor/acquire/analyze/plan/render/qa/captions/slice/build
campaign/   BRIEF_SOURCE.txt · captions.json · PRODUCTION_DOSSIER.md · HOOK_BANK.md
            RUNBOOK.md · PHASE2_ACQUISITION_LOG.(md|json) · clips/
dev/        make_fixture.py (synthetic, non-shippable) · smoke_test.py · SMOKE_RESULTS.json
```

## Status

| Phase | State |
|---|---|
| 1 — campaign deconstruction & compliance gateway | **Complete, signed** — 17 rules captured, 10 enforced as executable gates (the rest are publishing-side) |
| 2 — asset acquisition & integrity audit | **BLOCKED** — Frame.io egress refused from this sandbox; `FAILED_OFFLINE` logged, nothing substituted |
| 3–7 — analysis, blueprint, render, QA, delivery | **Built and executed end-to-end on a labelled synthetic fixture**; every table auto-populates on the real file |

The single open item is the official trailer MP4 (+ logo PNG). Upload it, or run
`campaign/RUNBOOK.md` somewhere with egress to the campaign folder.

## Proven, not asserted

`python3 dev/smoke_test.py` — **49/49 checks pass**, including a full encode:

```
master  10.000 s · 300 frames · 1080x1920 · yuv420p · H.264 High 4.2 · faststart
audio   -14.0 LUFS integrated · -5.4 dBTP true peak · single source stream
QA      0 black frames · 0 stuck freezes · caption anchors inside safe band · <=220 WPM
gates   15/15 mechanical campaign gates · delivery compliance 10.0/10.0
```

Five defects were found and fixed by that suite during the build, each now pinned by an assertion:

1. a filtergraph branch that re-read the **untrimmed** source — 15.0 s out of a 12.0 s plan;
2. a logo overlay with `shortest=1` that truncated the whole master to **one held frame**;
3. loudness measured *before* the 80 Hz high-pass — master landed at **−18.7 LUFS** instead of −14.0;
4. a character-count text fitter that **overflowed the 1080 px canvas** (a caps hook measures 997 px
   at 76 px — ratio 0.69, not the assumed 0.58);
5. `\N` line breaks escaped by the text sanitiser and **rendered literally on screen**.

## Install & run

```bash
pip install -r requirements.txt
python3 -m engine.cli doctor
python3 dev/make_fixture.py build/fixture_16x9.mp4   # synthetic test clip only
python3 dev/smoke_test.py
```

Campaign flow, once the asset is present:

```bash
python3 -m engine.cli analyze campaign/assets_raw/VFC_LIONEL_TRAILER.mp4 --out build/a.json
python3 -m engine.cli build --spec campaign/clips/CLIP1.json
```

## What is deliberately not automated

Scroll-stop rate, pacing feel and syllable sync are human judgements. The QA scorecard returns them
as `requires_human_signoff` with the evidence frame attached — it never prints a fabricated score.
Likewise, no timecode, dialogue line or moment score appears anywhere in this repository for footage
that was never decoded.
