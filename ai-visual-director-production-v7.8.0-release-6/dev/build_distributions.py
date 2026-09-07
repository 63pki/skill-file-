#!/usr/bin/env python3
"""Build the separated distributions described in DISTRIBUTIONS.md.

Two installable outputs, plus the canonical cumulative release:

  portable-core    Markdown-and-JSON only. No Python required. This is what a
                   content creator installs into an agent. Runs under the
                   PORTABLE_REFERENCE profile and is capped at PLAN-PASS, because
                   none of the deterministic gates can execute.

  validation-sdk   Python validators, bootstrap, fixtures, schemas, release policy,
                   and dev protocols. Optional add-on for a host that can execute
                   code. Unlocks VERIFIED_RUNTIME.

  cumulative       Every file. Canonical for auditing and installation.

The split is declarative: a file belongs to a distribution because it matches a
prefix rule below, not because someone remembered to copy it. The builder fails
closed on any file that matches no rule, so a new file cannot silently ship only
in the cumulative archive.

Usage:
    python3 dev/build_distributions.py [--outdir dist] [--zip]
"""
from pathlib import Path
import argparse, hashlib, json, shutil, sys

ROOT = Path(__file__).resolve().parents[1]

# Prefix rules, evaluated in order; first match wins.
PORTABLE_CORE = [
    'SKILL.md', 'QUICKSTART.md', 'ARCHITECTURE.md', 'DISTRIBUTIONS.md',
    'rules/', 'adapters/', 'references/', 'exports/', 'profiles/',
    'templates/', 'schemas/', 'routing/',
]
VALIDATION_SDK = [
    'validators/', 'bootstrap/', 'tests/', 'schemas/', 'release/', 'dev/',
    'templates/',
]
# Never shipped in a split distribution: the cumulative archive is their only home.
CUMULATIVE_ONLY = [
    'PACKAGE_MANIFEST.json',
]

SELF_EXCLUDE = {'__pycache__', '.DS_Store', 'Thumbs.db'}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def classify(rel: str):
    """Return the set of distributions a relative path belongs to."""
    out = set()
    for rule in PORTABLE_CORE:
        if rel == rule or rel.startswith(rule):
            out.add('portable-core')
            break
    for rule in VALIDATION_SDK:
        if rel == rule or rel.startswith(rule):
            out.add('validation-sdk')
            break
    return out


def collect():
    files = []
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file():
            continue
        if any(part in SELF_EXCLUDE for part in p.parts):
            continue
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith('dist/'):
            continue
        files.append(rel)
    return files


