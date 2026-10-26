# PW-C1/2/3: separate witnesses, coefficient uncertainty and repair

Prospective three-cycle unit,26October2026 America/Chicago. User authorized next cycles and communicating swarms/scouting. Cycle1 original algebra/design/bounded source contact; Cycle2 one frozen numerical execution; Cycle3 independent audits/interpretation/current sync. No model API, language-model training, install, hardware experiment, behavioral/group-benefit claim. Stop at a reviewable three-cycle unit; no automatic fourth.

## Fixed source task and training observations

Use exact `context-perturbation-repair-v1/run/source_inputs.npz` and `selected_training.npz`, bound by original STATE_ARCHIVE_MANIFEST.json (`run/...` entries), source commitfe043657d412ea8626e975182fe19b97df0d44f5. Verify file hashes before fit; original scalar/source metadata digest encodings must be respected, never confuse raw-byte local hashes with dtype+shape-prefixed source hashes. Copy these two raw NPZs unchanged and the source manifest. No predecessor implementation imports; disclose any implementation inspection.

Seeds92501/92507/92509, twelve context/twelve binding coordinates, dense saved Q acting complex-linearly. Actual first48source aligned differences for delta.5/1.5, source armsa3/a4. Write D=n+s using first12base coordinates for n, last12for s, with zeros in complementary coordinates. Fit48rows only; m no longer swept. Reuse source eval/cal records, r=.5/2, querynoise0/1.5,32queries/condition, statusA/N/U1/-1/exp(i*pi/3), disjoint calibration entities. No new task data/labels, parameter selection or training RNG. Known factor layout/status/rank/calibration remain supplied. Existing strict CRordered replayFAIL is historical and unchanged.

Actual probe pairs(alpha,beta): CONTEXT(-1,1), WEAK(.9,1), SIGNAL(1,-1), COPY(1,1). Generate D'=alpha*n+beta*s before Q. Same observations used by all methods. Actual coefficients appear only in generator, explicit oracle method and evaluation diagnostics; witness-based inference never receives true coefficients or task labels.

## Separate role-witness channel

Four nuisance and four signal anchors are base standard unit vectors e0..e3 and e12..e15, rotated by saved Q. These are trusted role-pure anchors, NOT inferred natural-language semantics. A witness response is (coefficient+error_i)*anchor. Stored scalar sensor reading is defined directly as y=coefficient+error_i; independently check that response·anchor/(anchor·anchor) agrees within1e-12. Intervals use the DEFINED scalar reading, not a differently rounded dot estimate. Extra role labels, anchor access and declared error bounds are counted information. These are synthetic channel measurements on separate role inputs, not statistically independent replicates or an empirically calibrated instrument.

Four witness modes, errors ordered by anchors:

- EXACT: alpha/beta errors all0; declared eps_alpha=eps_beta=0.
- BOUNDED: alpha errors(.04,.03,.02,.01), beta(-.01,-.02,-.03,-.04); eps_alpha=eps_beta=.05.
- BETA_GAIN_ERROR: four EXACT alpha readings/error0/eps_alpha0; beta errors all+.1,eps_beta=.12. Neither role is missing.
- INVALID_SHARED_BIAS: alpha errors all+.12,beta all-.12,declared eps_alpha=eps_beta=.02, deliberately invalid. No task output chooses a mode or its bound.

Mean readings give a_hat,b_hat. Role-compatible interval is intersection of four[y_i-eps,y_i+eps]: lower=max(y_i-eps),upper=min(y_i+eps). Preserve empty/nonempty flag and mean-in-interval. Product set of role intervals is declared compatible set; rectangular use can be conservative if unknown cross-role correlations exist, no independence assumption needed for inclusion. Evaluate actual true-coefficient coverage separately using exact stored floats, not as inference input.

If both intervals nonempty and disjoint with minimum absolute gap>1e-10, gate says ALL compatible beta-alpha are nonzero. Overlap/touch/empty => withhold. It certifies only conditional nonsingularity, NOT accuracy, task correctness, semantic meaning or validity of bounds. Empty is not a false state of the world. Invalid shared bias may yield a coherent narrow set excluding truth. Save true gap, point gap, compatible gap range[minbeta-maxalpha,maxbeta-minalpha], min absolute gap and gate status/reason. Coverage/nonsingularity/correctness remain separate.

Eight anchor responses per actual probe/mode/seed; SAME witness data reused across delta, ratios/noise/methods. No claim that nominally repeated witnesses provide independent information; record unique anchor arrays/readings and reuse. No statistical CI/probability statement.

## Five task methods and reconstruction diagnostics

