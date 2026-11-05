# PHASE 1 — CAMPAIGN COMPLIANCE MATRIX (CCM)
## SEGA / VIRTUA FIGHTER CROSSROADS — "Lionel Rafale" trailer clipping campaign

**Source brief:** `SEGA - Virtua Fighter Crossroads Lionel Trailer (2).txt` (verbatim campaign doc)
**Programme owner:** Clipping Culture (manages the campaign on behalf of SEGA)
**Launch date:** 29 Oct 2026
**Matrix status:** LOCKED — every row below is a hard gate enforced in code (`pipeline/campaign.py`).

---

### 1.1 Binding constraints

| Parameter Category | Extracted Guideline Specification | Operational Boundary / Threshold | Enforcement Level |
|---|---|---|---|
| **Mandatory Mentions** | Account tag `@VFCROSSROADS` on TikTok + Instagram; `@SEGA_West` on YouTube Shorts | Exactly one tag, placed immediately after the caption's closing sentence | Hard Gate (Pass/Fail) |
| **Mandatory Mentions** | FTC disclosure — one of `#Ad`, `#Advertisement`, `#Sponsored` | Must appear on its own line, immediately after the account tag. We standardise on `#Ad` | Hard Gate (Pass/Fail) |
| **Mandatory Mentions** | Caption must be used **word for word** — "Do not shorten, reword, or add claims" | Byte-exact match of 4 required segments incl. the three stanzas | Hard Gate (Pass/Fail) |
| **Mandatory Mentions** | On-screen text on **every** post; wording flexible; must describe what is actually in the clip | ≥1 burned-in burst; every claim must be visible in that same clip | Hard Gate (Pass/Fail) |
| **Prohibited Content** | Third-party footage or audio; anything outside the official content folder | Zero tolerance — 100% of frames + audio from `f.io/V0QTpG9W` | Hard Gate (Pass/Fail) |
| **Prohibited Content** | Exaggerated hooks, rage bait, hate bait | All hook copy screened against `PROHIBITED_TERMS` | Hard Gate (Pass/Fail) |
| **Prohibited Content** | False claims, invented stats/dates | Every on-screen claim traceable to approved caption copy or visible footage | Hard Gate (Pass/Fail) |
| **Prohibited Content** | Mislabeling — "a trailer is not *gameplay*" | `MISLABEL_TERMS` banned in burned-in text (see §1.3) | Hard Gate (Pass/Fail) |
| **Prohibited Content** | NSFW, violence, controversy, political, race, gender content | Zero tolerance | Hard Gate (Pass/Fail) |
| **Audio Restrictions** | **NO background music.** "Use only the audio from the official trailer" | Single audio source: the trailer's own stem. No music bed, no added SFX, no trending sound | Hard Gate (Pass/Fail) |
| **Audio Restrictions** | No AI voices / narration / voice clones | Zero synthetic speech anywhere in the mix | Hard Gate (Pass/Fail) |
| **Visual / Brand Specs** | Official logo watermark on **every** clip | `snake_logo_w.png`, 302px wide (28% of canvas), top-centre, `y=272` — full duration | Hard Gate (Pass/Fail) |
| **Visual / Brand Specs** | Platform UI clearance | Top 260px / bottom 420px / right 140px clear of all text + logo | Hard Gate (Pass/Fail) |
| **Visual / Brand Specs** | "High-quality posts only. No blurry or low-effort content." | 1080×1920 (or 1080×1440), H.264 High L4.2, CRF18, yuv420p | Hard Gate (Pass/Fail) |
| **Duration Bounds** | "Video must be at least 10 seconds long" | `10.0s ≤ runtime ≤ 60.0s` (upper bound is our own platform-fit ceiling) | Hard Gate (Pass/Fail) |
| **Language** | English content only | ASCII + approved punctuation only in burned-in text | Hard Gate (Pass/Fail) |
| **Distribution** | Post live ≥ 30 days; likes visible; no paid promotion; ≤5 reposts of same video | Operational — enforced by the poster, flagged in handoff checklist | Hard Gate (Pass/Fail) |
| **Audience** | ≥35% combined USA + Canada audience (page or post) | Operational — verified via OAuth post-flight, not by the editor | Hard Gate (Pass/Fail) |
| **Performance** | ≥0.20% engagement rate (1,000 views → ≥2 likes) | Operational — post-flight metric | Soft (monitored) |

---

### 1.2 Signed gate check

> All rows above are locked. `pipeline/campaign.py` is the single source of truth; the
> renderer and the QA auditor both read from it. No render ships if `validate_caption()`
> or `validate_onscreen_text()` returns a failure, or if any Phase 6 check fails.
>
> Verified programmatically: `python -m pipeline.campaign` → all three platform blocks
> return **PASS — all hard gates clean**.

---

### 1.3 Two genuine conflicts in the brief, and how they were resolved

A real CCM audit surfaces contradictions rather than papering over them. Two exist here.

**Conflict 1 — "gameplay" is simultaneously required and banned.**
The brief bans mislabeling ("a trailer is not *gameplay*"), yet the mandatory, verbatim,
unalterable caption copy contains… `immersive narrative-driven gameplay`.
**Resolution:** the verbatim caption wins — it cannot be edited. The mislabel ban is
therefore scoped to the one place the editor has discretion: the burned-in on-screen text.
`pipeline/campaign.py` enforces this with two separate term lists — `PROHIBITED_TERMS`
(caption + screen) and `MISLABEL_TERMS` (screen only). A single combined list would
either fail every legal caption or let a trailer be labeled "gameplay".

**Conflict 2 — the general directive's hashtag/trending-audio playbook vs. this campaign.**
The house style template calls for trending tags, an appended engagement question, and
optional trending-sound pairing. This campaign forbids all three: the caption must be
word-for-word unaltered, music is prohibited, and audio must be the trailer's own.
**Resolution:** campaign law overrides house template (Asset Whitelist Override §0.3 has
no bearing here; CCM Hard Gates do). Concretely:
- **No** extra hashtags beyond `#Ad`. → hashtags moved into the pinned comment.
- **No** appended engagement question in the caption. → moved to pinned comment.
- **No** trending-sound pairing. → master audio is the trailer stem, full stop.

Both resolutions are enforced in code, not just documented.
