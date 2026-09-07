# 06 Anchor Pipeline and Token Behavior

## Control-path decision

Use an approved still/reference before motion when identity, product geometry, brand form, repeatability, or client approval matters. Text-first generation remains valid for exploration, atmospheric inserts, abstract motion, and disposable B-roll.

## Anchor loop

```text
reference intake → neutral asset/reference sheet if needed → hero/scene still →
look approval → motion proof → batch generation → edit review
```

## Token behavior by mode

| Mode | What to include |
|---|---|
| `text2image` | full subject and visual description |
| `ref2image` | reference role + preservation + non-visible invariants; avoid fighting the image |
| `text2video` | enough subject/world description for a fresh shot |
| `ref2video` | reference ID + preservation + motion/camera/audio; no full visible restatement |
| first/last-frame | frame IDs + transition path + invariants |

This resolves the former conflict between “paste the Bible verbatim” and “redact I2V descriptions.” Bible tokens are not pasted blindly into every mode.

## First/last-frame chain

Use chaining only for genuinely continuous action. A new scene should start from a newly approved keyframe rather than inheriting accidental drift.

Review at each link:

- identity and geometry;
- screen direction and eyeline;
- light and time continuity;
- wardrobe/prop state;
- action endpoint/start point;
- grade and canvas.

## Escalation ladder

1. Fix story/shot in text.
2. Approve a low-cost still or board frame.
3. Prove motion at the cheapest useful setting.
4. Generate delivery-quality variants only after the motion proof passes.

Exact tiers and settings depend on current verified tool capability (`03`).
