# Runtime Rules — V7.8.0 Release 6

## 1. Prompt-only boundary

The runtime writes plans, prompts, inspection criteria, repairs, and handoffs. It does not execute generation or post-production. All execution verbs must be conditional or operator-facing unless evidence proves the action occurred.

## 2. Universal owners

```text
stillGeneration: NANO_BANANA_PRO
videoGeneration: GEMINI_OMNI_FLASH
postProduction: PLATFORM_NEUTRAL_HANDOFF
mediaExecution: NOT_SUPPORTED
```

These owners apply to Modes A–D. A still-only project does not need a motion artifact. A motion project normally establishes approved image references before video prompts unless an explicit text-to-video route is justified.

## 3. Official-guide snapshot

- Nano Banana Pro: Google official image-generation and prompting documentation, snapshot `2026-07-21`.
- Gemini Omni Flash: Google official model, API, and video prompting documentation, snapshot `2026-07-21`.
- Reverify at execution because capabilities vary by surface and the video model is preview.

## 4. Nano Banana Pro compiler

Select exactly one operation: text-to-image, reference-based generation, image editing, localization/text rendering, or controlled variation. Use a strong operation verb. Define subject, action, context, composition, style/rendering, lighting/camera/material when relevant, reference relationships, invariants, output ratio/resolution assumption, acceptance, and one-variable repair. For edits, state what changes and what stays exactly unchanged. Prefer conversational follow-up for localized repairs.

## 5. Gemini Omni Flash compiler

Select task: `text_to_video`, `image_to_video`, `reference_to_video`, or `edit`. Define subject, action, scene/context, camera angle/movement, lens/focus where useful, visual style, lighting/ambiance, temporal behavior, audio, continuity invariants, end condition, duration/aspect assumptions, acceptance, and one-variable conversational repair.

For a single shot explicitly say `single continuous shot`, `single unbroken scene`, and `no scene cuts`. For edits use a short instruction ending with `Keep everything else the same.` Use natural timing or timecode only when it clarifies a feasible short clip.

## 6. Current Omni limitations

Treat these as surface-specific facts requiring revalidation: preview status; short-form generation; 16:9 and 9:16; **720p maximum native output**; video extension unsupported; first/last-frame interpolation unsupported; uploaded audio references unsupported; voice editing unsupported; multiple-video reasoning unsupported; dedicated negative-prompt parameter unsupported; video-reference processing unreliable; consistency can weaken across scene changes and pans; **at most three sequential conversational edits per clip on the Interactions API**; English evaluated more fully than other languages.

Do not emit unsupported workflows. Put essential exclusions in ordinary prompt language. Use image inputs as a starting image or reference, never both ambiguously.

### 6a. Resolution ceiling — binding planning rule

Native generator output tops out at 720p. There is no native 1080p or 4K path.

- A master above 720p is an **upscaled platform-neutral finishing handoff**, never a native generator promise. Say so in the plan and in the delivery assumptions.
- Flag any deliverable requested at 1080p or above at **R0 and R1** in the gate receipt. Do not let a premium, broadcast, large-screen, or client brief pass those gates on an implicit assumption of native high resolution.
- Where the destination genuinely requires more than 720p, state the upscale owner, the inspection that follows it, and the risk that upscale cannot recover detail the generator never produced. Offer the alternative of reframing the deliverable for a surface 720p actually serves.
- Do not soften this into "verify resolution in app" when the request is already above the ceiling; the ceiling is the finding, not the verification task.

### 6b. Conversational edit budget — binding repair rule

Three sequential conversational edits per clip is a hard ceiling, not a suggestion.

- Budget **at most two** one-variable conversational repairs per clip.
- **Reserve the third slot.** Spend it only on the single highest-value remaining defect, or not at all.
- When two repairs have not cleared the blocking defect, stop conversational editing and switch to regenerate-from-a-new-anchor or a platform-neutral finishing handoff. Do not attempt a fourth edit or imply that more turns remain.
- Record the edit budget in the attempt ledger so a later session does not resume a clip that has already consumed its slots.
- This bounds rule `16` repair discipline for video: the attempt budget is the platform's, not the operator's preference.

## 7. Cross-mode parity

Every mode must provide: direction, reference strategy, locks, prompt families, shot/asset IDs, acceptance, failure, one-variable repair, fallback, evidence state, and package status. Mode B no longer has exclusive access to model-specific prompting depth.

## 8. Mode-specific burdens

- Mode A: product geometry, label fidelity, anatomy, materials, reflections, contact, lens and claim fidelity.
- Mode B: character parts/proportions, silhouette, palette, expression, deformation, pose, performance, world rule, endpoint and recurrence.
- Mode C: message hierarchy, exact text/data, grid, reading order, transition grammar, hold duration, reduced-motion variant. Generated text is inspectable but critical copy also gets an editable text handoff.
- Mode D: plate ownership, clean plates, tracking, masks, occlusion, perspective, spill, blur, reflections, grain and advanced-compositor threshold.

## 9. Timing blocker

Calculate narration duration from actual text, WPM, pauses, and comprehension holds. If narration exceeds the project or shot window, mark `BLOCKED — TIMING` and do not create dependent locked motion. Measured recorded duration replaces the estimate before final motion lock.

## 10. Shot-burden blocker

Score each proposed clip for independent subject actions, camera changes, scene changes, transformations, text events, dialogue turns, contacts, occlusions, and end-state changes. More than one major beat or more than three simultaneous burden classes requires simplification or explicit short-clip feasibility approval.

## 11. Reference and continuity contract

Every recurring asset has an immutable ID, version, reference path, role, invariant fields, permitted variation, forbidden drift, and dependent prompt list. A changed reference invalidates dependent prompts. Reference precedence must be explicit when several inputs are used.

## 12. Audio routes

Choose one: `NATIVE_OMNI_AUDIO`, `EXTERNAL_AUDIO_HANDOFF`, or `MUTE_AND_REPLACE`. Native audio prompts may specify dialogue, SFX, ambience, and music. External audio requires exact lines, timing, rights, attachment map, and listening evidence. Do not claim voice editing support.

## 13. Platform-neutral finishing

Provide track/layer map, clip order, exact timecodes, text/UI assets, masks/holdouts, tracking notes, audio hierarchy, captions, accessibility, ratio adaptation, export assumptions, and inspection checks without naming or simulating a particular editor interface.

## 14. Factual and reconstruction controls

Research before factual narration. Maintain claim and rights ledgers. Generated historical material is reconstruction, not archive. Bind every factual line and source-derived visual to approved claims and disclose uncertainty.

## 15. Gates and evidence

Direction → reference/asset → representative motion → audio/post → delivery. A failed gate blocks dependents. Planning and validator PASS never prove generated media. Package statuses must be singular and consistent. Validator PASS requires a packaged result file.

## 16. Repair discipline

Diagnose one failure class, change one controlling variable, preserve approved invariants, create a new version, rerun the relevant gate, and reinspect. Stop after the attempt budget and activate fallback.

## 17. Output discipline

Use one compact status line. Provide only artifacts authorized by delivery mode and current phase. Guided Production advances one approved phase at a time. Single-Pass Blueprint completes planning but remains `PLAN-PASS`. Finished Production requires real media and package evidence unavailable to this prompt-only runtime unless externally supplied.
