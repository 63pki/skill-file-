# Optional Animation Style Families

Use with core `13_animation_manual.md`. Choose a family by its actual construction—not by copying a studio or artist.

| Family | Construction vocabulary | Strong use cases | Main drift risk |
|---|---|---|---|
| Flat 2D/vector | bold or controlled outlines, flat fills, limited palette, simple geometric shadows | explainers, mascots, kids | gradients/3D creep |
| Cel animation | clean line art, stepped cel shadows, expressive poses, controlled highlights | narrative/action | inconsistent faces and shadow bands |
| Stylized 3D family animation | rounded shape language, soft global light, tactile surfaces, appealing proportions | character ads, family stories | accidental photoreal skin/material |
| Cut-paper/collage | layered flat shapes, visible paper edges, shallow cast shadows | quirky explainers/story | inconsistent material scale |
| Clay/stop-motion | matte clay, fingerprints/tool marks, frame-by-frame holds, handmade sets | whimsical ads | smooth CGI conversion |
| Storybook painterly | watercolor/gouache texture, soft edge hierarchy, restrained palette | calm stories | brush/detail drift |
| Graphic novel/comic | ink contours, halftone or block shadows, panel-aware staging | history/drama | unreadable texture/noise |
| Pixel art | fixed pixel scale, limited palette, crisp nearest-neighbor edges | games/retro | mixed resolutions/smoothing |
| Whiteboard/doodle | marker line, simple symbols, progressive reveal | education | random handwriting/pseudo-text |

## Style token template

```text
Family:
Shape language/proportions:
Line:
Shading:
Palette:
Texture/material convention:
Background detail:
Timing convention:
Forbidden drift:
```

## Character acting vocabulary

```text
anticipation → readable key pose → action → reaction → hold
```

For repeated characters, build neutral turnarounds, expression sheets, hand/prop rules, and a voice token. For dialogue, board reaction coverage and use the native-versus-external decision in core `10`.
