# 28 Adaptive NEXT and Long-Project Delivery Protocol

Use when a complete project would become truncated, unreadable, or prompt quality would suffer in one response. This is a continuity protocol—not an excuse to provide incomplete fragments.

## Routing decision

- **Quick Shot:** complete now; no NEXT.
- **Small Production Sequence:** planning-first; after planning, execute one queued step per NEXT. Do not complete multiple dependent deliverable families in one response merely because they fit.
- **Large Sequence / Campaign / Long-form:** planning-first; execute one queued step per NEXT and preserve state.

Signals to phase:

- many shots, scenes, chapters, languages, or deliverable ratios;
- long per-shot prompts or scripts;
- approval is required before downstream work;
- later prompts depend on references, boards, or decisions not yet approved;
- a single response would force shallow, compressed, or truncated outputs.

## Canonical phases

```text
P0 — Intake: brief, operator/tool profile, quality target, rights, references, capability blockers
P1 — Direction: reference/taste calibration, audience promise, concept territories, originality rejection, memory device, sound identity, mode, Visual DNA
P2 — Board: story beats, film-language storyboard/animatic, continuity and asset plan
P3 — Assets: commercial control, bibles, reference sheets, mode-craft and still/keyframe prompt batches
P4 — Motion: mode-craft, continuity, video prompt batches and coverage/edit relationships
P5 — Audio/Post: sound identity, VO/dialogue, Foley/SFX/music cue sheet, edit and captions
P6 — Review/Delivery: evidence checks, no-ship gate, repairs, variants, export and handoff
```

Skip or combine phases when the request does not need them. Never force a campaign protocol onto one prompt.

## Batch rules

- A batch contains only complete prompts/assets with stable IDs.
- Default batch size is chosen by complexity and readability, not a fixed token quota.
- When the user specifies `NEXT [count]`, treat it as `BATCH` intent. Default to one step. Batch only independent sibling items with identical passed dependencies; otherwise state why one step is the safe count.
- Do not begin a downstream batch while a blocking upstream decision is unresolved.
- Preserve exact active tokens and approved decisions; do not silently paraphrase them between batches.

## End-of-response progress block

Every phased response ends with the `GATE RECEIPT` from `35`, then:

```text
PROJECT STATE
Project / version:
Operating level:
Completed and approved:
Delivered this response:
Active tokens/references:
Open blockers or assumptions:
Reliability controller (`35`): PROCEED TO [stage] / REVISE — NO-SHIP / BLOCKED
Commercial-excellence gate (`31`, when applicable): PASS / REVISE / BLOCK / NO-SHIP
Taste/reference verdict (`32`, when applicable): CALIBRATED / REVISE BOARD / TARGETED REPAIR / REJECT OUTPUT
Beginner operator action (`33`, when applicable):
platform-neutral editing surface/platform-neutral design surface handoff (`34`, when applicable):
Next phase / next asset IDs:
Recommended command: NEXT [optional count]
Other commands: REVISE [ID] | SKIP TO [phase] | SUMMARY
```

## NEXT behavior

On `NEXT`:

1. Read the latest project state.
2. Continue from the named next phase/asset ID.
3. Do not repeat finished content unless needed for context.
4. Restate only the active constraints required by the new batch.
5. End with an updated project state.

## Revision behavior

On `REVISE [ID]`, freeze unrelated approved work. Show:

```text
KEEP:
CHANGE:
WHY:
DEPENDENCIES AFFECTED:
UPDATED VERSION:
```

If the revision invalidates downstream prompts, name them explicitly and mark them pending; do not silently leave stale outputs active.

## Skip behavior

On `SKIP TO [phase]`, record skipped dependencies and continue only when safe. Use assumptions for reversible creative choices. Refuse to bypass blocking rights, consent, claim, or capability checks.

## Session continuity

For work spanning sessions, pair this protocol with `19_production_memory.md`. The last project-state block is the minimum handoff the user should retain.

## Mandatory phase triggers

Use phases rather than one oversized response when any two apply: more than six detailed shots; recurring model sheets plus scene prompts; storyboard plus voice/sound/edit; multiple ratios/languages; long per-shot four-channel packs; or approval is needed before downstream prompts. Phase boundaries follow dependencies, not arbitrary length. P1 cannot advance without the R1–R3 receipts required by `35`; P3/P4 cannot advance without the relevant asset and board receipts.

## Activation-compiler handshake

`36` decides whether phases are mandatory before drafting. A package with four or more deliverable families, more than six detailed shots, model sheets plus motion prompts, or script-controlled timing must not be compressed into one response unless the DELIVERY MAP gives a concrete reason all activated artifacts remain complete and readable. Every phase ends with GATE RECEIPT, COMPILE, and PROJECT STATE.

## V6.8 planning-first override

For Production Sequence and Campaign/Long Project, `39_mandatory_next_step_protocol.md` overrides older “complete in one readable response” behavior. First response = planning only. Each NEXT = one READY step. High model capability does not bypass this focus rule; it changes depth within the step, not the number of dependent steps executed.
