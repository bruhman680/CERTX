# Reset-reader study RR1: prospective bounded trial

Question: when does retaining more visible history help prediction, and when can a wrong assumption about how a reset was prepared reverse that comparison?

This protocol and the implementation are to be saved before their first execution. The source-kernel mismatch phenomenon is already known from the relay; that part is a controlled extension, not a novel discovery or untouched confirmation. Two additional prespecified kernels test transfer within the same small model family. They are not independent real-world evidence or an independently authored held-out benchmark. No parameters or acceptance thresholds will be tuned after inspecting their outcomes.

## Construction and comparisons

`MODELS.json` fixes three pairs of binary transition matrices and five h values per pair. State is (visible y, environment e). First draw next y from K[e][y], then replace e with the previous y with probability h. All observations start with y=0. Enumerate every visible history at times t=0 through 8; compute probability-weighted expected KL risk against the oracle that sees current e. Use natural logarithms. This is deterministic finite enumeration in floating point, not sampled data.

Prepare the initial e distribution five ways: stationary conditional given naturally observed y=0; stationary marginal with y independently forced to 0; fixed e=0; fixed e=1; independent fresh uniform e. At h=0 select the stationary mixture with equal environment weights explicitly, since the joint chain has no unique stationary distribution. The other tested h values have a unique stationary distribution in these constructions.

At each time compare readers retaining the last 1,2,4 symbols or all available symbols. A matched reader uses the correct preparation law. An assumed-natural reader uses the natural-conditional preparation for every actual preparation. Both short and full readers condition on the same elapsed time under their respective assumed laws. Thus the assumed-natural history comparison changes retained history while holding the assumed preparation fixed. Include a separate stationary one-symbol reader to connect to the older source comparison; do not mix that different age/preparation assumption into a pure history-length claim.

Each predictor knows K, h and elapsed time. No reader sees the realized e. Giving a matched reader the preparation type is additional metadata; its benefit is not evidence of an equal-information algorithmic improvement. Finite suffix models use exact conditional distributions, not learned finite-sample estimates.

## Predictions and decision rules, before this run

1. Under matched preparation, full-history expected risk is no greater than any suffix risk, and matched suffix risks are ordered as their available information increases. This is a log-score conditional-expectation consequence, not an FRR-specific empirical prediction.
2. Expected risk of an assumed-natural full reader minus matched-full risk equals the history-averaged KL between their next-symbol predictions. It is nonnegative. Check the identity for every reader as well, not just the full one.
3. Under mismatched preparation, an assumed-natural full reader may lose to its assumed-natural one-symbol counterpart in at least one source-kernel cell. This is an existential extension informed by previous results. Report whether it also occurs in each additional kernel. A negative transfer result remains a result; do not tune kernels to force it.
4. At h=1 and t>=1, the environment equals the previous visible symbol. Full-history and two-symbol matched/assumed-natural readers should have zero oracle-relative risk and zero preparation penalty, up to numerical tolerance.

Algebraic/integrity checks use tolerance 1e-11. All cells are retained, including ties and unfavorable outcomes. Report the first and largest assumed-natural full-minus-one-symbol reversal for each kernel, along with total grid counts and matched-reader comparisons. Counts describe this prespecified correlated grid; do not attach statistical confidence or population frequencies.

Acceptance: proceed to interpretation only if probability mass, joint marginal cross-checks, risk decomposition, matched-information ordering and h=1 checks pass. If they fail, preserve the failing output and version any repaired implementation/evaluator explicitly. No result in this toy will justify modifying core FRR or claiming general reasoning improvement. Useful outcome means a clearer scoped relationship or a counterexample, not necessarily a favorable score.

## Execution and resource scope

One local CPU execution, at most 60 seconds; stop and retain available error output if it exceeds that budget. No GPU training, external model calls, or agent-swarm experiment. Measure wall-clock duration with perf_counter and save Python/NumPy/platform details. Tokens, money, energy and causal physical entropy are not measured. Exact enumeration has no RNG seed; model tables are fixed.

Run `python FRR/experiments/reset_reader_study.py`. Save rows and checks in this directory as `RESULTS.json`, a compact `SUMMARY.json`, and captured stdout/stderr. A launch receipt will pin the protocol, model tables and executable hashes. Retain these artifacts regardless of outcome. New research questions or repairs require a later version rather than silently changing this run.

Next contact depends on results: investigate preparation metadata versus history, reader misspecification, and the lifespan of preparation dependence. Transfer to actual retrieval/continuation agents remains a separate experiment.
