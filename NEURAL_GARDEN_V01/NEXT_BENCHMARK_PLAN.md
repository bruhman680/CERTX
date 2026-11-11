# Predeclared Garden cross-condition benchmark (before running)

**Status at creation: design frozen, no benchmark outcomes observed.** This benchmark is an exploratory multi-factor assessment of *already selected* policies and world laws, not pristine preregistration of the policies themselves. Do not retune any policy after results arrive; do not claim cross-world independence of observations at different horizons from the same run.

## Controls and tested policies (all formulas fixed before execution)

All policies observe the same pre-step local `resource` `R`, energy `E`, and where applicable four-neighbor mean resource `N`; no birth/death, mutation or language. Actions are deterministic `A in {0,1}` at test time.

1. `fixed050`: `A=(R>0.50)`.
2. `fixed051`: `A=(R>0.51)`.
3. `energy_rescue`: `A=(R>0.51) OR (E<0.12 AND R>0.485)` (historically selected rescue exactly).
4. `reverse_rescue`: `A=(R>0.535 if E<0.12 else R>0.51)` (adversarial reversed gate).
5. `neighbor_gradient`: `A=(R>0.51 + 0.5*(N-R))`.
6. `learned_energy`: the frozen deterministic logit from `SOC_ENERGY_AWARE_policy.EnergyAwareGarden` (input `[3*(R-.5), 3*(E-.5), 1]`, action if dot(theta,x)>0), trained **without a teacher** on separate original-law initial worlds for 1200 ticks with raw reward, lr=.04 and eligibility decay=.97. The trained parameters are not optimized on this benchmark, and the test-time neural controller does NOT update.

## Test worlds and horizons

Four distinct environments, all with original energy accounting, original resource consumption and regrowth unless explicitly varied:

- `stable`: regrowth .06, diffusion .08, no intervention.
- `mild_regrowth`: regrowth .055 on test ticks501–1500, otherwise .06, diffusion .08.
- `no_diffusion`: diffusion coefficient 0 throughout, regrowth .06.
- `shock`: initial laws; after the update for tick600 multiply every resource by .70 exactly once, no further interventions.

Sizes: `8, 12, 16`. Four matched test seeds for each size: `33000, 33001, 33002, 33003`, with fresh training seeds `25000..25003` (shared trained neural model by size/seed, evaluated on separate test world seeds). All six policies start with exactly identical resource and energy arrays for the matched size/seed; learned model differs in its *weights*, not physical initial state.

Simulate each environment/policy/seed/size to **6,000 ticks** and retain checkpoints at ticks **1,000, 3,000, and 6,000**. There will be 4 worlds ×3 sizes×4 seeds×6 policies = **288 distinct test trajectories**, with 864 nested horizon observations; don't claim 864 independent worlds. The same test seed across worlds is paired initial conditions, not an identical exogenous trajectory after first intervention. The four training seeds are a small convenience sample, not evidence of model-general policy efficacy.

## Outcomes and decisions

At each checkpoint record mean energy, fraction of cells at energy floor <=.01, upper cap >=.99, mean resource, mean harvest frequency, average resource-action covariance, tail raw energy budget (last 100 ticks), and lower-decile cell energy. Record source SHA256, environment/config hashes, Python and NumPy version, and unique IDs. Confirm exact resource and energy accounting against the Garden formulas for stable mode on a smoke seed. No weights/thresholds modified in response to benchmark results.

Benchmark interpretation is multiobjective: energy retention, distributional welfare and recovery after disturbance are separate. Do not choose a global winner based on average energy alone. Report scale/horizon reversals, null results, floor clipping, and non-identical law regimes. This is **one substantive comparative benchmark research loop**, not 288 loops.
