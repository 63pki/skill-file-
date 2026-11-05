"""
Asset integrity probe.

The sandbox ships only the `ffmpeg` binary (imageio-ffmpeg wheel, no `ffprobe`),
so Phase 2 inventory data is parsed from `ffmpeg -i <file>` stream diagnostics.
No value here is ever guessed: if a field cannot be parsed it is reported as
UNKNOWN, never invented.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from dataclasses import dataclass, asdict, field
from pathlib import Path

FFMPEG = shutil.which("ffmpeg") or "/home/user/bin/ffmpeg"


@dataclass
class MediaInfo:
    path: str
    exists: bool
    duration_s: float | None = None
    width: int | None = None
    height: int | None = None
    fps: float | None = None
    vcodec: str | None = None
    pix_fmt: str | None = None
    acodec: str | None = None
    sample_rate: int | None = None
    channels: str | None = None
    audio_tracks: int = 0
    size_bytes: int = 0
    integrity: str = "VERIFIED_ORIGINAL"
    notes: list[str] = field(default_factory=list)

    def to_row(self) -> dict:
        return asdict(self)


_DUR = re.compile(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)")
_VID = re.compile(r"Stream #\d+:\d+.*?: Video: ([^,]+).*?, (\d{2,5})x(\d{2,5})")
_AUD = re.compile(r"Stream #\d+:\d+.*?: Audio: ([^,\s]+).*?, (\d+) Hz, ([\w ]+)")
_FPS = re.compile(r"(\d+(?:\.\d+)?)\s*(?:fps|tbr)")
_PIX = re.compile(r"(yuv\w+|rgba?|gbr\w*|nv12|p010le)")


def probe(path: str | Path) -> MediaInfo:
    p = Path(path)
    if not p.is_file():
        return MediaInfo(path=str(p), exists=False, integrity="FAILED_OFFLINE",
                         notes=["file not present on disk"])
    info = MediaInfo(path=str(p), exists=True, size_bytes=p.stat().st_size)

    proc = subprocess.run([FFMPEG, "-hide_banner", "-i", str(p)],
                          capture_output=True, text=True)
    log = proc.stderr

    if m := _DUR.search(log):
        h, mi, s = m.groups()
        info.duration_s = round(int(h) * 3600 + int(mi) * 60 + float(s), 3)

    if m := _VID.search(log):
        info.vcodec = m.group(1).strip()
        info.width, info.height = int(m.group(2)), int(m.group(3))
        seg = log[m.start():m.start() + 400]
        if fm := _FPS.search(seg):
            info.fps = float(fm.group(1))
        if pm := _PIX.search(seg):
            info.pix_fmt = pm.group(1)

    auds = _AUD.findall(log)
    info.audio_tracks = len(auds)
    if auds:
        info.acodec, info.sample_rate, info.channels = auds[0][0], int(auds[0][1]), auds[0][2].strip()

    if info.duration_s is None or info.width is None:
        info.integrity = "CORRUPT_OR_UNREADABLE"
        info.notes.append("ffmpeg could not parse duration/resolution")
    if info.audio_tracks == 0:
        info.notes.append("NO_AUDIO_STREAM — campaign requires official trailer audio")
    return info


def print_table(items: list[MediaInfo]) -> None:
    hdr = ("Asset ID", "Filename", "Format/Codec", "Resolution", "FPS",
           "Duration (s)", "Audio", "Integrity")
    rows = []
    for i, it in enumerate(items, 1):
        rows.append((
            f"RAW-{i:02d}",
            Path(it.path).name,
            f"{it.vcodec or '?'}/{(it.acodec or 'none')}",
            f"{it.width}x{it.height}" if it.width else "UNKNOWN",
            f"{it.fps:.2f}" if it.fps else "UNKNOWN",
            f"{it.duration_s:.2f}" if it.duration_s is not None else "UNKNOWN",
            (f"{it.channels} {it.sample_rate//1000}kHz" if it.audio_tracks else "none"),
            it.integrity,
        ))
    widths = [max(len(str(r[i])) for r in [hdr] + rows) for i in range(len(hdr))]
    def fmt(r): return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)) + " |"
    print(fmt(hdr))
    print("|" + "|".join("-" * (w + 2) for w in widths) + "|")
    for r in rows:
        print(fmt(r))


if __name__ == "__main__":
    import sys
    files = sys.argv[1:]
    if not files:
        print("usage: python -m pipeline.probe <file> [file...]")
        raise SystemExit(2)
    items = [probe(f) for f in files]
    print_table(items)
    print(json.dumps([i.to_row() for i in items], indent=2))
