# Creative density test — rendered head-to-head, Round 2

**Status:** six one-shot images generated and inspected; qualitative verdict complete. No rerolls or numerical scores.

## Headline findings

- **Prompt text:** raw coffee copy is the most creatively alive. The merged Arm 3 is the best client-ready foundation after two small prompt-integrity fixes recorded below.
- **Rendered images:** Arm 3 is my narrow coffee-hero pick; skill Arm 2 is my sparse-mug pick.
- **Round 1 delta:** no clear visual improvement from the described new pipeline in this one-sample comparison; the Round 2 skill coffee frame is busier in the copy area.
- **Sparse control:** respected; the skill mug render adds no story or prop.

## Source and test integrity

- **Skill target checked:** `origin/main` exposes the 8.7.0 / Release 16 cumulative archive, SHA-256 `4790157ee898f46e81612fcc339ffd3a06e53d5707d2be6b3d1125098d23d17d`. No updated skill attachment or newer skill file containing the three described fixes was present in the workspace/repository at test time.
- **Important qualification:** I operationalized the user's descriptions as the Round 2 rules: invention is permitted in the surrounding fiction zone but not the product/claim facts; paste prose should be connected rather than field-form; sensory cues need visible physical carriers and a stated display-size boundary. This is a behavior probe of those descriptions, **not** a source-exact execution/audit of a newer attached implementation. The previously reported 5/5 prompt-text retest is user-supplied context, not independently re-run evidence.
- **Same budget:** six prompts total (three arms × two briefs), one text-to-image call per prompt, one attempt each, no options, no iterative repair; same Arena image-generation tool path. The tool does not expose its model/version, so this is not a Nano Banana Pro validation.
- **Blindness:** outputs use opaque IDs and will be inspected in shuffled order before the ID-to-arm key is revealed. I authored the prompts and saw the generation calls, so this is semi-blind at most—not a truly blind test.
- **No numerical score:** the AVD shot card explicitly says it is intent, not proof, and must never be scored. Verdicts below are qualitative observations only.

## Shared facts, arms, and image prompts

### Brief 1 — coffee website hero

**Shared brief facts:** premium coffee brand; matte black kraft bag; copper zip at top; no other markings; 250 g; 12 cm wide × 20 cm high; copper is the brand color; 16:9 website hero. No claims, origin, roast, certification, logo or label text were supplied. The surrounding setting is creative latitude; product and claim facts are not. Each arm was written against this shared fact ledger, though a minor wording asymmetry discovered after generation is documented under “Prompt-fidelity note.”

#### Arm 1 — raw chat, free-form prompt

> Before the roastery door is unlocked, the room still belongs to the dark: a 250 g coffee bag, exactly 12 cm wide and 20 cm high, matte black kraft with a copper zip at the top, stands on a scarred oak tasting bench. The package is utterly unmarked; copper appears only in the zip, with no logo, label or claims. First light from a low window grazes the bag so the paper stays dry and matte, one ember of copper glint at the zip. Beside it, one used espresso cup has a dark crescent at its lip and leaves a fading ring; a few grounds from the first pull sit where they fell—not sprinkled for decoration. The bag holds left of frame; its long shadow carries the image into a broad dark copy field at right. The room is pre-opening, still cool beyond the beam, someone just gone. Tactile, intimate, premium without showroom staging. 16:9 website hero. No hands, second package, added markings, text, origin, roast, certification, claims or fog.

#### Arm 2 — updated skill behavior, connected prose

> Keep the product as fact and invent only the surrounding fiction: one entirely unmarked 250 g matte-black kraft bag, 12 cm wide and 20 cm high, with a copper zip at the top; copper is the brand color, and the zip is its only visible copper mark. No logo, label, origin, roast, certification or claim is authorized. Imagine the roastery just before opening, after one first tasting: a single used espresso cup leaves a faint ring, and a few grounds rest where they fell. Place the bag left of frame; subject placed left of centre; frame weight falls right into reserved copy space. A single low window camera-left, hard falloff to true black frame-right. Let grazing light show the dry paper tooth without glossing it, and let one narrow highlight carry the copper zip. At normal website-hero viewing size, the bag silhouette and copper line must read first; fiber grain, ring and grounds are secondary traces, never micro-details the image depends on. Keep the right copy field clear; no person, second bag, props, extra markings, text or claim. 16:9 landscape.

