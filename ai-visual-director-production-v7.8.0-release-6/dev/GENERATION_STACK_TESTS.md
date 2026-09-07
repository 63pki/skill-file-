# V7.0.1 Nano Banana Pro and Gemini Omni Flash Stack Tests

| ID | Input | Required behavior | Fail if |
|---|---|---|---|
| G1 | “Use Nano Banana Pro for images” | Load Nano adapter and output target-specific image prompts | Only generic image advice |
| G2 | “Use Gemini Omni Flash for videos” | Load Gemini Omni Flash adapter and select T2V/I2V/first-last mode | Manual editor recipe replaces prompt |
| G3 | Nano + Gemini Omni Flash, no platform-neutral design surface/platform-neutral editing surface | Complete generation pipeline without requiring editors | platform-neutral design surface/platform-neutral editing surface becomes mandatory |
| G4 | Nano-approved keyframe to Gemini Omni Flash | Stable frame ID/version and preservation block | Undefined/unapproved anchor |
| G5 | Mode B cartoon | Animation language in Nano Banana Pro/Omni Flash prompts | Photoreal leakage or generic motion only |
| G6 | Gemini Omni Flash native audio unknown | Verify surface or mute-and-replace fallback | Native audio support invented |
| G7 | Exact Gemini Omni Flash/Nano limits unknown | ASSUMPTION — VERIFY | Frozen universal limits |
| G8 | Failed Gemini Omni Flash identity | Re-anchor to Nano, simplify/split, re-inspect | Same prompt repeated unchanged |
| G9 | platform-neutral design surface/platform-neutral editing surface requested for post | Separate optional operation card | Editor controls mixed into generator prompt |
| G10 | Final compilation | Nano prompts, Gemini Omni Flash prompts, stack handoff table present | Generation deliverables omitted |
