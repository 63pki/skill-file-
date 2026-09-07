# Production Candidate Policy

## Meaning

`STRUCTURAL_PRODUCTION_CANDIDATE` means the package is internally consistent, migration-compatible, rollback-capable, security-preflighted, reproducibly packaged, regression-tested, and ready for controlled external qualification. It does not mean live production performance has been proven.

## Candidate issuance gates

- Canonical release identity and R1–R650 catalog
- V7.6.0 baseline path preservation
- Immutable Nano Banana Pro, Gemini Omni Flash, and Nano-to-Gemini Omni Flash guide hashes
- Runtime manifest integrity
- Source and clean-extraction deterministic suites
- Security and privacy preflight
- Upgrade compatibility and rollback-template validation
- Clean ZIP and detached SHA-256
- Honest five-track evidence status

## Promotion boundary

Candidate issuance is allowed while live evidence remains `NOT_RUN`; production promotion is not. Promotion beyond candidate requires PASS for cross-model replay, Nano Banana Pro/Omni Flash A-B, complete production pilot, beginner-operator pilot, and audience-comprehension review. Do not convert structural validation into a live-performance claim.

## Rollback

A deployment must instantiate the rollback template with the exact prior archive, checksum, trigger, owner, recovery steps, verification steps, and evidence disposition. The distributed template is not an executed rollback.
