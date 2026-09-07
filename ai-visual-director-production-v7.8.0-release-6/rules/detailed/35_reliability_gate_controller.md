# 35 Reliability Gate Controller

This is the binding release controller for every Production Sequence and Campaign/Long Project. It converts distributed craft rules into dependency-aware pass/fail receipts. It is broad: ads, films, products, documentary, animation, motion graphics, faceless video, hybrid work, and client delivery use the same controller with different relevant gates.

## 1. Gate status vocabulary

- **PASS:** required evidence is present and internally consistent.
- **REVISE:** creative/production defect with a defined repair.
- **BLOCK:** missing rights, capability, reference, approval, or user input prevents a safe decision.
- **NO-SHIP:** proceeding would predictably waste credits or create unacceptable risk.
- **N/A:** gate truly does not apply; state why.

Never mark PASS because a section exists. Mark PASS only when the receipt names its evidence.

## 2. Dependency graph

```text
R0 scope/honesty/rights/capability
  ↓
R1 brief + mode + taste calibration
  ↓
R2 concept originality + one-frame thesis + memory device + sonic thesis
  ↓
R3 story/mechanism causality and durable resolution
  ↓
R4 recurring asset schema + true model sheets/reference locks
  ↓
R5 timed storyboard + shot feasibility + spoken timing
  ↓
R6 separated keyframe/I2V/manual/fallback execution packs
  ↓
R7 motivated sound/edit + verified delivery plan
  ↓
R8 evidence-based output QA + ship/repair decision
```

Skip a gate only when N/A. Never bypass a failed upstream gate by producing downstream polish.

## 3. Binding gate requirements

### R0 — Scope, execution honesty, rights, capability

Evidence: requested deliverable; what the host actually did; rights/consent/claims status; named tool surface or visible verify-in-app placeholders. Reject invented files, exports, tests, platform variants, technical specs, cron/automation, or legal ownership guarantees.

**Resolution ceiling flag (mandatory):** if any requested deliverable is 1080p or above, or is described as broadcast, cinema, large-screen, or premium master, R0 cannot pass silently. Record the requested resolution, the 720p native ceiling, and the consequence: masters above 720p are an upscaled platform-neutral finishing handoff, never a native generator promise. See `rules/RUNTIME.md` 6a.

### R1 — Brief, mode, and taste

Evidence: Mode A/B/C/D; audience/context; promise/action; supplied-reference roles or a reference-category plan containing north-star quality, construction/material, staging/performance, edit rhythm, sound identity, and anti-references.

**Resolution ceiling flag (mandatory):** carry the R0 resolution finding forward. Any deliverable at 1080p or above must show, in the brief itself, either an accepted upscale handoff with its owner and inspection step, or a reframed deliverable that 720p native output actually serves. A premium or client quality target does not raise the native ceiling. See `rules/RUNTIME.md` 6a.

### R2 — Originality

Evidence: mechanically different territories; category clichés rejected; selected one-frame thesis; recurring visual memory device; ownable sonic identity when audio matters; why the direction belongs only to this brief. A palette, lens, grade, or adjective alone cannot pass.

### R3 — Causality/mechanism

Evidence: setup → cause → visible consequence → meaningful choice/action → durable resolution. Ask: “What keeps the solved state solved after the hero/product/demo leaves?” Ads and explainers use problem → mechanism → proof → consequence → CTA. Unsupported proof cannot pass.

### R4 — Asset control

Evidence for each independently drifting recurring entity: stable ID; anatomy/geometry/part count; movement; gesture; contact/attachment points; allowed states; scale; palette/material/style; forbidden changes. A recurring complex character/product requires true model-sheet deliverables, not a hero portrait. Magical/detachable/effect entities get separate IDs.

### R5 — Board feasibility and timing

