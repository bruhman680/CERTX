# Reader/interpretation review for the derived-control Reddit report

Reviewed REPORT.md, PLAN.md, NEXT_CONTACT.md and RESULTS.json from RM-C1. This is an additional AI-assisted review of the record, not a blinded replication or fresh empirical confirmation.

## Most consequential clarifications

- The identity is elementary expansion plus standard realification. Present it as a useful derived **control**, not a new theorem, novel mathematical discovery, refutation of complex representations, or priority claim. The paper already expands its score in terms of energy and the real part of an inner product; our added framing is an explicitly information-matched real-coordinate baseline and consequences for interpretation.
- The 1,200 evaluations comprise **400 generated base pairs, each evaluated at three scales**. They are not 1,200 independent samples, retrieval tasks, models or language tests. Common random construction and scale repeats matter for describing the experiment, even though no statistical inference is made.
- Equal-norm language needs precision: a fixed query and equal nonzero candidate norms make R constant and therefore preserve cosine ranking, even if the query norm differs from candidate norms. Unit-normalizing all vectors is one sufficient special case. Across candidates with different R, monotonicity in c alone is insufficient to infer ranking equivalence.
- A complex d-vector and its real 2d-vector carry the same Cartesian information and number of real scalars. This does not establish identical runtime, numerical conditioning, training inductive biases, algebraic interfaces, or indexing cost. Polar phase at amplitude zero is not an observable extra degree of freedom in the complex value.
- Distinguish cosine on (Re, Im) coordinates from cosine on magnitudes, cosine on a raw concatenated (amplitude, phase) array, and abs(Hermitian inner product). These are different baselines. Raw phases have a wrap discontinuity; the exact baseline uses cos/sin or Cartesian coordinates.
- Phase information may be newly supplied by a context/encoder, or may just be a lossless change of coordinates of existing signed embeddings. Realification does not invalidate encoding improvements. Ask where a useful distinction originates rather than assuming the score invented it or the representation is useless.
- A metric does not have to infer semantics itself to be useful. The fair objection is to attributing improvements to the scoring rule without holding encoded information fixed, not to encoders or prescribed features being inherently illegitimate.

## Limits and attribution

- Formula checks do not reproduce the paper's operator retrieval benchmark, phase encoder, timing, storage engine, indexing or current product kernel. Current README and older paper are separately pinned sources; don't treat differences as errors without version/context analysis.
- Eight passing checks cover declared moderate synthetic inputs, not overflow/underflow, adversarial numerical values, variable dimensions, NaN/Inf, or arbitrary implementations. The existing implementation uses zip and assumes equal lengths; don't present it as a production validator.
- Missing-as-zero and destructive-sum witnesses are authored representation counterexamples, not measured faults of ResonanceDB. Storing records separately does not cancel their existence. A proposed aggregate cancellation hazard must be described conditionally.
- High or low alignment does not determine truth, authority, uncertainty or relevance. A contradiction can be relevant, but low cosine is not itself proof of contradiction. Arbitrary opposite vectors do not demonstrate scoped natural-language negation.
- The original run was coordinator-authored/unblinded. This new review is another agent in the same system/project context, not an outside researcher. Preserve that distinction if describing review history.

## Strongest useful objections to invite

1. Is the published formula transcribed exactly, including the factor1/2 and energy-balance factor?
2. Does an example violate the identity on finite, equal-dimensional, nonzero inputs in exact arithmetic, or does it instead reveal numerical/implementation mismatch?
3. Does a claimed retrieval improvement survive a full-information real-coordinate score, separately controlling energy and phase assignments?
4. Does a different product kernel break the premises? If so, that bounds this result rather than contradicting it.
5. Is magnitude meaningful/calibrated in the downstream task? A different ranking can be helpful even though its cause is energy balance.
6. Do practical complex pipelines deliver advantages in training, compositional operations, routing or deployment that this static pairwise identity doesn't assess?

## Useful follow-up experiments

- With fixed stored encodings, compare direct complex formula with the realified exact control. Score differences beyond numerical tolerance are a correctness issue, not an efficacy contest.
- With those encodings, compare cosine versus the energy-balanced expression at original norms and after declared normalization. Attribute any ranking change to energy handling, not unseen semantic reasoning.
- Evaluate encoder variations separately, using the same downstream scorer and held-out task families. Permit ordinary metadata/status-aware retrieval as a practical comparator, accounting for its supplied information.
- Independently prepare future questions before writer outputs. Include evidence-set recall (including relevant disagreement), correct source/version/status and downstream warranted decisions; report ties, unresolved answers, actual context-level counts and cost.

## Reddit presentation

Use ASCII math/code blocks alongside explanations; ordinary Reddit Markdown does not reliably render LaTeX. Include a short main result near the top, clearly marked definitions/assumptions, worked cases, reproducible code/links, exact run counts/errors, objections, and specific invitations for external checks. Near40k should add reconstructible reasoning rather than repetition. Count the raw Markdown body (including URLs/code) with Unicode and UTF-16 measures and retain headroom for Reddit editor transformations. Separate title and body; don't include delivery notes in the counted copy-ready body. State AI-assisted analysis plainly. Do not publish to Reddit on the user's behalf: they asked for a post they can publish.
