"""Deterministic FFmpeg assembly: ASS typography, eased reframing, two-pass
EBU R128 mastering, H.264 High 4.2 delivery.

Hard rules encoded here (campaign > engine defaults where they conflict):
  * audio is the official trailer audio only - no music, no SFX, no AI voice
  * every clip carries the official logo watermark
  * every clip carries on-screen text
  * >= 10.0 s runtime
"""
from __future__ import annotations

import json
import os
import re
import subprocess

from . import ff
from .plan import ANCHORS

ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: HOOK,{font},{hook_size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,1.5,0,1,5,2,5,0,0,0,1
Style: CAPTION,{font},{cap_size},&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,1.0,0,1,4,2,5,0,0,0,1
Style: BADGE,{font},{badge_size},&H0000B8FF,&H0000B8FF,&H00000000,&H96000000,-1,0,0,0,100,100,2.5,0,1,3,0,9,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

DEFAULT_FONT = "DejaVu Sans"


def _ts(seconds: float) -> str:
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:d}:{m:02d}:{s:05.2f}"


def _ass_escape(text: str) -> str:
    """Escape everything that can terminate or corrupt an ASS dialogue line."""
    text = text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
    text = text.replace("\r", " ").replace("\n", "\\N")
    return text.strip()


# Typography is measured with the real font file, not estimated from character
# counts. A 19-character all-caps hook measured 997 px at 76 px in DejaVu Sans
# Bold (ratio 0.69) while a mixed-case line measured 0.56 - any single ratio
# overflows one of them, and the rendered master proved it.
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/DejaVuSans-Bold.ttf",
]
CHAR_WIDTH_FALLBACK = 0.66
ASS_NL = chr(92) + "N"   # ASS line break: backslash-N
MAX_TEXT_WIDTH = 900          # 1080 canvas minus editorial side margins
MIN_FONT_SIZE = 38
_FONT_CACHE: dict[int, object] = {}


def _font(size: int):
    if size in _FONT_CACHE:
        return _FONT_CACHE[size]
    try:
        from PIL import ImageFont
    except Exception:
        return None
    for path in FONT_CANDIDATES:
        if os.path.isfile(path):
            f = ImageFont.truetype(path, size)
            _FONT_CACHE[size] = f
            return f
    return None


def _text_width(text: str, size: int) -> int:
    f = _font(size)
    if f is None:
        return int(round(len(text) * CHAR_WIDTH_FALLBACK * size))
    box = f.getbbox(text)
    return int(box[2] - box[0])


def _wrap_px(text: str, size: int, max_width: int = MAX_TEXT_WIDTH) -> list[str]:
    """Greedy word wrap measured in pixels, not characters."""
    lines, cur = [], ""
    for word in text.split():
        cand = f"{cur} {word}".strip()
        if not cur or _text_width(cand, size) <= max_width:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_text(text: str, size: int, max_width: int = MAX_TEXT_WIDTH,
             max_lines: int = 3) -> tuple[list[str], int]:
    """Return (lines, font size) where the lines physically fit the canvas.

    Lines are returned unescaped so the caller can escape each one and then
    join with a live ASS \\N. Joining first and escaping afterwards doubles the
    backslash and libass renders a literal "\\N" on screen (observed).
    """
    size = max(MIN_FONT_SIZE, size)
    while size >= MIN_FONT_SIZE:
        lines = _wrap_px(text, size, max_width)
        if len(lines) <= max_lines:
            return lines, size
        size -= 4
    return _wrap_px(text, MIN_FONT_SIZE, max_width)[:max_lines], MIN_FONT_SIZE


def _ass_block(lines: list[str]) -> str:
    """Escape each line, then join with a real ASS newline directive."""
    return "\\N".join(_ass_escape(line) for line in lines)


