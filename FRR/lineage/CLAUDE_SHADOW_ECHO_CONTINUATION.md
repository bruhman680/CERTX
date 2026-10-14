# Claude shadow–echo sweep continuation — 2026-10-11

User supplied simplex_edge.py, eps_sweep.py, and a Claude chat report for later exploration. Original scripts are preserved unchanged under sources/claude-shadow-echo-2026-10-11 with SHA-256 hashes. This intake was code inspection only: no local reproduction or independent source verification was performed.

Claude reports a continuous interpolation between frozen hidden-bit and visible-history-copying kernels, resolution-dependent next-symbol prediction counts, and finite-window switch-rate dispersion. Reported numbers remain attributed to Claude pending reproduction.

## Next contacts

1. Reproduce exact finite-word probability tables and normalization before changing source copies.
2. Correct a working copy of eps_sweep.py: sim_rates reuses U[r,t] for visible-symbol generation and the noisy-echo hidden fair coin. Use a separate independent draw; compare simulated joint transitions with the exact kernel. Deterministic forward tables do not share this simulation defect.
3. Rename rounded next-symbol-probability counts accurately. Full predictive-state equivalence concerns entire future conditional distributions; one-step agreement alone does not establish it.
4. Vary history depth, future-block length, resolution, trajectory length, seeds, and kernel tables. Separate finite-window mixing diagnostics from hidden-state detection and claims of infinite predictive-state structure.
5. Implement retained-versus-cleared environmental state after a focal reset, with paired replay and fresh readers, to test wake location.
6. Revisit thermodynamic claims only with an explicit valid transition chain, stationary distribution, detailed-balance checks, and appropriate entropy-production observable. Review cited sources directly before extending their scope.
7. Treat stigmergy, niche construction, performative prediction, and model collapse as related candidates with different mechanisms, not established equivalents. If older drafts or hardcoded findings contradict verified results, preserve originals and add dated errata.

Resting question: does a distinction disappear, or does observation horizon/resolution stop revealing it? User intends to resume from laptop; no further experiment initiated during intake.
