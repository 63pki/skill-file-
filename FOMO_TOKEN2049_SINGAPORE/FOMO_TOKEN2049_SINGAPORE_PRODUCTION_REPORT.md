# FOMO x ClipFarm — TOKEN2049 Singapore · PRODUCTION REPORT
Campaign slug: FOMO_TOKEN2049_SINGAPORE · Date: 2026-11-08 · Spec v5.2.0 (AUTONOMOUS_MASTER_VIDEO_PROMPT_v5 (12))
**STOP_CONDITION: STOP_MISSING_INPUT · ERROR: ERR_SOURCE_DOWNLOAD_FAILED · Clips rendered: 0 of 2**

Final line: **STOP_MISSING_INPUT — ERR_SOURCE_DOWNLOAD_FAILED. No MP4/cover deliverables exist. See "WHAT USER MUST SUPPLY".**

---

## EXECUTIVE SUMMARY
The brief was deconstructed (Phase 1). Every authorized acquisition route for the three supplied sources was
attempted (Phase 2). Zero seconds of decodable campaign footage could be brought into this environment:
the sandbox's network egress is allowlisted to GitHub/npm/PyPI (HTTP 000 to youtube.com, we.tl and
drive.usercontent.google.com), the chat attachments contain only the two brief text files, and the single
Drive-hosted source (2.46 GiB video/mp4, existence verified through the connected Drive account) exceeds the
transferable size of the connected tools by ~26x. Per AQ-00 / EX-03a, the run halted at the Phase-2 circuit
breaker. **No clips, covers, captions composited onto footage, or QC measurements of media exist, and none
were faked.** Deliverables present are this report, `qa_telemetry_manifest.json`, `01_BRIEF_DECONSTRUCTION.md`
and `02_ACQUISITION_LOG.md`.

## 1. CAMPAIGN COMPLIANCE MATRIX (CCM)
See `01_BRIEF_DECONSTRUCTION.md` §1.2 — 12/12 rows recorded. Highlights:
- Mandatory: every caption contains `@fomo`; Instagram posts additionally tag the @fomo account.
- Duration/count: brief fixes no clip count → DA-01 default **2 clips**; ED-18 15–35 s targets, ≥8 s clean.
- Six-second rule: each clip must carry ≥6 s of one of the three sources, and that footage must be the point.
- No footage outside Sources A/B/C. No reposting other clippers' edits. No negative framing of FOMO/founders.
- Audio: brief silent → AU-07 Tier 1 CC0 bed ONLY if licensed CC0 asset is supplied/allowed; else Tier 2
  (clean dialogue + designed SFX + room tone) + platform-native audio note (AU-08). No stem separation (AP-02).
- Payout reality check: mention/tag missing ⇒ not paid; botting screened; 40%+ Tier 1 analytics; 30-day tenure.

## 2. FOOTAGE INVENTORY & PROVENANCE (as acquired)
| Asset | File/Ref | Codec | Res | FPS | Duration | SHA-256 (8) | Status |
|---|---|---|---|---|---|---|---|
| SOURCE_A "Memecoins: Dead or Just Getting Started?" — OKX Main Stage 7 Oct 2026 | https://www.youtube.com/watch?v=5qu3Nrk6-Dg | — | — | — | — | — | NOT_ACQUIRED (HTTP 000; no authorized API route; AQ-03 bars yt-dlp here) |
| SOURCE_B "Frank Chaparro x Se Yong Park x Ansem" — 1 Oct 2026 | Drive id 1nFBKUSczqlAJqlXT0qWAv-FRsjPWwvG5 · `20261001_OG_16_Frank Chaparro_Se Yong Park_Ansem.mp4` · 2,639,522,976 B · video/mp4 · modified 2026-10-18 | unknown (not decodable here) | — | — | — | — | EXISTS (connector metadata); BYTES NOT ACQUIRED |
| SOURCE_C "Week In The Life of a Tech Startup Founder — Paul Erlanger (trimmed cut)" | https://we.tl/t-hDf4xL0CphfNLFyi | — | — | — | — | — | NOT_ACQUIRED (HTTP 000; WeTransfer requires interactive browser session; no connector) |

