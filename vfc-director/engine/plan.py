"""Turn measurements into a deterministic render plan.

The plan is the contract between analysis and rendering: canvas, eased pan
keyframes, caption cues with resolved coordinates, logo box, audio chain and
the campaign gates that must hold before a render is allowed to ship.
"""
from __future__ import annotations

import json
import os
from typing import Iterable

import numpy as np

from . import ff

CANVAS_9x16 = {"w": 1080, "h": 1920}
CANVAS_3x4 = {"w": 1080, "h": 1440, "card_y": 240}

# Platform UI reserved bands (directive 1.3 / Phase 6 safe-zone audit)
SAFE = {"top": 260, "bottom": 420, "right": 140}

ANCHORS = {
    "hook": (540, 430),        # upper-centre, below the 260px platform band
    "caption": (540, 1330),    # collarbone zone, above the 420px bottom band
    "badge": (900, 300),       # upper-right, clear of the 140px right rail
}

FRAMING_MODES = ("9x16_full_bleed", "3x4_glass_card", "9x16_punch_pan")


def _even(v: float) -> int:
    return int(round(v / 2.0) * 2)


def _smoothstep_keyframes(points: list[tuple[float, float]]) -> str:
    """FFmpeg expression: eased (cubic ease-in-out) interpolation through points."""
    pts = sorted(points)
    if len(pts) == 1:
        return f"{_even(pts[0][1])}"
    expr = f"{_even(pts[-1][1])}"
    for (t0, v0), (t1, v1) in reversed(list(zip(pts, pts[1:]))):
        dur = max(t1 - t0, 1e-3)
        u = f"clip((t-{t0:.3f})/{dur:.3f},0,1)"
        eased = f"({u}*{u}*(3-2*{u}))"
        seg = f"{_even(v0)}+({_even(v1)}-{_even(v0)})*{eased}"
        expr = f"if(lt(t,{t1:.3f}),{seg},{expr})"
    return expr


def _pan_keyframes(analysis: dict, start: float, end: float, src_w: int,
                   crop_w: int, sample_offset: float = 0.0) -> list[tuple[float, float]]:
    """Saliency-centroid driven crop-x keyframes, clamped to the legal range."""
    sal = analysis.get("saliency") or {}
    fps = sal.get("fps", 6)
    cxs = sal.get("centroid_x_norm") or []
    max_x = max(0, src_w - crop_w)
    if not cxs:
        return [(0.0, max_x / 2), (end - start, max_x / 2)]

    # one keyframe per ~0.5 s inside the clip, centroid smoothed to avoid jitter
    times = []
    t = 0.0
    while t <= (end - start) + 1e-6:
        times.append(t)
        t += 0.5
    kf: list[tuple[float, float]] = []
    for t in times:
        absolute = start + t
        idx = int(round(absolute * fps))
        window = cxs[max(0, idx - 2): idx + 3] or [0.5]
        cx = float(np.mean(window))
        x = cx * src_w - crop_w / 2.0
        kf.append((round(t + sample_offset, 3), float(min(max(x, 0), max_x))))
    # collapse to the two extreme anchors if movement is negligible (<8 px)
    if max(v for _, v in kf) - min(v for _, v in kf) < 8:
        mid = float(np.mean([v for _, v in kf]))
        return [(kf[0][0], mid), (kf[-1][0], mid)]
    return kf


