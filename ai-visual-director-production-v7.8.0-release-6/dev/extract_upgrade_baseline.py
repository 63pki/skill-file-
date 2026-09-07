#!/usr/bin/env python3
"""Extract a V7.6.0 Release 4 upgrade-compatibility baseline from a real archive.

`validators/validate_upgrade_compatibility.py` needs
`release/V7_6_0_RELEASE_4_BASELINE_HASHES.json`, and that file does not ship in this
package. It cannot be generated from a 7.8.0 tree: every path would trivially be
"preserved" and every immutable hash would trivially agree, turning a real gate into a
no-op. That is fabricated provenance, and the skill kernel forbids it.

So this tool refuses to invent the baseline. It only *reads* a real V7.6.0 Release 4
archive that you supply, and derives the baseline from those actual bytes.

Usage:
    python3 dev/extract_upgrade_baseline.py ARCHIVE [--immutable PATH ...] [--out release/V7_6_0_RELEASE_4_BASELINE_HASHES.json]

ARCHIVE may be a .zip or a directory containing an extracted V7.6.0 Release 4 package.

The tool verifies before writing:
  * the archive actually declares itself 7.6.0 (release/RELEASE.json), so a wrong
    archive cannot be laundered into a baseline;
  * no path escapes the archive root (zip-slip).
"""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, sys, tempfile, zipfile

EXPECTED_VERSION_PREFIX = '7.6.0'


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read_version(root: Path):
    rel = root / 'release/RELEASE.json'
    if not rel.is_file():
        candidates = list(root.rglob('release/RELEASE.json'))
        if not candidates:
            return None, None
        rel = candidates[0]
        root = rel.parents[1]
    try:
        data = json.loads(rel.read_text())
    except Exception:
        return None, root
    return str(data.get('version', '')), root


def open_archive(archive: Path):
    """Return (tempdir_or_None, package_root). Caller removes tempdir."""
    if archive.is_dir():
        version, root = read_version(archive)
        return None, root, version
    if archive.suffix.lower() == '.zip':
        tmp = Path(tempfile.mkdtemp(prefix='avd-baseline-'))
        with zipfile.ZipFile(archive) as zf:
            for name in zf.namelist():
                # zip-slip guard: reject absolute paths and traversal before extracting
                if name.startswith('/') or '..' in Path(name).parts or os.path.splitdrive(name)[0]:
                    shutil.rmtree(tmp, ignore_errors=True)
                    raise SystemExit(json.dumps({
                        'status': 'FAIL', 'reason': 'unsafe path in archive', 'path': name}, indent=2))
            zf.extractall(tmp)
        version, root = read_version(tmp)
        return tmp, root, version
    raise SystemExit(json.dumps({
        'status': 'FAIL', 'reason': 'ARCHIVE must be a .zip or a directory', 'given': str(archive)}, indent=2))


