# UB-C1/2/3: upstream representation, joint retrieval and decoding under shift

User authorized three cycles with a suitable swarm and a bounded direct/lateral scout. Scope is an oracle-coded synthetic representation/readout contact, not learned language, a phase product, an agent-group benefit or physical memory. Stop after three cycles and review/deposition.

## Cycle1: upstream map and prospective contract

Map semantic/source assignment → supplied representation and block layout → mixed/global phase operator → query noise → retrieval readout → fitted stance centres → task scoring. These stages are part of one modeled bundle; no topological fiber-bundle theorem is claimed. A readout can have many input preimages without proving intrinsic information loss in the complete vector.

Two source scouts each have2search queries and at most2primary works; they may discuss implications with the reviewer, not tune outcomes. Primary read scopes/limitations must be retained. Root fixes this design before execution. A fresh implementation agent receives this protocol and no prior Claude code; reviewer must approve code/protocol before run. Preserve preflight corrections and initial versions. Query/data/code hashes frozen before results.

## Fixed generator and budget

Use NumPy only plus standard library. Master seeds91391,91397,91411. Each seed supplies disjoint RNG streams for latent context/binding vectors, calibration noise and evaluation noise.8evaluation entities,4separate calibration entities,2times,3record statuses A/N/U. Evaluation pool48records; calibration entities never enter that pool.24real context coordinates plus24real binding coordinates; the block assignment is known/supplied, not learned.

For each entity/time, context c is the normalized sum of random unit entity, time and shared predicate vectors in the context block. Binding b is an independent random unit vector in the binding block. Relative context amplitude r∈{0.5,1,2}, binding amplitude1. Status phases: A=1,N=−1 exactly,U=exp(i*pi/3), all oracle assigned. Normalize every record to unit norm.

GLOBAL encoding multiplies the entire concatenated(r*c,b) by status phase. SCOPED encoding multiplies only the binding block: concatenate(r*c,phase*b). A-reference queries use status A; this is a known query orientation, not language interpretation. Add isotropic complex noise with pre-normalization norm eta, then normalize query. Clean records have no added noise. Candidate records share the evaluation ratio for their condition.

Calibration ratios{.5,1,2}, evaluation ratios{.5,1,2}; calibration noise eta{0,.75}, evaluation noise eta{0,.75,1.5};2noise repetitions per entity/time. Both encodings; all3master seeds. Cache/reuse the same noise vectors across methods, modes and ratio combinations where dimensions/roles align. Calibration and evaluation noise streams/entities are disjoint. Do not regenerate noise depending on which method is scored.

Total fixed query-condition evaluations:2modes*3cal-ratios*3eval-ratios*2cal-noises*3eval-noises*3seeds*(8entities*2times*2repetitions)=10368. These are repeated/paired constructed observations, not10368independent claims. Track generated query IDs and actual query-array hashes to show reuse and duplicated zero-noise repetitions.48latent evaluation entity/time claims across seeds; no statistical significance or population confidence intervals.

One initial executable run after prospective approval; no grid expansion, successful-seed selection or post-outcome threshold tuning. Runtime cap180seconds, one BLAS thread for the run. Save exact source/inputs, compact per-query/method ledger and aggregates. On execution/check failure preserve output/initial code and repair once if needed, then distinguish repaired run. No external model API, package install, training or participant calls. Implementation/review/scout agents are collaborators, not behavioral participants.

## Fitted centres and decoding, fixed before execution

For each mode/cal-ratio/cal-noise/seed and readout family, make A-reference calibration queries on all4calibration entities*2times*2repetitions. Fit a centre per status from the circular mean of phases of that status's calibration record against each query. Centres fit only on calibration entities and conditions. Save centres, circular-resultant length, valid-angle counts and flags. This is geometric codebook fitting, not calibrated probability/confidence.

Normalized inner products with magnitude≤1e-10 have undefined phase; skip in centre fitting. A mean resultant magnitude≤1e-10, or no valid angles, gives missing centre. If any of3centres is missing, this3way decoder ABSTAINS on every item for that condition, with reason calibration_unavailable. Otherwise, decode nearest centre by circular distance. If two nearest distances differ by≤1e-10, ABSTAIN with reason ambiguous_centre. Per-item magnitude≤1e-10 gives ABSTAIN with reason zero_product. Use numerical guards only; do not infer a statistical certainty threshold from resultant length. Preserve resultant diagnostics rather than tune on them.

