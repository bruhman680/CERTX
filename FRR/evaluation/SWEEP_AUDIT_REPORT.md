# Shadow–echo sweep audit

Original scripts were executed unchanged, with stdout saved in results/sweep-audit-original-eps.txt and sweep-audit-original-simplex.txt. The n=8 TV 0.3604 and n=12 TV 0.4545 reproduce. Original manifest/source copies are unchanged. Working copy experiments/sweep-audit-corrected-eps.py adds a separately sampled W for noisy echo's hidden fair coin.

## What changed

The original shared U couples visible-symbol and hidden-coin draws. Conditional on e=0,y=0,delta=.2, the target probability P(y_next=1,e_next=1) is .015, while original code gives .03. A million independent samples verify both values within .0005; see sweep-audit-rng-joint.json. The deterministic law calculations do not use this faulty simulation code.

Corrected full-script noisy echo delta=.2 switch-rate mean is .264 versus original .258 (200 trajectories of 3000 steps). These two full runs are not paired: adding W advances the generator and changes later samples, even in unaffected conditions. Their discrepancy alone does not quantify bias. The conditional joint test directly isolates the implementation error.

## A useful correction to our earlier correction

The scripts count rounded next-symbol probabilities, not general full predictive states. HOWEVER, in their particular K table, an exact next-symbol probability uniquely identifies the last visible symbol and the posterior hidden-bit probability: the two symbol-conditioned ranges are disjoint ([.15,.45] and [.6,.9]), and each map is affine with nonzero slope. These are sufficient statistics for all future predictions under a fixed kernel. Thus exact one-step equality is sufficient for full-future equality HERE. The general warning should not erase this special-case sufficiency.

Rounding removes this exact sufficiency. At epsilon=.05, depth12, histories 000000100101 and 001110111101 both round to next probability .63, but have exact probabilities .6252033584 and .6349944908 and two-step-future TV .01395236. Counting rounded future vectors also depends on coordinatewise tolerance and block length. Forty-five finite depth/kernel/block combinations were normalized and recorded in sweep-audit-future-blocks.json. A generic counterexample outside this table has hidden states A and B both emit 0 immediately, while A then transitions to an emitting-1 state and B remains emitting-0: next predictions equal, two-symbol futures disjoint.

At epsilon=.01 the source reports 4095, not 4096, distinct nine-decimal predictions at depth12. No finite depth count proves infinitely many predictive states; initialization is uniform and generally nonstationary, so stationary-process literature cannot be applied without addressing the initialization limit.

## Surviving interpretation and next contact

A continuous interpolation of finite-word laws exists by construction within this kernel family. Hidden-state update persistence and visible-history copying need not be mutually exclusive diagnostic modes. Trajectory switch-rate spread probes finite-window mixing; it does not uniquely identify hidden state or environmental memory. No thermodynamic or retained-environment-after-focal-reset claim was tested here. Next substantive test is paired retain/clear environment with reset focal state; next mathematical contact is stationary filtering and sufficiency proof, rather than promoting rounded cardinalities to infinite-state claims.

Reproduce: run both originals, experiments/sweep-audit-corrected-eps.py, and experiments/sweep-audit-future-blocks.py. Results are numerical reproduction plus local implementation discrimination, not independent cross-domain confirmation.
