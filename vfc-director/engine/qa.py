"""Adversarial QA: measure the shipped file, not the intention behind it."""
from __future__ import annotations

import json
import os

from . import ff
from .plan import SAFE

THRESHOLDS = {
    "duration_min_s": 10.0,
    "integrated_lufs": (-14.5, -13.5),
    "true_peak_max_dbtp": -1.0,
    "canvas": {(1080, 1920), (1080, 1440)},
}


def black_frames(path: str) -> dict:
    proc = ff.run(["-nostdin", "-i", path, "-vf", "blackdetect=d=0.04:pix_th=0.10",
                   "-an", "-f", "null", "-"], check=True)
    hits = [line for line in proc.stderr.splitlines() if "black_start" in line]
    return {"black_segments": len(hits), "raw": hits[:20]}


def freeze_frames(path: str) -> dict:
    proc = ff.run(["-nostdin", "-i", path, "-vf", "freezedetect=n=-60dB:d=0.4",
                   "-an", "-f", "null", "-"], check=True)
    hits = [line for line in proc.stderr.splitlines() if "freeze_start" in line]
    return {"freeze_segments": len(hits), "raw": hits[:20]}


def safe_zone_overlay(frame_png: str, out_png: str, canvas: tuple[int, int]) -> str:
    """Draw the platform-reserved bands on a diagnostic frame."""
    w, h = canvas
    boxes = [
        (0, 0, w, SAFE["top"], "top UI band"),
        (0, h - SAFE["bottom"], w, SAFE["bottom"], "bottom UI band"),
        (w - SAFE["right"], 0, SAFE["right"], h, "right rail"),
    ]
    filters = []
    for x, y, bw, bh, _label in boxes:
        filters.append(f"drawbox=x={x}:y={y}:w={bw}:h={bh}:color=red@0.35:t=fill")
        filters.append(f"drawbox=x={x}:y={y}:w={bw}:h={bh}:color=white@0.9:t=3")
    ff.run(["-nostdin", "-y", "-i", frame_png, "-vf", ",".join(filters),
            "-frames:v", "1", out_png])
    return out_png


def extract_diagnostics(path: str, outdir: str, canvas: tuple[int, int],
                        duration: float, cover_t: float | None = None) -> dict:
    os.makedirs(outdir, exist_ok=True)
    w, h = canvas
    points = {"t0": 0.0, "t1": 1.0, "t50": duration * 0.5,
              "t85": duration * 0.85, "tend": max(duration - 0.1, 0)}
    if cover_t is not None:
        points["cover"] = max(0.0, min(cover_t, duration - 0.05))

    out = {}
    for name, t in points.items():
        raw = os.path.join(outdir, f"frame_{name}.png")
        ff.extract_frame(path, t, raw)
        out[name] = {"t": round(t, 3), "png": raw}
        if name in ("t0", "cover"):
            out[name]["safe_zone_png"] = safe_zone_overlay(
                raw, os.path.join(outdir, f"frame_{name}_safezone.png"), (w, h)
            )
    return out


def cover_score(path: str, t: float) -> dict:
    """Sharpness + exposure of a real frame, used to pick the cover JPEG."""
    import numpy as np
    from PIL import Image

    tmp = f"/tmp/vfc_cover_{abs(hash((path, round(t, 3))))}.png"
    ff.extract_frame(path, t, tmp, width=360)
    try:
        img = np.asarray(Image.open(tmp).convert("L"), dtype=np.float32)
    finally:
        os.unlink(tmp)
    if img.ndim != 2 or min(img.shape) < 8:
        return {"t": t, "sharpness": 0.0, "brightness": 0.0, "score": 0.0}
    gx = np.abs(np.diff(img, axis=1))[:-1, :]   # (H-1, W-1)
    gy = np.abs(np.diff(img, axis=0))[:, :-1]   # (H-1, W-1)
    sharp = float((gx + gy).mean())
    bright = float(img.mean()) / 255.0
    exposure_penalty = abs(bright - 0.55)
    score = sharp * (1.0 - min(exposure_penalty, 0.9))
    return {"t": round(t, 3), "sharpness": round(sharp, 3),
            "brightness": round(bright, 4), "score": round(score, 3)}


