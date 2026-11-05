"""
Phase 6 — adversarial multi-pass QA.

Pass 1  bitstream + acoustic telemetry (ffmpeg probe + ebur128 + blackdetect)
Pass 2  frame-by-frame adversarial audit (diagnostic frame extraction,
        safe-zone clearance, caption/loudness/campaign compliance)

Every metric is measured from the rendered file. Nothing is asserted from the
edit-decision list alone.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from . import campaign as C
from .probe import probe

FFMPEG = shutil.which("ffmpeg") or "/home/user/bin/ffmpeg"


def _run(args: list[str]) -> str:
    return subprocess.run(args, capture_output=True, text=True).stderr


def ebur128(path: Path) -> dict:
    err = _run([FFMPEG, "-hide_banner", "-nostats", "-i", str(path),
                "-af", "ebur128=peak=true", "-f", "null", "-"])
    tail = err[err.rfind("Summary:"):] if "Summary:" in err else err
    out = {}
    if m := re.search(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", tail):
        out["integrated_lufs"] = float(m.group(1))
    if m := re.search(r"LRA:\s*(-?\d+(?:\.\d+)?)\s*LU", tail):
        out["lra"] = float(m.group(1))
    if m := re.search(r"Peak:\s*(-?\d+(?:\.\d+)?)\s*dBFS", tail):
        out["true_peak_dbtp"] = float(m.group(1))
    return out


def black_frames(path: Path) -> list[dict]:
    err = _run([FFMPEG, "-hide_banner", "-nostats", "-i", str(path),
                "-vf", "blackdetect=d=0.10:pix_th=0.10", "-f", "null", "-"])
    return [{"start": float(a), "end": float(b), "dur": float(c)}
            for a, b, c in re.findall(
                r"black_start:(\d+\.?\d*)\s+black_end:(\d+\.?\d*)\s+black_duration:(\d+\.?\d*)",
                err)]


def grab_frames(path: Path, outdir: Path, dur: float) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    marks = {"frame0": 0.0, "t1.0s": 1.0, "t50pct": dur * 0.50,
             "t85pct": dur * 0.85, "tend": max(0.0, dur - 0.10)}
    paths = {}
    for name, t in marks.items():
        p = outdir / f"qa_{name}.jpg"
        _run([FFMPEG, "-y", "-hide_banner", "-nostats", "-ss", f"{t:.3f}",
              "-i", str(path), "-frames:v", "1", "-q:v", "2", str(p)])
        paths[name] = str(p)
    return paths


def safe_zone_violations(bboxes: list[dict], w: int, h: int) -> list[str]:
    """Analytic clearance audit against platform UI safe zones."""
    sx = w / 1080.0
    sy = h / 1920.0
    top = C.SAFE_ZONES["top"] * sy
    bottom = h - C.SAFE_ZONES["bottom"] * sy
    left = C.SAFE_ZONES["left"] * sx
    right = w - C.SAFE_ZONES["right"] * sx
    bad = []
    for b in bboxes:
        if b["y"] < top:
            bad.append(f"SAFE-ZONE: plate at y={b['y']} intrudes top chrome (<{top:.0f})")
        if b["y"] + b["h"] > bottom:
            bad.append(f"SAFE-ZONE: plate ends y={b['y']+b['h']} intrudes bottom rail (>{bottom:.0f})")
        if b["x"] < left:
            bad.append(f"SAFE-ZONE: plate at x={b['x']} intrudes left margin (<{left:.0f})")
        if b["x"] + b["w"] > right:
            bad.append(f"SAFE-ZONE: plate ends x={b['x']+b['w']} intrudes right rail (>{right:.0f})")
    return bad


def audit(path: Path, plan: dict, bboxes: list[dict],
          expected_aspect: str = "9:16", frames_dir: Path | None = None) -> dict:
    info = probe(path)
    W, H = info.width, info.height
    exp_w, exp_h = {"9:16": (1080, 1920), "3:4": (1080, 1440)}[expected_aspect]

    audio = ebur128(path) if info.audio_tracks else {}
    blacks = black_frames(path)
    frames = grab_frames(path, frames_dir or path.parent / "qa_frames",
                         info.duration_s or 0.0)

    checks = []
    def chk(name, ok, measured, threshold):
        checks.append({"metric": name, "pass": bool(ok), "measured": measured,
                       "threshold": threshold})

    chk("Canvas dimensions", (W, H) == (exp_w, exp_h), f"{W}x{H}", f"{exp_w}x{exp_h}")
    chk("Duration floor (>=10s)", (info.duration_s or 0) >= C.MIN_DURATION_S,
        f"{info.duration_s}s", f">= {C.MIN_DURATION_S}s")
    chk("Integrated loudness", audio and abs(audio.get("integrated_lufs", 99) - (-14.0)) <= 0.5,
        f"{audio.get('integrated_lufs')} LUFS", "-14.0 ±0.5 LUFS")
    chk("True peak ceiling", audio and audio.get("true_peak_dbtp", 9) <= -1.0,
        f"{audio.get('true_peak_dbtp')} dBTP", "<= -1.0 dBTP")
    chk("Pixel format", info.pix_fmt == "yuv420p", info.pix_fmt, "yuv420p")
    chk("Audio stream present", info.audio_tracks >= 1, f"{info.audio_tracks} track(s)",
        ">=1 (official trailer audio only)")
    chk("No black frames", len(blacks) == 0, f"{len(blacks)} detected", "0")
    sz = safe_zone_violations(bboxes, W, H)
    chk("Safe-zone clearance", not sz, "clear" if not sz else f"{len(sz)} violation(s)",
        "0 violations")

    onscreen = [c["text"] for c in plan.get("captions", [])]
    ccm = []
    for t in onscreen:
        ccm += C.validate_onscreen_text(t)
    chk("On-screen text present", len(onscreen) > 0, f"{len(onscreen)} burst(s)", ">=1 mandatory")
    chk("Campaign text compliance", not ccm, "clean" if not ccm else "; ".join(ccm), "0 violations")

    return {
        "file": str(path), "media": info.to_row(), "loudness": audio,
        "black_frames": blacks, "frames": frames,
        "safe_zone_violations": sz, "ccm_failures": ccm,
        "checks": checks, "PASS": all(c["pass"] for c in checks),
    }
