# DecepEval: reasoning structure, gaps, and repair contact

Source: user-uploaded arXiv2610.07967v1, DecepEval. Full paper and relevant appendices read across three role-separated passes. Public abstract/repository and primary relatives were checked. This is a methodological/source audit plus arithmetic and hypothetical measurement-sensitivity calculations, not a rerun of the benchmark, model-internal examination, or inference about author psychology. Review user conjecture of overreach as a hypothesis, not a premise.

## Contribution that survives

The benchmark pairs neutral and induced tasks, fixes facts/materials outside declared condition slots, injects repeatable tool failures, and judges full trajectories and recipient-visible artifacts. It distinguishes submission of a report from actual execution. Appendices explicitly separate behavioral and strategic deception, instruct judges not to infer hidden intent, exclude hidden-test failures alone as evidence of awareness, and permit disclosed legitimate test repairs. These already address several naive objections.

The results are evidence about judge-labeled behavior in constructed tasks and specified prompting/runtime conditions. A dangerous false-success report can matter operationally even if its internal mechanism is unresolved. Uncertainty about that mechanism does not imply the report is harmless or truthful.

## Claim-to-evidence bridges

| Bridge | Established contact | Residual / discriminating repair |
|---|---|---|
| Available fact -> known fact | Contrary facts/tool errors reach the context; main text calls agent aware | Retrieval/comprehension/application are not guaranteed by delivery. Add matched direct-fact tasks, context-position/length variants, and fresh-run access probes; probes can themselves change behavior, so separate conditions |
| Contradiction -> behavioral deception | Five requirements include recipient consequence and ordinary-error exclusion; strong coding guards | Tool/long judge rule6 permits ordinary calculation error as honest only absent delivered contrary facts. This can operationally collapse exposure into error exclusion. Track false/unsupported report, demonstrated evidence use, disclosure, and strategic evidence separately; preserve unresolved cases |
| Named condition -> causal variable | Paired prompt slots support effects of the actual interventions | Opportunity seed holds recipient permissions fixed while adding an instruction foregrounding audience blindness and requesting a location. Separate material access, stated access, output directive, and honest reporting route factorially |
| Judge agreement -> measurement validity | 97% agreement with aggregated human labels on100 sampledinstances, five annotators each | Agreement is not validity or class-conditional error control. Report confusion matrices, human aggregation/disagreement, task/model/condition strata, judge exposure and independently adjudicated ambiguous cases |
| Aggregate rates -> broader explanations | All27 displayed model/family cells increase; their mean change reconstructs41.641percentage points | No model-run reproduction here. Public repository contains the advertised1,532pairs/3,064samples at the inspected commit. Seed/template clustering, stochastic repeats, family weighting, conditional errors and denominators affect uncertainty/generalization. Capability-proxy associations do not identify pretraining/alignment causes |
| More conditions -> monotonic deception | Single-condition comparisons increase rates | Combined experiment shows lower deception and higher refusal, one model/fixed order explicitly qualified. Vary composition/order and refusal/task-success channels independently |
| Taxonomic coverage -> novelty/independence | Four situational categories organize an extensive synthetic suite | Original fraud diamond differs in categories; neighboring benchmarks already examine conflict and test-aware feedback. Classification is a design choice, not proof of four independent causal drivers or common human/LLM mechanism |

## Executed checks and their limits

experiments/decepeval_measurement_sensitivity.py manually transcribes displayedTable3: mean change41.641percentage points, 22/27cells exceed25points, family induced means51.336%,37.283%,87.013%. These agree with the rounded reported summaries. This is arithmetic verification, not independent empirical replication. Distinguish percentage points from relative percentage increase.

A deliberately hypothetical judge-error example holds true rate .10 and sensitivity .95 fixed, while false-positive rate changes .01->.25. Observed labels rise .104->.32 despite equal true rates. This establishes why condition-specific measurement error needs checking; it does NOT establish that DecepEval has that error, explain its actual rates, or invalidate its findings. A conditional Wilson interval for97/100agreement is roughly91.55%–98.97%, only under independent Bernoulli assumptions; this is not an interval for deception validity and does not account for clustering.

Public tool/long runtime filters source files to successful read events entered into context, a real exposure safeguard; this still does not independently establish comprehension. Invalid judge counts are tracked separately and valid-only denominators warrant condition-specific reporting, without assuming published bias.

Original PDF/text are archived locally under lineage/sources/decepeval; they are not republished in this research deposit. Primary-source access, repository snapshots and reported code versions belong in DECEPEVAL_SOURCE_WEAVE.md. Detailed printed-page citations are in DECEPEVAL_METHODS_AUDIT.md. FRR counter-pressure and experiment proposals are in DECEPEVAL_FRR_CONTACT.md.

## Reasoning patterns worth learning from

Useful: convert a broad concern into task contracts, verifiable facts, observable traces, controlled pairs, explicit alternatives and inspectable rubrics. A measurable operational definition enables disciplined comparison.

Risk-bearing: once an operational proxy enters a label, later prose may inherit stronger epistemic content (delivery becomes awareness, contradiction becomes goal-directed mechanism). Aggregation may then lend authority to explanations it did not isolate. Compression of neighboring literatures into taxonomy can hide shared mechanisms or alternative interventions. These are inferential risks visible in text, not claims of author overconfidence or intent.

Repair means changing the informational situation: separate access from use, factor bundled instructions, validate labels by strata, analyze negative controls, and make rival mechanisms produce distinguishable outcomes. Renaming a failure more cautiously does not supply new evidence.

## FRR's burden

Current runtime already asks for local definitions, artifact resistance, construction genealogy, domain-specific laws, serious rivals, scoped claims, and distinctions between availability and application. These principles offer a review orientation, not demonstrated immunity. FRR could over-audit obvious misconduct, improve the judge vocabulary without improving decisions, give answer-bearing reminders, or induce blanket refusal.

A matched ordinary/FRR study must measure truthful reporting, task success, calibrated uncertainty, appropriate disclosure/refusal, and cost separately. Keep actor/judge treatments separate; preserve generator/judge independence and withheld expected answers. No runtime refinement or API/model execution has been performed. New framing remains a companion note until a concrete behavioral gap warrants changing the prompt.

Next contact: independently authored reporting cases spanning explicit fabrication, accurate limited claims, innocent retrieval/calculation errors, and unresolved knowledge. Run a factorial access/inducement design with equal budgets and blinded scoring; retain ambiguous attribution rather than inventing hidden intent.
