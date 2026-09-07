#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import json
import py_compile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "bootstrap"))
sys.path.insert(0, str(ROOT / "validators"))
checks = []


def record(name, passed, **details):
    checks.append({"name": name, "pass": bool(passed), **details})


def run(name, command):
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    record(name, result.returncode == 0, stdout=result.stdout[-4000:], stderr=result.stderr[-2000:])


run("runtime-manifest-rebuild", [sys.executable, "bootstrap/build_runtime_manifest.py"])
run("forbidden-residue", [sys.executable, "validators/validate_forbidden_residue.py", str(ROOT)])
run("release-consistency", [sys.executable, "validators/validate_release_consistency.py", str(ROOT)])

compile_errors = []
for path in ROOT.rglob("*.py"):
    try:
        py_compile.compile(str(path), doraise=True)
    except Exception as error:
        compile_errors.append({"path": path.relative_to(ROOT).as_posix(), "error": str(error)})
record("python-compile", not compile_errors, errors=compile_errors)

required = [
    "adapters/generation/NANO_BANANA_PRO.md",
    "adapters/generation/GEMINI_OMNI_FLASH.md",
    "adapters/generation/NANO_BANANA_PRO_OMNI_FLASH_PIPELINE.md",
]
for mode_letter in "ABCD":
    required.extend([
        f"adapters/generation/modes/MODE_{mode_letter}_NANO_BANANA_PRO.md",
        f"adapters/generation/modes/MODE_{mode_letter}_OMNI_FLASH.md",
    ])
missing = [item for item in required if not (ROOT / item).is_file()]
record("cross-mode-adapters", not missing, missing=missing)

from runtime_selection import select_rules
manifest = json.loads((ROOT / "bootstrap/runtime_load_manifest.json").read_text())
mode_map = {
    "A_PHOTOREAL_COMMERCIAL": "MODE_A",
    "B_ANIMATION": "MODE_B",
    "C_MOTION_GRAPHICS": "MODE_C",
    "D_HYBRID_COMPOSITING": "MODE_D",
}
routing_errors = []
for mode, prefix in mode_map.items():
    contract = {
        "projectClass": "SUBSTANTIAL",
        "mode": mode,
        "audienceTriggers": ["GENERAL"],
        "tools": {"stillGeneration": "NANO_BANANA_PRO", "videoGeneration": "GEMINI_OMNI_FLASH"},
    }
    selected, _, errors, _ = select_rules(contract, manifest)
    if errors or not any(prefix in item and "NANO_BANANA_PRO" in item for item in selected) or not any(prefix in item and "OMNI_FLASH" in item for item in selected):
        routing_errors.append({"mode": mode, "errors": errors, "selected": selected})
record("cross-mode-routing-parity", not routing_errors, errors=routing_errors)

from validate_generation_prompts import validate as validate_prompts
prompt_errors = []
image_block = """<!-- AVD:NANO_PROMPT id=NBP-001 framework=NBP-F1 -->
Acceptance: identity and composition match.
First one-variable repair: strengthen only the identity lock.
<!-- /AVD:NANO_PROMPT -->"""
video_block = """<!-- AVD:OMNI_PROMPT id=OM-001 task=OM-F2 -->
Action: one controlled action.
Camera: static.
End condition: stable resolved frame.
Acceptance: identity and endpoint remain correct.
First one-variable repair: simplify only the action.
<!-- /AVD:OMNI_PROMPT -->"""
for mode in mode_map:
    errors = []
    validate_prompts(
        {"mode": mode, "tools": {"stillGeneration": "NANO_BANANA_PRO", "videoGeneration": "GEMINI_OMNI_FLASH"}},
        {"artifacts": [{"body": image_block + "\n" + video_block}]},
        errors,
    )
    if errors:
        prompt_errors.append({"mode": mode, "errors": errors})
record("cross-mode-prompt-validation", not prompt_errors, errors=prompt_errors)