#### Arm 3 — my client prompt (merge)

> Create a 16:9 website hero in the breath before a roastery opens. Keep the product exact and unmarked: one 250 g, 12 cm wide × 20 cm high matte-black kraft bag with a copper zip at the top; the zipper is the only copper mark, and no logo, label, origin, roast, certification or claim may appear. On a scarred oak tasting bench, one recently used espresso cup and a few fallen grounds hint that the first cup has just been tasted; no person is visible. Let one low window from camera-left skim the kraft so its dry surface reads matte, catch the zipper with a single copper hairline, and let the shadow open a clean dark copy field at right. Place the bag left of frame, keep the cup quiet and out of the headline area; at normal hero size the silhouette and zip read immediately while paper grain and cup ring remain subtle. Lived-in, hushed, tactile—not staged luxury. No extra prop, second package, markings, text, or claim.

### Brief 2 — sparse mug control

**Locked input facts for all three arms:** one white ceramic mug; plain background; 4:5 portrait for print; nothing else in frame. Shape beyond a simple mug is not specified; no logo or decoration is authorized.

#### Arm 1 — raw chat, free-form prompt

> A single unmarked white ceramic mug, centered and alone against a plain pale-grey studio sweep, vertical 4:5 for print. Let its rim make one clean oval and the handle leave a readable open shape; a broad soft source gives it one quiet highlight and a feathered contact shadow. Empty air, exact form, no drama. Nothing else in frame: no coffee, steam, ring, coaster, surface edge, plant, text, mark or second object.

#### Arm 2 — updated skill behavior, connected prose

> Respect the sparse studio intent: one unmarked white ceramic mug, alone against a plain pale neutral-gray background, 4:5 portrait for print. The fiction zone is intentionally empty—do not add a story, stain, ring, steam, coaster, table edge, texture prop or lettering. Use one soft, broad studio source and only a faint contact shadow to separate the base; at print viewing size the rim and handle opening should stay legible, while glaze detail stays quiet and does not turn into visual noise. Keep the mug simple, centered and the only object in frame.

#### Arm 3 — my client prompt (merge)

> One simple, unmarked white ceramic mug centered alone on a plain pale-gray seamless background, 4:5 portrait for print. Use broad diffuse light, a soft contact shadow, a clean rim ellipse and a readable handle opening; preserve ample plain background and let no decorative detail compete. No coffee, steam, stains, ring, coaster, tabletop edge, texture prop, logo, text or other object.

## Skill-mode pipeline record

### Routing and project contract

- **Delivery mode:** `SINGLE_PASS_BLUEPRINT`; two still-image briefs, three text-prompt arms each, no motion.
- **Modes:** Mode A photoreal/commercial for both.
- **Still owner in the skill plan:** `NANO_BANANA_PRO`; the actual Arena image tool is a separate, model-unidentified probe.
- **Coffee asset:** `COFFEE-HERO-R2`, version `0.2-test`; fact locks as stated above; fiction permitted only in setting/moment; no visual package reference. Acceptance: dimensions/weight/material/zip/unmarked state represented; copper zip and silhouette read at hero size; right copy reserve usable; no invented product/claim facts. Failure: changed package fact, added mark, claim, or clutter in the copy reserve. Fallback: one-variable repair only.
- **Mug asset:** `MUG-CONTROL-R2`, version `0.2-test`; one unmarked white ceramic mug only, plain background, 4:5. Acceptance: mug alone, handle/rim legible at print size, background plain. Failure: added trace/object/text or object lost against ground. Fiction zone is empty because sparse studio is the intent.
- **Reference strategy:** no visual references supplied for either. Text facts outrank invented design. Output resolution is unspecified by the briefs; no native pixel-size promise is made.

