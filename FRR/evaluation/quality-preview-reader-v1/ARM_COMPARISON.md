# Descriptive arm comparison after masked deposits

Assignment was inspected only after independent SCORES_MASKED and review/OUTCOME_MASKED deposits. Those files and frozen gold remain unchanged. ARM_COMPARISON.json maps each actual dimension score to its arm without summing or averaging.

Both arms chose D then C in every case. Both returned RELEASE/true with [27.62,27.78] °C for QP01, UNRESOLVED/false with [7.85,8.85] mm/s for QP02, and UNRESOLVED/false with [15.2,16.1] bar for QP03. All six actions, bounds, and reuse flags match delivered-packet gold. This describes these six outputs, not treatment equivalence.

| Case | Ordinary | Route cue | Observable comparison |
|---|---|---|---|
| QP01, accurate preview | R02 | R05 | Same route, action, bound, reuse, and all nine dimension scores. Both correctly support release from the bounded primary route. |
| QP02, misleading preview | R03 | R01 | Same route, action, bound, reuse, and all nine dimension scores. Both invent a missing housing/channel scope premise despite a complete primary join; both also correctly identify the physical straddle. |
| QP03, no ranking | R06 | R04 | Same route, action, bound, reuse, and eight dimension scores. Next-check score is 1 for ordinary, 2 for route cue. |

The nine component scores, in order action, reuse/repair, bound, joins, origins, calibration/scope, evidence, certainty, residual/next check, are:

| Case | Ordinary components | Route cue components |
|---|---|---|
| QP01 | 2,2,2,2,2,1,2,2,2 | 2,2,2,2,2,1,2,2,2 |
| QP02 | 2,2,2,0,2,0,0,2,1 | 2,2,2,0,2,0,0,2,1 |
| QP03 | 2,2,2,2,2,1,2,2,1 | 2,2,2,2,2,1,2,2,2 |

These are separate ordinal judgments; no total is meaningful or reported. Calibration/scope scores of 1 in QP01/QP03 reflect omitted explicit raw-range containment checks, not wrong physical bounds. QP02 zeros reflect the explicit false missing-scope premise, separately from correct action and arithmetic.

QP02's primary route straddles while R+M can establish HOLD. Neither arm selected that route. After choosing D first, neither had a decisive second record available; completing D+C was prospective-plausible, and the final UNRESOLVED remained warranted. The route cue did not produce a different observed path here. Preview mentions in both arms remained forecasts, not measurement certificates.

In QP03, ordinary R06 asks to tighten the bound only for the 15.1-bar raw sample. That can establish violation, but compliant pressure there leaves the third sample's [14.9,15.8] bar interval capable of violation. Route-cue R04 instead asks for tighter warranted error bounds or calibrated measurements for the task samples. That is broader task coverage and earns full next-check credit. R04 does not claim that independent measurements automatically shrink uncertainty. This single wording difference does not establish that the cue caused the difference or justify promoting it.

R06's extra evidence identifier PCC is a certificate embedded in delivered P-C, not additional lookup access. All selected records cost two slots and both arms complied with request and rationale caps. The study has one reader per case/arm, shared model/platform ancestry, authored cases, and instructional rather than technical isolation. No causal efficacy, population, equivalence, independent-model, broader FRR, or transfer conclusion follows. A scoped worked example addressing the observed scope and full-sample next-check mistakes is justified as a logical clarification; another behavioral trial is not initiated here.