def build(outdir: Path, make_zip: bool):
    files = collect()
    unclaimed = [
        f for f in files
        if not classify(f) and not any(f == r or f.startswith(r) for r in CUMULATIVE_ONLY)
    ]
    if unclaimed:
        print(json.dumps({
            'status': 'FAIL',
            'reason': 'Files matched no distribution rule and are not cumulative-only. '
                      'Add a prefix rule rather than letting them ship only in the '
                      'cumulative archive.',
            'unclaimed': unclaimed,
        }, indent=2))
        return 1, {'status': 'FAIL', 'unclaimed': unclaimed}

    version = json.loads((ROOT / 'release/RELEASE.json').read_text())['version']
    report = {'status': 'PASS', 'sourceFiles': len(files), 'distributions': {}}
    specs = (
        ('portable-core', lambda f: 'portable-core' in classify(f), {
            'requiresPython': False,
            'standalone': True,
            'assuranceCeiling': 'PLAN-PASS (PORTABLE_REFERENCE) — no deterministic gate can execute',
        }),
        ('validation-sdk', lambda f: 'validation-sdk' in classify(f), {
            'requiresPython': True,
            'standalone': False,
            'requires': f'portable-core@{version}',
            'assuranceCeiling': 'Unlocks VERIFIED_RUNTIME, but only when installed alongside '
                                'portable-core: the validators hash the runtime files that live '
                                'there. Install the combined tree, or place both side by side.',
        }),
        ('combined', lambda f: 'portable-core' in classify(f) or 'validation-sdk' in classify(f), {
            'requiresPython': True,
            'standalone': True,
            'assuranceCeiling': 'VERIFIED_RUNTIME capable: runtime rules and validators in one tree',
        }),
        ('cumulative', lambda f: True, {
            'requiresPython': True,
            'standalone': True,
            'assuranceCeiling': 'Canonical audit archive; not an install target',
        }),
    )
    for name, selector, meta in specs:
        chosen = [f for f in files if selector(f)]
        target = outdir / name
        if target.exists():
            shutil.rmtree(target)
        rows = []
        for rel in chosen:
            src = ROOT / rel
            dst = target / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            rows.append({'path': rel, 'bytes': src.stat().st_size, 'sha256': sha(src)})
        manifest = {
            'distribution': name,
            'schemaVersion': version,
            'hashAlgorithm': 'SHA-256',
            'fileCount': len(rows),
            'files': rows,
            **meta,
        }
        (target / 'DISTRIBUTION_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')

        entry = {'files': len(rows), 'bytes': sum(r['bytes'] for r in rows)}
        if make_zip:
            archive = shutil.make_archive(str(outdir / name), 'zip', root_dir=str(outdir), base_dir=name)
            entry['zip'] = Path(archive).name
            entry['zipBytes'] = Path(archive).stat().st_size
            entry['zipSha256'] = sha(Path(archive))
        report['distributions'][name] = entry

    def paths_of(name):
        man = json.loads((outdir / name / 'DISTRIBUTION_MANIFEST.json').read_text())
        return {r['path'] for r in man['files']}

    # Every split distribution must be a subset of cumulative.
    cum = paths_of('cumulative')
    for name in ('portable-core', 'validation-sdk', 'combined'):
        extra = paths_of(name) - cum
        if extra:
            report['status'] = 'FAIL'
            report['distributions'][name]['notInCumulative'] = sorted(extra)

    # combined must contain everything a VERIFIED_RUNTIME host needs: the runtime
    # files that validators hash, plus the validators themselves.
    runtime_manifest = json.loads((ROOT / 'bootstrap/runtime_load_manifest.json').read_text())
    combined = paths_of('combined')
    missing_runtime = sorted(set(runtime_manifest.get('files', {})) - combined)
    if missing_runtime:
        report['status'] = 'FAIL'
        report['combinedMissingRuntimeFiles'] = missing_runtime
    for needed in ('validators/validate_release_consistency.py', 'dev/run_v780_release6_tests.py'):
        if needed not in combined:
            report['status'] = 'FAIL'
            report.setdefault('combinedMissingValidators', []).append(needed)

    # The two halves together must cover every source file, except the ones that are
    # deliberately cumulative-only (the self-excluding package manifest).
    pc = paths_of('portable-core')
    vs = paths_of('validation-sdk')
    cumulative_only = {
        f for f in files
        if any(f == r or f.startswith(r) for r in CUMULATIVE_ONLY)
    }
    uncovered = sorted(set(files) - (pc | vs) - cumulative_only)
    if uncovered:
        report['status'] = 'FAIL'
        report['uncoveredBySplits'] = uncovered
    report['cumulativeOnly'] = sorted(cumulative_only)
    report['overlap'] = len(pc & vs)
    report['proofBoundary'] = (
        'Splitting delivery does not weaken the cumulative release, which remains canonical. '
        'portable-core cannot execute validators, so its assurance ceiling is PLAN-PASS. '
        'validation-sdk is an add-on, not a standalone product: install combined for VERIFIED_RUNTIME.'
    )
    return (0 if report['status'] == 'PASS' else 1), report


def main():
    ap = argparse.ArgumentParser(description='Build the separated distributions.')
    ap.add_argument('--outdir', default=str(ROOT.parent / 'dist'),
                    help='Output directory. Defaults to a sibling of the package so the '
                         'generated trees never land inside the canonical archive.')
    ap.add_argument('--zip', action='store_true', help='Also produce a zip per distribution.')
    ns = ap.parse_args()
    outdir = Path(ns.outdir).resolve()
    if ROOT in outdir.parents:
        print(json.dumps({
            'status': 'FAIL',
            'reason': f'--outdir {outdir} is inside the package root. build_package_manifest.py '
                      'would sweep the generated trees into the canonical archive. Use a sibling path.',
        }, indent=2))
        raise SystemExit(1)
    outdir.mkdir(parents=True, exist_ok=True)
    code, report = build(outdir, ns.zip)
    print(json.dumps(report, indent=2))
    raise SystemExit(code)


if __name__ == '__main__':
    main()
