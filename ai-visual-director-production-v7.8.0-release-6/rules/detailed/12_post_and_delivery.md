# 12 Post-Production, Accessibility, and Delivery

## Timeline ownership

```text
V1 main picture | V2 alternates/overlays | V3 brand/type/captions | V4 VFX/mattes
A1 dialogue/VO | A2 Foley/SFX | A3 ambient | A4 music
```

## Picture edit procedure

1. Build the target orientation and verified delivery settings.
2. Sync VO/dialogue and picture to the approved board.
3. Trim unstable heads/tails; keep only usable fragments.
4. Cut on information, reaction, action, sound, match, or contrast—not generator endpoints.
5. Match exposure, white balance, saturation, black level, and grain/texture by mode.
6. Add logos, CTA, legal copy, UI, and typography as editable overlays.
7. Review at actual phone size and without sound.

## AI-footage repair in post

- Hide brief morphing with motivated cutaways/inserts.
- Freeze or speed-ramp only when the style supports it.
- Add motion blur only to match actual motion.
- Do not use grain to excuse broken geometry or identity.
- Replace inconsistent native audio instead of layering more noise over it.

## Mix procedure

1. Solo and clean dialogue/VO.
2. Add room tone/ambient continuity.
3. Place synchronized Foley/SFX.
4. Add music and duck it under speech.
5. Check transitions and silence intentionally.
6. Check for clipping, masking, and abrupt ambience changes.
7. Listen on headphones and phone speaker.

## Captions and accessibility

- Provide captions when speech or story-critical audio exists.
- Prefer editable/soft captions where supported; burn in only where feed behavior requires it.
- Proofread; retime by phrase; keep lines short and readable.
- Use strong contrast and safe placement over changing backgrounds.
- Include speaker labels and meaningful sound labels when accessibility captions are required.
- Do not rely on color alone.
- Avoid hazardous flashing and gratuitous motion.
- Provide transcript/audio description when the deliverable requires it.

Exact caption speed, safe zones, loudness, codec, bitrate, duration, and resolution are current platform facts: verify via `03` and log in `27`.

## Aspect and reframing decision

- Generate per-ratio when composition, movement, or type placement is critical.
- Crop a master only when the subject, look-room, and motion survive the new frame.
- Protect faces, hands, products, captions, logo, and CTA.
- For multiple ratios, board each crop before generation and reserve adaptable negative space.

## Delivery checklist

```text
[ ] Current destination specs verified
[ ] Correct canvas, frame rate, color/profile, codec, audio, and captions
[ ] Brand/type/disclosures editable and inside current safe zones
[ ] No missing frames, clipped audio, caption errors, or unintended native sound
[ ] Accessibility and photosensitivity checks passed
[ ] Rights/claims gate passed
[ ] Filename/version matches 19
[ ] Final file watched from start to end on destination-like devices
```

## Motivated-effect gate

Do not prescribe a universal crossfade, vignette, glow, LUT, gamma/lift value, speed ramp, zoom, or transition duration. For every non-cut effect state:

```text
Effect/transition:
Story/information/continuity reason:
Why a hard cut or unprocessed image is insufficient:
Reference/world-rule dependency:
Acceptance condition:
```

Use hard cuts for clean changes of action or information. Use dissolves only for motivated time, memory, emotional, or visual continuity. Match clips to the approved reference rather than applying identical numbers.

## Numerical-value classification

Label precise values as `LOCKED CREATIVE VALUE`, `CALCULATED VALUE`, `VERIFIED SPEC — surface/date`, or `ASSUMPTION — VERIFY`. Percentages, frame counts, opacity, easing, grade, mix, export, and safe-zone values must not appear authoritative without this classification. Test creative values against the approved reference and revise when they do not improve the result.