### Conception: coffee (STANDARD card)

- **GOAL:** sell a premium coffee product on a site hero; a buyer should notice the bag's black kraft/copper contrast and feel a specific pre-opening coffee ritual. Client approval, not audience preference, is the success authority; no audience test is run.
- **FACT vs latitude:** all product facts remain locked; roastery setting, first-light window, tasting cup/ring/grounds are fiction in the scene only. They do not assert origin, roast, quality, or certification.
- **MOMENT:** first tasting is over, the person has stepped away, the door is not yet open. The bag remains closed and unmarked. The quiet aftermath gives the static hero a time inside it.
- **ELEMENTS/defaults rejected:** left-side bag/right-side copy field instead of centered packshot; one low window instead of flat fill; matte kraft shown by grazing light rather than gloss; one used cup instead of generic lifestyle clutter; no label copy instead of invented branding; no extra coffee objects.

### CRAFT ledger: coffee

- **Loaded:** `MOVE-LIGHT-01` motivated source — ORGANIZER, medium, exact language “single low window camera-left, hard falloff to true black frame-right”; `MOVE-COMP-03` weight placement — ORGANIZER, medium, exact language “subject placed left of centre; frame weight falls right into reserved copy space”. Two loaded organizers, no activators, no concept move. Destination key art cap 4+1; two moves used. The cap is a manual check, not automated per-brief enforcement.
- **Considered, not loaded:** `MOVE-CONCEPT-04` (one grid/shape/repeat) would make a bean pattern arbitrary decoration; `MOVE-TEXTURE-02` uses literal flour/kneading language and its catalog record flags new-product/food-hygiene; `MOVE-TEXTURE-01` includes irrelevant translucency/gloss directions. The human trace is authored in the fiction zone, not falsely credited to those moves.
- **Five laws:** oneLightSetup—one window; oneWithholding—no hidden-info stack; oneMystery—bag reads immediately; attentionPointsCoincide—zip and bag face share the focal path; candidVsDesigned—designed key art, not reportage.
- **`DECLARED-QUIET`:** MOMENT—one static aftermath, no extra action; PALETTE—black/copper/oak, no grade; TEXTURE—matte kraft only, no added product wear; CAMERA—fixed near-counter view; CONCEPT—literal coffee ritual, no metaphor. LIGHT and COMPOSITION are loaded.

### CRAFT ledger: sparse mug

- **Loaded:** none. No exact-language move fit without adding a copy layout, extra object, or decorative device. This intentionally stays below the catalog's stated two-move floor rather than force an unsuitable move into a brief whose central intent is absence.
- **Considered, not loaded:** `MOVE-PAL-02` monochrome discipline adds no visible decision beyond the supplied white mug/plain ground; `MOVE-COMP-03` would invent a copy reserve; `MOVE-CONCEPT-04` would invent a repeat; `MOVE-COMP-02` would add an imperfection to a clean studio object.
- **Five laws:** oneLightSetup—one diffuse source; oneWithholding—none; oneMystery—single obvious mug; attentionPointsCoincide—rim/handle/object stay together as one read; candidVsDesigned—designed studio shot, not UGC.
- **`DECLARED-QUIET` (all families):** LIGHT—one soft source, no shaping effect; MOMENT—static; COMPOSITION—centered single object; PALETTE—white mug/pale neutral ground, no grade; TEXTURE—clean glaze, no added wear; CAMERA—fixed; CONCEPT—literal studio product shot, no fiction.

### Rules applied

- Mode A: “Hero frame first, shot list never.”
- Conception: “idea → design → look” and “Facts carry the image, not vocabulary.”
- Image manual: “Output purpose → subject → reference roles → state/action → environment → composition → mode-specific craft → critical constraints → canvas/aspect → post-production reservations.”
- Updated behavior as described by the user: factual product zone separated from fiction zone; prose compilation in the skill paste block; sensory carrier and resolution boundary named in skill prompts. The exact updated source file was not available to inspect.

## Blind review and reveal

