#!/usr/bin/env python3
"""Validate path preservation and immutable-guide compatibility against V7.6.0.

A baseline path that is absent from the current tree is not automatically a defect.
Between Release 4 and Release 6 the generation stack was deliberately replaced
(NANO_BANANA/VEO_3_1 -> NANO_BANANA_PRO/GEMINI_OMNI_FLASH) and the per-version test
runners were consolidated. Those are documented migrations, not losses.

So the baseline may carry a ``retiredPaths`` record: path -> {reason, successor}.
A missing path is tolerated only when it is declared retired with a non-empty reason.
Anything else still fails as CANDIDATE_BASELINE_PATH_MISSING, so accidental deletion
remains a blocker.

A path may not be both immutable and retired; that contradiction fails closed.
"""
from pathlib import Path
import argparse, hashlib, json, re


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


BASELINE_RX = re.compile(r'^V(\d+)_(\d+)_(\d+)_RELEASE_(\d+)_BASELINE_HASHES\.json$')


def locate_baseline(root):
    """Find the predecessor baseline: explicit pointer first, then highest version.

    Prefers release/RELEASE.json ``baselineManifest`` so the active baseline is
    declared rather than inferred. Falls back to the highest versioned baseline
    file so the gate keeps working if the pointer is absent.
    """
    rel = root / 'release/RELEASE.json'
    try:
        declared = json.loads(rel.read_text()).get('baselineManifest')
    except Exception:
        declared = None
    if declared:
        p = root / declared
        if p.is_file():
            return p
    cands = []
    for f in (root / 'release').glob('*_BASELINE_HASHES.json'):
        m = BASELINE_RX.match(f.name)
        if m:
            cands.append((tuple(int(g) for g in m.groups()), f))
    if cands:
        return max(cands)[1]
    return root / 'release'


def validate(root):
    root = Path(root).resolve()
    e = []
    advisories = []
    bp = locate_baseline(root)
    if not bp.is_file():
        return [{'code': 'CANDIDATE_BASELINE_MISSING', 'message': str(bp)}]
    try:
        b = json.loads(bp.read_text())
    except Exception as x:
        return [{'code': 'CANDIDATE_BASELINE_PARSE', 'message': str(x)}]

    files = b.get('files', {})
    retired = b.get('retiredPaths', {})
    if not isinstance(retired, dict):
        e.append({'code': 'CANDIDATE_RETIRED_TYPE', 'message': type(retired).__name__})
        retired = {}

    # A retirement must state why. An empty reason is an undocumented deletion.
    for rel, rec in sorted(retired.items()):
        if not isinstance(rec, dict) or not str(rec.get('reason', '')).strip():
            e.append({'code': 'CANDIDATE_RETIREMENT_UNJUSTIFIED', 'message': rel})
        if rel not in files:
            e.append({'code': 'CANDIDATE_RETIREMENT_UNKNOWN_PATH', 'message': rel})

    # Nothing may be declared both immutable and retired.
    for rel in b.get('immutablePaths', []):
        if rel in retired:
            e.append({'code': 'CANDIDATE_IMMUTABLE_AND_RETIRED', 'message': rel})

    current = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    expected = set(files)

    for rel in sorted(expected - current):
        if rel in retired:
            advisories.append({
                'code': 'CANDIDATE_PATH_RETIRED',
                'message': rel,
                'reason': retired[rel].get('reason', ''),
                'successor': retired[rel].get('successor'),
            })
        else:
            e.append({'code': 'CANDIDATE_BASELINE_PATH_MISSING', 'message': rel})

    for rel in b.get('immutablePaths', []):
        p = root / rel
        want = (files.get(rel) or {}).get('sha256')
        if not p.is_file() or sha(p) != want:
            e.append({'code': 'CANDIDATE_IMMUTABLE_DRIFT', 'message': rel})

    validate.advisories = advisories
    return e


def main():
    a = argparse.ArgumentParser(description='V7.6.0 upgrade-compatibility gate.')
    a.add_argument('root', nargs='?', default=str(Path(__file__).resolve().parents[1]))
    ns = a.parse_args()
    validate.advisories = []
    errors = validate(ns.root)
    out = {
        'validator': 'V7.8.0-UPGRADE-COMPATIBILITY',
        'pass': not errors,
        'errors': errors,
        'retiredPathsAccepted': validate.advisories,
        'proofBoundary': 'Path preservation and declared immutable hashes only; declared '
                         'retirements are accepted on their stated reason and are not '
                         'semantic equivalence for every historical behavior.',
    }
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == '__main__':
    main()
