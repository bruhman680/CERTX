# AS-C1: bounded arXiv scout and next-contact recommendation

The user requested a fluid exploratory scout of recent and earlier developments, using an FRR-oriented swarm. Three delegated lanes plus the coordinator selected ten primary papers: causal identification, prediction/adaptation, and agent memory evaluation. This is a targeted scout, not a systematic review, exhaustive recency sweep or novelty search. No paper's experiments, code or theorem proofs were reproduced.

## What the harness actually did

Each scout was asked to work forward from the observable/intervention to the claim; backward through the assumptions and source; and laterally through a rival explanation and a concrete transferable test. Roles were divided by question rather than instructed to endorse FRR. The coordinator shared promising search leads and a methods caveat across lanes, so these are coordinated readings, not independent confirmations. Same platform/model ancestry remains.

[SOURCES.json](SOURCES.json) records exact versions, dates, primary URLs, readers and read depth. The coordinator read CMP's primary methods/assumptions/limitations and verified primary arXiv metadata/abstracts for four recent scout sources; other method reading is explicitly delegated. Search snippets and secondary pages supplied leads, not accepted scientific evidence. Unselected search hits were not promoted into the source ledger. No runtime/schema change is made by this scout, and this does not test whether FRR improved the search.

## What we can borrow, with boundaries

### Causal identification

- [On the Identifiability of Causal Abstractions, 2503.10834v1](https://arxiv.org/html/2503.10834v1), March2025: available interventions may support identification of an aggregate rather than every underlying variable. Paired interventions, a faithful latent DAG, continuous variables and smooth invertible mixing are material assumptions. Our binary temporal feedback model does not inherit that theorem. Borrow the option to report an unresolved equivalence class.
- [Linear Causal Representation Learning from Unknown Multi-node Interventions, 2406.05937v1](https://arxiv.org/html/2406.05937v1), June2024: intervention diversity can matter even with unknown multi-target effects. Linear full-rank mixing, continuous latent distributions and intervention regularity/rank conditions restrict transfer. An imperfect soil reset is not automatically its soft-intervention model.
- [Beyond identifiability: Learning causal representations with few environments and finite samples, 2603.25796v1](https://arxiv.org/html/2603.25796v1), March2026: finite-sample recovery complements population identification under a structured linear latent model and separating interventions. Noise/conditioning assumptions and its knockout/two-scale design matter. We should compare different interventions against more repetitions, not borrow its numerical guarantees.

### Prediction and adaptation

- [Prediction from compression for models with infinite memory, with applications to hidden Markov and renewal processes, 2404.15454v1](https://arxiv.org/html/2404.15454v1), April2024: predict the next symbol conditional on observed history; parameter identification is a different target. Its stationary HMM assumptions do not automatically cover imposed-reset segments. This reinforces the information-matched comparator from ST-C1.
- [Bayesian Online Changepoint Detection, 0710.3742](https://arxiv.org/abs/0710.3742), October2007: uncertainty over run length supplies an alternative to one fixed forgetting constant. Conditionally iid segments and independent segment parameters limit transfer. A marked forced error should not automatically count as evidence of spontaneous regime change.
- [Efficient Methods for Non-stationary Online Learning, 2309.08911v3](https://arxiv.org/abs/2309.08911v3), September2025 revision of2023 work: local/interval and changing-comparator regret can reveal poor recovery hidden by a total average. Convexity and theorem-specific regularity underpin the guarantees. This is not evidence that a larger reasoning swarm is computationally efficient.

**An important correction to our framing:** hidden state can keep moving while the observable process remains stationary. The supplied soil wake begins in stationarity. Test actual exogenous parameter changes separately before calling a prediction problem nonstationary or assigning a changepoint model mechanistic significance.

### Real-agent memory bridges

- [MemoryArena, 2602.16313v2](https://arxiv.org/html/2602.16313v2), September2026 revision: evaluate memory through later actions in interdependent sessions. Its approximate oracle supplies prior outcomes/workflows without certifying a sufficient or optimally usable state. Borrow availability-versus-application measurement; do not assume delivering a correct note makes task completion inevitable.
- [STALE, 2605.06527v1](https://arxiv.org/html/2605.06527v1), May2026: recognize an update, resist a stale premise and act on the revised state as distinct checks. Controlled conflict pairs and semantic judging leave retrieval/reasoning/instruction effects entangled. A correct account of what changed is not a certificate of corrected behavior.
- [MemSecBench, 2607.27080v1](https://arxiv.org/html/2607.27080v1), July2026: separate persistence, recall, adoption, external consequence and repair. Selective repair also preserves required benign information. Controlled tasks, particular stacks and semantic judges limit generalization; clearing everything should not earn full repair credit.
- [Causal Memory Policy, 2610.02070v3](https://arxiv.org/html/2610.02070v3), October2026: randomized retrieval exposure addresses a support problem that store-only perturbations can miss. Read §§2–3 and AppendicesI/J. Its generator receives retrieved text/query under a specified mediation model; a candidate pool constructed with knowledge of required memories limits practical deployment. Retrieved-use utility is not automatically a future retention policy. Borrow controlled exposure with known assignment, while tracking context displacement and the query-specific estimand.

These sources supply methods and counterconditions, not independent confirmation of the entire soil metaphor or of FRR's general effectiveness. Apparent agreement can reflect related assumptions, shared datasets or related research lineages.

## Strongest next step

First perform the **different-parameterization, leaky-reset robustness contact**, varying intervention diversity separately from sampling precision. Treat a precise carrier name as one possible outcome, not a required success. Report candidates that remain observationally equivalent and propagate calibration uncertainty. The draft now explicitly includes a gate-restoration rival and sham, unknown/known calibration conditions, and a readout-access failure control.

Then use an **information-set-controlled predictor comparison**, distinguishing stationary hidden dynamics from genuine parameter shifts. Give learners identical visible history and intervention flags; score predictions before natural outcomes. Keep a privileged hidden-state ceiling separate, and measure false alarms/local recovery alongside aggregate loss.

The nearest practical bridge is a small actual-agent source/exposure/repair contact: independently checked task state, independently varied note correctness and exposure, observable actions and preservation of an unrelated benign fact after repair. It need not wait for a universal memory theory, but should not be mistaken for a carrier-identification experiment or another FRR-brand ranking trial.

[NEXT_CONTACTS_DRAFT.md](NEXT_CONTACTS_DRAFT.md) makes these proposals reviewable. They are **not registered/frozen protocols or executed experiments**. This scout changes no queue completion state. Existing LEGACY-01, PID-01, MEM-04 and FIELD-01 provide the related families; there is no need to inflate the queue with duplicates.

## Independent noticings to carry forward

- Extra observations can reduce uncertainty about an answer while leaving the mechanism ambiguous. More repeated samples do not repair an intervention design that never separates rivals.
- A record can be written, retrieved and even correctly described without changing the next action. Preserve those as separate observations rather than a single memory-success score.
- A correction can remove a bad premise while damaging useful context. Repair should be tested on both the corrected target and something that ought to survive.
- An anchor can fail through its read path as well as its content. Our next tests should challenge witness access, not simply announce that witnesses are independent.

These are operational questions suggested by the weave, not claims that all mistakes share one seed or that the papers establish a universal law.
