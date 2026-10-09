# AVD 8.7.0 — exploratory prompt visual-probe report

**Run date:** 2026-10-08
**Target identity:** `SKILL.md` 8.7.0; `release/RELEASE.json` and `PACKAGE_MANIFEST.json` identify Release 16 / 8.7.0.
**Archive:** `/tmp/avd-8.7.0-cumulative.zip` — SHA-256 `4790157ee898f46e81612fcc339ffd3a06e53d5707d2be6b3d1125098d23d17d`.

## Result and evidence ceiling

**External visual probe:** 10 image generations completed and were manually inspected; a further generation was refused after the image tool's per-turn limit of 10. No video was generated. These are exploratory outputs, not final approved assets.

This is **not a Nano Banana Pro validation**. The available Arena image-generation tool did not expose its model/version, while the 8.7.0 target names `NANO_BANANA_PRO` for stills and `GEMINI_OMNI_FLASH` for video. `rules/RUNTIME.md` §2 declares `mediaExecution: NOT_SUPPORTED`; `SKILL.md` says the skill “does not directly generate, edit, inspect, listen to, assemble, or export media.” The images here were generated and inspected separately with Arena tools; they do not change the AVD package's own execution boundary or prove generator-specific performance.

The exact six prompt blocks from the earlier planning response were not saved in the workspace and are not present in the condensed context. Accordingly, these are **fresh reconstructions from the retained brief summaries**, not verbatim replay of the earlier prompt wording. Where the original package/bottle details were absent, the images use visibly generic, unbranded placeholders. The exact text sent for each successful output is preserved in [PROMPTS_USED.md](PROMPTS_USED.md). No external sources were used. The generator tool did not expose a model/version or a source snapshot, so no current-model capability claim is made.

## Output index and inspection notes

| Brief | Output(s) | Visual result / disposition |
|---|---|---|
| **1 — orange-cat model sheet** | [PNG](brief-01-cat-model-sheet.png) | Four views, three expressions, teal collar and a wave study are visible; identity is broadly consistent. The wave study is cut off at the lower canvas edge. **TEST-PASS for sheet structure only; REVISE crop before using as a lock.** Six-second motion prompt remains **NOT_RUN**. |
| **2 — fintech title-card frame** | [first probe](brief-02-fintech-style-frame.png), [CRAFT-verbatim correction](brief-02-fintech-style-frame-v2.png) | Left subject / right negative-space hierarchy appears. First output has a conspicuous full-frame grid; v2 still makes the grid and rounded placeholder bars visually prominent. **REVISE** grid strength and avoid bars that can read as pseudo-UI. No FDIC claim, exact copy, final card, or three-second motion was generated/readability-tested. |
| **3 — coffee-bag hero** | [first proxy](brief-03-coffee-hero-proxy.png), [CRAFT-verbatim correction](brief-03-coffee-hero-proxy-v2.png) | Left-side pouch and right-side copy reserve read clearly. In v2 the generator added an unrequested cup despite the exclusion; the bean row also approaches the copy area. **REVISE** prop exclusion and confine the repeat. Both pouches are generic placeholders: package geometry, supplied product text, material, label and brand fidelity are **not tested**. |
| **4 — coffee feedback directions** | [warm-practical first probe](brief-04-warm-practical-direction.png), [product-only first probe](brief-04-product-only-warm-direction.png), [warm-practical CRAFT-verbatim correction](brief-04-warm-practical-direction-v2.png) | Both directions are visually distinguishable. The user selected **warm practical/lived-in trace**. The first warm version puts a cup in copy space; v2 moves it left but the cup/bean line still adds competing detail. The product-only version has the cleanest copy reserve but was not selected. **Direction selected; final product prompt still awaits the actual package reference/specifications.** Neither image is final product art or a valid matched A/B because the pouch is generic and the test histories differ. A direction-specific proxy edit draft is in [BRIEF-04-WARM-PRACTICAL-DRAFT.md](BRIEF-04-WARM-PRACTICAL-DRAFT.md). |
| **5 — sleep supplement** | [neutral non-efficacy placeholder](brief-05-supplement-neutral-placeholder.png) | A plain blank bottle on a neutral studio ground; no bedroom or explicit efficacy text/imagery. **TEST-PASS for the neutral non-efficacy proxy only.** This is not the requested efficacy treatment, not the real bottle, and does not clear the claim review. |
| **6 — Japan localization** | [setting proxy](brief-06-japan-context-proxy.png) | Product/copy composition remains, with a quiet wood-toned café setting. It reads as a generic café rather than an unmistakably Japan-specific market setting. **REVISE / native review still required.** The package is a placeholder, not the approved Brief 3 product. |

