# Gemini Omni Flash Video Prompt Adapter

**Owner:** `GEMINI_OMNI_FLASH`  
**Model identifier snapshot:** `gemini-omni-flash-preview`  
**Official snapshot:** 2026-07-21  
**Boundary:** prompt authoring only; preview capabilities require surface verification

## Task families

- `OM-F1 TEXT_TO_VIDEO`
- `OM-F2 IMAGE_TO_VIDEO`
- `OM-F3 REFERENCE_TO_VIDEO`
- `OM-F4 CONVERSATIONAL_EDIT`
- `OM-F5 EXISTING_VIDEO_EDIT`

## Required block

```text
AVD:OMNI_PROMPT id=... task=OM-F1|OM-F2|OM-F3|OM-F4|OM-F5
Task parameter:
Inputs and roles:
Subject:
Action:
Scene/context:
Camera:
Lens/focus:
Style, lighting and ambiance:
Temporal direction:
Audio:
Continuity invariants:
End condition:
Output assumption:
Acceptance:
First one-variable repair:
```

For one shot say `single continuous shot`, `single unbroken scene`, and `no scene cuts`. For a conversational edit, keep the instruction short and end with `Keep everything else the same.` Timing may use natural language or `[0-3s]` notation. Do not request extension, first/last interpolation, uploaded-audio reference use, voice editing, multiple-video reasoning, or a dedicated negative-prompt parameter.
