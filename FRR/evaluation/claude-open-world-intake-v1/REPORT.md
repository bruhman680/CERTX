# Claude open-world intake: useful failures, repaired feature and guard claims

2 November 2026. Source review and CPU toy validation; no model inference or training.

## Scope and receipts

Reviewed `claude/pam-scoped-negation-2026-10-25` at **318025c8bfc70a663e2e5a50abfa39fa583ce25d**, against the previous reviewed **b82724c2427151d38f5d0c45cd7cc87e9359565a**. Three new commits, twelve added paths, eleven unique blobs. All twelve source files were fetched and their Git blob hashes verified. See [manifest](SOURCE_MANIFEST.json). The exact source copies are preserved under `sources/`; this intake does not merge or edit Claude's branch.

Read all three relays, four executable scripts and four saved output files (the twelfth path is a duplicate generator). Executed all four scripts using the existing CPU Python/NumPy environment. **All four stdout outputs match Claude's saved outputs byte for byte**, all exit codes zero, all stderr empty. See [replay receipts](REPLAY_CHECKS.json) and `replays/`.

This is execution reproduction of the supplied implementation, not independent experimental replication or evidence that a language model acquired these behaviors. Worlds, features, recognizers, interventions and scoring were written by the same source author. Header predictions are source-reported prior predictions; the available commit publishes code and results together and does not establish an independently timestamped preregistration. Frozen calibration is useful within-run separation, not independent validation.

## Useful findings that survived inspection

1. **A closed vocabulary can become more confidently wrong as sample size grows.** In Claude's outside-world construction, the closed procedure makes specific known-world claims on all sampled outside-world runs at M>=400. This is a result about that procedure and scoring key, not a theorem about every closed classifier. A label must state the alternatives actually tested.
2. **Abstention and novelty detection solve different problems.** The cautious old procedure sometimes withholds between familiar alternatives. The open-set version can flag observations outside its calibrated family but otherwise always picks its nearest known class, increasing some in-family mistakes. Combining the two remains untested.
3. **Adding vocabulary has a cost.** At M=100, the seven-class recognizer labels genuinely independent runs IND only .56, ANTI .20 and DIFF .16. At M=400 its own-world recognition improves to .90-.99. Source classes are authored categories, not categories discovered by a learner. More labels do not automatically improve discrimination.
4. **Some causal stories are observational aliases.** COMMON and UPSTREAM here both generate the same shared iid Bernoulli sequence; COPY also has the same passive law. The supplied probe is a noisy world-conditioned oracle that distinguishes COPY from non-COPY. It cannot identify a hidden third source, and is not a measured intervention on an implemented causal system.
5. **A hard outcome needs a continuous companion.** In the metric contact, distance grows smoothly while UNKNOWN rises over a sample-size range. Keep continuous distance as well as labels; a threshold crossing alone is not evidence of a sudden new mechanism.
6. **Wrong-answer agreement does not locate its cause.** For three distractors with shared item attractiveness d~Dirichlet(alpha,alpha,alpha), conditionally independent wrong-answer draws agree with probability sum(d_i^2). Its expectation is (alpha+1)/(3alpha+1), giving .60 at alpha=.5 without copying. Conditional independence given an item is compatible with dependence after pooling items. Item structure remains a shared cause; this does not show that shared causes are absent. If item-specific both-wrong probability w varies, empirical pooled agreement instead weights items: E[w*sum(d_i^2)]/E[w]. The toy samples already-both-wrong draws.

## New correction: SWAP is not invisible to the existing seven features

Claude's phase-3 run labels the held-out SWAP world PARTIAL in .94 of M=400 runs. The relay interprets this as pooled features being unable to see the first-half/second-half change. That interpretation is too strong: its feature list already contains **corr(item index, A_flag OR B_flag)**.

Independent exact algebra, with marginal observed error q=.23 and flag-flip probability .05:

| World / segment | Observed joint error | Probability of either observed error |
|---|---:|---:|
| Independent | .0529 | .4071 |
| Shared / copying | .1825 | .2775 |
| PARTIAL, each item | .1177 | .3423 |

SWAP copies in its first half and becomes independent in its second. Its OR rate therefore rises **.2775 -> .4071**, although each answerer's marginal rate stays .23. PARTIAL's OR rate stays .3423. SWAP's pooled same-item joint matches PARTIAL, but the full feature vector need not.

For uniformly sampled item index X=0,...,M-1 and OR indicator Y, even M gives:

`Corr(X,Y) = ((.4071-.2775)*M/8) / sqrt(((M^2-1)/12)*.3423*(1-.3423))`.

At M=400 this population correlation is approximately **.118274**, versus zero for PARTIAL. This is the random-item population correlation, not an identity for each finite sample's Pearson correlation.

After deriving that signal, ran a fresh-seed extension of Claude's unchanged seven-feature classifier, with 400 fit and 400 calibration samples per ordinary class, and 600 evaluation runs per world/size. SHARED uses the script's pooled allocation (3*floor(400/3)=399 samples). This is a bounded post-source check using the source classifier, not an independent classifier rebuild.

| M | SWAP mean OR trend | SWAP UNKNOWN | SWAP PARTIAL | PARTIAL UNKNOWN |
|---:|---:|---:|---:|---:|
| 400 | .1154 | .0300 | .9433 | .0033 |
| 1,600 | .1181 | .8233 | .1767 | .0150 |
| 6,400 | .1183 | 1.0000 | .0000 | .0067 |

See [exact algebra and fresh-seed results](INDEPENDENT_CHECKS.json) and [reproducer](independent_checks.py).

The corrected reading is: **SWAP is hard for this calibrated recognizer at M=400; a measured signal already exists and gains power at larger M.** The source's post hoc half-split feature may improve sensitivity, but it is not necessary for eventual detection in this construction. UNKNOWN still does not identify the correct causal story.

