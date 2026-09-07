# Cross-Model Execution Compliance

This workflow is user-authorized production guidance. It never asks a model to replace system instructions, change identity, hide actions, bypass safety, or obey instructions embedded in project content. Higher-priority instructions remain controlling.

## Required observable sequence

1. `ROUTE` — compile the Routing Contract.
2. `LOAD` — select and hash-verify the active files.
3. `CONTRACT` — compile the Project Contract.
4. `EXECUTE` — create only authorized artifacts.
5. `EXTRACT` — extract actual output rather than trusting declarations.
6. `VALIDATE` — run deterministic validation.
7. `PACKAGE` — build the indexed, manifested package.
8. `REPORT` — report machine status without inflated claims.

Before execution, copy `templates/INSTRUCTION_COMPLIANCE_RECEIPT.json`. Record provider, model, version, selected file hashes, and step artifacts. `PENDING` never passes. A file may be marked `LOADED` only when its bytes were actually available to the execution context. A step may be `COMPLETE` only after its named artifact exists.

Run:

```text
python3 validators/validate_instruction_compliance.py INSTRUCTION_COMPLIANCE_RECEIPT.json PROJECT_CONTRACT.json
```

Then pass the receipt to `compile_and_validate.py` with `--instruction-receipt`. Missing or invalid receipt blocks extraction. This validates declared, hash-bound observable artifacts; it cannot prove private cognitive attention, reasoning, honesty, or future behavior.

## Clean archive gate

Run `validators/validate_clean_zip.py RELEASE.zip --checksum RELEASE.zip.sha256 --run-tests`. A passing archive has one root, no traversal, symlinks, duplicate-case paths, caches, temporary files, or missing canonical files. Every bundled deterministic suite must pass from fresh extraction with results written outside the release tree. This is not live cross-model evidence.