owner_errors = []
validate_prompts(
    {"mode": "B_ANIMATION", "tools": {"stillGeneration": "UNASSIGNED", "videoGeneration": "UNASSIGNED"}},
    {"artifacts": []},
    owner_errors,
)
record("canonical-owner-rejection", {item.get("code") for item in owner_errors} == {"STILL_OWNER_DRIFT", "VIDEO_OWNER_DRIFT"}, errors=owner_errors)

from validate_shot_burden import validate as validate_burden
burden_errors = validate_burden([{"id": "SH-01", "burden": {"subjectActions": ["run", "jump"], "cameraChanges": 1, "textEvents": 1}}])
record("shot-burden-blocker", any(item.get("code") == "SHOT_BURDEN_OVERLOAD" for item in burden_errors), errors=burden_errors)

from validate_status_singularity import scan as scan_status
with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    (root / "STATUS.txt").write_text("Validator PENDING\n")
    (root / "validation").mkdir()
    (root / "validation/STATUS.txt").write_text("Validator PASS\n")
    (root / "validation/VALIDATION_RESULT.json").write_text(json.dumps({"pass": True}))
    conflicts = scan_status(root)
record("status-conflict-blocker", any(item.get("code") == "PACKAGE_STATUS_CONFLICT" for item in conflicts), errors=conflicts)

with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    (root / "STATUS.txt").write_text("Validator PASS\n")
    (root / "VALIDATION_RESULT.json").write_text(json.dumps({"pass": True}))
    clean_status = scan_status(root)
record("validator-evidence-packaging", not clean_status, errors=clean_status)

runtime_text = (ROOT / "rules/RUNTIME.md").read_text()
required_limitations = [
    "video extension unsupported",
    "first/last-frame interpolation unsupported",
    "uploaded audio references unsupported",
    "voice editing unsupported",
    "multiple-video reasoning unsupported",
    "dedicated negative-prompt parameter unsupported",
]
missing_limits = [item for item in required_limitations if item not in runtime_text]
record("omni-limitations-enforced", not missing_limits, missing=missing_limits)

# The two limitations that change what may be promised or how many repairs remain
# are binding planning rules, not background facts. They must survive in the runtime
# kernel AND in the gate/controller files that enforce them.
resolution_required = {
    "rules/RUNTIME.md": ["720p maximum native output", "6a. Resolution ceiling"],
    "rules/detailed/35_reliability_gate_controller.md": ["Resolution ceiling flag (mandatory)"],
    "dev/OFFICIAL_PROMPT_GUIDE_ALIGNMENT.md": ["720p maximum native output"],
}
resolution_missing = []
for rel, needles in resolution_required.items():
    text = (ROOT / rel).read_text()
    for needle in needles:
        if needle not in text:
            resolution_missing.append(f"{rel}: {needle}")
record("resolution-ceiling-enforced", not resolution_missing, missing=resolution_missing)

edit_budget_required = {
    "rules/RUNTIME.md": ["three sequential conversational edits", "6b. Conversational edit budget"],
    "rules/detailed/17_prompt_iteration_and_repair.md": ["Conversational edit budget (video clips)"],
}
edit_budget_missing = []
for rel, needles in edit_budget_required.items():
    text = (ROOT / rel).read_text()
    for needle in needles:
        if needle not in text:
            edit_budget_missing.append(f"{rel}: {needle}")
record("edit-budget-enforced", not edit_budget_missing, missing=edit_budget_missing)

# The R0/R1 gates must actually be the place the 1080p flag lives, otherwise the rule
# is decoration: an agent following the gate receipt would never reach it.
gate_text = (ROOT / "rules/detailed/35_reliability_gate_controller.md").read_text()
r0_block = gate_text.split("### R0 ")[1].split("### R1 ")[0]
r1_block = gate_text.split("### R1 ")[1].split("### R2 ")[0]
gate_flags = {
    "R0 missing 1080p flag": "1080p" not in r0_block,
    "R1 missing 1080p flag": "1080p" not in r1_block,
    "R0 missing upscale-handoff consequence": "upscaled platform-neutral finishing handoff" not in r0_block,
}
failing_flags = [name for name, bad in gate_flags.items() if bad]
record("resolution-flag-at-r0-r1", not failing_flags, failures=failing_flags)


