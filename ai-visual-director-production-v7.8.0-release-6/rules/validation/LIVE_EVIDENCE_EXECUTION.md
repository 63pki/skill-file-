# Live Evidence Execution Runbook

## Boundary

This release provides import, binding, and validation infrastructure. It does not contain live model runs, generated media, beginner trials, or audience reviews. Keep every live status `NOT_RUN` until independently supplied evidence passes its track validator.

## Track order

1. Freeze the skill ZIP and detached SHA-256.
2. Freeze Routing Contract, Project Contract, runtime receipt, prompt, settings, references, rubric, and benchmark IDs.
3. Execute outside the skill package on the declared provider/model/surface.
4. Preserve raw request/response, provider receipt where available, generated media, and all hashes.
5. Perform independent review after execution; preserve blinding, conflicts, uncertainty, and excerpts.
6. Build a self-excluding evidence manifest.
7. Validate external trials and human sessions.
8. Compile status only from validator outputs. Never hand-edit a PASS.

## Release floors

- Cross-model replay: 3 model configurations, 2 providers, 3 clean comparable runs per configuration.
- Nano Banana Pro/Omni Flash A-B: at least 1 matched control pair and 2 unique blind independent ratings per trial.
- Production pilot: BRIEF → DESIGN → ANIMATIC → ASSET → MOTION → DELIVERY, one binding chain, real delivery media, visual/audio inspection, export manifest, and 2 independent final reviews.
- Beginner operators: 5 independent completed sessions using the frozen package.
- Audience comprehension: 3 privacy-safe, appropriately consented, version-bound sessions when such review is appropriate.

## Prohibited upgrades

`SIMULATED_TEST`, `DRY_RUN`, self-review, generated metadata, prompts, hashes without files, or declared receipts without execution cannot advance live status. The validators cannot prove hidden provider behavior, reviewer honesty, rights, generalization, child safety, or market success.
