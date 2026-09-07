# 19 Production Tracker, Continuity Memory, and Handoff

## One naming convention

```text
[project]_[sequence-or-chapter]_[shot-or-asset]_[stage]_[version]_[status].[ext]
```

Example: `launch_CH01_S03_video_v02_approved.mp4`.

Stages: brief, board, still, video, vo, sfx, music, edit, delivery. Never use competing `final_final` conventions.

## Asset tracker

```text
Asset ID | story function | mode | refs/tokens | stage | version/change |
evidence verdict | rights status | cost/attempts | owner | next action
```

## Project memory

```text
Project / deliverable / platform:
Approved brief and concept:
Active global tokens:
Active project tokens:
Approved references:
Storyboard version:
Approved assets:
Rejected attempts + reason:
Capability evidence IDs:
Rights/claims status:
Open issues / next controlled test:
```

## Long-form chapter checkpoint

```text
Chapter ID | purpose | first/last asset | identity/style drift | factual/source issues |
VO status | edit status | verdict | next chapter dependency
```

## Session handoff

Return this at the end of multi-session work:

```text
SESSION HANDOFF
Project:
Last approved stage / asset ID:
Brief + board version:
Active tokens and references:
Completed:
Rejected / do not repeat:
Open blockers:
Next exact action:
Files/context to paste at next session:
```

The skill has no guaranteed cross-session memory. Continuity depends on this record being preserved and supplied again.

## Gate receipt memory

For Production Sequences and Campaign/Long Projects, preserve the latest `35` gate receipt with the project state. Store which downstream assets were frozen by a failed gate and invalidate them explicitly after an upstream revision. Do not keep stale prompts “approved” after their concept, story, asset, timing, or delivery dependency changed.

## Filename compiler check

Before delivery, parse the filename into all six required fields: project, sequence/chapter, shot/asset, stage, version, status. A name such as `Project_MASTER_v1` fails because fields are missing. Example:

```text
milo-shadow_CH00_MASTER_delivery_v01_review.mp4
```

## Cross-model switch packet

```text
MODEL-SWITCH HANDOFF
Project/version:
Execution profile (new runtime resets to CONTROLLED):
Approved brief/mode:
Current STEP QUEUE and one ACTIVE/next READY step:
Locked Style/Brand Bible:
Active asset schemas and approved references:
Approved board/timing:
Latest gate and compiler receipts:
Rejected decisions — do not restore:
Verified specs / assumptions:
Open blockers:
Next authorized artifact only:
```

A new model may not infer completion from prose history or self-promote to FULL.
