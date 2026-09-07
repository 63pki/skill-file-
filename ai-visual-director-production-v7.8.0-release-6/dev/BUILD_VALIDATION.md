# V7.8.0 Production Candidate Build Validation

- Base release: V7.6.0 Release 4 preserved; earlier compatibility retained
- Scope: structural production-candidate qualification and promotion boundary
- Canonical release metadata: `release/RELEASE.json`
- Upgrade-compatibility baseline hashes: `release/V7_6_0_RELEASE_4_BASELINE_HASHES.json` — **SHIPPED in this archive**, derived from the real V7.6.0 Release 4 archive (293 files, sha256 `5cbf77a8…c6140`). It carries a `retiredPaths` record justifying all 81 intentionally removed paths; an undeclared removal still fails as `CANDIDATE_BASELINE_PATH_MISSING`. `validators/validate_upgrade_compatibility.py` therefore passes, and `validate_candidate_readiness.py` reports `STRUCTURAL_CANDIDATE_PASS`. Discovery is via `release/RELEASE.json` → `baselineManifest`, with a highest-version fallback.
- Contract schemas: project and routing
- **Policy reconciliation (`requiredRegressionLastId` / `requiredFreshExtractionSuites`).** The originally shipped `validators/validate_candidate_readiness.py` line 21 asserted, in a single compound condition:

  ```python
  if policy.get('release')!='7.8.0' \
     or policy.get('requiredRegressionLastId')!=610 \
     or policy.get('requiredFreshExtractionSuites')!=22:
      add(e,'CANDIDATE_POLICY_DRIFT',str(policy))
  ```

  That assertion **could never pass**, for two independent reasons:

  1. `release/PRODUCTION_CANDIDATE_POLICY.json` declares `requiredRegressionLastId: 650`, not `610`. The `610` was a V7.6.0-lineage figure (lastId 610, ~21 bundled runners); `650` was always the correct 7.8.0 value and was never in dispute.
  2. `requiredFreshExtractionSuites` **does not exist** in the policy at all. `.get()` returned `None`, so `None != 22` was unconditionally true. Release 6 consolidated the per-version runners into one bundled suite, so the count the key was meant to pin no longer has a referent.

  Because the file was dead code — wired into no runner and imported by nothing — the guaranteed failure was invisible and shipped undetected.

  **How it was reconciled:** the policy file was *not* edited. The stale expectation was deleted and replaced with policy↔package cross-checks that read the actual shipped state (`validate_release_consistency.regression_last_id(root)` and a live count of `rules/detailed/**/*.md`). The validator now asserts the policy agrees with the package, and separately that the package matches the release-declared constants (`650`, `52`). `requiredFreshExtractionSuites` is referenced nowhere in the tree; the consolidated-runner fact is instead asserted by the `regression-fixture-coverage` suite check.

  Reproducing the original defect: check out the pristine `ai-visual-director-production-v7.8.0-release-6.zip` from `main` and run its `validators/validate_candidate_readiness.py` — it emits `CANDIDATE_POLICY_DRIFT` and exits 1 on an unmodified tree.
- Legacy `repair` input: normalized to canonical `repairAction`
- Character-lock type errors: fail with structured diagnostics; no Python crash
- Portable Reference scripts required: false
- Portable Reference deterministic verification: NOT_AVAILABLE
- Portable Reference instruction compliance: NOT_VERIFIED
- Unsupported hosts: fail closed as UNSUPPORTED_EXECUTION
- Mandatory portable context: core + profile + triggered owners/adapters only
- Active base modes: A photoreal/commercial, B animation, C motion graphics, D hybrid compositing
- Supplemental owners: factual, localization, architecture, UGC, cinematic scene
- Specialist audiences: children, expert, vulnerable, accessibility, multilingual, regulated
- Unknown mode/production/audience triggers: fail closed
- Live tracks: cross-model, Nano Banana Pro/Omni Flash A-B, production pilot, beginner operator, audience comprehension
- Distribution live status: all NOT_RUN
- Simulation and dry runs: tooling only; cannot advance status
- Evidence package manifest: self-excluding SHA-256 inventory
- Candidate class: STRUCTURAL_PRODUCTION_CANDIDATE
- Candidate promotion eligibility: false while live evidence is NOT_RUN
- Security/privacy preflight: required
- V7.6.0 upgrade compatibility: required
- Rollback template: required and honestly unexecuted
- Executable bundled suite: 1 (`dev/run_v780_release6_tests.py`, 14 checks). The remaining R1–R650 rows are manual behavioural checklists, not automated tests.
- Regression range source: canonical release manifest, R1–R650 (verified present and gapless by `validators/validate_release_consistency.py`)
- Test results: external-directory capable
- Clean-extraction validation: required
- Nano Banana Pro/Gemini Omni Flash ownership: preserved
- Audio-attachment-only editor policy: preserved
- Detailed manuals: 52 preserved
- Live cross-model replay: NOT_RUN
- Nano Banana Pro/Omni Flash A-B generation: NOT_RUN
- Complete production pilot: NOT_RUN
- External evidence claimed: false