def build_ass(plan: dict, out_path: str, font: str = DEFAULT_FONT) -> str:
    canvas = plan["framing"]["canvas"]
    hook_size = 76 if canvas["h"] == 1920 else 64
    header = ASS_HEADER.format(w=canvas["w"], h=canvas["h"], font=font,
                               hook_size=hook_size, cap_size=58, badge_size=34)
    events = []

    hook = plan["typography"].get("active_hook_text")
    if hook:
        x, y = ANCHORS["hook"]
        lines, hook_size_fit = fit_text(hook, hook_size, max_lines=2)
        text = _ass_block(lines)
        events.append(
            f"Dialogue: 1,{_ts(0.10)},{_ts(plan['window']['duration'] - 0.05)},HOOK,,0,0,0,,"
            f"{{\\an5\\pos({x},{y})\\fs{hook_size_fit}\\fad(160,180)\\blur0.6"
            f"\\t(0,140,\\fscx116\\fscy116)\\t(140,340,\\fscx100\\fscy100)}}{text}"
        )

    for cue in plan["typography"]["cues"]:
        base_size = 34 if cue["anchor"] == "badge" else 58
        max_w = 760 if cue["anchor"] == "badge" else MAX_TEXT_WIDTH
        lines, size_fit = fit_text(cue["text"], base_size, max_width=max_w, max_lines=3)
        text = _ass_block(lines)
        style = "BADGE" if cue["anchor"] == "badge" else "CAPTION"
        an = 9 if cue["anchor"] == "badge" else 5
        events.append(
            f"Dialogue: 0,{_ts(cue['t0'])},{_ts(cue['t1'])},{style},,0,0,0,,"
            f"{{\\an{an}\\pos({cue['x']},{cue['y']})\\fs{size_fit}\\fad(90,90)"
            f"\\t(0,110,\\fscx112\\fscy112)\\t(110,300,\\fscx100\\fscy100)}}{text}"
        )

    with open(out_path, "w") as fh:
        fh.write(header + "\n".join(events) + "\n")
    return out_path


def _quote(expr: str) -> str:
    return "'" + expr.replace("'", "") + "'"


def logo_geometry(logo_path: str, target_width: int) -> tuple[int, int]:
    """Real pixel height for the requested overlay width, from the file itself."""
    try:
        from PIL import Image

        with Image.open(logo_path) as im:
            w, h = im.size
        return target_width, max(2, int(round(target_width * h / w)))
    except Exception:
        return target_width, max(2, int(round(target_width * 0.55)))


SCRIM_PAD = 30      # canvas padding around the wordmark
SCRIM_MARGIN = 14   # solid plate margin beyond the wordmark box
SCRIM_ALPHA = 158   # 0.62 - the floor that keeps white text above 4.5:1
SCRIM_BLUR = 6


