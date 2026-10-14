# Imperfect-reset two-carrier experiment

## Setup and surviving relationship

200,000 trials per condition, 72 matched conditions, seed714. A randomized writer bit independently overwrites a private actor bit and an environment bit with probability.8. Both initial bits and erasure replacements are independent fair coins. A reader selects the environmental carrier with probability q (0,.5,1), otherwise the private carrier. Each carrier undergoes independent .1 bitflip noise, then the reader undergoes separate .1 measurement noise. Reset of private state retains it accidentally with probability ℓ (0,.05,.5); explicit private retention bypasses reset. Field retention and private retention form independent factorial controls; no-write and blind reader controls are included.

With write strength a=.8, both channel attenuations .8, and effective retention R_E,R_P, exact expected accuracy is

`0.5 + 0.5*a*0.8*0.8*(q*R_E + (1-q)*R_P)`.

All arms agreed with this expectation within six Monte Carlo standard errors. No-write arms agreed with chance. At q=.5 and zero private leakage, retaining field gave accuracy .628565 versus clearing .500615: paired effect .12795 versus analytic .128. Blind accuracy .49937.

When BOTH carriers are nominally cleared but private reset leaks with probability.5, accuracy rises to .5642 despite no retained field. Hence post-reset above-chance performance alone does not locate persistence in the environment. Holding leakage fixed, the retained-versus-cleared-field paired contrast still separates a specifically environmental pathway in this model.

## Boundaries of the claim

Carrier identity, source payload, read mixture, write success law and reset leakage are specified by construction. No learned agent infers the carrier; no semantic interpretation is tested. A single-bit reader cannot identify whether an individual correct response came from field or private state. The observer's source-selection architecture, rather than collective wisdom, makes location effects identifiable across interventions.

Initial states are independent of writer payload by construction. Real unknown initial fields could already carry correlated information. Erasure substitutes distribution-matched fair coins, so it does not introduce a unique reset-marker cue; physical erasure can also change opportunities and noise. These alternatives need controls when translating this toy. Common random arrays across arms provide paired comparisons; separate arrays for causal-role draws prevent the noisy-echo within-step coupling defect.

Reproduce with `python experiments/imperfect-reset-carriers.py`. Full per-condition accuracy, analytic expectation and standard error are in evaluation/results/imperfect-reset-carriers.json. This is execution plus analytic agreement for designed pathways, not proof of emergent external memory or successful AI swarm reasoning.

## API separation and independent inspection

Writer, reset controller, reader and scorer are now distinct pure functions with explicit inputs. Only the writer and scorer receive the target bit. Reader receives carrier arrays, known read mixture and noise arrays; it has no target argument. Changing the entire environment bit array leaves q=0 reader outputs identical; changing the entire private bit array leaves q=1 outputs identical. Refactoring reproduced every prior per-condition record and paired contrast exactly. This is designed API separation, not independent development of autonomous agents.

A separate agent inspected formulas, draw semantics and paired standard error and found no implementation bug. This review shares the research context and is not independent replication. One seed and 72 correlated arms do not constitute 72 independent experiments. Six-SE assertions are numerical checks, not guaranteed events for every possible random seed.
