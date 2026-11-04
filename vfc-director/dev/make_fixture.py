"""Generate a SYNTHETIC test clip so the render chain can be exercised offline.

This fixture is NOT campaign footage and must never be shipped. It exists so
that every filtergraph, expression and loudness pass in this package is proven
to execute on a real encode before any real asset arrives.

    python3 dev/make_fixture.py build/fixture_16x9.mp4
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine import ff  # noqa: E402

GRAPH_PARTS = [
    # three visibly different "shots" with moving subjects to drive saliency
    "testsrc2=size=1920x1080:rate=30:duration=5,"
    "drawbox=x='mod(t*420,1500)':y=380:w=340:h=340:color=white@0.9:t=fill",
    # continuously moving plate: a frozen source would trip the freeze detector
    "life=size=1920x1080:rate=30:mold=10:ratio=0.12:death_color=#101820:"
    "life_color=#00E0FF:stitch=0,trim=duration=5,"
    "drawbox=x='mod(t*260,1400)':y=300:w=320:h=520:color=black@0.85:t=fill",
    "mandelbrot=size=1920x1080:rate=30,trim=duration=5,"
    "hue=h='20*t':s=1.4",
]


def make(path: str, seconds: int = 15) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)) or ".", exist_ok=True)
    args = ["-nostdin", "-y"]
    for g in GRAPH_PARTS:
        args += ["-f", "lavfi", "-i", g]
    args += ["-f", "lavfi", "-i",
             f"aevalsrc='0.35*sin(2*PI*55*t)*(0.5+0.5*sin(2*PI*2.4*t))"
             f"+0.08*sin(2*PI*1400*t)|0.35*sin(2*PI*55*t)*(0.5+0.5*sin(2*PI*2.4*t))':s=48000:d={seconds}"]
    args += [
        "-filter_complex",
        "[0:v][1:v][2:v]concat=n=3:v=1:a=0,trim=duration=%d,setpts=PTS-STARTPTS,format=yuv420p[v]" % seconds,
        "-map", "[v]", "-map", "3:a",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-t", str(seconds), path,
    ]
    ff.run(args, timeout=300)
    info = ff.probe(path)
    print(f"fixture written: {path}  {info.video.width}x{info.video.height} "
          f"{info.duration_s}s @ {info.video.fps}fps, audio={bool(info.audio)}")
    return path


if __name__ == "__main__":
    make(sys.argv[1] if len(sys.argv) > 1 else "build/fixture_16x9.mp4")
