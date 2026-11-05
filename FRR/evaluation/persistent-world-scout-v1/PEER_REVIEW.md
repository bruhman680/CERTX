# Targeted peer review

Reviewed `TEXT_WORLD_SCOUT.md`, `RESOURCE_SCOUT.md`, and the DiscoveryWorld distinction in `OPEN_ENDED_SCOUT.md`. Research only, 2026-11-05; no installation or execution. Other reports were not edited.

## DiscoveryWorld: both observations are correct, but the adoption conclusion needs the implementation caveat

The [paper §3.1](https://arxiv.org/html/2406.06769v1) establishes that an **agent can consume text observations without consuming images**. It does not establish that the stock runtime avoids rendering.

I independently opened the [current API source](https://github.com/allenai/discoveryworld/blob/main/discoveryworld/DiscoveryWorldAPI.py#L117). For valid initialized agents, `getAgentObservation()` renders two viewport variants, writes PNG files and base64-encodes images before calling `ui.renderJSON()`. Construction also creates a pygame headless window; scenario initialization loads sprite-related resources. Ignoring the returned `vision` field does not skip that work. “Headless” means no visible window, not no image processing.

Thus the resource scout's caution is supported. My open-ended report's “graphics are optional” should be read as an observation-modality claim, **not a lightweight, rendering-free deployment claim**. Recommended synthesis wording: “DiscoveryWorld supports text-consuming agents, but its inspected stock API still renders and writes images. Its object/experiment design transfers; a minimal text runtime requires engineering.” No measured CPU or disk cost is available, and removing one rendering call would not prove all visual dependencies are gone. This check used moving `main`, not a pinned revision.

## Other targeted qualifications

- **The recommendations are compatible when labeled by purpose.** TextWorldExpress is the strongest inspected executable baseline for small text tasks; ScienceWorld offers richer existing tending; Crafter supplies accessible construction rules. None is demonstrated as a drop-in persistent workshop. The proposed tiny object engine is a new implementation borrowing these architectures.
- **Replay restoration is narrower than continuous life.** TextWorldExpress's recorded configuration and action replay support reconstruction under compatible code, seeds and transition semantics. They do not by themselves establish indefinite continuation after task termination, arbitrary newly created object serialization, or inexpensive replay of a growing lifetime. Continuing after milestones needs explicit engine/terminal-policy design; a snapshot recommendation is prospective work.
- **Do not turn suggestive examples into supported simulator behavior.** The text scout's powered loops, pumps and persistent gardens are clearly design proposals. ScienceWorld's reported series-circuit limitation and the resource scout's incomplete plant-precondition audit matter: unrestricted circuit graphs or a validated watering schedule do not follow from those inspections. Crafter placement recipes establish bounded construction, not arbitrary functioning machines.
- **Evaluation information changes the task.** Full object trees, valid action menus, gold paths and task scorecards have different information privileges. A valid-action list can reveal a hidden prerequisite or object even without a gold path. Keep acting observations separate from diagnostics and record menu exposure when comparing model behavior.
- **HF descriptors are task-selection data.** ScienceWorld task name plus variation number should not casually be called a generic RNG seed. The resource report already flags runtime-version incompatibility and nonstandard splits; retain those qualifications when summarizing reproducibility.

All three reports correctly stop short of inferring small-model planning or motivation. The final synthesis should preserve that boundary: these are candidate affordances and harness mechanisms whose usefulness for the fixed 135M+LoRA model remains untested.
