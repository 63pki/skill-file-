"""
Spatial typography + watermark compositor (CPU only, PIL).

Renders transparent PNG overlay plates that render.py flips on/off with FFmpeg
`enable='between(t,a,b)'`. Generating plates in PIL (rather than raw drawtext)
buys real kerning control, letter-tracking, glassmorphic pills, specular strokes
and the 3px feathered outline required by CCM §3 — and it keeps every text
string out of the FFmpeg filtergraph, so colon/quote escaping can never break
the render (CCM §1.3 Text Escaping Invariant is satisfied by construction).

Every plate reports its pixel bbox so qa.py can assert safe-zone clearance
analytically instead of eyeballing a frame.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from . import campaign as C

FONT_DIR = Path("vendor/fonts")


# ---------------------------------------------------------------- text engine
@dataclass
class TextStyle:
    font: str = str(FONT_DIR / "Montserrat-ExtraBold.ttf")
    size: int = 89
    tracking: int = 2
    color: tuple = C.INK_RGB + (255,)
    stroke: int = 8


def _font(style: TextStyle, size: int | None = None) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(style.font, size or style.size)


def measure(text: str, style: TextStyle) -> tuple[int, int]:
    f = _font(style)
    w = 0
    for ch in text:
        w += f.getlength(ch) + style.tracking
    w = max(0, w - style.tracking)
    asc, desc = f.getmetrics()
    return int(w), asc + desc


def draw_tracked(draw: ImageDraw.ImageDraw, xy, text: str, style: TextStyle,
                 soft_outline: bool = True) -> None:
    """Draw with letter-tracking and a multi-pass feathered dark outline."""
    f = _font(style)
    x, y = xy
    passes = []
    if soft_outline and style.stroke:
        # wide+transparent -> narrow+opaque  == feathered edge
        passes = [(style.stroke, (0, 0, 0, 70)),
                  (int(style.stroke * 0.75), (0, 0, 0, 130)),
                  (int(style.stroke * 0.5), (0, 0, 0, 210))]
    for width, col in passes:
        cx = x
        for ch in text:
            draw.text((cx, y), ch, font=f, fill=col,
                      stroke_width=max(1, width // 2), stroke_fill=col)
            cx += f.getlength(ch) + style.tracking
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=f, fill=style.color)
        cx += f.getlength(ch) + style.tracking


# ---------------------------------------------------------------- watermark
def logo_plate(width: int, canvas_w: int) -> tuple[Image.Image, dict]:
    """
    Official logo watermark (CCM: mandatory on every clip).
    Scaled to `width`, given a soft drop shadow for contrast on bright footage,
    and returned with its placement bbox on the canvas.
    """
    src = Image.open(C.LOGO_PATH).convert("RGBA")
    bbox = src.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox()
    src = src.crop(bbox)                      # trim dead margin
    ratio = width / src.width
    logo = src.resize((width, int(src.height * ratio)), Image.LANCZOS)

    pad = 18
    shadow = Image.new("RGBA", (logo.width + pad * 2, logo.height + pad * 2), (0, 0, 0, 0))
    if C.LOGO_SHADOW:
        sh = Image.new("RGBA", shadow.size, (0, 0, 0, 0))
        alpha = logo.split()[3].point(lambda v: int(v * 0.62))
        black = Image.new("RGBA", logo.size, (0, 0, 0, 255))
        sh.paste(black, (pad, pad), alpha)
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        shadow = Image.alpha_composite(shadow, sh)
    shadow.alpha_composite(logo, (pad, pad))

    x = (canvas_w - shadow.width) // 2
    # The plate carries its own transparent shadow margin, so the *plate* is
    # pinned exactly on the safe line and the visible mark sits below it.
    y = C.LOGO_TOP_Y
    return shadow, {"x": x, "y": y, "w": shadow.width, "h": shadow.height}


# ---------------------------------------------------------------- captions
def _wrap(words: list[str], style_bold: TextStyle, max_w: int) -> list[str]:
    f = _font(style_bold)
    lines, cur = [], []
    for w in words:
        trial = " ".join(cur + [w])
        tw = sum(f.getlength(ch) + style_bold.tracking for ch in trial) - style_bold.tracking
        if tw > max_w and cur:
            lines.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(" ".join(cur))
    return lines


def caption_plate(text: str, canvas_w: int, canvas_h: int,
                  accent: tuple = C.ACCENT_RGB,
                  anchor_y: int | None = None,
                  uppercase: bool = True) -> tuple[Image.Image, dict]:
    """
    One caption burst: glass pill + feathered outline + accent spine.
    Returns (RGBA plate the size of the canvas, bbox dict in canvas coords).
    """
    text = text.upper() if uppercase else text
    size = int(canvas_w * C.CAPTION_SIZE_RATIO)
    style = TextStyle(size=size, tracking=C.CAPTION_TRACKING)

    # Hard width budget: the finished plate (text + pill padding + shadow
    # margin) must fit inside BOTH the left and right platform safe margins.
    pad_x, pad_y, bleed = 46, 30, 20
    safe_w = canvas_w - C.SAFE_ZONES["left"] - C.SAFE_ZONES["right"]
    usable = safe_w - pad_x * 2 - bleed * 2
    lines = _wrap(text.split(), style, usable)

    f = _font(style)
    asc, desc = f.getmetrics()
    line_h = int((asc + desc) * 1.16)
    text_w = max(
        int(sum(f.getlength(ch) + style.tracking for ch in ln) - style.tracking)
        for ln in lines
    )

    box_w, box_h = text_w + pad_x * 2, line_h * len(lines) + pad_y * 2

    plate = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    layer = Image.new("RGBA", (box_w + bleed * 2, box_h + bleed * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    ox, oy = bleed, bleed
    radius = 20
    d.rounded_rectangle([ox, oy, ox + box_w, oy + box_h], radius=radius,
                        fill=C.GLASS_RGBA, outline=(255, 255, 255, 46), width=2)
    # accent spine (brand terracotta sampled from the official logo)
    d.rounded_rectangle([ox, oy, ox + 8, oy + box_h], radius=4, fill=accent + (255,))

    ty = oy + pad_y
    for ln in lines:
        lw = int(sum(f.getlength(ch) + style.tracking for ch in ln) - style.tracking)
        draw_tracked(d, (ox + pad_x + (text_w - lw) // 2, ty), ln, style)
        ty += line_h

    x = max(C.SAFE_ZONES["left"], min((canvas_w - layer.width) // 2,
                                      canvas_w - C.SAFE_ZONES["right"] - layer.width))
    y = anchor_y if anchor_y is not None else C.CAPTION_ZONE_Y[0]
    if canvas_h != 1920:  # scale anchor band for 3:4 / other canvases
        y = int(y * canvas_h / 1920)
    bottom_limit = canvas_h - int(C.SAFE_ZONES["bottom"] * canvas_h / 1920)
    y = max(C.SAFE_ZONES["top"], min(y, bottom_limit - layer.height))

    plate.alpha_composite(layer, (max(0, x), max(0, y)))
    bbox = {"x": int(x), "y": int(y), "w": layer.width, "h": layer.height}
    return plate, bbox


def step_badge(index: int, total: int, canvas_w: int, accent: tuple = C.ACCENT_RGB
               ) -> tuple[Image.Image, dict]:
    """[STEP 01/03] floating glass pill for enumerated points."""
    txt = f"STEP {index:02d}/{total:02d}"
    size = int(canvas_w * 0.030)
    style = TextStyle(size=size, tracking=6, stroke=0)
    f = _font(style)
    tw = int(sum(f.getlength(ch) + style.tracking for ch in txt) - style.tracking)
    asc, desc = f.getmetrics()
    w, h = tw + 64, asc + desc + 34
    badge = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(badge)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=accent + (230,))
    x = (w - tw) // 2
    for ch in txt:
        d.text((x, 17), ch, font=f, fill=(255, 255, 255, 255))
        x += f.getlength(ch) + style.tracking
    plate = Image.new("RGBA", (canvas_w, 1920), (0, 0, 0, 0))
    bbox = {"x": (canvas_w - w) // 2, "y": C.SAFE_ZONES["top"] + 96, "w": w, "h": h}
    plate.alpha_composite(badge, (bbox["x"], bbox["y"]))
    return plate, bbox


def accent_from_logo() -> tuple:
    """Re-derive brand accent from the official logo at runtime (no hardcode drift)."""
    im = Image.open(C.LOGO_PATH).convert("RGBA")
    from collections import Counter
    c = Counter()
    for r, g, b, a in im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata():
        if a > 200 and not (abs(r - g) < 12 and abs(g - b) < 12):
            c[(r // 8 * 8, g // 8 * 8, b // 8 * 8)] += 1
    return c.most_common(1)[0][0] if c else C.ACCENT_RGB
