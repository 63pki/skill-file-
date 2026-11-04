"""Command line surface: doctor / acquire / analyze / plan / render / qa / build.

    python3 -m engine.cli doctor
    python3 -m engine.cli build --spec campaign/clips/CLIP_SPEC.example.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from . import analyze, assets, compliance, ff, plan as planmod, qa, render

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _print(obj) -> None:
    print(json.dumps(obj, indent=2))


def cmd_doctor(args) -> int:
    caps = ff.capabilities()
    missing = [k for k, v in caps["filters"].items() if not v]
    report = {
        "ffmpeg": caps["ffmpeg"],
        "python": sys.version.split()[0],
        "build_flags": caps["config_has"],
        "encoders": caps["encoders"],
        "missing_filters": missing,
        "python_deps": _deps(),
        "ready": not missing and caps["encoders"]["libx264"] and caps["encoders"]["aac"],
    }
    _print(report)
    return 0 if report["ready"] else 1


def _deps() -> dict:
    out = {}
    for mod in ("numpy", "PIL", "imageio_ffmpeg"):
        try:
            __import__(mod)
            out[mod] = "ok"
        except Exception:
            out[mod] = "MISSING"
    return out


def cmd_acquire(args) -> int:
    rec = assets.acquire(args.url, args.outdir, args.log, name=args.name)
    _print(rec["final"])
    return 0 if rec["resolved"] else 2


def cmd_analyze(args) -> int:
    a = analyze.full_analysis(args.source)
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump(a, fh, indent=2)
    _print({
        "out": args.out,
        "duration_s": a["probe"]["duration_s"],
        "canvas": f"{a['probe']['video']['width']}x{a['probe']['video']['height']}",
        "cuts": len(a["cuts"]),
        "transients": a.get("audio", {}).get("transient_count"),
        "framing_recommendation": a.get("framing_recommendation"),
    })
    return 0


def cmd_plan(args) -> int:
    with open(args.analysis) as fh:
        a = json.load(fh)
    with open(args.captions) as fh:
        cues = json.load(fh)
    framing = args.framing
    if framing == "auto":
        framing = a["framing_recommendation"]["chosen"]
    p = planmod.build_clip_plan(
        source=args.source, analysis=a, clip_id=args.clip_id,
        start=args.start, end=args.end, framing=framing,
        captions=cues, hook=args.hook, logo=args.logo,
    )
    planmod.write_plan(p, args.out)
    _print({"plan": args.out, "framing": framing, "cues": len(p["typography"]["cues"]),
            "gates": p["gates"]})
    return 0


def cmd_render(args) -> int:
    p = planmod.load_plan(args.plan)
    if args.logo:
        p["logo"]["file"] = args.logo
    log = render.render(p, args.out, args.workdir, logo_path=p["logo"]["file"],
                        preset=args.preset, crf=args.crf, dry_run=args.dry_run)
    _print({k: log[k] for k in ("output", "bytes") if k in log})
    if "loudness" in log:
        _print(log["loudness"])
    return 0


def cmd_qa(args) -> int:
    p = planmod.load_plan(args.plan)
    rep = qa.verify(args.master, p, args.outdir)
    _print(rep["scorecard"])
    return 0 if all(v is not False for v in rep["checks"].values()) else 3


def cmd_captions(args) -> int:
    if args.validate:
        text = open(args.validate).read()
        results = [compliance.validate_caption(text, args.platform)]
    else:
        results = [{"platform": k, **v["validation"]}
                   for k, v in compliance.write_captions(args.outdir, args.optional_copy).items()]
    _print(results)
    return 0 if all(r["pass"] for r in results) else 4


def cmd_slice(args) -> int:
    for line in render.slice_commands(args.canvas, args.mode):
        print(line)
    return 0


def cmd_build(args) -> int:
    """End-to-end: analyse -> plan -> render -> QA -> covers -> manifest."""
    with open(args.spec) as fh:
        spec = json.load(fh)
    outdir = args.outdir or os.path.join(ROOT, "build", spec["clip_id"])
    workdir = os.path.join(outdir, "work")
    os.makedirs(workdir, exist_ok=True)

    analysis = analyze.full_analysis(spec["source"])
    analysis.pop("saliency_maps", None)
    with open(os.path.join(workdir, "analysis.json"), "w") as fh:
        json.dump(analysis, fh, indent=2)

    framing = spec.get("framing", "auto")
    if framing == "auto":
        framing = analysis["framing_recommendation"]["chosen"]

    p = planmod.build_clip_plan(
        source=spec["source"], analysis=analysis, clip_id=spec["clip_id"],
        start=spec["start"], end=spec["end"], framing=framing,
        captions=spec.get("captions", []), hook=spec.get("hook"),
        logo=spec.get("logo"),
    )
    gate = compliance.validate_plan(p)
    if not gate["pass"]:
        _print({"aborted": "compliance gates failed", "gates": gate["gates"]})
        return 5

    # cover frame: sharpest, best-exposed real frame inside the clip window
    best = qa.cover_score(spec["source"], spec["start"] + 0.5)
    for cand in analysis.get("cover_candidates", []):
        if spec["start"] <= cand["t"] <= spec["end"]:
            score = qa.cover_score(spec["source"], cand["t"])
            if score["score"] > best["score"]:
                best = score
    p["qa_cover_time"] = round(best["t"] - spec["start"], 3)
    planmod.write_plan(p, os.path.join(outdir, f"{spec['clip_id']}_plan.json"))

    master = os.path.join(outdir, f"{spec['clip_id']}_MASTER_1080x1920.mp4")
    rlog = render.render(p, master, workdir, logo_path=p["logo"]["file"],
                         preset=args.preset, crf=args.crf)

    rep = qa.verify(master, p, os.path.join(outdir, "qa"))
    deliver = compliance.validate_delivery(master, p, rep)

    cover_jpg = os.path.join(outdir, f"{spec['clip_id']}_COVER.jpg")
    ff.run(["-nostdin", "-y", "-ss", f"{p['qa_cover_time']:.3f}", "-i", master,
            "-frames:v", "1", "-q:v", "2", cover_jpg])

    captions = compliance.write_captions(os.path.join(outdir, "captions"))
    manifest = {
        "clip_id": spec["clip_id"],
        "framing": framing,
        "master": master, "master_sha256": ff.sha256(master),
        "cover": cover_jpg, "cover_sha256": ff.sha256(cover_jpg),
        "duration_s": rlog["probe"]["duration_s"],
        "loudness": rlog["loudness"],
        "qa_scorecard": rep["scorecard"],
        "delivery_compliance": deliver,
        "captions": {k: {"path": v["path"], "pass": v["validation"]["pass"]}
                     for k, v in captions.items()},
    }
    with open(os.path.join(outdir, "DELIVERY_MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    _print(manifest)
    return 0 if deliver["pass"] else 6


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="vfc-director", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("doctor"); s.set_defaults(fn=cmd_doctor)

    s = sub.add_parser("acquire")
    s.add_argument("url"); s.add_argument("--outdir", default="campaign/assets_raw")
    s.add_argument("--log", default="campaign/PHASE2_ACQUISITION_LOG.json")
    s.add_argument("--name", default=None)
    s.set_defaults(fn=cmd_acquire)

    s = sub.add_parser("analyze")
    s.add_argument("source"); s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_analyze)

    s = sub.add_parser("plan")
    s.add_argument("--analysis", required=True); s.add_argument("--source", required=True)
    s.add_argument("--clip-id", required=True); s.add_argument("--start", type=float, required=True)
    s.add_argument("--end", type=float, required=True)
    s.add_argument("--framing", default="auto",
                   choices=["auto", *planmod.FRAMING_MODES])
    s.add_argument("--captions", required=True); s.add_argument("--hook", default=None)
    s.add_argument("--logo", default=None); s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_plan)

    s = sub.add_parser("render")
    s.add_argument("--plan", required=True); s.add_argument("--out", required=True)
    s.add_argument("--workdir", default="build/work"); s.add_argument("--logo", default=None)
    s.add_argument("--preset", default=None); s.add_argument("--crf", type=int, default=None)
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(fn=cmd_render)

    s = sub.add_parser("qa")
    s.add_argument("--master", required=True); s.add_argument("--plan", required=True)
    s.add_argument("--outdir", default="build/qa")
    s.set_defaults(fn=cmd_qa)

    s = sub.add_parser("captions")
    s.add_argument("--platform", default="tiktok",
                   choices=["tiktok", "instagram", "youtube_shorts"])
    s.add_argument("--outdir", default="build/captions")
    s.add_argument("--optional-copy", action="store_true")
    s.add_argument("--validate", default=None, help="path to a caption file to lint")
    s.set_defaults(fn=cmd_captions)

    s = sub.add_parser("slice")
    s.add_argument("--canvas", required=True); s.add_argument("--mode", default="9x16",
                                                             choices=["9x16", "3x4"])
    s.set_defaults(fn=cmd_slice)

    s = sub.add_parser("build")
    s.add_argument("--spec", required=True); s.add_argument("--outdir", default=None)
    s.add_argument("--preset", default="slow"); s.add_argument("--crf", type=int, default=18)
    s.set_defaults(fn=cmd_build)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
