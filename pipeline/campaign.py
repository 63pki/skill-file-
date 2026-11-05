"""
Campaign Compliance Matrix (CCM) — SEGA / Virtua Fighter Crossroads — Lionel Rafale.

Every constant in this module is transcribed verbatim from the official campaign
brief (see docs/CCM.md for the signed Phase 1 table). These are HARD GATES:
render.py and qa.py refuse to emit a PASS verdict if any of them is violated.
"""

CAMPAIGN = "VFC"
TALENT = "Lionel Rafale"
GAME = "VIRTUA FIGHTER CROSSROADS"

# ---------------------------------------------------------------------------
# 1. EXACT CAPTION (verbatim, word-for-word, do not reword — brief §CAPTION)
# ---------------------------------------------------------------------------
# Note the U+2019 right single quote in "series’" — intentional, preserved.
CAPTION_BODY = (
    "A mysterious young martial artist named Lionel Rafale has arrived in the "
    "city of Vilasapara. A highly skilled fighter capable of outclassing Cielo "
    "in a street fight, he is a force to be reckoned with. But what is his true "
    "reason for coming to this city?"
)

CAPTION_REQUIRED_STANZAS = [
    "A city you've never seen",
    "A story you've never heard",
    "A totally new Virtua Fighter",
]

CAPTION_CLOSER = (
    "Experience a rich, cinematic single-player adventure with immersive "
    "narrative-driven gameplay, and the series\u2019 trademark thrilling VS battles!"
)

ACCOUNT_TAGS = {
    "tiktok": "@VFCROSSROADS",
    "instagram": "@VFCROSSROADS",
    "youtube": "@SEGA_West",   # brief: on Shorts tag @SEGA_West instead
}

FTC_DISCLOSURES = ["#Ad", "#Advertisement", "#Sponsored"]
FTC_REQUIRED = "#Ad"

# ---------------------------------------------------------------------------
# 2. HARD PROHIBITIONS (from brief §NOT ALLOWED)
# ---------------------------------------------------------------------------
# Terms banned EVERYWHERE (caption + burned-in text).
PROHIBITED_TERMS = [
    # brief: "Exaggerated hooks, rage bait, or hate bait"
    "you won't believe", "insane", "shocking", "unbelievable", "mind-blowing",
    "100%", "guaranteed", "best ever", "must see", "must-see",
    # brief: "False or made-up claims, stats, or dates"
    "free", "giveaway", "leak", "leaked", "exclusive reveal",
    # brief: "Political content, or content about race or gender"
    "political", "election", "race", "gender",
    # brief: "AI voiceovers or AI-generated voices"
    "ai voice", "ai narration",
]

# Terms banned in BURNED-IN TEXT ONLY.
# Resolution of a real CCM conflict: the brief bans "mislabeling the content
# (a trailer is not 'gameplay')", yet the *required, verbatim, unalterable*
# caption copy says "immersive narrative-driven gameplay". The verbatim caption
# wins (it must not be changed); the mislabel ban is therefore enforced where
# the editor has discretion — the on-screen text burned into the clip.
MISLABEL_TERMS = [
    "gameplay", "game play", "walkthrough", "playthrough", "let's play",
    "live gameplay", "actual gameplay", "gameplay footage", "hands-on",
]

ALLOWED_AUDIO_SOURCES = ["official_trailer_audio"]
FORBIDDEN_AUDIO = ["background_music", "added_music", "trending_sound", "sfx_bed", "ai_voice"]

MIN_DURATION_S = 10.0
MAX_DURATION_S = 60.0
LANGUAGE = "en"

# ---------------------------------------------------------------------------
# 3. BRAND + SPATIAL SPECS
# ---------------------------------------------------------------------------
LOGO_PATH = "assets/brand/snake_logo_w.png"
# Brand accent sampled programmatically from the official logo's "V" glyph
# (dominant non-greyscale cluster, 48,553 px): #A84828 terracotta.
ACCENT_HEX = "#A84828"
ACCENT_RGB = (168, 72, 40)
INK_RGB = (255, 255, 255)
GLASS_RGBA = (15, 15, 15, 191)      # rgba(15,15,15,0.75)

