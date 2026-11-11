# Two-input neural harvesting: teacher-free learning and deployment ablations

**Status:** Two executed substantive hypothesis passes on an explicitly separate policy family. These are toy-world model experiments, not biological findings. Sources: `SOC_ENERGY_AWARE_policy.py`, `SOC_ENERGY_AWARE_study.py`, `SOC_ENERGY_AWARE_results.json`, `SOC_ENERGY_AWARE_deployment.py`, and `SOC_ENERGY_AWARE_deployment_results.json`.

## Design and what the model already knows

Each 16×16 cell has a learnable logistic action policy with local `resource`, local `energy`, and a bias. Teacher-free REINFORCE uses a `.97` delayed eligibility trace and *unclipped raw local energy reward*. No action labels, imitation teacher, explicit energy-rescue threshold, or externally designed stewardship bonus are provided to this learner. Its resource weight, however, starts with an **explicit positive resource-sensitive inductive bias** (approximately coefficient 4); the energy weight starts at zero. This is a test of whether the model can exploit **an additional energy input**, not a demonstration that all resource-dependent behavior emerges from an unstructured blank network.

The matched resource-only ablation sets the energy feature to zero with otherwise identical physics and learning code. A frozen pretrained energy-aware comparator tests online updates; a clipped-reward ablation tests raw-versus-realized feedback. Fixed `.50` and a *separately labeled hand-coded rescue* comparator (`.48` when energy below `.18`, else `.50`) have no neural training. All original resource, diffusion, harvest and energy coefficients are unchanged except an **explicitly labeled mild-regrowth test** (`.06→.055→.06` during test ticks 1001–2000).

First pass: 12 fresh matched seeds per regime (stable seeds 15000–15011, mild 16000–16011). Train for 1,200 ticks in the ordinary world, transfer learned weights to independently seeded but arm-matched test worlds, and run 3,000 ticks.

## Pass 1: stochastic operation after training

| Test world | Energy-aware raw, online | Resource-only raw, online | Energy-aware raw, frozen | Energy-aware clipped, online | Fixed `.50` | Hand-coded energy rescue |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Stable mean energy t3000 | .0406 | .0500 | .0528 | .0505 | **.6509** | .6509 |
| Mild change mean energy t3000 | .0409 | .0507 | .0532 | .0520 | .0442 | .0270 |

The energy-aware raw-reward learner **performed worse** than its resource-only ablation and even its own matched frozen pretrained stochastic comparator on these seeds. Raw feedback and an energy input did not automatically improve ecology. The hand-coded rescue rule lowered performance in the perturbed world: simplistic rescue is not sufficient.

The key ambiguity is **stochastic exploration cost**: training-time random harvest actions remain active during testing, and that may dominate what the learned action preferences could accomplish if deployed deterministically.

## Pass 2: deterministic deployment of the same teacher-free weights

This was a separate question tested on **12 new matched seeds per regime** (stable seeds17000–17011, mild18000–18011), with the same 1,200-tick training on original laws but frozen deterministic action at test time. The action is selected by the sign of the learned two-feature logit; no further updates during deployment.

| Test world | Energy-aware learned | Resource-only learned | Fixed `.50` |
| --- | ---: | ---: | ---: |
| Stable mean energy t3000 | **.5849** | .4672 | **.6531** |
| Stable fraction near energy floor | .55% | 4.72% | **0%** |
| Mild change mean energy t3000 | **.1172** | .0929 | .0447 |
| Mild fraction near energy floor | 20.31% | 26.33% | 20.31% |

The energy-aware policy outperformed the otherwise equivalent resource-only ablation in all 12 matched seeds in each regime: mean paired advantage +.1177 in stable worlds and +.0243 under mild regrowth change. It **did not beat fixed `.50` under stable laws**, but did beat it in all 12 mild-change seeds by about +.0725 mean energy. The latter is a held-out same-generator simulated result after the architecture was chosen, not a general claim of adaptability. The energy-aware policy did **not** reduce the near-zero-cell share below fixed `.50` in the mild regime (both ~20.3%).

## Correct interpretation and next test

1. **Extra information can help**, but *how the policy is deployed* matters strongly. Deterministic learned energy-sensitive decisions outperform the matched resource-only decisions in these tests, whereas stochastic online learning failed to do so.
2. A policy that survives a shift better when deployed with frozen weights is **state-conditioned robustness**, not evidence that it learned *during* the shift. The policy was pretrained on original laws, and its parameters were frozen during the altered regime.
3. The architecture uses an explicit positive resource input prior; learning did not construct an entire ecological strategy from scratch.
4. The fixed threshold `.50` remains better in the stable regime and leaves fewer depleted cells. The model does not establish universal fitness, social intelligence, indefinite ecological viability, or open-ended evolution.
5. The 12-seed matched findings need independent source audit, broader world-law perturbations, predeclared coefficients, very long horizons, and action-conditioned policy interpretation before stronger claims.

**Next pressure:** systematically ablate the energy coefficient itself at deployment (set it to zero after training while keeping other learned weights), so that any advantage is traced directly to the *learned energy dependency* rather than indirect training differences. Then test the exact same policy across held-out mild and severe shifts with cell-level floor and recovery metrics, not just mean energy.
