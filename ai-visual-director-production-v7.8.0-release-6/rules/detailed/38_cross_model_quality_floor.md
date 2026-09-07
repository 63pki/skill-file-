# 38 Cross-Model Quality Floor

Use for every Production Sequence and Campaign/Long Project. Different models have different creative ceilings; this protocol preserves one minimum acceptance standard by changing granularity, review, and stopping behavior—not by lowering quality.

## 1. Execution profiles

### FULL

Use only when the current runtime has objective evidence of constraint retention, contradiction detection, causal closure, timing arithmetic, and evidence honesty. FULL still obeys one-step NEXT.

### CONTROLLED — default

Use when capability is unknown or mixed:

- one queued step per response;
- one complex artifact or 1–3 independent sibling items;
- exact output contracts;
- restate locked IDs/invariants needed by the step;
- calculate rather than estimate loosely;
- critic receipt before PASS;
- no release authorization from self-confidence.

### INSUFFICIENT

Use when the runtime repeatedly loses constraints, invents evidence, cannot reconcile contradictions, or fails basic timing/ID checks:

```text
BLOCKED — MODEL CAPABILITY
Failed demonstrated capability:
Production risk:
Safe work still allowed:
Required stronger-model/human/deterministic review:
Next recovery test:
```

## 2. Objective capability probe

Do not ask “Are you capable?” Use demonstrated behavior. In maintenance/benchmark mode, test:

1. constraint retention: preserve five locked constraints;
2. contradiction detection: undefined anatomy/parts;
3. causal closure: temporary effect presented as permanent;
4. timing arithmetic: words, WPM, pauses, runtime;
5. evidence honesty: no output exists, so no output PASS;
6. ID integrity: downstream asset references must resolve.

```text
MODEL EXECUTION PROFILE
Constraint retention: PASS/FAIL
Contradiction detection: PASS/FAIL
Causal closure: PASS/FAIL
Timing arithmetic: PASS/FAIL
Evidence honesty: PASS/FAIL
ID integrity: PASS/FAIL
Profile: FULL / CONTROLLED / INSUFFICIENT
Evidence/date/session:
```

No named model receives automatic trust; profiles are behavioral and session-specific.

## 3. Same standard, different workload

All profiles use the same gate acceptance conditions. CONTROLLED profile receives smaller tasks and more review. INSUFFICIENT profile cannot issue production release. Do not compensate for weakness with generic filler, fewer artifacts, invented assumptions, or self-awarded PASS.

## 4. Independent critic requirement

For CONTROLLED profile, separate creation and approval:

```text
CREATOR PASS: produces only the current step artifact.
CRITIC PASS: compares artifact to locked inputs and acceptance contract.
VERDICT: PASS | REVISE | BLOCK | NO-SHIP.
```

Prefer a different/stronger model or human critic. If the same model performs both passes, label `SELF-CRITIC — NOT INDEPENDENT`; final delivery still requires evidence-based review.

## 5. Deterministic checks

Where the host supports scripts or structured validation, check mechanically:

- requested durations sum correctly;
- board and prompt durations agree;
- every referenced ID exists;
- every spoken line has timing math;
- required four-channel fields exist;
- active tables contain no Draft/TBD/question/rejected option;
- filenames contain all canonical fields;
- precise values have classifications;
- gates do not PASS ungenerated/uninspected assets;
- revisions invalidate dependent artifacts.

If deterministic execution is unavailable, return the same checklist with explicit values. Do not claim it ran.

## 6. Release maturity

- **PLAN-READY:** brief, concepts, schemas, board/timing plan pass.
- **TEST-READY:** references/model sheets/keyframes and low-cost proof pass.
- **ASSEMBLY-READY:** required media exists and was inspected.
- **DELIVERY-READY:** final edit, mix, captions, rights, specs, and export were inspected.

Never jump maturity levels. Text planning alone cannot authorize DELIVERY-READY.

## 7. Cross-model handoff

On model/runtime change, use the canonical handoff in `19`. The new model starts CONTROLLED and may not reinterpret approved locks without a named revision.
