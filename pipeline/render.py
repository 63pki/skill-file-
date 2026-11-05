"""
Master compositing + render engine (FFmpeg, CPU only).

Pipeline per clip
-----------------
 1. Temporal assembly   trim/concat segments, optional J/L offset on audio
 2. Kinetic reframe     cover-crop to 9:16 or 3:4 (or glass-card treatment)
 3. Colour harmonisation base grade, optional shock-freeze colour snap
 4. Overlay stack       official logo watermark + spatial caption plates
 5. Audio master        high-pass 80Hz, 2-pass EBU R128 to -14 LUFS / -1 dBTP
 6. Container           H.264 High L4.2, yuv420p, CRF18, +faststart

Audio law (campaign hard gate): the ONLY permitted audio is the official
trailer's own audio. No music bed, no SFX layer, no AI voice. This module
therefore never mixes a second audio source — it only cleans and normalises
the trailer stem.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from . import campaign as C
from . import graphics as G

FFMPEG = shutil.which("ffmpeg") or "/home/user/bin/ffmpeg"
CANVAS = {"9:16": (1080, 1920), "3:4": (1080, 1440)}
CARD_MASK_IDX = 1


def run(args: list[str], label: str = "", t_limit: float | None = None) -> str:
    if t_limit:
        args = args[:-1] + ["-t", f"{t_limit:.3f}", args[-1]]
    proc = subprocess.run(args, capture_output=True, text=True, timeout=3600)
    if proc.returncode != 0:
        raise RuntimeError(f"FFMPEG FAILED [{label}]\n{' '.join(args)}\n{proc.stderr[-4000:]}")
    return proc.stderr


# ------------------------------------------------------------------ reframe
def reframe_chain(aspect: str, mode: str = "crop") -> tuple[str, str, int, int]:
    """Return (filtergraph_body, out_label, W, H)."""
    W, H = CANVAS[aspect]
    if mode == "card" and aspect == "3:4":
        cw, ch = 972, 1296
        body = (
            f"split=2[bg][fg];"
            f"[bg]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
            f"boxblur=30:5,eq=brightness=-0.35:saturation=1.1[bgb];"
            f"[fg]scale={cw}:{ch}:force_original_aspect_ratio=increase,crop={cw}:{ch}[fgc];"
            f"[fgc][{CARD_MASK_IDX}:v]alphamerge[fgm];"
            f"[bgb][fgm]overlay=(W-w)/2:(H-h)/2"
        )
        return body, "vrf", W, H
    body = (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},fps=30,setsar=1")
    return body, "vrf", W, H


def card_mask(path: Path, w: int, h: int, radius: int = 32) -> Path:
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    m.convert("RGBA").save(path)
    return path


# ------------------------------------------------------------------ audio
def loudness_measure(path: Path) -> dict:
    args = [FFMPEG, "-hide_banner", "-nostats", "-i", str(path),
            "-af", "loudnorm=I=-14:TP=-1:LRA=11:print_format=json", "-f", "null", "-"]
    err = run(args, "loudnorm measure")
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", err, re.S)
    if not m:
        raise RuntimeError("loudnorm: no JSON payload in ffmpeg output")
    return json.loads(m.group(0))


# ------------------------------------------------------------------ main
def render(src: Path, plan: dict, out: Path, aspect: str = "9:16",
           mode: str = "crop", verbose: bool = True) -> dict:
    out.parent.mkdir(parents=True, exist_ok=True)
    work = out.parent / "_work"
    work.mkdir(exist_ok=True)
    W, H = CANVAS[aspect]

    # ---- 1. temporal assembly -------------------------------------------
    segs = plan.get("segments") or [[0.0, None]]
    parts_v, parts_a = [], []
    for i, (s, e) in enumerate(segs):
        e_ = "" if e is None else f":end={e}"
        parts_v.append(f"[0:v]trim=start={s}{e_},setpts=PTS-STARTPTS[sv{i}]")
        parts_a.append(f"[0:a]atrim=start={s}{e_},asetpts=PTS-STARTPTS[sa{i}]")
    n = len(segs)
    concat = ("[sv" + "][sv".join(str(i) for i in range(n)) + "]"
              + "[sa" + "][sa".join(str(i) for i in range(n)) + "]"
              + f"concat=n={n}:v=1:a=1[vcat][acat]")

    # ---- 2+3. reframe + grade -------------------------------------------
    rf_body, rf_lbl, W, H = reframe_chain(aspect, mode)
    grade = "eq=contrast=1.05:saturation=1.07:brightness=0.012"
    snap = plan.get("color_snap")
    if snap:
        a, b = snap
        grade += (f",eq=saturation=if(between(t\\,{a}\\,{b})\\,0.2\\,1)"
                  f":contrast=if(between(t\\,{a}\\,{b})\\,1.15\\,1)")

    chain = parts_v + parts_a + [concat, f"[vcat]{rf_body},{grade}[{rf_lbl}]"]

    # ---- 4. overlay stack ------------------------------------------------
    inputs = ["-i", str(src)]
    extra_inputs: list[str] = []          # looped stills appended after src
    if mode == "card" and aspect == "3:4":
        extra_inputs.append(str(card_mask(work / "card_mask.png", 972, 1296)))

    overlay_defs: list[tuple[Path, int, int, str | None]] = []
    if plan.get("logo", True):
        logo_w = int(W * C.LOGO_WIDTH_RATIO)
        plate, bb = G.logo_plate(logo_w, W)
        lp = work / "logo_plate.png"
        plate.save(lp)
        overlay_defs.append((lp, bb["x"], bb["y"], None))

    for idx, cap in enumerate(plan.get("captions", [])):
        plate, bb = G.caption_plate(cap["text"], W, H,
                                    anchor_y=cap.get("y"))
        cp = work / f"cap_{idx:02d}.png"
        plate.save(cp)
        overlay_defs.append((cp, 0, 0, f"between(t,{cap['t0']},{cap['t1']})"))

    for idx, bd in enumerate(plan.get("badges", [])):
        plate, bb = G.step_badge(bd["i"], bd["n"], W)
        bp = work / f"badge_{idx:02d}.png"
        plate.save(bp)
        overlay_defs.append((bp, 0, 0, f"between(t,{bd['t0']},{bd['t1']})"))

    cur = rf_lbl
    for k, (p, x, y, enable) in enumerate(overlay_defs):
        extra_inputs.append(str(p))
        vin = 1 + len(extra_inputs) - 1     # src is input 0
        opts = f"x={x}:y={y}:format=auto:shortest=1"
        if enable:
            opts += f":enable='{enable}'"
        nxt = f"ov{k}"
        chain.append(f"[{cur}][{vin}:v]overlay={opts}[{nxt}]")
        cur = nxt
    chain.append(f"[{cur}]format=yuv420p[vout]")

    for e in extra_inputs:
        inputs += ["-loop", "1", "-i", e]

    premaster = work / "premaster.mp4"
    # Total programme duration == sum of segment lengths. This is a hard upper
    # bound for the overlay chain, which otherwise stays alive forever on the
    # looped still-image inputs.
    t_total = sum((e - s_) if e is not None else 3600.0 for s_, e in segs)
    fc = ";".join(chain)
    (work / "filtergraph.txt").write_text(fc)

    run([FFMPEG, "-y", "-hide_banner", "-nostats", *inputs,
         "-filter_complex", fc, "-map", "[vout]", "-map", "[acat]",
         "-c:v", C.ENCODE["vcodec"], "-profile:v", C.ENCODE["profile"],
         "-level", C.ENCODE["level"], "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
         "-movflags", "+faststart", str(premaster)], "premaster",
        t_limit=t_total)

    # ---- 5. two-pass EBU R128 audio master -------------------------------
    meas = loudness_measure(premaster)
    af = (
        "highpass=f=80,"
        f"loudnorm=I={C.LOUDNESS['I']}:TP={C.LOUDNESS['TP']}:LRA={C.LOUDNESS['LRA']}"
        f":measured_I={meas['input_i']}:measured_TP={meas['input_tp']}"
        f":measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}"
        f":offset={meas['target_offset']}:linear=true,"
        "aresample=48000"
    )
    run([FFMPEG, "-y", "-hide_banner", "-nostats", "-i", str(premaster),
         "-af", af, "-c:v", "copy", "-c:a", "aac", "-b:a", C.ENCODE["abitrate"],
         "-ar", C.ENCODE["ar"], "-movflags", "+faststart", str(out)], "master")

    if verbose:
        print(f"[render] {out}  {W}x{H}  pass-1 I={meas['input_i']} LUFS "
              f"TP={meas['input_tp']} dBTP")
    return {"out": str(out), "w": W, "h": H, "premaster": str(premaster),
            "filtergraph": fc, "loudness_in": meas}
