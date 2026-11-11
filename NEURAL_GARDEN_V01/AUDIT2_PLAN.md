# Independent stress audit — online-updating verdict

Question: Is the earlier result that frozen trained neural weights outperform online updates robust beyond the previous mild regrowth regime, or is it a narrow environmental finding?

Design locked before execution: train `reserve_resource` per-cell neural weights for 1,000 ticks with `NEXT_WELFARE_study.train`, then test matched worlds (same seed, initial physical state, and action RNG) over 3,000 ticks with stochastic online weights vs stochastic frozen weights. Stress laws are constant regrowth 0.03 (sustained scarcity) and 0.08 (abundance), plus the original 0.06 stable reference. Use eight held-out seeds 11000–11007, grid size 10. Record final energy, energy AUC, fraction at the floor and last-500-tick raw drift, per-seed paired differences, and final theta divergence. No hyperparameter selection or dropping unfavorable seeds.

This tests **only** the given learner and named synthetic laws. It cannot establish a universal effect of ongoing learning or distinguish environment-specific natural resource exhaustion from incompetent learning unless supplemented by action and resource traces. In saturated floor regimes, final-energy differences may cease to be informative, so AUC and raw drift remain necessary.
