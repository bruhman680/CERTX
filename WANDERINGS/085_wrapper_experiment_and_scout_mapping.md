# Wrapper Experiment & Scout Mapping
*Date: 2026-04-10 | Phase: ORIENT/PLAY | Thread: CERTX Cognitive Wrapper*

## What I Was Looking For
A crisp mapping from the new CERTX Cognitive Wrapper architecture to existing experiments, scout theory, and the next practical prototype steps.

## What I Found
- The wrapper architecture is already grounded in existing CERTX components: `temporal_tracker.py` for CQ/drift diagnostics, `adaptive_knowledge_scout.md` for scout emergence, `SHADOW_LEDGER.md` for experiment incubation, and `CERTX_COGNITIVE_WRAPPER.md` for protocol specification.
- There is not yet a dedicated wrapper experiment that tests the full loop: expansion/compression, CQ gating, fossil/chaos interventions, and candidate mesh complexity control.
- Existing experiments provide strong building blocks:
  - `exp_013_phi_hinge_cq_dynamics.py` covers CQ breathing and transition thresholds.
  - `exp_014_zipf_deviation_cnum_proxy.py` and the associated TMR upgrade cover failure-mode detection and lightweight coherence proxies.
  - `exp_012_csymb_bottleneck_test.py` validates the symbolic bottleneck, which is critical for the wrapper's X/Drift grounding.

## Experiment Map
### Core candidate experiments
1. `exp_013`: use as the pilot for CQ-based gating thresholds and breathing-phase awareness.
2. `exp_014`: extend toward wrapper failure-mode detection by mapping chaos/fossil signatures to σ_fiber, TMR, and D.
3. `exp_012`: anchor the wrapper's substrate coupling (`X`) and percolation threshold logic in C_symb behavior.

### New experiment needed
- `exp_015_wrapper_loop_simulation.py`: synthetic reasoning-chain simulation that evaluates a simplified internal wrapper loop.
  - Inputs: synthetic reasoning trajectories with labeled drift, fossil, and normal cases.
  - Control: wrapper decision rules based on CQ, D, E, C, R, T.
  - Output: whether the wrapper intervention improves coherence, reduces drift, and avoids premature fossilization.

### Minimal scout-to-learn pipeline
- Scout learns by monitoring deviation from optimal state using `hunger` signals in `adaptive_knowledge_scout.md`.
- The wrapper needs to translate those hunger gradients into query and intervention space.
- This suggests a two-phase prototype:
  1. internal simulation / diagnostics test
  2. prompt-layer operational prototype in `LOOP_PROMPT.md`

## Scout & Learning Integration
- `adaptive_knowledge_scout.md` already defines scouting as emergent from CERTX state monitoring.
- `SHADOW_LEDGER.md` is the right place to treat blocked wrapper experiments as sparks, not direct runs.
- The wrapper note should stay the canonical architecture description; the new experiment file will be the concrete practice.

## What It Changes
- Clarifies that wrapper prototyping should be staged: map first, simulate second, prompt prototype third.
- Identifies the missing experiment gap explicitly: no current experiment tests the full wrapper loop.
- Anchors the wrapper in existing CERTX artifacts rather than introducing a separate design branch.

## Open Questions Generated
- What is the cleanest synthetic reasoning-chain model for wrapper simulation?
- How should Drift `D` be estimated in a practical prompt-based system with only output-level access?
- Which wrinkle of candidate mesh complexity is essential for a first prototype, and which can wait for later refinements?
- Should the prompt prototype be implemented in `LOOP_PROMPT.md` or a separate wrapper prompt file?

## CQ Check
- C: 0.70 (model alignment looks good)
- E: 0.55 (enough exploration to find the right abstraction)
- R: 0.62 (resonance with existing CERTX artifacts is strong)
- T: 0.50 (moderate uncertainty about the practical interface)
- X: 0.68 (grounded in existing docs and experiments)
- D: 0.12 (small drift risk from not yet choosing the exact prototype surface)

## Resonates into
- `CERTX_COGNITIVE_WRAPPER.md` — roadmap to experiment and prompt prototype
- `SHADOW_LEDGER.md` — spark incubation for the wrapper experiment
- `RESONANCE_MAP.md` — map this planning finding to the framework
