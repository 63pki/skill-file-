# Nano Banana Pro Prompt Adapter

**Owner:** `NANO_BANANA_PRO`  
**Official snapshot:** 2026-07-21  
**Boundary:** prompt authoring only

## Prompt families

- `NBP-F1 TEXT_TO_IMAGE`: Subject + Action + Context + Composition + Style.
- `NBP-F2 REFERENCE_GENERATION`: References + relationship/precedence + new scenario.
- `NBP-F3 IMAGE_EDIT`: Base image + requested change + exact invariants.
- `NBP-F4 CONTROLLED_VARIATION`: Approved anchor + one permitted variation + preserved locks.
- `NBP-F5 TEXT_LOCALIZATION`: exact quoted text + language + hierarchy/style + accuracy inspection.

## Required block

```text
AVD:NANO_PROMPT id=... framework=NBP-F1|NBP-F2|NBP-F3|NBP-F4|NBP-F5
Operation:
Subject/references:
Reference roles and precedence:
Action or requested change:
Context:
Composition:
Style and rendering:
Camera/lighting/material:
Preserve exactly:
Output assumption:
Acceptance:
First one-variable repair:
```

Use positive, specific direction. For edits, change only the named region or property and preserve everything else. Treat text, labels, brands, factual graphics, anatomy, and product geometry as inspection-critical even when the model supports them.
