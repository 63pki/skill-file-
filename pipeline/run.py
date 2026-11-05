"""
End-to-end orchestrator:  plan -> render -> audit -> scorecard.

    python -m pipeline.run --src RAW.mp4 --plan plan.json --aspect 9:16 \
        --out out/VFC_RAW-01_MASTER_9x16.mp4
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import campaign as C
from . import qa, render


def scorecard(res: dict, out_json: Path) -> None:
    out_json.write_text(json.dumps(res, indent=2))
    c = res["checks"]
    print("\n=== PHASE 6 SCORECARD ===")
    print(f"{'Metric Evaluated':38} {'Measured':34} {'Threshold':28} Status")
    print("-" * 108)
    for ch in c:
        st = "PASS" if ch["pass"] else "FAIL"
        print(f"{ch['metric']:38} {str(ch['measured'])[:33]:34} "
              f"{str(ch['threshold'])[:27]:28} {st}")
    print("-" * 108)
    verdict = "PASS" if res["PASS"] else "FAIL — REBUILD REQUIRED"
    print(f"OVERALL: {verdict}  (details -> {out_json})")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--aspect", default="9:16", choices=["9:16", "3:4"])
    ap.add_argument("--mode", default="crop", choices=["crop", "card"])
    a = ap.parse_args()

    plan = json.loads(Path(a.plan).read_text())
    out = Path(a.out)
    render.render(Path(a.src), plan, out, aspect=a.aspect, mode=a.mode)

    # recompute plate bboxes for the safe-zone audit
    from . import graphics as G
    W, H = render.CANVAS[a.aspect]
    bboxes = []
    if plan.get("logo", True):
        _, bb = G.logo_plate(int(W * C.LOGO_WIDTH_RATIO), W)
        bboxes.append(bb)
    for cap in plan.get("captions", []):
        _, bb = G.caption_plate(cap["text"], W, H, anchor_y=cap.get("y"))
        bboxes.append(bb)

    res = qa.audit(out, plan, bboxes, expected_aspect=a.aspect,
                   frames_dir=out.parent / "qa_frames")
    scorecard(res, out.with_suffix(".qa.json"))


if __name__ == "__main__":
    main()
