# 07 Reference Intake and Asset Bibles

## Reference intake verdict

Assign every input one verdict:

- **Use:** clear, owned, relevant, and technically adequate.
- **Repair first:** useful but needs crop, cleanup, color neutralization, or missing-view support.
- **Reject:** unowned, contradictory, too degraded, deceptive, or likely to contaminate the result.

## Intake checks

```text
ID / filename:
Rights/consent owner:
Role: [identity / geometry / material / scale / environment / lighting / style / copy]
Resolution/crop/occlusion:
Perspective and lens clues:
Color/white-balance reliability:
Conflicts with other references:
Use / repair / reject:
```

Do not assign two incompatible roles to one reference without saying which wins.

## Bible templates

### Product

```text
Asset ID / SKU:
Shape, proportions, part count:
Material behavior:
Color target and tolerance:
Label/logo placement:
Scale cues:
Approved angles:
Forbidden changes:
Reference IDs:
```

### Character

```text
Character ID:
Identity anchor and consent status:
Age range/build/features:
Wardrobe and continuity variants:
Expression/gesture vocabulary:
Voice ID/token:
On-model rules:
Forbidden changes:
```

### Brand

```text
Brand ID:
Approved logos and clear-space rule:
Palette and type system:
Tone and banned language:
Approved claims/disclosures:
CTA system:
Post-only elements:
```

### Location/world

```text
World ID:
Era/place/architecture:
Recurring props and spatial map:
Time/weather/light logic:
Palette/atmosphere:
Continuity anchors:
Anachronisms/forbidden elements:
```

### Voice

```text
Voice token:
Consent/licensing:
Language/accent:
Pace/energy/warmth:
Pronunciations:
Do/don't:
```

## Token scopes

- **Global:** stable across a campaign/series—identity, product geometry, brand system, voice.
- **Project:** stable inside one production—wardrobe variant, location state, look.
- **Shot:** action, framing, camera, local timing.

Use short IDs in boards and logs. Store full wording once in `19_production_memory.md`.

## Reuse rule

- In text-driven generation, include the needed full token.
- In reference-driven image generation, include role and non-visible invariants.
- In reference-driven video, use the reference ID plus preservation; include only hidden constraints the image cannot communicate.

## Versioning

```text
TOKEN-ID v# | changed variable | reason | evidence/result | active/archive
```

A new version changes one meaningful decision. Do not overwrite the last approved token.

## Canonical-view-first fallback

When a generator cannot maintain one asset across a multi-panel model sheet:

1. generate and approve one neutral canonical front/primary view;
2. use that approved view to produce one three-quarter view;
3. compare silhouette, part count, proportions, palette, and attachment points;
4. continue side/back/state views one at a time;
5. reject drift before creating the next view;
6. assemble the approved views manually into the final sheet;
7. keep rejected alternates out of active reference sets.

A combined multi-panel sheet is a convenience, not proof of consistency. Record each approved view as a separate asset version.