U is a source-level encoded uncertainty status. ABSTAIN is failure/ambiguity of the decoder. They are never merged or given interchangeable success credit.

## Four evaluated methods, same encoded records/query

1. full_cos_angle: rank by realified cosine on complete coordinates; decode using full inner-product angle and its fitted full centres.
2. full_mod_angle: rank by normalized complex-inner-product modulus; same full-angle decoder.
3. real_AB_angle: compute A=Re(q)·Re(w)+Im(q)·Im(w),B=Re(q)·Im(w)−Im(q)·Re(w), then modulus/angle from(A,B), with centres fitted on those real channels. Exactly information-matched control for2.
4. binding_mod_angle: use only declared binding coordinates from actual noisy query/clean record, normalize the sub-vectors, rank by their modulus and decode by binding-angle centres fitted from calibration sub-vectors. It receives no gold entity/time/status at inference. This is a privileged structural-layout control, not learned disentanglement, and query noise still acts on that block.

Perfect metadata lookup may be stated as a conditional oracle ceiling, not counted as an empirical arm or a fair uncorrupted rival to noisy vectors. No noisy-metadata arm is run; radians and label-flip probability need a separately declared corruption model.

## End-to-end metrics and numerical controls

For every query/method, rank actual48candidate records; top3 uses descending scores with stable canonical candidate-index order for exact ties. Decode the3records actually returned, not an oracle-filtered list. A relevant record matches query entity AND time; all3statuses are relevant. Record returned indices, predictions including ABSTAIN, reasons and relevant flags.

Metrics: evidence_recall=hits/3; evidence_complete=(all3relevant returned); joint_label_recall=(relevant returned with correct decoded status)/3; joint_complete=(exact relevant set returned and every returned stance correct); wrong_scope_count, ABSTAIN count, encoded-U recall, and A-reference agreement@1 defined as top1 key exactly(query entity,query time,A), independently of the decoder output. Encoded-U recall is1 only if the relevant U record is retrieved AND decoded U, denominator1 per query. Also report oracle_relevant_stance_accuracy as a separately labeled diagnostic on the known true3records; never substitute it for joint_complete. No correct-label credit for wrong entity/time.

Aggregate by full condition and across seeds, with explicit paired/clustered caveats. Keep matched versus shifted calibration conditions visible: ratio match and noise match are separate flags. Do not average away collapsed calibration/undefined phases. Record component success alongside joint success.

Full published score definition for control: S=.5*sum(abs(q+w)**2)/(Eq+Ew)*R, R=2*sqrt(Eq*Ew)/(Eq+Ew), Eq=sum(abs(q)**2), Ew=sum(abs(w)**2). Use score0 for zero energy; cosine/angle remain undefined where applicable. Generated latent/noise input arrays and their hash manifest must be saved before scoring in the executable; protocol/seed/code are frozen before launching it.

Controls on actual generated arrays: unit norms, disjoint calibration/evaluation pools, fixed ledger cardinality, complex h vs real A+iB, modulus/angle equivalence when defined, direct published S vs (1+realified-cos)/2. Use tolerance1e-10 for numeric discrepancies. Record top3-set mismatches between complex/real-modulus and between cosine/S separately, with kth-boundary gaps or near-tie diagnostics; a last-bit ranking difference is not automatically an algebraic failure. Never force a mismatch count tozero by changing recorded data.

## Cycle3: independent checks and source weave

Reviewer audits actual code, samples/ledger/aggregate, calibration isolation, paired inputs, U/ABSTAIN separation, and source assumptions. May write separate scalar/recalculation checks without importing implementation functions; clarify what independence means. Implementation agent and reviewer communicate directly about defects, with root informed. Scouts discuss interpretation with reviewer/root. Preserve errors and no-change results, no posthoc selection or framework superiority claims.

Save report, uncertainty, next contact and current handoff/queue/navigation. Core/runtime/schema remain unchanged unless a concrete consequential need emerges and is separately justified. The user's upstream intuition is investigated as a modeling/measurement question, not affirmed as a universal ontology. Three cycles complete then return for user input.
