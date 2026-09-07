#!/usr/bin/env python3
"""Reject conflicting package-wide validator and media statuses."""
from pathlib import Path
import json
import re
import sys


def normalize(value):
    text = str(value).strip().upper().replace("-", "_").replace(" ", "_")
    if text in {"TRUE", "PASS", "PASSED"}:
        return "PASS"
    if text in {"FALSE", "FAIL", "FAILED", "REVISE", "BLOCKED"}:
        return "REVISE"
    return text


def scan(root):
    root = Path(root)
    found = {"validator": [], "media": [], "maturity": []}
    for path in root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        rel = path.relative_to(root).as_posix()
        if path.name.upper() == "STATUS.TXT":
            text = path.read_text(encoding="utf-8", errors="replace")
            for key, pattern in {
                "validator": r"(?im)\bvalidator\s*[:·-]?\s*(PASS|PENDING|REVISE|BLOCKED|FAILED)",
                "media": r"(?im)\bmedia\s*[:·-]?\s*([A-Z][A-Z_ -]+)",
                "maturity": r"(?im)\b(?:maturity|ceiling)\s*[:·-]?\s*([A-Z][A-Z_ -]+)",
            }.items():
                for match in re.findall(pattern, text):
                    found[key].append({"path": rel, "value": normalize(match)})
        elif path.suffix.lower() == ".json" and path.name in {"DELIVERY_STATUS.json", "VALIDATION_RESULT.json"}:
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if path.name == "VALIDATION_RESULT.json" and "pass" in data:
                found["validator"].append({"path": rel, "value": normalize(data["pass"])})
            if "deterministicValidation" in data:
                found["validator"].append({"path": rel, "value": normalize(data["deterministicValidation"])})
            if "media" in data:
                found["media"].append({"path": rel, "value": normalize(data["media"])})
            if "maturity" in data:
                found["maturity"].append({"path": rel, "value": normalize(data["maturity"])})
    errors = []
    for key, rows in found.items():
        values = sorted({row["value"] for row in rows if row["value"]})
        if len(values) > 1:
            errors.append({"code": "PACKAGE_STATUS_CONFLICT", "field": key, "values": values, "records": rows})
    pass_claimed = any(row["value"] == "PASS" for row in found["validator"])
    if pass_claimed and not any(path.name == "VALIDATION_RESULT.json" for path in root.rglob("VALIDATION_RESULT.json")):
        errors.append({"code": "VALIDATOR_EVIDENCE_MISSING", "message": "Validator PASS requires packaged VALIDATION_RESULT.json."})
    return errors


def main():
    root = Path(sys.argv[1]).resolve()
    errors = scan(root)
    out = {"validator": "V7.8.0-STATUS-SINGULARITY", "pass": not errors, "errors": errors}
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
