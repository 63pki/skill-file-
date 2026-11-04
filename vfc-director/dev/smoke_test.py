"""Self-verifying suite for the render engine, run against a SYNTHETIC fixture.

    python3 dev/smoke_test.py            # full run (encodes a 10 s master)
    python3 dev/smoke_test.py --fast     # skip the encode, structure only

Every assertion here exists because something actually broke during the build:
untimed branches, single-frame overlays, literal \\N on screen, a 4.7 LU
loudness miss, and a character-count text fitter that overflowed the canvas.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
sys.path.insert(0, PKG)

from engine import analyze, compliance, ff, plan as planmod, qa, render  # noqa: E402
from engine.render import _text_width, fit_text  # noqa: E402

BUILD = os.path.join(PKG, "build")
FIXTURE = os.path.join(BUILD, "fixture_16x9.mp4")
LOGO = os.path.join(BUILD, "fixture_logo.png")
CHECKS: list[dict] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    CHECKS.append({"name": name, "pass": bool(cond), "detail": detail})
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail and not cond else ""))


def expect_raises(name: str, fn, needle: str = "") -> None:
    try:
        fn()
    except Exception as exc:
        check(name, needle.lower() in str(exc).lower(), f"{type(exc).__name__}: {exc}")
        return
    check(name, False, "no exception raised")


def main(fast: bool = False) -> int:
    os.makedirs(BUILD, exist_ok=True)

    # ---------------------------------------------------------------- doctor
    caps = ff.capabilities()
    check("ffmpeg has libx264", caps["encoders"]["libx264"], caps["ffmpeg"])
    for filt in ("ass", "crop", "overlay", "loudnorm", "ebur128", "boxblur", "split"):
        check(f"filter available: {filt}", caps["filters"][filt])

    # --------------------------------------------------------------- fixture
    if not os.path.isfile(FIXTURE):
        from dev.make_fixture import make  # type: ignore

        make(FIXTURE)
    if not os.path.isfile(LOGO):
        ff.run(["-nostdin", "-y", "-f", "lavfi", "-i", "color=c=black@0.0:s=440x120,format=rgba",
                "-vf", "drawtext=text='VFC TEST LOGO':fontcolor=white:fontsize=34:"
                       "x=(w-tw)/2:y=(h-th)/2:box=1:boxcolor=black@0.55:boxborderw=10",
                "-frames:v", "1", LOGO])

    info = ff.probe(FIXTURE, count_frames=True)
    check("fixture is 16:9 1080p", (info.video.width, info.video.height) == (1920, 1080),
          f"{info.video.width}x{info.video.height}")
    check("fixture duration measured", abs(info.duration_s - 15.0) < 0.1, str(info.duration_s))
    check("fixture frame count measured by decoding", info.frame_count and info.frame_count > 400,
          str(info.frame_count))
    check("fixture has audio", bool(info.audio))

    # -------------------------------------------------------------- analysis
    a = analyze.full_analysis(FIXTURE)
    check("analysis found cuts", len(a["cuts"]) >= 1, str(len(a["cuts"])))
    check("analysis decoded audio", a["audio"]["decoded_seconds"] > 14.0,
          str(a["audio"]["decoded_seconds"]))
    check("analysis found transients", a["audio"]["transient_count"] > 0,
          str(a["audio"]["transient_count"]))
    check("framing audit is computed", "framing_recommendation" in a,
          str(a.get("framing_recommendation")))
    check("9:16 horizontal field is 31.6%",
          a["framing_audit"]["9x16_full_bleed"]["horizontal_field_kept_pct"] == 31.6,
          str(a["framing_audit"]["9x16_full_bleed"]["horizontal_field_kept_pct"]))

    # ----------------------------------------------------------------- plan
    cues = [{"text": "A city you've never seen", "t0": 1.2, "t1": 3.0},
            {"text": "A totally new Virtua Fighter", "t0": 5.0, "t1": 7.4}]
    p = planmod.build_clip_plan(source=FIXTURE, analysis=a, clip_id="SMOKE_TEST",
                                start=1.0, end=11.0, framing="3x4_glass_card",
                                captions=cues, hook="A story you've never heard", logo=LOGO)
    check("plan window is 10.0 s", p["window"]["duration"] == 10.0, str(p["window"]["duration"]))
    check("plan gates all true", all(p["gates"].values()), str(p["gates"]))
    check("pan keyframes are even pixels",
          all(k["x"] % 2 == 0 for k in p["framing"]["pan_keyframes"]))
    check("caption anchors inside safe zone",
          all(c["safe_zone_ok"] for c in p["typography"]["cues"]))
    check("caption density under 220 wpm",
          all(c["wpm"] <= 220 for c in p["typography"]["cues"]),
          str([c["wpm"] for c in p["typography"]["cues"]]))

    expect_raises("under-10s window is refused",
                  lambda: planmod.build_clip_plan(source=FIXTURE, analysis=a, clip_id="SHORT",
                                                 start=1.0, end=9.0, framing="9x16_full_bleed",
                                                 captions=cues),
                  "10.0s")

    # ------------------------------------------------------------ typography
    for text in ("SYNTHETIC TEST HOOK", "A totally new Virtua Fighter",
                 "Lionel Rafale vs Cielo", "In Virtua Fighter Crossroads"):
        lines, size = fit_text(text, 76, max_lines=2)
        widest = max(_text_width(line, size) for line in lines)
        check(f"text fits canvas: {text[:24]}", widest <= 900, f"{widest}px at {size}px")

    # ----------------------------------------------------------- filtergraph
    graph, extras = render.build_filtergraph(p, "/tmp/x.ass", LOGO)
    check("graph splits the trimmed stream", "split=2" in graph)
    check("logo overlay repeats instead of truncating",
          "eof_action=repeat" in graph and "shortest=1[vout]" not in graph)
    check("logo is a second input", len(extras) == 1)
    check("audio is source-only (no synth inputs)", graph.count("[0:a]") == 1)

    # -------------------------------------------------------------- captions
    good = compliance.build_caption("tiktok")
    check("canonical caption passes its own validator",
          compliance.validate_caption(good, "tiktok")["pass"])
    bad = good.replace("A city you've never seen", "A city like no other")
    check("reworded caption is rejected",
          not compliance.validate_caption(bad, "tiktok")["pass"])
    check("missing FTC disclosure is rejected",
          not compliance.validate_caption(good.replace("#Ad", ""), "tiktok")["pass"])
    check("wrong platform tag is rejected",
          not compliance.validate_caption(good, "youtube_shorts")["pass"])
    check("YT caption uses @SEGA_West",
          "@SEGA_West" in compliance.build_caption("youtube_shorts"))
    check("hype copy is rejected",
          not compliance.validate_caption(good + "\nINSANE best game ever", "tiktok")["pass"])

    if fast:
        summary = {"checks": len(CHECKS), "failed": [c["name"] for c in CHECKS if not c["pass"]]}
        print(json.dumps(summary, indent=2))
        return 0 if not summary["failed"] else 1

    # --------------------------------------------------------------- render
    work = os.path.join(BUILD, "smoke_work")
    master = os.path.join(BUILD, "SMOKE_TEST_MASTER.mp4")
    log = render.render(p, master, work, logo_path=LOGO, preset="veryfast")
    probe = log["probe"]
    check("master is 1080x1920",
          (probe["video"]["width"], probe["video"]["height"]) == (1080, 1920),
          f"{probe['video']['width']}x{probe['video']['height']}")
    check("master duration matches plan", abs(probe["duration_s"] - 10.0) < 0.12,
          str(probe["duration_s"]))
    check("master frame count is ~300", probe["frame_count"] is not None
          and abs(probe["frame_count"] - 300) <= 3, str(probe["frame_count"]))
    check("master is yuv420p", probe["video"]["pix_fmt"] == "yuv420p", str(probe["video"]["pix_fmt"]))
    check("master is H.264 High", qa._is_h264_high(master))
    check("master is faststart", qa._has_faststart(master))
    lufs = log["loudness"]["integrated_lufs"]
    check("integrated loudness -14.0 +/- 0.5 LUFS", abs(lufs + 14.0) <= 0.5, str(lufs))
    check("true peak under -1.0 dBTP", log["loudness"]["true_peak_dbfs"] <= -1.0,
          str(log["loudness"]["true_peak_dbfs"]))
    check("single audio stream", len([s for s in probe["streams"] if s["kind"] == "Audio"]) == 1)

    rep = qa.verify(master, p, os.path.join(BUILD, "smoke_qa"))
    check("QA finds no black frames", rep["checks"]["no_black_frames"])
    check("QA finds no stuck freezes", rep["checks"]["no_stuck_freezes"])
    deliver = compliance.validate_delivery(master, p, rep)
    check("delivery compliance 10/10", deliver["pass"], json.dumps(deliver["failed_checks"]))

    results = {
        "passed": sum(1 for c in CHECKS if c["pass"]),
        "failed": sum(1 for c in CHECKS if not c["pass"]),
        "checks": CHECKS,
        "master": {"path": master, "duration_s": probe["duration_s"],
                   "frames": probe["frame_count"], "lufs": lufs,
                   "true_peak": log["loudness"]["true_peak_dbfs"]},
    }
    with open(os.path.join(HERE, "SMOKE_RESULTS.json"), "w") as fh:
        json.dump(results, fh, indent=2)
    print(json.dumps({k: results[k] for k in ("passed", "failed", "master")}, indent=2))
    return 0 if results["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(fast="--fast" in sys.argv))
