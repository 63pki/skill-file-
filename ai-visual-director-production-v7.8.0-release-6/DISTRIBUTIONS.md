# V7.8.0 Release 6 Distributions

Built by `dev/build_distributions.py --zip`. Four distributions, one canonical source.

- **`cumulative`** — complete authoritative package; use for installation and auditing. **Canonical.**
- **`combined`** — the active skill plus the validation tooling needed to run the gates: rules, adapters, templates, bootstrap, validators, and the bundled suite. The smallest archive that can reach `VERIFIED_RUNTIME`.
- **`portable-core`** — prompt and rule content only. **Contains no Python.** Maximum assurance `PLAN-PASS` under `PORTABLE_REFERENCE`. This is the default install for hosts that cannot execute Python.
- **`validation-sdk`** — validators, tests, fixtures, protocols, and templates for release and evidence work. **An add-on to `portable-core`, not a standalone product**: it declares `requires: portable-core@7.8.0` and cannot run its own gate alone.

## Choosing one

| If you need | Install |
| --- | --- |
| To write prompts and plan a production, no Python available | `portable-core` |
| To run the release gates and reach `VERIFIED_RUNTIME` | `combined` |
| To audit the release or verify provenance | `cumulative` |
| To add validation to an existing `portable-core` install | `validation-sdk` |

`portable-core` ships `QUICKSTART.md`, which states this boundary at the top: skip every step beginning with `python3` and follow *Portable Assurance* instead.

## Guarantee

Splitting delivery does not delete or weaken the cumulative release. The cumulative ZIP remains canonical, and every distribution is derived from the same 246-file source tree — never hand-edited.

## Live evidence

The live-evidence bundle ships an empty campaign structure and protocols only. All five live tracks remain `NOT_RUN`; no distribution upgrades that. See `release/RELEASE.json` → `liveEvidence`.
