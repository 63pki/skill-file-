# RUNBOOK — from a dropped file to a shippable post

## 0. One-time setup

```bash
pip install -r requirements.txt      # imageio-ffmpeg (bundles a static ffmpeg), numpy, pillow
python3 -m engine.cli doctor         # must print ready: true
```

`doctor` is not decoration: it asserts that the build actually carries libx264, libass, loudnorm,
ebur128, split, overlay and boxblur. A build without them fails here, not 40 minutes into a render.

## 1. Acquire the official asset

```bash
# where Frame.io is reachable
python3 -m engine.cli acquire https://f.io/V0QTpG9W \
        --outdir campaign/assets_raw --name VFC_LIONEL_TRAILER.mp4
```
…or drop the trailer MP4 into `campaign/assets_raw/` directly. Never substitute another source.

## 2. Validate the logo

Export the official PNG from the same folder into `campaign/assets_raw/VFC_OFFICIAL_LOGO.png`.
Reject any logo that is not the campaign's own file — the watermark is a hard gate.

## 3. Analyse the trailer (real measurements, whole file)

```bash
python3 -m engine.cli analyze campaign/assets_raw/VFC_LIONEL_TRAILER.mp4 \
        --out build/trailer_analysis.json
```
Produces: probe table, shot boundaries, audio transients + tempo + band split, saliency centroids,
cover candidates, and the framing shootout recommendation.

## 4. Choose the two moments

Read the shot list and the transient map, then write the two clip specs (copy
`campaign/clips/CLIP_SPEC_TEMPLATE.json`). Rules:

- **≥ 10.0 s** each — the engine refuses anything shorter.
- The two clips must target different psychological angles (e.g. reveal vs rivalry) and different
  pacing profiles. Same-scene twins cannibalise each other's reach.
- Every hook/caption must be justified by a `C-*` condition you have actually seen in the frames
  (`campaign/HOOK_BANK.md`).

## 5. Build

```bash
python3 -m engine.cli build --spec campaign/clips/CLIP1.json
python3 -m engine.cli build --spec campaign/clips/CLIP2.json
```

`build` runs analyse → plan → render → QA → cover → caption files → `DELIVERY_MANIFEST.json`.
Exit codes: `0` clean, `5` compliance gates refused the plan, `6` delivery compliance failed.

Typical timings on this image (2 vCPU): 12 s master at `--preset slow` ≈ 90–150 s.

## 6. Inspect before publishing (mandatory)

Open, in this order:

1. `build/<CLIP_ID>/qa/frame_t0.png` — is the first frame a real stop-scroll frame?
2. `.../qa/frame_t50.png`, `.../qa/frame_t85.png` — pacing and pattern interrupts.
3. `.../qa/frame_cover_safezone.png` — the red bands are the platform UI zones; nothing readable may
   sit inside them.
4. `<CLIP_ID>_COVER.jpg` — eyes open, high expression, sharp.
5. Watch the master once with sound, once muted. Captions must carry the story muted.

Anything that fails here is a re-edit, not a re-render: fix the spec, rebuild.

## 7. Publish (campaign rules, not preferences)

| Rule | Value |
|---|---|
| Caption | `build/<CLIP_ID>/captions/caption_<platform>.txt` — verbatim, no edits |
| Tag | `@VFCROSSROADS` (TikTok/IG) · `@SEGA_West` (YouTube Shorts) |
| FTC | `#Ad` on its own line, immediately after the tag line |
| Platforms | TikTok, Instagram Reels, YouTube Shorts |
| Minimum lifetime | 30 days, likes visible |
| Engagement floor | ≥ 0.20 % (1,000 views → ≥ 2 likes) |
| Audience | ≥ 35 % combined US + Canada (page or post) |
| Music | none added — trailer audio only |
| Reposts | same video max 5 times, never across multiple accounts |
| Paid promotion | forbidden — permanent ban |

## 8. Archive

Keep `DELIVERY_MANIFEST.json` next to the master. It carries the SHA-256 of the exact file posted,
the measured loudness, the QA scorecard and the compliance result — the audit trail if a post is
ever questioned.

## Dual-nest fallback (single-canvas environments)

If a session can only emit one 1920×1080 file, assemble the side-by-side master and slice it back
losslessly:

```bash
python3 -m engine.cli slice --canvas build/DUAL_MASTER_1920x1080.mp4 --mode 9x16
ffmpeg -i build/DUAL_MASTER_1920x1080.mp4 -filter:v "crop=608:1080:176:0"  -c:a copy clip_1.mp4
ffmpeg -i build/DUAL_MASTER_1920x1080.mp4 -filter:v "crop=608:1080:1136:0" -c:a copy clip_2.mp4
```
