# Shadow, echo, and reset: research pulse

This pulse reproduced the original Claude scripts, corrected a simulation defect in a working copy, read primary predictive-state sources, and constructed an exact retained/cleared-field intervention. Three role-separated agents contributed; their shared prompt and code ancestry are not independent empirical replication.

## Surviving relationships

The original finite-word TV values reproduce: .3604 at depth8 and .4545 at depth12. A continuous interpolation between persistence and copying exists in the specified kernel family. It is not a universal identity between diagnostic modes.

The noisy-echo simulation reused a visible-emission random draw for its hidden coin. A conditional joint-event test distinguishes the intended probability .015 from the original .03; corrected independent sampling returns .015059 in a million draws. Exact forward probability tables were unaffected. See SWEEP_AUDIT_REPORT.md.

Our earlier generic warning about next-symbol predictions needed refinement: this K makes the exact next probability sufficient to reconstruct last symbol and hidden belief, hence the full future. Rounding destroys that exact sufficiency: two histories round to .63 but differ by .01395 in two-step-future TV. Finite-prefix counts are not stationary infinite-past state counts. At the frozen endpoint, infinite history can identify the persistent class, yielding a finite limiting description despite proliferating finite-prefix posteriors. See ../lineage/PREDICTIVE_STATE_SCOUT_NEW.md.

## A controlled carrier test

experiments/wake_reset_transfer.py explicitly designates y as independently resettable focal state and e as transferable latent environment. Its field vector represents a probability distribution over a bit, not a realized continuous physical field. A writer repeatedly imposes a bit with deposition strength h; holding noise flips e with probability epsilon. A fresh reader starts with fixed y and receives no writer history.

5,376 exact conditions cover write strength, pass count, holding noise, delay, visible reset, read horizon, and seven controls. Checks establish normalized probability laws, zero cleared/no-write/reader-blind effects, and the analytic one-step contrast:

TV = .3 [1-(1-h)^passes] |1-2epsilon|^delay.

For h=.2 and ten passes, contrast is .26779 immediately, .21880 after ten holding steps at epsilon=.01, and .03551 after100. Clearing gives zero. Copying a prepared field into a fresh reader preserves the contrast; swapping fields swaps which writer history produces which outcome. Transfer invariance is stipulated by the reader API and tested algebraically, not an independent physical transplantation discovery. Retaining a writer whose state has no channel to the reader cannot restore an erased field by construction.

This separates action-conditioned writing, persistence, and access. It does not show useful semantic memory, growth, emergence, irreversible law, or real AI swarm improvement. Another history preparing the same field yields identical future observations: residual state does not uniquely recover its genealogy.

## Source contact and remaining residual

Primary predictive-state and lumpability texts were read substantively in the predictive scout. The wake scout records weaker access to some sources: abstract/figure captions for Reid et al., abstract for causal abstraction, blocked full text. Source routes have different evidential depths; shared citations are not independent confirmation. See ../lineage/WAKE_RESET_SCOUT_NEW.md.

Next tests: stationary initialization and longer future blocks; genuinely distinct writer/reader implementations; noisy access and imperfect resets; independent held-out kernel families; dynamic parameters if claiming field-rule change rather than merely changing state. Thermodynamic claims remain pending a valid stationary-chain construction. Core FRR runtime/schema are unchanged.

Reproduce originals under lineage/sources/claude-shadow-echo-2026-10-11; corrected/audit scripts under experiments/sweep-audit-*; reset experiment under experiments/wake_reset_transfer.py. Full results remain in evaluation/results.
