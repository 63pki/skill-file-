# 13 Animation and Cartoon Manual

## Core quality order

```text
style consistency → silhouette/staging → shape/line → shading → palette → expression → timing
```

Do not apply photoreal pores, film stock, or anti-plastic language to stylized work.

## Style Bible

```text
Family: [flat 2D / cel / stylized 3D / cutout / clay / painterly / comic / pixel / other]
Shape language and proportions:
Line weight/color:
Shading model:
Palette and accent rule:
Texture/material convention:
Background/detail level:
Animation timing convention:
Forbidden style drift:
```

Avoid trademarked studio shorthand such as “Pixar-style.” Describe the actual shape, lighting, material, and animation qualities.

## Character production

Create a neutral model sheet and expression/pose library; store it in `07`. For each shot, prioritize readable staging and one emotional beat. Use anticipation, action, reaction, overshoot, and holds intentionally.

## Animation video template

```text
Use [CHAR/STYLE REF IDs] as the on-model source. Preserve silhouette, proportions, outfit, line, palette, and shading. Staging: [clear screen position and eyeline]. Action: [beat with anticipation/action/reaction]. Camera: [locked or motivated move]. Timing: [snappy/held/exaggerated]. Audio: [voice/SFX plan]. No photoreal conversion, palette drift, extra character, or shape mutation.
```

## Dialogue

Use the decision in `10`. A talking character needs mouth-shape feasibility, reaction coverage, and an external-dialogue fallback.

## Kids-directed work

Route consent, platform audience settings, advertising restrictions, manipulative CTA risk, scary themes, and data collection through `21`. Do not use fear hooks designed for adults.

## Character asset schema

Before prompting a recurring animated character, lock:

```text
Character ID:
Canonical silhouette:
Body parts that exist:
Body parts that do not exist:
Movement method:
Gesture method:
Face construction:
Identity anchors:
Scale relative to other characters:
Shadow/contact rule:
Palette:
Outline ratio:
Shading rule:
Scene-state variants:
Forbidden anatomy and transformations:
```

Do not let later prompts invent arms, hands, feet, a neck, separate head, facial features, or movement mechanics absent from the canonical schema. Replace human anatomy words with the asset’s actual construction.

Important magical/story objects with recurring behavior require separate IDs and asset rules; do not refer to the same asset by changing generic names across scenes.

## True model-sheet gate

A recurring character is not locked by description alone. Its model-sheet prompt must request:

- front, three-quarter, side, and back views;
- neutral pose and consistent scale;
- expression row;
- action/gesture row;
- palette and outline/shading reference;
- shadow/contact/attachment point;
- identity anchors and forbidden-change list;
- neutral background and no scene-state effects unless labeled as variants.

Return **MODEL SHEET READY** only when every view uses one consistent silhouette, anatomy, proportion, palette, and style rule. Otherwise return **REVISE CHARACTER SCHEMA**.

## 2D cutout execution appendix

For cutout/paper/vector workflows, define per recurring asset:

```text
Layer/piece map:
Parent-child hierarchy:
Pivot/anchor points:
Neutral pose:
Key storytelling poses:
Mouth/eye states when used:
Allowed squash/stretch:
Occlusion order:
Contact/shadow layer:
Reusable entrance/exit actions:
```

For each shot, provide a compact pose/timing chart:

```text
Beat | pose/state | hold | moving layers | pivot | interpolation/easing intent | fallback still
```

Do not invent joints that the character schema forbids. This appendix is optional for drawn frame-by-frame animation and mandatory only when the chosen workflow uses reusable cutout layers.
