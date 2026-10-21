# ES-C1: what determines error and success?

A targeted source weave, exact counterexamples and candidate diagnostic architecture following [PID-C1](../pid-contact-v1/REPORT.md). The user asks for a proverbial controller across domains. The defensible cross-domain object is a way to specify, observe, diagnose and revise a comparison, not one numeric error signal or controller guaranteed to recognize every failure. No general FRR efficacy result, domain-complete taxonomy or new universal law is claimed.

## Main finding

The word error mixes distinct relations: a claim to reality, a conclusion to premises, an observation to the state measured, an outcome to an objective, and an intervention to its intended effects. Success likewise can mean a true answer, valid inference, good probabilistic forecast, achieved objective, respected constraint or a useful investigation. These verdicts can disagree.

For a context c, an explicit task can specify an acceptable set K_c of trajectories tau, including constraints and horizon. Then task success can be represented by S_c(tau)=1 if tau lies in K_c, and 0 otherwise. A graded loss L_c(tau) is another option. This is a representation after the criterion is supplied; it does not derive the right criterion, establish its observability, or discover a successful policy. Some human goals remain contested, incomplete or incomparable. A chosen scalar weighting adds priorities rather than revealing a natural universal ranking. Physical feasibility and factual truth are not made arbitrary by specifying a task.

Also distinguish the underlying verdict from our warranted estimate of it. The controller sees observations, not necessarily the full trajectory, correct measurement model or eventual consequences. A failure can exist without being detectable from the currently available evidence. Conversely, an unexpected event need not show that a probabilistic prediction was badly made.

## Established anchors, with their assumptions

