# V7.4 Phase D Assurance Bootstrap

## Verified Runtime

1. Create the minimal Routing Contract.
2. Run `python3 bootstrap/bootstrap_runtime.py ROUTING_CONTRACT.json --outdir SESSION_DIR`.
3. Inject the complete `RUNTIME_CONTEXT.md`.
4. Compile the full Project Contract and copy the routing hash from the preload receipt.
5. Run `python3 bootstrap/finalize_contract_binding.py ROUTING_CONTRACT.json PROJECT_CONTRACT.json SESSION_DIR/PRELOAD_RECEIPT.json --outdir SESSION_DIR`.
6. Use `FINAL_RUNTIME_MARKER.txt` in the output and `FINAL_RUNTIME_RECEIPT.json` during validation.

Routing drift, project-contract drift, hash failure, missing triggers, or missing challenge proof blocks Verified Runtime.

## Portable Assurance

When execution or receipt retention is unavailable, use Portable Assurance for text planning only. It is visibly unverified and capped at PLAN-PASS. It cannot claim deterministic PASS, generated/inspected media, audience evidence, or RELEASE-PASS.

Verified Runtime proves context availability, byte integrity, final-contract binding, and response linkage—not private cognitive attention or instruction compliance.
