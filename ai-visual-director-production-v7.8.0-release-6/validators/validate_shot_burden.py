#!/usr/bin/env python3
"""Mechanical short-clip burden checks."""

BURDEN_FIELDS = [
    "subjectActions",
    "cameraChanges",
    "sceneChanges",
    "transformations",
    "textEvents",
    "dialogueTurns",
    "contacts",
    "occlusions",
    "endStateChanges",
]
MAJOR_FIELDS = {"subjectActions", "cameraChanges", "sceneChanges", "transformations", "endStateChanges"}


def count(value):
    if isinstance(value, list):
        return len([item for item in value if str(item).strip()])
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return max(0, int(value))
    return 1 if str(value or "").strip() else 0


def validate(shots):
    errors = []
    for shot in shots or []:
        if not isinstance(shot, dict):
            continue
        burden = shot.get("burden", {}) if isinstance(shot.get("burden"), dict) else {}
        if not burden:
            continue
        counts = {field: count(burden.get(field)) for field in BURDEN_FIELDS}
        active_classes = sum(1 for value in counts.values() if value)
        major_beats = sum(counts[field] for field in MAJOR_FIELDS)
        approved = bool(burden.get("explicitFeasibilityApproval"))
        if (major_beats > 1 or active_classes > 3) and not approved:
            errors.append({
                "code": "SHOT_BURDEN_OVERLOAD",
                "message": f"{shot.get('id', '?')}: majorBeats={major_beats}, activeClasses={active_classes}",
                "shotId": shot.get("id", "?"),
                "counts": counts,
            })
    return errors