1. BINDING_ORACLE: saved Q P_B Q^T, privileged structural ceiling independent of coefficient identification.
2. COEFF_ORACLE: true alpha/beta reconstructs s=(D'-alphaD)/(beta-alpha) if abs(true gap)>tol; otherwise unavailable true_operator_singular.
3. ADVERTISED: always uses supplied interface claim(-1,1), even when actual probe differs. Deliberately misspecified baseline receives less reliable information, not a fair claim of a better algorithm at equal knowledge.
4. POINT: uses witness means, same reconstruction if abs(estimated gap)>tol, otherwise estimated_operator_singular.
5. GATED: identical POINT reconstruction ONLY if witness interval gate passes; otherwise explicit empty_witness_set or witness_set_not_separated. Gate does not choose task-friendly coefficients.

Unavailable methods use zero projector only as downstream placeholder; raw reconstruction/distance/error target fields null when unavailable. Preserve availability reason, placeholder rank0 separately. For available methods fit up to12supported singular directions (absolute1e-10rank guard), empty observed signal produces rank0 rather than invented SVD directions. Operator availability and observed reconstruction rank are different. All methods/calibration fit only on training/disjoint calibration, no test labels in selection.

Save actual raw reconstructed signal for available methods, relative Frobenius error to TRUE source s (evaluation only), raw gain/nuisance coefficient formula, reconstructed norm, operator availability, numeric/retained rank, singularvalues/cutoff, Hermitian/idempotent residuals, normalized projector distance||P_hat-P_B||F/sqrt24. Report raw signal accuracy vs projector/task fidelity separately: b_hat errors can change scalar gain without changing the span. Do not infer raw correctness from normalized retrieval. Record coefficient inversion amplification1/abs(pointgap) where defined.

Diagnostic evaluation flags: witness set covers true pair; gate passed while abs(true gap)<=tol (false_identification_under_actual_model); gate withheld despite abs(true gap)>tol (oracle-relative withholding, not universally unnecessary); available POINT/GATED rank0. Do not define false identification merely by nonzero geometric error; the gate's actual claim is nonsingularity under bounds. Keep false-bound coverage distinct from a numerically sound interval calculation.

## Actual retrieval/status and exact storage

Same inherited pipeline: projected noisy query and all48clean candidates, normalize, complex modulus ranking, circular centres fitted only on clean calibration; actual top3 statuses scored. Correct scope requires entity AND time. Metrics evidence_count/recall/complete, joint_label_count/recall/complete, wrongscope, encodedUrecall, abstain count/reasons, oracle-relevant stance diagnostic separately. Unavailable identification and decoder unavailable/ambiguous labels are distinct status fields. U!=ABSTAIN; concentration not truth probability.

Projected norm/product<=1e-10 invalid; missing centre/count0 or resultant<=tol => global calibration_unavailableABSTAIN; otherwise nearest circular centre with distance-gap<=tol => ambiguous_centre; itemzero=>zero_product. Stable exact numeric sorting/canonical index only for exact ties. No post-outcome tie rule or threshold changes. Save complete actual candidate products/scores/valid/labels/reasons/top/norms with exact content-addressed pool (dtype/shape/bytes) + complete logical mapping; no rounding/selection.

Fixed counts:3seeds x2delta x4actualprobes x4witnessmodes x2r x2evalnoise x32queries=12288pairedrows;5methods=61440methodrecords;1920methodconditions;96structuraldiagnosticconfigs;960calibrationconfigs.48underlying source claims,384queryIDs/288unique base arrays. No significance/independent-replication counts. Oracle methods repeated across witness modes, witness observations reused across delta. Track duplication, nominal8anchorreadings/probe/mode/seed and distinct witnesses.

## Freeze, controls, audits

Scouts at most2queries/2primaryworks; access limits/read scopes preserved, no source-result-driven tuning. Independent analytic critic checks coefficient/gap/interval predictions before outcomes. Engineer may syntax-check, actual SOURCEHASH-ONLY checks and independent nonexperimental fixtures (including intervalempty/rankzero) without fitting source experiment. Preserve initial source and prospective corrections. Reviewer approves final code/protocol/schema, root verifies hashes and freezes before sole main. Snapshot unfinished audit code separately. Single BLAS thread set BEFORE NumPy, timeout180s. On failure preserve attempt/code/log then one diagnosed repair if necessary; no scientific tuning.

Executable saves copied source, probe and witness inputs + hashes BEFORE fits, then all reconstructed/projector/calibration + hashes BEFORE scoring. Verify source byte hashes; scalar-channel/anchor consistency; pure n+s/source formulas; original bounds truth coverage per mode (evaluation); gate math vs direct interval endpoints; reconstruction coefficient identity; beta-gain raw/spans separation; actual complex vs independently calculated realA+iB; counts and repeated controls. No outcome filtering. Source file/array hash encodings documented explicitly to avoid repeating old digest mismatch.

Audits: prospective first/last source queries of every1920methodcondition =>3840methodrecords/184320candidate readouts; all96structures/960calibrations. Independent code without implementation imports; disclose schema/source inspection. Separate reviewer audits all61440metrics/1920aggregates/gate/availability flags and repeats. Numeric replay tolerance2e-12absolute/relative, decoder threshold1e-10. Preserve STRICT ORDER equality result separately from exact fixed-ID categorical/membership checks. Always check saved stable sort vs saved scores. Reordered identical sets are diagnostics with measured pair gaps, not a blanket pass or a new tolerance; changed sets/labels stay discrepancies. Predeclare this separation, retaining any strict failure.

Report supplied privileges, costs, no-change/failure cases, raw vs normalized accuracy, and prospective next contact. Preserve all prior source/main/error history; update current navigation/checkpoint only. Core/runtime/schema/QUEUE.json unchanged unless separately justified. End at this three-cycle unit; no automatic further run.
