# Official Prompt Guide Alignment — Snapshot 2026-07-21

## Nano Banana Pro

Sources:
- https://ai.google.dev/gemini-api/docs/image-generation
- https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana

Mapped capabilities: text-to-image, reference-based generation, conversational editing, controlled variations, text/localization, reference roles, aspect/resolution assumptions, acceptance and repair.

## Gemini Omni Flash

Sources:
- https://ai.google.dev/gemini-api/docs/omni
- https://ai.google.dev/gemini-api/docs/video
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide

Mapped capabilities: text-to-video, image-to-video, reference-to-video, existing-video editing, stateful conversational editing, starting-image/reference roles, continuous-shot control, natural/timecode timing, native audio, exact text prompting and simple edit locks.

Mapped limitations: preview status, short-form surface limits, 720p maximum native output, no extension, no first/last interpolation, no uploaded-audio reference, no voice editing, no multiple-video reasoning, no dedicated negative parameter, unreliable video-reference processing, three-edit conversational ceiling, and consistency risk across scene changes or pans.

## Resolution ceiling and conversational edit budget — evidence

Two limitations are promoted into binding planning rules because they change what should be promised and how many repairs remain. They are recorded here with their sources and snapshot so the staleness machinery covers them.

| Fact | Value | Source class | Snapshot |
|---|---|---|---|
| Maximum native video resolution | 720p; no native 1080p or 4K in the current preview | Official model documentation and provider launch announcement, corroborated by independent provider reviews | 2026-07-21 |
| Sequential conversational edits per clip | 3 (Interactions API multi-turn session history) | Official provider launch announcement for the Interactions API | 2026-07-21 |

Planning consequences, enforced by `rules/RUNTIME.md` 6a and 6b:

- A master above 720p is an upscaled platform-neutral finishing handoff, never a native generator promise. Deliverables at 1080p or above are flagged at R0 and R1.
- At most two one-variable conversational repairs per clip; the third slot is reserved. After three, regenerate from a new anchor or hand off to platform-neutral finishing.

Both remain preview-stage facts. Revalidate on the same 90-day ceiling as the rest of this alignment record, and revalidate immediately on any general-availability announcement, because GA is the most likely point at which the resolution ceiling changes.

This mapping proves documentation alignment only, not successful media generation.