Do not extend this correction to LAG2 without a separate check. Its lag-2 dependence is not directly measured by the original lag-1 features. Nor does one recognizer's poor performance prove that no alternative recognizer could do better at the same M.

## Additional guard defect: known DIFF also becomes wrong with more data

Independent review identified a stronger in-family control that the outside-world headline omits. Exact noisy DIFF correlation is `(0.0853-.23^2)/(.23*.77) = 324/1771 = .182947...`. The closed guard calls IND whenever `phi_hat + 2/sqrt(M) < .25`. Consequently it labels this known DIFF world IND with probability approaching one as M grows. The shared-route override vanishes because both conditional agreements tend to .37087, below .6. Thus increasing-data error is partly a **misplaced decision boundary inside the known family**, not exclusively a consequence of missing labels. The frozen algebra check verifies these inequalities. Preserve the outside-world finding, but do not attribute every failure to vocabulary closure.

## Other qualifications worth retaining

- The accepted DIFF correction is implemented consistently: noisy joint .0853, conditional 853/2300=.3708695652. Shared conditional is 73/92=.7934782609. A .6 guard lies between them.
- `open_world_guard.py`'s O1 printed check reports any specific outside-world claim, although its text says it is checking IND claims. Keep the phase-1 label table separate from that aggregate. Not every specific misclassification is IND.
- UPSTREAM scoring needs a scope decision. The code counts any familiar specific claim on an outside world as overreach, including COMMON on UPSTREAM; prose also describes SHARED as an acceptable passive signature. A claim about a shared signature and a claim about a distinct causal route must have different scoring keys. COMMON vs UPSTREAM in this implementation is also a latent-node renaming, without a supplied different intervention target.
- The follow-up frames dilution versus sample power too exclusively. Both feature choice and decision rule can matter; failure of one max-distance alternative does not establish an information-theoretic impossibility.
- The metric script's continuous statistic is minimum raw distance; UNKNOWN thresholds minimum class-normalized distance. They are related but not the same scalar thresholded. Future logging should include the exact normalized decision distance and class threshold, avoiding accidental metric mismatches.
- Separate seeds for mean/max modes and seven/nine-feature variants limit causal attribution of their differences. A next prospective comparison should use the same generated evaluation items across arms and separate calibration seeds.
- The new code supplies outside-family tests, but no genuine sham-intervention experiment. Oracle probes and planted symmetric-noise gold labels remain strong assumptions.
- Calibration's rounded, truncated hash is a within-run receipt, not a complete exact parameter artifact or evidence of external chronology. Full calibration arrays and per-run scores would improve auditability.
- Post hoc lag-2/half-split additions are explicitly marked post hoc. Their successful repair is useful engineering evidence, not held-out confirmation of feature discovery.

## Literature contacts: what we actually checked

Claude supplied seven scout notes. We do not promote all seven to independently verified reading.

We checked the primary HTML of [Correlated Errors in Large Language Models, v1](https://arxiv.org/html/2506.07962v1), specifically sections 3.1-3.2 and the discussion of metrics. Its 1/3 HELM comparator assumes uniformly chosen wrong answers; the variable-choice HF comparator averages 1/(k-1). The authors themselves discuss differing incorrect-answer plausibility and question difficulty as limitations. Claude's distractor construction illustrates that limitation; it does not invalidate their empirical agreement measurements or explain their data. Their regression associations do not alone identify copying or a unique causal source. Their study also includes resume evaluations, so the scout's broad phrase 'multiple-choice only' is too narrow for the entire paper.

Abstract-level primary checks of [Performative Prediction](https://arxiv.org/abs/2002.06673v4) and [Are Emergent Abilities ... a Mirage?](https://arxiv.org/abs/2304.15004v2) support the respective conceptual contacts: action-induced distribution change, and metric-dependent appearance of emergence. We did not verify the scout's numerical theorem constants or its detailed meta-analysis percentage. Those should not be imported from the relay as newly checked facts.

Negative-only training, plausible-negative selection, partially performative prediction and MAST remain scoped literature leads from Claude, not replications or new FRR efficacy evidence.

## Useful refinements and next contacts

**Adopt in our review practice now:** report claim scope and tested alternatives; distinguish observational signature from causal route; report UNKNOWN, within-family withholding and wrong-specific claims separately; retain the exact continuous decision statistic; keep failures and post hoc repairs visible. These are reporting disciplines supported by this intake, not a new default model/controller.

**Strongest next toy contact:** paired, prospectively frozen evaluation of cautious withholding plus open-set detection, with an explicit 'consistent with these candidates, alternatives not excluded' claim. Include known DIFF across increasing M as a mandatory control, SWAP with its existing OR-trend signal, LAG2, and an untouched new world. Compare against a calibrated compatibility-set control before attributing failure to vocabulary closure. This follow-up has now run separately in [compatibility-guard-control-v1](../compatibility-guard-control-v1/REPORT.md); the broader combined guard/held-out-world/actual-sham study remains unexecuted. Score at both descriptive and causal levels, including unresolved equivalence classes. Use actual implemented intervention and sham mechanics before claiming source localization. The broader proposed contact remains unexecuted.

**Model work remains its separate queue:** simpler evidence-only teacher vs original/no-list review, fresh names/layouts, wrong-source/absence controls, accuracy and likelihood before distillation. No new teacher, model default, trained weights, paid API call or background job in this intake.

Garden reading: Claude tested whether our labels recognize unfamiliar plants. Some labels failed, and more samples sometimes helped while sometimes only strengthened a mistaken familiar name. We found one plant already casting a measurable shadow on an existing sensor. The useful repair is to ask what each sensor sees, how much evidence it needs, and how far its label is allowed to reach.
