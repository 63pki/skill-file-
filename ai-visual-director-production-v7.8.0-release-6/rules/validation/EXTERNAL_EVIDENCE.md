# Triggered External Evidence Module — V7.6.0 Evidence Release

Load this module only for cross-model replay, controlled Nano Banana Pro/Gemini Omni Flash A-B work, production pilots, imported evidence, or external-performance claims.

## Required binding

Every live trial binds the exact prompt file and hash, raw response path and hash, settings and rubric hashes, skill archive, Routing Contract, Project Contract, final runtime receipt, project/benchmark identity, references, provider/model/version, operator, execution time, and provenance level.

## Campaign tracks

Select `CROSS_MODEL_REPLAY`, `NANO_OMNI_AB`, `PRODUCTION_PILOT`, or `ALL_TRACKS`. Unselected tracks are `NOT_APPLICABLE`, never failed or silently required. Configured minimums may exceed but never reduce release-policy floors.

## Cross-model replay

Use one comparable benchmark/control tuple. Minimum release floor: three model configurations, two providers where available, and three clean runs per configuration. Preserve every raw response and validator result.

## Controlled A-B

Baseline and candidate share one immutable A-B control hash covering model/version, settings, references, dimensions, duration, seed when available, audio route, and rubric. Only the intended prompt-system variable differs. Require unique blind independent raters.

## Production pilot

Bind BRIEF → DESIGN → ANIMATIC → ASSET → MOTION → DELIVERY to one pilot, project, contract, runtime receipt, and receipt chain. Delivery requires the actual media file/hash, visual and audio inspection records, export manifest, chronology, and independent final reviews.

## Proof boundary

`SIMULATED_TEST` and `DRY_RUN` test tooling only. Declared provenance and hashes do not prove hidden provider behavior or reviewer honesty. Audience comprehension, rights, superiority, and production validation remain unclaimed until corresponding live evidence passes.
