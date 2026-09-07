# Update Workflow (Maintenance Only)

1. Name the affected canonical owner from `00a_router.md`.
2. Verify volatile facts using `03`; record evidence using `27`.
3. Edit the owner first; secondary files should link, not duplicate.
4. Check every local `.md` reference and section name.
5. Search for contradictory `always`, `never`, `mandatory`, stale model IDs, prices, caps, and numeric thresholds.
6. Confirm safety remains above user preference.
7. Confirm mode-specific vocabulary cannot leak into another mode.
8. Confirm examples claim no generated result, metric, or approval without evidence.
9. Run Markdown lint and the package validator.
10. Record a concise change note here only; do not add a runtime changelog.

## Release build order (binding)

`PACKAGE_MANIFEST.json` hashes every other file, so it must be built **last**. Running the
suite after the manifest silently re-dirties it, because the suite rewrites
`dev/V7_8_0_RELEASE_6_RESULTS.json` (and `bootstrap/build_runtime_manifest.py` rewrites
`bootstrap/runtime_load_manifest.json`). This ordering slip is what produced the three
hash-drifted manuals in the original Release 6 archive.

```text
1. Edit sources.
2. python3 dev/run_v780_release6_tests.py            # writes its results file
3. refresh dev/COMPLETE_PACKAGE_AUDIT.json           # counts every file
4. python3 validators/build_package_manifest.py .    # LAST write — hashes everything above
5. find . -name "__pycache__" -type d -prune -exec rm -rf {} +
6. python3 validators/validate_release_consistency.py .
7. Zip. Do not edit, run, or regenerate anything after step 4 except the step-5 cleanup.
```

Step 5 is safe after step 4 because `build_package_manifest.py` never lists `__pycache__`
paths, so removing them cannot invalidate a hash. It is nevertheless mandatory: merely
*running* any validator writes `__pycache__` beside it, and
`validators/validate_clean_zip.py` rejects caches with `ZIP_TEMP_FILE`. A package that
passes every validator can still fail the clean-archive gate for this reason alone.

