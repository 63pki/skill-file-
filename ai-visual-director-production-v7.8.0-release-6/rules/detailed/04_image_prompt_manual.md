# 04 Image Prompt Manual

## Role

Use the image stage for hero frames, products, characters, environments, thumbnails, design assets, reference sheets, and first/last frames.

## Mode gate

- **Photoreal:** physical light, lens perspective, materials, contact shadows, controlled imperfection.
- **Animation:** style family, silhouette, line, shape, shading, palette, on-model identity.
- **Motion graphics:** hierarchy, grid, palette, type, icon family, negative space.
- **Hybrid:** create clean plates and isolated layers for compositing.

Never leak photoreal skin/grain language into animation or flat design.

## Prompt order

```text
Output purpose → subject → reference roles → state/action → environment → composition →
mode-specific craft → critical constraints → canvas/aspect → post-production reservations
```

## Prompt levels

- **Seed:** subject + visual idea; for territory exploration.
- **Working:** adds composition, mode-specific craft, and canvas.
- **Locked:** adds approved reference roles and non-visible invariants.

More words are not inherently more control.

## Photoreal keyframe template

```text
Create a [purpose] keyframe of [subject] in [environment].
Use [REF ID] for [identity/geometry/material] only.
Composition: [shot size, placement, foreground/midground/background, movement/text space].
Lens perspective: [one coherent focal-length feel].
Light: [motivated source, direction, contrast/falloff].
Material behavior: [specific reflection/refraction/texture/contact].
Atmosphere/grade: [only what serves the concept].
Preserve: [load-bearing invariants].
Do not introduce: [short mode-specific suppression].
Canvas: [target aspect/orientation; verify support].
Reserve critical logo, CTA, legal copy, and subtitles for post.
```

## Reference-sheet template

```text
Create a neutral [turnaround/contact/location] sheet of the SAME [asset].
Views/panels: [list]. Vary only [named dimension].
Keep identity/geometry, scale, wardrobe/material, palette, and neutral light consistent.
No beautification, hybridization, new features, labels, or hero lighting.
Treat panel count and cross-panel consistency as targets to review, not guarantees.
```

## Typography

Generated text is exploratory. If short display text is useful, quote exact copy and define hierarchy and placement. Add logos, prices, CTA, subtitles, disclosures, and fine print in an editable design/post layer.

## Mode-aware suppression library

Use only relevant constraints:

```text
Product: no shape/part/count change; no alternate label; no extra logo.
Person: no identity/age/feature drift; no extra fingers; no beauty-filter smoothing.
Animation: no photoreal conversion; no line-weight/palette/outfit drift.
Design: no pseudo-text; no off-grid clutter; no inconsistent icon family.
Clean plate: no subject, text, watermark, baked shadow, or unwanted depth effect.
```

Long negative lists can introduce noise. Prefer one positive invariant plus a concise prohibition.
