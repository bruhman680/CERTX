# Cycle1 method review

Scope: inspect actual protocol/code/results and independently replay saved contrasts. Same platform/context and stipulated model, not blind research replication or validation of real witnesses. No samples rerun. Numerical details bind to the source SHA in CYCLE1_AUDIT.json; rerun audit if the source record changes.

## Supported

- Union bound: 6 outcome means and 6 witness means with epsilon=sqrt(log(24/.05)/(2n)) gives simultaneous failure bound .05. Pooling the two repeated-arm estimates cannot exceed the maximum individual estimation error. The known-rate comparison uses this conservative outcome radius as declared.
- Continuous interval: under full column rank, the estimate error equals a left inverse applied to outcome contrast error plus coefficient error times the true contributions. Using |a|<=.2, |b|<=.4 yields the stated 2epsilon+.6epsilon bound. It is conditional on those bounds, independence/validity of witnesses, operator semantics and the additive response model.
- Separate candidate-set replay and normal-equation allocation replay agree with saved artifacts. Published summaries reflect the saved rows.
- Population-confounded designs always withhold generic continuous allocation. This is consequential: noisy redundant calibration matrices are numerically rank2 in2338/2400 cases. Sampling fluctuations do not create genuine population identifying information.
- Equal measured-draw budgets hold: each underlying dataset has6n outcome draws and6n calibration draws. There are4800 underlying datasets and14400 inference records because three calibration modes reuse each dataset. Unique scalar draw total is213,120,000; it is not three times that total.

## Required clarification / bounded repair

1. `point_identified` is a finite-library singleton flag, not a claim about arbitrary continuous allocation. Reports must use the latter distinction explicitly. At n10000 the diverse finite-library classifier identifies all fixed candidates in this run, while broad conservative continuous intervals need not detect each positive coordinate.
2. The original diverse estimated-calibration branch has no guard against finite-sample rank deficiency. All observed diverse matrices were full rank, so recorded results do not require correction. A deterministic singular-input check and explicit refusal guard should be a separate repair, preserving original code/output. Its test supports instrument behavior, not new scientific performance.
3. Known/estimated/absent modes are offline analyses of shared data. The absent mode's return of all four candidates is an intentionally conservative policy, not a proof that every possible information set without witnesses leaves all candidates indistinguishable.
4. Candidate truth retention and conservative coverage are1.0 in these replicates. This is not proof of zero real-world attribution error or of optimal intervals. No rival invalid-witness model is included in Cycle1.
5. The declared fixed library has unmatched passive laws; the experiment does not establish interventions are necessary for identifying that library. Unknown kernels/families require a different assessment.

## Harness interpretation

Prospective protocol, raw measurements, declared limits and source-bound replay are observable adherence to saved guidance. Without a no-guidance comparison or longer repeated sessions, they do not establish that the FRR harness caused better reasoning, that the habits persist, or that the sampled mechanism occurs in agents. Cycle2 selected using Cycle1 is adaptive development, not an independent confirmatory test.
