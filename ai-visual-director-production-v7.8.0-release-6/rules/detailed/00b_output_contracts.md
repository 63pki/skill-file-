# 00b Output Contracts

Use the smallest contract that makes the answer executable. Omit empty fields.

## Universal header for substantial work

```text
Mode + preset:
Deliverable / platform:
Goal and audience action:
Assumptions:
Evidence or capability checks still needed:
```

## Single image/keyframe

```text
Tool role: image anchor
Reference attachments: [ID → role]
Canvas/aspect: [target; verify tool support if needed]
Prompt level: [Seed / Working / Locked]
Prompt:
[copy-ready prompt]
Critical post additions:
Failure watchlist:
First repair lever:
```

## Single video clip

```text
Generation mode: [ref2video / text2video / first-last-frame]
Purpose in edit:
Start frame/reference:
Duration/settings: [verified values or “verify”]
Camera grammar:
Action and environmental motion:
Audio decision: [native dialogue / diegetic / mute-and-replace]
Prompt:
[copy-ready prompt]
Best fragment/edit note:
Failure watchlist:
```

## Storyboard row

```text
Shot ID | time | story function | frame/shot size | action | camera | audio/VO | transition | reference IDs | mode | status
```

## Full project package

1. Brief and assumptions
2. Mode and concept territories
3. Reference/rights intake
4. Visual DNA and asset bibles
5. Timed storyboard/animatic
6. Image-anchor prompts
7. Video prompts
8. Voice/dialogue script
9. Music/SFX cue sheet
10. Edit, captions, accessibility, delivery
11. Evidence-based QA and repair plan
12. Budget/stop-loss and handoff, when requested

Return all sections together unless guided mode was requested.

## Repair response

```text
Evidence available:
Observed or user-reported symptom:
Likely cause:
Keep unchanged:
Change exactly one variable:
Before → after diff:
Revised prompt:
Test and acceptance condition:
If it fails again:
```

## Capability honesty note

When a volatile fact matters:

```text
Capability note: [claim] is [verified for surface/date OR unverified].
Check: [exact official page or in-app location].
Fallback: [surface-agnostic workaround].
```

## Phased project response

Return one complete phase or prompt batch, then the exact `PROJECT STATE` block from `28_adaptive_next_protocol.md`. Never split an individual prompt or silently omit the remaining scope.

## Reliability gate receipt

Every Production Sequence or Campaign/Long Project must end each phase with the `GATE RECEIPT` from `35`, followed by `PROJECT STATE` from `28`. A downstream deliverable is invalid when its required upstream gate is not PASS or N/A.

## Per-shot four-channel execution pack

When a shot requires both generation and manual/edit execution, keep channels separate:

```text
SHOT ID / approved references / start-end state
A. KEYFRAME IMAGE PROMPT
B. I2V NATURAL-LANGUAGE MOTION PROMPT
C. MANUAL platform-neutral design surface/platform-neutral editing surface KEYFRAME RECIPE (only if requested)
D. FAILURE FALLBACK + ACCEPTANCE CONDITION
TECHNICAL VALUES: VERIFIED [surface/date] or ASSUMPTION — VERIFY
```

Do not compress these channels into one “universal” prompt.

## Spoken timing row

```text
Line ID | exact line | words | assumed rate | estimated/read-aloud time |
pauses + comprehension allowance | allocated window | FITS/REWRITE/SPLIT
```

## No-reference taste plan

If no references were supplied for a substantial visual project, output categories—not fabricated citations:

```text
North-star quality category | construction/material category |
staging/performance category | edit-rhythm category |
sound-identity category | anti-reference categories | original combination rule
```

## Delivery map and compile verdict

Before a Production Sequence or Campaign/Long Project, output the compact `DELIVERY MAP` from `36`. End the phase with `GATE RECEIPT`, `COMPILE`, and—when phased—`PROJECT STATE`. Do not append a skill audit unless the user explicitly requested one.

## Active-version hygiene

Production tables must contain only the approved active version. Move rejected brainstorms, questions, and superseded ideas into a clearly marked archive or remove them. Never leave a rejected prop/action in an active storyboard row and “correct” it later in prose.

## ACTIVE STEP response contract

For every planning/NEXT response under `39`:

```text
ACTIVE STEP CONTRACT
[triggered owners, locked inputs, one primary artifact, acceptance]

CURRENT STEP ARTIFACT
[only this step]

STEP RECEIPT
Evidence:
Verdict:
Frozen dependencies:

COMPILE
PASS | REVISE | BLOCKED

PROJECT STATE + STEP QUEUE

WAITING FOR NEXT — [next step]
```

Do not include completed deliverables from future steps.
