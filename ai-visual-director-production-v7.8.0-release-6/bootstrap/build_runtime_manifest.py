#!/usr/bin/env python3
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
profiles = {
    "SUBSTANTIAL": ["SKILL.md", "rules/CORE_CONTROLLER.md", "rules/RUNTIME.md"],
    "QUICK_SHOT": ["SKILL.md", "rules/CORE_CONTROLLER.md"],
}
base = "rules/production/AUDIENCE_SUITABILITY.md"
audiences = {
    "GENERAL": [base],
    "CHILDREN": [base, "rules/audience/CHILDREN_6_9.md"],
    "CHILDREN_6_9": [base, "rules/audience/CHILDREN_6_9.md"],
    "EXPERT": [base, "rules/audience/EXPERT_TECHNICAL.md"],
    "VULNERABLE": [base, "rules/audience/VULNERABLE_AUDIENCES.md"],
    "ACCESSIBILITY": [base, "rules/audience/ACCESSIBILITY.md"],
    "MULTILINGUAL": [base, "rules/audience/MULTILINGUAL.md"],
    "REGULATED": [base, "rules/audience/REGULATED_CLAIMS.md"],
}
shared = [
    "adapters/generation/NANO_BANANA_PRO.md",
    "adapters/generation/GEMINI_OMNI_FLASH.md",
    "adapters/generation/NANO_BANANA_PRO_OMNI_FLASH_PIPELINE.md",
    "rules/production/POST_PRODUCTION_HANDOFF.md",
    "rules/production/AUDIO_CAPTION_HANDOFF.md",
]
modes = {
    "A_PHOTOREAL_COMMERCIAL": ["rules/production/MODE_A_PHOTOREAL_COMMERCIAL.md"] + shared + ["adapters/generation/modes/MODE_A_NANO_BANANA_PRO.md", "adapters/generation/modes/MODE_A_OMNI_FLASH.md"],
    "B_ANIMATION": ["rules/production/2D_ANIMATION.md"] + shared + ["adapters/generation/modes/MODE_B_NANO_BANANA_PRO.md", "adapters/generation/modes/MODE_B_OMNI_FLASH.md"],
    "C_MOTION_GRAPHICS": ["rules/production/MODE_C_MOTION_GRAPHICS.md"] + shared + ["adapters/generation/modes/MODE_C_NANO_BANANA_PRO.md", "adapters/generation/modes/MODE_C_OMNI_FLASH.md", "rules/production/EDITABLE_TEXT_UI_HANDOFF.md"],
    "D_HYBRID_COMPOSITING": ["rules/production/MODE_D_HYBRID_COMPOSITING.md"] + shared + ["adapters/generation/modes/MODE_D_NANO_BANANA_PRO.md", "adapters/generation/modes/MODE_D_OMNI_FLASH.md", "rules/production/COMPOSITING_HANDOFF.md"],
}
production = {
    "FACTUAL_DOCUMENTARY": ["rules/production/FACTUAL_DOCUMENTARY.md"],
    "LOCALIZATION": ["rules/production/LOCALIZATION.md"],
    "ARCHITECTURAL_CONTINUITY": ["rules/production/ARCHITECTURAL_CONTINUITY.md"],
    "UGC_ADVERTISING": ["rules/production/UGC_ADVERTISING.md"],
    "CINEMATIC_SCENE": ["rules/production/CINEMATIC_SCENE.md"],
}
tools = {
    "NANO_BANANA_PRO": ["adapters/generation/NANO_BANANA_PRO.md"],
    "GEMINI_OMNI_FLASH": ["adapters/generation/GEMINI_OMNI_FLASH.md"],
    "PLATFORM_NEUTRAL_HANDOFF": ["rules/production/POST_PRODUCTION_HANDOFF.md"],
}
combos = [{"owners": ["NANO_BANANA_PRO", "GEMINI_OMNI_FLASH"], "files": ["adapters/generation/NANO_BANANA_PRO_OMNI_FLASH_PIPELINE.md"]}]
paths = []
for seq in list(profiles.values()) + list(audiences.values()) + list(modes.values()) + list(production.values()) + list(tools.values()) + [x["files"] for x in combos]:
    for rel in seq:
        if rel not in paths:
            paths.append(rel)
files = {}
for rel in paths:
    p = ROOT / rel
    if not p.is_file():
        raise SystemExit("Missing manifest source: " + rel)
    files[rel] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size}
out = {
    "schemaVersion": "7.8.0",
    "packageVersion": "7.8.0",
    "hashAlgorithm": "SHA-256",
    "proofBoundary": "Integrity and selection, not private attention or media execution.",
    "profiles": profiles,
    "audienceTriggers": audiences,
    "modeTriggers": modes,
    "productionTriggers": production,
    "toolTriggers": tools,
    "combinationTriggers": combos,
    "customToolPolicy": "Unmapped owners are prohibited in the canonical prompt-only build.",
    "files": files,
}
(ROOT / "bootstrap/runtime_load_manifest.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"manifestFiles": len(files), "version": "7.8.0"}, indent=2))