**Review method:** the six renders were opened in shuffled order under opaque IDs: `blind-q8`, `blind-a6`, `blind-m1`, `blind-c9`, `blind-z4`, `blind-f2`. Notes below are keyed by image ID and limited to visible output traits; the arm key is shown afterward. This is only semi-blind: I wrote the prompts and saw the generation calls, so arm identity was not truly hidden from me. No scores were assigned.

### ID-keyed visual notes

- **`blind-q8`** — One white mug on a smooth warm-gray field. Rim and handle opening read clearly; broad light and a soft grounded shadow. No extra object or decorative treatment.
- **`blind-a6`** — Matte dark bag left of frame with a copper top zip; one cup and fallen grounds/ring on a window-lit oak bench. The right side is broadly dark and copy-capable, though the bench grain and the cup/ring remain visible near its left edge. The package stays distinct.
- **`blind-m1`** — One white mug against a cool, very pale studio field. Rim and handle are readable and nothing else enters frame. The shadow is especially faint, making the mug feel a little less grounded than the other two mug renders.
- **`blind-c9`** — Unmarked dark bag left, copper zip visible, cup and grounds on a long bench, warm side light, and a broad dark area at right. Strong hero/copy layout; the tabletop still has visible texture, but the headline area is the calmest of the coffee renders.
- **`blind-z4`** — Dark bag and copper zip read, with a cup more prominent in the foreground. Roasting machinery and sack-like forms appear in the background; they make the place legible but add unrequested visual weight and reduce the clean copy reserve.
- **`blind-f2`** — One centered white mug on a pale warm-gray field. Clear rim and handle, the most convincing contact shadow of the mug set, no added object or ornament. Provisional mug favorite for print use.

My ID-keyed visual preferences are `blind-c9` for the calmer coffee copy area, with `blind-a6` close and more atmospheric, and `blind-f2` for the mug’s shape legibility and grounding. These are subjective use-case judgments, not quality scores or truly blinded picks.

### Arm key and output manifest

| Opaque ID | Brief / arm after reveal | Render | SHA-256 |
|---|---|---:|---|
| [`blind-a6.png`](blind-a6.png) | Coffee / Arm 1 raw chat | 1376×768 (1.792:1; requested 16:9) | `9a7c47dd20bf27851da8fc663dcbfdbed7b17b78e2cc11ba06619dccf43f41ed` |
| [`blind-c9.png`](blind-c9.png) | Coffee / Arm 3 my client prompt | 1376×768 (1.792:1; requested 16:9) | `45d4674d5010a5ffc548729d32a0a79ff8f49d3660ed3fffab2067491cc84a51` |
| [`blind-z4.png`](blind-z4.png) | Coffee / Arm 2 updated-skill behavior | 1376×768 (1.792:1; requested 16:9) | `1e425f83dfe05ac7054a32d40c97fd04bfb0fb602072f8b0c62441ce11871b68` |
| [`blind-m1.png`](blind-m1.png) | Mug / Arm 1 raw chat | 928×1152 (0.806:1; requested 4:5) | `e8ba6a2e3df57db0fcc0ced896a55115340f91e0354c786ca7cba4e9dec413dc` |
| [`blind-f2.png`](blind-f2.png) | Mug / Arm 2 updated-skill behavior | 928×1152 (0.806:1; requested 4:5) | `fed7d4a895c52d2eb7b3a999585219131cd37ada986d9cc8a79838f626a5d76f` |
| [`blind-q8.png`](blind-q8.png) | Mug / Arm 3 my client prompt | 928×1152 (0.806:1; requested 4:5) | `72d6eaabef9c468b13a5d2bfbf38f34667fee1f345345788b691557f7e0c9992` |

Each prompt received exactly one Arena image-generation call with `offer_options:false`; there were no rerolls, options, edits, or post-generation repairs. All six used the same tool path. The actual tool model/version is not exposed. The returned rasters are close to, but not exact matches for, the requested aspect ratios; no crops were made. Dimensions/weight and true package construction cannot be verified from generated pixels without an approved product reference.

