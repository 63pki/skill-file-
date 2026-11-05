"""
Pipeline smoke test — NOT a campaign deliverable.

The campaign's official content folder (Frame.io) is unreachable from this
sandbox, so Phases 3-6 cannot run on real footage. This module proves every
render/QA code path executes correctly against a generated 16:9 test plate,
so that the moment the official trailer is dropped into assets/raw/ the real
run is a single command. Output is named PREVIS_* and is never posted.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from . import qa, render

FFMPEG = shutil.which("ffmpeg") or "/home/user/bin/ffmpeg"


def make_plate(dst: Path, dur: float = 12.0) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", f"testsrc2=size=1920x1080:rate=30:duration={dur}",
        "-f", "lavfi", "-i", f"sine=frequency=220:duration={dur}:sample_rate=48000",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest", str(dst),
    ], check=True)
    return dst


PLAN = {
    "logo": True,
    "segments": [[0.0, 12.0]],
    "captions": [
        {"t0": 0.2, "t1": 2.2, "text": "Lionel Rafale"},
        {"t0": 2.3, "t1": 4.4, "text": "A New Rival Arrives"},
        {"t0": 4.5, "t1": 6.6, "text": "Vilasapara"},
        {"t0": 6.7, "t1": 8.8, "text": "A Totally New Fighter"},
    ],
    "badges": [],
    "color_snap": [9.2, 9.6],
}


def main() -> None:
    outdir = Path("out")
    plate = make_plate(outdir / "_work" / "PREVIS_plate_16x9.mp4")
    for aspect, mode, tag in [("9:16", "crop", "9x16"), ("3:4", "card", "3x4")]:
        out = outdir / f"PREVIS_pipeline_{tag}.mp4"
        render.render(plate, PLAN, out, aspect=aspect, mode=mode)
        from . import graphics as G
        from . import campaign as C
        W, H = render.CANVAS[aspect]
        bbs = [G.logo_plate(int(W * C.LOGO_WIDTH_RATIO), W)[1]]
        bbs += [G.caption_plate(c["text"], W, H, anchor_y=c.get("y"))[1]
                for c in PLAN["captions"]]
        res = qa.audit(out, PLAN, bbs, expected_aspect=aspect,
                       frames_dir=outdir / "qa_frames" / tag)
        print(f"\n--- {tag} ({aspect}, {mode}) --- PASS={res['PASS']}")
        for ch in res["checks"]:
            print(f"  {'OK ' if ch['pass'] else 'BAD'}  {ch['metric']:34} "
                  f"{str(ch['measured'])[:40]:42} {ch['threshold']}")
        Path(f"out/PREVIS_{tag}.qa.json").write_text(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
