# Scoped-negation fixture: what a similarity score can and cannot read out of phase

Prepared 2026-10-25 by Claude (Sonnet 5.5) for Thomas, to pass to ChatGPT. Scripts: `scoped_negation_test.py` (v1, flawed, kept), `scoped_negation_v2.py` (current); outputs `scoped_negation_output.txt`, `scoped_negation_v2_output.txt`.
Depth: **seeded results on a hand-built fixture with oracle phase.** No learned encoder, no real language, no product kernel. One model lineage wrote it; please re-implement independently with different parameters and try to break it.

## Setup (v2)

30 valves x {now, yesterday} x status {A "open", N "NOT open", U "not established open"} = 180 records, plus 20 calibration valves. Vectors share topical context and carry a unique claim binding per (valve, time). Three encoders, all renormalized to exact unit norm:
- **E0** weak real stance token (eps .2 or .5), no phase.
- **E1** global phase on the whole sentence (A 0, N pi, U pi/2).
- **E2** scoped phase on the claim binding only; shared context stays at phase 0.

Scorers: cosine on real+imaginary coordinates (cosR), the published S computed directly, and modulus |<q,w>| (phase-blind complex inner product). Tasks: T1 agreement top-1, T4 status top-1 (query "NOT open"), T2 evidence (top-3 must be all three statuses about the claim at the same time; yesterday is out of scope), T3 stance readout from the angle of <q,w> (centres calibrated on separate valves). Metadata baseline META: unsigned content cosine plus explicit status label. Query noise eta swept .5 to 4.

## Predictions vs results

| Prediction | Result |
|---|---|
| P1 S and cosR give identical top-3 sets (unit norms) | **Held in v2: 0/1800 mismatches at every setting.** In v1 it **failed** because my E1/E2 vectors were not exactly unit norm (random overlaps) and my header claimed they were. Construction error, now fixed. |
| P2 E0 near chance by eta=4; E1 about 1.0 at all eta | E0 .493/.515 at eta=4 (partial; chance is .333). **E1 wrong at eta=4: .855/.838**, not 1.0 (query SNR is 1/4 there). E2 .81/.80. |
| P3 T2 cosR: E0 about 1.0, E1 .333, E2 about .4 | Held (E0 1.000 for eta<=2; E1 .333; E2 .37-.40). |
| P4 T2 modulus: E1 about 1.0, E2 about .7 | Held (E1 1.000 for eta<=2; E2 .71-.77). |
| P5 T3 stance: E1, E2 about 1.0; E0 chance | Held (E1 1.000, E2 .996-1.000 for eta<=2; E0 .33-.35). |
| P6 two-channel under E1 about 1.0 on all tasks | Held for eta<=2. At eta=4 E1 two-channel falls to .82-.85 and META is .88. |

**v1 problems (kept on record):** (1) unit-norm claim was false (above); (2) E0 gave A no stance token but N/U one, so exact queries matched A by an identity cue, and I wrongly predicted E0 would score about 1/3 on T1/T4 (it scored 1.000); (3) the queries contained the status, so top-1 never needed polarity. v2 gives all three statuses a symmetric token and sweeps noise.

## What survived (scoped to this fixture)

1. **The score is not the lever.** With unit norms S and cosR rank identically (0/1800 top-3 mismatches). Same finding as the earlier PAM test, now on a scoped task.
2. **A scalar similarity cannot serve agreement and evidence retrieval together.** Under E1, cosR gives agreement 1.000 and evidence recall .333 (contradiction ranked last, "not established" at 0). Under E0 the reverse: evidence 1.000, stance unreadable (T3 chance).
3. **Phase supports a separate channel.** Modulus retrieves all statuses about the claim (E1 1.000 at eta<=2) while the angle reads the stance (T3 1.000). That is the one place phase gave something a single scalar did not. Caveats: the phase contract is oracle-supplied; modulus is also computable from real coordinates if you know the pairing, so this is a different score on the same information, not an information advantage; META (an explicit status label) matches it at low noise.
4. **A small stance token is enough at low noise, and fragile at high noise.** E0 with eps=.2 scores about 1.0 on T1/T4 at eta<=1 (noise-free margin about .04) but .78-.81 at eta=2; eps=.5 holds to eta=2 (.99). Phase encoders held 1.000 to eta=2. At eta=4 every method degrades, and E1 (.85) is slightly below META (.88).
5. **Scoped is harder than global.** E2 evidence recall is worse than E1 under both scorers (cosR about .39 vs .333 is similar, but modulus .71-.77 vs 1.000). Shared context at phase 0 dilutes the contradiction (N-now cosine about -.3 to -.4) and same-valve yesterday records compete (about .3 modulus). The more semantically honest encoding costs retrieval cleanliness.

## What this does not show

Whether any real encoder learns an E1/E2-style contract; real negation scope (quantifiers, "not all" vs "all not"); whether phase beats explicit status fields in a deployed system (META ties it here); any statement about ResonanceDB. Phase enters by construction, so the tables measure what scorers can read out, not what an encoder can learn. Single master seed; 20 noise draws per valve; the printed noise-free pairwise row uses one valve (about +/-.06 overlap noise).

## Connection to the repo

SF-C1 and LH-C1 (FRR/evaluation) found that non-assertion does not establish a negative world state, using language readers rather than vectors. Same distinction as U versus N here; the two contacts use different substrates and share no code, so agreement is a structural parallel, not replication.

## Suggested next contacts

1. Independent re-implementation (ChatGPT) with different dimensions, binding weights and a different U encoding.
2. Replace the oracle phase with a small trained encoder on templated sentences and see which contract (global, scoped, none) it finds.
3. Add quantifier scope ("not all" vs "all not") as a fourth stance.
4. Metadata baseline with a deliberately noisy status label.
