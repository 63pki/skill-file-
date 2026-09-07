#!/usr/bin/env python3
"""V7.8.0 canonical release-consistency gate.

Exposes ``validate(root)`` so other validators (notably
``validate_candidate_readiness.py``) can compose it without executing module-level
side effects. Running this file directly prints the same JSON report it always has.
"""
from pathlib import Path
import argparse, json, re, sys, hashlib

EXPECTED_VERSION = '7.8.0'
EXPECTED_REGRESSION_LAST_ID = 650


def validate(root):
    """Return a list of structured error dicts. Empty list means consistent."""
    ROOT = Path(root).resolve()
    e = []

    def add(c, m, p=''):
        e.append({'code': c, 'message': m, 'path': p})

    try:
        r = json.loads((ROOT / 'release/RELEASE.json').read_text())
    except Exception as x:
        r = {}
        add('RELEASE_PARSE', str(x), 'release/RELEASE.json')
    if r.get('version') != EXPECTED_VERSION:
        add('VERSION_DRIFT', str(r.get('version')))
    stack = r.get('generationStack', {})
    if stack.get('stillOwner') != 'NANO_BANANA_PRO':
        add('STILL_OWNER_DRIFT', str(stack))
    if stack.get('videoOwner') != 'GEMINI_OMNI_FLASH':
        add('VIDEO_OWNER_DRIFT', str(stack))
    if stack.get('mediaExecution') != 'NOT_SUPPORTED':
        add('PROMPT_ONLY_DRIFT', str(stack))

    try:
        m = json.loads((ROOT / 'bootstrap/runtime_load_manifest.json').read_text())
    except Exception as x:
        m = {}
        add('RUNTIME_MANIFEST_PARSE', str(x))
    if m.get('packageVersion') != EXPECTED_VERSION:
        add('RUNTIME_VERSION_DRIFT', str(m.get('packageVersion')))
    for rel, rec in m.get('files', {}).items():
        p = ROOT / rel
        if not p.is_file():
            add('RUNTIME_FILE_MISSING', rel, rel)
        elif hashlib.sha256(p.read_bytes()).hexdigest() != rec.get('sha256'):
            add('RUNTIME_HASH_MISMATCH', rel, rel)

    catalog = ROOT / 'dev/REGRESSION_TESTS.md'
    if not catalog.is_file():
        add('REGRESSION_CATALOG_MISSING', str(catalog), 'dev/REGRESSION_TESTS.md')
    else:
        ids = [int(x) for x in re.findall(r'^\| R(\d+) \|', catalog.read_text(), re.M)]
        expected = list(range(1, EXPECTED_REGRESSION_LAST_ID + 1))
        if len(ids) != EXPECTED_REGRESSION_LAST_ID or sorted(ids) != expected:
            add('REGRESSION_CATALOG_DRIFT', str({
                'count': len(ids),
                'first': min(ids or [0]),
                'last': max(ids or [0]),
                'expected': EXPECTED_REGRESSION_LAST_ID,
            }))
    return e


def regression_last_id(root):
    """Highest R-id actually present in the regression catalog (0 if absent)."""
    catalog = Path(root).resolve() / 'dev/REGRESSION_TESTS.md'
    if not catalog.is_file():
        return 0
    ids = [int(x) for x in re.findall(r'^\| R(\d+) \|', catalog.read_text(), re.M)]
    return max(ids or [0])


def main():
    ap = argparse.ArgumentParser(description='V7.8.0 canonical release-consistency gate.')
    ap.add_argument('root', nargs='?', default=str(Path(__file__).resolve().parents[1]),
                    help='Package root to validate (default: the installed package).')
    ns = ap.parse_args()
    errors = validate(ns.root)
    print(json.dumps({'validator': 'V7.8.0-RELEASE-CONSISTENCY', 'pass': not errors, 'errors': errors}, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == '__main__':
    main()
