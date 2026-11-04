"""Measurements taken from real decoded pixels and real decoded audio.

Nothing here estimates, extrapolates or invents. Every number in the output
JSON comes from decoding the supplied file with ffmpeg and doing arithmetic on
the samples:

  * `audio`   - RMS envelope, spectral-flux onsets, tempo estimate, band energy
  * `video`   - per-sample-frame gradient saliency, brightness, sharpness
  * `cuts`    - ffmpeg scene-change detector hits (real frame differences)
  * `framing` - saliency-energy retention for each candidate crop (the
                "framing shootout" in the directive, made measurable)
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass

import numpy as np

from . import ff

SAMPLE_RATE = 16000
FRAME_SAMPLES = 512
HOP_SAMPLES = 160          # 10 ms hop at 16 kHz
VIDEO_SAMPLE_FPS = 6       # analyse 6 frames/sec for saliency
SAL_W, SAL_H = 192, 108


# --------------------------------------------------------------------------
# Audio
# --------------------------------------------------------------------------

def decode_audio(path: str, start: float | None = None, end: float | None = None,
                 sr: int = SAMPLE_RATE) -> np.ndarray:
    args = ["-ss", f"{start:.3f}"] if start is not None else []
    if start is not None and end is not None:
        args += ["-t", f"{end - start:.3f}"]
    proc = ff.run_bytes([*args, "-i", path, "-map", "0:a:0", "-ac", "1",
                         "-ar", str(sr), "-f", "f32le", "-"])
    samples = np.frombuffer(proc.stdout, dtype=np.float32)
    if samples.size == 0:
        raise ff.FFmpegError(f"no audio decoded from {path}")
    return samples


def _stft_mag(x: np.ndarray) -> np.ndarray:
    if x.size < FRAME_SAMPLES:
        x = np.pad(x, (0, FRAME_SAMPLES - x.size))
    n_frames = 1 + (x.size - FRAME_SAMPLES) // HOP_SAMPLES
    idx = np.arange(FRAME_SAMPLES)[None, :] + HOP_SAMPLES * np.arange(n_frames)[:, None]
    window = np.hanning(FRAME_SAMPLES).astype(np.float32)
    return np.abs(np.fft.rfft(x[idx] * window, axis=1)).astype(np.float32)


def analyse_audio(path: str, start: float | None = None, end: float | None = None) -> dict:
    samples = decode_audio(path, start, end)
    duration = samples.size / SAMPLE_RATE

    # RMS envelope per 10 ms
    n = samples.size // HOP_SAMPLES
    frames = samples[: n * HOP_SAMPLES].reshape(n, HOP_SAMPLES)
    rms = np.sqrt(np.mean(frames.astype(np.float64) ** 2, axis=1) + 1e-12)
    rms_db = 20 * np.log10(rms + 1e-9)
    hop_s = HOP_SAMPLES / SAMPLE_RATE

    # Spectral flux onsets
    mag = _stft_mag(samples)
    flux = np.concatenate([[0.0], np.maximum(0, np.diff(mag, axis=0)).sum(axis=1)])
    flux = flux / (flux.max() + 1e-9)
    onset_times = np.arange(flux.size) * hop_s

    # Peak picking: local maxima that clear an adaptive threshold
    thresh = float(np.quantile(flux, 0.92))
    peaks = [
        i for i in range(1, flux.size - 1)
        if flux[i] >= thresh and flux[i] >= flux[i - 1] and flux[i] > flux[i + 1]
    ]
    # Collapse peaks closer than 80 ms
    transients: list[dict] = []
    for i in peaks:
        t = float(onset_times[i])
        if transients and t - transients[-1]["t"] < 0.08:
            if flux[i] > transients[-1]["strength"]:
                transients[-1] = {"t": round(t, 3), "strength": round(float(flux[i]), 4)}
            continue
        transients.append({"t": round(t, 3), "strength": round(float(flux[i]), 4)})

    # Tempo via autocorrelation of the onset envelope (60-200 BPM)
    tempo = None
    if flux.size > 64:
        env = flux - flux.mean()
        ac = np.correlate(env, env, mode="full")[env.size - 1:]
        lo, hi = int(60 / 200 / hop_s), int(60 / 60 / hop_s)
        hi = min(hi, ac.size - 1)
        if hi > lo + 1:
            lag = lo + int(np.argmax(ac[lo:hi]))
            if lag > 0:
                tempo = round(60.0 / (lag * hop_s), 2)

    # Band energy split (low <150 Hz, mid, high) for impact/whoosh cueing
    spectrum = mag.mean(axis=0)
    freqs = np.fft.rfftfreq(FRAME_SAMPLES, 1 / SAMPLE_RATE)
    bands = {
        "sub_20_80": float(spectrum[(freqs >= 20) & (freqs < 80)].sum()),
        "low_80_250": float(spectrum[(freqs >= 80) & (freqs < 250)].sum()),
        "mid_250_2000": float(spectrum[(freqs >= 250) & (freqs < 2000)].sum()),
        "high_2000_8000": float(spectrum[(freqs >= 2000) & (freqs < 8000)].sum()),
    }
    total_band = sum(bands.values()) + 1e-9
    bands = {k: round(v / total_band, 4) for k, v in bands.items()}

    loud_floor = float(np.quantile(rms_db, 0.05))
    dialogue_band = float(np.quantile(rms_db, 0.95)) - loud_floor

    return {
        "decoded_seconds": round(duration, 3),
        "sample_rate": SAMPLE_RATE,
        "rms_db_mean": round(float(rms_db.mean()), 2),
        "peak_dbfs": round(float(20 * np.log10(np.abs(samples).max() + 1e-9)), 2),
        "dynamic_range_db": round(dialogue_band, 2),
        "tempo_bpm_estimate": tempo,
        "transient_count": len(transients),
        "transients": transients[:400],
        "band_energy_share": bands,
        "envelope_db": [round(float(v), 2) for v in rms_db[::5]],  # 50 ms resolution
        "envelope_hop_s": hop_s * 5,
    }


# --------------------------------------------------------------------------
# Video
# --------------------------------------------------------------------------

def decode_saliency(path: str, fps: int = VIDEO_SAMPLE_FPS) -> dict:
    proc = ff.run_bytes(["-i", path, "-vf",
                         f"fps={fps},scale={SAL_W}:{SAL_H},format=gray",
                         "-f", "rawvideo", "-"])
    raw = np.frombuffer(proc.stdout, dtype=np.uint8)
    frame_size = SAL_W * SAL_H
    if raw.size < frame_size:
        raise ff.FFmpegError(f"no video frames decoded from {path}")
    count = raw.size // frame_size
    frames = raw[: count * frame_size].reshape(count, SAL_H, SAL_W).astype(np.float32)

    gx = np.abs(np.diff(frames, axis=2))          # (N, H,   W-1)
    gy = np.abs(np.diff(frames, axis=1))          # (N, H-1, W)
    mag = gx[:, :-1, :] + gy[:, :, :-1]           # (N, H-1, W-1)
    total = mag.sum(axis=(1, 2)) + 1e-6
    xs = np.arange(mag.shape[2], dtype=np.float32)
    ys = np.arange(mag.shape[1], dtype=np.float32)
    cx = (mag.sum(axis=1) * xs).sum(axis=1) / total
    cy = (mag.sum(axis=2) * ys).sum(axis=1) / total

    # Sharpness: normalised gradient energy; Brightness: mean luma
    sharp = total / mag.size
    bright = frames.mean(axis=(1, 2))

    # frame-to-frame mean absolute difference -> corroborates scene cuts
    mad = np.concatenate([[0.0], np.abs(np.diff(frames, axis=0)).mean(axis=(1, 2))])

    return {
        "fps": fps,
        "frame_count": int(count),
        "centroid_x_norm": [round(float(v) / SAL_W, 4) for v in cx],
        "centroid_y_norm": [round(float(v) / SAL_H, 4) for v in cy],
        "sharpness": [round(float(v), 6) for v in sharp],
        "brightness": [round(float(v) / 255, 4) for v in bright],
        "frame_delta": [round(float(v), 4) for v in mad],
        "saliency_maps": mag,   # numpy, kept in-memory only
    }


def detect_cuts(path: str, threshold: float = 0.30) -> list[dict]:
    proc = ff.run_bytes(["-i", path, "-filter:v",
                         f"select='gt(scene,{threshold})',metadata=print:file=-",
                         "-an", "-f", "null", "-"])
    text = proc.stdout.decode("utf-8", "replace") + proc.stderr.decode("utf-8", "replace")
    cuts: list[dict] = []
    pending: float | None = None
    for line in text.splitlines():
        m = re.search(r"pts_time:([\d.]+)", line)
        if m:
            pending = float(m.group(1))
            continue
        s = re.search(r"scene_score=([\d.]+)", line)
        if s and pending is not None:
            cuts.append({"t": round(pending, 3), "scene_score": round(float(s.group(1)), 4)})
            pending = None
    return cuts


def framing_audit(sal: dict, source_w: int, source_h: int,
                  targets: dict | None = None) -> dict:
    """Saliency-energy retention for each candidate crop.

    A 16:9 master cropped to 9:16 keeps ~31.6% of the horizontal field; whether
    that loses the subject is a measurement, not an opinion. We sum the
    gradient energy that survives each crop window and compare.
    """
    targets = targets or {
        "9x16_full_bleed": (9 / 16, "center"),
        "3x4_modern_card": (3 / 4, "center"),
        "3x4_modern_card_left": (3 / 4, "left"),
        "3x4_modern_card_right": (3 / 4, "right"),
    }
    mag = sal["saliency_maps"]
    h, w = mag.shape[1], mag.shape[2]
    results = {}
    for name, (ar, anchor) in targets.items():
        # fraction of the source width that survives a full-height crop to `ar`
        keep_frac = min(1.0, ar / (source_w / source_h))
        win = max(2, int(round(w * keep_frac)))
        if anchor == "left":
            x0 = 0
        elif anchor == "right":
            x0 = w - win
        else:
            x0 = (w - win) // 2
        inside = mag[:, :, x0:x0 + win].sum(axis=(1, 2))
        total = mag.sum(axis=(1, 2)) + 1e-6
        retention = inside / total
        results[name] = {
            "window_px_in_source": [int(round(source_w * keep_frac)), source_h],
            "horizontal_field_kept_pct": round(keep_frac * 100, 1),
            "mean_saliency_retention": round(float(retention.mean()), 4),
            "min_saliency_retention": round(float(retention.min()), 4),
            "frames_under_75pct": int((retention < 0.75).sum()),
            "frames_analysed": int(retention.size),
        }
    return results


def recommend_framing(audit: dict, directive_threshold: float = 0.75,
                      material_gain: float = 0.05) -> dict:
    """Directive rule, made measurable.

    9:16 is locked when the crop keeps >= 75% of the saliency energy (i.e. the
    subject truncation stays under the directive's 25% limit). If it does not,
    3:4 is chosen only when it is *materially* better; widening the frame for a
    1-2 point gain is not worth the platform spread. Otherwise the 9:16 punch-pan
    treatment is used, which follows the subject instead of cropping blindly.
    """
    nine = audit["9x16_full_bleed"]["mean_saliency_retention"]
    three = max(
        audit[k]["mean_saliency_retention"]
        for k in ("3x4_modern_card", "3x4_modern_card_left", "3x4_modern_card_right")
    )
    if nine >= directive_threshold:
        choose = "9x16_full_bleed"
    elif three - nine >= material_gain:
        choose = "3x4_glass_card"
    else:
        choose = "9x16_punch_pan"
    return {
        "chosen": choose,
        "rule": ("9:16 locked when retained saliency >= 0.75 (subject truncation < 25%); "
                 f"3:4 only if it gains >= {material_gain} retention; else 9:16 punch-pan"),
        "retention_9x16": round(nine, 4),
        "best_3x4_retention": round(three, 4),
        "measured_delta": round(three - nine, 4),
    }


@dataclass
class Shot:
    start: float
    end: float

    @property
    def duration(self) -> float:
        return round(self.end - self.start, 3)


def shots_from_cuts(cuts: list[dict], duration: float, min_shot: float = 0.20) -> list[Shot]:
    bounds = [0.0] + [c["t"] for c in cuts if min_shot < c["t"] < duration - min_shot] + [duration]
    bounds = sorted(set(round(b, 3) for b in bounds))
    merged: list[Shot] = []
    for a, b in zip(bounds, bounds[1:]):
        if b - a < min_shot and merged:
            merged[-1] = Shot(merged[-1].start, b)
        else:
            merged.append(Shot(a, b))
    return merged


def cover_candidates(sal: dict, window: tuple[float, float] = (0.0, 2.0)) -> list[dict]:
    """Rank real frames by sharpness (expression proxy) inside a time window."""
    fps = sal["fps"]
    n = sal["frame_count"]
    out = []
    for i in range(n):
        t = i / fps
        if window[0] <= t <= window[1]:
            out.append({
                "t": round(t, 3),
                "sharpness": sal["sharpness"][i],
                "brightness": sal["brightness"][i],
            })
    out.sort(key=lambda d: (-d["sharpness"] * (0.4 + d["brightness"])))
    return out[:12]


def to_jsonable(obj):
    if isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items() if k != "saliency_maps"}
    if isinstance(obj, list):
        return [to_jsonable(v) for v in obj]
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def full_analysis(path: str, start: float | None = None, end: float | None = None) -> dict:
    info = ff.probe(path, count_frames=False)
    vid = info.video
    result: dict = {
        "path": info.path,
        "probe": info.to_dict(),
        "synthetic_fixture": _is_fixture(path),
    }
    if info.audio:
        result["audio"] = analyse_audio(path, start, end)
    sal = decode_saliency(path)
    result["saliency"] = to_jsonable({k: v for k, v in sal.items() if k != "saliency_maps"})
    result["cuts"] = detect_cuts(path)
    result["shots"] = [{"start": s.start, "end": s.end, "duration": s.duration}
                       for s in shots_from_cuts(result["cuts"], info.duration_s)]
    if vid and vid.width and vid.height:
        audit = framing_audit(sal, vid.width, vid.height)
        result["framing_audit"] = audit
        result["framing_recommendation"] = recommend_framing(audit)
    result["cover_candidates"] = cover_candidates(sal, (start or 0.0, (start or 0.0) + 2.0))
    return to_jsonable(result)


def _is_fixture(path: str) -> bool:
    name = path.lower()
    return "fixture" in name or "synthetic" in name


if __name__ == "__main__":  # pragma: no cover
    import json
    import sys

    print(json.dumps(full_analysis(sys.argv[1]), indent=2)[:4000])
