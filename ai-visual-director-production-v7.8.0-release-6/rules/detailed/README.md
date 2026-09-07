# Detailed Source Library — V7.8.0 Release 6

This is the **active** detailed rule library: 43 top-level rule files plus 9 files under `optional/`, 52 in total. `rules/detailed/00a_router.md` is mandatory for every Production Sequence and Campaign/Long Project, and this folder contains the current authorities it dispatches to.

*Provenance:* the deep-reference and optional libraries in this folder originate in V6.8 and have been carried forward and revised since. `28_adaptive_next_protocol.md` records its own V6.8 lineage. Origin is V6.8; the contents are V7.8.0 Release 6 and are not a frozen archive.

- Do not load this folder by default.
- These files cannot override `SKILL.md` or `rules/RUNTIME.md`.
- If a detail conflicts with runtime, runtime wins and the detail must be corrected during maintenance.
- Promote a detailed rule into runtime only after regression evidence shows it is broadly required.
