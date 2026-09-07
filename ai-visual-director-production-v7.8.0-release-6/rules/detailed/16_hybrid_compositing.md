# 16 Hybrid and Compositing Plan

Mode D needs a layer plan, not “mix styles and grade them together.”

## Composite breakdown

```text
Background/clean plate:
Foreground subject/product:
Generated character/effect:
Mattes/masks needed:
Tracking points:
Contact shadow/reflection:
Occlusion order:
Lens/perspective match:
Light direction/color temperature:
Grain/sharpness/motion blur match:
Editable type/brand layers:
```

## Workflow

1. Create/approve the background clean plate.
2. Create isolated foreground assets with compatible angle and light.
3. Plan masks, occlusions, contact, and tracked movement.
4. Generate motion only for layers that benefit from it.
5. Composite in the editor; match scale, perspective, edge softness, black level, color, grain, and blur.
6. Add shadows/reflections that connect layers physically.
7. Review frame edges and contact at full size and in motion.

## Common failures

- sticker look → missing contact, edge, grain, or light integration;
- scale drift → no shared reference plane;
- sliding overlay → weak tracking points;
- mismatched worlds → perspective/light/color conflict;
- baked text/effects → regenerate clean layer and rebuild in post.

State when a requested effect exceeds a simple platform-neutral editing surface plan and requires a more capable compositor; do not imply the skill performs compositing.
