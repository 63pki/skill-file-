# Hermes Migration to V7.0

V7.0 changes the skill identity from `ai-visual-director-production-v6` to `ai-visual-director-production-v7`.

## Safe migration

1. Back up the currently installed V6 skill folder and active project state.
2. Install V7.0 into a separate `ai-visual-director-production-v7` folder.
3. Verify root `SKILL.md`, `rules/RUNTIME.md`, the triggered production module, templates, and adapters.
4. Run the Performance, Quality, Production, and Conflict test suites.
5. Move active projects with a model-switch/project handoff; reset model capability to CONTROLLED.
6. Disable or remove the old V6 installation only after V7 passes live behavioral tests.

Do not leave both V6 and V7 registered under the same skill name. Do not overwrite a working installation without an approved backup and rollback path.

## Behavioral migration

- V6.9 micro-step NEXT is obsolete.
- V6.10 six-gate performance behavior remains active.
- V6.11 quality evidence and critical floors remain active.
- V7.0 adds production modules, media inspection, operator adapters, human review, and validated exports.

A static file check is not a live behavioral PASS.
