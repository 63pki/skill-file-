# Hermes Vision Configuration Guide

This guide configures optional inspection; it does not change the text-only mission.

## Required status declaration

```text
VISION STATUS
Host vision available: YES / NO / UNKNOWN
Asset attached and accessible: YES / NO
Asset actually processed: YES / NO
Inspection basis: DIRECT OBSERVATION / USER REPORT / NONE
```

Only `DIRECT OBSERVATION` permits visual-quality findings.

## Configuration sequence

1. Enable a Hermes-compatible vision model/surface in the host configuration.
2. Confirm supported image/PDF attachment types and size limits in the current host documentation.
3. For video, extract representative frames/contact sheets and inspect audio separately when supported; do not claim full-video review from one frame.
4. Pass asset IDs and source metadata into the Evidence Binder.
5. Separate observed facts from inference.
6. If vision is unavailable, use user-reported symptoms and return `PREFLIGHT ONLY` or `OUTPUT NOT INSPECTED`.

## Inspection checklist

- correct asset/version;
- frame/crop and resolution adequate for review;
- identity/geometry/style continuity;
- text/logo accuracy;
- artifact/morphing/contact issues;
- comparison against approved references;
- limits of the observation.

Never claim listening, timing, motion continuity, or export integrity from still-image inspection alone.