def _rel_luminance(rgb):
    """WCAG 2.x relative luminance for sRGB 0-255 triples."""
    import numpy as np

    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def logo_contrast(master: str, plan: dict, samples=(0.02, 0.25, 0.5, 0.75, 0.98),
                  threshold: float = 4.5) -> dict:
    """Measure the watermark's real legibility against the real footage.

    The logo is white and orange; what matters is the plate behind it. For each
    sample we crop the exact overlay box out of the encoded master, take the
    background pixels (the dark plate the scrim creates) and compute the WCAG
    contrast ratio of white text over them. Below 4.5:1 the watermark fails the
    brief's "high-quality post" bar, whatever it looks like on a still.
    """
    import numpy as np
    from PIL import Image

    from . import render as render_mod

    box = plan["logo"]["box"]
    lw, lh = render_mod.logo_geometry(plan["logo"]["file"], box["w"])
    duration = ff.probe(master, count_frames=False).duration_s
    ring = 10   # inside the 14 px solid plate margin, outside the wordmark
    rows = []
    for frac in samples:
        t = max(0.0, min(duration * frac, duration - 0.05))
        tmp = f"/tmp/vfc_logo_{int(frac * 100)}.png"
        ff.extract_frame(master, t, tmp)
        with Image.open(tmp) as im:
            full = np.asarray(im.convert("RGB"), dtype=np.uint8)
        x0, y0 = max(0, box["x"] - ring), max(0, box["y"] - ring)
        x1, y1 = min(full.shape[1], box["x"] + lw + ring), min(full.shape[0], box["y"] + lh + ring)
        patch = full[y0:y1, x0:x1].copy()
        # blank out the logo itself: what remains is the plate that sits behind it
        patch[box["y"] - y0:box["y"] - y0 + lh, box["x"] - x0:box["x"] - x0 + lw] = 0
        mask = patch.sum(axis=2) > 0
        lum = _rel_luminance(patch[mask])
        bg = float(lum.mean()) if lum.size else 0.0
        rows.append({"t": round(t, 3), "plate_luminance": round(bg, 4),
                     "contrast_vs_white": round(1.05 / (bg + 0.05), 2),
                     "pixels_sampled": int(mask.sum())})
    worst = min(r["contrast_vs_white"] for r in rows)
    return {"samples": rows, "worst_contrast": worst, "threshold": threshold,
            "pass": worst >= threshold}


def verify(master: str, plan: dict, outdir: str) -> dict:
    info = ff.probe(master, count_frames=True)
    vid, aud = info.video, info.audio
    canvas = (vid.width, vid.height) if vid else (0, 0)
    loud = ff.measure_loudness(master)
    black = black_frames(master)
    freeze = freeze_frames(master)
    cover_t = plan.get("qa_cover_time")
    frames = extract_diagnostics(master, outdir, canvas, info.duration_s, cover_t)
    logo = logo_contrast(master, plan) if plan.get("logo", {}).get("file") else None

    expected_dur = plan["window"]["duration"]
    checks = {
        "duration_min_10s": info.duration_s >= THRESHOLDS["duration_min_s"],
        "duration_matches_plan": abs(info.duration_s - expected_dur) <= 0.12,
        "canvas_supported": canvas in THRESHOLDS["canvas"],
        "pix_fmt_yuv420p": (vid.pix_fmt or "").startswith("yuv420p") if vid else False,
        "h264_high_profile": _is_h264_high(master),
        "single_audio_stream_source_only": len([s for s in info.streams if s.kind == "Audio"]) == 1,
        "loudness_in_tolerance": THRESHOLDS["integrated_lufs"][0] <= loud["integrated_lufs"] <= THRESHOLDS["integrated_lufs"][1],
        "true_peak_under_ceiling": loud["true_peak_dbfs"] <= THRESHOLDS["true_peak_max_dbtp"],
        "no_black_frames": black["black_segments"] == 0,
        "no_stuck_freezes": freeze["freeze_segments"] == 0,
        "faststart": _has_faststart(master),
        "logo_contrast_wcag_4_5": bool(logo and logo["pass"]),
    }

    report = {
        "master": os.path.abspath(master),
        "probe": info.to_dict(),
        "loudness": loud,
        "blackdetect": black,
        "freezedetect": freeze,
        "frames": frames,
        "logo_contrast": logo,
        "checks": checks,
        "measured": {
            "duration_s": info.duration_s,
            "frame_count": info.frame_count,
            "canvas": f"{canvas[0]}x{canvas[1]}",
            "fps": vid.fps if vid else None,
            "integrated_lufs": loud["integrated_lufs"],
            "true_peak_dbfs": loud["true_peak_dbfs"],
        },
    }
    report["scorecard"] = scorecard(plan, report)
    with open(os.path.join(outdir, "qa_report.json"), "w") as fh:
        json.dump(report, fh, indent=2)
    return report


