# Pass 3: challenge the evaluator, including its headline

Read 14 November 2026. This is a selected-section source audit, not a benchmark replication. No external code ran, no dependency, model or dataset was installed, and no main-world state changed. The continuing garden remains at 1580. Pass 1 verification, Pass 2 history, and the completed observability report supplied the questions; primary sources supplied the checks below.

## What the deeper contact changed

CAREFUL-Bench is a verified primary contact: Alexander Kovalenko and Artem Redchych, *CAREFUL-Bench: Effect-Aware, Judge-Free Evaluation of Multi-Turn LLM Function Calling*, [arXiv 2611.02978v2](https://arxiv.org/abs/2611.02978v2), revised 3 November 2026. Its abstract's final-state-only characterization of BFCL is too broad. The paper's own §3 explicitly describes both public-state comparisons and an unordered sub-multiset check of reference function results against accumulated model results. The official BFCL V3 methodology likewise describes state and response checks after every turn. Thus the useful criticism is incomplete trajectory/effect coverage, rather than the absence of every non-state check.

The paper scopes its audit to `bfcl-eval 2026.3.23`; it is not an audit of every BFCL category/version. Its later discussion acknowledges the response check. This is a reconciliation of claim scope, not a reason to dismiss the whole paper.

## Three primary contacts

**1. CAREFUL-Bench, selected §§2–6 and §8.** Sections 4–5 propose controlled state-diff observations and call-by-call replay, alongside existing BFCL scores. They separate repeated writes, repeated reads, extra calls, failures, confirmation, and final task outcomes. Effects absent from the simulator remain invisible; sampled idempotence is evidence, not proof. §8 explicitly admits that a confirmation script can accept the right function with the wrong arguments. These limitations matter as much as the scoring idea. A repeated read without an intervening state change is not intrinsically irrational: checking uncertainty, transient failure or instrumentation may justify it. That last point is our general inference, not a finding reproduced here.

The proposed collateral-call rule counts excess destructive functions relative to the reference per turn. It does not establish that every alternative function sequence is unrequested or inferior. The paper's safety-success definition combines official success with no collateral destructive calls and no duplicate writes; its strict version adds confirmation. It does not simply reject every surplus read. Our free garden has no externally assigned optimum action sequence, so these task-specific labels cannot be transferred as behavioral gates.

There is an unresolved source discrepancy even within v2: the arXiv abstract landing page gives rank correlation .99 and leader loss 14.0 points, while HTML abstract gives .98 and 14.5. We do not select or reuse either numeric claim as settled. The paper says its release includes replay tests on 800 reference trajectories, but no author code URL was located in the inspected HTML links, abstract metadata or focused search. That release/test claim remains author-reported and unreplicated here.

**2. BFCL V3 official methodology plus actual scorer.** The [methodology](https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html) is dated 19 September 2024, updated 10 December 2024. Its minimum-path language can sound stronger than the implementation. At inspected GitHub commit `6ea57973c7a6097fd7c5915698c54c17c5b1b6c8` (23 March 2026), the complete [multi_turn_checker.py](https://github.com/ShishirPatil/gorilla/blob/6ea57973c7a6097fd7c5915698c54c17c5b1b6c8/berkeley-function-call-leaderboard/bfcl_eval/eval_checker/multi_turn_eval/multi_turn_checker.py) was read. The connector reports blob `34b36715cdfaa4464ba1be137af4d30e85da8efb`, last modified 9 June 2025.

The main checker executes predicted and reference calls, accumulates model results across turns, checks state, and then calls `response_checker`. That checker passes reference results as the first argument to `_is_subsequence_unordered`; the helper removes matching occurrences from a copy of accumulated model results, enforcing multiplicity but not order. The prose docstring reverses the intuitive containment wording; the actual argument flow establishes direction. `_compare_instances` skips underscore-prefixed attributes. The separate method-invocation-order check exists but its call is commented out. Therefore this code corroborates CAREFUL's detailed account: reads are not evaluated solely through unchanged final public state, while result containment does not impose a complete effect-sensitive trace contract. We did not audit every executor/decoder/service or execute synthetic counterexamples.

The inspected commit date matches the package date claimed by CAREFUL, but exact identity with the published wheel was not proved: `pyproject.toml` uses dynamic setuptools-scm versioning. We pin our inspected code rather than asserting package equivalence. The official blog's leaderboard composition also warns it is outdated; its current page should not be treated as a complete description of all current BFCL categories.

**3. τ-bench, focused §3 reread.** [arXiv 2406.12045v1](https://arxiv.org/html/2406.12045v1), Yao et al., 17 June 2024, multiplies a final database outcome check by required response-information checks. It explicitly warns that passing reward may still miss policy violations such as missing confirmation. This is a useful prior admission of the same general verification boundary. It does not validate CAREFUL's numbers or convert every interaction into a customer-service policy task. No additional τ-bench implementation audit was performed in this pass.

## Extraction for our detached file experiment

Our four exit-0 cells caught a JSON parsing exception after parsing a filename as text. Their source file was valid and unchanged, but never read by those cells. The evidence layers should remain independently reportable:

| Layer | Observation to retain | What it does not establish |
| --- | --- | --- |
| Process | exit code, exception handling, stdout/stderr | requested goal achieved |
| Acquisition | target path resolved, actual content read/returned, provenance | information used in an answer |
| Use | correct nonce in output and its available source | understanding or general retrieval competence |
| Requested effect | task-specific predicate on output/state | all intermediate effects acceptable |
| Trajectory | extra reads/writes, errors, changed state, reversibility where defined | a unique best path or free-world success score |

An open event alone need not prove bytes consumed. A correct value supplied in the prompt is not a model-chosen filesystem read. Identical input under hidden nonce substitutions gives an acquisition control; it does not prove an internal representational mechanism. Read-only goals require evidence beyond unchanged final state, and successful final state can conceal intermediate changes. These are interpretation refinements, not new requirements imposed on the main garden.

The strongest prospective design is still the same truthful retrieval task under inherited, fresh, and declared matched alternative histories. Preserve errors and alternative implementations. Score explicit requested outcomes in that detached diagnostic; retain traces externally for interpretation. Do not replace the garden's lawful actions with a preferred reference path, erase failures, or feed observer judgments back as hidden rewards.

## Confidence and remaining contacts

High confidence: the inspected BFCL scorer uses both public-state and unordered result checks; exit status cannot substitute for our requested-value predicate; final-state and complete-trajectory claims differ. Moderate confidence: effect replay is a useful observational pattern if we define instrument coverage and preserve alternative paths. Unresolved: CAREFUL release availability, its numeric discrepancies, wheel-to-commit identity, scorer correctness on all reference/model traces, and transfer to our 135M model. None was experimentally resolved by this reading pass.

Access methods and failures are recorded in SOURCES.json. A local HTML extraction first failed because `bs4` was absent; standard-library extraction then succeeded, without installation. This is an access-workflow failure, not a paper failure.
