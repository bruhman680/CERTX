# Scout: substrate as a temporal channel

Date: 2026-10-05. Status: literature contact and proposed experiment, not empirical validation of the FRR seed.

## Surviving relationship

A present substrate can carry a dependence on earlier inputs that a newly instantiated reader can use. The reader need not have existed when the input occurred. Calling this a channel across time does not imply backward causation, nor that every earlier distinction remains recoverable.

Three things must be separated: dependence retained by the substrate; information accessible through the permitted observation; and inference performed by the reader. A sophisticated reader can supply priors that make an ambiguous trace appear specific.

## Primary contacts

### Boyd and Chua (1985): fading memory and faithful finite-history approximation

[Author-hosted paper](https://web.stanford.edu/~boyd/papers/pdf/fading_volterra.pdf).

The formal notion says, roughly, that inputs agreeing sufficiently in the recent past yield close present outputs even if they disagree in the remote past. Their approximation results require stated signal classes and continuity with respect to a fading weighting of history. In continuous time the displayed signal class is bounded and slew-limited; their discrete-time results include nonlinear moving-average approximation. The peak-hold counterexample is especially useful: a permanent earlier maximum does not satisfy fading memory and cannot be uniformly approximated over all time by the same fading-memory class.

Contribution: a precise boundary for when history can be compressed to a recent window. Limit: fading memory is a property of the input/output map, not a diagnosis that the carrier is a static mark rather than ongoing dynamics. It does not establish a universal transition from wake to law.

### Dambre et al. (2012): what a later reader can recover

[Published paper in author institution repository](https://biblio.ugent.be/publication/2972574/file/2972575.pdf); [publication record](https://biblio.ugent.be/publication/2972574).

They measure capacity through optimal linear reconstruction of functions of past inputs from current accessible dynamical variables. Under their independent-identically-distributed input protocol, orthogonal target functions and moment conditions, summed capacities are bounded by the number of observed variables in the infinite-data limit. Equality additionally needs fading memory, a full-rank correlation matrix, a complete function basis, and the stated initialization/data limits.

Contribution: delayed linear reconstruction and nonlinear functions of history can be measured separately. Limit: this normalized capacity is not Shannon capacity in bits, does not recover every history uniquely, and is not a finite-sample guarantee. A finite experiment needs held-out scoring and rank/conditioning checks. Several lagged targets derived from correlated inputs can appear recoverable through correlation alone, hence the independent-input protocol matters.

### Gonon and Ortega (2020 preprint / 2021 publication): approximation with a well-defined reservoir state

[Primary full text](https://arxiv.org/html/2010.12047v1); [abstract and publication links](https://arxiv.org/abs/2010.12047).

Theorem 2.1 gives uniform approximation of causal, time-invariant fading-memory filters on uniformly bounded semi-infinite inputs by echo state networks that themselves have echo-state and fading-memory properties. The activation must be bounded, nonconstant, and Lipschitz-continuous. The paper explicitly repairs a gap in an earlier universality result: approximation alone had not guaranteed those properties in the approximants.

Contribution: a substrate-like recurrent state plus a static linear readout can express a large class of temporal relations without a reader carrying its own recurrent history. Limit: an existence theorem does not guarantee a randomly chosen reservoir, a successful training procedure, permanent storage, or unchanged control behavior under transplantation. The repair paper inherits the preceding research program; these sources are related genealogy, not three independent experiments.

## Proposed distinctions and tests

Represent the substrate provisionally as z[t+1] = A z[t] + B u[t], with a fresh readout y[t] = C z[t]. For an isolated input, its later contribution is C A^k B u. This formula is our illustrative linear-model derivation, not a claim that the cited physical systems share this mechanism.

- **Transport:** the distinguishing contribution changes location. A local sensor may lose access while another location gains it. Whole-domain retention and local observability differ.
- **Retained mark:** the contribution stays locally accessible after the travelling driver leaves. Continued refresh is not required over the tested horizon.
- **Maintained pattern:** feedback or an external driver continually reconstructs the distinction. Interrupting maintenance tests this explanation; disappearance alone does not distinguish destruction of storage from removal of the reader's access.

These modes can coexist. An active travelling pattern can itself carry memory. Therefore transport-versus-memory is not a universal dichotomy; the question is whether persistence is carried by transport, a residual mark, maintenance, or their interaction.

Run randomly prepared message histories through a substrate and instantiate fresh readers at increasing lags. Train linear readouts on calibration runs; evaluate once on independently generated held-out histories. Include direct past-input reconstruction and nonlinear targets such as products of two earlier independent inputs. Keep all observer logs inaccessible to future-only readers. A paired comparator may receive before/after records, but must be labeled as a different information condition.

Compare intact evolution with: no writing; substrate reset; removal of the travelling disturbance; maintenance interruption; spatially relocated readers; and a substrate transplant into a fresh actor. Match initial conditions, noise draws, and observation resolution where feasible. Test software snapshot noninterference by replaying identical trajectories with and without snapshot collection. This certifies that implementation only; physical probes need a separate coupling assessment.

Important rival: unknown initial substrate preparation can produce the same final field as the tested event. Future-only readers cannot generally resolve that inverse problem. Independent initial preparations, randomized messages, no-event replays, and held-out decoding reduce this confound without guaranteeing unique retrodiction.

## Next contact

The useful near-term experiment is a lag-by-location decoding map with driver removal and maintenance interruption. It can distinguish disappearance from a local observation window, degradation of accessible information, and dependence on continual reconstruction. Do not infer a physical entropy cost, crystallization threshold, or fundamental law from decoding alone.

## Retrieval limits

Direct Nature retrieval for Dambre failed; the full published PDF was read through Ghent University's repository. Boyd/Chua and Gonon/Ortega primary full text were accessible. A Jaeger report was located and opened but its extracted text was poor, so it is not used for theorem claims here. No claim of exhaustive literature coverage or novelty is made.
