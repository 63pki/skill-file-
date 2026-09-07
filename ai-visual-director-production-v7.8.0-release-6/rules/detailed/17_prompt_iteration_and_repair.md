# 17 Prompt Lint, Diff, Iteration, and Repair

## Pre-generation prompt lint

- [ ] Correct mode vocabulary?
- [ ] Clear output purpose and canvas?
- [ ] Reference IDs each have one role?
- [ ] Anchored video avoids re-describing visible identity?
- [ ] One coherent lens/light/style world?
- [ ] Action and camera complexity intentional?
- [ ] Critical text/logo reserved for post?
- [ ] Suppression line short and mode-specific?
- [ ] Volatile settings verified or marked to verify?
- [ ] No unsupported claim or copyrighted-style imitation?
- [ ] Vague quality words converted into observable visual, optical, light/material, sound, or edit decisions?
- [ ] Concept-specific memory device and sound identity preserved when required by `31`?

Flag undefined uses of: `cinematic`, `epic`, `premium`, `engaging`, `dynamic`, `dramatic`, `stunning`, `beautiful`, `futuristic`, `emotional`, `high quality`, `professional`, `viral`, `luxury`, `powerful`, and `cool`. Do not delete the intended feeling; translate it into controllable decisions.

## Diagnostic sequence

1. Name the visible/user-reported symptom.
2. Separate prompt cause, reference cause, model limit, and post issue.
3. Freeze the KEEP list.
4. Change one causal variable.
5. Show the exact diff.
6. Define acceptance before rerunning.
7. Log the result.

## Diff format

```diff
KEEP: identity, composition, product geometry, camera, duration
- Lighting: dramatic cinematic light
+ Lighting: one soft window key from camera-left; stable exposure; no second source
REASON: removes conflicting light logic
ACCEPT IF: direction remains camera-left through the full usable fragment
```

## Experiment card

```text
Hypothesis:
Control prompt/version:
Single changed variable:
Everything held constant:
Current surface/settings:
Evidence/result:
Verdict: keep / reject / inconclusive
Reusable only within:
Next test:
```

## Escalation

```text
clarify words → fix/select reference → simplify shot → change generation mode →
change tool/surface after capability probe → repair in post → discard
```

Do not intensify adjectives when the actual problem is a bad reference, unsupported control, or over-complex shot.

## Conversational edit budget (video clips)

Gemini Omni Flash allows at most three sequential conversational edits per clip on the Interactions API. Treat that as the attempt budget, not as room to iterate freely.

```text
Edit 1 — highest-leverage single variable.
Edit 2 — one more single variable, only if edit 1 held.
Edit 3 — RESERVED. Spend only on the single worst remaining blocking defect, or not at all.
After 3  — stop. Regenerate from a newly approved anchor, or hand off to platform-neutral finishing.
```

Rules:

- Never attempt a fourth conversational edit or imply that more turns remain.
- Never bundle two variables into one edit to "save" slots; a bundled edit is unauditable and usually costs two.
- If the blocking defect is identity or geometry, do not spend conversational edits on it at all — re-anchor with a fresh still and regenerate. Conversational edits cannot restore an identity the clip never had.
- Log consumed edit slots per clip ID and version in the tracker (`19`) so a later session does not resume an exhausted clip.
- This platform ceiling overrides operator preference and any larger attempt budget declared elsewhere in the project.

## Style and asset contradiction linter

Before generation, check:

```text
[ ] Palette values are valid and consistently formatted
[ ] Gradient rule is consistent
[ ] Shading rule is consistent
[ ] Glow/bloom rule is consistent
[ ] Outline rule scales with output rather than relying on arbitrary pixels
[ ] Character anatomy matches the canonical asset schema
[ ] Body-part/action language uses only defined construction
[ ] Scene-state variants are separated from permanent character design
[ ] Shadow/contact/attachment behavior is consistent
[ ] Environment and character style families are compatible
[ ] Magical/world rules use stable asset IDs and behavior
[ ] No prompt contradicts the approved Style Bible or quality mode
```

When a contradiction appears, do not average both instructions. Name the conflict, choose the canonical owner, update dependent prompts, and version the changed token.
