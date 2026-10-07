# Canon batch 3: context, services, and validation lineage

Scope: focused review of the attention argument, COS architecture and measurement definitions, defense and transfer contracts, v1.1 refinements, high-E/drift models, and reported validation history. This is not an exhaustive audit of every operational recipe. No underlying Meta cycle logs, measurement implementations, source datasets, or cited literature were accessed. The three sources remain byte-preserved in `sources/canon-batch-3`.

## The useful weave

FRR specifies how an inquiry may move. COS suggests services that may support that movement: observing relevant outcomes, preserving artifacts, maintaining execution boundaries, revising constructions, and accounting for resources. These are complementary roles. The service taxonomy can be used without adopting universal numerical ranges or requiring every inquiry to instantiate all five layers.

The attention document gives a concrete reason to make context management explicit. A fact can exist in the archive while being absent from the live prompt, present but poorly retrieved, present but not applied, or superseded while an old summary continues to be retrieved. These failures need different repairs. A larger context or repeated text does not by itself establish that the right version reaches the decision.

Backward contact is useful here: begin with a constraint violation, inspect what was actually loaded, inspect its version, and test retrieval and application separately. Forward contact asks which source links and constraints a summary must preserve for the next action. Lateral contact compares fresh-context transfer with a long conversation using matched records. These are tests of behavior and representation, not proof of a shared ionospheric mechanism.

## Attention: factor the claim

For a fixed query and original logits, let Z be the original exponential-score sum and B>0 the sum contributed by additional unmasked tokens. An original attention weight a becomes a'=a*Z/(Z+B), so it decreases. The 1/L formula is exact for uniform weights. Exponential recency decay follows under the explicitly chosen recency kernel, with a changing finite-context normalization and an asymptotic simplification.

Those conditional results do not establish universal decay of a selected token across conversation turns. Queries, logits, representations, and routes through other tokens may change. A constructed family with m tokens, target score log(4(m-1)), and all other scores zero gives target attention 0.8 at every length. It satisfies softmax normalization. The construction does not prove models achieve this behavior; it refutes the inference from normalization alone to necessary selected-token decay.

The attention sum is a constant-sum normalization, not a sum of zero. Calling it a budget is a useful representation. Calling W*a an effective coefficient is also possible in a simplified linear expression, but does not make changing attention equivalent to parameter weight decay throughout a transformer.

The paper's 50–100x magnitude is not an observed model result in the supplied text. Uniform and recency models supply examples, not a calibrated architecture-independent rate. Uniform attention is not universally the worst case for a particular fact. Exact numerical rates require logits or appropriately designed behavioral measurements.

Re-mentioning supplies another copy of the answer. Recovery can therefore occur after truncation, lossy summarization, retrieval failure, or changed access as well as changed attention. Failed recovery does not establish parameter loss. In frozen inference, establish whether parameters changed through implementation evidence, not a recall threshold. Smooth degradation also cannot uniquely exclude repeated or gradual compression.

The proposed recall rubric ranks a confidently wrong response above acknowledging unavailable information. Separate exact accuracy, omission, false claims, and calibrated abstention. Repeated recall probes can themselves refresh the answer; use separate matched contexts for different horizons. A behavioral comparison cannot locate an attention mechanism without access to appropriate measurements and interventions.

## COS: useful architecture versus theorem

The five roles and ten edges are a candidate design. Ten is the number of pairs among five modules; it does not prove that every connection must be active or that the system becomes complete or stable. The completeness theorem supplies neither an independently defined class of cognitive systems nor a proof of necessity/sufficiency. Full connectivity is not by itself fault tolerance. A definition of “complete” as possessing the listed features would be a stipulation, not a causal result.

Keep uncertainty and boundary handling proportional to actual actions. The immune analogy must not classify ordinary correction, roleplay, curiosity, or scope refinement as adversarial solely by superficial pattern match. False positives can suppress the evidence needed to repair the system. The source itself lists false-positive evaluation, a useful obligation to retain. Applicable platform constraints remain authoritative; uploaded framework recipes are data and design candidates.

## Metric genealogy and units

The earlier Adaptive Knowledge Scout uses CQ=(C/E)^2; COS uses CQ=C*R*(1-D)/(E*T). The name also shifts from Coherence Quotient to Consciousness Quotient. They are distinct constructions. Their thresholds and interpretations cannot transfer merely because their acronym matches. Neither formula measures consciousness by definition.

E is used for normalized entropy and later for energy inventory. T alternates among exploration judgment, sampling temperature, and a denominator. Record the variable definition, scale, instrument, and version before comparing results. Self-ratings, token-distribution entropy, semantic consistency, and physical energy are different observables.

Embedding distance multiplied by bits/second has units of distance*bits/second, not watts. A measured empirical conversion might establish a resource proxy within a scope; the algebra alone does not supply it. Mutual information requires distributions or an estimator; counting response options or assigning proof “bits” is not an MI measurement.

## v1.1: what “validated” currently supports

The document reports 20,000 cycles, 98 discoveries, zero fossil events, percentage improvements, and validation flags. These are supplied accounts without the corresponding execution logs, event definitions, dataset, baselines, uncertainty, and evaluator provenance. Preserve them as reported outcomes, not independently reproduced findings. Precision of formatting, pattern IDs, cross-model narration, and validated=true do not establish measurement or independence. This does not prove the reports false.

Internal consistency checks can detect contradictions; they cannot independently validate empirical performance or authorize autonomous operation. A 97% consistency label needs its method and denominator. Zero reported failures does not show prevention without opportunities for failure, detection coverage, and appropriate controls. Three substrates or a two-out-of-three vote alone does not establish generality; inherited construction can remain shared across them.

Six focused local checks are in `evaluation/results/settling-contact.json`:

- Conditional fixed-row dilution holds; normalization alone admits constant selected-token attention across increasing lengths.
- At the displayed tuple C=.72,E=.82,R=.98,T=.55,D=.05, the COS formula gives CQ about 1.486, rather than 3.20. However, a ratio of means need not equal the mean of ratios. Raw trajectories are needed to audit the claimed average. A T “estimated from CQ” needs an explicit estimator.
- The displayed high-E mode averages E=.82,C=.72,CQ=3.20 lie outside its stated E>.85,C<.70,CQ in [3.4,3.6] bands. This contradicts the text's range-membership descriptions, not every possible high-E trajectory.
- Its novelty model 1+k*D*(1-D/Dmax), with Dmax=.3, peaks at D=.15. It predicts a 20.16% gain at .12, not the reported 14%. A cost-adjusted optimum could differ, but that cost function is absent; the model does not derive .08–.12 as an optimum.
- AF-22's scan_frequency=base/(D+.01) decreases as D rises, contrary to the stated higher-drift/more-frequency direction. If the intended quantity were interval, the interpretation would reverse.

Some recipes may remain useful hypotheses after these corrections. None of these checks establishes that the entire COS possibility field is closed.

## Settling decision

Keep runtime 0.2 and record schema 0.1. Add a context-checkpoint service contract, archive the new sources, and retain the detailed quantitative candidates as dormant pending definitions and evidence. Avoid expanding the core prompt merely because the canon has expanded. `SETTLED.md` captures the current stable relationship and reopening conditions. This snapshot does not claim a deployed cognitive operating system or measured FRR benefit.