Verification after step 4 must not itself re-run validators inside the tree, or it will
recreate the caches it is checking for. Set `PYTHONDONTWRITEBYTECODE=1` and parse in
memory instead of `py_compile`:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -c "import pathlib;[compile(p.read_text(),str(p),'exec') for p in pathlib.Path('.').rglob('*.py')];print('parse OK')"
PYTHONDONTWRITEBYTECODE=1 python3 -c "import json,hashlib,pathlib;m=json.load(open('PACKAGE_MANIFEST.json'));print([r['path'] for r in m['files'] if hashlib.sha256(pathlib.Path(r['path']).read_bytes()).hexdigest()!=r['sha256']] or 'CLEAN')"
```

Without the flag, a verification pass that shells out to any validator writes
`__pycache__` and then reports the package dirty — a self-inflicted failure that looks
like a real one.

## V6.0.0

Canonical safety-first refactor; removed stale spec tables and business-coaching scope; unified QA, naming, camera grammar, token behavior, routing, and cost ownership; added directing/editing grammar, storyboard/animatic, output diagnostics, SFX/Foley, Mode C execution, Mode D compositing, reference intake, prompt diffs, session handoff, localization retiming, and evidence registry.

## V6.1.0 Hybrid

Merged the V6 canonical core with curated V5.6 creative depth as nine optional libraries. Preserved V6 safety, capability, routing, QA, naming, sound, storyboard, Mode C, and Mode D owners; excluded stale specifications, monetization ladders, duplicated rubrics, forced NEXT flow, and unsupported PROVEN claims.

## V6.5.0 Reliability hardening

Added execution-honesty and no-self-modification boundaries; story causality; animation asset schemas and true model sheets; scene/shot/generation-clip separation; shot feasibility; dialogue timing; technical-value honesty; style contradiction linting; reliability no-ship conditions; Milo benchmark replay; and regression tests R21–R28.

## V6.4.0 Testing and operator-readiness layer

Added visual taste/reference calibration, beginner operator mode, platform-neutral editing surface/platform-neutral design surface execution recipes, a ten-brief benchmark suite, and twenty regression tests. Routed each as a unique owner and kept benchmark/regression material under `dev/` so it cannot affect runtime creative answers.

## V6.3.0 Commercial-excellence autopilot

Added an automatic eight-gate system for film/commercial/premium work: quality target, concept divergence and replacement, anti-generic language conversion, film-language board, commercial control, mode-specific craft, sound identity, and evidence-based no-ship review. Integrated it into the constitution, router, preflight, prompt lint, adaptive phases, QA, completion standard, and project-state handoff.

## V6.2.0 Production merge

Merged the V6.1 production discipline with the curated Hybrid V6.1 libraries. Added adaptive NEXT phases and prompt batching, concept divergence, and factual-visual reconstruction ownership. Core owners remain unique; optional libraries cannot override safety, capability, mode, QA, delivery, or state rules.

## V6.6.0 Broad reliability enforcement

Added a cross-format gate controller, evidence receipts, dependency freezes, no-reference taste plans, four-channel shot packs, motivated-effect gate, child-directed CTA guard, ownership/platform-name guard, mandatory adaptive-phase triggers, broad regression cases R29–R41, and cross-format benchmark B12.

## V6.7.0 Runtime activation and regression hardening

Added mandatory delivery maps, evidence-to-owner trigger compilation, final artifact lint, stale-draft removal, durable-resolution proof, mechanical speech timing, canonical-view-first model-sheet fallback, mode-pure boards, value classification, strict filename parsing, audience suitability, 2D cutout execution depth, compact beginner mode, activation tests A1–A12, regressions R42–R53, and benchmark B13.

## V6.8.0 Cross-model quality floor and mandatory NEXT

Added default CONTROLLED profile, objective capability probes, fail-closed INSUFFICIENT mode, independent critic labels, deterministic checks, release maturity, model-switch handoff, mandatory planning-only first response, dynamic STEP QUEUE, exactly-one-step NEXT semantics, batch safety, active-step contracts, NEXT compiler lint, cross-model tests X1–X10, regressions R54–R65, and benchmark B14.

## V6.10.0 Runtime consolidation and host adapters

Replaced the many-controller runtime with a compact SKILL kernel and one `rules/RUNTIME.md` read containing five authoritative bundles. Preserved all V6.8 deep references under `rules/detailed/`; added compatibility notice, Project Asset Registry, Evidence Binder, Hermes AGENTS enforcement, Hermes vision setup, five-layer architecture, policy-tension resolutions, and consolidation tests. No Hermes commands entered the portable core and no duplicate runtime authority was retained.

## V6.10.0 Performance release

- Replaced micro-step conversation flow with six approval gates.
- Added FAST/STANDARD/CONTROLLED operating depths.
- Internalized successful routine receipts/state.
- Added compact prompt compiler layers.
- Added attempt budgets and stop-loss rules.
- Added representative motion-proof-first workflow.
- Added mandatory final compilation and templates.
- Updated Hermes adapter and behavioral tests.

## V6.11.0 Quality release

- Added evidence-backed Visual Exploration Matrix.
- Added Signature Test to reject coherent but interchangeable direction.
- Added silhouette comparison before principal canonical-view lock.
- Added sequence-level color scripting.
- Added composition/hierarchy and thumbnail/value/silhouette checks.
- Added quality-weighted critic with independent critical floors.
- Integrated quality artifacts into Hermes, gates, compiler, final compilation, and regression tests.

## V7.0.0 Production release

- Promoted the system from planning/quality control to host-conditional production control.
- Added full 2D rig, pivot, layer, pose, spacing, exposure, mouth, cleanup, and continuity module.
- Added exact-version visual inspection and mandatory reinspection after repairs.
- Added deterministic/perceptual audio inspection separation.
- Added date/surface-evidenced platform-neutral design surface Web/Mobile and platform-neutral editing surface Desktop/Mobile adapters.
- Added real human review checkpoint with child safeguarding and evidence rules.
- Added automatic host-capable production package exports, hashes, and archive validation.
- Added production, regression, cross-model, conflict, and bug audits while preserving V6.10/V6.11 architecture.

## V7.0.1 generation-stack hotfix

- Restored and promoted Nano Banana Pro image-prompt and Gemini Omni Flash video-prompt rules into active generation adapters.
- Added target-specific prompt templates, capability verification, native-audio decisions, failure routing, and inspected Nano-to-Gemini Omni Flash handoff.
- Made platform-neutral design surface/platform-neutral editing surface explicitly optional post-production surfaces rather than generation dependencies.

## V7.1.0 cross-model reliability and execution release

- Added production-intent and tool-role contracts.
- Kept six internal gates while adding default RUN-TO-BLOCKER and explicit GUIDED/FORENSIC modes.
- Replaced bare PASS with evidence-typed gate maturity.
- Added cross-gate lock diffs, measured-voice motion dependency, complete target-prompt compilers, technical-value classification, 2D generation/manual lane separation, evidence-media inventory, and two-pass archive validation.
- Added executable static conformance, R95–R110, and a mandatory live cross-model replay protocol.
- Preserved V6.10 performance, V6.11 quality, V7.0 production, V7.0.1 Nano Banana Pro/Omni Flash adapters, and all detailed source manuals.

## V7.2.0 deterministic execution and behavioral validation

- Added Project Contract Compiler, explicit delivery modes, Artifact Queue, tool-role assignment, story-world/durable-resolution locks, and actual-output validation.
- Added arithmetic, lock-drift, tool-substitution, evidence-ceiling, and package checks.
- Added three V7.1 cross-model failure fixtures and R111–R126.
- Added compact beginner profile without visible receipt ceremony.
- Preserved five runtime bundles, Nano Banana Pro/Gemini Omni Flash adapters, V6.10/V6.11/V7/V7.1 systems, and all detailed manuals.

## V7.2.1 official prompt-guide alignment

- Rebuilt Nano Banana Pro adapter around the five official frameworks and current family router.
- Rebuilt Gemini Omni Flash adapter around the official five-part formula, generation modes, audio syntax, exclusions, ingredients, first/last frames, and timestamp prompting.
- Added source/date mapping, claim boundary, R127–R139, and executable alignment checks.
- Preserved deterministic V7.2 execution and all earlier production systems.

## V7.3.0 actual-output enforcement and evidence release

- Added compact Core Controller and reduced active SKILL+controller+runtime to under 2,700 words while preserving exactly five bundles, 52 detailed manuals, and archived V7.2.1 authorities.
- Added raw Markdown/package extraction, body hashing, automatically generated Output Records, actual-line timing, expanded locks, evidence file/hash verification, compact status receipt, host probe, and guide staleness trigger.
- Separated deterministic validation from model/human semantic review.
- Added positive, boundary, malformed, mutation, non-narrative, Mode A/B/C/D, faceless, localization, and preserved V7.2 failure tests; regressions R140–R180.
- Added current live replay, Nano Banana Pro/Omni Flash A/B, and complete production pilot protocols without claiming they were executed.
- Resolved receipt/beginner, semantic/deterministic, solo/human-review, compression/preservation, guide/mode, and manifest self-reference conflicts.

## V7.3.1 cryptographic bootstrap hotfix

- Added fail-closed runtime selection, file hashes, ordered context hashing, unpredictable challenge-response, load receipt, detached receipt checksum, and validator enforcement.
- Added trigger mapping for Mode B, Nano Banana Pro, Gemini Omni Flash, Nano-to-Gemini Omni Flash, and declared post surfaces.
- Preserved V7.3.0 authorities and all earlier systems.
- Defined the proof boundary: integrity and context availability are verified; private cognitive attention is not claimed.