### Prompt-fidelity note (found after generation)

- The shared brief names copper as the brand color. Coffee Arms 1 and 3 constrain copper visually to the zipper but omit the literal “copper is the brand color” phrase; Arm 2 includes it. This is a wording asymmetry, not a change to the requested appearance, but the production prompt should restore the explicit fact.
- Coffee Arm 2 asks for a used cup and grounds, then says “no … props,” which contradicts that request. The intended wording was “no additional props.” Do not silently treat the rendered output as evidence about that contradictory instruction; correct it before client use.

### Answers to the five comparisons

1. **Strongest prompt text / safest client prompt.** The raw coffee prompt (Arm 1) is the most creatively alive: the pre-opening time, cup trace, and grounds “where they fell” have clear causes rather than generic premium adjectives. The best client-ready foundation is Arm 3, my compact merge: it carries that lived-in moment while giving clear product exclusions, left-side hero, right copy reserve, and normal-view legibility without shot-card process language. It is **not quite safe to send unchanged**: add the explicit fact “copper is the brand color” and attach an approved package reference. Arm 2 has the strongest explicit fact-versus-fiction and size/readability boundary, but correct its contradictory “no … props” to “no additional props” before reuse. Prompt preference is not image preference.

2. **Most usable rendered images.** `blind-c9` (Arm 3) is my narrow coffee-hero pick: the bag reads on the left and the dark right reserve is the calmest of the three. `blind-a6` (raw) is a close alternative with a stronger sense of atmosphere, but its ring/grounds and table grain compete a little more near the copy boundary. `blind-z4` (skill) has a compelling roastery setting, but the machinery and sack-like background shapes make it the least copy-safe. For the sparse mug, `blind-f2` (skill) is the most usable print image: clean single object, legible opening/handle, and a better contact shadow; `blind-q8` is close. This is a single-render preference, not evidence that either prompt mode is generally better.

3. **Did the described new pipeline visibly improve on Round 1?** No clear improvement is visible in this pair. Round 1’s selected skill image, [`skill-mode-selected.png`](../creative-density-test/skill-mode-selected.png) (2048×1152; SHA-256 `7834393a629b61384d20a81b5e76a2d7bea7f7a1955ff957f46c96dd2a951e69`), has a larger, more isolated package and cleaner dark copy field. Round 2 skill output `blind-z4` adds a more legible roastery, but also machinery/sack-like shapes and a more prominent cup, making the right side busier. The new prose/sensory rules may improve prompt formulation, but one generated sample per arm, an unidentified tool model, and a different prompt make this an uncontrolled visual comparison—not proof that the pipeline regressed or failed.

4. **Sparse control: over-decorated or respected?** Respected. `blind-f2` contains only the white mug and a plain pale background; its soft contact shadow and light gradient support legibility rather than adding a story or prop. The raw and my-choice mug outputs also stay sparse. The zero-move CRAFT decision was appropriate: forcing a decorative move would have contradicted the brief.

5. **Commercial recommendation.** Use the merged Arm 3 as the starting brief, explicitly restore “copper is the brand color,” carry over Arm 2’s fact/fiction boundary, and supply an approved image of the real package as the controlling reference. If borrowing Arm 2 language, change “no props” to “no additional props.” Generate only a hero concept; verify the bag geometry, materials, zipper, and crop against the actual SKU. Keep the copy reserve free of machinery and extra sacks, add approved logo/legal copy in post, and crop/export to the exact destination ratio. Treat these renders as comps—not approved product photography or proof of package accuracy. The skill’s useful value here is the decision/acceptance discipline, not a guarantee that one render will be better.

### Limits

Six one-shot images cannot establish general superiority, an audience preference, or causal effect from any one of the described pipeline changes. I authored the prompt arms, the generator model/version is undisclosed, no controlled reference image was used, and no formal user/client evaluation was run. The earlier Round 1 selected image was itself part of a confounded comparison; the side-by-side delta above is a practical visual check only. The shot card and CRAFT ledger are process records, not scores.
