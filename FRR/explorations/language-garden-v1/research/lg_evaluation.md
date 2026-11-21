# Evaluation: observe first, test particular claims later

Planning proposal, 2026-11-21 UTC (user-facing project date: 20 November 2026, America/Chicago). Read LAB_BRIEF.json and exact compact.md before developing this note. No model inference or training occurred. The garden’s expressive life is the purpose; measurements describe it externally. An observation that challenges an observer’s hypothesis is valuable even when it does not improve a score. None of the bookkeeping below requires a model-visible schema, compulsory explanations, or approval of an utterance before it enters history.

## Minimal observation record

Preserve complete raw turns and available environment events in order, including contradictions, abandoned branches, errors, repetition and silence. Alongside them, keep an observer index: source turn/span, context available then, event/frame interpretation, links to earlier spans, and unresolved annotation questions. Start with a fixed natural-interaction window containing the full exact earlier history in every rendered input, with no accuracy feedback or probes added for measurement. Pause before context overflow; recent-window or recall policies are later, separately documented alternatives. Report the entire window and its selection rule; illustrative excerpts do not establish prevalence.

Separate two audits. **Record integrity** asks whether bytes, order, actor attribution, environment outcomes and references are faithfully retained. Hashes can detect changes relative to a recorded version, not certify that an account is true. **Semantic assessment** asks what an utterance commits to in its local frame and what evidence bears on it. A perfect log can contain inaccurate factual claims; a fictional event can be perfectly preserved without having happened externally.

Use provisional, possibly overlapping observer labels:

- **Authored narrative contribution:** an utterance proposes or narrates an event or relationship under a provisional local reading. Retaining the text does not establish its proposition as host-certified truth or canonical fact, even within a branch; no automatic story canon is assumed.
- **Record claim:** a statement about what was actually written, observed or executed previously. Compare against the cited record and accessible context.
- **Hypothetical, prediction or counterfactual:** distinguish a proposed future outcome from a scenario whose antecedent is explicitly contrary to the operative history.
- **Unresolved:** irony, metaphor, unstated framing, or competing readings. Preserve the excerpt and alternatives; do not force a correctness label.

Example: “the moon ate the key” may contribute a narrated event without establishing a canonical world fact. “Earlier I wrote that the moon ate the key” is separately checkable against history. “If it had eaten the key…” need not contradict either branch. Later factual use of an invention creates a new assessable claim; it does not retroactively turn its invention into an error. Contradictions may be narrative resources. Annotate incompatible commitments only where their frame, entity, time and branch coincide.

## What to count, and what not to infer

Repetition: report exact repeated spans and recurrence distance, with denominators in turns/tokens; label near-paraphrase judgments as interpretation. Separate a refrain or requested reprise from an apparently stuck loop. Neither frequency nor lexical diversity establishes understanding.

Revision: link original and replacement, what changed, whether an incompatible commitment was acknowledged, and any downstream reuse of the older version. Preserve both. A later correction is evidence of that correction, not proof of a stable mechanism or erased failure.

Prediction: archive the prediction, information boundary, target, horizon and interpretation before the outcome is revealed. Score only targets whose resolution is specified independently of the answer. If an utterance authors its own predicted outcome, record narrative follow-through rather than independent predictive success. Report all eligible predictions, unresolved outcomes and post-outcome reinterpretations. Do not infer calibration from confident-sounding prose; evaluate probabilities only if naturally supplied and sufficiently numerous under a declared scoring rule.

## Optional discriminating contact

After the observation window is frozen, an optional separate probe can test a narrow transfer hypothesis. Pair a renamed target preserving source operations with a matched target changing exactly one operation. With the transfer colleague, I revised my initial suggestion of “new rules”: changing all operations would remove the relation being tested. Give all comparison arms identical target-only evidence and a neutral invitation; withhold the transfer map and answers. No rule explanation is necessary for a correct prediction.

Compare accessible source history with an equally budgeted irrelevant history and a target-only baseline using the same model revision, token budget and decoding policy. A matched passive transcript can further ask whether active participation contributes beyond supplied text. This intervention changes history accessibility; it does not establish weight learning. Visible-history success supports context-mediated adaptation. Report offered, accepted, declined and uninterpretable contacts separately. Declining is missing ability evidence, not failure; unequal acceptance can make conditional comparisons causally inconclusive.

Discriminating next observation: source history helps on renamed operations while the model selectively changes predictions where target evidence changes one operation. Uniform copying across both targets favors a simpler imitation rival. Renaming alone tests a bounded relation, not universal understanding.

## Leakage and interpretation controls

Freeze generator families, scoring and invitations before evaluation; separate calibration examples from held-out families. Audit routes by which answers could enter prompts, summaries, filenames, demonstrations, scoring rubrics or evaluator context. Keep scoring keys external to the model. Report prompt variants, selection history and failed pilots; retire exposed tests rather than repeatedly tuning toward them. Publish participation and interpretability denominators alongside correct/incorrect counts. A second annotator can expose ambiguity, but agreement among agents sharing prompts, records and ancestry is not independent replication or a truth oracle.

## Primary sources actually read; scope limits

[Dwork et al. (2015), Generalization in Adaptive Data Analysis and Holdout Reuse](https://arxiv.org/html/1506.02629): read introduction/results and experiments/conclusion. Their synthetic classifier selects correlations using reused holdout data and appears successful despite random labels; Thresholdout mitigates this under specified conditions. This motivates fresh evaluation after prompt selection. Their i.i.d./algorithmic guarantees do not automatically apply to a single evolving garden; no Thresholdout guarantee is claimed here.

[Recht et al. (2018), Do CIFAR-10 Classifiers Generalize to CIFAR-10?](https://arxiv.org/html/1806.00451): read formal setup, main results, gap investigations and discussion, with introduction. Thirty classifiers lose absolute accuracy on newly collected images while relative ranking largely survives. The study does not establish adaptive overfitting as the cause. It motivates distinguishing fresh samples, changed distributions and ranking from absolute success; it supplies no small-language-model result.

## Cross-department review resolution

Reviewers correctly identified that my original “authored fact within that branch” wording could imply an automatic story canon. After reading DESIGN.md, I replaced it with “authored narrative contribution”: the inscription is mechanically retained, while its narrative interpretation stays provisional and creates no host-established semantic truth. This resolves a wording ambiguity, not a substantive disagreement with record-first mechanics. The initial window now explicitly uses full exact history and pauses before overflow; reduced-window/recall alternatives require later documentation. No model run accompanied this correction.