def make_scrim(path: str, w: int, h: int, alpha: int = SCRIM_ALPHA) -> str:
    """Rounded, feathered dark plate that sits exactly behind the watermark.

    The plate must extend past the wordmark, otherwise there is no background
    left to measure and the legs of the wordmark sit on raw footage. The first
    implementation drew the plate inside a blurred canvas and then offset it by
    the overlay position, so the sample ring landed on the video and the gate
    read 1.64:1. Geometry is now explicit: canvas = wordmark + 2*PAD, plate =
    wordmark + 2*MARGIN, overlay at (x-PAD, y-PAD).
    """
    from PIL import Image, ImageDraw, ImageFilter

    img = Image.new("RGBA", (w + 2 * SCRIM_PAD, h + 2 * SCRIM_PAD), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle(
        (SCRIM_PAD - SCRIM_MARGIN, SCRIM_PAD - SCRIM_MARGIN,
         SCRIM_PAD + w + SCRIM_MARGIN, SCRIM_PAD + h + SCRIM_MARGIN),
        radius=24, fill=(0, 0, 0, alpha),
    )
    img.filter(ImageFilter.GaussianBlur(SCRIM_BLUR)).save(path)
    return path


def build_filtergraph(plan: dict, ass_path: str, logo_path: str | None,
                      scrim_path: str | None = None) -> tuple[str, list[str]]:
    fr = plan["framing"]
    win = plan["window"]
    canvas = fr["canvas"]
    crop = fr["crop"]
    cw, ch = canvas["w"], canvas["h"]
    sw, sh = crop["scale_to"]
    inputs: list[str] = []
    parts: list[str] = []

    parts.append(
        f"[0:v]trim=start={win['start']:.3f}:end={win['end']:.3f},setpts=PTS-STARTPTS,"
        f"fps={plan['encode']['fps']}[v0]"
    )
    # A labelled stream may only be consumed once: split before fan-out, or the
    # second branch silently re-reads the untrimmed source (measured: 15.0s out
    # of a 12.0s plan, and a 4.7 LU loudness error from the appended silence).
    parts.append("[v0]split=2[vmain][vplate]")

    pan = _quote(fr["pan_expression"])
    if fr["mode"] == "9x16_punch_pan":
        p_ = fr["punch"]
        ramp = f"(1+({p_['to']}-{p_['from']})*min(t/{p_['seconds']},1))"
        w_expr = _quote(f"trunc({sw}*{ramp}/2)*2")
        h_expr = _quote(f"trunc({sh}*{ramp}/2)*2")
        parts.append(
            f"[vmain]crop={crop['w']}:{crop['h']}:{pan}:0,"
            f"scale=eval=frame:w={w_expr}:h={h_expr}:flags=lanczos,"
            f"crop={cw}:{ch},setsar=1[fg]"
        )
    else:
        parts.append(
            f"[vmain]crop={crop['w']}:{crop['h']}:{pan}:0,"
            f"scale={sw}:{sh}:flags=lanczos,setsar=1[fg]"
        )

    if fr["mode"] == "3x4_glass_card":
        bx, by = crop["overlay_xy"]
        parts.append(
            f"[vplate]scale={cw}:{ch}:force_original_aspect_ratio=increase,"
            f"crop={cw}:{ch},boxblur=30:5,eq=brightness=-0.35:saturation=0.8,setsar=1[bg]"
        )
        parts.append(f"[bg][fg]overlay={bx}:{by}:format=auto:shortest=1[card]")
        parts.append(
            f"[card]drawbox=x={bx}:y={by}:w={cw}:h={sh}:color=white@0.18:t=2[plate]"
        )
        current = "[plate]"
    else:
        current = "[fg]"

    parts.append(f"{current}ass={ass_path}[txt]")
    current = "[txt]"

    if logo_path:
        box = plan["logo"]["box"]
        idx = 1
        if scrim_path:
            inputs.append(scrim_path)
            parts.append(f"[{idx}:v]format=rgba[sc]")
            parts.append(f"{current}[sc]overlay={box['x'] - SCRIM_PAD}:{box['y'] - SCRIM_PAD}:"
                         f"format=auto:eof_action=repeat[scrimmed]")
            current = "[scrimmed]"
            idx += 1
        inputs.append(logo_path)
        parts.append(f"[{idx}:v]scale={box['w']}:-2:flags=lanczos,format=rgba[lg]")
        # eof_action=repeat holds the single-frame watermark for the whole clip.
        # shortest=1 here would end the programme at frame 1 (measured defect).
        parts.append(f"{current}[lg]overlay={box['x']}:{box['y']}:format=auto:"
                     f"eof_action=repeat[vout]")
    else:
        parts.append(f"{current}null[vout]")

    # audio: source only, high-passed; the two-pass loudnorm stage is appended
    # by render() once pass 1 has measured this exact window.
    parts.append("[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS,"
                 "highpass=f=80[aout]".format(s=win["start"], e=win["end"]))
    return ";".join(parts), inputs


def _loudnorm_stage(measured: dict, plan: dict) -> str:
    a = plan["audio"]
    return (f"loudnorm=I={a['target_lufs']}:TP={a['target_true_peak_dbtp']}:LRA=11:"
            f"measured_I={measured['input_i']}:measured_TP={measured['input_tp']}:"
            f"measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}:"
            f"offset={measured['target_offset']}:linear=true:print_format=summary")


def render(plan: dict, out_path: str, workdir: str, *, logo_path: str | None = None,
           font: str = DEFAULT_FONT, preset: str | None = None, crf: int | None = None,
           dry_run: bool = False) -> dict:
    os.makedirs(workdir, exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)

    ass_path = os.path.join(workdir, f"{plan['clip_id']}.ass")
    build_ass(plan, ass_path, font=font)

    scrim_path = None
    if logo_path and plan["logo"]["box"].get("scrim", True):
        lw, lh = logo_geometry(logo_path, plan["logo"]["box"]["w"])
        scrim_path = make_scrim(os.path.join(workdir, f"{plan['clip_id']}_scrim.png"), lw, lh)

    graph, logo_inputs = build_filtergraph(plan, os.path.abspath(ass_path),
                                           os.path.abspath(logo_path) if logo_path else None,
                                           os.path.abspath(scrim_path) if scrim_path else None)

    # ---- pass 1: measure the exact audio window we will ship ---------------
    win = plan["window"]
    measured_raw = ff.loudnorm_pass1(
        plan["source"]["path"], win["start"], win["end"],
        target_i=plan["audio"]["target_lufs"],
        target_tp=plan["audio"]["target_true_peak_dbtp"],
        prefix="highpass=f=80",
    )
    measured = {
        "input_i": measured_raw["input_i"],
        "input_tp": measured_raw["input_tp"],
        "input_lra": measured_raw["input_lra"],
        "input_thresh": measured_raw["input_thresh"],
        "target_offset": measured_raw["target_offset"],
    }
    if "highpass=f=80[aout]" not in graph:
        raise RuntimeError("audio tail of the filtergraph changed shape; refusing to guess")
    graph = graph.replace(
        "highpass=f=80[aout]",
        "highpass=f=80," + _loudnorm_stage(measured, plan) + "[aout]",
    )

    cmd = ["-nostdin", "-y", "-i", plan["source"]["path"]]
    for extra in logo_inputs:
        cmd += ["-i", extra]
    cmd += [
        "-filter_complex", graph,
        "-map", "[vout]", "-map", "[aout]",
        "-c:v", "libx264", "-profile:v", "high", "-level", "4.2",
        "-pix_fmt", "yuv420p", "-crf", str(crf if crf is not None else plan["encode"]["crf"]),
        "-preset", preset or plan["encode"]["preset"],
        "-g", str(int(round(plan["encode"]["fps"] * 2))),
        "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-max_muxing_queue_size", "1024",
        out_path,
    ]
    log = {"pass1_measured": measured_raw, "filter_complex": graph,
           "command": " ".join(["ffmpeg", *cmd]), "output": os.path.abspath(out_path)}

    if dry_run:
        log["dry_run"] = True
        return log

    proc = ff.run(cmd, timeout=3600)
    log["ffmpeg_exit"] = proc.returncode
    log["stderr_tail"] = proc.stderr[-1200:]
    if not os.path.isfile(out_path) or os.path.getsize(out_path) < 1024:
        raise ff.FFmpegError(f"render produced no usable file: {out_path}\n{proc.stderr[-2000:]}")
    log["bytes"] = os.path.getsize(out_path)
    log["probe"] = ff.probe(out_path, count_frames=True).to_dict()
    log["loudness"] = ff.measure_loudness(out_path)
    with open(os.path.join(workdir, f"{plan['clip_id']}_render_log.json"), "w") as fh:
        json.dump(log, fh, indent=2)
    return log


def slice_commands(canvas_path: str, mode: str = "9x16") -> list[str]:
    """Phase 7 lossless extraction one-liners for a dual-nest canvas."""
    if mode == "9x16":
        return [
            f'ffmpeg -i {canvas_path} -filter:v "crop=608:1080:176:0" -c:a copy clip_1_extracted.mp4',
            f'ffmpeg -i {canvas_path} -filter:v "crop=608:1080:1136:0" -c:a copy clip_2_extracted.mp4',
        ]
    return [
        f'ffmpeg -i {canvas_path} -filter:v "crop=810:1080:76:0" -c:a copy clip_1_extracted.mp4',
        f'ffmpeg -i {canvas_path} -filter:v "crop=810:1080:1036:0" -c:a copy clip_2_extracted.mp4',
    ]
