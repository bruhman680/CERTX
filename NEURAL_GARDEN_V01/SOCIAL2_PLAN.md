# Local neural-policy sharing: pre-outcome study plan

Question: After identical teacher-free neural training, does copying a neighbor's neural policy help during an environmental shift, compared with copying an arbitrary policy or preserving one's own?

This is an *engineered* social-transfer mechanism, not spontaneous communication or evolutionary learning. All cells retain separate parameter tensors. The intervention copies only the three coefficients of the pre-existing `EnergyAwareGarden` policy; original world laws and the primary Living Garden are untouched.

Design: train every cell for 1,500 ticks in stable regrowth .06; fork to altered regrowth .055 and deploy deterministic policies for 3,000 more ticks. A parallel stable-regrowth cohort is a control. All policy-gradient updates are disabled after the fork in all arms. At the fork, optionally copy weights from (a) highest-energy cardinal neighbor, (b) lowest-energy cardinal neighbor, (c) a randomly selected cardinal neighbor, (d) globally shuffled donor, (e) average of four local neighbors, or (f) no copy. Topological torus is the original Garden's neighborhood. A copied donor is selected by *current* pre-shift energy only (not future outcomes), and all choices are simultaneous to avoid ordering effects. Stable and mild changing environments, 12 held-out seeds per environment, size 12.

Primary outcomes: final mean energy, energy-floor fraction, bottom-decile energy, mean resource; plus paired seed-level wins vs no transfer and vs local-random copying. All outcomes are exploratory, not statistical population inference. Copying can wash out local specialization or propagate a lucky but unsuitable donor; source-neighbor covariance and transfer magnitude are logged.

Precommitted initial expectation: high-energy-neighbor copying might confer a modest benefit immediately after shift, but could fail because observed energy confounds starting conditions with policy quality. Thus frozen/no-copy and same-rate randomized copying are essential.
