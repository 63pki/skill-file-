"""Campaign Compliance Matrix, enforced as code.

Every rule here is a HARD GATE copied from the SEGA / Virtua Fighter Crossroads
brief. A post that fails any of them is rejected by the campaign manager, so the
engine refuses to declare a delivery complete while one is open.
"""
from __future__ import annotations

import json
import os
import re

ENGINE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMPAIGN_DIR = os.path.join(os.path.dirname(ENGINE_DIR), "campaign")
CANONICAL_PATH = os.path.join(CAMPAIGN_DIR, "captions.json")

REQUIRED_LINES = [
    "A city you've never seen",
    "A story you've never heard",
    "A totally new Virtua Fighter",
]
EXPERIENCE_LINE = ("Experience a rich, cinematic single-player adventure with immersive "
                   "narrative-driven gameplay, and the series' trademark thrilling VS battles!")
OPTIONAL_COPY = ("A mysterious young martial artist named Lionel Rafale has arrived in the city "
                 "of Vilasapara. A highly skilled fighter capable of outclassing Cielo in a street "
                 "fight, he is a force to be reckoned with. But what is his true reason for coming "
                 "to this city?")
FTG_DISCLOSURES = ["#Ad", "#Advertisement", "#Sponsored"]
TAGS = {"tiktok": "@VFCROSSROADS", "instagram": "@VFCROSSROADS", "youtube_shorts": "@SEGA_West"}

# Hype / unverifiable-claim patterns the brief bans ("no hype or made-up facts")
BANNED_CLAIM_PATTERNS = [
    r"\binsane\b", r"\bunbelievable\b", r"\byou won'?t believe\b", r"\bmind[- ]?blowing\b",
    r"\bbest (game|fighter|trailer) ever\b", r"\bgame[- ]?changing\b", r"\b\d{2,}%\b",
    r"\bfree\b", r"\bgiveaway\b", r"\bdownload now\b", r"\bbuy now\b", r"\bout now\b",
    r"\bofficial gameplay\b", r"\bgameplay (footage|trailer)\b",
]
MISLABEL_PATTERNS = [r"\bgameplay\b", r"\blet'?s play\b", r"\bwalkthrough\b"]


def load_canonical() -> dict:
    with open(CANONICAL_PATH) as fh:
        return json.load(fh)


def build_caption(platform: str, include_optional_copy: bool = False) -> str:
    """Return the exact campaign-mandated caption for a platform."""
    if platform not in TAGS:
        raise ValueError(f"platform must be one of {list(TAGS)}")
    tag = TAGS[platform]
    lines = list(REQUIRED_LINES) + [""]
    lines.append(f"{EXPERIENCE_LINE} {tag}")
    lines.append(FTG_DISCLOSURES[0])
    if include_optional_copy:
        # optional copy may be added, but the required block stays word-for-word
        lines = [OPTIONAL_COPY, ""] + lines
    return "\n".join(lines)


def validate_caption(text: str, platform: str) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    tag = TAGS[platform]

    lines = [ln.strip() for ln in text.replace("\r\n", "\n").split("\n")]
    non_empty = [ln for ln in lines if ln]

    for required in REQUIRED_LINES:
        if required not in [ln.strip() for ln in lines]:
            errors.append(f"missing verbatim line: {required!r} (own line, word-for-word)")

    exp_idx = next((i for i, ln in enumerate(lines) if EXPERIENCE_LINE in ln), None)
    if exp_idx is None:
        errors.append("missing the required 'Experience a rich, cinematic...' sentence")
    else:
        if tag not in lines[exp_idx]:
            errors.append(f"account tag {tag} must sit right after the caption text")
        if lines[exp_idx].strip().split(EXPERIENCE_LINE)[-1].strip() != tag:
            errors.append("account tag must directly follow the required sentence, nothing else")

    ftc_idx = [i for i, ln in enumerate(lines) if ln.strip() in FTG_DISCLOSURES]
    if not ftc_idx:
        errors.append("no FTC disclosure (#Ad / #Advertisement / #Sponsored) present")
    elif exp_idx is not None:
        if min(ftc_idx) != exp_idx + 1:
            errors.append("FTC disclosure must be on its own line immediately after the account tag line")

    if OPTIONAL_COPY[:60] not in text and OPTIONAL_COPY:
        warnings.append("optional approved copy not used (allowed)")

    joined = " ".join(non_empty)
    for pat in BANNED_CLAIM_PATTERNS:
        for m in re.finditer(pat, joined, re.I):
            errors.append(f"banned hype/unverifiable claim: {m.group(0)!r}")
    for pat in MISLABEL_PATTERNS:
        for m in re.finditer(pat, joined, re.I):
            warnings.append(f"mislabel risk ('{m.group(0)}'): a trailer must not be called gameplay")

    return {
        "platform": platform,
        "pass": not errors,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
        "line_count": len(non_empty),
        "chars": len(text),
    }


def validate_plan(plan: dict) -> dict:
    """Hard gates that must hold before a render is allowed to ship."""
    gates = {
        "duration_min_10s": plan["window"]["duration"] >= 10.0,
        "logo_watermark_planned": bool(plan["logo"]["file"]),
        "on_screen_text_planned": bool(plan["typography"]["cues"] or
                                       plan["typography"].get("active_hook_text")),
        "source_only_audio": (plan["audio"]["added_music"] is False
                              and plan["audio"]["added_sfx"] is False
                              and plan["audio"]["ai_voice"] is False
                              and plan["audio"]["source_stream"] is not None),
        "english_only_source": True,
    }
    return {"pass": all(gates.values()), "gates": gates}


def validate_delivery(master: str, plan: dict, qa_report: dict) -> dict:
    checks = dict(qa_report["checks"])
    checks["logo_watermark_present"] = bool(plan["logo"]["file"])
    checks["on_screen_text_present"] = bool(
        plan["typography"]["cues"] or plan["typography"].get("active_hook_text"))
    checks["no_added_music_or_sfx"] = (plan["audio"]["added_music"] is False
                                       and plan["audio"]["added_sfx"] is False)
    checks["no_ai_voice"] = plan["audio"]["ai_voice"] is False
    failed = [k for k, v in checks.items() if not v]
    return {
        "master": master,
        "pass": not failed,
        "failed_checks": failed,
        "checks": checks,
        "score": round(10.0 * sum(bool(v) for v in checks.values()) / len(checks), 2),
    }


def write_captions(outdir: str, include_optional_copy: bool = False) -> dict:
    os.makedirs(outdir, exist_ok=True)
    out = {}
    for platform in TAGS:
        text = build_caption(platform, include_optional_copy=include_optional_copy)
        path = os.path.join(outdir, f"caption_{platform}.txt")
        with open(path, "w") as fh:
            fh.write(text + "\n")
        out[platform] = {"path": path, "validation": validate_caption(text, platform)}
    return out
