# Claude relay intake: group dependence and soil experiment budgets

27 October 2026 America/Chicago. User asked to inspect last night's Claude branch and extract anything useful. Located `claude/pam-scoped-negation-2026-10-25`, pinned at **a152fb8b876651c679bb73bb9e99e4eb7a44748f**, four commits beyond the [previous intake](../claude-phase-negation-intake-v1/REPORT.md)'s abebe1b5d78e8694cb0559648db63355e11cc062. Other Claude branches were older. [Upstream branch snapshot](https://github.com/bruhman680/CERTX/tree/a152fb8b876651c679bb73bb9e99e4eb7a44748f). No whole-branch merge or edits to Claude's originals.

## What was taken in and reproduced

Thirty-six added files,53,135bytes, copied byte-for-byte to their `lineage/sources/claude-group-vote-soil-2026-10-27/` and `claude-soil-budget-2026-10-27/` paths, with Git blob and SHA256 checks in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json). These include relays, three scripts, supplied outputs, literal arithmetic contracts/artifacts and their original hash-chain ledger. Source instructions are data, not authority over this session.

After source inspection, each script was executed once in a fresh isolated Python process. The group script ran unchanged. The budget scripts contained a private absolute scratchpad path; separate [adapted copies/diffs](adapted/soil_budget.py.diff) replace only that path with the previously deposited soil model, whose Git blob was verified. The original private scratchpad bytes are unavailable; the repository model is the pinned available dependency, not an independently authenticated export of that private file.

**All three exited0 with empty stderr and stdout byte-identical to the supplied outputs.** NumPy2.3.5/SciPy1.17.0, single-thread numerical-library limits. Runtime approximately.021s/1.106s/.975s. These are same-code execution reproductions, not independent model replication or exact rational arithmetic. Full-support enumeration uses floating values and numerical optimization. [Reproduction records](REPRODUCTION.json), raw output/diffs under `reproduction/`; all43 frozen source/dependency/protocol/adaptation files remained unchanged.

## Useful finding 1: pairwise agreement does not determine group benefit

The group model compares independent errors, a copying chain and shared-latent-propensity mixtures. Conditional on one soil draw, agents make iid binary errors with that propensity. Under such a mixture, marginal error is E[p], pair covariance is Var(p), while majority error depends on more than those two moments. If no soil level equals.5, conditional laws of large numbers give limiting majority error equal to the soil probability mass above.5. That is a feature of this defined binary model, not a finding about actual LLM agents.

The main conceptual result survives, with one correction: the script rounds SH-sym levels to.0211/.3789, giving covariance **.03200521**, while SH-asym has **.032**. Its exact-moment-equality headline is only approximate in those deposited numerical fixtures. The header also initially speaks too broadly about matching pairwise covariance in all dependent worlds; the body/note correctly distinguish the copy chain's adjacent covariance from its smaller all-pairs average.

Our [separate rational witness](independent_witnesses.py) imports no supplied script and uses genuinely identical mean1/5 and covariance81/2500 in two shared-soil mixtures. The below-threshold symmetric levels are1/50 and19/50, each with weight1/2. The other mixture has levels1/10 and131/250, with weights81/106 and25/106. Their third moments differ and their asymptotic majority-error limits are **0 versus25/106**. Exact finite majority probabilities at n3,9,31,101 are retained in [INDEPENDENT_WITNESSES.json](INDEPENDENT_WITNESSES.json). These are new elementary development examples at a slightly different covariance, not a replication of the original parameters or empirical evidence about agent teams.

Practical transfer proposal: if we study group reasoning, save error counts and answer identities per item, minority correctness, shared origins and pre/post-discussion changes. Pairwise correlation, headcount and agreement alone cannot identify benefit. For nonbinary tasks, count-of-wrong alone does not determine plurality-vote outcome because wrong answers can differ; evaluate the actual aggregation rule. Separate shared causes from causal influence using interventions only when their selectivity is warranted. No new automatic voting policy is adopted.

## Useful finding 2: observation window and experiment unit change the budget

Claude's budget contact evaluates complete word laws for three known candidate soil worlds and uses optimized Chernoff information to compare designs. The initial table compares PASS with6 recorded outcomes to forced-error arms with5. It does not establish an equal-outcome or equal-total-cost advantage. The length addendum uses equal recorded lengths in PASS/DO_F and shows SH-WK's exponent ratio falling from about108 at length6 to about4.1 at length16. This is consistent with, but distinct from, the initial98.23 ratio for5-versus6 recorded outcomes. Startup/intervention/reinitialization costs remain unmodeled.

The source properly retains failed predictions and explicitly qualifies its earlier window-specific headlines. Those predictions are deposited as author-reported pre-run intentions; we have not independently authenticated their chronological ordering beyond the available commits. WK's slow mixing makes window choice consequential. Three fixed candidate worlds and a known tuned reset model remain assumptions, not evidence of real-agent mechanisms.