**Motion status:** no video tool was available in this run. B1 animation, B2 motion, and all other motion work remain **NOT_RUN**; a still frame cannot validate timing, continuity, accessibility, or motion behavior.

## Prompt language and CRAFT ledger

The catalog's prompt-language contract says each loaded move contributes its `promptLanguage` **verbatim** (`templates/SHOT_CARD.md`, “CRAFT MOVES”). The two exact strings are:

- `MOVE-COMP-03` — “subject placed left of centre; frame weight falls right into reserved copy space”
- `MOVE-CONCEPT-04` — “pick one system and obey it ruthlessly - one grid, one shape, one repeat”

The v2 probes for Briefs 2, 3 and the warm-practical Brief 4 direction include both exact strings. The first probe versions paraphrased the composition string; they are retained as initial attempts, not counted as verbatim CRAFT tests. The Brief 4 product-only first probe, Brief 5 neutral bottle, and Brief 6 setting probe also did **not** include the exact CRAFT strings; their visuals are useful only as provisional proxies, not as tests of those move phrases. The cap stopped a corrected rerun of Brief 4 product-only; no further generation was attempted.

| Brief | Loaded move(s), type and salience | Considered but not loaded for this reconstruction | `DECLARED-QUIET` for unloaded families |
|---|---|---|---|
| **1** | None. No catalog move fit the Mode B mascot without rewriting its verbatim language. | `MOVE-COMP-03` / `MOVE-CONCEPT-04` were rejected: catalog applicability is A/C, not B. | LIGHT—neutral even sheet light; MOMENT—static pose studies; COMPOSITION—flat, non-overlapping reference panels; PALETTE—flat orange/teal, no grade; TEXTURE—no visible wear; CAMERA—neutral reference views; CONCEPT—literal turnaround, no metaphor. |
| **2** | `MOVE-COMP-03` ORGANIZER, medium; `MOVE-CONCEPT-04` ORGANIZER, medium. **2 records total**; the latter also affects CONCEPT. Exact strings in v2. | `MOVE-COMP-05` contour clearance was not needed for the simple abstract card silhouette; `MOVE-PAL-01` was not loaded because no approved palette was supplied (teal/mint here is a probe choice). | LIGHT—flat vector, no light shaping; MOMENT—static frame; PALETTE—provisional teal/mint, no grade; TEXTURE—flat vector; CAMERA—straight-on. COMPOSITION and CONCEPT are loaded. |
| **3** | `MOVE-COMP-03` ORGANIZER, medium; `MOVE-CONCEPT-04` ORGANIZER, medium. **2 records total**. Exact strings in v2. | `MOVE-TEXTURE-01` material truth was not loaded because the real pouch specification/reference was unavailable; `MOVE-CAMERA-02` proof-plane focus would add an unnecessary second focal plane. | LIGHT—one soft side-window source, no extra shaping move; MOMENT—still hero; PALETTE—natural kraft/neutral, no grade; TEXTURE—no added wear; CAMERA—level product view. COMPOSITION and CONCEPT are loaded. |
| **4** | Carries the same two medium ORGANIZERS from Brief 3; no new move loaded while the direction is unresolved. Only the warm-practical v2 contains the exact strings. | `MOVE-TEXTURE-02` human traces was considered for the lived-in option but not loaded as a CRAFT move while the client direction is undecided. | LIGHT—single soft/warm source; MOMENT—static still; PALETTE—natural warm tone, no grade; TEXTURE—clean placeholder pouch; CAMERA—locked product view. COMPOSITION and CONCEPT are loaded. |
| **5** | `MOVE-COMP-03` ORGANIZER, medium, in the earlier plan; **one move only**, below the catalog's stated two-move floor. No unsuitable move was forced in. The generated neutral proxy did not include the exact phrase, so it does not test this move. | `MOVE-CONCEPT-03` demonstrate-don't-claim was rejected: a comparison panel could imply unsupported efficacy. | LIGHT—soft neutral daylight; MOMENT—static product; PALETTE—neutral white/grey, no grade; TEXTURE—no visible wear; CAMERA—level packshot; CONCEPT—no device. COMPOSITION is loaded in the plan. |
| **6** | Carries the same two medium ORGANIZERS as Brief 3. The initial setting proxy did not include the exact move strings, so it is not a verbatim move test. | `MOVE-PAL-01` two-colour commitment was not loaded because no approved local palette was supplied; `MOVE-TEXTURE-01` was not loaded without the actual pouch reference/specification. | LIGHT—diffuse daylight; MOMENT—static hero; PALETTE—natural wood/neutral, no grade; TEXTURE—clean surfaces; CAMERA—eye-level/locked. COMPOSITION and CONCEPT are loaded in the plan. |

