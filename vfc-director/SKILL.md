---
name: vfc-director
description: Deterministic short-form video engine for the SEGA Virtua Fighter Crossroads campaign. Measures real media, enforces campaign hard gates as executable code, renders 9:16 / 3:4 masters with mastered audio and verified typography. Use when cutting, reframing, captioning, mastering or QA-ing a campaign clip.
---

# SKILL: deterministic short-form video direction

## When to use this

Any task that turns an authorised long-form trailer into 9:16 (or 3:4) social masters with burned-in
typography, a logo watermark, platform-safe captions and EBU R128 audio — under a campaign whose rules
are hard gates rather than preferences.

## Non-negotiable laws

1. **Decode before you decide.** Every timecode, duration, cut and loudness value must come from a
   file that was actually opened. If a value cannot be measured, it is `null` with the reason —
   never a plausible estimate.
2. **One authorised source.** Footage and audio come from the campaign's own folder. No stock, no
   reuploads, no "close enough" clips. If acquisition fails, log `FAILED_OFFLINE` and stop.
3. **Campaign gates outrank stylistic defaults.** This campaign bans added music, added SFX and AI
   voices, so the engine's sound-design layer is switched off entirely — the master carries only the
   trailer's mix, mastered for loudness.
4. **Never claim what is not on screen.** On-screen text may only describe features present in the
   clip; a trailer is never called "gameplay".
5. **Human judgement is not simulated.** Scroll-stop, feel and syllable sync are returned as
   `requires_human_signoff` with the evidence frame. The machine does not invent scores.

## The pipeline (each step has a machine-checkable exit)

| Step | Command | Exit criterion |
|---|---|---|
| Environment | `python3 -m engine.cli doctor` | `ready: true` — libx264, libass, loudnorm, ebur128, split present |
| Acquire | `python3 -m engine.cli acquire <url> --outdir campaign/assets_raw` | file probes clean; SHA-256 + stream table recorded |
| Analyse | `python3 -m engine.cli analyze <file> --out build/a.json` | shot list, transient map, saliency centroids, framing verdict |
| Plan | `engine.plan.build_clip_plan(...)` | ≥10 s window, gates all true, pan keyframes even px, cues in safe band |
| Render | `python3 -m engine.cli build --spec campaign/clips/CLIPx.json` | 1080×1920, H.264 High 4.2, yuv420p, faststart, −14 LUFS ±0.5, ≤−1 dBTP |
| QA | `engine.qa.verify(...)` | 0 black frames, 0 stuck freezes, 15/15 compliance gates |
| Deliver | `DELIVERY_MANIFEST.json` | SHA-256 of the exact posted file + scorecard + captions |

## Spatial & typographic contract (1080×1920)

| Element | Anchor | Constraint |
|---|---|---|
| Hook | `(540, 430)` | ≤ 2 lines, fitted against the real font file, ≤ 900 px wide |
| Caption | `(540, 1330)` | collarbone band, 1–4 words per burst, ≤ 220 WPM |
| Badge | `(900, 300)` | upper-right, clear of the 140 px right rail |
| Logo | `(48, 292)` | inside the safe band, whole-clip duration |

Reserved platform bands: top 260 px, bottom 420 px, right 140 px. Anything readable must stay out of
them — `qa.safe_zone_overlay()` draws them on a diagnostic frame for inspection.

## Framing decision (measured, not assumed)

A 16:9 master cropped full-height to 9:16 keeps `0.5625 / 1.7778 = 31.6 %` of the horizontal field.
The engine sums the gradient energy that survives each candidate window:

- retention ≥ 0.75 → lock **9:16 full-bleed**;
- else 3:4 **only if** it gains ≥ 0.05 retention → **3:4 glass card** on a blurred mirrored plate;
- else **9:16 punch-pan** that follows the saliency centroid with cubic-eased crop expressions.

## Copy contract (this campaign)

```
A city you've never seen
A story you've never heard
A totally new Virtua Fighter

Experience a rich, cinematic single-player adventure with immersive narrative-driven gameplay, and the series' trademark thrilling VS battles! @VFCROSSROADS
#Ad
```

`@SEGA_West` replaces the tag on YouTube Shorts. The block is verbatim, the tag closes the sentence,
the disclosure sits alone on the next line. `engine.compliance.build_caption()` emits it; the
validator rejects rewording, missing disclosure, wrong tag and hype claims.

## Failure playbook

| Symptom | Cause | Fix |
|---|---|---|
| master duration ≠ plan | a labelled stream consumed twice without `split` | add `split=2` before fan-out |
| master is one held frame | `shortest=1` on a single-frame overlay | `eof_action=repeat` |
| loudness off by >1 LU | pass-1 measurement taken without the mastering prefix | measure the exact chain (`highpass` included) |
| text off the canvas / literal `\N` | character-count wrapping, or escaping the line-break token | measure with the real TTF; escape per line, then join |