**Cybernetics.** Ashby treats regulation through disturbances, available responses, essential variables and acceptable states. His requisite-variety table argument limits regulation under specified distinguishability assumptions; it is not a claim that more agents or more arbitrary noise guarantee better regulation. Chapter 12 explicitly takes the goal as supplied from outside the regulator. Source contact: selected sections 10/5–10/7, 11/5–11/7, 11/20–11/21 and 12/1, not a full-book audit. [An Introduction to Cybernetics](https://ashby.info/Ashby-Introduction-to-Cybernetics.pdf).

**Forecasting.** Gneiting and Raftery's proper-scoring framework rewards reporting the predictive distribution through expected score; strict propriety makes that expected optimum unique within the specified class. An individual realized score is not a direct test of whether the forecaster knew the true probability. Source contact: abstract/introduction and categorical/binary scoring sections. [Strictly Proper Scoring Rules, Prediction, and Estimation](https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jasa.pdf).

**Proxy optimization.** Manheim and Garrabrant distinguish regressional, extremal, causal and adversarial mechanisms for a proxy losing its relation to the intended goal under optimization. This is a taxonomy with differing mechanisms, not a theorem that every metric inevitably fails. Source contact: the four-part paper's HTML text, particularly introductory definitions and causal intervention cases. [Categorizing Variants of Goodhart's Law](https://arxiv.org/html/1803.04585v3).

**Deduction.** In the propositional proof system discussed in Cornell's notes, derivability from premises implies semantic consequence. This conditional guarantee does not certify that a real-world premise is true. Source contact: soundness argument; later philosophical discussion was not used. [Soundness and completeness](https://www.cs.cornell.edu/courses/cs2800/2017fa/lectures/lec38-sound.html).

**Allocation of reasoning.** Russell's metareasoning overview separates object-level problems from choosing computations, gathering information and stopping. Meta-level work itself has a cost and risks regress. Source contact: seven-page PDF. [Metareasoning](https://people.eecs.berkeley.edu/~russell/papers/mitecs-metareasoning.pdf). No claim that an LLM has the full internal-state observability discussed for some architectures.

Access limits: Stanford's corresponding logic page timed out; Mitchell's textbook PDF exceeded the web tool's size limit. Search snippets from those sources are not treated as full-text evidence. This is a targeted contact, not exhaustive coverage of statistics, philosophy, control, software assurance or biology.

## Exact witnesses: where a universal scalar controller breaks

[Executable source](../../experiments/error_success_witnesses.py) and [full output](WITNESSES.json). Six authored mathematical illustrations, checked with exact arithmetic/truth tables; not six empirical replications, held-out trials or actual-agent tests. Conditions were selected to expose distinctions, not sampled to estimate prevalence. No new model calls.

1. **Same mismatch, opposite correction.** Both worlds start at y=0 with target 1. World A has next y=u; B has next y=−u. Available one-shot actions are ±1, and there is no observation/history revealing which world applies. The same error +1 requires opposite actions. A randomized policy choosing +1 with probability p succeeds with p in A and 1−p in B. Its worst-case success is at most 1/2. This follows algebraically for every p; the 101-point rational grid only checks the implementation. Additional informative observations or probes can change the problem. This counterexample rules out guaranteed success from such insufficient feedback, not all adaptive learning.
2. **Good forecast, unfavorable realization.** With true event probability q=4/5, binary Brier loss has expectation q(1−p)^2+(1−q)p^2. Subtracting its value at q gives (p−q)^2, so forecasting p=q is optimal in expectation. Yet the event is absent with probability 1/5, yielding realized loss 16/25. A bad outcome does not by itself establish a reasoning error. The true q is supplied by construction; real calibration needs appropriate repeated cases and assumptions.
3. **Valid rule, false premise.** Truth-table enumeration verifies modus ponens: P and P→Q entail Q. In a world with P=true, Q=false, the implication premise is false. Applying the valid rule to that unsupported premise can produce a false conclusion. This is not a counterexample to modus ponens. More deduction does not repair an unexamined empirical premise.
4. **Facts held fixed, priorities differ.** Option A has quality 9/cost 9; B quality 6/cost 1. Quality minus 0.1 times cost selects A; quality minus cost selects B. The arithmetic is objective given either rule. The rule needs a priority choice; choosing a new rule after failure must not erase the old verdict.
5. **Measured success, state failure.** Target 1, true state 3/5 and sensor bias 2/5 give measured error zero and true error 2/5. This is the algebraic limit illustrated numerically by PID-C1, not an independent physical experiment.
6. **Memory preserved, crucial distinction erased.** Two histories record opposite actuator gains but identical latest y=0. A summary retaining only y merges them. The next control action cannot be selected correctly for both using that summary alone. Retaining the gain would solve this example. This is an information-loss witness for a chosen compression, not evidence that all compression fails.

All assertions passed. More controllers/agents seeing the same undifferentiated record do not, by their number alone, reveal the missing world identity. Computation can expose consequences already implicit in evidence; it cannot guarantee the missing distinguishing fact in this construction.

## A practical map across domains

This is a diagnostic mapping, not a proof of identical mechanics across substrates.

| Domain/task | What establishes an error or success? | A misleading substitute |
|---|---|---|
| Deduction | Valid steps relative to explicit premises/semantics; empirical premises need their own warrant. | A coherent conclusion treated as verified reality. |
| Empirical explanation | Fit to relevant observations, rival discrimination and demonstrated scope; causal claims need appropriate identification assumptions. | Agreement with the observations used to invent the explanation. |
| Probabilistic prediction | Appropriate scoring, calibration checks and evaluation on the intended population/horizon. | One lucky hit or one unlucky miss treated as proof. |
| Control/engineering | Desired state/trajectory and constraints under actual dynamics and credible measurements. | Zero display error. |
| Software | Behavior against the intended specification, including relevant failure conditions. | Passing tests that omit the decisive requirement. |
| Decisions with several objectives | Outcomes and constraints assessed under explicit priorities, uncertainty and stakeholder scope. | One improved metric hiding a worse consequential outcome. |
| Shared memory/reasoning | Grounded claims, useful preserved distinctions, warranted revisions and appropriate continuation. | Consensus, fluent summaries, or persistence alone. |

## The candidate architecture: diagnose before increasing correction

Retain the optional [evidence-gated feedback procedure](../../modules/evidence-gated-feedback.md). ES-C1 adds a diagnostic guide rather than a new required FRR core/version:

1. **Specify:** What claim or outcome, for whom, under which constraints, tolerance and horizon? Separate factual correctness from preference or task completion.
2. **Observe:** What evidence is accessible, and what could the measurement/summary hide? Keep true state, measured state and inferred state distinct.
3. **Compare separately:** Check inferential validity, evidential support, prediction quality, objective attainment, constraints and cost without forcing one master score.
4. **Diagnose alternatives:** Is the failure in the premise, measurement, model, chosen objective, action, available resources, scope, or evaluation? An anomaly alone does not locate the cause.
5. **Discriminate and intervene:** Pick an affordable observation, calculation, rival test or corrective action whose possible results would matter. Where the real process has a usable numeric signal, a controller can regulate effort/action. Missing identification may require a probe or an unresolved verdict rather than stronger correction.
6. **Reassess and preserve:** Did the warranted claim or actual outcome improve under the original criterion? Record any criterion/version change separately. Preserve failed predictions, rejected changes, delayed effects and reopening conditions. Bound auditing itself; no infinite meta-review.

This yields two linked functions: improve the result under a stated specification, and examine whether the specification/measurement still serves the intended question. The second function also needs evidence and limits; it is not an infallible supervisor.

## What this changes for our research

The most useful refinement is to locate the alleged error before strengthening a corrective loop. Prior wrong-reference studies already caution against an auditor correcting toward inherited bad evidence. REV-C1 preserved corrections but ordinary/FRR guidance tied. Neither establishes a general detector. The current broad FRR orientation may help notice missing distinctions, but this remains a behavioral hypothesis.

The next test should deliberately separate an incorrect inference, false premise, biased measurement, correct but unlucky forecast, invalid proxy, lost historical distinction, and a changed legitimate objective. Include settled correct cases so constant doubt can be penalized. Use authoritative task-grounded labels; permit unresolved/underdetermined verdicts; compare ordinary review, provenance-only and the optional procedure with matched budgets. Score diagnosis and useful correction separately from eloquence, agreement and result-only luck. These six witnesses are development material and must not be presented as held-out confirmation of that later test.
