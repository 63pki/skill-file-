# Audio Attachment to Generated Clips

This is the only editor-operation guide in the active skill. It is platform-neutral and does not authorize any editor as an image or video generator.

## Inputs

For every shot record: clip ID/version, exact start/end time, narration/dialogue file, SFX file, ambience file, music cue, required silence, and whether Gemini Omni Flash native audio is retained, muted, or replaced.

## Attach audio

1. Import the approved generated clip and the approved audio files into the editor available to the operator.
2. Place the clip on the picture track at its locked timecode.
3. Place narration/dialogue on a dedicated voice track and align its first audible word to the shot cue.
4. Place synchronized SFX on a separate track at the visible contact/action frame.
5. Place ambience under the full scene and use short overlaps across cuts when continuity requires it.
6. Place music on its own track; keep entry, exit, and ducking decisions from the cue sheet.
7. If Gemini Omni Flash produced native audio, choose one declared route: `KEEP_VERIFIED_NATIVE`, `MUTE_AND_REPLACE`, or `SEPARATE_IF_SUPPORTED`. Never layer conflicting dialogue or duplicate impacts.
8. Trim clip or audio handles without deleting required reaction and comprehension holds.
9. Add short fades only to prevent clicks or abrupt ambience; do not use automatic effects by default.
10. Export a synchronized review file and inspect it from start to finish.

## Acceptance

- Every spoken line occurs once and fits its assigned window.
- Visible contact and synchronized SFX agree.
- Dialogue is intelligible; music does not mask speech.
- No doubled native/external audio, clipping, clicks, abrupt ambience, or missing silence.
- The final frame and reaction holds remain intact.
- The reviewed export path/hash is recorded before any audio or release PASS.

If the active editor cannot perform one operation, label it `UNVERIFIED`, use the closest generic timeline operation, or block. Do not invent menu names or controls.
