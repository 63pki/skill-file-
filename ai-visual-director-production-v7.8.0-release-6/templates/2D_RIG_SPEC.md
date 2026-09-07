# 2D Rig Specification

```text
2D RIG SPEC
Project/version / asset ID / method / software surface:
Canonical schema/reference IDs:

LAYER MAP
Layer ID | visual content | parent | pivot | draw order | mask/occlusion | deformation | visibility states | export group

PIVOT AND CONSTRAINT MAP
Part/layer | pivot location | allowed translation/rotation/scale/deformation | limit | contact dependency | failure mode

REPLACEMENT STATES
State ID | replaces | trigger | transition rule | continuity lock

MOTION GRAMMAR
Idle / locomotion / turn / stop / take / reaction / gesture / blink-eye / overshoot-settle / forbidden

VALIDATION
Part count / volume / silhouette / pivot drift / layer pop / contact / occlusion / naming / tool compatibility
Evidence IDs:
VERDICT: PASS | REVISE | TOOL TEST REQUIRED
```