def _is_h264_high(master: str) -> bool:
    banner = __import__("subprocess").run(
        [ff.ffmpeg_path(), "-hide_banner", "-i", master], capture_output=True, text=True
    ).stderr
    return "Video: h264" in banner and "High" in banner.split("Video: h264")[1][:120]


def _has_faststart(master: str) -> bool:
    """moov must precede mdat. mdat usually sits past the first read window,
    so an absent mdat is not a failure - an absent moov is."""
    with open(master, "rb") as fh:
        head = fh.read(65536)
    i_moov, i_mdat = head.find(b"moov"), head.find(b"mdat")
    if i_moov < 0:
        return False
    return i_mdat < 0 or i_moov < i_mdat


def scorecard(plan: dict, report: dict) -> dict:
    """Score only what this machine can physically measure.

    Anything that needs a human eye or an ASR pass is returned as
    `requires_human_signoff` with the evidence path - never as a fabricated
    number. That distinction is the whole point of the audit.
    """
    checks = report["checks"]
    lufs = report["loudness"]["integrated_lufs"]
    audio_points = 10.0 if (THRESHOLDS["integrated_lufs"][0] <= lufs <= THRESHOLDS["integrated_lufs"][1]
                            and report["loudness"]["true_peak_dbfs"] <= -1.0) else 6.0

    caption_cues = plan["typography"]["cues"]
    typography_points = 10.0 if (caption_cues and all(c["safe_zone_ok"] for c in caption_cues)
                                 and all(c["wpm"] <= 220 for c in caption_cues)) else 7.0

    booleans = [v for v in checks.values()]
    compliance_points = 10.0 if all(booleans) else round(10.0 * sum(booleans) / len(booleans), 2)

    return {
        "audio_engineering": {"score": audio_points, "threshold": 9.5,
                              "pass": audio_points >= 9.5, "evidence": report["loudness"]},
        "caption_safe_zone_and_density": {
            "score": typography_points, "threshold": 10.0, "pass": typography_points >= 10.0,
            "cues": len(caption_cues), "evidence": report["frames"].get("t50", {}).get("png"),
        },
        "campaign_compliance_mechanical": {
            "score": compliance_points, "threshold": 10.0, "pass": compliance_points >= 10.0,
            "checks": checks,
        },
        "hook_stop_rate_viability": {
            "score": None, "threshold": 9.0, "pass": None,
            "requires_human_signoff": True,
            "evidence": report["frames"].get("t0", {}).get("png"),
            "note": "scroll-stop is a human judgement; frame 0 is exported for review",
        },
        "temporal_pacing_rhythm": {
            "score": None, "threshold": 9.0, "pass": None,
            "requires_human_signoff": True,
            "evidence": report["frames"].get("t85", {}).get("png"),
            "note": "no ASR/beat-grid model is installed; pacing reviewed from exported frames",
        },
        "caption_syllable_sync": {
            "score": None, "pass": None, "requires_human_signoff": True,
            "note": "needs a transcription pass (whisper) or a human; not fabricated here",
        },
    }
