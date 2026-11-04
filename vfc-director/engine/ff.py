"""FFmpeg/FFprobe-free binary shim.

The sandbox that produced this package ships no system ffmpeg and no ffprobe.
`imageio-ffmpeg` (PyPI) carries a fully static ffmpeg build (n9.x) with
libx264, libass/freetype, loudnorm, ebur128 and libvmaf compiled in, so every
measurement and every render in this package is executed by a real encoder.

There is no ffprobe binary, so container/stream interrogation is implemented by
parsing ffmpeg's own `-i` banner. That parse is pinned by unit tests in
`dev/smoke_test.py` so a future ffmpeg banner change fails loudly instead of
silently returning zeros (the classic "measured nothing, reported success" bug).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, asdict, field
from typing import Iterable, Sequence


class FFmpegError(RuntimeError):
    pass


def ffmpeg_path() -> str:
    env = os.environ.get("VFC_FFMPEG")
    if env:
        return env
    try:  # preferred: static build from PyPI
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass
    found = shutil.which("ffmpeg")
    if not found:
        raise FFmpegError(
            "No ffmpeg found. Install with: pip install imageio-ffmpeg "
            "(or set VFC_FFMPEG=/path/to/ffmpeg)."
        )
    return found


def capabilities() -> dict:
    """Report the real build flags, so downstream code never assumes a filter."""
    out = subprocess.run(
        [ffmpeg_path(), "-hide_banner", "-version"],
        capture_output=True, text=True, check=True,
    ).stdout
    filters = subprocess.run(
        [ffmpeg_path(), "-hide_banner", "-filters"],
        capture_output=True, text=True, check=True,
    ).stdout
    encoders = subprocess.run(
        [ffmpeg_path(), "-hide_banner", "-encoders"],
        capture_output=True, text=True, check=True,
    ).stdout
    wanted_filters = ["drawtext", "ass", "subtitles", "boxblur", "eq", "crop",
                      "scale", "overlay", "zoompan", "alphamerge", "ebur128",
                      "loudnorm", "xfade", "concat", "highpass", "sidechaingate",
                      "split", "blackdetect", "freezedetect", "drawbox", "drawtext"]
    return {
        "ffmpeg": out.splitlines()[0],
        "version": out.splitlines()[0].split()[2] if len(out.splitlines()[0].split()) > 2 else "unknown",
        "config_has": [flag for flag in (
            "--enable-libx264", "--enable-libass", "--enable-libfreetype",
            "--enable-libvmaf", "--enable-libharfbuzz") if flag in out],
        "filters": {f: bool(re.search(rf"\s{f}\s", filters)) for f in wanted_filters},
        "encoders": {
            "libx264": "libx264" in encoders,
            "aac": bool(re.search(r"\baac\b", encoders)),
        },
    }


def run(args: Sequence[str], *, timeout: int | None = None, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run([ffmpeg_path(), "-hide_banner", *args],
                          capture_output=True, text=True, timeout=timeout)
    if check and proc.returncode != 0:
        raise FFmpegError(
            f"ffmpeg exited {proc.returncode}\nargs: {' '.join(args[:14])}...\n"
            f"stderr tail:\n{proc.stderr[-2500:]}"
        )
    return proc


def run_bytes(args: Sequence[str], *, timeout: int | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([ffmpeg_path(), "-hide_banner", "-v", "error", *args],
                          capture_output=True, timeout=timeout)


# --------------------------------------------------------------------------
# Container / stream interrogation (ffprobe replacement)
# --------------------------------------------------------------------------

_DURATION = re.compile(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)")
_STREAM = re.compile(r"Stream #(\d+):(\d+)(?:\[[^\]]*\])?(?:\([^)]*\))?: (\w+): ([^\n]+)")
_VIDEO_DIMS = re.compile(r"(\d{2,5})x(\d{2,5})")
_VIDEO_FPS = re.compile(r"([\d.]+)\s*fps")
_AUDIO_RATE = re.compile(r"(\d+)\s*Hz")
_AUDIO_CH = re.compile(r"(mono|stereo|[\d.]+\s*\(?[a-z0-9.]+\)?)\s*$")
_BITRATE = re.compile(r"bitrate:\s*(\d+)\s*kb/s")


@dataclass
class StreamInfo:
    index: int
    kind: str
    codec: str
    detail: str
    width: int | None = None
    height: int | None = None
    fps: float | None = None
    pix_fmt: str | None = None
    sample_rate: int | None = None
    channels: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MediaInfo:
    path: str
    duration_s: float
    size_bytes: int
    bitrate_kbps: int | None
    format_name: str
    streams: list[StreamInfo] = field(default_factory=list)
    frame_count: int | None = None

    @property
    def video(self) -> StreamInfo | None:
        return next((s for s in self.streams if s.kind == "Video"), None)

    @property
    def audio(self) -> StreamInfo | None:
        return next((s for s in self.streams if s.kind == "Audio"), None)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["video"] = self.video.to_dict() if self.video else None
        d["audio"] = self.audio.to_dict() if self.audio else None
        return d


def probe(path: str, *, count_frames: bool = True) -> MediaInfo:
    """Interrogate a real file. Raises if the file yields no duration/streams."""
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    banner = subprocess.run([ffmpeg_path(), "-hide_banner", "-i", path],
                            capture_output=True, text=True).stderr

    m = _DURATION.search(banner)
    if not m:
        raise FFmpegError(f"could not read duration from {path}:\n{banner[-800:]}")
    duration = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))

    streams: list[StreamInfo] = []
    for sm in _STREAM.finditer(banner):
        kind, detail = sm.group(3), sm.group(4)
        codec = detail.split(",")[0].strip().split(" ")[0]
        info = StreamInfo(index=len(streams), kind=kind, codec=codec, detail=detail.strip())
        if kind == "Video":
            dims = _VIDEO_DIMS.search(detail)
            fps = _VIDEO_FPS.search(detail)
            if dims:
                info.width, info.height = int(dims.group(1)), int(dims.group(2))
            if fps:
                info.fps = float(fps.group(1))
            # detail begins at the codec, e.g.
            #   "h264 (High) (avc1 / 0x31637661), yuv420p(progressive), 1080x1920 ..."
            fields = [f.strip() for f in detail.split(",")]
            if len(fields) > 1 and re.fullmatch(r"[a-z0-9]+(\([^)]*\))?", fields[1]):
                info.pix_fmt = fields[1].split("(")[0]
        if kind == "Audio":
            rate = _AUDIO_RATE.search(detail)
            if rate:
                info.sample_rate = int(rate.group(1))
            ch = re.search(r"\b(mono|stereo|quad|2\.1|5\.1|7\.1)\b", detail)
            info.channels = ch.group(1) if ch else None
        streams.append(info)

    if not any(s.kind == "Video" for s in streams):
        raise FFmpegError(f"no video stream in {path}")

    frames = None
    if count_frames:
        # decode rather than stream-copy: with -c copy ffmpeg reports packet
        # batches, not frames (observed: "frame= 1" on a 360-frame master).
        stats = subprocess.run(
            [ffmpeg_path(), "-hide_banner", "-nostdin", "-i", path,
             "-map", "0:v:0", "-f", "null", "-"],
            capture_output=True, text=True).stderr
        found = re.findall(r"frame=\s*(\d+)", stats)
        if found:
            frames = int(found[-1])

    br = _BITRATE.search(banner)
    fmt_name = re.search(r"Input #0, ([^,]+),", banner)
    return MediaInfo(
        path=os.path.abspath(path),
        duration_s=round(duration, 3),
        size_bytes=os.path.getsize(path),
        bitrate_kbps=int(br.group(1)) if br else None,
        format_name=fmt_name.group(1) if fmt_name else "unknown",
        streams=streams,
        frame_count=frames,
    )


def measure_loudness(path: str) -> dict:
    """EBU R128 integrated loudness / true peak via the ebur128 filter."""
    proc = run(["-nostdin", "-i", path, "-map", "0:a:0",
                "-af", "ebur128=peak=true", "-f", "null", "-"], check=True)
    text = proc.stderr
    summary = text[text.rfind("Summary:"):] if "Summary:" in text else text
    integrated = re.search(r"I:\s*(-?[\d.]+)\s*LUFS", summary)
    lra = re.search(r"LRA:\s*(-?[\d.]+)\s*LU", summary)
    peak = re.search(r"Peak:\s*(-?[\d.]+)\s*dBFS", summary)
    if not integrated or not peak:
        raise FFmpegError(f"ebur128 produced no summary for {path}")
    return {
        "integrated_lufs": float(integrated.group(1)),
        "lra_lu": float(lra.group(1)) if lra else None,
        "true_peak_dbfs": float(peak.group(1)),
        "raw_summary": summary.strip(),
    }


def loudnorm_pass1(path: str, start: float | None = None, end: float | None = None,
                   target_i: float = -14.0, target_tp: float = -1.0, lra: float = 11.0,
                   prefix: str = "") -> dict:
    """Measure the EXACT chain pass 2 will run.

    Measuring without the mastering prefix and then applying it in pass 2
    silently lands the master wherever the prefix moved it (observed: -18.7
    LUFS instead of -14.0 when an 80 Hz high-pass removed the programme's
    fundamental). The prefix is therefore mandatory, not optional.
    """
    af = f"loudnorm=I={target_i}:TP={target_tp}:LRA={lra}:print_format=json"
    if prefix:
        af = f"{prefix},{af}"
    args = ["-nostdin", "-i", path]
    if start is not None:
        args += ["-ss", f"{start:.3f}"]
    if end is not None and start is not None:
        args += ["-t", f"{end - start:.3f}"]
    args += ["-map", "0:a:0", "-af", af, "-f", "null", "-"]
    stderr = run(args).stderr
    payload = stderr[stderr.rfind("{"):]
    payload = payload[: payload.rfind("}") + 1]
    return json.loads(payload)


def extract_frame(path: str, t: float, out_png: str, *, width: int | None = None) -> str:
    vf = f"scale={width}:-2" if width else "null"
    run(["-nostdin", "-y", "-ss", f"{max(t, 0):.3f}", "-i", path,
         "-frames:v", "1", "-vf", vf, "-q:v", "2", out_png])
    return out_png


def sha256(path: str) -> str:
    import hashlib

    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()
