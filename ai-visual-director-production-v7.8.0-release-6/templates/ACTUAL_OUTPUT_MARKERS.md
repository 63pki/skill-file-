# Actual Output Metadata — V7.8.0

Supported surfaces are HTML `AVD:*` comments, fenced `avd-artifact` / `avd-evidence` JSON, and indexed package sidecars. Parsing is fail-closed: unclosed/nested/orphan blocks, malformed attributes, invalid numeric fields, type mismatches, and conflicting status/tool/structure metadata become validator errors.

## Binding status and artifact example

```markdown
<!-- AVD:RUNTIME challenge=... manifestSha256=... receiptSha256=... contextSha256=... -->
<!-- AVD:STATUS delivery=SINGLE_PASS_BLUEPRINT maturity=PLAN-PASS media=NOT_GENERATED -->
<!-- AVD:ARTIFACT id=STYLE_BIBLE -->
## Visual family
...
<!-- /AVD:ARTIFACT -->
```

## Shared source files

When multiple index records point to one file, each record must resolve to exactly one body. Use an `AVD:ARTIFACT` block, a unique `sourceAliases` heading, or `sourceSelector`:

- `AUTO`: unique matching artifact marker, then unique heading.
- `ARTIFACT_MARKER`: matching `id`.
- `HEADING`: heading named by `value`.
- `RANGE`: exact `start` and `end` sentinels.

A shared file without an unambiguous selector fails with `SHARED_SOURCE_SELECTOR_REQUIRED`; the extractor never assigns the entire shared file to multiple artifacts. Paths escaping the package root are rejected.

## Fenced JSON

A fence may contain one object or an array of objects. Non-object values fail with a structured type error. Metadata is not evidence by itself. Referenced files, hashes, versions, methods, and reinspection must validate.

## Generation prompts

Use the exact Nano Banana Pro and Gemini Omni Flash block formats in `templates/GENERATION_PROMPT_MARKERS.md`. Nested, unclosed, orphaned, duplicate-ID, or malformed prompt blocks fail closed.