Evidence: scene/shot/generation-clip distinction; one unique function per shot; start/end state; one dominant action or deliberately ordered causal action; one camera intention; continuity; fallback. Split on independent discovery, reaction, decision, transformation, speaker, or camera change. Spoken content requires line-by-line word count, estimated/read-aloud duration, pauses, comprehension allowance, and allocated window.

### R6 — Execution-channel separation

Each shot pack must visibly separate:

1. keyframe image prompt;
2. natural-language I2V/motion prompt;
3. manual platform-neutral design surface/platform-neutral editing surface/keyframe recipe when requested;
4. failure fallback and acceptance condition.

Do not put editor coordinates/easing into a generic I2V prompt. Do not claim one instruction works unchanged across generators and editors.

### R7 — Sound, edit, technical delivery

Evidence: project-specific sound thesis/motif; cue-level role; motivated cut/transition/effect decisions; no universal crossfades, vignette, glow, LUT, gamma, speed ramp, or numerical grade recipe. All volatile values are verified for the named surface/date or labeled **ASSUMPTION — VERIFY** with check location and fallback.

For children, do not direct engagement, purchase pressure, urgency, shame, fear, parasocial manipulation, or “like/share/subscribe” language at the child. Use a story close or clearly adult-facing co-viewing note. Never invent a platform variant.

### R8 — Evidence QA

If outputs are not attached/observable, issue **PREFLIGHT ONLY**—not an output-quality pass. If outputs exist, compare them against approved references and acceptance conditions. Decide ACCEPT, REPAIR IN POST, REGENERATE, or DISCARD.

## 4. Gate receipt

Return after every substantial phase:

```text
GATE RECEIPT — [phase/project version]
R0 Scope/rights/capability: PASS|REVISE|BLOCK|NO-SHIP|N/A — evidence
R1 Brief/mode/taste: ...
R2 Originality: ...
R3 Causality/mechanism: ...
R4 Assets/model sheets: ...
R5 Board/timing/feasibility: ...
R6 Execution channels: ...
R7 Sound/edit/delivery: ...
R8 Evidence QA: ...
Frozen downstream dependencies:
Smallest corrective deliverable:
Cheapest validation test:
Acceptance condition:
Release verdict: PROCEED TO [stage] | REVISE — NO-SHIP | BLOCKED
```

Show all gates for a full project; for a narrow task, show only relevant gates plus R0.

## 5. Output lint before sending

Fail and repair the response if any are present:

- unresolved cause/effect or temporary resolution presented as permanent;
- recurring asset action uses undefined anatomy/parts;
- “model sheet” lacks required views/rows;
- generic concept without thesis/memory/sound identity;
- no-reference project silently invents taste instead of a category plan;
- overloaded shot with independent actions/reactions/camera changes;
- spoken lines lack fit verification;
- generator prompts and manual keyframes are mixed;
- exact technical number lacks evidence or an assumption label;
- ownership is guaranteed or a platform/surface is invented;
- children receive manipulative CTA;
- edit uses automatic decorative effects;
- filename violates `19`;
- phased response lacks `PROJECT STATE` and this receipt;
- off-mission automation/tool instructions appear unrequested;
- completion is claimed while a blocking receipt remains.

## 6. Cost-control rule

When a blocker remains, authorize only the cheapest useful diagnostic: concept rewrite, logic map, style tile, model sheet, neutral keyframe, short motion proof, scratch VO timing, or editor mockup. Do not recommend full motion generation until dependent gates pass.

## Scope-closure guard

Do not append an audit of the skill, recommendations for future skill development, automation instructions, or business advice to a creative deliverable unless explicitly requested. The final section should close the requested production work, gate status, and next authorized production action only.

## Cross-model evidence rule

A gate may PASS only from the required artifact, not from confidence or a statement that the rule was followed. Under CONTROLLED profile, creation and critic verdict are separate sections. If the model cannot produce the artifact without losing locks, reduce the step size or return `BLOCKED — MODEL CAPABILITY`.
