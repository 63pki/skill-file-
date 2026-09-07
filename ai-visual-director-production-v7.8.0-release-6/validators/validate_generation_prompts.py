#!/usr/bin/env python3
"""Fail-closed universal prompt validation for all four modes."""
import re


def norm(value):
    return re.sub(r"[^A-Z0-9]+", "_", str(value).upper()).strip("_")


def issue(errors, code, message, **extra):
    errors.append({"code": code, "message": message, **extra})


def validate(contract, output, errors):
    mode = norm(contract.get("mode"))
    tools = contract.get("tools", {}) if isinstance(contract.get("tools"), dict) else {}
    if mode not in {"A_PHOTOREAL_COMMERCIAL", "B_ANIMATION", "C_MOTION_GRAPHICS", "D_HYBRID_COMPOSITING"}:
        return
    if norm(tools.get("stillGeneration")) != "NANO_BANANA_PRO":
        issue(errors, "STILL_OWNER_DRIFT", str(tools.get("stillGeneration")))
    video = norm(tools.get("videoGeneration", "GEMINI_OMNI_FLASH"))
    if video not in {"GEMINI_OMNI_FLASH", "NONE", "NOT_REQUIRED"}:
        issue(errors, "VIDEO_OWNER_DRIFT", str(tools.get("videoGeneration")))

    text = "\n".join(str(a.get("body", "")) for a in output.get("artifacts", []) if isinstance(a, dict))
    image_blocks = re.findall(r"<!--\s*AVD:NANO_PROMPT\s+([^>]*)-->(.*?)<!--\s*/AVD:NANO_PROMPT\s*-->", text, re.I | re.S)
    video_blocks = re.findall(r"<!--\s*AVD:OMNI_PROMPT\s+([^>]*)-->(.*?)<!--\s*/AVD:OMNI_PROMPT\s*-->", text, re.I | re.S)
    ids = set()

    for metadata, body in image_blocks:
        prompt_id = re.search(r"\bid=([^\s]+)", metadata, re.I)
        framework = re.search(r"\bframework=(NBP-F[1-5])", metadata, re.I)
        if not prompt_id or not framework:
            issue(errors, "NANO_MARKER_INVALID", metadata)
            continue
        value = prompt_id.group(1)
        if value in ids:
            issue(errors, "DUPLICATE_PROMPT_ID", value)
        ids.add(value)
        for field in ["Acceptance:", "First one-variable repair:"]:
            if field.lower() not in body.lower():
                issue(errors, "NANO_FIELD_MISSING", value + "." + field)

    for metadata, body in video_blocks:
        prompt_id = re.search(r"\bid=([^\s]+)", metadata, re.I)
        task = re.search(r"\btask=(OM-F[1-5])", metadata, re.I)
        if not prompt_id or not task:
            issue(errors, "OMNI_MARKER_INVALID", metadata)
            continue
        value = prompt_id.group(1)
        if value in ids:
            issue(errors, "DUPLICATE_PROMPT_ID", value)
        ids.add(value)
        for field in ["Action:", "Camera:", "End condition:", "Acceptance:", "First one-variable repair:"]:
            if field.lower() not in body.lower():
                issue(errors, "OMNI_FIELD_MISSING", value + "." + field)
        if task.group(1).upper() in {"OM-F4", "OM-F5"} and "keep everything else the same" not in body.lower():
            issue(errors, "EDIT_LOCK_MISSING", value)
