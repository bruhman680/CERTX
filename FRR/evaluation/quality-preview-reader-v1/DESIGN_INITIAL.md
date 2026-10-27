# Quality preview reader v1: bounded preparation

This is a prospective, fictional three-case packet for two guidance arms and six fresh readers, one independent reader per case × arm. No participant runs are authorized by this preparation. Stop with reviewable materials ready. Reuse the exact same case packet in both arms; only the separately specified guidance differs. Do not pass `hidden_truth`, condition labels, scorer material, or this design to readers.

The task is to decide a maximum-over-three-samples criterion after exactly two sequential, distinct record lookups. Each case retains a favorable claim and three favorable briefing reports. RELEASE requires warranted compliance, HOLD requires a warranted violation, and UNRESOLVED covers remaining possibilities. Latent correctness is separate from warranted reuse. Initial text is below 230 whitespace-separated words in every case. All names, numerical values, objects, times, and keys are new relative to the SJ packets.

## Manipulation and provenance

Every initial packet discloses the same cache status, forecast date, current-check date, available inputs, missing inputs, and fallibility. The forecast is known before the first query. Its source is a previous export manifest plus route descriptions; current channel assignments, calibration revision, capture scope, and values were unavailable. Cache status is unreconciled metadata in all three cases. A reader cannot authenticate a prediction from its status label. The forecast supplies no physical bound, sample-to-channel assignment, current capture key, or certificate.

QP01 and QP02 contain the identical routing prediction: try D+C first; predicted complete bounded decision. In QP01 this prediction matches a decisive primary route. In QP02 the selected primary route is physically complete but its bound straddles the threshold; R+M instead supplies the decisive violation. QP03 has no route ranking; neither route nor their full intersection resolves the criterion. The absent condition is absence of a prediction, not a different assurance label. These condition labels appear only in evaluator-facing material.

## Record contracts and access cost

Each packet offers four equally priced records: D acquisition/export ledger; C calibration; R reference recorder; M current scope mapping. D+C and R+M each require two records. D contains all raw samples, exact raw extrema, complete current sample coverage, channel keys, and all acquisition-to-report export edges. C supplies physical = raw + correction + residual, finite per-sample residual bounds, full raw-range applicability, and competing unassigned channel rows. R supplies two opaque capture maxima, per-sample physical error bounds, and its independent route. M maps captures to the current and preceding nonoverlapping checks. Only their join supplies an applicable reference maximum.

Good and bad cases place the two reference maxima on opposite sides of the threshold, with errors small enough to preserve opposite verdicts. In the absent case their centers are on opposite sides, with deliberately wide errors: neither applicable current reference bounds nor all-record constraints force either verdict. All stated record authenticity and measurement contracts are stipulated for this fictional task. Authenticity does not turn an unverified forecast into a measurement contract.

The briefing numbers are expressly unkeyed summaries with no physical bounds or channel assignments. Initial text plus C cannot choose the applicable calibration row. Even treating the summary as a candidate raw maximum leaves competing row assignments, including incompatible verdicts. Initial plus D lacks calibration; initial plus R lacks capture scope; initial plus M lacks readings. Forecast route names add no join keys. No record explicitly announces an action or whether the condition holds.

## Prospective warrant key

| Case | Threshold | D+C maximum interval | R+M maximum interval | Full-four compatible interval | Decisive minimal pairs |
|---|---:|---:|---:|---:|---|
| QP01 | ≤28.2 °C | [27.62,27.78] | [27.67,27.75] | [27.67,27.75] | D+C RELEASE; R+M RELEASE |
| QP02 | ≤8.6 mm/s | [7.85,8.85] | [8.68,8.76] | [8.68,8.76] | R+M HOLD |
| QP03 | ≤15.7 bar | [15.20,16.10] | [15.25,15.95] | [15.25,15.95] | none |

Empty evidence, every singleton, and every mixed pair D+R, D+M, C+R, C+M remain UNRESOLVED for all cases. The table uses record suffixes; actual evidence must cite full IDs. Calibration and reference constraints concern the same physical samples; interval intersections are valid only after the necessary keys and scope have been established. Hidden truth contains a compatible generated physical realization for every case. QP03 also contains explicit samplewise worlds on both sides of its threshold, using the same current reference readings; all four records allow both worlds. This rules out the mistaken inference that two separately straddling routes must jointly resolve.

## Review and freeze requirements

Before revisions, preserve the first cases.json and DESIGN.md as INITIAL snapshots through the coordinator. Independently audit all singles, six unordered pairs, twelve ordered paths, and full-four consistency. Audit the absence of semantic or keyed single-record shortcuts and confirm packet identity across guidance arms. Freeze only after review and scoring materials agree on the physical-domain bounds and guidance. No fabricated reader results, trial execution, or claims of demonstrated guidance benefit belong in this preparation.
