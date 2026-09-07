# 05 Video Prompt Manual

## Generation mode first

Declare one:

- `ref2video`: animate an approved reference; preserve visible identity/geometry.
- `text2video`: create fresh motion; best for exploration or elements with no continuity burden.
- `first-last-frame`: interpolate between compatible approved frames.

For an anchored shot, do not repeat a full visible description. State preservation plus motion, timing, camera, environment, and audio.

## Video prompt shape

```text
Purpose in edit:
Starting reference/frame:
Preserve:
Shot size and camera grammar:
One dominant action or intentionally staged sequence:
Environmental/material motion:
Timing/ending:
Audio decision:
Mode-specific constraints:
```

## Anchored I2V template

```text
Use [REF/FRAME ID] as the exact starting composition. Preserve its visible identity, geometry, material, scale, wardrobe, environment, and light direction. Camera: [one named move or locked frame]. Action: [one physically clear beat] with [weight/contact/inertia or animation timing]. Environmental motion: [only relevant elements]. End on [editable ending composition]. Audio: [diegetic cue / native dialogue decision / mute-and-replace]. No unintended cut, second camera move, identity drift, geometry change, text, subtitle, or logo.
```

## Complexity rule

“One action / one move” is a **control default**. A multi-beat shot is acceptable when:

- the story needs continuous choreography;
- the beats share one clear causal action;
- references and model capability support it;
- the prompt gives timing order;
- failure can be cut or split.

Otherwise split the scene at the edit.

## Unified camera grammar

Use the owner in `08` for shot size, movement, continuity, and cut logic. Common move families:

- locked;
- push/pull;
- pan/tilt;
- track/follow;
- orbit/arc;
- crane/rise/drop;
- handheld/POV;
- optical/focus move.

Do not maintain a second competing M1–M5 vocabulary.

## Native dialogue decision

Use **native generated dialogue** when the shot needs visible short lip-sync, the line belongs physically in the scene, and the current surface supports it well enough for the risk.

Use **external voice/dialogue** when wording, brand tone, pacing, localization, continuity, long narration, or revision control matters.

Use **off-camera VO** when lip-sync is unnecessary. See `10_voice_and_dialogue.md`.

For native dialogue:

```text
Speaker: [visible person/character].
Line: "[short exact line]."
Delivery: [emotion and pace].
Ambient/SFX: [diegetic].
No subtitles, music, or extra speech.
```

## First/last-frame

Frames should share compatible identity, geometry, canvas, and visual logic unless the contradiction is the deliberate effect. Describe the transition path—not both images again.

## Failure decisions

- Late degradation → shorten or split the beat.
- Morphing → re-anchor, simplify, remove redundant appearance prose.
- Floaty action → add contact, mass, resistance, and endpoint.
- Chaotic camera → select one movement and remove implicit cuts.
- Unwanted dialogue/music → explicitly mute or replace in post.
- Poor lip-sync → external dialogue, reaction coverage, or off-camera VO.