def build_clip_plan(*, source: str, analysis: dict, clip_id: str, start: float, end: float,
                    framing: str, captions: list[dict], hook: str | None = None,
                    logo: str | None = None, logo_box: dict | None = None,
                    campaign: str = "VFC", fps: float | None = None) -> dict:
    if framing not in FRAMING_MODES:
        raise ValueError(f"framing must be one of {FRAMING_MODES}")
    if end <= start:
        raise ValueError("end must be after start")
    if end - start < 10.0:
        # Campaign hard gate: video must be at least 10 seconds long.
        raise ValueError(
            f"clip window is {end - start:.2f}s; the campaign hard gate requires >= 10.0s"
        )

    info = ff.probe(source, count_frames=False)
    vid = info.video
    src_w, src_h = vid.width, vid.height
    src_fps = fps or vid.fps or 30.0
    clip_dur = round(end - start, 3)

    if framing == "3x4_glass_card":
        crop_h = src_h
        crop_w = _even(src_h * 3 / 4)
        scale_to = (CANVAS_3x4["w"], CANVAS_3x4["h"])
        overlay_xy = (0, CANVAS_3x4["card_y"])
        canvas = {"w": 1080, "h": 1920}
    else:
        crop_h = src_h
        crop_w = _even(src_h * 9 / 16)
        scale_to = (CANVAS_9x16["w"], CANVAS_9x16["h"])
        overlay_xy = (0, 0)
        canvas = {"w": 1080, "h": 1920}

    # never crop wider than the source
    crop_w = min(crop_w, _even(src_w))
    if framing == "9x16_punch_pan":
        # slow 100% -> 106% push, expressed as a scale ramp in the filtergraph
        punch = {"from": 1.0, "to": 1.06, "seconds": 2.5}
    else:
        punch = None

    pan = _pan_keyframes(analysis, start, end, src_w, crop_w)
    pan_expr = _smoothstep_keyframes(pan)
    pan_range = [min(v for _, v in pan), max(v for _, v in pan)]

    # caption cues: clamp to canvas + verify safe-zone clearance
    cues = []
    for i, c in enumerate(sorted(captions, key=lambda d: d["t0"])):
        tb = c.get("timebase", "clip")           # "clip" = relative, "source" = absolute
        off = start if tb == "source" else 0.0
        t0 = max(0.0, round(float(c["t0"]) - off, 3))
        t1 = min(clip_dur, round(float(c["t1"]) - off, 3))
        if t1 <= t0:
            continue
        anchor = c.get("anchor", "caption")
        x, y = ANCHORS[anchor]
        cues.append({
            "index": i,
            "text": c["text"],
            "t0": round(t0, 3),
            "t1": round(t1, 3),
            "anchor": anchor,
            "x": x,
            "y": y,
            "style": c.get("style", anchor.upper()),
            "timebase": tb,
            "safe_zone_ok": _in_safe_zone(x, y),
            "wpm": _wpm(c["text"], t1 - t0),
        })
    if any(not c["safe_zone_ok"] for c in cues):
        raise ValueError("a caption anchor falls outside the platform safe zone")

    plan = {
        "plan_version": "1.0.0",
        "campaign": campaign,
        "clip_id": clip_id,
        "source": {"path": info.path, "sha256": ff.sha256(info.path),
                   "width": src_w, "height": src_h, "fps": src_fps,
                   "duration": info.duration_s},
        "window": {"start": round(start, 3), "end": round(end, 3), "duration": clip_dur},
        "framing": {
            "mode": framing,
            "canvas": canvas,
            "crop": {"w": crop_w, "h": crop_h, "scale_to": list(scale_to),
                     "overlay_xy": list(overlay_xy)},
            "pan_keyframes": [{"t": t, "x": _even(v)} for t, v in pan],
            "pan_pixel_range": [_even(pan_range[0]), _even(pan_range[1])],
            "pan_expression": pan_expr,
            "punch": punch,
            "background": {"fill": "blurred mirrored plate", "boxblur": "30:5",
                           "eq_brightness": -0.35} if framing == "3x4_glass_card" else None,
        },
        "typography": {"cues": cues, "hook_style": "HOOK", "active_hook_text": hook},
        "logo": {"file": logo, "box": logo_box or {"x": 48, "y": 292, "w": 220}},
        "audio": {
            "source_stream": "0:a:0" if info.audio else None,
            "added_music": False,
            "added_sfx": False,
            "ai_voice": False,
            "chain": ["highpass=f=80", "loudnorm(two-pass)"],
            "target_lufs": -14.0,
            "target_true_peak_dbtp": -1.0,
        },
        "encode": {"codec": "libx264", "profile": "high", "level": "4.2",
                   "pix_fmt": "yuv420p", "crf": 18, "preset": "slow",
                   "movflags": "+faststart", "fps": src_fps},
        "gates": {
            "duration_min_10s": clip_dur >= 10.0,
            "logo_required": True,
            "on_screen_text_required": True,
            "source_only_audio": True,
            "has_hook": bool(hook),
            "captions_present": bool(cues),
        },
    }
    return plan


def _in_safe_zone(x: int, y: int) -> bool:
    return (SAFE["top"] + 40) <= y <= (1920 - SAFE["bottom"] - 40) and x <= (1080 - SAFE["right"] - 40)


def _wpm(text: str, seconds: float) -> float:
    words = len([w for w in text.replace("\n", " ").split(" ") if w.strip()])
    return round(words / max(seconds, 0.1) * 60.0, 1)


def wpm_ceiling_check(plan: dict, ceiling: float = 220.0) -> dict:
    bad = [c for c in plan["typography"]["cues"] if c["wpm"] > ceiling]
    return {"ceiling_wpm": ceiling, "violations": bad, "pass": not bad}


def write_plan(plan: dict, path: str) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(plan, fh, indent=2)
    return path


def load_plan(path: str) -> dict:
    with open(path) as fh:
        return json.load(fh)
