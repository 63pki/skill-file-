# v8.0.0 CONSULTATION SYNTHESIS — FIVE DOMAINS

Basis: 23 model outputs across 22 chunks (5 prompts × 4-5 models; the 23rd — prompt-2 model 2 —
was fused into the m1 chunk and initially unanalyzed; it was read and credited in the audit
round's P2 appendix, per V8_SELF_AUDIT.md §0.4 erratum) + 6 agon implementation trees, read
first-hand against the merged v7.8.0 Release 6 tree. No subagent reports were used:
every background analysis agent failed before finishing (15/15); all verdicts below are
from direct reading with line-level citations available in the split files.

---

## CROSS-DOMAIN FINDING (all five prompts converged)

Every domain independently arrived at the same architecture, which is the strongest
possible signal it is correct:

1. **Embedded AVD:STATE markers, not sidecar files** — dual output inside existing
   markdown (P1 m1/m2/m3 all converged; m2 explicitly rejected sidecars: "two
   artifacts drift").
2. **Additive-only patches to the three existing schemas** — no field is moved or
   duplicated; new optional properties + `x-avd` composition annotations.
3. **X14 symmetric enforcement** — unsupported scores rejected in BOTH directions;
   `promotionEligible` written by exactly one code path (five live tracks); approval
   completeness computed but never coupled.
4. **Hard facts as policy constants, capabilities as data** — 720p/3-edit/2-repair
   are AVD *policy*; model capabilities travel with surface/tier/asOf/verifyAtRuntime
   (P1 m3's explicit resolution; echoed by P5 m4's videoPolicySnapshot).
5. **Fail-closed everything** — timeouts DENY, migrations fail closed on
   undeclared loss, STALE fails closed in release mode, no auto-approve path.
6. **Line-2 schemaVersion untouched; line-3 versionMeta/versionEnvelope carries
   ruleVersion/producerVersion/migratedFrom** — preserving the 35-artifact line-2
   convention while adding the producer dimension (P5 m1/m2/m3/m4 all converged).

---

## PROMPT 1 — STATE SERIALIZATION & SCHEMAS

### Verdicts
- **m1 (EXCELLENT)** — additive patches with preconditions per schema edit,
  digestStatus computed/uncomputed discipline, if/then gating, JCS canonicalization,
  AVD:STATE markers `AVD-STATE-<id>`, promotionLane withheld-in-8.0.0. Cleanest
  patch discipline of the entire corpus.
- **m2 (EXCELLENT)** — deepest design: semantic layer compares dated capability
  snapshots vs policy constants ("mismatch produces INSUFFICIENT; it is not silently
  treated as a new capability" L15-20). Rejects sidecar (L9-11 embedded JSON in
  markdown). 3171 lines, most complete EDITS section.
- **m3 (EXCELLENT)** — sharpest Rule-03/HARD-FACTS resolution (L7: "Policy bounds
  (3 edits / 2 repairs) are hardcoded in schemas as AVD policy; every model
  capability ... travels as data with surface/tier/asOf/verifyAtRuntime"). Adds
  artifact_schemas.json catalog entries with hosts arrays. `runtime_load_manifest.
  json.expectedSchemaVersion` as single release-version source of truth.
- **m4 (GOOD)** — envelope-linkage-no-duplication composition mode; `EXAMPLE:`
  digest prefix for examples (nice honesty pattern). Weaker: `https://avd.local/`
  URIs assume external resolution that agents can't do.

### Agon tree (agent_2-16083eb5, 101 files)
Built against stub baselines (v800/baseline/* are 300-900 byte stubs, NOT the real
tree) — its "edited" files must NOT be applied as-is. Its NEW artifacts are strong:
7 artifact schemas + `_avd_defs.schema.json`, 6 positive examples, 5 negative tests
(asset_bad_name, handoff_not_self_describing, receipt_over_budget,
receipt_score_no_evidence, switch_hardcoded_cap), extract_receipt_from_markdown.py,
version_detector.py, validate_state_serialization.py. Example JSONs show line-2
schemaVersion 8.0.0 + digestStatus discipline. Negative tests = ready-made R651+
material.

### Domain decision
**WINNER: m1's patch skeleton + m2's semantic layer + m3's Rule-03 resolution and
catalog hooks + agon's schema/example/negative-test corpus.**
- 5 artifact schemas from agon tree (reviewed, cross-checked against m1/m2 shapes).
- Embedded AVD:STATE marker format: m2's fenced-block with schemaId/version/
  artifactId/path/sha256 (matches agon gate-receipt example).
- digestStatus computed/uncomputed (m1) everywhere a digest appears.
- Capability-vs-policy split: m3 L7 + m2 L15-20, encoded as schema annotations.

---

## PROMPT 2 — MCP TOOL CONTRACTS

### Verdicts
- **m1 (EXCELLENT pre-degeneration)** — packet-in/asset-ref-out boundary, 12 tools,
  3 approval classes (AUTONOMOUS/LEDGERED/HUMAN_APPROVAL), per-clip hash-chained
  budget ledger, `avd-facts` fenced block + `avd-fact-mirror` staleness marker
  (RULE 03 one-source-of-truth), tool_gating by probed capabilities. Tail degenerates
  (~L1700+) — ignore.
- **m3 (EXCELLENT)** — binding-design table (MCP 2025-03-26 + outputSchema, envelope
  compatibility for older clients), avd:// resource URIs, assurance caps per
  distribution, hard_facts block in routing, approval_policy autonomous-list,
  R656 banned-backend probe test. Most complete error/retry design.
- **m4 (GOOD)** — action-discriminator gate tools (one tool per gate, ISSUE/COLLECT/
  LOCK/CHECK actions), claim_boundary block on every result, gate-tier mapping table.
  Sound but less deep than m1/m3.
- **m5 (EXCELLENT)** — file-first contract set: contract JSONs readable as worksheets
  under portable-core (manual fallback = reading the same file), x-avd wire rules
  (_meta["avd"]), structuredContent + content[0].text mirror, error schema as lint
  target R665, hard_facts.json single-source policy.

### Agon tree (agent_2-e5aef16f, 29 files)
Strong and coherent: 9 tool contracts (R2-R7 + validate_gate_evidence +
avd_list_capabilities + avd_request_approval), TOOL_CONTRACT/gate_receipt schemas,
ERROR_CODES.json machine-actionable, HARD_FACTS.json verified faithful (720p/
above-policy/3-edit/2-repair with violation codes AVD-E-4001..4004 + staleness
checker), worksheets per gate, SECURITY_BOUNDARY.json, PROMPT_CATALOG.json.
Matches m5's file-first design almost exactly.

### Domain decision
**WINNER: m3's routing/protocol layer + m1's packet/ledger/security model + m5/agon's
file-first tool contract corpus.**
- HOST_CAPABILITY_ROUTING.json gains `mcp` key (m1 E1 shape, m3 protocol version).
- Tool roster: agon's 9 tools (they cover m1's 12 via action discriminators — m4's
  pattern) + `avd_request_approval` security boundary.
- HARD_FACTS.json from agon, extended with m1's mirror-marker verification.
- Manual fallback: contracts double as worksheets (m5 + agon), PLAN-PASS cap.

### Decision-round appendix (PHASE 1 re-adjudication, all five outputs on the table)
The original P2 verdicts above were written without m2 on the table (m2 was read for the first
time during the v8.0.0 self-audit). Re-adjudicated with m2 present, the built MCP layer's
provenance credit changes: m2 independently proposed the architecture that agon also proposed and
the build adopted. Convergent-idea credit (fresh-verified against the shipped tree, decision
round):

- **I1 sampling-ban** → shipped as `PROMPT_ONLY_CONTROLLER` ("this server never invokes a
  generation backend", `mcp/server/MCP_SERVER_MANIFEST.json` L42).
- **I2 one-result-envelope** → shipped as the TOOL_CONTRACT meta-schema envelope discipline
  (`mcp/schema/TOOL_CONTRACT.schema.json`).
- **I3 no-numbers-in-contracts, tokens + bindings** → shipped as Rule 03 (`x-avd-fact-max` /
  `x-avd-fact-budget` / `hard_fact_bindings`, values resolved at runtime from HARD_FACTS.json).
- **I3b hard-facts digest guard** → hybridized: equality-assertion at validation time
  (validators/check_guide_staleness.py --hard-facts, decision-round D-19 fix) instead of
  digest-pinning.
- **I4 evidence-required scores + not_proven tails** → shipped as X14 discipline (AVD-E-3001/
  3002, evidence_uri required on every Score); agon's claim-boundary prose instead of m2's
  not_proven[]/claim_scope wire tails.
- **I5 FAIL-is-success semantics** → shipped as `retryable: false` on all gate-verdict/
  hard-fact/evidence error classes (mcp/errors/ERROR_CODES.json; only 1003/2003/6002 transient
  classes retryable); no isError wire field needed.
- **HardFactsBinding** → shipped as `hard_fact_bindings` in the contract meta layer (required on
  video-touching tools, R662).
- **gate→validator dispatch** → shipped as `wraps_validators` (validate_gate_evidence.json L123).
- **staleness hooks** → shipped as R672 (validate_mcp_contracts.py); the advertised checker
  invocation was dead as shipped (D-50) and was made executable in the decision round.

Rejected m2 elements, with reasons (adjudicated in the decision round; see V8_SELF_AUDIT.md
PHASE 1): in-schema const-pinning of hard facts (idea 8) — contradicts the runtime-resolution
doctrine the re-adjudication reaffirmed; E_AVD_4xx HTTP-like error numbering — agon's class-grouped
AVD-E-Nxxx shipped and is live; not_proven[]/claim_scope wire tails — agon's X14 + claim-boundary
prose shipped instead; AVD-TR/1 transport receipt — one-envelope achieved via the TOOL_CONTRACT
meta-schema; structuredContent/content[] wire-mirror rule — never shipped (audit rows corrected to
NOT SHIPPED). The original verdicts above stand as the historical record of a 4-output synthesis;
this appendix is the 5-output correction.

---

## PROMPT 3 — GATE DAG

### Verdicts
- **m1 (EXCELLENT)** — the formal strongest: gate-DAG owned by 35, admission
  projection to 39's STEP QUEUE (OPEN ≠ ACTIVE), ASYNC_EXTERNAL nodes consume no
  ACTIVE slot (client approval ∥ technical QA), epoch-keyed feedback edges make the
  unrolled graph a DAG by construction, cohort batching reuses 39 §6, 28/39
  consolidation explicitly NOT reopened. Verbatim quote check: L27 "The deferred
  28/39 consolidation is NOT reopened... 36 §E is extended, not rewritten."
- **m3 (GOOD)** — "Gate Execution Plan (GEP)" above rule 39; compatible but less
  formal; worth mining for per-gate timing/trigger tables.
- **m4 (WEAK-GOOD)** — shorter; parallel-group coordination ideas.
- **m2 (DEGENERATE)** — 7-line repetition loop, no content.
- Agon tree (agent_1-795f4e37) — 35_gate_dag_v800.json is a sound simplified m1:
  correct gate names R0-R8 (+R7.TECH/R7.CLIENT, R8.TECH/R8.CLIENT sub-gates),
  720p flags on R0/R1, repair budget metadata on R4, FB-R6-R4-DRIFT feedback with
  max_iterations 2 + preserve/reset lists + escalation BLOCK, SKIP-R4-MOTION /
  SKIP-R4-NO-CHARACTERS with state_snapshot_required, EARLY-R5-AUDIO early-start,
  PAR-R3-R4 + PAR-R7-SUB + PAR-R8-SUB coordination, deadlock invariants I1-I4,
  dag_state handoff serialization, predicate_schema allowed_fields +
  forbidden_patterns. Its rule-file rewrites are stubs (35 lines vs real) — use its
  §E extension list (6 checks) as the pattern for extending the real 36.

### Domain decision
**WINNER: m1's architecture (epoch formalism, OPEN≠ACTIVE, ASYNC_EXTERNAL) with
agon's DAG JSON as the concrete starting artifact (upgraded with m1's epoch-keyed
feedback semantics + ASYNC_EXTERNAL for R7.CLIENT/R8.CLIENT and finer node split
R0a/R0b, R1a/R1b, R6a/R6b).**
- 36 §E extension: agon's six validation checks (DAG presence, gate-to-step mapping,
  feedback bounds, predicate schema, deadlock invariants, dag_state serialization)
  appended to the real 36 §E.
- 00a_router.md: add 35_gate_dag_v800.json to 35's load set (one line).

---

## PROMPT 4 — QUALITY SIGNALS & DIAGNOSTIC MATRIX

### Verdicts
- **m1 (EXCELLENT)** — three authority classes (A DETERMINISTIC may auto-fail;
  B PERCEPTUAL-CALIBRATED candidate-fail needs human, unreachable in v8.0.0; C
  PERCEPTUAL-PROVISIONAL advisory-only — ALL perceptual ship as Class C now),
  X14 symmetric (L16: "An unsupported 9/10 is rejected — and so is an unsupported
  3/10 used to block work"), thresholds as intervals with calibration_status
  CALIBRATION_REQUIRED + promotion criterion (AUC ≥ 0.75, n ≥ 150), cost_tier =
  max(generation_tier, labor_tier) rule making short-motion-proof the only HIGH →
  escalation ladder structurally cannot auto-authorize video generation, diagnostics
  never touch delivery budgets (promotable: false, separate ledger).
- **m2 (EXCELLENT)** — weighted-geometric-mean composite dropping missing signals
  (conservative on evidence), abstract spend units LOW=1/MED=3/HIGH=8, D07→D08
  escalation documented (no MED in sound/edit family), evaluator ≠ generator
  (L18-19: "Nano Banana Pro and Gemini Omni Flash cannot self-score into a
  receipt"), explicit cut-list (FID/IS/FVD/CLIP-R as required signals, learned
  gate-pass classifier, per-frame exhaustive aesthetic, parallel catalog, auto-fail
  on composite, any MEASURED status, any promotionEligible:true).
- **m3 (EXCELLENT)** — calibration-only mode, null not invented values,
  gate_pass_probability stays null until calibration, UNAVAILABLE with reason
  (never guessed), provider fingerprint invalidation on drift, reliability-weighted
  composite (no naive average).
- **m4 (GOOD)** — signal_catalog.json + diagnostic_matrix.json as the two machine
  sources of truth; UNCALIBRATED global tier with tier_rule; NOT_MEASURED on
  provider absence = graceful degradation; BU budget unit.
- **m5 (WEAK-GOOD)** — provider-abstraction Python with X14 honesty-guard interface
  (UnsupportedMetricError, return None never fabricate); useful interface sketch
  but thin on catalogs/thresholds.

### Agon trees
- **agent_2-19303081 (STRONG)**: QUALITY_SIGNALS_CATALOG.json (406 lines: 8 signals
  with formulas, provisional typical ranges, providers, surfaces, confidence
  methods, hard_facts blocks, limitations) + DIAGNOSTIC_MATRIX.json + LIVE_EVIDENCE_
  EXECUTION.md + signal_schema.json + signal_provider_interface.py + phase_b_quality
  .py (42KB) + EDITS_MANIFEST.md. Honest banners throughout. **DEFECT: its
  LIVE_EVIDENCE_STATUS.json replaced the five real tracks (liveCrossModelReplay,
  nanoOmniABGeneration, completeProductionPilot, beginnerOperatorPilot,
  audienceComprehensionReview) with invented T1-T5 signal tracks — REJECTED;
  build must extend the real tracks, add signal-calibration as a SEPARATE section,
  not replace.** Also cites "Rule 38 §3" for threshold rejection where real 38 §3
  is "Same standard, different workload" — citation error, doctrine itself is
  correct and lives in CROSS_MODEL_TESTS X14.
- **agent_1-c683d8cd (WEAKER)**: .docx design (unparseable in pipeline), smaller
  catalogs, similar tracks-replacement defect expected (LIVE_EVIDENCE_STATUS edit).

### Domain decision
**WINNER: m1's authority classes + escalation structure, m2's composite + cut-list
as policy, m3's null-discipline, agon-19303081's catalog content (with the track
defect repaired: real five tracks preserved; signal calibration state added as
new keys, T1-T5 renamed as calibrationSubtracks under each real track's signal
scope or as a separate calibration section).**
- Diagnostics extend rule 35 §6's 8 items with cost/tier/budget/duration/escalation
  (agon matrix does this; verify no 9th diagnostic invented — check during build).
- Every threshold row: status CALIBRATION_REQUIRED (m1) / UNCALIBRATED tier_rule
  (m4); typical_range_provisional bands (agon); calibration procedure pointer.

---

## PROMPT 5 — STAKEHOLDER APPROVAL & VERSION MIGRATION

### Verdicts
- **m1 (EXCELLENT)** — 9-decision table: additive approval block on 35 §4 receipt +
  hash-chained ledger in 19; dimension-owned vetoes (HARD/SOFT, not total ordering —
  "legal overruling taste" absurdity argument L14); timeouts never approve (HOLD →
  escalation → project hold, CONDITIONAL with open conditions block R8);
  approvals bind to (gate, artifact sha256[]) not sessions/models — model switch
  invalidates only technical_qa at R5/R6; D5 schemaVersion line-2 + versionEnvelope
  line-3; D6 migration registry declarative ops KEEP/ADD/RENAME/MOVE/RETIRE/COMPUTE
  with declared inverses, RETIRE = MOVE→legacy.retired.<path>+{reason,successor} =
  exact retiredPaths shape; D7 SEMANTIC_REVIEW repair with structural-diff gate +
  tree-wide label check making the defect class unrepeatable; D8 agents-first
  rollout (v8 migrates on read, refuses FUTURE, never writes 7.8.0); D9 single
  promotionEligible writer + promotionEligibleInfluence: NONE on every approval
  artifact.
- **m2 (EXCELLENT)** — deepest: 4-tier version-detection ladder ending in
  structural fingerprint ("declared ≠ inferred is a hard failure" — the only
  mechanism that catches the shipped 7.4.0 defect); lossCapsule (canonical pre-image
  + digest) for non-exactly-invertible ops; hash-chained APPROVAL_LEDGER.json +
  rule 19 carry_forward_invariant class (R668); typed veto classes ABSOLUTE_LEGAL >
  ABSOLUTE_TECHNICAL_HARDFACT > ABSOLUTE_COMMERCIAL_SCOPE > OVERRIDABLE_CREATIVE
  (two absolute vetoes → BLOCKED, no override, only scope change back to R0/R1);
  default-DENY with no auto-approve path anywhere (R696 fuzz test).
- **m3 (EXCELLENT)** — role-scoped resumable overlay on 35 §4 receipt (approvedBy
  remains rollup); version triple; reset-exempt approvalState in rule 19 handoff;
  evidence segregation with visibility ACLs; dual-read/v8-write/migrate-on-read
  hybrid window; proxy-after-expiry rejected → PENDING; explicit cut list.
- **m4 (EXCELLENT)** — videoPolicySnapshot object (touches_video, 720p + R0/R1
  flags, edit_cap/edits_used, repair_budget/repairs_used, capability_snapshot_ref)
  with migration-never-defaults-flags invariant; versionMetadata snake_case with
  schema_version must-equal-schemaVersion redundancy detector.
- **m5 (GOOD with one slip)** — GATE_APPROVAL_LEDGER hash-pointer segregation;
  D6 transform algebra "lossless ≡ inverse replay reproduces preMigrationSha256";
  D7 line-2 + expectedVersions cross-check; D10 DEFAULT DENY; D11 hard facts
  schema-required; D12 delegation depth-1 forward-only revocation. **SLIP: E2 says
  "entire file. Replace with" for MIGRATION_RECORD.json — prime-directive violation
  (must be append); everything else in m5 is additive.**

### Agon tree (agent_1-26295442)
Mixed: ROLE_REGISTRY.json + MIGRATION_REGISTRY.json + APPROVAL role matrix content
usable as reference, but its SEMANTIC_REVIEW.json breaks line-2 convention ($schema
at line 2, schemaVersion at line 3) and ships invented template scores (0.98/0.95
with evidence_ref stubs) — REJECT that file; its baseline-hashes file is a 2KB stub
(not the real 293-file baseline); its rule 19/21/24/35 files are stubs. Take its
registry JSONs as content reference only.

### Domain decision
**WINNER: m1's decision table as spine + m2's detection ladder/lossCapsule/typed
vetoes + m3's overlay shape + m4's videoPolicySnapshot.**
- Approval: additive roleApprovals[] on 35 §4 receipt (m3), approvals bind to
  (gate, artifact hashes) (m1 D4), hash-chained ledger (m2 D4), typed veto classes
  (m2 D5), default-DENY timeouts (all), delegation depth-1 (m5 D12).
- Version: line-2 untouched + line-3 versionMeta (m2's field set incl.
  structuralFingerprint), 4-tier detection ladder, lossCapsule on lossy ops.
- Migration: declarative op registry with inverses (m1 D6 / m5 D6), SEMANTIC_REVIEW
  repaired via identity-content transform with MIGRATION_RECORD entry (m5's E1
  two-step is the honest pattern: 7.4.0→7.8.0 alignment first, then 8.0.0 bump),
  tree-wide stale-label check R651-class + immutable canary fixture.
- videoPolicySnapshot on every video-touching approval/migration artifact (m4).

---

## BINDING BUILD ORDER (respects coupling)

1. **Phase 0 — defect fixtures**: repair templates/SEMANTIC_REVIEW.json (two-step),
   add canary fixture test/canary/stale_version_template.json (7.4.0 forever) so
   the detector has a permanent target.
2. **Phase 1 — schemas (P1)**: _avd_defs + 5 artifact schemas + 3 contract-schema
   additive patches + artifact_schemas.json catalog entries + version_detector.py
   + validate_state_serialization.py + examples + negative tests. Gate: existing
   validate_contract_schema.py passes; new validators pass.
3. **Phase 2a — DAG (P3)**: 35_gate_dag_v800.json (agon base + m1 semantics) + real
   36 §E extension (6 checks) + 00a one-line load + 35 §4.9 receipt→DAG state block +
   19 handoff dag_state. Gate: 36 §E still fails without STEP QUEUE; 39 untouched.
4. **Phase 2b — MCP (P2)**: mcp/ tree (contracts, schemas, HARD_FACTS, ERROR_CODES,
   worksheets) + routing mcp key + manifest entries. Gate: no tool references a
   banned backend; HARD_FACTS values match avd-facts; portable-core = no Python
   required to READ contracts.
5. **Phase 3 — signals (P4)**: signal catalog + diagnostic matrix (35 §6 extension)
   + phase_b_quality.py honesty guards + LIVE_EVIDENCE extension preserving the
   five real tracks. Gate: R-checks "threshold-as-measured rejected", "unsupported
   score rejected", "no parallel catalog".
6. **Phase 4 — approval/versioning (P5)**: roleApprovals[] on 35 §4 + ledger +
   carry_forward_invariant in 19 + videoPolicySnapshot + versionMeta line-3 sweep
   (35 artifacts) + migration registry. Gate: approval never writes
   promotionEligible; CONTROLLED reset never touches approvalState.
7. **Phase 5 — suite**: extend dev/run_v780_release6_tests.py with R651+ (numbering
   from the real suite's last check), run everything, binding-order rebuild.

## DEFECT LEDGER (from consultation + agon trees; carry into build)
- D-1 agon-P4 replaced the five real live tracks → build restores them.
- D-2 agon-P4 mis-cites Rule 38 §3 → cite CROSS_MODEL_TESTS X14 instead.
- D-3 agon-P5 SEMANTIC_REVIEW breaks line-2 convention + invented scores → reject
  file, keep registries as reference.
- D-4 agon trees' "edited" files are stubs → never apply as-is; extend real files.
- D-5 p5_m5 E2 "replace entire file" → convert to append.
- D-6 p2_m1 degenerate tail → content up to degeneration only.
- D-7 all agon baseline-hash files are 2KB stubs → v8 baseline must be generated
  from the real tree (293+ files, retiredPaths pattern).
