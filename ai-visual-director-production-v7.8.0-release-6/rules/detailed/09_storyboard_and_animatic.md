# 09 Storyboard and Animatic

A shot list names assets. A storyboard defines frames. An animatic tests timing and edit logic before expensive motion.

## Storyboard table

| Field | Purpose |
|---|---|
| Shot ID | traceability |
| Time in/out | edit duration |
| Story function | why the shot exists |
| Frame description | visible composition, not mood alone |
| Shot size/lens | perspective |
| Action | one beat or ordered beats |
| Camera | direction, speed, endpoint |
| Screen direction/eyeline | continuity |
| VO/dialogue | exact line/time |
| SFX/ambient/music | audio cue |
| Transition/cut | relation to adjacent shots |
| Reference IDs | identity/world anchors |
| Generation mode | text/ref/first-last |
| Post layers | logo/type/VFX/captions |
| Status | draft/approved/generated/rejected |

## Frame description test

A frame description should let another person sketch the image without guessing:

```text
WHO/WHAT is WHERE, doing WHAT, viewed from WHICH SIZE/ANGLE, under WHICH motivated light,
with WHAT foreground/background relationship, leaving WHERE for motion/type.
```

## Animatic method

1. Place board frames on the target timeline.
2. Add scratch VO/dialogue.
3. Add rough music pulse and essential SFX cues.
4. Hold each frame only as long as the information/emotion needs.
5. Test the opening without sound.
6. Test the story with only sound.
7. Cut any shot with no unique function.
8. Lock approximate timing before generating delivery motion.

## Short-form beat map

```text
0–opening: immediate tension/proof
hold: mechanism, escalation, or question
turn: new information or sensory change
payoff: deliver promise
push: one clear action/brand close
```

Do not hardcode universal second marks; fit the beat map to the actual duration and platform.

## Long-form chapter board

```text
Chapter ID | purpose | open loop | sections | visual modes | recurring anchors | re-hook | payoff | transition
```

Then create shot rows only for the current approved chapter. Avoid planning hundreds of clips as an undifferentiated list.

## Board approval gate

- [ ] Every shot has one unique story/edit function.
- [ ] Geography and screen direction are understandable.
- [ ] The hook/payoff relationship is honest.
- [ ] VO duration fits the visual plan.
- [ ] Post-only elements are identified.
- [ ] Expensive identity-critical shots have references.

## Scene, shot, and generation-clip distinction

- **Scene:** a story unit that may contain several shots.
- **Shot:** one continuous camera view with one edit relationship.
- **Generation clip:** one generator request; it may provide only the usable portion of a shot.

Do not convert each scene into one generation prompt automatically. Split a scene when it includes multiple camera views, several speakers, independent actions, a reveal plus reaction, or more motion than one controlled clip can hold.

## Shot feasibility gate

Before writing a video prompt, confirm:

```text
[ ] One primary emotional/information beat
[ ] One dominant action or clearly ordered causal action
[ ] One camera intention and endpoint
[ ] One clean start state
[ ] One clean ending state / edit point
[ ] Dialogue and reaction time fit the target edit duration
[ ] Identity/reference burden is feasible
[ ] No hidden internal cut or second shot
[ ] Cutaway, reaction, insert, still, or post fallback exists
[ ] Current generation duration/control verified for the named surface
```

If any item fails, split, simplify, or redesign the shot before prompting. Never compress an overloaded scene into one long prompt merely to reduce prompt count.

## Mode-pure board fields

Use only fields that help the declared mode:

- **Mode A photoreal:** shot size, perspective/lens character, motivated light, physical action/contact, camera, production design.
- **Mode B animation:** staging, silhouette/pose, shape/line/palette state, anticipation/action/reaction/hold, layer or rig dependency; lens fields only when perspective is intentionally cinematic.
- **Mode C motion graphics:** message, hierarchy, layout state, element entrance/hold/exit, easing meaning, exact editable type/data.
- **Mode D hybrid:** live/generated layer ownership, perspective/scale/light match, matte/occlusion/contact, transition into/out of composite.

Do not mechanically copy photoreal fields into animation or design boards.
