# V7.2 Deterministic Execution Tests

The three V7.1 Milo runs are encoded as failure fixtures. They verify tool substitution, missing artifacts/world rules, anatomy/face drift, and timing contradictions. These fixtures are concise evidence records, not claimed full-model replays.

The fixtures are executed by the bundled release suite: `python3 dev/run_v780_release6_tests.py` runs the `regression-fixture-coverage` check, which feeds every `tests/fixtures/*_contract.json` / `*_output.json` pair through `validators/validate_project.py` and asserts that the error codes declared in the matching `*_expected.json` are produced (and that the declared `forbiddenErrorCodes` are not). There is no separate `run_v72_tests.py`; that runner was consolidated into the release suite and this reference previously pointed at a file that did not ship.

Each `*_expected.json` declares `expectedErrorCodes` (defect classes the fixture must still trigger) and `forbiddenErrorCodes` (defects the fixture must not accidentally trigger). Fixtures are pinned to `schemaVersion` 7.8.0: if the contract schema advances again, the fixtures must be migrated in the same change, or the validator short-circuits on `CONTRACT_FIELD` and the suite silently stops testing anything.

A live replay still requires exact prompts, model/runtime capture, complete outputs, and media evidence where applicable.
