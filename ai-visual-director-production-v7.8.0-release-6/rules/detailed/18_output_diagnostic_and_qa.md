# 18 Evidence-Based Output Diagnostic and QA

The skill must not pretend it can review an unseen result.

## Evidence declaration

Start every review with one:

```text
Evidence: attached image inspected directly.
Evidence: attached video/audio inspected directly.
Evidence: user-reported symptoms only; verdict is conditional.
Evidence: no output evidence; cannot issue an asset verdict yet.
```

## If the result is not available

Ask the user to inspect and report only relevant symptoms:

### Photoreal/product

- Does identity/geometry match the approved reference?
- Are hands, labels, parts, reflections, shadows, and contact stable?
- Does one light direction remain plausible?
- Does motion preserve mass and material?

### Animation

- Does silhouette, proportion, line, palette, shading, and outfit remain on-model?
- Is the acting readable? Did unwanted realism appear?

### Motion graphics

- Is hierarchy readable at delivery size?
- Are text/data exact and editable? Are grid and easing consistent?

### Audio/edit

- Is speech intelligible? Are seams, unwanted native audio, masking, clipping, caption errors, or abrupt ambience present?

## Canonical R/Y/G rubric

No competing numeric scores.

- **GREEN — approve:** on brief; no blocking safety/rights issue; defects are invisible or acceptable at delivery size.
- **YELLOW — repair:** core asset is usable; defect can be fixed in prompt, post, or one controlled regeneration.
- **RED — regenerate/discard:** wrong identity/geometry/concept, persistent morphing, broken story function, or blocking rights/claim problem.

## Commercial-excellence no-ship gate

When `31` applies, do not recommend shipping if the concept remains interchangeable or cliché-led; the opening promise is unclear or unpaid; identity, geometry, continuity, typography, data, claims, or sound has a visible blocking failure; the edit feels like unrelated generated clips; rights/disclosures are unresolved; or required delivery/accessibility checks are incomplete.

A no-ship result must name the smallest valid next action: restructure, repair in post, controlled regenerate, obtain rights/evidence, or discard.

## Review card

```text
Asset ID:
Evidence:
Brief/story function: G/Y/R — reason
Identity/style: G/Y/R — reason
Craft/motion: G/Y/R — reason
Audio/edit/delivery: G/Y/R — reason
Safety/rights: PASS/BLOCK — reason
VERDICT: approve / repair in post / controlled regenerate / no-ship / discard
Commercial-excellence gate (`31`, when applicable): PASS / REVISE / BLOCK / NO-SHIP
One changed variable or post action:
Lesson to log:
```

## First-frame check

For scroll-led work, test at small size and without sound:

- one focal read;
- visible tension, proof, or curiosity specific to the concept;
- no dead frame or premature logo unless intentionally justified;
- text legible and not duplicating the visual;
- the opening promise is paid off later.

## Reliability no-ship additions

Return **NO-SHIP** or **BLOCK** when any applies:

- story cause, consequence, and resolution contradict one another;
- a recurring character uses undefined anatomy, movement, gesture, or attachment rules;
- a magical or recurring story asset lacks a stable ID/reference;
- dialogue and comprehension time cannot fit the storyboard;
- one generation prompt contains several camera views, hidden cuts, unrelated actions, or speaker exchanges;
- palette, gradient, shading, glow, outline, shadow, or state rules contradict;
- technical settings are invented, stale, or unverified for a load-bearing decision;
- the response claims nonexistent files, paths, exports, generations, inspections, tests, or successful repairs;
- the skill modified itself without an explicit maintenance request;
- a long response bypassed adaptive phases and left deliverables truncated or silently omitted.

The no-ship response must identify the canonical owner, smallest corrective action, affected dependencies, and acceptance condition.
