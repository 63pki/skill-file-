# 03 Capability Verification — No Stale Spec Tables

This file intentionally contains **no permanent model IDs, prices, caps, or platform numbers**. Those facts change by product surface, tier, region, date, and provider.

## What must be verified

Verify when the answer depends on:

- current model name or ID;
- supported input/output types;
- duration, resolution, frame rate, aspect, or reference count;
- prompt or character limits;
- native audio, dialogue, first/last-frame, extension, or seed support;
- regional or plan availability;
- pricing/credits;
- commercial terms, licensing, watermarks, disclosure, or retention policy;
- export limits or platform delivery specifications.

## Verification order

1. Current in-app model/settings panel for the user’s exact surface.
2. Official product documentation or model card.
3. Official release notes/help center.
4. Official provider documentation when the provider is the access layer.
5. Creator/community observations only for behavior—not authoritative limits, price, or rights.

Record evidence in `27_evidence_registry.md`.

## Ask for the surface, not just the model

```text
Tool/model family:
Surface: [consumer app / studio / API / cloud / third-party]
Plan/tier:
Region:
Date checked:
```

The same model family may expose different controls on different surfaces.

## If verification is unavailable

Do not stall. Give:

1. a surface-agnostic plan;
2. the exact capability the user must check;
3. the in-app or official-doc location to inspect;
4. a fallback.

Example:

```text
Check the video model’s settings/model card for maximum clip duration and first/last-frame support.
If unsupported, split the beat into multiple clips and bridge them with an edit or a newly approved start frame.
```

## Planning without volatile numbers

- Plan clips as short, editable beats rather than one long take.
- Use the delivery canvas chosen for the destination; verify generator support before promising native output.
- Split long narration by semantic sections and current model limits.
- Export using the destination’s current official recommendations rather than remembered bitrate numbers.
- Quote cost only after current unit price and expected attempt count are known.

## Capability probe for a new tool

Before a paid job, test with non-sensitive material:

```text
identity/reference obedience | geometry | text | hands/faces | material behavior |
camera control | action complexity | clip stability | audio behavior | aspect control |
iteration controls | watermark/rights | cost per usable result
```

The probe produces observations, not universal claims. Save the surface/date and failures in `27`.

## Technical-value honesty gate

Do not provide frame counts, frame rate, native clip ceiling, resolution, bitrate, loudness target, export setting, model ID, reference count, or platform-safe area as a universal production fact.

For every load-bearing technical value:

```text
Value needed:
Exact tool/surface/tier/destination:
Current official or in-app evidence:
Verified date:
Status: VERIFIED / VERIFY IN APP / NOT AVAILABLE
Surface-agnostic creative plan:
Fallback:
```

If the value is unverified, describe creative timing and control intent without false precision. Frame-level counts belong only to a workflow that actually exposes frame-level control. Do not infer a generator’s supported duration from the storyboard duration.
