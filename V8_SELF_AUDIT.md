# V8.0.0 SELF-AUDIT — 23 model outputs vs. the built tree

Auditor stance: adversarial. Assumption: the build contains mistakes; the goal is to find them.
Rules enforced: verbatim quote (≤25 words) from BOTH source and build with file paths; no praise
vocabulary; UNVERIFIED where evidence is absent; MISSING = defect; **no fixes in this run**.

Build under audit: `D:\New folder (2)\v800-build` (v8.0.0 Release 7, 307 manifest files).
Corpus (corrected): `D:\New folder (2)\audit-inputs\` — 23 .txt files. Pre-fix evidence preserved
in `D:\New folder (2)\audit-inputs-archive\` (originals + composite chunk + manifests + sweep
report + SPLIT_RECORD.json; split verified byte-exact by concatenation).

---

## PART 0 — CORPUS INTEGRITY (Finding 0, now fully adjudicated)

### 0.1 The defect

`New folder\prompt 2 outputs.txt` (9289 lines) contains **five** model documents; its second header
is mistyped:

> Source: `New folder\prompt 2 outputs.txt` L215 — `moddl 2 output`

The original splitter keyed on `model \d`; `moddl 2` did not match, so chunk `p2_m1.txt` (1807
lines) fused **two complete outputs**: model 1 (L1–214) and model 2 (L215–1807). The build's
analysis therefore ran on 22 chunks covering 23 outputs. Prompt-2 model 2 was never read, never
adjudicated, never documented as rejected.

### 0.2 Full header inventory (fuzzy sweep, typo-tolerant; `audit-inputs-archive\SWEEP_REPORT.txt`)

| Source file | Total lines | Model spans | Count |
|---|---|---|---|
| `prompt 1.txt` | 5808 | m1 L3–1084 · m2 L1085–4255 · m3 L4256–5185 · m4 L5186–5808 | 4 |
| `prompt 2 outputs.txt` | 9289 | m1 L1–214 · **m2 L215–1807 (header `moddl 2 output`)** · m3 L1808–4283 · m4 L4284–7401 (header `model 4 oputput`) · m5 L7402–9289 | 5 |
| `prompt 3 output.txt` | 4209 | m1 L1–1635 · m2 L1636–1642 (7-line degenerate loop) · m3 L1643–3512 · m4 L3513–4209 | 4 |
| `prompt 4 outputs.txt` | 6765 | m1 L1–1207 · m2 L1208–3208 · m3 L3209–5746 · m4 L5747–6352 · m5 L6353–6765 | 5 |
| `prompt 5 outputs.txt` | 7824 | m1 L1–286 · m2 L287–2241 · m3 L2242–3936 · m4 L3937–6843 · m5 L6844–7824 | 5 |

Sweep verdicts: (a) every chunk starts with a real header (22/22 first lines are genuine model
headers; BOM-only regex noise excluded by inspection); (b) exactly ONE fused chunk existed
(p2_m1, interior header L215); (c) line sums: p2/p3/p4/p5 exact (0 delta); p1 sums 5806 vs 5808
— the missing 2 lines are the file preamble note above `model 1` (L1–2: "this prompt only had 4
outputs means it only reached to 3 models"), not model content. **No other fusion defects.**

### 0.3 The fix (approved Option 1)

Archived first: `prompt-2-outputs.original.txt`, `p2_m1.composite.txt` (both SHA-256-verified
identical to their sources), `PRE_FIX_MANIFEST.txt`, `SOURCE_MANIFEST.txt`. Then byte-exact
binary split at composite line 215 → new `audit-inputs\p2_m1.txt` (214 lines) +
`audit-inputs\p2_m2.txt` (1593 lines, first line the verbatim mistyped header as evidence).
Reconstruction check: `p2_m1 + p2_m2 == composite` byte-for-byte (`SPLIT_RECORD.json`). Total
corpus now exactly 23 files.

### 0.4 ERRATUM (recorded openly; history not rewritten)

The v8.0.0 closing report claimed "all 22 model outputs analyzed." That claim is now known
inaccurate: it was **22 chunks covering 23 outputs**; the 23rd (prompt-2 model 2) was fused into
the m1 chunk and never analyzed. The same error propagated into `New folder\V8_SYNTHESIS.md` L3
("Basis: 22 model outputs (5 prompts × 4-5 models)"). V8_SYNTHESIS.md is analysis input, not
build output, and is outside the no-build-changes boundary for this run; its correction is
deferred to the post-audit decision round. The build tree itself makes no "22 outputs" claim in
any artifact (checked: no such string in `v800-build\release\` or `dev\` documents).

**Decision-round extension (PHASE 2/3 — audit's own evidence corrections):**

1. **D-31 transcription errors in this audit, corrected during the decision round's fresh
   re-verification:** the audit rows (and the pin's known-defects note, inherited from them)
   described the shipped AV band as "symmetric SyncNet-confidence band [3.5, 6.0] ms". The
   `[3.5, 6.0]` values are the unitless SyncNet-CONFIDENCE advisory range (catalog `units:
   "SyncNet confidence"`); the only ms-valued AV numeric in the tree was the symmetric
   correlation SEARCH window [−200, +200] ms, and no acceptance tolerance existed at all. The
   audit also transcribed m4's EBU numbers as "+60/−40ms"; m4's actual words (prompt-4 corpus
   L5835) are "EBU R37 +40/−60 ms". The defect itself (asymmetry dropped) was confirmed and
   fixed; only the evidence characterizations were wrong. Original rows stand as history; the
   corrected evidence lives in the PHASE 2 D-31 entry.
2. **The pin's `knownDefectsAtPin` D-31 entry carries the same "ms" slip** (as-shipped record,
   left as-is by the no-rewrite doctrine; this erratum is the correction of record).

**Decision-round V8_SYNTHESIS.md correction (deferred item, now executed):** V8_SYNTHESIS.md
L3's "22 model outputs" basis line is corrected this round — the PHASE 1 appendix and this
erratum are the record; the m2 chunk-fusion (23rd output) was analyzed and credited in the
PHASE 1 appendix (9 convergent ideas + rejected ideas with reasons), closing the analysis gap
the original count error opened.

---

## PART I — PER-OUTPUT AUDIT (23 sections)

## Section 1 — Output p1_m1 (`prompt 1.txt` L3–1084)

Source: "Extension design over v7.8.0 Release 6. No file is replaced. Every schema below is
additive." (L5–6).

| # | Idea (source anchor, `prompt 1.txt`) | Class | Build evidence |
|---|---|---|---|
| 1 | Optional `productionStateLayer` binding in `schemas/PROJECT_CONTRACT.schema.json` (L50) | **MISSING** | Contract schemas byte-identical to `merged-v780` baseline (SHA-256 equal); only pointer entries exist: "composed-by-pointer; this schema is neither superseded nor duplicated" — `v800-build\schemas\PRODUCTION_STATE.schema.json` L37 |
| 2 | `stateArtifacts` index array in `PROJECT_INDEX.schema.json` (L117–150) | **MISSING** | No `stateArtifacts` key under `schemas/` (grep 0 hits) |
| 3 | `stateHandoffBinding` in `ROUTING_CONTRACT.schema.json` — machine-checkable rule-38 reset (L165–198) | **MISSING** | ROUTING_CONTRACT.schema.json unchanged; reset remains prose in rule 38 |
| 4 | Capability-claim expiry policy `maxClaimAgeDays`/`onStaleClaim` (L184–193) | **MISSING** | Only `verifyAtRuntime` const exists — `schemas\artifacts\_avd_defs.schema.json` L71 |
| 5 | Six artifact catalog entries in `validators/artifact_schemas.json` (L210–262) | **MISSING** | Catalog keys still `['STYLE_BIBLE','STORYBOARD','ASSET_REGISTRY','VOICE_PLAN','ANIMATION_PROMPTS','ASSEMBLY_PLAN']` (verified read) |
| 6 | `x-stateLayer` root sibling in catalog (L268–278) | **MISSING** | No such key; file untouched |
| 7 | Semantic rules S-01…S-14 in `artifact_semantic_schemas.json` (L288–394) | **MISSING** | File still keyed by 4 shipped classes (verified read) |
| 8 | S-03 live-evidence-for-PASS: "verdict == 'PASS' AND requiresLiveEvidence == true ⇒ ∃ evidence[i].proofClass == 'OBSERVED_LIVE'" (L308) | **HYBRIDIZED (weakened)** | Const form only: "written by exactly one code path — the five live-evidence tracks" — `schemas\artifacts\GATE_RECEIPT.schema.json` L107 |
| 9 | S-06 cross-artifact model-switch reset (L328–335) | **ADOPTED (weakened)** | Single-record check: `executionProfileAfter == "CONTROLLED"` — `validators\validate_state_serialization.py` L149 |
| 10 | S-10 cross-artifact edit-budget aggregation "per clipId across ALL artifacts: sum ≤ 3" (L360–361) | **MISSING** | Per-record caps only: `chainDepth > 3 or repairsUsed > 2` — `validate_state_serialization.py` L117 |
| 11 | Bundler emits `schemas/dist/*.bundle.schema.json` (L424, 593) | **MISSING** | `schemas/dist` does not exist (glob verified) |
| 12 | JCS (RFC 8785) canonical digest form (L27) | **HYBRIDIZED (hollow)** | `canonicalization: { "const": "JCS-1" }` — `_avd_defs.schema.json` L29; but no JCS function exists anywhere (grep `def jcs` = 0). The label claims a canonicalization the tree cannot perform. D-14b |
| 13 | Version classify CURRENT/STALE/FUTURE/MISSING with v7/v8 floors (L451–527) | **HYBRIDIZED (weakened)** | Line-2 equality sweep only: `STATE_STALE_LABEL` — `validate_state_serialization.py` L308–314 |
| 14 | Placeholder-digest rejection incl. all-zero/all-f (L441, 541–554) | **MISSING (defect)** | Regex accepts all-zero hex as computed: `SHA256.match(...)` — `validate_state_serialization.py` L82. D-9 |
| 15 | R-IDs R651+ (L1075–1083) | **ADOPTED (renumbered)** | Rows R651–R688 — `dev\REGRESSION_TESTS.md` |
| 16 | AVD:STATE marker grammar w/ class/canon/digestAlgo attributes (L810–826) | **ADOPTED (drift)** | Narrower regex `id= schema= version= artifact= path= sha256=` — `validate_state_serialization.py` L42–45; class/canon attrs dropped |
| 17 | Rule 35 §4.5–§4.8 dual-output receipts prose (L792–855) | **MISSING** | Rule 35 has no §4.5; heading map verified L90–114 |
| 18 | Rule 19 `avd-vocab` machine vocabulary mirror (L864–877) | **MISSING** | grep `avd-vocab` in rule 19 = 0 |
| 19 | `templates/PROJECT_ASSET_REGISTRY.md` AVD:STATE batch tail (L929–964) | **MISSING** | grep `AVD:STATE` in template = 0 |
| 20 | `runtime_load_manifest.json` stateLayer/markerTypes/versionFloors keys (L976–1052) | **MISSING** | grep = 0; manifest untouched |
| 21 | SEMANTIC_REVIEW canary: "the canary keeps R653 alive after the real file is fixed" (L1035) | **ADOPTED** | Canary fixture `test/canary/stale_version_template.json` + suite check `v8-canary-integrity` green (suite results file) |
| 22 | Suite extension inside shipped runner (L1066–1068) | **REJECTED (weakly documented)** | Separate runner `dev/run_v800_release7_tests.py`; rationale (subprocess blocked in sandbox) recorded in session, not in-tree. D-10 |

Drift check (5 most important implemented):
1. **Marker grammar (16):** source attributes `class schemaVersion schemaId markerId canon
   digestAlgo digestStatus`; build ships 6 attrs, dropping `class=` (artifact-kind
   discriminator). Silent scope cut.
2. **Canary (21):** renumbered from R653 into sweep + dedicated check; meaning preserved.
3. **S-06 (9):** source is temporal/cross-artifact ("no intervening profile promotion evidence");
   build checks one static field. Temporal clause dropped.
4. **Version floors (13):** FUTURE/MISSING/DRIFT lanes dropped; equality sweep only.
5. **Placeholder digests (14):** source bans `{0*64, f*64}`; build accepts them as computed.
   Silent weakening = D-9.

Coverage: ADOPTED 3 (one with drift) · HYBRIDIZED 3 · REJECTED 1 · MISSING 15.

---

## Section 2 — Output p1_m2 (`prompt 1.txt` L1085–4255)

Source: "Add an **authoritative embedded-JSON state layer inside the existing Markdown artifacts**."
(L1090).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | AVD:STATE fenced block is machine authority (L1093) | **ADOPTED** | "one fenced ```json block per artifact host; block must parse" — `PRODUCTION_STATE.schema.json` L73 |
| 2 | Marker carries schemaId/version/artifactId/path/SHA-256 (L1094) | **ADOPTED** | `stateMarkerHeader` required fields — `_avd_defs.schema.json` L102–108 |
| 3 | Contracts composed by $ref, "not copied into the source master schema" (L1095) | **HYBRIDIZED** | Path-consts only, no $ref linkage — `PRODUCTION_STATE.schema.json` L33–59. D-11 |
| 4 | Schemas must NOT encode 720/3/2 as const/maximum (L1102) | **REJECTED (documented override)** | `nativeVideoCeiling: {"const": "720p"}` — `_avd_defs.schema.json` L44; override text "policy, not model claims" L42; doctrine credit goes to p1_m3 |
| 5 | Semantic comparison vs ROUTING snapshot; "mismatch produces INSUFFICIENT" (L1103–1104) | **MISSING** | `capabilitySnapshot` optional free-form — `GATE_RECEIPT.schema.json` L36–39 |
| 6 | `stateSerialization` block in PROJECT_CONTRACT (L1134–1168) | **MISSING** | Schema untouched |
| 7 | `runtimeCapabilitySnapshots` in ROUTING_CONTRACT (L1306–1366) | **MISSING** | Schema untouched |
| 8 | `videoFacts` per-claim block (L1500–1544) | **MISSING** | Only artifact-level policyConstants exists |
| 9 | `urn:avd:schema:*` aliases (L1177–1181) | **MISSING** | `$id`s are repo-relative — `_avd_defs.schema.json` L3 |
| 10 | 14 S8-* semantic operators (L1645–1748) | **MISSING** | `artifact_semantic_schemas.json` untouched; fragments inlined in validators. D-13 |
| 11 | S8-OMNI-FLASH assertion enforcing numbers "without placing those numbers in a permanent schema" (L1751) | **HYBRIDIZED (inverted)** | Numbers ARE consts — `_avd_defs.schema.json` L44–48 (m3 path won; see Section 5b conflict) |
| 12 | Version-inventory errors E_VERSION_* (L1841–1849) | **HYBRIDIZED** | Single `STATE_STALE_LABEL` code |
| 13 | `sha256=COMPUTE_ON_EMIT` sentinel (L1867–1873) | **MISSING** | No sentinel mechanism |
| 14 | CLI modes `--assemble-project-state` etc. (L1889–1897) | **MISSING** | grep = 0 |
| 15 | Rule 35 §4.1–§4.6 authoritative receipt prose (L1906–1964) | **MISSING** | No §4.x additions to rule 35 §4 |
| 16 | Rule 19 "v8.0.0 video control assertion" (L1993–2021) | **MISSING** | No such section |
| 17 | Switch invalidates OBSERVED_LIVE evidence unless re-verified (L899–900 area) | **MISSING** | No invalidatedEvidence field |
| 18 | `legacySource.payloadBase64` + rawMarkdown preservation (L1958–1963) | **MISSING** | No converter exists |
| 19 | bootstrap_runtime.py emits AVD:STATE/END (L2124–2137) | **MISSING** | Untouched (grep = 0) |
| 20 | validate_instruction_compliance.py five runtime instructions (L2149–2157) | **MISSING** | Untouched (grep = 0) |
| 21 | Shared-defs resource (L2167+) | **ADOPTED (renamed)** | `_avd_defs.schema.json` "shared state-layer definitions" L4 |
| 22 | Master composer by pointer (L3217) | **ADOPTED (renamed)** | `PRODUCTION_STATE.schema.json` "Single composition root" L6 |
| 23 | Negative-test fixtures (doctrine) | **ADOPTED** | Five fixtures under `schemas\examples\negative_tests\` (glob verified) |
| 24 | `requireControlledAfterModelSwitch` (L1739–1742) | **ADOPTED** | `executionProfileAfter == "CONTROLLED"` — `validate_state_serialization.py` L149 |
| 25 | Zero-context handoff `validateSelfContainedResumeBundle` (L1731–1737) | **HYBRIDIZED (severely weakened)** | Only `producerVersion` non-empty enforced — `validate_state_serialization.py` L135. D-12 |

Drift check (5 most important):
1. **(21/22)** rename preserves roles; no weakening.
2. **(3)** composition-by-$ref reduced to path-consts; no validation linkage (D-11).
3. **(25)** five-part self-description reduced to one non-empty string (D-12).
4. **(10)** 14 operators → ~4 inlined branches, undocumented (D-13).
5. **(13)** sentinel dropped; templates carry no machine face, so problem absent — scope cut
   without documentation.

Contradiction: m2's Rule-03 stance (idea 4) is inverted by the build; documented in-tree at
`_avd_defs.schema.json` L42 but V8_SYNTHESIS never marks m2's stance REJECTED.

Coverage: ADOPTED 6 · HYBRIDIZED 4 · REJECTED 1 · MISSING 14.

---

## Section 3 — Output p1_m3 (`prompt 1.txt` L4256–5185)

Source: "Policy bounds (3 edits / 2 repairs) are hardcoded in schemas as *AVD policy*; every
*model capability* … travels as data with `surface/tier/asOf/verifyAtRuntime`" (L4262).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | Policy/capability split (L4262) | **ADOPTED** | "policy, not model claims; model capabilities travel as data with surface/tier/asOf/verifyAtRuntime" — `_avd_defs.schema.json` L5, consts L44–48 |
| 2 | `x-avd-composition` annotations; "Do NOT add `$id`" (L4274–4283) | **REJECTED (undocumented)** | Schemas untouched entirely; annotation never added; no in-tree record of the choice |
| 3 | Catalog entries w/ marker+hosts (L4290–4295) | **MISSING** | Catalog untouched |
| 4 | AVD-SEM-* semantic rules (L4303–4342) | **MISSING** | `artifact_semantic_schemas.json` untouched |
| 5 | LOCAL_REGISTRY no-retriever guard R666 (L4350–4365) | **HYBRIDIZED** | `STATE_REF_EXTERNAL` — `validate_state_serialization.py` L207–209 |
| 6 | Extractor with hash + duplicate-id checks R663/R665 (L4378–4401) | **HYBRIDIZED (weaker)** | Regex + duplicate-marker check only; no payload-hash re-verification. D-14 |
| 7 | Rule 35 §4 machine-receipt prose (L4426–4442) | **MISSING** | No §4.x additions |
| 8 | Rule 19 machine handoff/switch packets prose (L4448–4460) | **MISSING** | Only reset-exempt section added to 19 |
| 9 | `expectedSchemaVersion` single source in manifest (L4483) | **MISSING** | Manifest untouched; version hardcoded in validator. D-15 |
| 10 | verdict enum PASS/FAIL/CONDITIONAL/BLOCKED (L4554) | **REJECTED (documented)** | Shipped vocabulary kept: `["PASS","REVISE","BLOCK","NO-SHIP","N/A","PENDING"]` — `_avd_defs.schema.json` L84; "Statuses and gates match the shipped vocabulary exactly" — `GATE_RECEIPT.schema.json` L5 |
| 11 | `legacySource`/rawMarkdown preservation (L4578–4586) | **MISSING** | Absent from shipped schema |
| 12 | evidenceItem oneOf uri/hash/structured/inlineText (L4601–4611) | **HYBRIDIZED** | Flat `evidenceRef` w/ artifactSha256-or-EXAMPLE pattern — `_avd_defs.schema.json` L86–96 |
| 13 | videoState/resolutionProfile/delivered (L4613–4651) | **MISSING** | No videoState in shipped schemas |
| 14 | editLedger caps inside schema (L4653–4660) | **HYBRIDIZED (moved to validator)** | `chainDepth > 3` — `validate_state_serialization.py` L117 |
| 15 | `converters/markdown_to_state_json.py` (L5114–5137) | **MISSING** | No converters dir |
| 16 | R651–R670 regression table (L5145–5166) | **ADOPTED (renumbered)** | R651–R688 rows + suite checks |
| 17 | "Machines MUST treat the block as authoritative; the prose MUST restate it" (L4429) | **ADOPTED** | "Markdown remains the human artifact; one fenced JSON block … is the machine authority" — `PRODUCTION_STATE.schema.json` L66 |
| 18 | Handoff self-describing (L4844–4847) | **ADOPTED (weakened)** | Validator checks producerVersion only. D-12 |
| 19 | postSwitchExecutionProfile CONTROLLED (L4985) | **ADOPTED** | `executionProfileAfter` check L149 |
| 20 | Diagnostics require evidence when PASS/FAIL or scored (L5068–5073) | **ADOPTED (weakened)** | Numeric-value-only trigger: `value is not None and not evidenceRefs` — `validate_state_serialization.py` L171. D-16 |

Drift check (5 most important):
1. **(1)** substance preserved; build adds aboveCeilingPolicy handoff string. No drift.
2. **(10)** deliberate vocabulary-preservation, self-documented.
3. **(6)** R663 hash-recompute dropped → regex-only markers. D-14.
4. **(9)** hardcoded version duplicates truth across validator+manifest. D-15.
5. **(20)** status-only PASS w/o numeric value escapes the evidence requirement. D-16.

Coverage: ADOPTED 6 · HYBRIDIZED 5 · REJECTED 2 (1 undocumented) · MISSING 7.

---

## Section 4 — Output p1_m4 (`prompt 1.txt` L5186–5808)

Source: "> Prime Directive honored: nothing below replaces a shipped file. Every change is
`EXTEND`." (L5192).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | `x-avd-state` + `stateEnvelopeRef` on three schemas (L5200–5220) | **MISSING** | Schemas untouched (SHA-256 equal to baseline) |
| 2 | Catalog array entries id/path/kind/strict/offline (L5231–5236) | **MISSING** | Catalog shape unchanged |
| 3 | `EXAMPLE:` digest prefix (L5217) | **ADOPTED** | `pattern: "^(|[0-9a-f]{64}|EXAMPLE:…)$"` — `_avd_defs.schema.json` L92 |
| 4 | R03-no-stale-caps: reject schema containing `"const": 720` (L5243) | **REJECTED (documented)** | Policy consts allowed; override text at `_avd_defs.schema.json` L42 |
| 5 | Sidecar pair protocol (L5754–5759) | **REJECTED (documented)** | "Sidecar files rejected (two artifacts drift)" — `PRODUCTION_STATE.schema.json` L66 |
| 6 | `check_schema_version_line2` (L5259–5271) | **HYBRIDIZED** | `STATE_STALE_LABEL` sweep |
| 7 | `validate_sidecar_pair` (L5276–5305) | **MISSING** (consequence of 5; undocumented) | grep sidecar = 0 |
| 8 | X14 triple: promotionEligible/structuralValidationOnly/liveProof (L5321–5331) | **HYBRIDIZED** | Two of three shipped; `promotionEligibleInfluence: NONE` is a build addition — `GATE_RECEIPT.schema.json` L105–112; no liveProof anywhere |
| 9 | `videoObservation` observed-only shape (L5515) | **MISSING** | No videoObservation |
| 10 | `policyExceeded` + evidence pattern (L5350, 5516) | **HYBRIDIZED (inverted)** | Overflow is hard fail, never representable-with-evidence — `validate_state_serialization.py` L117. D-17 |
| 11 | `legacyProsePreserved`/`legacySourceVersion` (L5501–5502) | **MISSING** | Absent |
| 12 | Default converted verdict BLOCKED (L5773–5775) | **MISSING** | No converter |
| 13 | R651–R666 checks (L5781–5796) | **ADOPTED (partial)** | ~6/16 equivalents shipped as suite rows; sidecar/liveProof family dropped undocumented |
| 14 | Rule 35 §4.5 "Machine Sidecar" (L5355–5364) | **REJECTED (documented via 5)** | Embedded mode chosen — `PRODUCTION_STATE.schema.json` L66 |
| 15 | Registry sidecar columns (L5376–5383) | **MISSING** | Template untouched |
| 16 | Manifest loadOrder six entries (L5386–5394) | **MISSING** | Manifest untouched |
| 17 | liveProof:true-reject regression (L5789) | **MISSING** | No liveProof concept |
| 18 | humanReadable/humanReadableSha256 (L5397–5400) | **MISSING** | Absent |
| 19 | Asset-name regex (L5562) | **ADOPTED (adapted)** | `FILENAME` 4-underscore + `_v<N>_(PASS|REVISE|BLOCK|DRAFT|RETIRED)` — `validate_state_serialization.py` L46–48; vocabulary mismatch with rule 19 real names. D-18 |
| 20 | `check_r03_no_hardcoded_caps` schema scan (L5333–5340) | **HYBRIDIZED** | Analogous scan lives in `signal_authority.py` (signals, not schemas) w/ PROSE_KEYS exclusion |

Drift check (5 most important): (3) EXAMPLE: extended to allow empty string — unstated; (8)
two-of-three + additive NONE field; (10) strictness inverted (D-17); (19) neither source nor
build matches rule 19's real vocabulary (D-18); (13) 6/16 shipped, rest undocumented.

Coverage: ADOPTED 4 · HYBRIDIZED 5 · REJECTED 4 (documented) · MISSING 7.

---

## Section 5a — Output p2_m1 (`prompt 2 outputs.txt` L1–214)

Source: "The tool boundary is packet-in / asset-ref-out, never model-in-the-loop." (L8).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | Packet-in/asset-ref-out boundary (L8) | **ADOPTED** | "PROMPT_ONLY_CONTROLLER: this server never invokes a generation backend" — `mcp\server\MCP_SERVER_MANIFEST.json` L42 |
| 2 | Tools/Resources/Prompts separation; only ledgered packets are evidence (L9) | **ADOPTED** | Separation in manifest L23–38; X14 codes AVD-E-3001/3002 — `mcp\errors\ERROR_CODES.json` L14–15 |
| 3 | `avd-facts` block + `avd-fact-mirror` verified by check_guide_staleness.py (L10) | **HYBRIDIZED (partial)** | HARD_FACTS.json + x-avd-fact-max exist; mirror-equality verifier absent from check_guide_staleness.py. D-19 |
| 4 | verdict/assurance/proof_class axes; MANUAL ⇒ PLAN-PASS (L11) | **ADOPTED** | "assurance_cap": "PLAN-PASS" — `mcp\tools\avd_r6_generation_execute.json` L257; AVD-E-3003 cap code |
| 5 | Hash-chained budget ledger recomputed (L12) | **ADOPTED** | `videoLedger.recomputed` required-true — `validate_state_serialization.py` L151 |
| 6 | Approval classes AUTONOMOUS/LEDGERED/HUMAN_APPROVAL (L13) | **ADOPTED (transformed)** | Three-class execution matrix: "AUTONOMOUS" / "HUMAN_APPROVAL" / "HUMAN_APPROVAL_ELEVATED" — `mcp\security\SECURITY_BOUNDARY.json` L11–27 |
| 7 | Cost tiers attach to §6 catalog (L14) | **ADOPTED** | `cost_tier` enum + `diagnostic_binding` to `rules/detailed/35#s6` — `mcp\schema\TOOL_CONTRACT.schema.json` L39–54 |
| 8 | 12-tool roster (L16) | **HYBRIDIZED (9 via action discriminators)** | Nine contracts — `mcp\server\MCP_SERVER_MANIFEST.json` L23–33 |
| 9 | routing `mcp` key w/ tool_gating + banned backends (L26–81) | **HYBRIDIZED (transformed)** | `v8_mcp_contract_layer` block w/ execution_mode_rules + banned backends — `routing\HOST_CAPABILITY_ROUTING.json` |
| 10 | `probe_host.probe_mcp_capabilities` (L99–130) | **MISSING** | probe_host.py untouched. D-20 |
| 11 | `select_host_profile` derives ACTIVE_TOOLSET.json (L133–168) | **MISSING** | No runtime/ACTIVE_TOOLSET.json |
| 12 | x14_checks walker incl. LOOSE_SCORE_FIELD (L187–205) | **MISSING** | No walker in compile_and_validate.py; signal-authority analog covers signals only |
| 13 | X14_UNKNOWN_METRIC vs metric_registry (L192–193) | **MISSING** | No metric_registry |
| 14 | X14_LIVE_WITHOUT_ATTESTATION (L202–204) | **MISSING** | No attestation mechanism |
| 15 | mcp_entry STRICT mode (L207–212, truncated at source) | **MISSING** | No MCP entrypoint in compile_and_validate.py |

Coverage: ADOPTED 5 · HYBRIDIZED 4 · REJECTED 0 · MISSING 6.

---

## Section 5b — Output p2_m2 (RECOVERED; `prompt 2 outputs.txt` L215–1807; `audit-inputs\p2_m2.txt`)

Source: "**I1** | **The locked models are never behind a tool.**" (L233). **This output was never
read during the build** (Finding 0). First full read: this audit.

### 5b.1 Idea classification

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | I1: locked models never behind a tool; server MUST NOT declare sampling (L233) | **HYBRIDIZED (via agon)** | "this server never invokes a generation backend" — `mcp\server\MCP_SERVER_MANIFEST.json` L42; no `forbidden_capabilities: ["sampling"]` text exists (grep mcp/ for sampling = 0) |
| 2 | I2: one result envelope, two producers, byte-identical AVD-TR/1 (L234) | **HYBRIDIZED (via agon)** | TOOL_CONTRACT meta-schema enforces one envelope — `mcp\schema\TOOL_CONTRACT.schema.json` L6; no "AVD-TR/1" transport-receipt concept |
| 3 | I3: "No numbers in contracts" — tokens + spec_binding{spec_ref, spec_digest} (L235) | **ADOPTED (via agon, uncredited)** | "RULE 03: no numeric ceiling in this contract" — `mcp\tools\avd_r6_generation_execute.json` L29; `x-avd-fact-max` bindings resolve from HARD_FACTS.json |
| 4 | I3b: `hard_facts_digest` mismatch → E_AVD_405 (L235) | **HYBRIDIZED (via agon)** | "AVD-E-1004": HASH_MISMATCH — `mcp\errors\ERROR_CODES.json` L8; no digest-pinned facts binding |
| 5 | I4: every scored object requires evidence_ref; not_proven[] on every result (L236) | **ADOPTED (via agon, uncredited)** | "every `Score` requires `method + evidence_uri + computed_by`" — agon design doc L4, enforced by R658 (agon tests 22/22) |
| 6 | I5: "`verdict: FAIL` is a success" — isError for contract violations only (L237) | **UNVERIFIED** | isError semantics not visible in read contracts; MCP annotations exist but FAIL-vs-error distinction requires deeper read — flagged for round 2 |
| 7 | 9 tools: 6 gate tools + meta + cycle + security (L239) | **ADOPTED (via agon, uncredited)** | Nine contracts L23–33 — `mcp\server\MCP_SERVER_MANIFEST.json` (exact roster match: 6 gate + validate_gate_evidence + avd_list_capabilities + avd_request_approval) |
| 8 | HardFactsBinding const-pins `slots_total 3, repair_slots_usable 2, final_slot_reserved true` IN-schema (L390–393) | **REJECTED (in favor of agon)** | Build resolves at runtime from HARD_FACTS.json instead: "Ceiling resolved at runtime from avd://facts/hard-facts" — `avd_r6_generation_execute.json` L29; agon design L9 rejects in-schema maximums |
| 8b | …but the STATE layer pins the same numbers as policy consts | **CONTRADICTS m2 / AGREES p1_m3** | `_avd_defs.schema.json` L46–48 consts — the split-brain is real and spans layers |
| 9 | `variable` exactly one name; multivariate → E_AVD_412 (L402–403) | **ADOPTED (via agon)** | "diff is schema-capped to exactly one variable" + AVD-E-4003/4004 — `avd_r6_generation_execute.json` L4 |
| 10 | EditChain ordinal closed 1..3; ordinal>3 → E_AVD_432 (L377) | **ADOPTED (via agon, renumbered)** | AVD-E-4002 EDIT_CHAIN_EXHAUSTED w/ remedy — `mcp\errors\ERROR_CODES.json` L19 |
| 11 | Above-ceiling ⇒ finishing handoff; named_vendor must be null (L345–358) | **ADOPTED (via agon)** | "above-ceiling output is an upscaled platform-neutral finishing handoff; must be flagged at R0/R1" — ERROR_CODES AVD-E-4001 hint L18; finishing_handoff schema `avd_r6_generation_execute.json` L32–40 |
| 12 | ArtifactRef provenance enum (L424) | **HYBRIDIZED (via agon)** | COLLECT registers `{uri, sha256}` — agon design L4; no explicit provenance enum |
| 13 | content[] exactly one text item mirroring structuredContent; blobs forbidden (L255–257) | **UNVERIFIED (likely adopted-via-agon)** | agon design L25: "no binary payloads anywhere (URIs+sha256 only)"; per-contract mirror not yet verified |
| 13b | structuredContent+content mirror semantics | **ADOPTED (via agon)** | Same L25 + TOOL_CONTRACT envelope discipline |
| 14 | ERROR_REGISTRY E_AVD_400–429 w/ retry classes (L1792–1804) | **ADOPTED (via agon, re-coded)** | AVD-E-1001..6002 registry w/ retry_policies — `mcp\errors\ERROR_CODES.json` L4–32; build's coding scheme is agon's (class-grouped 1xxx–6xxx), not m2's (HTTP-like 4xx) |
| 15 | Gate→validator dispatch map w/ fixed argv tails (L1774–1784) | **HYBRIDIZED (via agon)** | `wraps_validators` array per contract — `TOOL_CONTRACT.schema.json` L59; no argv-tail map shipped |
| 16 | TargetModel closed enum; violation → E_AVD_435 (L301–302) | **ADOPTED (via agon, transformed)** | `locked_models` block — `MCP_SERVER_MANIFEST.json` L39–43; violation → banned-backend grep R657 instead of a schema enum |

### 5b.2 Leak-check adjudication (did m2 content reach the build mislabeled as m1?)

Token-level provenance established this audit:
- m2's distinctive tokens — `E_AVD_`, `HardFactsBinding`, `slots_total`, `repair_slots_usable`,
  `forbidden_capabilities`, `TargetModel`, `ERROR_REGISTRY`, "9 tools" — appear **ONLY** in the
  L215–1807 span. Zero hits in m1 (L1–214), m3, m4, m5 spans (programmatic count, this audit).
- The adopted mcp/ base is agon-agent_2-e5aef16f; its `ERROR_CODES.json` is **byte-identical** to
  the build's (SHA-256 equal), and its design doc uses agon's own vocabulary (`AVD-E-`,
  `x-avd-fact-max`, `submit/collect cycle`) with **zero** m2 tokens (`E_AVD`, `forbidden_cap`,
  `slots_total` all = 0 hits in agon tree).
- Conclusion: **no leak**. The build's mcp/ layer converged with m2's design via agon, not via
  m2. The build is NOT contaminated by m2 content; it independently matches it. Misattribution
  risk is prospective, not retrospective: any future documentation crediting "m1/m3/m4/m5" for
  the 9-tool/fact-binding/envelope design would misdescribe provenance — m2 proposed the same
  architecture first among the consultation outputs and was never read.

### 5b.3 Adjudication outcomes (per approved instruction 4)

1. **Built layer substantially matches m2 but credited to others → misattribution?** YES in
   substance, NO in mechanism. The build's mcp/ matches m2's architecture (9 tools, fact-ref
   resolution, evidence-required scores, error registry with retry classes, two-phase ISSUE/
   COLLECT/VERIFY) — and m2 is nowhere credited. The mechanism is independent convergence: the
   build adopted agon's tree, which contains no m2-derived text. The prompt-2 synthesis verdicts
   are therefore **incomplete** (they evaluate 4/5 outputs), though every verdict they do contain
   is honestly grounded in what those 4 outputs say.
2. **Superior or conflicting m2 elements → defect?** THREE conflicts recorded, no changes:
   - **C-P2a (major):** m2 pins hard facts as schema consts (HardFactsBinding L390–393) with a
     digest guard; agon/build resolve at runtime. Both are Rule-03-honest, but they are
     different mechanisms; the build ALSO ships p1_m3-style consts in `_avd_defs.schema.json`
     L44–48, so the tree holds BOTH doctrines in two layers. D-8b.
   - **C-P2b (minor):** m2's tool roster is 9; m1's is 12. The synthesis credits m1's 12 covered
     "via action discriminators — m4's pattern" (m4 idea); the built 9 matches m2/agon exactly.
     The synthesis's tool-count reasoning is sound but was never tested against m2's 9-tool
     design, which is the one actually built.
   - **C-P2c (minor):** m2's error coding (HTTP-like E_AVD_4xx) vs build's class-grouped
     AVD-E-Nxxx. Build's scheme is agon's; m2's scheme arguably clearer (status-code semantics)
     but neither is wrong.
3. **Genuinely no overlap → documented with evidence?** N/A — overlap is extensive (above).

Coverage: ADOPTED 8 (all "via agon, uncredited") · HYBRIDIZED 6 · REJECTED 1 (idea 8, in favor
of agon — undocumented as a rejection of m2 specifically) · UNVERIFIED 2 (ideas 6, 13) ·
CONTRADICTION 1 (8b, cross-layer split-brain).

### 5b.4 Re-adjudication requirement (no change now)

The prompt-2 domain decision ("WINNER: m3's routing/protocol layer + m1's packet/ledger/security
model + m5/agon's file-first tool contract corpus") was made without m2. Because the built layer
matches m2's architecture more closely than m1's (9 vs 12 tools; fact-refs vs mirror markers),
the domain decision needs re-adjudication AFTER this audit, with m2 on the table. Deferred to
the decision round per instruction 6.

---

## Section 6 — Output p2_m3 (`prompt 2 outputs.txt` L1808–4283)

Source: "binding-design table (MCP 2025-03-26 + outputSchema, envelope compatibility for older
clients)" — synthesis L83–86. m3 was the P2 domain decision's routing/protocol winner. Key ideas
verified this round against the build:

| # | Idea (source anchor) | Class | Build evidence |
|---|---|---|---|
| 1 | Binding-design table: MCP protocol version + outputSchema, older-client envelope compat (m3 §binding) | **ADOPTED (transformed)** | "protocolVersion": "2026-07-28", "compatible_protocol_versions": ["2026-07-28","2025-06-18"] — `mcp\server\MCP_SERVER_MANIFEST.json` L3–4 |
| 2 | avd:// resource URIs (31 hits in m3 span) | **ADOPTED** | "avd://facts/hard-facts", "avd://prompts/omni-flash/shot-generate", "avd://worksheets/r6-generation" — `mcp\tools\avd_r6_generation_execute.json` L20, L29, L257 |
| 3 | assurance caps per distribution | **ADOPTED** | "portable-core cannot execute validators, so its assurance ceiling is PLAN-PASS" — `dev\build_distributions.py` proofBoundary (distributions output verified) |
| 4 | hard_facts block in routing | **ADOPTED (transformed)** | Facts live in `mcp/resources/HARD_FACTS.json` + routing carries execution_mode_rules; not a routing hard_facts block per se |
| 5 | approval_policy autonomous-list | **ADOPTED (transformed)** | Per-op matrix: "autonomous_ops": ["COLLECT","VERIFY"], "approval_required_ops": ["ISSUE"] — `avd_r6_generation_execute.json` L256 |
| 6 | R656 banned-backend probe test | **ADOPTED (renamed)** | "R657 greps mcp/ for banned backends on every test run" — agon design L19; suite runs validate_mcp_contracts 140/140 incl. banned-backend check |
| 7 | Most complete error/retry design | **HYBRIDIZED (agon base)** | Retry policies exist: "BOUNDED_BACKOFF_3: retry up to 3 times, backoff 1s/4s/9s" — `mcp\errors\ERROR_CODES.json` L28–32; scheme is agon's, m3's specific retry table not compared line-by-line — partial UNVERIFIED at row level |

Coverage: ADOPTED 5 · HYBRIDIZED 1 · REJECTED 0 · MISSING 0 (row-level drift unverified — deeper
m3 comparison deferred; m3's own text was only spot-read this round via synthesis anchors + leak-check).

---

## Section 7 — Output p2_m4 (`prompt 2 outputs.txt` L4284–7401)

Source: "action-discriminator gate tools (one tool per gate, ISSUE/COLLECT/LOCK/CHECK actions)"
(synthesis L87–88).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | Action-discriminator gate tools: one tool per gate, ops as enum | **ADOPTED** | `"op": { "enum": ["ISSUE", "COLLECT", "VERIFY"] }` — `mcp\tools\avd_r6_generation_execute.json` L10; agon design L7 credits the op-discriminated choice |
| 2 | ISSUE/COLLECT/LOCK/CHECK action set | **ADOPTED (renamed ops)** | ISSUE/COLLECT/VERIFY + ISSUE_ANCHOR/LOCK/DRIFT_CHECK in R4 contract; LOCK present — `mcp\security\SECURITY_BOUNDARY.json` L17 |
| 3 | claim_boundary block on every result | **ADOPTED (transformed)** | "VERIFY PASS is structural/deterministic proof … never live proof of model behavior (X14)" — `avd_r6_generation_execute.json` L4 |
| 4 | gate-tier mapping table | **ADOPTED** | `cost_tier` + `diagnostic_binding` to §6 catalog — `mcp\schema\TOOL_CONTRACT.schema.json` L39–54 |

Coverage: ADOPTED 4 · HYBRIDIZED 0 · MISSING 0 (spot-audit via synthesis anchors; full 3118-line
extraction deferred to a later round — flagged as incomplete coverage in the summary table).

---

## Section 8 — Output p2_m5 (`prompt 2 outputs.txt` L7402–9289)

Source: "file-first contract set: contract JSONs readable as worksheets under portable-core"
(synthesis L90–92).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | Contracts double as worksheets; manual fallback = reading the same file | **ADOPTED** | "portable_reference": { "worksheet": "avd://worksheets/r6-generation", "assurance_cap": "PLAN-PASS" } — `avd_r6_generation_execute.json` L257 + 7 worksheet files in `mcp\worksheets\` |
| 2 | x-avd wire rules (_meta["avd"]) | **ADOPTED (transformed)** | `_meta` with `io.avd/contract` required block — `mcp\schema\TOOL_CONTRACT.schema.json` L25–34 |
| 3 | structuredContent + content[0].text mirror | **UNVERIFIED** | Not verified in contracts read this round; flagged for round 3 |
| 4 | error schema as lint target R665 | **ADOPTED (renumbered)** | R660 in agon's table: "error registry machine-actionable + closed" — agon design L116; build suite validates registry (140/140 incl. error-code closure) |
| 5 | hard_facts.json single-source policy | **ADOPTED** | `mcp/resources/HARD_FACTS.json` + `x-avd-fact-max` bindings (verified in R6 contract) |

Coverage: ADOPTED 4 · UNVERIFIED 1 · MISSING 0 (spot-audit; full extraction deferred).

---

## Section 9 — Output p3_m1 (`prompt 3 output.txt` L1–1635)

Source: "Add a second, coarser granularity — the GATE DAG — owned by rule 35 … bind it to rule
39's STEP QUEUE by a one-way admission projection." (L11).

| # | Idea (source anchor, `prompt 3 output.txt`) | Class | Build evidence |
|---|---|---|---|
| 1 | Gate DAG owned by 35; one-way admission projection to 39 (L11) | **ADOPTED (verbatim doctrine)** | "bound to rule 39's STEP QUEUE by a one-way admission projection: the DAG produces a ready-set of OPEN gate lanes; 39 still elects exactly one ACTIVE step. OPEN is not ACTIVE." — `rules\detailed\35_gate_dag_v800.json` L6 |
| 2 | OPEN ≠ ACTIVE; 39 semantics preserved verbatim (L23) | **ADOPTED** | Same L6 + `ownership.admissionProjection` "one-way: DAG ready-set -> 39 ACTIVE election. 39 never projects back." L11 |
| 3 | ASYNC_EXTERNAL consumes no ACTIVE slot (L24) | **ADOPTED** | "laneModel": "ASYNC_EXTERNAL", "consumesActiveSlot": false — DAG L24, L27; invariant I5 L136 |
| 4 | Cohort batching reuses 39 §6 sibling predicate (L25) | **ADOPTED** | "batchPredicate": "identical dependency set {R2: PASS} — rule 39 section 6 sibling-batching default applies" — DAG L47 |
| 5 | 28/39 consolidation NOT reopened (L27) | **ADOPTED (verbatim)** | "The deferred 28/39 consolidation is NOT reopened by this file." — DAG L11 |
| 6 | Acyclicity trick: feedback as epoch-keyed scheduling directives (L29) | **ADOPTED (verbatim)** | "epochSemantics": "…scheduling directive over gate INSTANCES keyed (epoch, gateIndex)… unrolled graph is a DAG by construction" — DAG L94 |
| 7 | Finer node split R0a/R0b…R8c + JOIN nodes (L36–85 diagram) | **HYBRIDIZED (coarsened)** | Build keeps R0–R8 + only R4.JOIN + R7/R8 sub-gates; no R0a/R0b/R1a/R1b/R6a/R6b split — DAG L15–28 |
| 8 | Eight feedback edges FB1–FB8 with per-edge failure types, human-approval classes (L89–96) | **HYBRIDIZED (reduced to one)** | Only FB-R6-R4-DRIFT ships — DAG L82–96. FB2 (R6b→R5 timing), FB3/FB4 (R8a→R7b/R7c), FB5 (R3→R2 premise), FB6 (R8b→R1b taste), FB7 (R5→R4b), FB8 (R2→R1a) absent. D-23 |
| 9 | Exhausted budget ⇒ "BLOCK, reason REPAIR_BUDGET_EXHAUSTED … NEVER auto-PASS" (L98–99) | **ADOPTED** | "escalationOnExhaustion": { "action": "BLOCK" … } — DAG L93 |
| 10 | Leases: shared-asset W-locks with epoch + snapshotEpoch (L1577) | **MISSING** | No lease concept in DAG or dag_state schema; parallelGroups use queue-based coordination — DAG L98–116. D-24 |
| 11 | Reconstruction algorithm: readySetDigest compare, "mismatch ⇒ BLOCK:STATE_INTEGRITY (never resume)" (L1591–1592) | **MISSING** | dag_state carries no readySetDigest; HANDOFF dagState has node/epoch/cohort only — `schemas\artifacts\HANDOFF_PACKET.schema.json` dagState |
| 12 | Compaction rules (PASS-only nodes compact; ledgers NEVER truncated) (L1598–1605) | **MISSING** | No compaction rules in DAG or handoff schema |
| 13 | Gate state EXEMPT from rule 19 decay policy (L1609–1611) | **ADOPTED (as reset-exemption, different mechanism)** | "dag_state is reset-exempt (carry_forward_invariant) and survives the CONTROLLED reset" — DAG L143; decay≠reset — partial drift, meaning preserved at the carry-forward level |
| 14 | Three-way scheduler-agreement test (39 + DAG + verifier) retaining v7 assertions verbatim (L1616–1624) | **HYBRIDIZED (weaker)** | Suite check `next-protocol-authority-agreement` (two-way 39/00a) + separate DAG validator; no three-way single test — `dev\run_v800_release7_tests.py` |
| 15 | dagRef digest pin verified against 00a pin; "mismatch ⇒ BLOCK:DIGEST_DRIFT" (L1585) | **MISSING** | No DAG digest pin in 00a (registry row exists but no sha256 pin) — `rules\detailed\00a_router.md` v8 rows |
| 16 | naLedger frozen-once; "do NOT re-run resolveNA" (L1589–1590) | **MISSING** | No naLedger concept; N/A handled per-gate via naReason |
| 17 | Frozen flags "frozen by dominator nodes and re-deriving them is a compliance violation" (L1586–1588) | **MISSING** | No dominator/freeze concept; resolutionCeilingFlag is metadata only — DAG L15–16 |

Drift check (5 most important implemented):
1. **(1/2/3/4/5/6)** — adopted near-verbatim from m1's architecture (the synthesis's "WINNER:
m1's architecture … with agon's DAG JSON as the concrete starting artifact upgraded with m1's
epoch-keyed feedback semantics" is accurate; build quotes match m1's text nearly word-for-word
in L6/L11/L94).
2. **(7)** m1's 21-node fine split coarsened to agon's 14 nodes; the coarsening is undocumented
   (the synthesis said "upgraded with … finer node split R0a/R0b, R1a/R1b, R6a/R6b" — the build
   does NOT contain the finer split the synthesis promised). D-25.
3. **(8)** eight feedback edges reduced to one; six failure-type-specific routes (incl.
   timing-drift→R5, edit-defect→R7, client-taste→R1b) dropped without documented rejection.
4. **(13)** decay-exemption converted to reset-exemption; adjacent but not identical semantics
   (decay is time-based; reset is event-based). Documented nowhere as a substitution.
5. **(14)** three-way agreement test reduced to two separate checks; m1's "RETAINED verbatim"
   guarantee for the old two-way test holds (suite re-asserts shipped checks), but the three-way
   fusion did not land.

Contradiction: none — m1's core is the build's core.

Coverage: ADOPTED 8 · HYBRIDIZED 3 · REJECTED 0 · MISSING 6.

---

## Section 10 — Output p3_m2 (`prompt 3 output.txt` L1636–1642)

Source (entire output): "I'll start by reading the existing gate, queue, compiler, and router
files so the DAG layers on the verified v7.8.0 machinery rather than replacing it. I'll inspect
the current gate/queue/compiler/router files first so the DAG layers on the verified machinery.
I'll inspect… (repeats)" (L1639, 7-line degenerate loop).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | Degenerate repetition loop; zero extractable design content | **N/A (documented)** | Synthesis L126: "m2 (DEGENERATE) — 7-line repetition loop, no content." This is the one output where zero-adoption is correct and documented. |

Coverage: N/A 1 (legitimately). No defect.

---

## Section 11 — Output p3_m3 (`prompt 3 output.txt` L1643–3512)

Source: "Add a **Gate Execution Plan (GEP)** above the existing Rule 39 STEP QUEUE." (L1649).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | GEP above rule 39; 35 computes eligible gate frontiers; 39 stays sole scheduler (L1649–1657) | **ADOPTED (as the DAG's frontier concept)** | "the DAG produces a ready-set of OPEN gate lanes" — DAG L6; 39 ownership preserved L9–10 |
| 2 | Base graph acyclic; feedback compiled into later repair epochs, "never inserted as same-epoch back-edges" (L1655–1656) | **ADOPTED (via m1 formalism)** | epochSemantics — DAG L94 |
| 3 | Gate-lifecycle ACTIVE concurrent while 39 keeps one active step/batch (L1657) | **ADOPTED** | cohort + parallelGroups — DAG L46–117 |
| 4 | Gate PASS "remains artifact- and approval-based. Confidence never substitutes for a receipt." (L1658) | **ADOPTED** | "Gate PASS still requires the required artifact — never confidence (35 §7)" — `rules\detailed\35_reliability_gate_controller.md` L155 |
| 5 | Provisional R5 audio-start: "may overlap R4 … cannot PASS … frozen immediately if R3 or R4 becomes REVISE, BLOCK, or NO-SHIP" (L1692–1705) | **ADOPTED (weakened)** | EARLY-R5-AUDIO: "stillRequiresBeforePass": ["R3","R4.JOIN"], artifactTag "provisional:true" — DAG L69–79; the freeze-on-upstream-REVISE clause is absent. D-26 |
| 6 | In-gate ALL-ENABLED-PASS join (owner sign-off + technical QA + client approval) (L1709–1715) | **ADOPTED (moved to R7/R8 sub-gates only)** | subGates + aggregation "all_sub_gates_pass" — DAG L25, L28; per-gate approval joins for R0–R6 absent (requiredApprovals exist but no in-gate three-way join) |
| 7 | client approval N/A "with a serialized reason when its production-state predicate is false" (L1717) | **ADOPTED** | naReason required when N/A — `schemas\artifacts\GATE_RECEIPT.schema.json` L18–22, L127–129 |
| 8 | §3A DAG overlay prose in rule 35 with "Agents MUST NOT implement gate-ID switch statements or locally hardcode edges" (L1737–1745) | **HYBRIDIZED (partial)** | Rule 35 §7.1 exists but does not contain the anti-hardcode clause; predicateSchema.forbiddenPatterns covers part — DAG L149–153 |
| 9 | Scoped N/A: "A scoped N/A does not make the aggregate gate N/A; the aggregate gate still requires its remaining artifacts" (L1752–1755) | **ADOPTED** | R4.JOIN "joinRule": "all upstream PASS or N/A" + SKIP rules with downstreamEffect — DAG L20, L49–67 |
| 10 | GEP instance versioning by 36 (L1652) | **HYBRIDIZED** | 36 §E.1 six checks validate the DAG; no instance-versioning concept — `rules\detailed\36_runtime_activation_compiler.md` §E.1 |

Coverage: ADOPTED 6 · HYBRIDIZED 3 · MISSING 0 · 1 weakened (D-26).

---

## Section 12 — Output p3_m4 (`prompt 3 output.txt` L3513–4209)

Source: "35 evaluates the DAG against production-state → emits a gate frontier → 39 materializes
artifact steps only for gates in the frontier" (L3522).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | Single new artifact gate_dag json; 35 sole interpreter (L3520) | **ADOPTED** | `rules\detailed\35_gate_dag_v800.json` + ownership block L7–13 |
| 2 | One-directional contract; 28/39 NEXT ownership untouched (L3524) | **ADOPTED** | admissionProjection — DAG L11 |
| 3 | "The DAG is static; only *state* is dynamic" (L3524) | **ADOPTED** | Static nodes/edges + runtime dag_state — DAG structure throughout |
| 4 | R8.TECH/R8.CLIENT parallel sub-gates with join=ALL (L3537–3539) | **ADOPTED** | R8 sub-gates — DAG L26–28 |
| 5 | FB-R6-R4 scoped: "scope=drifted assets only, max 2 iterations, final slot reserved, NEVER an R2 restart" (L3547–3549) | **ADOPTED** | FB-R6-R4-DRIFT preserveState/resetState/budget — DAG L82–96 |
| 6 | "concept_broken → NO-SHIP + human, not an edge" (L3549) | **ADOPTED** | No R2 feedback edge exists in build (matches); NO-SHIP vocabulary intact in rule 35 §1 |
| 7 | FB-R8-ORIGIN evidence_mismatch → re-activate failing ancestor, max 2 (L3551–3552) | **MISSING** | No R8 feedback edge; only FB-R6-R4-DRIFT — DAG L81–96. D-23 (shared with m1 #8) |
| 8 | Global budget "≤ 8 total feedback firings per run" (L3553) | **MISSING** | No global feedback budget; per-edge budgets only — DAG L89. D-27 |
| 9 | run_budget + predicate_whitelists blocks (L3573–3579) | **HYBRIDIZED (transformed)** | predicateSchema.allowedFields + forbiddenPatterns — DAG L146–154; no separate whitelists per predicate kind |
| 10 | hard_facts note: "System constants expressed as flags/state assertions. No model names, versions, or spec literals" (L3580–3585) | **ADOPTED** | Same doctrine in `predicateSchema.rule03Compliance` — DAG L154 + HARD_FACTS.json |
| 11 | approvals with "on_absence": "AWAITING-APPROVAL; never implicit pass" (L3601–3604) | **ADOPTED (transformed)** | requiredApprovals + DEFAULT-DENY timeoutPolicy on client lanes — DAG L24, L118–127 |
| 12 | "on_na" policies on dependencies (L3614) | **HYBRIDIZED** | SKIP rules carry downstreamEffect; edges carry no on_na — DAG L49–67 |
| 13 | emits/pass_requires artifact+flag strings per node (L3607–3610) | **MISSING** | Nodes carry artifactRequired only; no emits/pass_requires arrays — DAG L15–28 |

Coverage: ADOPTED 8 · HYBRIDIZED 3 · MISSING 3 (D-23 shared, D-27, node-requirement arrays).

---


## Section 13 — Output p4_m1 (`prompt 4 outputs.txt` L1–1207)

Source: "Ship the numeric layer as a default‑ADVISORY sidecar, not as gate authority." (L11).

| # | Idea (source anchor) | Class | Build evidence |
|---|---|---|---|
| 1 | Three authority classes A/B/C; "every perceptual signal ships as Class C in v8.0.0" (L15) | **HYBRIDIZED (partial)** | Build ships all 7 signals as one class only: "class": "C_PERCEPTUAL_ADVISORY" — `dev\QUALITY_SIGNALS_CATALOG.json` L9; Class A deterministic family (DS-01…06) absent as catalog signals; Class B promotion state absent |
| 2 | X14 symmetric: "An unsupported 9/10 is rejected — *and so is an unsupported 3/10 used to block work*" (L16) | **ADOPTED (verbatim doctrine)** | "an unsupported 9/10 is rejected, and so is an unsupported 3/10 used to force diagnostics" — `rules\detailed\35_reliability_gate_controller.md` L168 |
| 3 | Thresholds as intervals + CALIBRATION_REQUIRED, "never as scalars" (L17) | **ADOPTED (transformed)** | Every threshold row: `"status": "provisional"` + advisory_range_provisional arrays — catalog L169+ |
| 4 | Promotion criterion "AUC ≥ 0.75, n ≥ 150 … ≤5% false-block rate" (L17) | **HYBRIDIZED (weakened)** | Catalog procedures require "N>=30"/"N>=100" and "ROC at 90% recall" — L169, L232; AUC/n≥150/FPR≤5% absent. D-28 |
| 5 | `cost_tier = max(generation_tier, labor_tier)`; ladder "structurally can never auto-authorize video generation" (L18) | **ADOPTED (verbatim effect)** | short_motion_proof the only HIGH (suite `v8-tier-map-agreement` green); LOW×2→MED→BLOCK ladder — rule 35 §8 L169 |
| 6 | Diagnostics never touch delivery budgets; "promotable: false", separate ledger (L19) | **ADOPTED** | promotionEligible const false in every artifact schema; diagnostic budgets separate (DAG R4 budget block) |
| 7 | `signals.mode = ADVISORY`; ASSISTED refused while tracks NOT_RUN (L21) | **HYBRIDIZED (renamed)** | No mode knob; "gate_decision_authority": "QUALITATIVE_ONLY" — catalog L10; signal_authority REJECTs measured-while-NOT_RUN |
| 8 | Universal field contract incl. encoder_family_tag_required, known_biases[], degrade_to (L33–41) | **ADOPTED (transformed)** | limitations + confidence_method + providers per signal; no tag-required/degrade-to fields — catalog L31–152 |
| 9 | QS-01 text_source_kind INTENT; "Providers are contractually forbidden from receiving the generator prompt" (L46) | **ADOPTED (transformed, weakened)** | "Encode prompt (brief) once" — catalog L43; forbidden-prompt rule not encoded. D-29 |
| 10 | QS-02 "Class C forever for the absolute value … Only Δa against the approved reference set is admissible" (L57) | **MISSING** | aesthetic_predictor uses absolute provisional range, no Δ-vs-reference-set mode — catalog L50–64 |
| 11 | QS-03 "Two thresholds, one metric" … "Never merge the two rows" (L67) | **ADOPTED** | R2 drift band "too low (<0.10) = near-copy/stock, too high (>0.28) = drift" — catalog L179; internal rows separate |
| 12 | QS-04 must_include[] "MUST_MISS = true … a stated requirement, not a perceptual judgment" (L76) | **MISSING** | No must_include/MUST_MISS concept — catalog L84–98. D-30 |
| 13 | QS-05 asymmetric "audio-late +125ms / audio-early −45ms … a symmetric \|Δt\| threshold is a design bug" (L85) | **MISSING** | Symmetric SyncNet-confidence band [3.5, 6.0] — catalog L205. D-31 |
| 14 | QS-05 source_stage EDIT_ASSEMBLY, "never on generator output" (L86) | **ADOPTED** | R7 evaluates audio_visual_sync; R5 advisory with scratch-VO note — catalog L205, L116 |
| 15 | QS-07 `provisional_band: null` + CALIBRATION_REQUIRED_STRICT (L107) | **REJECTED (weakened to uniform, undocumented)** | temporal_coherence numeric band [0.012, 0.035] — catalog L141. D-33 |
| 16 | QS-07 harmonic aggregation "one catastrophic component cannot be averaged away" (L106) | **MISSING** | Composite is logistic — catalog L263 |
| 17 | DS-01…DS-06 deterministic signal family (L111–120) | **MISSING (as catalog signals)** | Those checks exist as shipped validators, not catalog signals. D-32 |
| 18 | LX-01/LX-02 lexical signals (L122–127) | **MISSING** | No lexical signals in catalog |
| 19 | EV-01…EV-04 meta-signals; "UNSUPPORTED_CLAIM_COUNT … must be 0 — this is X14, generalized" (L129–136) | **HYBRIDIZED** | Substance enforced by signal_authority; not as named signals |
| 20 | Per-gate roles VETO/SUPPORT/ADVISORY/NA (L146) | **HYBRIDIZED (flattened)** | All advisory; no VETO/SUPPORT column — catalog per_gate_thresholds |
| 21 | Confidence HIGH "unreachable in v8.0.0 by construction" (L216) | **ADOPTED** | Levels defined without high reachability; value=null fallback — catalog L243 |
| 22 | INDETERMINATE "may not auto-pass and may not auto-fail … Silent rounding … is a design bug" (L222) | **ADOPTED** | "confidence is low and CI straddles threshold, MUST fall back to qualitative" — catalog L245 |
| 23 | No-provider path "v7.8.0 R6 behaviour is byte-identical. This is the tested path (R688)" (L227) | **ADOPTED (renumbered)** | Graceful-degradation check green in signal_authority suite run |
| 24 | Provider `UnsupportedMetricError`, never fabricated (L237+) | **ADOPTED** | `validators\signal_provider_interface.py` + provider-parity checks green |

Drift check (5 most important):
1. **(1)** A/B/C taxonomy reduced to all-C; m1's own sentence is quoted in the build's doctrine,
   but the Class A family was not unified into the catalog. D-32.
2. **(4)** calibration bar n≥150/AUC≥0.75/FPR≤5% → N≥30/90% recall. Materially lower,
   differently anchored. D-28.
3. **(11)** drift duality preserved in substance; two rows kept separate.
4. **(15)** QS-07 strict-null → uniform band; silent weakening. D-33.
5. **(9)** INTENT-vs-prompt distinction collapsed to "(brief)". D-29.

Contradiction: m1 declares symmetric |Δt| thresholds "a design bug" (L85); the build ships one
(catalog L205). Unforced doctrine violation. D-31.

Coverage: ADOPTED 8 · HYBRIDIZED 6 · REJECTED 1 (undocumented) · MISSING 9.

---

## Section 14 — Output p4_m2 (`prompt 4 outputs.txt` L1208–3208)

Source: "No thresholds are claimed measured. `promotionEligible` stays `false`." (L1213).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | "Signals never auto-pass or auto-fail a gate" (L1219) | **ADOPTED** | "signals_decide_gates": false — catalog L11 |
| 2 | "Every video metric is defined at native 720p" (L1219) | **ADOPTED** | hard_facts blocks on video signals — catalog L115, L150 |
| 3 | Weighted geometric mean dropping missing signals (L1222) | **REJECTED (transformed, partially documented)** | Logistic composite; missing → composite null — catalog L273; null-not-zero preserves the honesty substance; method documented in catalog |
| 4 | Abstract spend units LOW=1/MED=3/HIGH=8 (L1223) | **MISSING** | No numeric BU weights. D-34 |
| 5 | D07→D08 escalation "Documented exception; no ninth diagnostic" (L1224) | **HYBRIDIZED (UNVERIFIED rows)** | Matrix holds 8 items (rule 35 §8 "a ninth is INVALID"); the specific D07→D08 exception not yet located in matrix rows — flagged |
| 6 | "Nano Banana Pro and Gemini Omni Flash cannot self-score into a receipt" (L1225) | **ADOPTED (verbatim doctrine)** | "The generator … never scores its own output" — catalog L13 |
| 7 | "Scoring upscales inflates every video metric — rejected by schema" (L1232) | **ADOPTED** | video_native_note — catalog L18 |
| 8 | "Presenting calibration bands as measured while … NOT_RUN — rejected by X14/R652" (L1233) | **ADOPTED** | binding_notice L7 + REJECT check green |
| 9 | Cut FID/IS/FVD/CLIP-R as required signals (L1236) | **ADOPTED** | None present |
| 10 | Cut "Any `status: 'MEASURED'` and any `promotionEligible: true`" (L1242) | **ADOPTED** | Forbidden-status doctrine + const false everywhere |
| 11 | Cut learned classifier / auto-fail on composite P (L1237, 1241) | **ADOPTED** | Qualitative override wins; no auto-fail — catalog L270 |
| 12 | Catalog+matrix as machine sources under rules/detailed/ (L1252–1253) | **ADOPTED (relocated)** | Shipped under `dev/`; wired via 00a registry rows |
| 13 | Idempotency: failure fingerprints, deterministic run keys, cached reruns (L3259) | **MISSING** | D-35 |
| 14 | Per-project cap 32 "BLOCK+human, not a silent skip" (L1230) | **UNVERIFIED (likely MISSING)** | Global cap not found; per-gate budgets exist. Flagged |

Coverage: ADOPTED 9 · HYBRIDIZED 2 · REJECTED 1 (partially documented) · MISSING 2 · UNVERIFIED 1.

---

## Section 15 — Output p4_m3 (`prompt 4 outputs.txt` L3209–5746)

Source: "A supplementary quality-signal layer in **calibration-only mode** … Do not activate
calibrated thresholds or gate-pass probabilities while all five live-evidence tracks remain
`NOT_RUN`." (L1217–1219).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | Calibration-only mode (L3217–3218) | **ADOPTED** | Catalog status + provisional ranges + procedures |
| 2 | "Return `null`, never an invented value" (L3220) | **ADOPTED** | "value=null … fallback='qualitative_only', never invent" — catalog L243 |
| 3 | Preserve Rule 32 ladder / Rule 31 Gate 3 / X14 (L3221) | **ADOPTED** | Rules untouched; X14 both ways |
| 4 | Extend §6 eight diagnostics w/ IDs, cost tiers, budgets, durations, escalation, cumulative accounting (L3224) | **ADOPTED (via agon matrix)** | `dev\DIAGNOSTIC_MATRIX.json` 23 edges (suite matrix check green) |
| 5 | "do not create a ninth diagnostic or a parallel catalog" (L3225) | **ADOPTED** | "a ninth is INVALID" — rule 35 §8 L167 |
| 6 | Numeric layer "never independently determines a gate" (L3227) | **ADOPTED** | authority block — catalog L8–15 |
| 7 | gate_pass_probability stays null until calibration (L3237) | **ADOPTED (as pending flag)** | "p_calibration_pending": true — catalog L267; same honesty, different encoding |
| 8 | Provider-fingerprint invalidation on drift (L3246–3247) | **HYBRIDIZED** | Freshness windows 90d/30d — catalog L247; literal fingerprint absent |
| 9 | "reliability-weighted composite … no naïve arithmetic average" (L3249–3250) | **HYBRIDIZED (deferred)** | Equal-weighted prior pre-calibration — catalog L265; reliability weighting post-calibration. Consistent with m3's own until-calibration stance |
| 10 | UNAVAILABLE with reason (L3253) | **ADOPTED** | unavailable level + fallback — catalog L243 |
| 11 | Native-output inspection; upscale handoff-only (L3256) | **ADOPTED** | hard_facts on every video row |
| 12 | Cut dashboards/provider ranking/auto-tuning/model-specific tables (L3270–3273) | **ADOPTED** | None shipped |
| 13 | Do-not-cut list (L3279–3287) | **ADOPTED (7 of 9 verified)** | Idempotency + gate-receipt feedback loop UNVERIFIED — D-35 |
| 14 | "aesthetic predictor output of 8/10 is not Rule 32 level 8" (L3324) | **ADOPTED** | aesthetic limitation "taste proxy only; never substitutes for Rule 32 ladder" — catalog L64 |
| 15 | Rule 38 as the home for signal definitions + gate table + provider + composite (L3298) | **REJECTED (relocated, undocumented)** | Build used dev/ catalog + rule 35 §8; no documented rejection of the rule-38 home. D-36 |

Coverage: ADOPTED 11 · HYBRIDIZED 3 · REJECTED 1 (undocumented) · MISSING 0 (2 sub-items UNVERIFIED).

---

## Section 16 — Output p4_m4 (`prompt 4 outputs.txt` L5747–6352)

Source: "Numbers advise; gates decide; X14 is enforced bidirectionally." (L5755).

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | Two machine sources (signal catalog + diagnostic matrix) (L5755) | **ADOPTED** | `dev\QUALITY_SIGNALS_CATALOG.json` + `dev\DIAGNOSTIC_MATRIX.json` |
| 2 | Global tier UNCALIBRATED + tier_rule (L5768–5769) | **ADOPTED (renamed)** | "CALIBRATION_PROCEDURE_NOT_EMPIRICALLY_PROVEN" — catalog L6 |
| 3 | Edit/repair DEFINITIONS strings (L5775–5778) | **ADOPTED (partial)** | Hard facts everywhere; explicit definitions live only in MCP ledger semantics. D-37 |
| 4 | on_cap_breach "4th edit or 3rd repair … BLOCK + human" (L5779) | **ADOPTED** | AVD-E-4002/4003 remedies — ERROR_CODES L19–20 |
| 5 | BU spend units LOW=1/MED=3/HIGH=8 (L5781) | **MISSING** | D-34 |
| 6 | Paraphrase ensemble "5 deterministic paraphrases" + "sd > 0.03 → borderline forbidden" (L5785–5789) | **HYBRIDIZED** | "optional prompt-template ensemble (3 templates)" — catalog L43; count differs, sd-degrade absent |
| 7 | SIG-04 MUST/SHOULD weighted checklist + two independent backends (L5820+) | **MISSING** | D-30 |
| 8 | Dual AV anchors +60/−40ms w/ EBU basis (L5832–5836) | **MISSING** | D-31 |
| 9 | NOT_MEASURED graceful degradation (L5755) | **ADOPTED** | Graceful-degradation check green |
| 10 | SIG-07 temporal specifics (L5856+) | **UNVERIFIED** | Deferred; formula family matches |
| 11 | Per-signal cost_bu (L5792+) | **MISSING** | D-34 |

Coverage: ADOPTED 5 · HYBRIDIZED 1 · MISSING 3 (shared defects) · UNVERIFIED 1.

---

## Section 17 — Output p4_m5 (`prompt 4 outputs.txt` L6353–6765)

Source: "I am Claude Fable 5.1 by Anthropic." (L6356). Compact provider-abstraction design.

| # | Idea | Class | Build evidence |
|---|---|---|---|
| 1 | "Calibration First" mandate; all numbers Calibration Targets (L6360–6361) | **ADOPTED** | Provisional ranges + procedures everywhere |
| 2 | X14 honesty guard: "return None or raise UnsupportedMetricError, never a fabricated score" (L6397–6398) | **ADOPTED** | `validators\signal_provider_interface.py` + parity checks green |
| 3 | SignalConfidence enum LOW/MED/HIGH (L6378–6381) | **ADOPTED (transformed)** | 4 levels incl. unavailable — catalog L239–243 |
| 4 | SIG-07 Resolution Ceiling "Auto-fail if native > 720p claimed (hallucination check)" (L6437) | **ADOPTED (as AVD-E-4001, not a catalog signal)** | Enforcement in MCP fact binding + validators; not a catalog signal (build's 7 are all perceptual) — different-but-consistent placement |
| 5 | Per-gate threshold table w/ Failure Action → diagnostics (L6447–6452) | **ADOPTED (via matrix)** | `dev\DIAGNOSTIC_MATRIX.json` |
| 6 | Scalar targets CLIP > 0.28 / Aesthetic > 6.5 (L6431–6432) | **HYBRIDIZED** | Build bands [0.26,0.32] / [5.2,6.8] contain m5's scalars; interval doctrine preferred per m1 |
| 7 | Signal methods take `bytes` refs (L6400–6418) | **REJECTED (URI+hash instead)** | score(artifact: {uri, type, hash}) — catalog L253; agon URI discipline. Consistent with no-blob doctrine; documented via interface shape |

Coverage: ADOPTED 4 · HYBRIDIZED 1 · REJECTED 1 (documented via interface shape) · MISSING 0.

---

## Section 18 — Output p5_m1 (`prompt 5 outputs.txt` L1–286)

Source: "Approval is an additive block on the rule 35 §4 receipt + a hash-chained ledger in rule
19 production memory." (L13).

| # | Idea (source anchor) | Class | Build evidence |
|---|---|---|---|
| 1 | D1: additive approval block on 35 §4 receipt; "No parallel approval system" (L13) | **ADOPTED** | "roleApprovals[] … Absent = single-authority mode (v7.8.0 behavior)" — `schemas\artifacts\GATE_RECEIPT.schema.json` L43 |
| 2 | D2: dimension-owned vetoes HARD/SOFT, not total ordering; "legal overruling taste" absurdity (L14) | **HYBRIDIZED (m2's typed classes won)** | 4 veto classes not 2 — `release\APPROVAL_ROLE_REGISTRY.json` L7; the no-personal-ranking spirit is preserved (no seniority ladder) |
| 3 | D3: timeouts never approve; HOLD → escalation; CONDITIONAL open conditions block R8 (L15) | **ADOPTED** | "conditions: … R8 cannot close while any condition is open" — GATE_RECEIPT L63–64; timeoutPolicy const DEFAULT-DENY L71–74 |
| 4 | D4: approvals bind to (gate, artifact sha256[]); "Survives … CONTROLLED reset" (L16) | **ADOPTED (verbatim)** | "Approvals bind to (gate, artifact sha256[]), never to sessions, models, or conversations" — ROLE_REGISTRY L5; boundArtifactSha256 minItems 1 — GATE_RECEIPT L55–59 |
| 5 | D5: schemaVersion line-2 unchanged; versionEnvelope line-3 w/ ruleVersion, producerVersion, sourceVersion, migratedBy (L17) | **ADOPTED (renamed versionMeta)** | Line-2 + `"versionMeta": { "ruleVersion"… "migratedFrom"… }` at line 3 — every template (22/23 checked programmatically; EXTERNAL_TRIAL_RECORD missing it — D-39); sourceVersion→migratedFrom rename |
| 6 | D6: declarative migration ops KEEP/ADD/RENAME/MOVE/RETIRE/COMPUTE with inverses; "No transform ever deletes" (L18) | **ADOPTED (transformed)** | `templates\MIGRATION_REGISTRY.json` L44–107: artifact_migrations w/ transforms+inverse, lossless ≡ inverse replay L100; the 6-op algebra itself replaced by per-artifact transform chains |
| 7 | D7: SEMANTIC_REVIEW repair gated by structural diff; tree-wide label check "closes the class" (L19) | **ADOPTED (transformed)** | Canary fixture + tree-wide sweep R651; repair shipped as defectProvenance with transformChain — `templates\SEMANTIC_REVIEW.json` L3–14; structural-diff gate itself superseded by m2's 4-tier ladder |
| 8 | D8: agents-first rollout; v8 migrates on read, refuses FUTURE (L20) | **ADOPTED** | hybrid_operation_rules: reading ALLOWED_WITH_AUTO_TRANSFORM, writing v780 BLOCKED — MIGRATION_REGISTRY L92–98 |
| 9 | D9: promotionEligible single writer; "promotionEligibleInfluence: 'NONE'" on approval artifacts (L21) | **ADOPTED (verbatim)** | `"promotionEligibleInfluence": {"const": "NONE"}` — GATE_RECEIPT L109–112 |
| 10 | losslessProof invariants I1–I6 + validatorRun pin (L76–80) | **MISSING** | MIGRATION_RECORD.json has no losslessProof block (read in full, 17 lines); invariant I4-round-trip only in registry prose |
| 11 | detectionReport classes incl. STALE_LABEL consumable only via knownDefects (L57–66, 130–133) | **HYBRIDIZED (ladder instead)** | 4-tier ladder + VERSION_IDENTITY_CONFLICT — MIGRATION_REGISTRY L6–37 |
| 12 | rollbackVault {path, sha256} (L81) | **MISSING** | No vault in MIGRATION_RECORD or ROLLBACK_PLAN |
| 13 | projectMigrations w/ grandfatheredGates + APPROVED_LEGACY (L82–84) | **MISSING** | No projectMigrations array; grandfathering appears only as absent-overlay validity L14 |
| 14 | UPDATE_WORKFLOW.md label-check step "the fix for defect DEF-780-001" (L98) | **MISSING** | `dev\UPDATE_WORKFLOW.md` has no V8 sections (grep = 0). D-40 |
| 15 | V8-1…V8-8 workflow sections incl. hybrid window, rollback levels, lossless proof gating release publish (L103–151) | **MISSING** | Same — UPDATE_WORKFLOW untouched. D-40 |
| 16 | baseline chain: previousBaseline pin + V8_0_0 baseline file (L54–56, 165) | **MISSING (D-7 verified unfixed)** | No `V8_0_0_*.json` baseline anywhere (glob 0 hits); RELEASE.json L30 points `baselineManifest` at the 7.6.0 file. D-41 |
| 17 | validate_upgrade_compatibility gains label/envelope/chain flags (L186–239) | **MISSING (mostly)** | `validators\validate_upgrade_compatibility.py` L53–104 keeps only baseline checks; no check_schema_version_labels, no envelope check. D-42 |
| 18 | fieldRetirements same shape as retiredPaths (L70–72, 90) | **ADOPTED (as registry retired_paths_shape)** | `retired_paths_shape` block — MIGRATION_REGISTRY L101–106 |

Drift check (5 most important implemented):
1. **(2)** HARD/SOFT → 4 typed classes. m2's design won the synthesis ("typed veto classes
   (m2 D5)" — synthesis L259) and the build; m1's dimension-ownership validator ("rejects any
   registry where two HARD roles share a dimension" L14) is absent — no two-absolute check of
   that form exists. Accepted synthesis decision, documented in the synthesis.
2. **(5)** versionEnvelope→versionMeta rename; field set otherwise preserved (migratedFrom is
   m1's sourceVersion under another name).
3. **(7)** structural-diff gate replaced by the canary + ladder; same defect-class closure
   goal, different mechanism.
4. **(4)** binding doctrine verbatim.
5. **(6)** op-algebra → per-artifact transform chains; RETIRE-with-reason-and-successor
   preserved via retired_paths_shape.

Contradiction: none. m1's spine is the build's spine.

Coverage: ADOPTED 8 · HYBRIDIZED 3 · MISSING 7 (concentrated in UPDATE_WORKFLOW/baseline-chain,
all recorded as defects D-40/D-41/D-42).

---

## Section 19 — Output p5_m2 (`prompt 5 outputs.txt` L287–2241)

Source: "do not build an approval engine … build **two registries and one ledger**" (L298).

| # | Idea (source anchor) | Class | Build evidence |
|---|---|---|---|
| 1 | D1: versionMeta at line 3 with deliberate redundancy "the cheapest possible tamper/stale detector" (L304) | **ADOPTED (partial)** | versionMeta line-3 everywhere; the redundancy check (versionMeta.schemaVersion == line-2) is NOT enforced by any validator — validate_upgrade_compatibility has no envelope check (D-42) |
| 2 | D2: 4-tier detection ladder ending in structural fingerprint; "declared ≠ inferred is a hard failure" (L305) | **ADOPTED (verbatim)** | `version_detection_ladder` 4 tiers + "declaredVersion != inferredVersion … HARD FAILURE VERSION_IDENTITY_CONFLICT" — MIGRATION_REGISTRY L6–37 |
| 3 | D3: lossCapsule (canonical pre-image + digest) for non-invertible ops (L306) | **HYBRIDIZED (as lossless-definition)** | "A migration is lossless iff inverse replay … reproduces the preMigrationSha256" — MIGRATION_REGISTRY L100; lossCapsule artifact itself absent — no per-op pre-image store |
| 4 | D4: hash-chained APPROVAL_LEDGER + rule 19 carry_forward_invariant (L307) | **ADOPTED (verbatim)** | Append-only hash chain — `templates\APPROVAL_LEDGER.json` L6–13; "reset-exempt state (carry-forward invariants)" — rule 19 L94–99 |
| 5 | D5: typed veto classes, "Two absolute vetoes → BLOCKED with **no override path**, only scope change back to R0/R1" (L308) | **ADOPTED (verbatim)** | "Two ABSOLUTE vetoes of ANY class -> BLOCK with no override path. The only exit is a scope change re-entering at R0/R1." — ROLE_REGISTRY L8 |
| 6 | D6: "Timeout defaults to DENY … There is no auto-approve code path anywhere" (L309) | **ADOPTED** | DEFAULT-DENY consts — GATE_RECEIPT L71–74, ROLE_REGISTRY L9–10 |
| 7 | Evidence-honesty firewall: approvalComplete separate from promotionEligible; "refuses any receipt where approvalComplete appears in the derivation set" (L311) | **ADOPTED** | promotionEligibleInfluence const NONE — GATE_RECEIPT L109–112 + L104–108 single-writer description |
| 8 | DEF-780-001 SEMANTIC_REVIEW repair w/ defectProvenance, priorDeclaredVersions (L344–350) | **ADOPTED (renumbered DEF-780-011)** | defectId DEF-780-011 + priorDeclaredVersions ["7.4.0"] — `templates\SEMANTIC_REVIEW.json` L8–14 |
| 9 | Receipt gains exactly three blocks versionMeta/approval/hardFacts; "7.8.0 reader … ignores the three new blocks" (L368) | **HYBRIDIZED (2 of 3)** | versionMeta + roleApprovals present; hardFacts shipped as policyConstants block (different name, same numbers) — GATE_RECEIPT L35 |
| 10 | Wave-based approvals w/ waveState, SLA deadlines, entryDigest chaining (L400–419) | **MISSING** | No wave concept in ledger or schema — APPROVAL_LEDGER entries carry no wave/sla fields |
| 11 | vetoClass on each entry incl. SUSPENDED_BY_ROLLBACK decision (L409–410) | **HYBRIDIZED** | vetoClass present — GATE_RECEIPT L51–53; decisions enum has REVERSED not SUSPENDED_BY_ROLLBACK (APPROVAL_LEDGER L9) |
| 12 | R686/R687/R696 check IDs (L311, 309) | **ADOPTED (renumbered)** | Shipped as R682–R686 — `dev\REGRESSION_TESTS.md` L790–794; m2's R696 fuzz (no-auto-approve) has no shipped equivalent |
| 13 | LEGACY approval mapping via MAP_LEGACY_APPROVER compute fn (L277–283) | **MISSING** | No legacy-approval transform; absentOverlay covers the compat case instead |

Drift check (5 most important):
1. **(2)** ladder verbatim — tier names, sources, and conflict rule match m2's text closely
   (STRUCTURAL keys even cite versionMeta/roleApprovals/promotionEligibleInfluence as the 8.0.0
   discriminators — exactly the build's own fingerprints).
2. **(5)** two-absolute rule verbatim.
3. **(8)** defect provenance adopted; defect ID renumbered (011 vs m2's 011 in EDIT 1 but m1
   used 001 — the build followed m2's "011"). Consistent.
4. **(3)** lossCapsule → lossless-definition: same honesty goal; the pre-image vault is gone,
   so lossy-op reversal has no stored pre-image to restore from. Real weakening; D-43.
5. **(10)** waves dropped entirely; single-round approval matrix instead. Silent scope cut
   (large multi-stakeholder productions lose resumability granularity). D-44.

Contradiction: none.

Coverage: ADOPTED 7 · HYBRIDIZED 4 · MISSING 3.

---

## Section 20 — Output p5_m3 (`prompt 5 outputs.txt` L2242–3936)

Source: "Treat approval as a **role-scoped, resumable overlay** on the existing Rule 35 gate
receipt" (L2254).

| # | Idea (source anchor) | Class | Build evidence |
|---|---|---|---|
| 1 | Overlay preserves v7.8.0 readers; "approvedBy remains the rollup" (L2257) | **ADOPTED** | "approvedBy: Existing single-authority rollup field, unchanged" — GATE_RECEIPT L86–89; validator enforces approvedBy when roleApprovals present — validate_state_serialization L108 |
| 2 | Fail-closed timeouts HOLD_CLOSED (L2258) | **ADOPTED** | DEFAULT-DENY everywhere |
| 3 | Dual-read/v8-write/migrate-on-read hybrid window (L2259) | **ADOPTED** | hybrid_operation_rules — MIGRATION_REGISTRY L92–98 |
| 4 | Segregated evidence classes with visibility ACLs (L2260) | **ADOPTED** | evidence_segregation_tag per role — ROLE_REGISTRY L24 etc. |
| 5 | Reset-exempt approvalState in handoff packet; "CONTROLLED reset does **not** touch approvalState" (L2263, 2279) | **ADOPTED** | resetExempt enum includes approvalState — `schemas\artifacts\HANDOFF_PACKET.schema.json` L36; rule 19 L98 |
| 6 | Tree-walk stale-nested detector, not just root-field compare (L2264) | **ADOPTED (as ladder tiers)** | 4-tier ladder reads line-2, structure, semantics, markers — MIGRATION_REGISTRY L6–32 |
| 7 | New failure codes STALE_SCHEMA_VERSION + UNDECLARED_FIELD_DROP (L2265) | **HYBRIDIZED (renamed)** | VERSION_IDENTITY_CONFLICT — MIGRATION_REGISTRY L33; UNDECLARED_FIELD_DROP absent |
| 8 | Proxy-after-expiry rejected → PENDING (L2266) | **MISSING** | No delegation/proxy mechanism in build at all |
| 9 | "promotionEligible is independent (X14)" validator hard-assert (L2267) | **ADOPTED** | R656/R683 — REGRESSION_TESTS L764, L791 |
| 10 | Cut list: no new migration file format, no second baseline-hash algorithm, no model names (L2270–2273) | **ADOPTED** | Registry reuses MIGRATION_RECORD; single SHA-256 algorithm; Rule 03 honored |
| 11 | Version triple schemaVersion+ruleVersion+producerVersion (L2254) | **ADOPTED** | versionMeta required in all 5 state schemas + templates |
| 12 | Rule 19 handoff gains approvalState, producerVersion, ruleVersion (L2279) | **ADOPTED** | HANDOFF_PACKET L9–17, L39–56 |
| 13 | Role pointers in HUMAN_REVIEW/HUMAN_EVIDENCE_* "no campaign replacement" (L2288) | **ADOPTED (via agon reference)** | Campaign files untouched; overlay additive on receipts only |
| 14 | staleRepair block w/ transformId + "permanent regression (R651)" (L2310–2315) | **ADOPTED (renamed defectProvenance)** | defectProvenance + detectedBy "R651-class" — SEMANTIC_REVIEW L8–14 |

Coverage: ADOPTED 11 · HYBRIDIZED 2 · MISSING 1 · 0 rejected.

---

## Section 21 — Output p5_m4 (`prompt 5 outputs.txt` L3937–6843)

Source: "`v8_gate_passed = legacy_gate_passed AND stakeholder_gate_approved`" (L3948).

| # | Idea (source anchor) | Class | Build evidence |
|---|---|---|---|
| 1 | Event-sourced approval_state; gate passed = legacy AND stakeholder approved (L3947–3948) | **ADOPTED (as optional overlay)** | Build makes the overlay optional (absent = valid v7.8.0 mode) — GATE_RECEIPT L43; the AND-composition applies only in matrix mode. m4's unconditional AND was softened |
| 2 | Stakeholder approval never writes promotionEligible (L3949) | **ADOPTED** | Influence NONE consts |
| 3 | versionMetadata snake_case triple w/ must-equal redundancy (L3959–3972) | **ADOPTED (as camelCase versionMeta, no must-equal check)** | versionMeta camelCase — all schemas; the schema_version==schemaVersion redundancy check absent (D-42) |
| 4 | "Markdown artifacts use YAML front matter" (L3981) | **MISSING** | No front-matter convention shipped |
| 5 | Binary artifacts use "content-addressed JSON sidecar" (L3982) | **MISSING** | No sidecar mechanism (consistent with p1_m4 sidecar rejection — but undocumented here) |
| 6 | videoPolicySnapshot object: touches_video, r0/r1 flags, edits_used, capability_snapshot_ref (L3990–4000) | **HYBRIDIZED (as policyConstants + videoLedger)** | policyConstants carries ceiling/3/2 — `_avd_defs.schema.json` L44–48; edits_used lives in videoLedger; touches_video/r0-r1-flags/capability_snapshot_ref absent. D-45 |
| 7 | "Migration never defaults either flag to true" (L4007) | **MISSING (no flags exist)** | No R0/R1 ceiling-acknowledgement flags in schemas; rule 35 §1 prose requires the acknowledgement but nothing machine-checks flag-preservation across migration |
| 8 | "edits_used and repairs_used are preserved. Unknown values remain null and block further execution" (L4008) | **ADOPTED** | videoLedger required + recomputed=true on switch — HANDOFF/MODEL_SWITCH schemas; recomputed-at-switch (not preserve) — different mechanism, same honesty outcome |
| 9 | "720p, 3, and 2 are workflow-policy constants, not model capability claims" (L4010) | **ADOPTED** | "policy, not model claims" — `_avd_defs.schema.json` L42 |
| 10 | Atomic production-memory epoch cutover "not an in-place best-effort rewrite" (L3955) | **MISSING** | No epoch cutover mechanism; hybrid rules only |
| 11 | Signed migration registry (L3954) | **HYBRIDIZED (unsigned)** | Registry carries sha256s but no signature concept — acceptable (no PKI in tree), undocumented as a cut |

Coverage: ADOPTED 5 · HYBRIDIZED 3 · MISSING 4 (D-45).

---

## Section 22 — Output p5_m5 (`prompt 5 outputs.txt` L6844–7824)

Source: "Approval state is stakeholder-bound, not agent-bound." (L6850).

| # | Idea (source anchor) | Class | Build evidence |
|---|---|---|---|
| 1 | D1: approvals are facts about stakeholders and content hashes; "the ledger continues" across switches (L6850) | **ADOPTED (verbatim spirit)** | resetExempt approvalState + "never invalidated by the reset" — rule 19 L98 |
| 2 | D2: one normative registry pinned by "matrixVersion + hash" (L6852) | **ADOPTED (partial)** | `release\APPROVAL_ROLE_REGISTRY.json` is the single registry; but receipts carry no matrixVersion+hash pin (schema has ledgerRef only) — D-46 |
| 3 | D3: hash-pointer segregation {sha256, evidenceClass, byteLength}; "never payloads" (L6853) | **ADOPTED (partial)** | evidence_segregation_tag per role + evidenceRefs with sha256 — ROLE_REGISTRY L24; byteLength absent from evidenceRef |
| 4 | D4: "an approval entry with empty `evidenceRefs` is invalid" (L6856) | **ADOPTED** | evidenceRefs minItems 1 — GATE_RECEIPT L66–69; validator L110–111 |
| 5 | D5: producerVersion REQUIRED on handoff packets (L6858) | **ADOPTED** | `"required": [..., "producerVersion", ...]` — HANDOFF_PACKET L158 |
| 6 | D6: "Lossless ≡ inverse replay reproduces `preMigrationSha256`" (L6860) | **ADOPTED (verbatim)** | lossless_definition — MIGRATION_REGISTRY L100 |
| 7 | D7: detection line-2 + expectedVersions → CURRENT/STALE/FUTURE/MISSING; "MISSING fails closed always" (L6862) | **HYBRIDIZED (ladder instead)** | 4-tier ladder + conflict rule; FUTURE/MISSING lanes not distinct classes (VERSION_IDENTITY_CONFLICT covers both) |
| 8 | D8: hybrid window "read-any, write-new, evidence-coherent" (L6864) | **ADOPTED** | hybrid_operation_rules L92–98 |
| 9 | D9: rollback replays inverses "in exact reverse record order"; "rollback appends approval_orphaned events" (L6866) | **MISSING** | Registry declares inverses but no rollback executor ships; no orphaned-approval event concept — ROLLBACK_PLAN.json has no overlay section. D-38 adjacent |
| 10 | D10: "Silence is never consent. Unmapped conflict topics fail closed" (L6868) | **ADOPTED** | DEFAULT-DENY + unmapped→NONE veto? — no: unmapped-conflict escalation absent from registry (max 10 custom roles constraint exists L111–114). Partial |
| 11 | D11: "Hard facts are schema-required, not prose" — hardFacts REQUIRED iff video-class (L6870) | **ADOPTED** | policyConstants required on every state schema incl. receipts — GATE_RECEIPT required L121 |
| 12 | D12: delegation depth 1, forward-only revocation; legal → declared counsel only (L6872) | **MISSING** | No delegation mechanism anywhere (matches m3's proxy cut). D-47 |
| 13 | E1: two-step SEMANTIC_REVIEW fix (7.4.0→7.8.0 alignment then 8.0.0) — "the honest pattern" (synthesis L263–265) | **ADOPTED (verbatim)** | transformChain: ["T-V800-SEMREV-ALIGN-7-4-0-TO-7-8-0", "T-V800-SCHEMA-VERSION-BUMP-TO-8-0-0"] — SEMANTIC_REVIEW L7 |
| 14 | E2: canonicalization "json_sorted_keys_utf8_lf" + preMigrationSha256/postMigrationSha256 (L6908–6910) | **HYBRIDIZED** | lossless_definition references preMigrationSha256 — MIGRATION_REGISTRY L100; MIGRATION_RECORD template itself carries no pre/post hash fields |
| 15 | E2 SLIP: "entire file. Replace with" for MIGRATION_RECORD (L6895) — synthesis D-5 defect | **REJECTED (correctly, per D-5)** | Shipped template = v7.8.0 original 13 keys + versionMeta appended — byte-compare vs `merged-v780\templates\MIGRATION_RECORD.json` shows all 13 keys retained |
| 16 | retirements "empty `reason` fails closed" (L6916, 6945) | **ADOPTED (already shipped)** | CANDIDATE_RETIREMENT_UNJUSTIFIED — validate_upgrade_compatibility L72–74 |

Drift check (5 most important):
1. **(13)** two-step transform chain shipped exactly as m5 designed — the synthesis credited
   "m5's E1 two-step is the honest pattern" and the build matches it entry-for-entry.
2. **(6)** lossless definition verbatim.
3. **(2)** registry exists but the pin (matrixVersion + hash into every receipt) is absent —
   a receipt cannot prove which registry version governed it. D-46.
4. **(9)** orphaned-approval rollback semantics dropped with the rollback executor; registry
   note (L89) even points to a ROLLBACK_PLAN section that does not exist — dead reference. D-38.
5. **(15)** the one prime-directive violation in the corpus was caught and converted; D-5
   honored.

Contradiction: none. m5's D5 requirement (producerVersion required on handoffs) vs the D-12
finding: the SCHEMA requires it, but the shipped validator (validate_handoff L135) checks only
non-empty — see Check B for the full D-12 analysis.

Coverage: ADOPTED 8 · HYBRIDIZED 3 · REJECTED 1 (correctly, documented in synthesis) · MISSING 3.

---

## Section 23 — Output p3_m2 addendum (no change to Section 10 verdict)

Degenerate output; legitimately N/A. No new evidence this round.

---

# PART III — WHOLE-BUILD CHECKS

## Check A — INTENT: did v8.0.0 answer the intent of the 5 original prompts?

**UNVERIFIABLE in full** — the 5 original prompt texts do not exist in the workspace (Finding 0
of the audit-prep phase; `prompt N.txt` files contain only model outputs). Proxy: the domain
titles in `V8_SYNTHESIS.md` L34/75/114/149/208, tested against what shipped.

| Domain (synthesis title) | Shipped | Intent answered? |
|---|---|---|
| P1 "STATE SERIALIZATION & SCHEMAS" | State layer: 5 artifact schemas + composer + validator + examples/negative tests | **YES** — embedded JSON state, machine authority, additive |
| P2 "MCP TOOL CONTRACTS" | 9-tool mcp/ tree, contracts/schemas/errors/security/manifest | **YES** — machine-readable tool boundary |
| P3 "GATE DAG" | 35_gate_dag_v800.json + 36 §E.1 + 19 dag_state + rule 35 §7 | **YES** — conditional parallel layer over the step queue |
| P4 "QUALITY SIGNALS & DIAGNOSTIC MATRIX" | Signal catalog + diagnostic matrix + provider interface + authority guards | **YES** — advisory numeric layer, honest about calibration |
| P5 "STAKEHOLDER APPROVAL & VERSION MIGRATION" | roleApprovals overlay + ledger + role registry + migration registry + versionMeta sweep | **PARTIAL** — approval core shipped; version-migration ENFORCEMENT (label-check in validate_upgrade_compatibility, V8_0_0 baseline, UPDATE_WORKFLOW protocol) did not. D-40/41/42 |

Literal-text risk: the build followed the synthesis's BINDING BUILD ORDER phases, and the
synthesis followed the outputs' shared architecture. Where outputs' *intent* and *literal text*
diverged, the build chose intent in at least two verified places: (a) m5's "replace entire
file" → append (D-5, correct); (b) agon's invented scores → rejected (D-3, correct). No case
found where literal text was followed against evident intent.

**Verdict: intent substantially answered for P1–P4; P5 half-answered (approval yes, migration
enforcement no).**

## Check B — IDENTITY SAFETY: kernel boundaries intact, and the truth about D-12

Kernel-boundary sweep (each verified in-tree this round):

1. **Prompt-only controller preserved**: "PROMPT_ONLY_CONTROLLER: this server never invokes a
   generation backend" — `mcp\server\MCP_SERVER_MANIFEST.json` L42; `release\RELEASE.json`
   L9 `"promptOnly": true` and L14 `"mediaExecution": "NOT_SUPPORTED"`.
2. **No media-execution claims**: suite proofBoundary — `dev\V8_0_0_SUITE_RESULTS.json` L160
   "Structural and deterministic checks only; media and human evidence remain NOT_RUN";
   LIVE_EVIDENCE_STATUS five tracks NOT_RUN; externalEvidenceClaimed false.
3. **Locked models unchanged**: stillOwner NANO_BANANA_PRO / videoOwner GEMINI_OMNI_FLASH —
   RELEASE.json L11–12; MCP manifest locked_models.
4. **Status vocabulary unchanged**: `["PASS","REVISE","BLOCK","NO-SHIP","N/A","PENDING"]` —
   `_avd_defs.schema.json` L84; matches rule 35 L96 verbatim list.
5. **Modes A–D intact**: RELEASE.json L15–19 activeModes A/B/C/D.
6. **promotionEligible single-writer**: const false in every state schema; influence NONE.
7. **One CRITICAL exception — no rule text now guards "generated/inspected" claims**: rule 19
   L96's reset-exempt rationale states approvals are "facts about stakeholders, content hashes,
   and verified version lineage" — accurate. But no v8 rule PROHIBITS a receipt/ledger entry
   from claiming media execution; only promotionEligible-influence is blocked. The identity
   kernel survives because no shipped artifact type can carry a media-execution claim
   (artifactClass enum L28 is state-artifacts only), which is structural luck, not an explicit
   guard. **No regression found; pre-existing gap noted (not a v8 defect).**

**D-12 in plain language — what was claimed vs what shipped:**

- **The claim**: p1_m2's `validateSelfContainedResumeBundle` demanded a handoff packet prove it
  can resume work with zero outside context (five-part self-description). p1_m3's version:
  "Handoff self-describing" (L4844–4847).
- **What shipped**: the SCHEMA (`HANDOFF_PACKET.schema.json`) actually requires 10 fields —
  versionMeta, marker, projectId, sessionId, producerVersion, executionProfile, resetExempt,
  policyConstants, promotionEligible(+Influence) — L152–163. The rule-19 companion text
  (L94–104) specifies the reset-exempt classes and forbids dropping them. So the SCHEMA layer
  is NOT gutted; my earlier "one non-empty string" reading graded only the validator function.
- **What the validator actually checks**: `validate_handoff` (validate_state_serialization.py
  L134–143) verifies producerVersion non-empty, executionProfile in enum, resetExempt subset of
  the 5-class enum, approvalState present when declared, policyConstants, promotionEligible
  false. It does NOT verify: marker, versionMeta content, projectId, sessionId — because
  **no JSON Schema validation exists anywhere in the tree** (grep for jsonschema/Draft202012
  across validators = 0 hits). Enforcement is 100% hand-rolled functions.
- **Information lost**: a handoff packet could omit marker/projectId/sessionId/versionMeta and
  still pass every shipped validator. The zero-context resumption guarantee (a receiving agent
  can identify WHICH project, WHICH session, WHAT version lineage it inherits) is schema-declared
  but not runtime-enforced.
- **Does it touch the media-execution kernel?** **No.** producerVersion is required AND checked;
  the fields not runtime-checked (projectId/sessionId/marker) carry identity and provenance, not
  capability claims. Nothing in the handoff path can assert a model generated or media was
  produced. The identity kernel's safety does not depend on D-12's resolution.
- **Correct severity: MINOR→MAJOR downgrade justified?** The defect is real (declared-required
  vs enforced divergence) but its blast radius is provenance continuity, not honesty. I
  reclassify D-12: CRITICAL → **MAJOR** (with this analysis recorded).

## Check C — SHADOW RISK: old-vs-new conflicts and dead references

1. **D-8b split-brain (schema consts vs runtime resolution) — recommendation required.**
   The conflict: `schemas/artifacts/_avd_defs.schema.json` L44–48 pins
   `nativeVideoCeiling: "720p" const`, `editCap: 3 const`, `repairBudget: 2 const` into every
   state artifact (p1_m3's doctrine), while `mcp/` resolves the same numbers at runtime from
   `HARD_FACTS.json` via `x-avd-fact-max` bindings (agon's doctrine, also p2_m2's). If the two
   layers ever disagree (someone updates HARD_FACTS.json without touching the schema consts),
   mcp tools and state validators will enforce different physics.
   **Recommendation: the mcp/ runtime-resolution doctrine should WIN**, and the schema consts
   should become (a) default-value templates with `x-avd-fact-*` annotations, or (b) equality-
   asserted against HARD_FACTS at validation time (the D-19 mirror check, which was specified
   by p2_m1 and never shipped — its absence is exactly what makes this a live hazard instead
   of a checked invariant). Rationale: the mcp layer is the one that bound itself to
   avd://facts/hard-facts with staleness hooks (R672); the schema layer is the one with no
   update path for those numbers. Pinning policy in the layer that can never receive an update
   creates the stale-spec-table risk Rule 03 exists to prevent. The user decides; this is the
   audit's recommendation, not a change.
2. **Dead reference (D-38)**: `MIGRATION_REGISTRY.json` L89 "the rollback path for overlay
   projects is BLOCKED (see ROLLBACK_PLAN)" — ROLLBACK_PLAN.json contains no overlay/approval/
   BLOCKED text (grep = 0). A reader following the pointer finds nothing.
3. **D-39 sweep gap**: 22/23 templates carry versionMeta; `EXTERNAL_TRIAL_RECORD.json` does not
   — the line-3 convention is incompletely applied, and since no label/envelope check ships
   (D-42), nothing detects it. Found by this audit's programmatic sweep; nothing in-tree could.
4. **artifact_schemas.json (v7.8.0 catalog)**: still keyed by the 6 shipped artifact classes
   (verified Section 1 #5); the new state-artifact layer is invisible to it. Two catalogs of
   truth now coexist — the shipped one (no state artifacts) and the schema layer's own
   manifest. Any tool reading the old catalog will not find GATE_RECEIPT etc. Shadow catalog
   risk, live.
5. **V7.8.0-era display labels**: `validate_state_serialization.py` L46–48 FILENAME regex
   embeds the gate-status vocabulary (D-18) — unchanged finding, restated as shadow risk: the
   state layer's asset-naming convention shadows rule 19's real naming convention without
   replacing it.
6. **D-7 verified UNFIXED → structural shadow**: `release\RELEASE.json` L30
   `"baselineManifest": "release/V7_6_0_RELEASE_4_BASELINE_HASHES.json"` — the v8 release
   declares the 7.6.0 historical baseline as its manifest. No V8 baseline file exists. Every
   baseline check (validate_upgrade_compatibility L53–104) therefore runs against a 7.6.0
   file-set expectation — which is why CANDIDATE_BASELINE_PATH_MISSING passes today: the
   7.6.0 file list is what the tree evolved FROM. The v8 tree's own 307-file inventory is
   pinned NOWHERE. **This is the single most dangerous shadow in the build**: any future
   comparison "against baseline" compares against the wrong era.

## Check D — ORIGINAL LEDGER re-verification (D-1…D-7)

| ID | Original claim (V8_SYNTHESIS L299–307) | Verdict | In-tree evidence |
|---|---|---|---|
| D-1 | agon-P4 replaced the five real live tracks → build restores them | **FIXED** | Five named tracks NOT_RUN — `dev\LIVE_EVIDENCE_STATUS.json` L5–9; identical list in RELEASE.json L22–27; promotionEligible false everywhere |
| D-2 | agon-P4 mis-cites Rule 38 §3 → cite CROSS_MODEL_TESTS X14 instead | **FIXED** | X14 cited in signal_authority.py L98–138, validate_mcp_contracts L119, validate_state_serialization L11; no "Rule 38 §3" citation in any signal file (grep = 0) |
| D-3 | agon-P5 SEMANTIC_REVIEW breaks line-2 + invented scores → reject | **HONORED** | Agon file has "$schema" L2 + "score": 0.98 L13 — `agon\agon-agent_1-26295442\templates\SEMANTIC_REVIEW.json`; build's SEMANTIC_REVIEW.json L2 = schemaVersion, no scores, defectProvenance instead |
| D-4 | agon trees' "edited" files are stubs → never apply as-is | **HONORED** | Agon rule files exist as stubs (17 files in agon-agent_1-26295442); build rule files byte-differ from agon; agon content appears only as design reference (registries re-authored, line-2 honored) |
| D-5 | p5_m5 E2 "replace entire file" → convert to append | **HONORED** | Shipped MIGRATION_RECORD.json = original 13 keys + versionMeta (read both; key-by-key match) |
| D-6 | p2_m1 degenerate tail → content up to degeneration only | **MISDIAGNOSIS — rewritten this audit** | The "tail" was model 2's complete document (L215–1807); see §0 and D-21/D-22 |
| D-7 | agon baseline-hash files are 2KB stubs → v8 baseline must be generated | **NOT FIXED** | No `V8_0_0_*.json` baseline exists (recursive glob = 0); RELEASE.json L30 still points at the 7.6.0 file; `dev\extract_upgrade_baseline.py` exists but was never run to produce a v8 baseline artifact |

**Score: 4 FIXED/HONORED · 1 rewritten (D-6) · 1 NOT FIXED (D-7) · 1 partially verifiable
(D-4 honored by construction: agon files never entered the tree).** The D-7 failure is the
build's oldest unexecuted commitment — promised in the synthesis's own defect ledger.

---

# PART IV — DISPOSITION TABLE (every defect, one disposition each)

Silent-weakening test applied throughout: **was the choice wrong, or right-but-undocumented?**
The calibration bar (D-28) is the designated test case, judged as provisional-vs-earned.

| ID | Sev | Disposition | Justification |
|---|---|---|---|
| D-1 | — | (verified FIXED) | No action needed; recorded as honored. |
| D-2 | — | (verified FIXED) | X14 citations correct throughout. |
| D-3 | — | (verified HONORED) | Rejection documented in synthesis; build file clean. |
| D-4 | — | (verified HONORED) | Stubs never applied; registries re-authored. |
| D-5 | — | (verified HONORED) | Append conversion done; key-diff proves it. |
| D-6 | — | rewritten | Misdiagnosis corrected this audit; root causes are D-21/D-22. |
| D-7 | CRITICAL | **FIX-NOW** | Release 7 declares the wrong-era baseline as its manifest; the v8 inventory is pinned nowhere. Breaks the tree's own lossless/rollback doctrine at its root. |
| D-8 | CRITICAL | **ACCEPT-WITH-REASON** | The convergence-via-agon path is now documented (Section 5b); no build content was mislabeled. The outstanding item is P2 re-adjudication — a decision, not a fix; user gates it. |
| D-8b | MAJOR | **FIX-NEXT** | Two live doctrines for the same numbers will diverge on first HARD_FACTS update; needs the D-19 mirror check or schema-const removal (see Check C recommendation). |
| D-9 | MAJOR | **FIX-NOW** | All-zero digest accepted as computed is an honesty hole: any artifact can claim a real measurement with a null hash. Regex cost is trivial. |
| D-10 | MINOR | **ACCEPT-WITH-REASON** | Separate runner is defensible (subprocess unavailable in the build sandbox); the missing piece was documentation — now recorded here and in D-40's spirit. |
| D-11 | MAJOR | **ACCEPT-WITH-REASON** | Pointer-composition is a real, working pattern (all paths exist-checked at validate_state_serialization L216–219); $ref linkage would add jsonschema dependence the tree deliberately lacks. Right-but-undocumented; the audit is the documentation. |
| D-12 | MAJOR (recl.) | **FIX-NEXT** | Downgraded CRITICAL→MAJOR (Check B analysis). The gap is declared-vs-enforced divergence: schema requires 10 fields, validator checks 6. Enforce marker/versionMeta/projectId/sessionId in validate_handoff. |
| D-13 | MAJOR | **FIX-NEXT** | 14 semantic operators vanished without registration or documented rejection; the inlined ~4 cover the top cases but the other 10 are untraceable decisions. Either register them as future work or write the rejection rationale. |
| D-14 | MAJOR | **FIX-NEXT** | No runtime AVD:STATE payload re-hash; markers can rot silently. Straightforward addition to validate_state_serialization. |
| D-14b | MAJOR | **FIX-NOW** | "canonicalization: JCS-1" is a label for a canonicalization that does not exist anywhere. Either implement JCS or relabel to json-sorted-keys. As shipped it is a false claim in a schema. |
| D-15 | MINOR | **ACCEPT-WITH-REASON** | Hardcoded version in one validator is duplicated truth; tolerable until D-42's label-check lands, at which point one source should win. |
| D-16 | MINOR | **FIX-NEXT** | Numeric-only evidence trigger lets a PASS-with-prose-value escape; widen the trigger to any non-null value. |
| D-17 | MINOR | **ACCEPT-WITH-REASON** | Hard-fail on overflow is the MORE honest behavior vs represent-with-evidence; the rejection of m4's pattern was correct, just never written down. |
| D-18 | MINOR | **FIX-NEXT** | Two naming vocabularies in one tree is drift debt; align FILENAME regex to rule 19's real convention or document the state-layer namespace. |
| D-19 | MAJOR | **FIX-NEXT** | Mirror-equality check was specified (p2_m1 #3) and skipped; it is also the cheapest resolution of D-8b. High-value small fix. |
| D-20 | MINOR | **ACCEPT-WITH-REASON** | probe_host/select_host_profile hooks are genuinely out of scope for a contract-first tree; the cut is defensible but was never recorded. |
| D-21 | — | (process, recorded) | Split-process defect; the corrected split + archive IS the remedy; nothing further to fix in-tree. |
| D-22 | — | (process, recorded) | Chunk-count-vs-model-count defect; erratum at §0.4 is the remedy. |
| D-23 | MAJOR | **FIX-NEXT** | One feedback edge for eight designed routes is a real design gap for drift/taste/timing failure classes; at minimum document which failure types intentionally have no route. |
| D-24 | MINOR | **ACCEPT-WITH-REASON** | Queue-based coordination is sufficient at the tree's single-writer scale; leases would add machinery for a concurrency level the tree does not have. |
| D-25 | MAJOR | **ACCEPT-WITH-REASON** | The finer node split was a synthesis PROMISE not kept — but the coarse 14-node DAG is complete and coherent; the defect is the broken promise, now documented. If the fine split matters operationally, queue as FIX-NEXT by user choice. |
| D-26 | MINOR | **FIX-NEXT** | Missing freeze-on-upstream-REVISE clause leaves provisional artifacts legally dangling; one predicate + one validator branch. |
| D-27 | MINOR | **ACCEPT-WITH-REASON** | Per-edge budgets bound the same risk as a global cap at this graph size (max possible firings is small); the global-8 is belt-and-suspenders. |
| D-28 | MAJOR | **ACCEPT-WITH-REASON** | **The designated test case.** The build's bar (N≥30/100, 90% recall) is a PROVISIONAL calibration floor, honest under the doctrine that every threshold is provisional until live evidence; m1's AUC≥0.75/n≥150/FPR≤5% is an EARNED-promotion bar. The build's choice is not wrong as a starting point — but it silently dropped the PROMOTION criterion while keeping the word "promotion" nowhere. Right-but-undocumented: the calibration procedure should state that promotion to decision authority requires m1's stricter bar. As shipped: defensible start, missing the earned-bar sentence. |
| D-29 | MINOR | **FIX-NEXT** | One sentence in the catalog's clip_score definition ("text source = board intent, never the generator prompt") closes it. |
| D-30 | MAJOR | **FIX-NEXT** | must_include checklist is the only mechanism that makes text-image alignment Class-A-honest for claims; without it the signal stays advisory-forever by construction. |
| D-31 | MAJOR | **FIX-NOW** | m1 called symmetric AV thresholds a design bug and specified +125/−45ms; m4 gave EBU-basis +60/−40. Shipping symmetric anyway is wrong (not right-undocumented): two sources independently specified the asymmetry and the build ignored both. |
| D-32 | MAJOR | **ACCEPT-WITH-REASON** | Keeping determinists OUT of the perceptual catalog preserves "all signals advisory" as a single clean doctrine; their checks live in validators. Defensible split — but the A/B/C taxonomy should have been documented as considered-and-transformed. |
| D-33 | MINOR | **ACCEPT-WITH-REASON** | Uniform bands with provisional status are more usable than strict-null; the strict-null signal could never be read at all. Right-but-undocumented. |
| D-34 | MINOR | **ACCEPT-WITH-REASON** | cost_tier enum without numeric weights avoids Rule-03-adjacent price staleness; tier RATIOS are only needed for budget math the tree does not do. |
| D-35 | MINOR | **FIX-NEXT** | Idempotency fingerprints were cut without documentation; repeated diagnostics can re-spend budget. Real gap at production scale. |
| D-36 | MINOR | **ACCEPT-WITH-REASON** | dev/ + rule 35 §8 is as good a home as rule 38; the choice is fine, the silence was the defect (now documented). |
| D-37 | MINOR | **ACCEPT-WITH-REASON** | Definitions live in MCP ledger semantics; catalog omits them. Placement is fine; note it in the catalog for one-stop reading. |
| D-38 | MAJOR | **FIX-NOW** | Dead pointer: MIGRATION_REGISTRY L89 → ROLLBACK_PLAN section that does not exist. Either write the overlay-rollback section or fix the pointer. Dead references in the honesty layer are self-undermining. |
| D-39 | MINOR | **FIX-NOW** | One template missing versionMeta breaks the line-3 convention the whole P5 layer claims as its tamper detector. Add it (template edit, additive). |
| D-40 | MAJOR | **FIX-NEXT** | UPDATE_WORKFLOW.md untouched: no label-check wiring, no V8 sections. The migration story has no operator-facing protocol; ship m1's V8-1…V8-8 skeleton or a slimmer equivalent. |
| D-41 | CRITICAL | **FIX-NOW** | Same root as D-7 (recorded there as the fix target): generate `V8_0_0_RELEASE_7_BASELINE_HASHES.json` via the existing extract_upgrade_baseline.py and repoint RELEASE.json. |
| D-42 | MAJOR | **FIX-NOW** | validate_upgrade_compatibility has NO version-label/envelope checks; the 4-tier ladder and conflict rule exist only as registry prose. A prose-only invariant in the honesty layer is a contradiction of the tree's own doctrine. Implement check_schema_version_labels + envelope check (m1's code was written — m1 §1.5 L218–239). |
| D-43 | MAJOR | **FIX-NEXT** | lossCapsule pre-image store dropped: lossy ops can declare an inverse but have nothing to restore from. Either store pre-images or mark such transforms LOSSY-forbidden. |
| D-44 | MINOR | **ACCEPT-WITH-REASON** | Waves dropped for a single-round matrix — simpler and sufficient for the tree's approval scale; the resumability granularity loss is acceptable, now documented. |
| D-45 | MINOR | **FIX-NEXT** | videoPolicySnapshot's touches_video + R0/R1 flags + capability_snapshot_ref collapsed into policyConstants+videoLedger; the R0/R1 acknowledgement flags lost their machine representation entirely. |
| D-46 | MINOR | **FIX-NEXT** | Receipts cannot prove WHICH registry version governed them (no matrixVersion+hash pin); one additive field. |
| D-47 | MINOR | **ACCEPT-WITH-REASON** | Delegation mechanism absent: no delegation exists to constrain. If depth-1 delegation is ever added, D-12's m5 constraints come with it. |

---

# PART V — SUMMARY

## 23-row coverage table

| Output | ADOPTED | HYBRID | REJ | MISS | Notes |
|---|---|---|---|---|---|
| p1_m1 | 3 | 3 | 1 | 15 | JCS label hollow; canary solid |
| p1_m2 | 6 | 4 | 1 | 14 | $ref composition hollow; handoff weakened |
| p1_m3 | 6 | 5 | 2 | 7 | policy/capability split is the spine |
| p1_m4 | 4 | 5 | 4 | 7 | sidecar rejected documented |
| p2_m1 | 5 | 4 | 0 | 6 | packet/ledger model adopted |
| p2_m2 | 8 | 6 | 1 | 2 (+2 UNVER) | RECOVERED — converged via agon, uncredited |
| p2_m3 | 5 | 1 | 0 | 0 | spot-audit; binding/routing adopted |
| p2_m4 | 4 | 0 | 0 | 0 | action discriminators adopted |
| p2_m5 | 4 | 0 | 0 | 0 (+1 UNVER) | worksheets/file-first adopted |
| p3_m1 | 8 | 3 | 0 | 6 | architecture spine; FB1–8 collapsed to 1 |
| p3_m2 | — | — | — | — | degenerate loop; N/A documented |
| p3_m3 | 6 | 3 | 0 | 0 (+1 weak) | GEP→DAG frontier; freeze clause lost |
| p3_m4 | 8 | 3 | 0 | 3 | static-DAG doctrine; R8 feedback + global budget lost |
| p4_m1 | 8 | 6 | 1 | 9 | X14 symmetric adopted; AV symmetry contradicted |
| p4_m2 | 9 | 2 | 1 | 2 (+1 UNVER) | cut-list honored; BU units lost |
| p4_m3 | 11 | 3 | 1 | 0 | calibration-only core adopted |
| p4_m4 | 5 | 1 | 0 | 3 (+1 UNVER) | hard-facts teeth adopted |
| p4_m5 | 4 | 1 | 1 | 0 | provider abstraction adopted |
| p5_m1 | 8 | 3 | 0 | 7 | decision-table spine; workflow/baseline chain lost |
| p5_m2 | 7 | 4 | 0 | 3 | ladder/two-absolute/ledger verbatim; waves lost |
| p5_m3 | 11 | 2 | 0 | 1 | overlay + reset-exemption adopted |
| p5_m4 | 5 | 3 | 0 | 4 | videoPolicySnapshot partial |
| p5_m5 | 8 | 3 | 1 | 3 | two-step fix verbatim; orphan-rollback lost |
| **Total** | **132** | **65** | **15** | **85** | +7 UNVERIFIED items (Sections 5b/7/8/14/16) |

## Severity totals

- **CRITICAL: 3** — D-7/D-41 (same root: v8 baseline never generated; wrong-era manifest), D-8
  (narrowed: misattribution prospective-only; remains CRITICAL for the unaudited-output process
  breach it records).
- **MAJOR: 22** — D-8b, D-9, D-11, D-12 (downgraded), D-13, D-14, D-14b, D-19, D-23, D-25,
  D-28, D-30, D-31, D-32, D-38, D-40, D-42, D-43 (+D-24…D-27 band by severity counted above).
- **MINOR: 17** — remainder.
- **Process/rewritten: 4** — D-6, D-21, D-22 (+D-10 documented).

## The 10 worst findings

1. **D-7/D-41**: the v8 release's `baselineManifest` points at the 7.6.0 historical baseline;
   no V8 baseline file exists anywhere. Every "baseline" comparison in the tree compares against
   the wrong era. (`RELEASE.json` L30; glob proof.)
2. **D-42**: `validate_upgrade_compatibility.py` ships NO version-label or envelope checks —
   the 4-tier detection ladder and VERSION_IDENTITY_CONFLICT exist only as prose in a JSON
   description field. m1 wrote the exact code (L218–239) and it never landed. The defect class
   the whole P5 domain exists to close (7.4.0-in-7.8.0) is open again for 8.0.0.
3. **D-8b + D-19**: two live doctrines for the same hard facts (schema consts vs runtime
   resolution) with no equality check between them. First HARD_FACTS update silently forks the
   tree's physics. The check that would close it (avd-fact-mirror) was specified by p2_m1 and
   skipped.
4. **D-14b**: `"canonicalization": "JCS-1"` is claimed in a schema and implemented nowhere. A
   false technical claim inside the honesty layer.
5. **D-9**: all-zero digests accepted as computed measurements. Any artifact can carry a null
   hash as if measured.
6. **D-31**: the AV-sync threshold is symmetric although m1 explicitly called symmetric
   thresholds "a design bug" and two outputs independently specified asymmetric tolerances.
   The only finding where the build contradicts an explicit source warning.
7. **D-38**: MIGRATION_REGISTRY L89 points to a ROLLBACK_PLAN overlay section that does not
   exist — a dead reference inside the migration-honesty machinery itself.
8. **D-23/D-25**: the DAG shipped with 1 of 8 designed feedback routes and none of the finer
   node granularity the synthesis promised ("upgraded with m1's … finer node split" — synthesis
   L280–281). The build is coherent; the synthesis record of it is not.
9. **D-12 (regraded)**: schema requires 10 handoff fields; validator checks 6; no JSON Schema
   validation exists tree-wide (grep = 0), so declared-required ≠ enforced. Provenance
   continuity, not honesty — downgraded CRITICAL→MAJOR with analysis in Check B.
10. **D-8**: prompt-2 model 2 was never read, never adjudicated, and uncredited — its
    architecture matches the shipped mcp/ layer more closely than the outputs that WERE
    adjudicated. No leak (agon convergence proven by token forensics), but the P2 domain
    decision was made on 4/5 outputs and needs re-adjudication before it is cited again.

## Erratum (repeated from §0.4)

The v8.0.0 closing report's "all 22 model outputs analyzed" was inaccurate: 22 chunks covered
23 outputs. The 23rd (prompt-2 model 2) was fused into the m1 chunk by a typo'd header and never
analyzed until this audit. V8_SYNTHESIS.md L3 carries the same error and awaits the user's
post-audit decision round.

---

## APPENDIX — FULL DEFECT LEDGER (D-1…D-47; D-1…D-7 verdicts verified in Check D)

| ID | Severity | Defect (evidence) |
|---|---|---|
| D-1 | verified FIXED | agon-P4 replaced the five real live tracks → build restores them. Five tracks NOT_RUN — `dev\LIVE_EVIDENCE_STATUS.json` L5–9. |
| D-2 | verified FIXED | agon-P4 mis-cites Rule 38 §3 → X14 cited instead throughout signal layer. |
| D-3 | verified HONORED | agon SEMANTIC_REVIEW (line-2 break + invented 0.98/0.95 scores) rejected; build file clean. |
| D-4 | verified HONORED | agon stub files never applied as-is; registries re-authored. |
| D-5 | verified HONORED | m5's "replace entire file" converted to append — key-by-key match vs `merged-v780` original. |
| D-6 | **REWRITTEN (was misdiagnosis)** | Original D-6 said "p2_m1 degenerate tail → content up to degeneration only." The "tail" was model 2's complete document (L215–1807), not degeneration. The truncation discarded a whole output. Root defects D-21/D-22 below replace it. |
| D-7 | CRITICAL — **NOT FIXED** | Synthesis: "v8 baseline must be generated from the real tree." No V8 baseline file exists; `release\RELEASE.json` L30 still points baselineManifest at the 7.6.0 file. See D-41 (same root). |
| D-8 | CRITICAL | p2_m2 never audited/decided during build; synthesis P2 verdicts made on 4/5 outputs; 8 adopted-matching ideas uncredited (Section 5b). |
| D-8b | MAJOR | Cross-layer split-brain: mcp/ resolves hard facts at runtime (agon doctrine); state schemas pin them as consts (p1_m3 doctrine). Both Rule-03-honest, mutually inconsistent mechanism; documented nowhere as a deliberate split. |
| D-9 | MAJOR | All-zero/all-f placeholder digests accepted as computed — `validate_state_serialization.py` L82. |
| D-10 | MINOR | Separate suite runner; sandbox rationale not recorded in-tree. |
| D-11 | MAJOR | PRODUCTION_STATE composition is path-consts, not $ref; no validation linkage. |
| D-12 | **MAJOR (regraded from CRITICAL — see Check B)** | Schema requires 10 handoff fields (HANDOFF_PACKET.schema.json L152–163); validator checks 6 (validate_state_serialization.py L134–143); no JSON Schema validation exists tree-wide, so declared-required ≠ enforced. |
| D-13 | MAJOR | 14 semantic operators (S-01..S-14 / S8-*) never registered nor documented as rejected. |
| D-14 | MAJOR | No runtime AVD:STATE payload-hash re-verification. |
| D-14b | MAJOR | JCS-1 label shipped with no JCS implementation anywhere — label claims unperformed canonicalization. |
| D-15 | MINOR | Version hardcoded in validator instead of manifest single source. |
| D-16 | MINOR | Diagnostic evidence requirement triggers on numeric value only. |
| D-17 | MINOR | policyExceeded-with-evidence pattern rejected outright, undocumented. |
| D-18 | MINOR | Asset-name regex uses gate-status vocabulary, not rule 19's real vocabulary. |
| D-19 | MAJOR | avd-fact-mirror equality verification absent from check_guide_staleness.py. |
| D-20 | MINOR | probe_host/select_host_profile MCP hooks absent. |
| D-21 | **NEW (split process)** | Pattern-match split with no residual-content check: interior `moddl 2 output` header survived inside a chunk; no post-split verification that chunks partition sources. |
| D-22 | **NEW (process)** | Chunk count (22) accepted as model count without header-span reconciliation; the closing-report claim "all 22 model outputs analyzed" was inaccurate (22 chunks = 23 outputs). Erratum recorded at 0.4. |
| D-23 | MAJOR | Feedback-edge richness collapsed: m1's FB1–FB8 and m4's FB-R8-ORIGIN reduced to the single FB-R6-R4-DRIFT; timing-drift→R5, edit-defect→R7, evidence-mismatch→R8, premise/taste routes dropped without documented rejection. |
| D-24 | MINOR | m1's shared-asset lease mechanism (W-locks with epoch) absent; queue-based coordination is weaker than lock-based mutual exclusion for shared-asset writes. |
| D-25 | MAJOR | Synthesis promised "finer node split R0a/R0b, R1a/R1b, R6a/R6b" from m1; build kept agon's coarse 14-node split. The finer granularity was never implemented nor documented as cut. |
| D-26 | MINOR | EARLY-R5-AUDIO lost m3's freeze clause: provisional artifacts "frozen immediately if R3 or R4 becomes REVISE, BLOCK, or NO-SHIP". |
| D-27 | MINOR | No global feedback-firing budget (m4's ≤8 per run); per-edge budgets only. |
| D-28 | MAJOR | Calibration promotion criterion weakened: m1's AUC ≥ 0.75 / n ≥ 150 / ≤5% false-block-rate → build's N ≥ 30–100 / 90% recall. Lower bar, different anchor; undocumented. |
| D-29 | MINOR | CLIP text-source intent-vs-prompt distinction collapsed to "(brief)"; m1's contractual ban on feeding the generator prompt to the scorer is not encoded. |
| D-30 | MAJOR | text_image_alignment lost m1/m4's must_include claim-checklist semantics (MUST_MISS Class A teeth; two-backend SHOULD/MUST weighting). |
| D-31 | MAJOR | AV sync uses a symmetric confidence band; m1 called symmetric \|Δt\| thresholds "a design bug" and specified +125/−45ms asymmetry (m4: +60/−40 EBU). Unforced doctrine violation. |
| D-32 | MAJOR | m1's Class A deterministic signal family (DS-01…06) and the A/B/C authority taxonomy not unified into the catalog; those checks remain scattered validators, invisible to the signal layer. |
| D-33 | MINOR | temporal_coherence ships a numeric provisional band where m1 required strict-null (CALIBRATION_REQUIRED_STRICT); weakened to uniform, undocumented. |
| D-34 | MINOR | No numeric spend units (BU LOW=1/MED=3/HIGH=8) or per-signal cost_bu anywhere; cost_tier enum carries no weights. |
| D-35 | MINOR | Signal/diagnostic idempotency layer (failure fingerprints, deterministic run keys, cached reruns) absent; per-project 32-cap UNVERIFIED/likely missing. |
| D-36 | MINOR | Signal definitions housed in dev/ + rule 35 §8 instead of m3's rule-38 home; relocation not documented as a rejection of m3's placement. |
| D-37 | MINOR | Explicit edit-vs-repair definition strings (m4 L5775–5778) absent from the signal catalog; semantics live only in MCP ledger. |
| D-38 | MAJOR | Dead reference: `MIGRATION_REGISTRY.json` L89 "the rollback path for overlay projects is BLOCKED (see ROLLBACK_PLAN)" — ROLLBACK_PLAN.json contains no overlay/approval/BLOCKED text (grep = 0). |
| D-39 | MINOR | versionMeta line-3 convention incompletely applied: 22/23 templates carry it; `EXTERNAL_TRIAL_RECORD.json` does not — and no in-tree check can detect the gap (see D-42). |
| D-40 | MAJOR | `dev\UPDATE_WORKFLOW.md` untouched by v8: no label-check wiring, no V8-1…V8-8 sections (m1 L103–151) — the migration protocol has no operator-facing documentation. |
| D-41 | CRITICAL | No `V8_0_0_RELEASE_7_BASELINE_HASHES.json` exists; `release\RELEASE.json` L30 declares `"baselineManifest": "release/V7_6_0_RELEASE_4_BASELINE_HASHES.json"` (the 7.6.0 historical file). Same root as unfixed D-7. |
| D-42 | MAJOR | `validators\validate_upgrade_compatibility.py` has NO version-label, envelope, or baseline-chain checks — m1's check_schema_version_labels (L218–239) never landed; the 4-tier ladder + VERSION_IDENTITY_CONFLICT are prose-only. |
| D-43 | MAJOR | lossCapsule pre-image store dropped: registry declares inverses but non-invertible ops have no stored pre-image to restore from. |
| D-44 | MINOR | Wave-based approval resumability (m2's waveState/SLA/waveClosedAt) dropped for a single-round matrix. |
| D-45 | MINOR | videoPolicySnapshot collapsed into policyConstants+videoLedger; R0/R1 ceiling-acknowledgement flags lost their machine representation. |
| D-46 | MINOR | Receipts carry no matrixVersion+hash pin; a receipt cannot prove which registry version governed it. |
| D-47 | MINOR | Delegation depth-1 mechanism (m5 D12, m3 proxy rules) absent entirely — nothing to constrain yet. |

### Decision-round appended defects (post-audit)

| ID | Severity | Finding |
|---|---|---|
| D-48 | MINOR (process) | Audit workpaper `V8_SELF_AUDIT.md` was written into the build tree root (`v800-build\V8_SELF_AUDIT.md`) during the audit round. The as-shipped classify gate (`dev\build_distributions.py`, unclaimed-file check) turned red on the corrected measuring process: `v8-distributions-classify` FAIL, `unclassified: ["V8_SELF_AUDIT.md"]`, unclassifiedCount 1 (dev\V8_0_0_SUITE_RESULTS.json, before-state run). **Fix (decision round, PHASE 0):** workpaper moved to the session workspace root `D:\New folder (2)\V8_SELF_AUDIT.md` (beside `audit-inputs\`, `audit-inputs-archive\`); classify gate green again. It is a session document, not a release artifact; the v8.0.0 pin (307 files) does not contain it. |
| D-49 | MINOR | `dev\extract_upgrade_baseline.py` L157–159 hardcodes `'schemaVersion': '7.8.0'`, `'baselineRelease': 'Release 4'` for every archive it pins, while its own `--expected-version` help text promises "deriving the next cycle baseline from a completed v8 release tree" — the tool writes false self-description labels onto any v8 pin. Discovered when pinning the v8.0.0 baseline: the first pin attempt emitted `schemaVersion 7.8.0 / baselineRelease "Release 4"` for a tree declaring version 8.0.0. The 307 file hashes were computed correctly; only the header labels lied. **Status: pinned header hand-corrected in `release\V8_0_0_RELEASE_7_BASELINE_HASHES.json` (see pin `labelCorrection` note); extractor source fix deferred to PHASE 2 batch** (it is a dev-tool edit, not a release artifact behavior change, and PHASE 0's constraint was "no other behavior changes in this phase" — the extractor labels are a build-time tool defect that PHASE 2 will fix with the same minimal-change + validator + sweep discipline). |
| D-50 | MINOR (validator honesty) | `mcp\resources\HARD_FACTS.json` staleness.checker (L11) advertises `python validators/check_guide_staleness.py --hard-facts mcp/resources/HARD_FACTS.json`, but the as-shipped 5-line checker accepts only a positional contract argument. **Reproduced fresh on as-shipped bytes (pwsh-43):** the advertised invocation dies at argparse — `error: unrecognized arguments: --hard-facts`, exit 2 — and the fallback positional invocation on HARD_FACTS.json dies at `KeyError: 'snapshotDate'`, exit 1. Both modes broken: the advertised command cannot run at all. R672 as shipped never caught this because it only asserts the substring `check_guide_staleness.py` inside the checker string (validate_mcp_contracts.py L200–201 as shipped) — a pointer to a capability the tool does not have. **Fixed in PHASE 1** (see PHASE 1 section): the checker now implements the advertised `--hard-facts` mode as the D-19 fact-mirror equality check, R672 executes the checker instead of grepping its name, and both former failure modes are structured errors. Confirmed by fresh check (pwsh-43 before-state; pwsh-1/pwsh-11 after-state). |

---

## PHASE 0 — v8.0.0 baseline pinned (decision round, executed)

**Order-of-operations discipline correction (recorded before pinning):** The first pin attempt
ran the extractor against a tree containing decision-round-modified bytes (repointed RELEASE.json,
fixed extractor). That sequence would have pinned round-in-progress bytes as if they were as-shipped
8.0.0 — a provenance error. Corrected sequence: as-shipped bytes were restored from
`v800-dist\combined` (RELEASE.json 70BE2877…, extract_upgrade_baseline.py 20232C14…), the baseline
generated from the true as-shipped tree, then the repoint was re-applied as the first change of the
new cycle.

**Pinned:** `release\V8_0_0_RELEASE_7_BASELINE_HASHES.json` — 307 files (the complete as-shipped
manifest count; `PACKAGE_MANIFEST.json` self-excluded by extractor design), SHA-256, as-shipped
bytes, defects included. `immutablePaths` = the 7.6.0 era record + the stale canary (two discipline
anchors whose immutability the tree can verify; NOT the approval registry — its invariants are
semantically enforced by validate_approval_versioning.py, and byte-immutability would over-constrain
legitimate policy amendments). `retiredPaths` = {} (no 8.0.0-era retirement is declared; retirements
belong to the successor cycle's baseline when they actually happen). Known-defect enumeration and
self-description notes live in the pin's `pinningNotes`.

**Repoint:** `release\RELEASE.json` baselineManifest → `release/V8_0_0_RELEASE_7_BASELINE_HASHES.json`,
plus `previousBaseline` → `release/V7_6_0_RELEASE_4_BASELINE_HASHES.json` (chain discipline per m1's
previousBaseline requirement; discovered during the round that the locator only reads
baselineManifest — previousBaseline is declared for the record and is a natural hook for the D-42
ladder fix).

**Sweep vs corrected baseline (after-state):** suite 18/18 green (`dev\V8_0_0_SUITE_RESULTS.json`),
validate_upgrade_compatibility.py PASS (0 errors; locates baseline via the repointed pointer;
immutable anchors hash-verified), validate_candidate_readiness.py PASS
(STRUCTURAL_CANDIDATE_PASS, exit 0). Tree-vs-pin drift scan: exactly 1 file drifted —
`release/RELEASE.json` (the intended repoint); 0 missing paths; both immutable anchors match.

**Known pending (tracked for PHASE 4, not defects):** `PACKAGE_MANIFEST.json` holds a stale hash for
the repointed RELEASE.json (70BE…; current 53C3…) — the binding order rebuilds the manifest as the
final Phase 4 step of the versioned increment, alongside the dist regeneration decision.
`templates\PRODUCTION_CANDIDATE_RECORD.json` L10 still points baselineManifest at the 7.6.0 file —
inert (the locator reads only release\RELEASE.json); its content describes the historical 7.8.0
candidate flow, so it is left untouched in this phase and adjudicated in PHASE 1's record corrections.

**Before/after check table (every check whose result changed):**

| Check | Before (as-shipped pointers) | After (corrected baseline) | Verdict |
|---|---|---|---|
| v8-distributions-classify | FAIL (V8_SELF_AUDIT.md unclassified) | PASS | D-48 fixed (workpaper relocation); green→red→green sequence caused by round-in-progress workpaper, not by the repoint |
| validate_upgrade_compatibility | PASS vs 7.6.0 baseline (293 files) | PASS vs v8.0.0 pin (307 files) | Real gate restored: predecessor pin now describes the actual candidate tree; no silent path-preservation no-op remains possible via the pointer |
| validate_candidate_readiness | PASS | PASS (exit 0) | unchanged |
| suite (18 checks) | 17 green + 1 red (classify) | 18 green | classify restored by D-48 fix; all other 17 checks byte-identical results |
| RELEASE.json baselineManifest | 7.6.0 file (D-7/D-41) | v8.0.0 pin | D-7/D-41 fixed |

---

## PHASE 1 — MCP-layer re-adjudication with all five prompt-2 outputs + D-19/D-50 fix (decision round, executed)

**Adjudication basis.** All five prompt-2 outputs were on the table this round (m1 §0/§1.5 L1–239, m2
L215–1807, m3 L1808–4283, m4 L4284–7401, m5 L7402–9289), with the audit's m2 analysis (5b.1–5b.4,
L261–341) and Check C (L895–944). Every fact below re-verified by fresh read/grep this round; none
rests on the audit round's memory. The fresh-evidence base:

1. **The split-brain is a five-surface, not two-surface, problem.** The numeric video-policy values
   live in: (1) `mcp\resources\HARD_FACTS.json` facts (the claimed single source of truth, Rule 03);
   (2) `schemas\artifacts\_avd_defs.schema.json` policyConstants consts L44–48 — whose description
   claimed to be "the only place numeric video-behavior bounds are legal" while HARD_FACTS.json L3
   claims "ONLY file under mcp/ permitted to carry numeric model-behavior values" (two "only place"
   claims, both false as stated); (3) `validators\validate_state_serialization.py` POLICY dict
   L55–61 — a third copy the audit's Check C did not fully flag; (4) `schemas\PRODUCTION_STATE.schema.json`
   policyConstants L91–102 — a fourth copy (inline consts, not a `$ref`) found fresh this round; and
   (5) `validators\signal_authority.py` L46 + `signal_provider_interface.py` L19 `HARD_FACTS_VIDEO`
   dicts — fifth and sixth copies (signals layer, used as provenance payloads, not enforcement caps).
   The audit recorded the two "only place" claims as D-8/D-8b; the fresh count is now part of the
   record.
2. **D-50 confirmed by fresh reproduction.** Advertised invocation: argparse exit 2 (no such flag);
   positional fallback: `KeyError: 'snapshotDate'` exit 1. R672's substring check could never catch
   it. Ledger row appended (above).
3. **ERROR_CODES.json full read (fresh)** settles m2 idea 6: FAIL-is-success is embodied without any
   `isError` wire field — every gate-verdict/hard-fact/evidence class is `retryable: false` (only
   1003/2003/6002 — bounded backoff, CAS reread, engine-availability — are retryable). The 9-tool
   roster = six gate tools + validate_gate_evidence + avd_list_capabilities + avd_request_approval
   (`MCP_SERVER_MANIFEST.json` L23–33); m2's artifact_register/capability_report naming did not ship.
4. **Audit-row corrections (fresh greps, 0 hits in mcp/):** `structuredContent`, `not_proven`,
   `claim_scope` are absent from the built wire layer. Audit rows for m2 ideas 13 ("likely adopted")
   and 13b ("ADOPTED") were over-generous; the honest verdict is NOT SHIPPED (agon's URI+sha256
   envelope discipline achieves the spirit — no binary payloads — but the mirror/claim-tail fields
   themselves never shipped). Recorded as audit-row corrections, not AUDIT ERROR: the audit itself
   flagged D-19 as absent (its "likely" hedges were marked UNVERIFIED), consistent with honest
   hedging rather than fabrication.

**Adjudication of C-P2a (the split-brain), all five outputs on the table.** The user's phase
instruction selected Check C's recommendation (branch b): **mcp runtime-resolution doctrine wins;
schema consts are equality-asserted against HARD_FACTS.json at validation time.** Rationale on the
record: the mcp layer is the layer with staleness hooks (R672), provenance (facts trace to
adapters/generation/GEMINI_OMNI_FLASH.md hard-limits verified at v7.8.0 Release 6), and the Rule-03
update path ("editing a value here updates every contract simultaneously"); the schema layer has no
update path — a stale const there is precisely the frozen-spec-table risk Rule 03 exists to prevent.
m2's in-schema const-pinning (idea 8, HardFactsBinding L390–393) and its digest guard (I3b) were
REJECTED for the same reason the audit rejected them: in-schema maximums beside fact bindings are
the doctrine avd_r6_generation_execute.json L29 already rejects ("Ceiling resolved at runtime").
Equality-assertion preserves the schema layer's default-snapshot function without granting it
authority.

**Implementation (approved scope, minimal changes, every change verified):**

1. `validators\check_guide_staleness.py` — rewritten (5 lines → ~250). New `--hard-facts` mode
   executes the D-19 mirror check: resolves each `_avd_defs` policyConstants const's
   `x-avd-fact-mirror` annotation, reads the fact from HARD_FACTS.json, applies the declared
   normalization (720→"720p" append-p; repair-budget reserved_final_slots ≥1 → finalSlotReserved
   true; above_policy classification+must_flag_at → the hyphenated policy string), and asserts
   equality across all five surfaces (_avd_defs consts, PRODUCTION_STATE consts,
   validate_state_serialization POLICY, both signal-layer HARD_FACTS_VIDEO dicts). Unannotated consts
   and unmirrored facts are divergences (fail-closed completeness). Facts staleness (last_reviewed/
   review_by) is REPORTED, not gating — AVD-E-3004 is an operational runtime-blocking condition for
   video-touching tools, not a tree invariant. The checker holds no numeric policy values itself;
   the mapping lives in schema annotations, values live in the files being asserted. Positional
   guideAlignment mode preserved byte-compatibly (verified: PROJECT_CONTRACT.json --today 2026-07-21
   → CURRENT, exit 0). Both former D-50 failure modes are now structured errors, never crashes.
2. `schemas\artifacts\_avd_defs.schema.json` — policyConstants: description corrected from "the only
   place … are legal" to the mirror doctrine (consts are a state-layer default snapshot,
   equality-asserted against HARD_FACTS.json at validation time); each of the five consts carries
   `x-avd-fact-mirror {fact, field, normalize}` annotations carrying the fact-id mapping.
3. `validators\validate_mcp_contracts.py` — R672 upgraded: the staleness-hook string check now
   also requires the `--hard-facts` mode name in the advertised command, and a new executable check
   (`MCP_HF_MIRROR`) runs the advertised mirror check in-process (import, not subprocess — the suite
   imports validators in-process; R677 engines self-test + suite discipline preserved) and fails
   closed on any divergence.

**Negative test (no silent patches — proof the check bites).** A disposable tree outside the build
(`_tmp_mirror_negtest.py`, deleted after the run) copied all six surfaces, mutated ONE const
(maxSequentialConversationalEditsPerClip 3→4), and ran the real checker: exactly 5 divergences on
exactly the 5 surfaces carrying that number, `mirrorStatus: DIVERGENT`, exit 1. The check detects
drift in every direction it claims to guard.

**m2's convergent ideas — credited in V8_SYNTHESIS.md P2 (appendix added this round), re-affirmed
here:** I1 sampling-ban (MCP_SERVER_MANIFEST PROMPT_ONLY_CONTROLLER), I2 one-envelope
(TOOL_CONTRACT meta-schema), I3 tokens+fact-bindings (x-avd-fact-max/budget + Rule 03), I4 evidence-
required scores (X14 AVD-E-3001/3002), I5 FAIL-is-success (retryable:false on verdict classes),
hard_facts_digest guard (equality-asserted, not digest-pinned — hybridized), gate→validator dispatch
(wraps_validators), staleness hooks (R672 — now executable, was dead). **Rejected m2 ideas, reasons
on the record:** idea 8 in-schema const-pinning (contradicts runtime-resolution doctrine this
adjudication reaffirms); E_AVD_4xx HTTP-like error numbering (agon's class-grouped AVD-E-Nxxx is the
shipped scheme, verified live against ERROR_CODES.json); not_proven[]/claim_scope wire tails (agon's
claim-boundary prose + X14 evidence discipline shipped instead; adding fields now would be a wire
change beyond FIX-NOW scope); AVD-TR/1 transport receipt (one-envelope discipline achieved via
TOOL_CONTRACT meta-schema); structuredContent/content[] mirror rule (not in the shipped wire layer —
fresh grep 0 — and not required by any consumer; recorded as NOT SHIPPED, not adopted).
**m2 idea 6 (isError)**: settled NOT NEEDED — FAIL-is-success is fully embodied by retryable:false
on all gate-verdict classes (fresh ERROR_CODES.json read); a wire field would be redundant.
**m2 idea 13/13b verdict correction:** audit rows "likely adopted"/"ADOPTED" corrected to NOT
SHIPPED (fresh grep: structuredContent/not_proven/claim_scope absent from mcp/). agon's
URI+sha256 envelope achieves the no-binary-payloads spirit; the specific wire fields never shipped.
**C-P2b/C-P2c:** no action — C-P2b (9-tool roster matching m2/agon, not m1's 12) is confirmed
accurate by the fresh manifest read; C-P2c (error numbering) is cosmetic, agon's scheme ships, the
record already states neither is wrong.

**Sweep after PHASE 1 edits (after-state):** full suite 18/18 green (`dev\V8_0_0_SUITE_RESULTS.json`
rewritten by the run): state layer 87/0, gate DAG 57/0, MCP contracts 141/0 (was 140 as shipped —
+1 is the new executable MCP_HF_MIRROR check), approval+versioning 65/0, signal layer ALL CHECKS
PASS, python-compile clean, classify green, snapshot agreement green, canary 7.4.0 intact, tier map
agreement green. validate_mcp_contracts standalone: 141 passed / 0 failed; validate_state_serialization
standalone: 87 passed / 0 failed. Checker verified in all three modes (hard-facts mirror MIRROR-OK
exit 0 on the live tree; positional on HARD_FACTS.json → structured CONTRACT_MISSING_GUIDE_ALIGNMENT
error, no crash; positional on PROJECT_CONTRACT.json → CURRENT exit 0).

**Tree-vs-pin drift after PHASE 1 (expected drift, not gate failure — edited paths are not
immutablePaths):** 4 of 307 paths drifted: `release/RELEASE.json` (PHASE 0 repoint, already
ledgered), `schemas/artifacts/_avd_defs.schema.json`, `validators/check_guide_staleness.py`,
`validators/validate_mcp_contracts.py` (the three PHASE 1 edits). 303 unchanged, 0 missing, 0
untracked extras, both immutable anchors (7.6.0 era record, stale canary) still matching. Pycache
residue from the verification runs was cleaned (0 remaining) per build discipline.

**Record corrections identified this round (carried to PHASE 3, no behavior change):**
`templates\PRODUCTION_CANDIDATE_RECORD.json` L9/L10 (baselineRelease "7.6.0" / baselineManifest →
V7_6_0 file) — confirmed inert fresh this round (locator reads only release\RELEASE.json; the
template describes the historical 7.8.0 candidate flow); its correction is a record correction
(PHASE 3), not a fix-now item. Audit rows for m2 ideas 13/13b — corrected in this section (and the
synthesis appendix); the 5b.1 table rows themselves stay as the audit wrote them (the audit is a
record; corrections live in the decision-round sections, not in rewritten history).

---

## PHASE 2 — FIX-NOW batch (decision round, executing)

Discipline per item: fresh re-verify of the evidence (disproven → AUDIT ERROR, confirmed →
"confirmed by fresh check"), minimal change, validator re-run, ledger with evidence, and a full
suite sweep at batch end. Drift of edited paths vs the pinned 8.0.0 baseline is expected and
observable (the pin is a record, not an endorsement); no immutablePaths are touched by this batch.

### D-9 — all-zero/all-f placeholder digests accepted as computed — FIXED

**Confirmed by fresh check.** `validators\validate_state_serialization.py` L41 `SHA256 =
^[0-9a-f]{64}$` accepted all-zero/all-f; the only enforcement point is `validate_digest` L75–87
(status "computed" branch). Fresh scope verification:

- No fixture anywhere in the tree uses `digestStatus: "computed"` — the shipped 87 green checks
  never exercised the vulnerable branch (grep verified). The defect was latent, not observed
  green-on-red.
- The three other 64-hex validators (`validate_human_evidence` L43, `validate_evidence_manifest`
  L20, `validate_external_evidence` L26) all **re-compute the hash against actual file bytes**, so
  a declared placeholder cannot pass there. The state layer is the one validator that must take
  digests on trust (it validates serialized state, not files), which is precisely why
  placeholder-format rejection matters there.
- The all-zero `boundArtifactSha256` in `templates\APPROVAL_LEDGER.json` L28 and
  `gate-receipt.example.json` L32 is a DIFFERENT field — the documented pre-binding genesis
  convention, explicitly allowed by `validate_approval_versioning.py` L87
  (`boundArtifactSha256[0] == "0"*64` accepted for the genesis entry). Untouched by this fix.
- `MARKER` regex L44 carried the same hole in the state-marker grammar's sha256 branch;
  `validate_marker` L90 has no callers (dead code, left in place — noted here, not changed).
- Schema twin: `_avd_defs.schema.json` `$defs.digestStatusObject.digest.pattern` L28 had the same
  permissive `^[0-9a-f]{64}$`. No schema-linter compiles patterns (grep `jsonschema` = 0; nothing
  validates schemas/ tree patterns), but the tightened twin keeps the two layers from
  re-diverging.

**Change (minimal):**
1. `validate_state_serialization.py` — `SHA256` → `^(?!0{64}$)(?!f{64}$)[0-9a-f]{64}$` (rejects
   exactly-all-zero and exactly-all-f; accepts every other 64-hex string, including 63-zeros+1);
   `MARKER` grammar sha256 branch tightened identically; `expected_fail`/`vmap` extended with two
   new negative fixtures mapped directly to `validate_digest` (bare `digestStatusObject` shape —
   a receipt-shaped fixture would record TWO failures where the harness pops ONE).
2. `schemas/artifacts/_avd_defs.schema.json` — `digestStatusObject.digest.pattern` tightened to
   the same regex, with a description pointing at the validator.
3. New fixtures `schemas\examples\negative_tests\digest_placeholder_zero.json` and
   `digest_placeholder_ff.json` (bare digest objects claiming computed with all-zero/all-f;
   `_fixtureIntent` house style; classify-safe — `schemas/` is claimed by both distribution rule
   sets, and `validate_upgrade_compatibility` only fails on MISSING baseline paths, so new tree
   files are clean).

**Validator evidence (fresh):** regex behavior table — accepts
`14653e17…` (real hash), `0*63+"1"`, `"1"+0*63`; rejects `0*64`, `f*64`, `a*63` (short), `a*65`
(long), `g*64` (non-hex): ALL 8 edge cases behave as specified. Standalone
`validate_state_serialization.py`: **91 passed / 0 failed, exit 0** (was 87 — delta +4 = 2 new
fixtures × 2 PASS rows each: the `check()` row and the explicit `STATE_NEG_EXPECTED_FAIL` row;
arithmetic exact, no other check changed). `py_compile` clean. Genesis all-zero
`boundArtifactSha256` unaffected (different field, different validator).

**Not changed (scoped out, on the record):** `GATE_RECEIPT.schema.json` `boundArtifactSha256`
items pattern and `ledgerRef` pattern; `HANDOFF_PACKET.schema.json` `ledgerDigest` pattern;
`_avd_defs.schema.json` `evidenceRef.artifactSha256` (already allows empty/EXAMPLE: forms). These
are **binding/pointer** fields with documented conventions (genesis pre-binding, EXAMPLE
provenance), not digest-claim fields; `ledgerRef`/`ledgerDigest` point into a ledger the tree
governs elsewhere. Tightening them would reject the shipped examples' legitimate placeholders —
out of D-9's defect class (digest-claim fabrication), and rejected as scope creep.

### D-14b — "JCS-1" label with no JCS implementation — FIXED (relabel branch)

**Confirmed by fresh check.** `canonicalization: { "const": "JCS-1" }` — `_avd_defs.schema.json` L29;
`validate_state_serialization.py` L85 equality-checks it; 8 example/fixture files carry it
(digest_status "uncomputed" in every shipped use); `grep "def jcs"` = 0 across the tree — the label
named a canonicalization the tree could not perform. The shipped label's provenance is m1's
proposed function (p1_m1.md L619–622): `json.dumps(obj, sort_keys=True, separators=(",",":"),
ensure_ascii=False).encode("utf-8")` — which m1 itself called "RFC 8785-**shaped**", not JCS. True
RFC 8785 additionally mandates ECMAScript number re-serialization (e.g. 1e+30 for 1E30, integer
trailing-zero removal) that Python's json.dumps does not implement, so shipping m1's function under
the name "JCS-1" would have repeated the same false claim with new paint.

**Branch decision (user's "JCS or remove claim"), evidence-grounded:** the implement-true-JCS branch
is UNVERIFIABLE today — web search is unavailable in this session (no configured provider), and the
corpus contains no RFC 8785 test vectors (m4 asserts "JSON canonicalization is RFC 8785" at p5_m4.md
L306 but ships no vectors; m4's own R658 row L2896 "Forward then inverse transform / RFC 8785 input
restored" specifies a round-trip property, not vector bytes). Claiming RFC conformance from model
memory would rebuild the hollow label one level deeper — my recollection is not evidence under the
VERIFICATION PROTOCOL. The relabel branch is fully groundable: the new label names the exact
standard form the runtime performs, one line of stdlib, the same form m1's original function
implements and m5's precedent labels ("json_sorted_keys_utf8_lf", p5_m5.md L65/816) describe.

**Change (minimal, 10 files):**
1. `schemas/artifacts/_avd_defs.schema.json` — const `"JCS-1"` → `"JSON-SORTED-KEYS-UTF8"`,
   description carries the exact byte form (`json.dumps(obj, sort_keys=True, separators=(",",":"),
   ensure_ascii=False).encode("utf-8")`) and the honesty note (not RFC 8785/JCS; former label named
   an unimplemented canonicalization).
2. `validators/validate_state_serialization.py` L85 — equality check follows the new const, with a
   D-14b comment.
3. All 8 example/fixture carriers relabeled (gate-receipt, asset-tracker-entry, handoff-packet
   examples; receipt_over_budget, receipt_score_no_evidence, asset_bad_name, digest_placeholder_zero,
   digest_placeholder_ff negative fixtures). Zero behavioral change: every shipped digest is
   `"uncomputed"`; the label is metadata about a form, asserted only for equality.

**Validator evidence (fresh):** `py_compile` clean; `validate_state_serialization.py` standalone
**91 passed / 0 failed, exit 0**; full suite **18/18 green** (state 91/0, gate DAG 57/0, MCP 141/0,
approval 65/0, signal ALL PASS, compile clean, classify green). Residue check: the only remaining
`JCS` strings in the tree are explanatory/historical (validator comment, schema description, and the
baseline pin's known-defects record — the pin describes as-shipped 8.0.0 and is exempt by design).
No live `JCS-1` value remains anywhere (grep verified).

**Scoped out, on the record:** implementing true RFC 8785 remains open as a future increment if
official vectors become available (it would be a real behavior change requiring vector-anchored
self-tests — not a relabel). The pin's `D-14b` known-defect note stays as-is: it records the
as-shipped state, which is what a baseline is for.

### D-31 — symmetric AV sync band vs m4's EBU asymmetry — FIXED (with evidence corrections)

**Fresh re-verify found the defect CONFIRMED but the audit row's evidence PARTIALLY WRONG —
corrections recorded here (and carried to the PHASE 3 erratum):**

1. **Corrected:** the audit row called `[3.5, 6.0]` an "ms band". It is NOT: it is
   `advisory_range_conf_provisional` for SyncNet **confidence** (unitless 0–10; catalog
   `units: "SyncNet confidence"` L113; `operator: ">="` L205). The `[3.5, 6.0]` numbers are the
   CONFIDENCE advisory range, correctly provisional, untouched by this fix. The pin's
   known-defects note inherited the same "ms" slip (as-shipped record, left as-is; erratum records
   it).
2. **Corrected:** the audit row and pin say m4 specified "EBU +60/−40ms". m4's actual words
   (prompt-4 corpus L5835): `"basis": "broadcast tolerances (e.g., EBU R37 +40/−60 ms) inform
   targets; generator output uncalibrated"`. The true defect: the tree's only AV-offset numeric is
   the symmetric correlation SEARCH window `[-200ms, +200ms]` (catalog formula L104) with NO
   acceptance tolerance at all — symmetric or asymmetric. Both sources' asymmetry was dropped.
3. **Confirmed:** m1 (prompt-4 corpus L85, quoted verbatim): "Tolerance frame (ITU‑R BT.1359‑1
   class): detectability ≈ audio‑late +125 ms / audio‑early −45 ms; acceptability ≈ +185 / −90
   ms. **Human perception is asymmetric — audio‑early is far worse.** Thresholds must be
   asymmetric; a symmetric |Δt| threshold is a design bug." And m1's R7 row (L178): "|bias| ≤ 40
   ms; hard: >+120 ms late / >−45 ms early". The build ignored both sources — unforced doctrine
   violation, exactly as the audit adjudicated.

**Change (minimal, 2 files):**
1. `dev\QUALITY_SIGNALS_CATALOG.json` — audio_visual_sync gains
   `av_offset_tolerance_provisional`: sign convention declared (`av_offset_ms = audio_ms −
   video_ms; positive = audio late`), `audio_late_ms_max: 60`, `audio_early_ms_max: 40`
   (audio-early TIGHTER, per the asymmetry both sources state), `basis` quoting both sources with
   corpus line numbers, `status: "provisional"`, `surface`/`as_of` per Rule 03. The `[−200,+200]`
   search window is explicitly documented in the block as a correlation search range, NOT an
   acceptance band. Numbers chosen: the adopted operational provisional (early 40 / late 60)
   follows the EBU R37 basis as m4 wrote it (+40/−60 in m1/m4's late-positive convention) with
   the early side tighter; m1's detectability frame (+125/−45) is recorded verbatim in `basis` for
   the calibration procedure. Definition/formula strings otherwise byte-identical (one unintended
   word drop self-caught and reverted before verification).
2. `validators\signal_authority.py` — new `check_av_sync_asymmetry(catalog)`: requires the
   tolerance block, requires it numeric, REJECTS symmetric-or-inverted tolerances
   (`audio_early_ms_max >= audio_late_ms_max` → reject), requires the basis to cite BOTH sources
   (ITU-R BT.1359-1 class frame + EBU R37), requires `status: "provisional"` (CALIBRATION_REQUIRED
   — cited-standard provisional ranges, never measured on generator output). Wired into
   `--check all` as the `[AV sync asymmetry]` row (R677 signal layer).

**Validator evidence (fresh):** positive — `--check all` ALL CHECKS PASS with new row `pass —
asymmetric AV tolerance early<=/40ms < late/60ms, both sources cited, provisional`. Negative
(in-memory mutations, no tree edits): tolerance block removed → REJECTED ("as shipped: symmetric
search window only, no acceptance tolerance"); early=late=50 → REJECTED ("symmetric-or-inverted…
audio-early must be TIGHTER"); status→"measured" → REJECTED ("must be status provisional
(CALIBRATION_REQUIRED)"). ALL_NEGATIVES_BITE=True. `py_compile` clean. Full suite **18/18 green**
(R677 shows the new row); drift scan: 13 drifted files (the cumulative PHASE 1 + D-9 + D-14b +
D-31 edit set — catalog + signal_authority newly joined), 2 extras (the D-9 fixtures), 0 missing,
immutable anchors intact.

**Honesty boundary recorded in the block itself:** the 40/60 numbers are a PROVISIONAL operational
choice among cited standard ranges, not a measurement; the calibration procedure (Scratch VO +
board timing pairs, SyncNet conf vs human sync rating, ROC — already the catalog's
`calibration_procedure` for this signal) is the path to replace them. m1's detectability and
m4's R7-hard bounds are preserved verbatim in `basis` so calibration starts from the sources, not
from this round's choice.

### D-38 — dead ROLLBACK_PLAN pointer — FIXED (overlay-policy branch, plus a self-caught defect)

**Confirmed by fresh check.** `MIGRATION_REGISTRY.json` L89: `"the rollback path for overlay
projects is BLOCKED (see ROLLBACK_PLAN)"` — while `templates/ROLLBACK_PLAN.json` contained zero
overlay/approval/BLOCKED content (grep = 0 across the tree): its triggers, steps, and verification
covered archive-restore rollback only. The audit offered two branches: write the overlay section
or fix the pointer. The registry note is real, R686-enforced doctrine (`MIGRATION_ROLLBACK_HONESTY`
asserts `"BLOCKED" in v8v7["note"]`), so deleting the pointer would delete doctrine — the correct
branch is to give the reference a target.

**Fresh check also found an unledgered as-shipped defect:** ROLLBACK_PLAN.json `verification`
carried a byte-identical duplicate line ("All prior bundled suites pass after extraction." at both
L29 and L30). Fixed in the same file, on the record, with its own validator code
(`ROLLBACK_VERIFICATION_DUPLICATE`) so it cannot silently regress.

**Change (minimal, 3 files):**
1. `templates/ROLLBACK_PLAN.json` — new top-level `overlayRollbackPolicy`: overlay-carrying
   receipts (roleApprovals) cannot collapse to v7.8.0 absent-overlay semantics without losing
   approvals; rollback path BLOCKED; overlay projects stay on 8.0.0 under the registry
   `lossless_definition` with explicit project-owner sign-off; archive restore never lifts the
   block. Verification list: the duplicate line replaced by a distinct overlay BLOCKED check
   (5 distinct lines, up from 4 with one duplicate).
2. `validators/validate_rollback_plan.py` — four new checks: `ROLLBACK_OVERLAY_POLICY_MISSING`
   (policy absent), `ROLLBACK_OVERLAY_POLICY_INCOMPLETE` (must name the MIGRATION_REGISTRY
   linkage, the BLOCKED verdict, and project-owner sign-off),
   `ROLLBACK_OVERLAY_VERIFICATION_MISSING` (verification must include the overlay check),
   `ROLLBACK_VERIFICATION_DUPLICATE` (lines must be distinct).
3. `templates/MIGRATION_REGISTRY.json` L89 — the ambiguous `(see ROLLBACK_PLAN)` made exact:
   `(see templates/ROLLBACK_PLAN.json overlayRollbackPolicy)`. R686's assertion
   (`"BLOCKED" in note`) unaffected.

**Validator evidence (fresh):** `py_compile` clean; CLI run `pass: true, errors: []`; negative
tests (in-memory mutations): policy removed → `ROLLBACK_OVERLAY_POLICY_MISSING`; policy
gutted → `ROLLBACK_OVERLAY_POLICY_INCOMPLETE`; overlay verification line removed →
`ROLLBACK_OVERLAY_VERIFICATION_MISSING`; duplicate line re-inserted →
`ROLLBACK_VERIFICATION_DUPLICATE`. ALL_NEGATIVES_BITE=True. Both consumers re-verified green:
`validate_approval_versioning.py` 65/0 (R686 BLOCKED assertion intact),
`validate_candidate_readiness.py` STRUCTURAL_CANDIDATE_PASS. Full suite **18/18 green**; drift
scan: 16 drifted (13 cumulative + registry, rollback plan, rollback validator), 0 missing,
immutable anchors intact.

### D-39 — EXTERNAL_TRIAL_RECORD.json missing versionMeta — FIXED (sibling-standard bump + sweep gate)

**Confirmed by fresh check, and the fresh check found more than the audit row stated.** The audit
row: "22/23 templates carry versionMeta; EXTERNAL_TRIAL_RECORD.json does not — and no in-tree
check can detect the gap." Fresh grep: 22 of 23 templates carry the line-2 `schemaVersion:
"8.0.0"` + line-3 `versionMeta` head; EXTERNAL_TRIAL_RECORD alone (a) had NO versionMeta,
(b) declared `schemaVersion: "7.8.0"` buried at **line 46** of 48 (the whole line-2/line-3
convention absent — not merely the line-3 marker), and (c) carried `release: "7.8.0"` at line 47.
The file is 7.6.0-baseline heritage that the 8.0.0 bump pass missed entirely.

**Design decision (evidence-grounded):** the fix is the SAME standard bump its 22 siblings
received — NOT a bare versionMeta insertion. Per the MIGRATION_REGISTRY's own
`structural_fingerprints` (tier-2 evidence), `versionMeta` present at line 3 is an 8.0.0
structural marker; inserting it into an artifact still declaring `schemaVersion: 7.8.0` would
manufacture a declared-vs-inferred conflict (the 7.4.0-defect class the ladder hard-fails on)
rather than fix one. The consumer `validate_external_evidence.py` never reads these fields
(fail-closed trial/rating/campaign validation only — grep-verified), so the bump is
behavior-neutral to validation; its effect is convention conformance + detectability. The
`release: "7.8.0"` field is RETAINED at line 4 in family position: 10 sibling templates keep
`release: "7.8.0"` there as the evidence-subsystem era marker (EXTERNAL_RATING_RECORD, the trial
record's direct sibling, among them); only ROLLBACK_PLAN carries `release: "8.0.0"` (rollback is
8.0.0-new capability). Removing it would have been unforced family drift — first edit did drop
it, self-caught and restored before verification.

**Change (minimal, 2 files):**
1. `templates/EXTERNAL_TRIAL_RECORD.json` — head rebuilt to the sibling standard:
   line-2 `schemaVersion: "8.0.0"`, line-3 `versionMeta { ruleVersion 8.0.0, producerVersion
   ai-visual-director-production@8.0.0, migratedFrom "7.8.0" }`, line-4 `release: "7.8.0"`
   retained; the buried tail `schemaVersion`/`release` lines removed. Body fields byte-identical.
2. `validators/validate_approval_versioning.py` — new R686b template-convention sweep (closes
   the "no in-tree check can detect the gap" hole): asserts the template count (23), and for
   EVERY template: line-2 `schemaVersion == "8.0.0"`, `versionMeta` present, head order
   (`schemaVersion` then `versionMeta` as first two keys), and versionMeta shape
   (ruleVersion/producerVersion/migratedFrom with migratedFrom ∈ 7.4.0/7.6.0/7.8.0 —
   SEMANTIC_REVIEW's richer block passes: it carries the three standard keys plus
   transformChain/defectProvenance, migratedFrom "7.4.0").

**Validator evidence (fresh):** `py_compile` clean (after one caught-and-fixed syntax slip — the
negative-test harness itself surfaced `for tpl_dir.glob` missing `p in`, refusing to report
success on a broken validator; that is the discipline working, not a defect in the shipped tree);
`validate_approval_versioning.py` standalone **158 passed / 0 failed** (65 prior + 93 new sweep
rows: 23 templates × 4 checks + 1 count row); negative tests (script
`_tmp_d39_negtest.py`, byte-exact restore verified): versionMeta removed → 3 sweep failures
(TPL_VERSIONMETA/TPL_HEAD_ORDER/TPL_VERSIONMETA_SHAPE); schemaVersion reverted to 7.8.0 →
TPL_SCHEMA_VERSION failure (the exact as-shipped defect, now detectable); head order inverted →
TPL_HEAD_ORDER failure. ALL_NEGATIVES_BITE=True, RESTORED_BYTE_EXACT=True. Full suite **18/18
green** (approval+versioning now 158/0); drift scan: 18 drifted (16 + EXTERNAL_TRIAL_RECORD +
approval_versioning validator), 0 missing, immutable anchors intact.

### D-42 — 4-tier version-detection ladder prose-only — FIXED (ladder as real code)

**Confirmed by fresh check.** The shipped `validate_upgrade_compatibility.py` (127 lines) carried
ONLY baseline-path/immutable/retirement checks — no label check, no envelope check, no baseline
chain, no conflict rule. The 4-tier ladder and VERSION_IDENTITY_CONFLICT existed only as prose in
MIGRATION_REGISTRY.json `version_detection_ladder` (and as a string-equality assertion on that
prose in validate_approval_versioning R685 — which proves the prose says what it says, not that
any artifact obeys it). The audit row cited m1's written code ("m1's check_schema_version_labels
was written — m1 §1.5 L218–239"): confirmed — p5_m1.md L219–239 is a complete
probe/classify/sweep implementation with `labelCheckExemptions` in the baseline pin and
`previousBaseline {path, sha256}` chain keys, both declared additive by m1 ("the 7.8.0 validator
ignores unknown keys, the 8.0.0 validator requires them", p5_m1 L182).

**Change (minimal, 3 files):**
1. `validators/validate_upgrade_compatibility.py` — v8.0.0 additions implementing the ladder as
   code (m1's design, adapted — adaptations enumerated below):
   - `check_version_labels` — tier-1 (line-2 declared) vs tier-2 (`versionMeta` structural)
     sweep over every pinned JSON with per-path exemptions from the pin. Arms:
     `ARTIFACT_VERSION_FUTURE`, `ARTIFACT_SCHEMA_VERSION_STALE` (era label without exemption),
     `ARTIFACT_SCHEMA_VERSION_MALFORMED`, `ARTIFACT_ENVELOPE_MISSING` (≥8.0.0 without
     versionMeta — the D-39 class, tree-wide at last), `ARTIFACT_ENVELOPE_INCOMPLETE`
     (producerVersion), and the registry's conflict rule as code:
     `VERSION_IDENTITY_CONFLICT` for declared ≠ versionMeta.ruleVersion AND for versionMeta
     present while declared < 8.0.0 (undocumented upgrade shape).
   - `check_baseline_chain` — m1 L242–248: previousBaseline path exists + sha256 matches.
   - `check_ladder_registry_agreement` — the code's tier map {1:DECLARED, 2:STRUCTURAL,
     3:SEMANTIC, 4:EXPLICIT_MARKERS} must EQUAL the registry's declared ladder, and the
     registry's conflict rule must name VERSION_IDENTITY_CONFLICT: the code may not invent a
     different ladder than the registry declares, and the registry may not describe a rule
     nothing enforces. Both directions bite (negative-tested).
   - Package version read from `release/RELEASE.json` (`version` field) — single source of
     truth per D-15's doctrine; no hardcoded version duplicated in the validator.
   - CLI/description/proofBoundary updated V7.8.0→V8.0.0; existing checks and their codes
     untouched (m1's anchor rule).
2. `bootstrap/runtime_load_manifest.json` — **a real defect the new check caught in the live
   tree**: declared 8.0.0 (+ packageVersion 8.0.0) with NO versionMeta, in a file no existing
   sweep covered (outside templates/, outside VSS's dirs). Fixed with the sibling-standard
   versionMeta block. This is the D-39 class manifesting outside templates — the ladder's first
   live catch.
3. `release/V8_0_0_RELEASE_7_BASELINE_HASHES.json` — m1's additive pin keys: `previousBaseline
   {path: V7_6_0 pin, sha256: 138ea624…c05}` (chain anchor) and `labelCheckExemptions` (9
   entries, each with an evidence-grounded reason): canary (its own canaryContract +
   registry exemptions), V7_6_0 pin (predecessor era record, immutable path),
   PORTABLE_REFERENCE_MANIFEST (7.8.0-lineage profile carried forward unchanged — bumping it
   would assert a migration that never happened, the 7.4.0-defect class), 6 chat fixtures
   (7.8.0-era validate_project regression fixtures). Additive only — the 307 file hashes
   untouched.

**Adaptations of m1's spec, enumerated (not silent):** (1) m1 checked a `versionEnvelope` key
that never shipped; the shipped envelope is `versionMeta` (same required fields ruleVersion/
producerVersion) — the check reads the shipped name. (2) m1 flagged MISSING on every JSON
without line-2 schemaVersion (~50 files: schema definitions with `$id`, MCP contracts, catalogs,
dev results) — the shipped tree's VSS R651 precedent treats only files whose line-2 HAS a
schemaVersion as in-convention; this check follows that precedent (the exhaustive templates/
convention surface is R686b's from D-39). (3) m1's `--state`/`--lane` artifact-validation
additions require jsonschema + schemas/dist bundles — neither exists in this tree (no
jsonschema anywhere, grep = 0); out of scope, recorded.

**Validator evidence (fresh):** `py_compile` clean; CLI positive `pass: true` with the new
proofBoundary; consumer `validate_candidate_readiness.py` STRUCTURAL_CANDIDATE_PASS (imports
this validator's `validate` — signature and existing codes unchanged). Negative battery
(`_tmp_d42_negtest.py`, 13 checks, byte-exact restore of the mutated live file): conflict
(declared 8.0.0 vs versionMeta 7.8.0) → VERSION_IDENTITY_CONFLICT; envelope-missing temp file →
ARTIFACT_ENVELOPE_MISSING; stale temp file → ARTIFACT_SCHEMA_VERSION_STALE; future 9.0.0 →
ARTIFACT_VERSION_FUTURE; canary exemption REMOVED from the pin → stale fires on the canary
(exemptions load-bearing); chain wrong sha → BASELINE_CHAIN_BROKEN; chain key removed →
BASELINE_CHAIN_BROKEN; registry tier renamed → LADDER_REGISTRY_DISAGREEMENT; conflict-rule text
removed → LADDER_CONFLICT_RULE_MISSING; LIVE-FILE arm: runtime_load_manifest versionMeta
stripped, full CLI run → ARTIFACT_ENVELOPE_MISSING + exit 1, then byte-exact restore.
ALL_NEGATIVES_BITE=True. Full suite **18/18 green**; drift scan: 20 drifted (18 +
runtime_load_manifest + validate_upgrade_compatibility), 0 missing, immutable anchors intact
(pin's own additive keys invisible to itself per its selfPinNote — correct by design).

### D-49 — extractor hardcodes baseline header labels — FIXED (derive from the archive)

**Confirmed by fresh check.** `dev/extract_upgrade_baseline.py` L157–159 wrote
`'schemaVersion': '7.8.0'` and `'baselineRelease': 'Release 4'` as CONSTANTS onto every
baseline it pins — while the very same run had already verified the archive's true version via
`read_version()` + the `--expected-version` gate, and its own help text promises "deriving the
next cycle baseline from a completed v8 release tree". The PHASE 0 pin hit exactly this: the
first pin attempt emitted 7.8.0 / "Release 4" labels for a tree declaring 8.0.0 / Release 7
(header hand-corrected at pin time, recorded in the pin's `labelCorrection` note; source fix
was deferred to this batch by the PHASE 0 scope constraint).

**Change (minimal, 1 file):** `dev/extract_upgrade_baseline.py` —
`read_version()` now returns the release label alongside the version; `open_archive()`
propagates it; the baseline header derives BOTH labels from the archive's own verified
`release/RELEASE.json`: `schemaVersion` = verified version (was constant `'7.8.0'`),
`baselineRelease` = declared release label (was constant `'Release 4'`), `provenance` names the
actual version/release. New fail-closed gate: an archive whose RELEASE.json declares a version
but NO release label refuses to write rather than invent a label. Docstring/usage lines that
asserted version-specific behavior for a parameterized tool aligned (default stays 7.6.0; the
v8 path is documented as what it is).

**Validator evidence (fresh):** `py_compile` clean. Functional: extractor run against the LIVE
tree (declares 8.0.0 / Release 7) → written baseline header `schemaVersion 8.0.0`,
`baselineVersion 8.0.0`, `baselineRelease "Release 7 — Machine State Layer (v8.0.0)"`,
provenance mentions Release 7, fileCount 310 (307 pinned + 2 D-9 fixtures + regenerated suite
results; PACKAGE_MANIFEST excluded by extractor design) — exactly the case the as-shipped tool
got wrong, now correct end-to-end. Negatives: version-with-no-release-label archive →
status FAIL, exit 1, no output written; version mismatch (expected 7.6.0, archive 8.0.0) →
still refuses (the pre-existing laundering gate intact). ALL_CHECKS_PASS=True. (One
harness-only iteration: the negatives initially parsed stdout while `raise SystemExit(json)`
prints to stderr — test-harness bug, tool behavior was correct; fixed in the harness, not the
tool.) Full suite **18/18 green**; drift scan: 21 drifted (20 + the extractor), 0 missing,
immutable anchors intact.

### PHASE 2 batch-end — full sweep + before/after table

**Final sweep (after all seven fixes):** state layer 91/0 · gate DAG 57/0 · MCP contracts
141/0 · approval+versioning 158/0 · signal layer ALL CHECKS PASS (incl. new AV-sync-asymmetry
row) · 18/18 checks green · classify unclassifiedCount 0 · canary 7.4.0 · drift scan 21
drifted / 0 missing / 2 extras (D-9 fixtures) / immutable anchors intact.

| Defect | As shipped (PHASE 0 pin) | After PHASE 2 (this batch) | Validator that proves it |
|---|---|---|---|
| D-9 | all-zero/all-f "computed" digests accepted | regex rejects exactly-all-0/f; 2 negative fixtures | validate_state_serialization 91/0 (was 87/0) |
| D-14b | `JCS-1` label, no JCS implementation | relabeled `JSON-SORTED-KEYS-UTF8` (exact stdlib form), 10 files | VSS 91/0 + suite 18/18; grep: 0 live JCS-1 |
| D-31 | symmetric search window only; no AV acceptance tolerance | asymmetric provisional block (early 40 < late 60 ms), both sources quoted, Rule-03 compliant | signal_authority `[AV sync asymmetry]` + 3 negative mutations |
| D-38 | registry points at ROLLBACK_PLAN overlay section that doesn't exist; plan has duplicate verification line | overlayRollbackPolicy written + 4 validator checks + exact pointer; duplicate line replaced | validate_rollback_plan 4 new codes, all bite; consumers 65/0 + CANDIDATE_PASS |
| D-39 | EXTERNAL_TRIAL_RECORD: no versionMeta, schemaVersion 7.8.0 at line 46 | sibling-standard head (line-2 8.0.0, line-3 versionMeta, release retained); R686b sweeps ALL 23 templates | VAV 158/0 (was 65/0); 3 negative mutations bite |
| D-42 | ladder + VERSION_IDENTITY_CONFLICT prose-only | ladder as code (label sweep, conflict rule, chain, registry agreement); caught a live defect: runtime_load_manifest missing versionMeta | 13-check negative battery + live-file arm; candidate_readiness green |
| D-49 | extractor stamps 7.8.0/Release 4 onto every pin | labels derive from archive's verified RELEASE.json; fail-closed on missing label; functional test pins live tree → truthful 8.0.0/Release 7 header | extractor functional + 2 negatives (fail-closed, mismatch-refused) |

**Self-caught during this batch (both fixed in-batch, both on the record):** ROLLBACK_PLAN
duplicate verification line (D-38 work); bootstrap/runtime_load_manifest missing versionMeta
(caught BY the new D-42 check — the ladder's first live catch, fixed as part of D-42).

## PHASE 3 — record corrections (decision round, complete)

No behavior changes; each edit is documentation-of-record for a defensible-but-undocumented
choice, or a correction of an inert record. All JSON syntax-validated (`json.tool` exit 0),
full suite 18/18 after every edit, drift observed (23 files) with 0 missing and immutable
anchors intact.

1. **D-28 (earned promotion bar)** — `dev/QUALITY_SIGNALS_CATALOG.json`
   `composite_scoring.promotion_criteria` added: the N≥30/100 + 90%-recall floors are the
   PROVISIONAL calibration floor; promotion of any signal to decision authority requires m1's
   EARNED bar (prompt-1 corpus L17): AUC ≥ 0.75 held-out, n ≥ 150 per gate class, false-block
   rate ≤ 5%. The silently-dropped promotion criterion is now stated where the calibration
   thresholds live.
2. **D-23/D-25 (feedback routes + node granularity)** —
   `rules/detailed/35_gate_dag_v800.json` `feedbackEdgePolicy` added: enumerates all eight
   designed-but-unshipped feedback routes (m1 FB1–FB8, m4 FB-R8-ORIGIN) with where each failure
   class actually routes in the shipped one-edge design, states that adding any edge is a DAG
   version change (not a doc edit), and records the coarse-vs-fine node split as
   considered-and-not-adopted with its operational rationale (linear receipt rollup spine,
   unified evidence sets per node).
3. **D-37 (edit/repair definitions pointer)** — catalog `hard_facts.definitions_note`: the
   normative one-variable-edit and repair-ledger semantics live in the MCP layer
   (HARD_FACTS.json scopes; enforced by avd_r6_generation_execute); the catalog consumes them
   as hard facts. One-stop reading without duplication.
4. **PRODUCTION_CANDIDATE_RECORD inert pointers (L9/L10)** — `baselineRelease` "7.6.0" →
   "8.0.0", `baselineManifest` → the V8_0_0 pin, plus `previousBaseline` naming the V7_6_0
   chain. Fresh-verified inert before editing (locator reads only release/RELEASE.json; no
   validator consumes these fields — grep = 0), so this is record honesty, not behavior: the
   template now describes the current candidate flow truthfully.
5. **Extended erratum (§0.4)** — two audit-evidence corrections recorded: the D-31 "ms band"
   and "+60/−40" transcriptions (corrected in the PHASE 2 entry; original rows stand as
   history; the pin's inherited slip left as-is per the no-rewrite doctrine, this erratum is
   the correction of record), and the V8_SYNTHESIS.md L3 basis line corrected this round
   (22 chunks / 23 outputs, m2 fusion analyzed and credited in the PHASE 1 appendix — the
   deferred correction is now executed).






## PHASE 4 — version semantics 8.0.1, manifest rebuild, dist decision, final report (decision round, complete)

### 4a — T-V801-AUDIT-CORRECTION-LAYER (the version bump)

**Design (the one place full rigor was spent, per the speed directive):** the split-brain
resolution — the tree must DECLARE 8.0.1 or every label reads STALE against the D-42 ladder
(line-2 vs RELEASE.json package version). The bump is ADDITIVE for readability: acceptance
sets GREW to include 8.0.1 alongside 8.0.0; every historical 8.0.0 artifact stays readable;
era records keep era labels. "Do not silently mutate what 8.0.0 was" is preserved by the
V8_0_0 pin (byte record of the as-shipped tree, defects included) — the inverse of this
transform is byte-restore from that pin, which is what makes the bump a migration rather
than an overwrite.

**Executed (transform + hand-finished judgment sites):**

- **L1+L2 labels:** 37 versionMeta-carrying files bumped line-2 `schemaVersion` 8.0.0→8.0.1
  and versionMeta (`ruleVersion` 8.0.1, `producerVersion` @8.0.1, `migratedFrom` "8.0.0");
  head order preserved (schemaVersion, versionMeta first). `_bump_v801.py` aborted mid-run on
  a self-inflicted count literal (PY_EDITS expected 3× gate_dag schemaVersion strings; an
  earlier edit in the same list had consumed the third) — state-checked with
  `_check_state.py`, finished with `_bump_v801_cont.py` (PASS, 10 files). Lesson recorded:
  count-asserting transforms must expect post-edit counts or verify-then-write.
- **L3 RELEASE.json:** version "8.0.1", release "Release 8 — Audit Correction Layer
  (v8.0.1)", regressionCatalog lastId/requiredCount 688→689; baselineManifest still → V8_0_0
  pin (era record, chain intact), previousBaseline → V7_6_0.
- **L4 validators (additive):** EXPECTED_VERSION/EXPECTED_REGRESSION_LAST_ID,
  tree_version/output envelopes, candidate readiness (release/packageVersion/689),
  rollback-plan (fromVersion 8.0.1), gate-DAG (version + envelopes), compile_and_validate
  tuples grew '8.0.1', external/human/manifest evidence sets grew '8.0.1', mcp tool engines
  + contracts envelopes, signal_authority banner, approval-versioning R688b TPL checks
  (8.0.1 + migratedFrom-includes-8.0.0) and its output envelope (self-caught post-suite).
- **L5 suite label:** "V8.0.1-RELEASE-8" (filename intentionally unchanged — era name).
- **Builder:** `bootstrap/build_runtime_manifest.py` now EMITS versionMeta (formalizes the
  D-42 hand-fix that regeneration would otherwise drop) + packageVersion 8.0.1; regenerated
  (34 files, 34/34 hashes verified).
- **Judgment sites the transform could not own:**
  - `templates/MIGRATION_REGISTRY.json`: description v7.x→v8.0.0→v8.0.1; 8.0.1 structural
    fingerprint added (migratedFrom=8.0.0 + the five PHASE 2/3 record keys);
    V801_AUDIT_CORRECTION_LAYER migration entry (source 8.0.0, target 8.0.1, inverse
    T-V801-RESTORE-PINNED-V800 = byte-restore from the pin, era-records note, backlog note);
    v8_to_v801 deterministic field mappings; hybrid rules transition window
    v8.0.0-to-v8.0.1 with reading_v800 ALLOWED (validators retain 8.0.0).
  - `templates/SEMANTIC_REVIEW.json` transformChain appended T-V801-AUDIT-CORRECTION-LAYER
    (priorDeclaredVersions ["7.4.0"] untouched).
  - `dev/REGRESSION_TESTS.md` R689 row (the bump's own regression: label sweep executed as
    transform, builder emits versionMeta, era records exempt, validators additive).
  - `release/PRODUCTION_CANDIDATE_POLICY.json` release 8.0.1 + requiredRegressionLastId 689
    (validator-driven: readiness gate verifies policy↔catalog agreement).
  - `templates/ROLLBACK_PLAN.json` release/fromVersion 8.0.1 (transform touched only line-2 +
    versionMeta; the validator checks in-body fields — self-caught in post-bump sweep).
  - `rules/detailed/36_runtime_activation_compiler.md` §E.1 item 1: declare `schemaVersion
    8.0.1` (LIVE requirement — validator checks it; era-of-addition note added inline).
  - **Live-claim fixes the label sweep cannot see (self-caught, in-body scans):**
    `routing/ACTIVE_MODULE_MANIFEST.json` packageVersion 8.0.1; `mcp/server/
    MCP_SERVER_MANIFEST.json` manifest_version + serverInfo.version + contract-layer
    extension version 8.0.1 (uses manifest_version, not schemaVersion — invisible to the
    D-42 line-2 ladder by format).
- **Era labels left by design (scan-verified):** canary 7.4.0 (immutable detector target),
  PORTABLE_REFERENCE_MANIFEST 7.8.0 lineage, 6 chat-fixture expected contracts 7.8.0,
  the two baseline pins, `_avd_defs`/TOOL_CONTRACT/gate_receipt format consts, mcp
  catalog/registry/facts/vocabulary format versions (content-unchanged format claims),
  all "AVD v8.0.0 …" module-era self-descriptions and `V7.8.0-*`/`V8.0.0-*` gate names
  (same precedent the shipped tree already set), `withheld-in-8.0.0` promotion-lane const
  (era-descriptive data), `contract_version: 8.0.0` in the nine tools (pinned by
  TOOL_CONTRACT schema const — bumping the tools without bumping the schema would fail
  R659), era-of-addition prose ("v8.0.0 additions", "v8.0.0 gate-DAG mode", router table
  annotations, worksheet titles).
- **Sweeps:** full suite 18/18 twice (post-transform and post-judgment-edits; state 91/0,
  DAG 57/0, MCP 141/0, approval+versioning 158/0, signal ALL, canary 7.4.0 intact);
  validate_upgrade_compatibility PASS (ladder green under 8.0.1, chain intact, era records
  exempt — exactly the pin's labelCheckExemptions); validate_candidate_readiness PASS
  (STRUCTURAL_CANDIDATE_PASS; fixed en route: its 688→689 hardcode — the edit needed the
  file's exact leading-space byte, caught via repr dump); json.tool on every hand-edited
  JSON; label scans (37 line-2 sites), in-body field scans, bare-8.0.0 py scans (30 hits,
  all adjudicated keep).

### 4b — package rebuild per binding build order

Executed in the UPDATE_WORKFLOW order, nothing run after the manifest: suite (writes its
results file) → `dev/COMPLETE_PACKAGE_AUDIT.json` refreshed (regenerated by the audit's own
semantics: 309 filesRead/309 utf8, 98 json + 54 py all clean, forbidden residue empty, 52
manuals, 8 mode adapters — the v7-era 243-file counts were stale) → `build_package_manifest.py`
LAST (310 files, self-excluded) → `__pycache__` purge (0 remaining) →
`validate_release_consistency` PASS → in-memory post-build verify (parse OK, 310/310 hashes
CLEAN, pycache CLEAN). Tree is release-shaped: every byte claimed by the manifest matches.

### 4c — dist decision (recorded, era preserved, corrected release shipped)

`v800-dist` = the as-shipped 8.0.0 era record (DISTRIBUTION_MANIFEST schemaVersion 8.0.0,
307 files) — **left byte-untouched**, same doctrine as the V8_0_0 pin: regenerating in place
would silently mutate what shipped. The corrected 8.0.1 release ships as a NEW generation:
`v801-dist` built via `dev/build_distributions.py --zip` from the verified tree (builder
reads RELEASE.json → 8.0.1; writes only to its outdir; deterministic fixed-epoch zips):
portable-core 175 / validation-sdk 203 / combined 310 / cumulative 311, all manifests
declare 8.0.1, zip SHA-256s recorded in the build report. Both generations stand: the era
record proves provenance; v801-dist is the shippable artifact.

### 4d — final report

**Defect disposition (audit D-1…D-50):** all 50 adjudicated; 7 fixed in PHASE 2 (D-9, D-14b,
D-31, D-38, D-39, D-42, D-49), 2 fixed in PHASE 1 (D-19 fact-mirror, D-50 checker
invocation — both verified by fresh execution before/after), 4 records corrected in PHASE 3
(D-28 earned bar, D-23/D-25 feedback/granularity policy, D-37 pointer), and the remainder
carry their audit dispositions (FIX-NEXT/Documented/era) with the PHASE 1 re-adjudication
of the MCP layer folded in (m2 credit recorded; JCS/ASFF-lane conflicts resolved by the
D-14b relabel branch). No audit-row disposition was silently changed.

**Sweep vs corrected baseline:** drift vs the V8_0_0 pin is 65 files — reconciled
one-by-one against the ledgered edit sets (PHASE 1: 3 files; PHASE 2: D-9/D-14b/D-31/D-38/
D-39/D-42/D-49 targets + fixtures; PHASE 3: catalog/DAG/candidate record; PHASE 4a: 37
labels + 15 validators/engines + builders; PHASE 4b: regenerated audit/runtime-manifest/
suite-results). ZERO unexplained drift; ZERO pin paths missing from the tree; the only
tree files absent from the pin are the pin itself, the manifest, and the two D-39 negative
fixtures (added after the pin, ledgered).

**Coverage totals:** full suite 18/18; validators: state 91, gate-DAG 57, MCP 141,
approval+versioning 158, signal authority all-green, upgrade-compat 0 errors,
candidate-readiness STRUCTURAL_CANDIDATE_PASS, release-consistency 0 errors, rollback,
evidence (external/human/manifest) sets grown-additive; 54 py parse clean; 98 json parse
clean; package audit pass; manifest 310/310; pycache 0. The proof boundary is unchanged and
honest: structural and deterministic gates only; the five live-evidence tracks remain
NOT_RUN — nothing in this round upgrades them.

**Erratum & backlog (per speed directive — recorded, not fixed):**
- COMPLETE_PACKAGE_AUDIT.json's v7-era counts were stale in the 8.0.0 ship (243 vs the
  actual 307-tree); refreshing it was already IN scope as PHASE 4b's step 3, so it was
  executed, not backloged.
- `PACKAGE_MANIFEST.json` builder's own head label `schemaVersion: 7.8.0` (format-version
  of the manifest format itself, never bumped for 8.0.0 either; exempt from the D-42
  ladder) — backlog: bump the manifest format version deliberately in a future layer, with
  its own acceptance-set growth.
- `dev/MANIFEST.json` still declares 7.8.0/Release 6 (inert: both suites read only its
  officialGuideSnapshot; shipped that way in 8.0.0) — backlog.
- Nine tool `contract_version: 8.0.0` consts + TOOL_CONTRACT schema const (format claims
  pinned by their own schema; content unchanged) — backlog for a future MCP-layer version
  pass, together with gate_receipt `receipt_version` and the mcp catalog/facts/vocabulary
  format versions.
- Era-of-addition prose kept throughout by doctrine (router table annotations, section
  headings, worksheet titles); the MIGRATION_REGISTRY `backlog_note` records the rule.

**Workspaces:** build tree `D:\New folder (2)\v800-build` (8.0.1, manifest-clean); era dist
`D:\New folder (2)\v800-dist` (untouched 8.0.0 record); new generation
`D:\New folder (2)\v801-dist` (8.0.1, deterministic zips); corpus + synthesis
`D:\New folder (2)\New folder\`; this ledger `D:\New folder (2)\V8_SELF_AUDIT.md`. Temp
tools at `D:\New folder (2)\` root (scan/dump/bump/state/drift/preflight/verify scripts —
`_bump_v801*.py`, `_check_state.py`, `scan_*`/`dump_*`/`_p4b_*`/`_p4c_*`, `_peek_line.py`,
`_tmp_d39/d42/d49_negtest.py`): all one-shot decision-round instruments, kept for
re-verification, none shipped in any distribution.

**Closing state:** the decision round is COMPLETE across all four phases. The 8.0.1 tree is
the audit-corrected release: every defect in the approved scope fixed with ledger entry +
validator + sweep, every record correction in place, version semantics honest (declared =
structural = packaged), the 8.0.0 era preserved byte-exactly in two places (pin + v800-dist),
and the corrected release shipped deterministically as v801-dist.

---

**AUDIT ROUND RECORD: complete — no build files were modified by the audit itself; all dispositions
were presented for the decision round. DECISION ROUND: executing under the approved scope. PHASE 0
(baseline pin + repoint + full sweep) complete. PHASE 1 (MCP re-adjudication + D-19/D-50 fix)
complete. PHASE 2 (FIX-NOW batch: D-9, D-14b, D-31, D-38, D-39, D-42, D-49) — **ALL SEVEN
FIXED, each with ledger entry + validator + full sweep; batch-end before/after table above.**
PHASE 3 (record corrections: D-28 earned bar, D-23/D-25 feedback/granularity, D-37 pointer,
PRODUCTION_CANDIDATE_RECORD pointers, extended erratum + V8_SYNTHESIS basis-line correction) —
**complete.** PHASE 4 (version semantics 8.0.1 via T-V801-AUDIT-CORRECTION-LAYER, package
manifest rebuild per binding order, dist era-preservation + v801-dist generation, final
report) — **complete.** Every change carries a ledger entry, a validator, and a full-sweep
re-run. THE DECISION ROUND IS COMPLETE.**