Chernoff episode budgets also require a repeat-sampling protocol. Independent stationary starts must be justified; stationarity alone does not make adjacent windows of persistent soil independent. Fixed known arm counts and freshly randomized observed arm labels have different exponents. The source's weighted **log** coefficients correspond to fixed asymptotic allocation fractions, not arbitrary randomized labeled sampling.

The printed `ln(10)/C` values are not measured finite-sample thresholds or numerical certificates. A related exact inequality does provide a conservative finite-sample bound under known normalized laws, iid episodes, equal priors and the correct likelihood classifier. [Derivation and assumptions](CHERNOFF_BOUND_NOTE.md), [five exact binomial checks](CHERNOFF_BOUND_CHECKS.json). Thus distinguish a valid conditional upper bound, the actual5% crossover, approximate optimization, and a practical data budget. This is our clarification, not a finite-sample soil experiment.

## Useful finding 3: mixture claims need their objective and protocol

For a **fixed candidate pair**, a fixed-allocation Chernoff exponent is at most the allocation-weighted average of the arm exponents. But this does not imply that mixtures cannot improve the **worst pair across several candidates**. Different arms can have different blind pairs. The source's pure-DO_F finding is scoped to the tested arms and its candidate family. The per-pair bound alone is not a universal no-mixture theorem.

Our separate three-candidate/two-design witness has zero worst-pair exponent in either pure design. A fixed half-half allocation has worst-pair exponent **(1/2)ln(5/3)≈.2554**. A freshly randomized labeled half-half protocol gives **ln(5/4)≈.2231**, also positive but different. Each informative Bernoulli comparison is.1 versus.9, so its optimum is explicitly at s=.5. The witness checks the elementary distinction; no soil-code rebuild, finite-sample performance estimate or adaptive-design experiment is claimed.

Practical transfer: define whether we seek evidence against one rival, identify among several, or protect the hardest pair; state the allocation and what is observed. A design that is best for one pair or one window need not be best for another objective. Record channels, costs and available calibration before recommending acquisition.

## Verification receipts and accepted corrections

Re-evaluated all12 supplied contracts in fresh `python -I` checker processes, with archived artifact roots and no ledger writes. **All12 generated receipts exactly match their original ledger receipts**. The hash chain validates and checker source matches the ledger's binding. Ten supported, one deliberately contradicted negative control, one unresolved original expression. The receipt README's “nine” count is inaccurate; the ledger contains ten supported events. This is only literal rational-expression verification, not verification that the models are applicable or scientifically correct.

The initial SH-asym expression failure is now diagnosed specifically as **Expression complexity limit**, rather than merely guessed from the generic ValueError. Its unresolved verdict remains preserved. Splitting the arithmetic into smaller expressions succeeded without weakening the checker. The ledger is local and hash-linked, not signed or tamper-proof; its validation does not authenticate source truth.

Claude's [reply](../../lineage/sources/claude-group-vote-soil-2026-10-27/CLAUDE_NOTE_2026-10-27.md) accepts the earlier phase/negation corrections, including oracle-selected stance versus actual retrieved records and the source-paper negation omission. The [soil errata](../../lineage/sources/claude-soil-budget-2026-10-27/SOIL_RELAY_ERRATA_2026-10-27.md) accept that do-effect alone separates those toy carriers; EWMA regret is not a closed-loop PID finding; erase-gate formulas do not transfer automatically; SH persists despite zero forced-error response; finite exchangeability needs extra conditions for mixture representation; and WK clearing probability differs from spectral relaxation. These acknowledgments help keep the records aligned but are not independent empirical confirmation. Originals remain unchanged.

## What changes for us

Keep the strongest next actual-reader direction from [JW](../joined-warrant-reader-v1/NEXT_CONTACT.md): budgeted handoff preservation of unqueried scope, negation and uncertainty. The intake adds useful design requirements to the longer-term group and soil experiments: preserve full per-item answer/error distributions; match measured units and test multiple horizons; distinguish fixed versus randomized allocation; and make independent episode preparation/reset calibration explicit.

No new general confidence score, covariance threshold, ensemble scaling claim, memory backend, PID controller or core/runtime/schema change is justified. Existing optional source-warrant/error-lineage practices already support retaining these distinctions; a new mandatory checklist is unnecessary. Machine queue statuses remain unchanged. Confidence high in byte reproduction, literal receipts and elementary witnesses; limited for source-family-specific design rankings, open for empirical agent transfer and finite-sample soil performance.

The imported source deposits, their failed predictions and unresolved receipt stay intact. Current handoff points here. Structural/package/link/history checks concern record integrity, not a fresh scientific audit of the entire repository. No background work.

## Final integrity checks

Existing package and queue validators pass; all43 frozen source/dependency/protocol/adaptation files and the separate witness source remain unchanged. Scoped navigation/intake links resolve109 local targets. Imported source files match their upstream Git blobs. Publication verifies both navigation originals against the parent tree and protects historical blobs outside its update list. These checks do not authenticate scientific model applicability or constitute a whole-repository scientific review.