def main():
    ap = argparse.ArgumentParser(description='Derive the upgrade baseline from a real V7.6.0 Release 4 archive.')
    ap.add_argument('archive', help='.zip or directory of the V7.6.0 Release 4 package')
    ap.add_argument('--immutable', nargs='*', default=[],
                    help='Paths that must never change across upgrades (verified present in the archive).')
    ap.add_argument('--retired', default=None,
                    help='JSON file mapping baseline path -> {"reason": ..., "successor": ...} for paths '
                         'intentionally removed since the baseline. Every entry needs a non-empty reason.')
    ap.add_argument('--out', default='release/V7_6_0_RELEASE_4_BASELINE_HASHES.json')
    ns = ap.parse_args()

    archive = Path(ns.archive).resolve()
    if not archive.exists():
        raise SystemExit(json.dumps({'status': 'FAIL', 'reason': 'archive not found', 'path': str(archive)}, indent=2))

    retired = {}
    if ns.retired:
        rp = Path(ns.retired).resolve()
        if not rp.is_file():
            raise SystemExit(json.dumps({'status': 'FAIL', 'reason': 'retirement record not found', 'path': str(rp)}, indent=2))
        try:
            retired = json.loads(rp.read_text())
        except Exception as x:
            raise SystemExit(json.dumps({'status': 'FAIL', 'reason': 'retirement record is not valid JSON', 'error': str(x)}, indent=2))
        if not isinstance(retired, dict):
            raise SystemExit(json.dumps({'status': 'FAIL', 'reason': 'retirement record must be a JSON object'}, indent=2))
        unjustified = sorted(k for k, v in retired.items()
                             if not isinstance(v, dict) or not str(v.get('reason', '')).strip())
        if unjustified:
            raise SystemExit(json.dumps({
                'status': 'FAIL',
                'reason': 'Every retirement needs a non-empty reason, otherwise the gate cannot '
                          'distinguish a documented migration from an accidental deletion.',
                'unjustified': unjustified,
            }, indent=2))

    tmp, root, version = open_archive(archive)
    try:
        if not version:
            raise SystemExit(json.dumps({
                'status': 'FAIL',
                'reason': 'No readable release/RELEASE.json in the archive; cannot confirm this is V7.6.0 Release 4.',
            }, indent=2))
        if not version.startswith(EXPECTED_VERSION_PREFIX):
            raise SystemExit(json.dumps({
                'status': 'FAIL',
                'reason': f'Archive declares version {version!r}, expected {EXPECTED_VERSION_PREFIX}.x. '
                          'Refusing to derive a V7.6.0 baseline from a different release.',
            }, indent=2))

        files = {}
        for p in sorted(root.rglob('*')):
            if not p.is_file() or '__pycache__' in p.parts:
                continue
            rel = p.relative_to(root).as_posix()
            if rel == 'PACKAGE_MANIFEST.json':
                continue
            files[rel] = {'bytes': p.stat().st_size, 'sha256': sha(p)}

        missing_immutable = [i for i in ns.immutable if i not in files]
        if missing_immutable:
            raise SystemExit(json.dumps({
                'status': 'FAIL',
                'reason': 'Declared immutable paths absent from the archive.',
                'missing': missing_immutable,
            }, indent=2))

        unknown_retired = sorted(set(retired) - set(files))
        if unknown_retired:
            raise SystemExit(json.dumps({
                'status': 'FAIL',
                'reason': 'Retirement record names paths that never existed in the baseline archive.',
                'unknown': unknown_retired,
            }, indent=2))

        contradiction = sorted(set(ns.immutable) & set(retired))
        if contradiction:
            raise SystemExit(json.dumps({
                'status': 'FAIL',
                'reason': 'A path cannot be both immutable and retired.',
                'paths': contradiction,
            }, indent=2))

        baseline = {
            'schemaVersion': '7.8.0',
            'baselineVersion': version,
            'baselineRelease': 'Release 4',
            'derivedFrom': archive.name,
            'hashAlgorithm': 'SHA-256',
            'fileCount': len(files),
            'requiredPathCount': len(files),
            'immutablePaths': sorted(ns.immutable),
            'retiredPaths': {k: retired[k] for k in sorted(retired)},
            'files': files,
            'provenance': 'Derived from the actual bytes of the supplied V7.6.0 Release 4 archive. '
                          'Not reconstructed from a later release.',
        }
        out = Path(ns.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(baseline, indent=2) + '\n')
        print(json.dumps({
            'status': 'PASS',
            'baselineVersion': version,
            'fileCount': len(files),
            'immutablePaths': len(ns.immutable),
            'retiredPaths': len(retired),
            'written': str(out),
            'nextStep': 'Rebuild in binding order (see dev/UPDATE_WORKFLOW.md): suite -> audit -> '
                        'build_package_manifest.py -> clean pycache. Then '
                        'validate_candidate_readiness.py should clear CANDIDATE_BASELINE_MISSING.',
        }, indent=2))
        return 0
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    raise SystemExit(main())
