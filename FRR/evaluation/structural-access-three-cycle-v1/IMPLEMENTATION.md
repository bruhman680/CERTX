# Frozen implementation contract

`experiment.py` implements `PROTOCOL.md` using NumPy and the Python standard library. It has not been executed as a numerical experiment by the engineer. Syntax was checked with `python -m py_compile experiment.py`. The root runs once after prospective reviewer approval:

```bash
timeout 180s python experiment.py --output run
```

The script sets the usual BLAS/OpenMP thread environment variables to 1 before importing NumPy. It refuses to overwrite a directory containing `ATTEMPT.json`; an interrupted or failed attempt therefore remains distinguishable. Every output includes a copy of the executed source and protocol. The source presented for initial static review is preserved as `experiment_INITIAL.py`; any prospective correction must retain it and document the difference.

## Generation and reuse

Each seed creates five independent `SeedSequence.spawn` streams: latent, rotation, training noise, reserved zero calibration noise, evaluation noise. Evaluation and calibration each have their own entity and time vectors; the predicate vector is shared. Contexts are normalized sums of the corresponding real unit entity, time and predicate vectors. Bindings are independent real unit vectors per entity/time. All raw Gaussian draws and normalized vectors are saved. Training context/binding vectors are independent draws, not composed entities. Candidate order is entity, then time, then status A/N/U.

The 32 queries per seed/r/evaluation-noise condition are 16 entity/time claims with two numbered repetitions each. The query noise bank has 32 independent complex isotropic unit vectors and is reused across r, eta, Q, methods and supervision conditions. Zero-noise repetitions retain distinct IDs and identical arrays. Training member noises are independent per A/N member, reused when scaling eta_train and across Q; m selects nested prefixes. The calibration noise stream is reserved but draws no samples because calibration eta is exactly zero.

Each seed generates one sign-canonicalized QR matrix and the fixed context-0/binding-0 plane rotation. All methods see the same transformed actual query and candidate arrays. Real Q acts on complex vectors with row representation `x @ Q.T`. The estimated projector uses the top fixed `min(m,12)` complex left singular vectors of the uncentered difference columns, and `U @ U.conj().T`. No renormalization follows training noise. There is no outcome-dependent fit or rank selection.

## Decoder and metrics

A projected column vector P x is represented by row `x @ P.T`, including a complex estimated projector. Each projection is normalized; inner product is `q.conj() @ w.T`. Projected norms and normalized product magnitudes use the declared 1e-10 validity threshold. Calibration uses eight clean A-reference rows and their matching three status rows. Each status centre stores the complex circular mean, whose magnitude is the resultant concentration. An absent or zero-resultant centre triggers global calibration_unavailable. Otherwise nearest circular angle is decoded, with the fixed tie threshold and separate zero_product reason.

Retrieval ranks all 48 candidates by modulus with stable index order for exact score ties, returning three actual records. Gold claim/status enters only after retrieval and decoding. Evidence recall is relevant returned count/3; joint recall additionally requires correct decoded status. Complete means all three. Encoded-U recall is 1 only when the gold U record is returned and decoded U. Oracle-relevant stance accuracy scores the three relevant candidates independently of retrieval; abstentions are errors. Ledger records include returned IDs/indices, scores, angles, predictions, reasons, relevant-only predictions/reasons and metrics.

## Saved artifacts and audit boundary

`inputs.npz` and `INPUT_MANIFEST.json` are written before fitting, retrieval, decoding or scoring. They preserve all raw draws, candidate/query banks, noisy/clean training pairs, Q matrices and per-array hashes. `structures_centres.npz`, structural/algebra diagnostics, and `QUERY_MANIFEST.json` are written before scoring; `PRE_SCORING_CHECKPOINT.json` hashes that boundary.

`LEDGER.jsonl` has 27,648 method records. `PAIRED_ROWS.jsonl` has 6,912 paired query conditions linking four method-record indices. `AGGREGATES.json` provides counts, sums and means for every complete method condition. `INVARIANCE.json` compares every full/oracle transformed condition with its matching noisy identity condition: all candidate scores, top-three sets/order, predictions/reasons, metric differences and near-boundary gaps are retained without forcing agreement. `SUMMARY.json` includes actual unique query hashes and maximum identity errors. `OUTPUT_HASHES.json` hashes durable outputs. `ATTEMPT.json` marks start/completion; a crash leaves the started marker intact.

Algebra controls concatenate evaluation candidates, calibration candidates (including A references), actual noisy queries and clean/noisy training banks. They check full and oracle Gram products/norms, Q orthogonality, and the independently calculated real A+iB formula. Structural diagnostics include Hermitian/idempotent/transport errors, numerical difference rank at 1e-10, retained rank, all singular values, cutoff gap/tie flag, principal-angle cosines and normalized Frobenius projector distance. The naive fixed mask has the same Hermitian/idempotent identities as the saved constant P, and full I is exact by construction. No invariance mismatch is suppressed; cutoff ties are reported rather than treated as a unique equivariant fit.

The fixed bank contains 48 underlying evaluation entity/time claims over seeds, and 384 generated query IDs. Each base query participates in 72 method records: three Q, six supervision settings, four methods. Full/naive/oracle repeats across six settings are duplicate controls; zero-noise repetitions are duplicate arrays. These counts provide no independent replication or statistical inference.