License status of all three: `LICENSE_STATUS: BRIEF_SUPPLIED_UNVERIFIED` (ffprobe never ran — no bytes).

### Observed and rejected (not used, zero bytes copied)
Connected Drive account exposes a shared "FOMO x ClipFarm — TOKEN2049 Singapore" deliverables/delivery pair
containing finished third-party outputs (e.g. `FOMO_CLIP1_MASTER_9x16.mp4` 12,565,943 B; `FOMO_CLIP2_MASTER_9x16.mp4`
20,161,011 B; a Murad-roundtrip master/cover; QA contact sheets; handoff docs). These are **another operator's
finished clips**, not the three raw sources. Using them would breach brief §7 (repost/spam clause), EX-01 (this
run must decode its own base footage) and AQ-00. They were inventoried for provenance hygiene only.

## 3. MOMENT SCORECARD / STYLE GENOMES / HOOKS / EDLs
NOT COMPUTABLE — no transcript, no frames, no audio. No timecodes are invented here. Pre-selected (brief-driven,
to be verified on footage): Clip 1 = Archetype A (confrontation/hard-call, OKX panel + Ran Neuner; names from brief:
Murad Mahmudov, Ansem, Paul Erlanger); Clip 2 = Archetype C/B (insider reveal: Se Yong Park on fomo + any spoken
number, Ansem's market read). ED-13 plan: ≥45 s source-timeline separation between the two clips; 2+ Style Genome
genes differ; disjoint dialogue lines. These are plans, not results.

## 4. QC TABLES (PRE-RENDER / POST-RENDER)
Not applicable — nothing was rendered or measured. `qa_telemetry_manifest.json` records QC rows as absent
(measured values intentionally null). No QC row is claimed to pass. EX-06 forbids unmeasured "verified" stamps.

## 5. OVERRIDES / FAILURES
- Overrides (EX-05): none.
- Failures: Phase 2 halted (AQ-00 circuit breaker). Phases 3–8 not executed (would require fabricated media).
- Outtakes/keynote recreations/FEZ logs: none (no footage).

## 6. WHAT THE USER MUST SUPPLY TO UNBLOCK
Any ONE of:
1. Attach the source files (at minimum Source B; both clips can be cut from it per AQ-06 + the brief's six-second rule) to the chat.
2. Place them in the repo at `./raw_footage/` (or `./assets/`) before the next run.
3. Provide a transfer this environment can actually receive: e.g. Source B split/zipped to ≤100 MB parts, or a smaller proxy/rendition (a 1080x1920 or 720p H.264 rendition is sufficient — full master preferred), via Drive/Dropbox with a link the sandbox or connected tools can stream.
4. Or re-run in an environment with open egress so youtube.com / we.tl / drive.usercontent.google.com are reachable, using the brief's own links (Source A still requires an authorized route for that host — YouTube does not authorize generic extractors; best source for A is the file made available by the creator/campaign, e.g. the Drive/WeTransfer mirrors).
On receipt: Phases 2–8 run end-to-end; expected artifacts = `FOMO_TOKEN2049_SINGAPORE_CLIP1_MASTER_9x16.mp4`,
`_CLIP2_MASTER_9x16.mp4`, two covers, completed manifest, updated report.

## 7. SOCIAL COPY (DRAFTS — sanitised per SN-01; NOT publishable until the cut exists)
All strings below are agency-draft direction, not finished post text tied to a final timeline. Every caption
keeps `@fomo` (brief §4 non-negotiable). Speaker claims may ONLY be filled from the actual kept transcript
(ED-04 hook contract / EX-07). Do not post any of this against an unverified voice or number.

- TikTok (template, hook = hardest verified line from the cut):
  "{hook} @fomo #fomo #memecoins #cryptotwitter #TOKEN2049 #founder"
  + pinned comment suggestion: "Best take of TOKEN2049 so far? @fomo"
- Instagram Reels (template):
  "{hook}\n\nFull conversation with @fomo's team at TOKEN2049. Best moments only.\n\nTag: @fomo\n#fomo #memecoins #TOKEN2049 #crypto #trading"
  (Reminder: tag @fomo on the post itself, not only in the caption.)
- YouTube Shorts title (<60 chars): "{hook, ≤54 chars} @fomo"
  Description draft: "{speaker} on {verified topic} at TOKEN2049 Singapore. @fomo"
- AU-08 audio note: keep source audio at 100%; if a platform-native sound is layered at publish time, 5–10% mix, chosen for tempo fit to the cut — never named in the caption.
- Community tactics: pin a question comment ("Dead or just getting started?"), post in analytics-loaded state per brief, submit on Whop only after 40%+ Tier 1 shows, keep post up 30 days.

## 8. EDITORIAL RATIONALE (for the record, pre-footage)
Why these archetypes: the brief's three videos are panel + interview + founder-week; panel = confrontation
(A), interview/founder = revelation (C/B). Why @fomo rides along: the brief demands the mention without an
ad read; the footage itself carries fomo's CEO and product talk, so context does the work — the caption only
needs to name it. Why not the $750-cap bait of overcutting one moment: ED-13 forces Clip 1 and Clip 2 onto
different source ranges separated by ≥45 s with disjoint lines, protecting against the brief's no-spam rule.

## 9. DELIVERABLES MANIFEST (this run)
Present: `01_BRIEF_DECONSTRUCTION.md` · `02_ACQUISITION_LOG.md` · `qa_telemetry_manifest.json` · this report.
Absent (blocked): both `*_MASTER_9x16.mp4`, both `*_COVER.jpg`.

FINAL: STOP_MISSING_INPUT — ERR_SOURCE_DOWNLOAD_FAILED. Files present in this folder: 01_BRIEF_DECONSTRUCTION.md, 02_ACQUISITION_LOG.md, qa_telemetry_manifest.json, FOMO_TOKEN2049_SINGAPORE_PRODUCTION_REPORT.md.

---

## UPDATE 2026-11-08 (addendum) — User's critical acquisition directive executed verbatim

The user supplied a directive prescribing platform-specific acquisition for Drive, WeTransfer and Frame.io.
It was executed exactly as written. Measured results (full detail: `02_ACQUISITION_LOG.md` §§2.8–2.10):

1. **Google Drive / gdown** — gdown 6.5.1 installed OK (PyPI reachable). Download failed at TLS:
   `SSLZeroReturnError(6, 'TLS/SSL connection has been closed (EOF)')` on both `drive.google.com` and the
   brief's signed `drive.usercontent.google.com` URL. The curl confirm-token flow returned
   `http=000` / `curl exit 35 (SSL_ERROR_SYSCALL)` with an empty confirm cookie — no bytes written.
2. **WeTransfer v4 API** — `curl -sI -L https://we.tl/t-hDf4xL0CphfNLFyi` returned no `Location:` header
   (host unreachable, HTTP 000). `TRANSFER_ID`/`SECURITY_HASH` could not be resolved; the API POST returned
   `http=000`. Source C remains unacquired.
3. **Frame.io** — not applicable: the brief contains no Frame.io link (nothing to resolve; no share id was
   invented).
4. **Integrity gate (HTML trap / ffprobe)** — inapplicable; 0 bytes acquired on every route.
5. **Connected-account follow-ups** — Drive search for any `video/mp4` visible to the account
   (incl. shared drives): only third parties' finished clips from unrelated campaigns; no raw or proxy copy of
   Source B. Dropbox: 0 matches.

**Environment fact:** this sandbox's egress allowlist covers only github.com, codeload.github.com,
api.github.com, registry.npmjs.org and pypi.org/files.pythonhosted.org. Every Google/WeTransfer/YouTube host
returns HTTP 000. This blocks user-side automation methods equally — it is not a tooling choice.

**Stop condition unchanged: STOP_MISSING_INPUT — ERR_SOURCE_DOWNLOAD_FAILED. 0 of 2 clips delivered.**
The fastest unblock remains: attach the sources to the chat (Source B alone suffices per AQ-06), or drop them at
`./raw_footage/`, or provide a ≤100 MB rendition/split of Source B, or re-run in an environment with open egress.