### Cap and five-law screen

The catalog states feed **2+1**, poster **3+1**, editorial/key-art **4+1**, and video **at most 3 active per beat / 4 across a clip**; it also says the concept is not a free fifth slot (`dev/CRAFT_MOVES.json`, `capRules`). Destination is not preserved for every brief, so the ledger above stays at 0–2 records and uses 2+1 as the conservative still ceiling where applicable. This is a **manual screen**, not automated per-brief enforcement. The package's `templates/SHOT_CARD.md` example says `COUNT: 4 loaded + 1 concept`, then `ORGANIZERS: 3` and `ACTIVATORS: 2`; the reconciliation is ambiguous. R801 calls caps “salience-weighted,” but the cap definitions provide no weighting formula. The catalog validator's prior 325 checks passing does not resolve that documentation/runtime gap or prove output quality.

Five laws (`dev/CRAFT_MOVES.json`):

- `oneLightSetup` — one coherent physical light setup; simple single-source looks pass, no extra CRAFT light move was loaded.
- `oneWithholding` — do not stack hidden-information devices; none was needed in these still probes.
- `oneMystery` — keep the main read to one step; cat/model sheet, token, pouch, and bottle remain simple subjects.
- `attentionPointsCoincide` — Brief 2 needs repair because the grid competes with the token; Brief 3's bean row should not cross the copy reserve; Brief 4 warm option's cup/beans compete with the copy zone. Other simple product frames keep the hero as the main attention point.
- `candidVsDesigned` — not applicable: these are designed commercial/reference frames, not UGC or reportage.

The shot card is intent, not proof: `33B_scene_conception_and_shot_card.md` says “The card produces **intent**, never **proof**.” Its craft choices are not scored here.

## Engine guidance: strengths and thin areas

The still-image manual orders a prompt as: “Output purpose → subject → reference roles → state/action → environment → composition → mode-specific craft → critical constraints → canvas/aspect → post-production reservations” (`rules/detailed/04_image_prompt_manual.md`). Mode C says exact copy/data belongs in an editable handoff and that generated text is exploratory; the controller calls for one-variable repair and keeps still/video owners distinct. The CRAFT catalog pairs prompt wording with visible effect and risk, and the shot card requires explicit quiet declarations rather than silently inheriting defaults.

