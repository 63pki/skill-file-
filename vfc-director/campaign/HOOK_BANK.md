# HOOK BANK & BEAT-SHEET SCAFFOLD

Every string below is drawn from the campaign's own approved wording or from the brief's character
description. **None of them is hype, none invents a stat, a date, or a feature.** A hook may only be
burned in if the clip visually contains the thing it promises — that is the brief's rule
("Only mention features that actually appear in your clip") and it is enforced by the
`requires_in_clip` column.

## Content conditions (verified per clip, from the real shot list)

| Code | Condition | How it is verified |
|---|---|---|
| `C-REVEAL` | Lionel Rafale is introduced on screen | shot list + frame at that timecode exported and inspected |
| `C-CIELO` | Cielo appears in the clip | frame inspection |
| `C-VS` | Lionel and Cielo actually fight | frame inspection across the exchange |
| `C-STORY` | A story/cinematic beat plays (narrative scene, not a VS exchange) | shot list + frames |
| `C-CITY` | The city of Vilasapara is established on screen | frame inspection |

## Ten hooks (5 psychological archetypes × 2) — apply per clip

| # | Archetype | Hook (burn-in text) | Requires | Why it stops a scroll without lying |
|---|---|---|---|---|
| 1 | Contradiction | `A NEW FIGHTER BEAT CIELO` | `C-VS` | Contradicts the expected hierarchy, states only what the brief asserts |
| 2 | Contradiction | `CIELO HAS A RIVAL NOW` | `C-CIELO` | Reframes an existing character's status |
| 3 | Immediate proof | `LIONEL RAFALE vs CIELO` | `C-VS` | The match-up *is* the proof; no claim beyond the frame |
| 4 | Immediate proof | `VIRTUA FIGHTER CROSSROADS` + `LIONEL RAFALE` | `C-REVEAL` | Name-first for search and recognition |
| 5 | Forbidden secret | `HE CAME TO VILASAPARA FOR A REASON` | `C-STORY` | Mirrors the brief's own open question, asserts nothing further |
| 6 | Forbidden secret | `THE CITY HASN'T SEEN HIM YET` | `C-CITY`, `C-REVEAL` | Uses the campaign's “a city you've never seen” line |
| 7 | Negative warning | `DON'T UNDERESTIMATE THE NEWCOMER` | `C-REVEAL`, `C-VS` | Warning framing without a false threat claim |
| 8 | Negative warning | `CIELO ISN'T READY FOR THIS` | `C-CIELO`, `C-VS` | Tension sourced from the “outclassing Cielo” line |
| 9 | Open loop | `WHY DID LIONEL RAFALE COME HERE?` | `C-STORY` | The brief's own question — pure curiosity gap |
| 10 | Open loop | `A STORY YOU'VE NEVER HEARD` | `C-STORY` | Campaign-approved line, exact |

**Winner selection (1.2-second scroll-stop test):** at least 4 of 6 viewers must identify *who* and
*what kind of post* this is within 1.2 s of the first frame. Record two alternates with the chosen
hook in the delivery manifest.

**Hard exclusions:** no "insane", "you won't believe", "best ever", percentages, dates, "free",
"download now", "gameplay" (a trailer is not gameplay). `engine/compliance.py` blocks all of these
automatically.

## Beat-sheet scaffold (instantiate with measured cut times, never with guesses)

| Phase | Window | Visual | Typography | Retention trigger |
|---|---|---|---|---|
| Sensory blitz | 0.00 – 1.20 s | 2–4 micro-cuts (0.15–0.25 s) of the strongest verified frames | none yet | motion + face/impact recognition |
| Deceleration slam | 1.20 s | hard cut to a stable medium close-up | hook appears (fit-verified ≤ 900 px) | contrast break — audio chaos stops |
| Body | every 1.5 – 2.2 s | angle cut, 115 % punch-in, or b-roll cutaway on a measured transient | caption bursts of 1–4 words | pattern interrupt |
| Payoff | 80 – 92 % of runtime | the reveal / the resolution of the rivalry beat | payoff line | reward lands before the loop point |
| Loop | final 0.3 s → frame 0 | motion and audio resolve toward the opening frame | — | frictionless restart |

Cut placement is taken from the measured transient list (`analysis.audio.transients`) and the
measured scene-cut list (`analysis.cuts`) — the engine will not place a cut on a guessed beat.
