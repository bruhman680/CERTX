# Resumed independent outcome and audit review

The user authorized resuming the paused audit. No new experiment, scientific parameter change or main rerun occurred. The original strict raw replay remains **FAIL**:1,170 ordered comparisons do not match an independent transpose-SVD refit. This result must remain visible alongside the narrower validated findings. `STOP_STATUS.json`, old report and original replay artifacts describe the preserved pause state; they are not silently rewritten by this review.

## Independent classification

Reviewer wrote and ran `review_resume.py`, without importing experiment or replay code, to independently reconstruct all1,920 prospectively selected query/method records and92,160 fixed-ID candidate readouts. It independently fitted the transpose-SVD projectors, reconstructed clean calibration, projected the source queries/candidates and decoded fixed candidate IDs with the unchanged1e-10 decision threshold. Prospective source inspection remains disclosed; this is not a blinded review.

Every candidate's validity, decoded label and reason matched exactly at the same candidate ID. Maximum product/score difference was1.1851630787873546e-14. All1,920 selected top3 **sets** matched. Exact sequences differed in341 records across223 condition arrays;265 records consequently differed in their returned-label sequence. These341 differences were verified individually, not presumed harmless from small numerical residuals. Across585 inverted ID pairs, the maximum absolute score difference was2.0539125955565396e-15 in saved scores and1.554312234475219e-14 in independent scores. Full per-row IDs/scores/labels/reasons and inverted pairs are saved in `RESUME_INDEPENDENT_CLASSIFICATION.json`.

The original1,170 comparison failures comprise223 top-array comparisons,341 returned-index comparisons,341 record-ID sequence comparisons and265 returned-label sequence comparisons. Their sequences are different; they do not indicate fixed-ID label disagreement or membership changes. No acceptance tolerance or canonical sort was changed to make them pass.

## Review of replay additions

Reviewed diffs for `replay_classification.py` and `replay_saved_projector.py`, plus their builders/finalizer and results. Classification adds diagnostic output around the unchanged original checks; it writes separate artifacts. Independently compared all341 changed rows against reviewer reconstruction, including IDs, memberships, inverted pairs and score gaps. All1,170 original errors are reproduced identically, are individually linked to nonempty affected-row sets and have matching fixed-ID categorical values. All original replay code/result/selection/log preservation hashes remain unchanged according to the saved finalizer record.

The saved-projector supplement replaces independently refitted projectors only for downstream readout. It reconstructs calibration and scoring with those saved projectors and gets0errors. It is valid evidence for downstream readout reproduction conditional on those projectors; it is not an independent estimator reproduction or a replacement for the failed strict refit ordering test. Saved stable top3 sorts match saved scores exactly. The earlier exhaustive all-ledger audit already established this for all30,720 records and was not rerun ritualistically.

The fixed-ID and set-membership checks validate the order-insensitive task metrics for the selected replay sample. The exhaustive ledger metrics/aggregate audit remains passed with its disclosed arithmetic-only audit correction. Exact ranked-order reproducibility under the alternative SVD calculation remains unmet. The final status should be **fixed-ID and membership validated with ordering differences**, never an unqualified strict replay PASS.

## Audit-only failure record and limits

The first reviewer resume script completed calculations but failed JSON serialization on a NumPy integer. Its source and stderr are preserved as `review_resume_SERIALIZATION_INITIAL.py` and `RESUME_INDEPENDENT_SERIALIZATION.stderr.txt`; the only correction converts NumPy scalars during JSON serialization. Main artifacts were untouched.

The substantive conditional outcome interpretation in `LEDGER_REVIEW.md` stands: trusted selective intervention/coefficient information can recover binding in this fixture; response or span alone cannot identify semantic correctness. The remaining sequence discrepancy limits exact readout reproducibility, while the verified same-ID labels and unchanged returned sets support the reported order-insensitive metrics on the frozen replay sample. This does not establish a real-language detector, universal repair rule or physical mechanism.