| Brief | Guidance strength | Thin area exposed by this probe |
|---|---|---|
| **1** | Mode B explicitly calls for character-part/proportion, silhouette, palette, expression and recurrence continuity. | A text-only model sheet did not prevent the wave study from being cropped; there is no approved character reference to lock against. Still-image inspection cannot test the six-second motion prompt. |
| **2** | Mode C separates message hierarchy, exact-copy ownership, readability holds, and reduced-motion planning. | A text-free frame cannot validate the FDIC wording or its three-second readability; the visible grid/UI bars remain too dominant. |
| **3** | Mode A names geometry, label, material, contact, lens and claim fidelity; the prompt plan also protects copy space. | Without the actual bag reference/specifications in this test context, the output is only a composition probe; v2 also violates its no-cup exclusion. |
| **4** | Client-language translation produced two concrete, reviewable art-direction branches rather than vague adjectives. | No final branch was approved; the warm branch's prop/bean row competes with copy space, and the two images are not a controlled same-reference comparison. |
| **5** | Safety/claim priority blocks an unsupported efficacy implication and preserves a neutral route. | A blank generic bottle cannot stand in for approved packaging or substantiate the requested benefit; this run tested only absence of explicit efficacy cues. |
| **6** | The localization plan preserves the hero/copy composition and explicitly avoids tourist shorthand. | The output remains visually generic; no native reviewer or approved bag reference was available, so local authenticity is untested. |

**Thin areas / system caveats:** no per-brief CRAFT runtime selector was found in the prior audit; the catalog and validator do not prove selection is correct. The cap example/reconciliation and “salience-weighted” rule are ambiguous. CRAFT is inspiration-sourced; the catalog labels evidence as review-pending and says moves make no quality promise. Current prompt blocks were reconstructed, not replayed verbatim. The available image tool is model-unidentified; no external generator facts were verified. A single generated still cannot establish prompt reliability, product fidelity, comprehension, motion, or campaign quality.

## Next gates

1. **Brief 4:** warm practical/lived-in trace is selected. Use the proxy edit draft only for a visual test; bind the approved coffee package reference/specification before issuing the final client prompt. Keep the cup and bean repeat clear of the copy-safe area.
2. **Brief 2:** keep the final card blocked until the FDIC line has substantiation, a responsible owner, qualification and approval; add exact copy as an editable layer and run a real readability hold test.
3. **Brief 5:** keep the requested efficacy treatment blocked pending evidence/review, or approve a neutral non-efficacy route; supply the actual bottle reference for product fidelity.
4. **Briefs 3 and 6:** provide the actual coffee-bag reference/specifications. Brief 6 additionally needs native-market cultural review.
5. **Motion:** test only after an authorized, model-identified video-generation route and approved still anchors are available.

## Output hashes

| File | Dimensions | SHA-256 |
|---|---:|---|
| `brief-01-cat-model-sheet.png` | 1376×768 | `e99f1d9cc99b2f78d1049eccd7f7fa0090807862ed3b44d72dd3bdc6208a4a95` |
| `brief-02-fintech-style-frame.png` | 1376×768 | `6206c05b6fb534361a34d9ccf19a1916786e2bd1407da331cecc96a9f11cfc2e` |
| `brief-02-fintech-style-frame-v2.png` | 1376×768 | `bdb33af75824ba316e6b3c53fae4d36f9a9801bb0c973708baad4327057021fc` |
| `brief-03-coffee-hero-proxy.png` | 1376×768 | `a4acda432cdee85dc71c73d1c8da71945e4615ab068ad284035f6df9cec8d71d` |
| `brief-03-coffee-hero-proxy-v2.png` | 1376×768 | `2bf87f5fee0b236457197a0215d635aaa3d7982ec5cf2d27fa89d333f42685c5` |
| `brief-04-warm-practical-direction.png` | 1376×768 | `56c2a9c8887bf66f5e399bbed15f67ed25dd6e58e98969497b4d95575789ccf5` |
| `brief-04-warm-practical-direction-v2.png` | 1376×768 | `28c8c03aeadafa7f79bd8f3c7ec104c331848e407f59ceaf9a6be99775a84122` |
| `brief-04-product-only-warm-direction.png` | 1376×768 | `37d3da6049f9b2b08d51f60cfd53190daf6d70d47b1d5beeb47563ff522f5320` |
| `brief-05-supplement-neutral-placeholder.png` | 928×1152 | `d4c030603dcaf32ec1771a802ee1b6e592d5b04ae2786740c9d247929697e267` |
| `brief-06-japan-context-proxy.png` | 1376×768 | `4aad40220ada22909335ec62e0e0f08cb89ba1bc4d2c0ea49bebb4a80ed3e3b5` |
