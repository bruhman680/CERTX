# Independent rival review / sandbox, not official Cycle2

This sandbox was proposed and run under the root's request for exact calculations; official Cycle2 selection/protocol/execution is reserved for after Cycle1 results. Its files do not modify SR-C1 or Cycle1.

## Counterexample

Let E_A/E_S denote erasing the two coordinates. With marginal rates rA/rS and q=P(E_A=1,E_S=1), event probabilities (neither,A-only,S-only,both) are `(1-rA-rS+q,rA-q,rS-q,q)`. Feasible q is `[max(0,rA+rS-1),min(rA,rS)]`.

The joint-survival coefficient is `J=P(E_A=0,E_S=0)=1-rA-rS+q`, and therefore `max(0,1-rA-rS) <= J <= min(1-rA,1-rS)`. First-outcome contrast is `D=(1-rA)a+(1-rS)b+J*c`. Additive response is unchanged by this dependence. Interaction response is not.

Same marginal witnesses identify only rA/rS. A known nonzero coordinate-pair preparation observed through direct access on the same reset run can identify J, conditional on witness validity and state-independent reset-event law. Separate coordinate witness samples cannot recover correlation even with unlimited data. A witness sharing an access gate can report missing data when coordinates remain; missing access must not be coded as erased state without a separate control.

## Exact sandbox results

Using SR-C1 mixed_interaction with a=.064,b=.072,c=.0331941, independent and correlated resets have identical marginals. Fit the independence-assumed three-component model on sham/agent/soil; all three cases interpolate those three equations to numerical precision. Positive coupling nevertheless biases a/b each by+.0008971 and c by-.0017943, then mispredicts out-of-fit shared response by-.0075360. Negative coupling biases a/b each by-.0035886 and c by+.0071771, then mispredicts shared response by+.0035886. Independent control predicts within7e-18.

Thus training fit cannot validate reset independence in a saturated design. A out-of-fit operator helps reveal the mismatch here. It is not a general identifiability theorem: another violation could cancel at the selected holdout. Use several useful out-of-fit operators or verify the joint law when consequential.

Joint-survival witness coefficients recover a,b,c within floating-point precision in all three selected cases. Fréchet bounds widen the shared-row prediction enough to cover all three selected cases, but do not identify their actual dependence. These example intervals are conditional sensitivity envelopes, not calibrated frequentist confidence intervals or a general guarantee about fitted contributions. Marginal uncertainty and parameter uncertainty would need propagation for a noisy study.

## Recommended official Cycle2

Freeze additive versus interaction stress, retain marginal rates from Cycle1, then compare independent / positive / negative coupling; train on sham/agent/soil and check on shared. Contrast naive independence, calibrated joint witness, and Fréchet sensitivity. State that interventions are state independent and witness access is stipulated. Report both fit and out-of-fit errors; do not attribute terms to new physical carriers. No gate-erasure conclusion without an independently accessible witness or restored-access control.

## Development disclosure

The shared-row results were inspected during this sandbox before official Cycle2 selection. They are out-of-fit checks, not sealed confirmation. Legacy RESULTS.json field names containing held_out refer only to rows excluded from the algebraic fit. An initial in-memory sensitivity supplement failed JSON serialization on a NumPy boolean before writing; supplement.py converts the flag explicitly, preserving the original RESULTS.json and writing SUPPLEMENT.json separately. No model values were retuned.