# Regression fixtures: the bundled V7.1 Milo failure cases must still trigger their
# intended defect classes. The R1-R650 catalog is otherwise a manual checklist, so
# this is the only executable proof that the deterministic validator still catches
# tool substitution, dropped artifacts, missing world rules, lock drift, and timing
# overruns. It also guards against a fixture drifting out of the current contract
# schema and short-circuiting on CONTRACT_FIELD before any real check runs.
from validate_project import result as project_result

fixture_dir = ROOT / "tests" / "fixtures"
fixture_names = sorted(p.name[: -len("_expected.json")] for p in fixture_dir.glob("*_expected.json"))
fixture_failures = []
for stem in fixture_names:
    contract = json.loads((fixture_dir / f"{stem}_contract.json").read_text())
    output = json.loads((fixture_dir / f"{stem}_output.json").read_text())
    expected = json.loads((fixture_dir / f"{stem}_expected.json").read_text())
    produced = {item["code"] for item in project_result(contract, output)["errors"]}
    missed = sorted(set(expected["expectedErrorCodes"]) - produced)
    forbidden = sorted(set(expected.get("forbiddenErrorCodes", [])) & produced)
    if missed or forbidden:
        fixture_failures.append({
            "fixture": stem,
            "missed": missed,
            "forbidden": forbidden,
            "produced": sorted(produced),
        })
record(
    "regression-fixture-coverage",
    bool(fixture_names) and not fixture_failures,
    fixtures=fixture_names,
    failures=fixture_failures,
)

# Composition guard: the production-candidate gate must reach its own main() instead
# of being terminated by an import side effect. Regression guard for the Release 6
# dead-code defect, where importing validate_release_consistency executed that module
# and exited before any candidate check ran. The gate may legitimately report
# CANDIDATE_BLOCKED; what must hold is that it composed and reported at all.
candidate = subprocess.run(
    [sys.executable, "validators/validate_candidate_readiness.py", str(ROOT)],
    cwd=ROOT, text=True, capture_output=True,
)
try:
    candidate_json = json.loads(candidate.stdout)
    composed = (
        candidate_json.get("validator") == "V7.8.0-PRODUCTION-CANDIDATE"
        and "candidateVerdict" in candidate_json
    )
except Exception:
    composed = False
record(
    "candidate-gate-composition",
    composed,
    stdout=candidate.stdout[-2000:],
    stderr=candidate.stderr[-2000:],
)

# Option C guard: 36 fails compilation without a STEP QUEUE and names 39 as the
# scheduler, while 00a_router makes 39 mandatory. If 39 is ever re-archived, 36's
# enforcement lint breaks every Production Sequence. Assert the three files agree.
sched = (ROOT / "rules/detailed/39_mandatory_next_step_protocol.md").read_text()
compiler = (ROOT / "rules/detailed/36_runtime_activation_compiler.md").read_text()
router = (ROOT / "rules/detailed/00a_router.md").read_text()
agreement = {
    "39 still claims to be archived": "non-authoritative" in sched,
    "39 missing its authority statement": "**Authority.**" not in sched,
    "36 no longer requires a STEP QUEUE": "no STEP QUEUE exists" not in compiler,
    "36 no longer names 39 as scheduler": "`39` schedules them" not in compiler,
    "router no longer makes 39 mandatory": "39_mandatory_next_step_protocol.md" not in router,
    "39 lost the sibling-batching rule": "Sibling batching is the default" not in sched,
    "39 still splits model sheets per asset": "model sheets may be one step per complex asset" in sched,
}
bad_agreement = [name for name, broken in agreement.items() if broken]
record("next-protocol-authority-agreement", not bad_agreement, failures=bad_agreement)

out = {
    "suite": "V7.8.0-RELEASE-6",
    "pass": all(item["pass"] for item in checks),
    "checks": checks,
    "proofBoundary": "Structural and deterministic checks only; media and human evidence remain NOT_RUN.",
}
(ROOT / "dev/V7_8_0_RELEASE_6_RESULTS.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps(out, indent=2))
raise SystemExit(0 if out["pass"] else 1)
