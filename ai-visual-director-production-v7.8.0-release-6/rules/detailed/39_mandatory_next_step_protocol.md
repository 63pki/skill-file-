# 39 Mandatory NEXT Step Protocol

This protocol makes NEXT operational rather than advisory. Use for every Production Sequence and Campaign/Long Project.

> **Authority.** This file is the active NEXT scheduler. `36_runtime_activation_compiler.md` §E fails compilation when no STEP QUEUE exists, and `00a_router.md` makes this file mandatory for every Production Sequence and Campaign/Long Project. Nothing in it is archived.
>
> **Version history.** V6.9 issued one *micro-step* per NEXT, which produced 20+ round trips on a normal project. V6.10 replaced that with one READY step per NEXT and internal batching inside the step. The batching rule is in §6 and is binding: siblings with identical passed dependencies ship together. `../RUNTIME.md` §17 states the same rule at phase granularity.

## 1. First response: planning only

The first response may contain:

- brief diagnosis and assumptions;
- operating level and mode;
- request-to-rule activation map;
- rights/capability blockers;
- concept-direction plan or compact territories when required to define dependencies;
- STEP QUEUE;
- Planning Gate Receipt;
- PROJECT STATE.

It must not silently complete all downstream deliverables.

## 2. Build the STEP QUEUE dynamically

Create only steps relevant to the project. Example families:

```text
P0 Planning and activation
S1 Concept/taste direction
S2 Story/mechanism lock
S3 Style/brand/visual system
S4 Recurring asset schemas/model sheets
S5 Environment/location/design assets
S6 Storyboard/animatic
S7 Script/VO timing
S8 Keyframe prompts and approval
S9 Motion/manual/fallback packs
S10 Sound identity/cue sheet
S11 Edit/platform-neutral editing surface/platform-neutral design surface assembly
S12 Evidence QA/repair
S13 Delivery/handoff
```

Reorder by dependency. Non-narrative work may omit S2; still-image work omits motion/audio/edit steps. Each step has one primary artifact family.

```text
STEP QUEUE ROW
ID/name:
Depends on:
Active owners:
Primary artifact:
Acceptance condition:
Status: LOCKED | READY | ACTIVE | PASS | REVISE | BLOCKED | SKIPPED
```

Only one step may be ACTIVE.

## 3. NEXT command semantics

- `NEXT`: execute exactly the first READY step.
- `REVISE [ID]`: revise exactly that artifact/step and freeze dependents.
- `SUMMARY`: return state only; create no new artifact.
- `SKIP TO [ID]`: allowed only if dependencies are PASS/N/A; otherwise BLOCK.
- `BATCH [IDs]`: allowed only for independent sibling items with identical passed dependencies; compiler may reduce the batch.
- `NEXT 8` or other count syntax: interpret as a request to batch, but default to one step and require the batch safety check. Never compress quality to satisfy a count.

## 4. Response boundary

Each NEXT response contains:

1. ACTIVE STEP CONTRACT;
2. only the current step artifact(s);
3. creator self-check;
4. gate/critic receipt;
5. compiler verdict;
6. updated STEP QUEUE and PROJECT STATE;
7. `WAITING FOR NEXT — [next READY step]`.

Do not begin the next step, preview its deliverables, or append optional work.

## 5. Failure behavior

If the current step is REVISE/BLOCKED/NO-SHIP:

- keep it ACTIVE or REVISE;
- freeze downstream steps;
- provide the smallest repair/test;
- end `WAITING FOR REVISE [ID]` rather than NEXT.

## 6. Focus rule

“One thing at a time” means one primary artifact family, not one sentence, and not one asset. A Style Bible is one step. A storyboard is one step after schemas and timing dependencies pass.

**Sibling batching is the default, not an exception.** When several items share one artifact family and have identical passed dependencies, they belong in one step under the `BATCH` rule in §3. Splitting them is what wastes the operator's attention, not what protects quality.

Apply this to model sheets: the sheets for three recurring characters are three sibling instances of one artifact family, so they are **one step**, provided all three share the same approved style/brand dependency. Do not create one step per complex asset by default.

Split siblings into separate steps only when one of these is true:

- their upstream dependencies differ, so one is READY and another is not;
- one is already REVISE or BLOCKED while the others are clean;
- the batch would exceed what the operator can review carefully in one pass — say so and name the split;
- the CONTROLLED profile's critic cannot hold all of the batch's locked invariants at once, in which case `38` reduces the batch and records why.

A step is one reviewable unit of work. Its size is set by dependency state and reviewability, never by asset count.

## 7. Completion

The project is complete only when every requested queue item is PASS/N/A and the evidence maturity matches the claim. The final response may say `PLANNING COMPLETE`, `TEST READY`, `ASSEMBLY READY`, or `DELIVERY READY` only under `38` maturity rules.
