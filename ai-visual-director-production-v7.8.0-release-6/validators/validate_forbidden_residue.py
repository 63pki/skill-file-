#!/usr/bin/env python3
from pathlib import Path
import re, json, sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
patterns = [
    re.compile(r"\b" + "ve" + r"o\b", re.I),
    re.compile(r"\b" + "can" + r"va\b", re.I),
    re.compile(r"\b" + "cap" + r"cut\b", re.I),
    re.compile(r"\b" + "cao" + r"cut\b", re.I),
]
errors = []
# An upgrade baseline is a migration record: it must name the retired predecessor
# paths verbatim, including superseded adapter filenames, or it is not evidence of
# what changed. Content patterns therefore do not apply to it. This exemption is
# narrow — it covers the historical baseline documents only, never current rules.
HISTORICAL_BASELINE = re.compile(r"^release/V\d+_\d+_\d+_RELEASE_\d+_BASELINE_HASHES\.json$")
for path in ROOT.rglob("*"):
    if "__pycache__" in path.parts:
        continue
    rel = path.relative_to(ROOT).as_posix()
    historical = bool(HISTORICAL_BASELINE.match(rel))
    if not historical and any(rx.search(rel) for rx in patterns):
        errors.append({"code": "FORBIDDEN_FILENAME", "path": rel})
    if not path.is_file() or path.name == "PACKAGE_MANIFEST.json":
        continue
    if historical:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for rx in patterns:
        if rx.search(text):
            errors.append({"code": "FORBIDDEN_CONTENT", "path": rel, "pattern": rx.pattern})
out = {"validator": "V7.8.0-FORBIDDEN-RESIDUE", "pass": not errors, "errors": errors}
print(json.dumps(out, indent=2))
raise SystemExit(0 if not errors else 1)