# Platform UI safe zones (px @ 1080x1920 reference height)
SAFE_ZONES = {
    "top": 260,      # clear of platform top chrome
    "bottom": 420,   # clear of caption/CTA rail
    "right": 140,    # clear of like/share/comment rail
    "left": 60,
}

# Logo watermark
LOGO_WIDTH_RATIO = 0.28     # of canvas width  -> 302px @1080
LOGO_TOP_Y = 272            # sits 12px below the 260px top safe line
LOGO_SHADOW = True

# Caption typography
CAPTION_FONT = "vendor/fonts/Montserrat-ExtraBold.ttf"
CAPTION_SIZE_RATIO = 0.082  # of canvas width -> ~89px @1080
CAPTION_TRACKING = 2
CAPTION_ZONE_Y = (1180, 1420)   # 9:16 reference; collarbone safe band
MAX_WORDS_PER_BURST = 4
MAX_WPM_READING = 220

# Delivery encode spec (brief §POST SPECS: "high-quality posts only")
ENCODE = {
    "vcodec": "libx264",
    "profile": "high",
    "level": "4.2",
    "preset": "slow",
    "crf": "18",
    "pix_fmt": "yuv420p",
    "movflags": "+faststart",
    "acodec": "aac",
    "abitrate": "320k",
    "ar": "48000",
}
LOUDNESS = {"I": -14.0, "TP": -1.0, "LRA": 11.0}


# ---------------------------------------------------------------------------
# 4. Builders + validators
# ---------------------------------------------------------------------------
def build_caption(platform: str) -> str:
    """Assemble the exact required caption layout for a platform."""
    platform = platform.lower()
    if platform not in ACCOUNT_TAGS:
        raise ValueError(f"unknown platform {platform!r}")
    tag = ACCOUNT_TAGS[platform]
    return "\n".join([
        CAPTION_BODY,
        "",
        *CAPTION_REQUIRED_STANZAS,
        "",
        f"{CAPTION_CLOSER} {tag}",
        FTC_REQUIRED,
    ])


def validate_caption(text: str, platform: str = "tiktok") -> list[str]:
    """Return a list of hard-gate failures (empty list == PASS)."""
    fails: list[str] = []
    if CAPTION_BODY not in text:
        fails.append("CCM-CAPTION: required body text altered or missing")
    for line in CAPTION_REQUIRED_STANZAS:
        if line not in text:
            fails.append(f"CCM-CAPTION: required line missing -> {line!r}")
    if CAPTION_CLOSER not in text:
        fails.append("CCM-CAPTION: required closer altered or missing")
    tag = ACCOUNT_TAGS[platform.lower()]
    if tag not in text:
        fails.append(f"CCM-TAG: required account tag missing -> {tag}")
    if not any(d in text for d in FTC_DISCLOSURES):
        fails.append("CCM-FTC: no FTC disclosure present")
    low = text.lower()
    for term in PROHIBITED_TERMS:
        if term in low:
            fails.append(f"CCM-PROHIBITED: banned term present -> {term!r}")
    return fails


def validate_onscreen_text(text: str) -> list[str]:
    """Validate a burned-in on-screen text string against campaign law."""
    fails: list[str] = []
    low = text.lower()
    for term in PROHIBITED_TERMS:
        if term in low:
            fails.append(f"CCM-ONSCREEN: banned term -> {term!r}")
    for term in MISLABEL_TERMS:
        if term in low:
            fails.append(f"CCM-ONSCREEN: trailer mislabeled as gameplay -> {term!r}")
    if not text.strip():
        fails.append("CCM-ONSCREEN: on-screen text is mandatory on every post")
    words = len(text.split())
    if words > MAX_WORDS_PER_BURST:
        fails.append(
            f"CCM-DENSITY: {words} words exceeds {MAX_WORDS_PER_BURST}-word burst ceiling"
        )
    if any(ord(c) > 0x2500 for c in text):
        fails.append("CCM-LANG: non-English / emoji glyph detected")
    return fails


if __name__ == "__main__":
    for p in ("tiktok", "instagram", "youtube"):
        cap = build_caption(p)
        print(f"--- {p.upper()} ---")
        print(cap)
        print("VALIDATION:", validate_caption(cap, p) or "PASS (all hard gates)")
        print()
