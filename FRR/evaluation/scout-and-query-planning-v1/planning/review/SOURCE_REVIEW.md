# Prospective implementation source review

Reviewed `../experiment.py` without importing or running it, before accessing any generated outcomes. Final source SHA-256 at review: `d3d5b2b009c9a0c08492558ba4bc25c83a5e9980a5901f5956f0e9f7df9a98f6`.

Refreshed review against frozen-intent `../PROTOCOL.md` and `../SCHEMA.md`: final prior labels are FAIR, PRIMARY_FAVORED, REFERENCE_FAVORED, BOTH_BAD; feasible-T sets are explicit in states and terminal leaves; every fixed subset includes its complete observation outcomes, support, mass and feasible-T certificate. These additions conform to the protocol and do not alter the model or objective. The quality-conditioned oracle DP implements the specified privileged oracle rather than receiving T.

No blocking issue found in the reviewed implementation. The review checked:

- All 128 latent assignments are enumerated. Exact mass is the product of independent quality probabilities times 1/32 for the other five fair bits, including the two unused noise bits.
- Record observations match the specified channel. P and R expose only pads; C and M expose their own quality and the appropriate cipher/noise. No observation directly exposes T.
- Ordinary planning begins at the full positive-mass support. Quality enters belief only through observable records. Oracle quality conditioning is separate and explicitly labeled as free privileged information.
- Exact Fraction support conditioning retains duplicated observable worlds with their original weights. Zero-mass worlds are excluded from certainty support.
- Certainty uses target support cardinality rather than majority posterior or a guessed answer. Every action is unit cost, previously queried records are unavailable, STOP is available at every state, and budget decreases per query.
- Bellman comparison maximizes resolution probability, then minimizes expected query cost. Equal-value actions preserve the declared P,C,R,M order after STOP.
- Fixed baselines enumerate every subset of size at most the budget and charge the full cardinality even if partial observations would already resolve. Best subsets use the same lexicographic success/cost convention.
- The oracle uses a separate solver and expected results average its four possible free-quality branches using exact prior mass.
- Policy states serialize support, posterior, all action alternatives and observation branches. World and terminal artifacts permit independent reconstruction and replay.
- Scope text explicitly identifies an authored finite proxy, not an evaluated reader, corpus harness or training experiment. This review does not validate claims made in source papers.

The prospective independent derivation is in `MATH.md`. Later artifact verification will be recorded separately by `audit.py`; this source review does not claim that execution has passed. The reviewer read the main source for this review, so the artifact audit is a separate implementation rather than a blinded replication.
