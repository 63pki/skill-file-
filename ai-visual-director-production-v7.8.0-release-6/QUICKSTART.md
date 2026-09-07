# QUICKSTART — V7.8.0 Release 6

## Read this first: which distribution you have

The steps below are not all available in every distribution. Check before you start.

| You installed | Python tools present? | Highest assurance you can claim |
| --- | --- | --- |
| `portable-core` | **No** — prompt and rule content only | `PLAN-PASS` under `PORTABLE_REFERENCE` |
| `combined` | Yes | `VERIFIED_RUNTIME` |
| `cumulative` | Yes | `VERIFIED_RUNTIME` |
| `validation-sdk` | Yes, but it is an add-on to `portable-core`, not standalone | `VERIFIED_RUNTIME` when paired |

If you hold `portable-core`, **skip every step that begins with `python3`** and follow *Portable Assurance* instead. Do not report a runtime receipt, a validator result, or a hash you did not actually produce.

## Verified Runtime

Requires `combined`, `cumulative`, or `portable-core` + `validation-sdk`.

1. Fill `templates/ROUTING_CONTRACT.json`.
2. Run `python3 bootstrap/bootstrap_runtime.py ROUTING_CONTRACT.json --outdir SESSION_DIR`.
3. Inject `SESSION_DIR/RUNTIME_CONTEXT.md` completely.
4. Compile the full Project Contract from `templates/PROJECT_CONTRACT.json` and set its `routingContractSha256` from the preload receipt.
5. Run `python3 bootstrap/finalize_contract_binding.py ROUTING_CONTRACT.json PROJECT_CONTRACT.json SESSION_DIR/PRELOAD_RECEIPT.json --outdir SESSION_DIR`.
6. Copy the final runtime marker into the actual output.
7. Validate with `python3 validators/compile_and_validate.py PROJECT_CONTRACT.json RESPONSE.md --runtime-receipt SESSION_DIR/FINAL_RUNTIME_RECEIPT.json`.

## Portable Assurance

The only path available under `portable-core`. Use `templates/PROJECT_CONTRACT_PORTABLE.json` when verified execution is unavailable. Show `ASSURANCE: PORTABLE · RUNTIME NOT CRYPTOGRAPHICALLY VERIFIED · VALIDATOR NOT EXECUTED`; maximum PLAN-PASS. Do not claim generated, inspected, approved, or released media without real evidence.

## Phase C operator flow

1. Set `qualityPolicy` and `usabilityProfile` in the Project Contract.
2. Author each required artifact with acceptance, repair action, stable IDs, and executable steps.
3. If Python is available, run `compile_and_validate.py`; inspect compact `STATUS.txt`, then `REPAIR_PLAN.json`. If it is not, perform the same acceptance checks by hand and record `VALIDATOR NOT EXECUTED`.
4. Run the separate semantic review and pass it with `--semantic-review` when evidence is available.
5. Never turn an unavailable creative/media dimension into a numeric score.

## Phase D external evidence

Requires Python tools.

1. Copy `templates/EXTERNAL_EVIDENCE_CAMPAIGN.json`.
2. Register each real external run with provider/model/version, prompt hash, response/media path and hash, execution date, operator, and `LIVE_EXTERNAL`.
3. Add blind independent rating records without exposing variant labels.
4. Run `validate_external_evidence.py CAMPAIGN.json --root EVIDENCE_ROOT`.
5. Never relabel synthetic fixtures or dry runs as live evidence.

## Maintainers

`dev/UPDATE_WORKFLOW.md` is shipped in `combined` and `cumulative` only. It is not part of the operator flow and is absent from `portable-core` by design.
