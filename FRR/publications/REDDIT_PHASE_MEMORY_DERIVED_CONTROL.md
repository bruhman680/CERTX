# Phase-aware memory: an information-matched control, a derivation, and an invitation to test it

This is an AI-assisted research note from an ongoing public exploration of memory, retrieval, and reasoning. I am posting it as a record of how our understanding changed and as an invitation for other people to reproduce, criticize, or extend the work. The useful outcome would be a clearer experiment or a corrected interpretation, whether or not it favors our initial intuitions.

The immediate question came from reading Aleksandr Listopad's *Wave-Based Semantic Memory with Resonance-Based Retrieval: A Phase-Aware Alternative to Vector Embedding Stores*, arXiv:2509.09691v1. The paper describes amplitude/phase representations and a resonance similarity. Our contribution here is a small mathematical control and its implications for experimental design. This post does not reproduce the database, its performance benchmarks, or a learned language encoder.

All formulas below use plain text because Reddit does not consistently render LaTeX. "Control" means a comparison condition that helps locate the cause of an observed difference. It is not a feedback controller or a proposed universal law of memory.

## 1. The short result

Take the paper's published similarity S between two complex patterns. Preserve every complex coordinate by writing its real and imaginary parts as an ordinary real vector. Let c be ordinary cosine similarity between those expanded real vectors. Let R measure the balance between their squared norms.

Then the published score can be written exactly as:

    S = R/2 + (R^2 * c)/2

For equal, nonzero norms, R = 1, so:

    S = (1 + c)/2

That is an increasing affine transformation of cosine. It produces the same ranking and the same ties on the same represented information. It can produce different numeric scores, which matters for thresholds and weighting, but it cannot produce a different exact top-k ordering in that equal-norm setting.

With unequal candidate norms, R can vary across candidates and rankings can change. That is a real additional scoring effect. It should be tested separately from the effect of supplying information in phases that a comparison system never received.

This is the central proposal: when evaluating phase-aware retrieval, include a baseline that retains the same phase information in real coordinates. Otherwise, a comparison can mix up a better representation, additional inputs, a different score, and a different database implementation.

## 2. Why this question arose

Our memory exploration asks what survives when records and questions change. A compressed record can retain an old conclusion while losing its conditions. A source can exist without reaching the reader who needs it.

Wave and substrate language suggests representing context and competing influences explicitly. An analogy alone cannot tell us what a method preserves or why it improves a measured result.

We therefore narrowed the question. Before asking whether a wave-based memory improves an agent, ask what its published comparison formula computes. Before asking whether phase discovers semantic distinctions, ask where those phases come from. Before asking whether a database retrieves better, make sure competing methods receive comparable information.

The identity separates parts of the memory question that could otherwise move together.

## 3. What source was examined

Primary source: [the versioned paper, arXiv:2509.09691v1](https://arxiv.org/abs/2509.09691v1). We read the PDF's sections and appendix. The paper supplies a deterministic amplitude/phase score, externally assigned phases, compact operator experiments, and scan-based retrieval measurements. Its own limitations include phase noise, calibration, and scan cost. We did not reproduce those experiments.

We also inspected the [repository README at a fixed commit](https://github.com/LexProfi/ResonanceDB/blob/f059f06b0875f3e15ea058815202d332c772ee43/README.md). It describes later product features and says exact current scoring details are undisclosed. Consequently, the mathematical analysis here concerns the published v1 formula. It cannot establish equivalence to every current product behavior.

An initially guessed v2 HTML address returned 404. We corrected the source to v1 before the formula experiment. That access mistake is retained in the source record. It did not become a silently assumed second version.

This distinction matters: a paper, a current README, and an executable deployment are different artifacts. A conclusion about one should not quietly inherit the scope of another.

## 4. Three things that need separate names

An encoder turns inputs into a representation. A score compares representations. A retrieval system searches a collection using a score, routing policy, index, filters, and storage machinery.

Suppose a text encoder places a polarity marker into phase. A phase-sensitive score can use that marker. A baseline that receives only amplitudes cannot. If the first system wins, the experiment may show that the marker is useful, but it has not isolated the advantage of complex arithmetic or of a particular score.

Similarly, an index can improve latency without changing the underlying score, and a score can change rankings without improving the encoder's semantics. A database can preserve metadata that an embedding alone omits. These are all potentially useful contributions, but they answer different questions.

For this post, the boundaries are:

- Representation: which distinctions are present in the stored numbers?
- Scoring: how do those numbers determine pairwise similarity?
- Retrieval: which records are returned, at what cost and approximation level?
- Application: does a reader use the returned evidence correctly?

The identity addresses scoring given a representation. The later discussion proposes how to test the surrounding stages.

## 5. Notation and the published expression

Let z and w be complex vectors with the same finite dimension d. Their coordinates can be written in polar form:

    z_j = A_j * exp(i * phi_j)
    w_j = B_j * exp(i * theta_j)

Amplitudes A_j and B_j are nonnegative. Phases specify directions in the complex plane. Define energies:

    E_z = sum_j |z_j|^2
    E_w = sum_j |w_j|^2

For positive energies, define the energy-balance factor:

    R = 2 * sqrt(E_z * E_w) / (E_z + E_w)

The published score is:

    S(z,w) = (1/2) * [sum_j |z_j + w_j|^2 / (E_z + E_w)] * R

The sum is a sum of coordinatewise squared magnitudes. It is not the squared magnitude of one sum across all dimensions. Those operations are different; replacing one with the other would analyze a different formula.

When both inputs have zero energy, the paper defines S = 0. If exactly one input has zero energy, the expression also gives zero through R. Cosine is undefined for a zero vector, so our cosine-based identity will be stated only for positive energies, with the zero-score convention handled separately.

## 6. Realification preserves the supplied information

Write each coordinate as z_j = x_j + i*y_j and w_j = p_j + i*q_j. Form ordinary real vectors:

    u = [x_1, ..., x_d, y_1, ..., y_d]
    v = [p_1, ..., p_d, q_1, ..., q_d]

Each vector now has 2d real coordinates. This is often called realification. Interleaving real and imaginary coordinates would work equally well, provided both patterns use the same ordering.

The mapping is invertible. Given u, we can reconstruct every z_j. It has not discarded phase or added an independent semantic annotation. It has changed coordinates from complex notation to a real representation carrying the same numeric content.

The corresponding identities are:

    ||u||^2 = E_z
    ||v||^2 = E_w
    u dot v = sum_j (x_j*p_j + y_j*q_j)
            = Re(sum_j conjugate(z_j) * w_j)

This is why the appropriate control is not cosine on amplitudes alone. Cosine on amplitudes sees [A_1, ..., A_d]. Cosine on u sees both quadratures. These are different information conditions.

This preserves the complex vector, not every possible annotation in a raw polar buffer: phases differing by 2*pi denote the same value, and a zero-amplitude coordinate has no recoverable phase. If those raw fields carry extra application meaning, preserve them separately. Polar and Cartesian formats can also differ in quantization, storage and execution cost.

## 7. Derivation, step by step

For each coordinate:

    |z_j + w_j|^2
      = |z_j|^2 + |w_j|^2 + 2*Re(conjugate(z_j)*w_j)

Summing over coordinates gives:

    sum_j |z_j + w_j|^2 = E_z + E_w + 2*(u dot v)

Let c be ordinary real cosine:

    c = (u dot v) / (||u|| * ||v||)
      = (u dot v) / sqrt(E_z * E_w)

Substitute the expanded numerator into S:

    S = (1/2) * [1 + 2*(u dot v)/(E_z + E_w)] * R

But:

    2*(u dot v)/(E_z + E_w)
      = [2*sqrt(E_z*E_w)/(E_z + E_w)] * c
      = R*c

Therefore:

    S = (R/2) * (1 + R*c)
      = R/2 + R^2*c/2

Nothing in this expansion assumes that imaginary parts vanish. Nothing assumes that phases are zero, that coordinates are nonnegative, or that the patterns came from language. It applies to arbitrary finite complex vectors with positive energies in exact arithmetic.

This is the reason for calling it an information-matched control: the real calculation sees precisely the coordinates needed to reproduce the score. Appendix A of the paper already expands the score into energies and a real inner-product term. Our additional step makes the all-complex real-coordinate control and its experimental consequences explicit; we claim no new theorem priority.

## 8. Exactly when rankings must agree

If E_z = E_w > 0, then R = 1 and S = (1+c)/2. For c values c_1 and c_2:

    S_1 - S_2 = (c_1 - c_2)/2

The sign of the difference is preserved. Ties are preserved too. Sorting exact scores therefore yields the same ordering, apart from how an implementation resolves ties or floating-point differences.

There is a slightly broader ranking statement. Fix one nonzero query z and compare it with candidates whose norms are all the same positive value. The query's norm does not need to equal that candidate norm. R is still constant across candidates, so S is still an increasing affine function of c, with slope R^2/2.

Thus equal candidate norms are sufficient for ranking equivalence for a fixed query. Equal query and candidate norms give the especially simple numeric identity S = (1+c)/2.

If candidate norms vary, the offset and slope vary with the candidate. Ordinary cosine ranking alone is then insufficient. The full real-coordinate control must retain energies and evaluate R/2 + R^2*c/2. That control reproduces the formula without needing an equal-norm assumption.

## 9. Ranking equivalence is narrower than system equivalence

Equal rankings do not imply equal score values, equal calibration, or equal downstream behavior under arbitrary use of those scores.

If a system accepts records when S >= t in the R = 1 setting, the equivalent cosine threshold is c >= 2t - 1. Using the same numerical threshold for both methods would change the decision rule. That would be a threshold comparison, not evidence of different rankings.

Likewise, sampling or weighting records with raw scores is not the same as selecting top-k. Applying softmax to S with a fixed temperature changes weights relative to applying softmax to c at that same temperature. For R = 1, the additive constant cancels within a softmax, and matching cosine temperature T_c requires score temperature T_S = T_c/2. For a constant R, T_S = R^2*T_c/2. Candidate-dependent R requires the full formula.

Approximate indexes may retrieve different candidate sets even when their exact pairwise scores are mathematically related. Precision, tie handling, routing, filters, and candidate truncation can all matter. The identity supplies a score-level control; it does not make those implementation details disappear.

A fair test should name its object: exact ranking, thresholded acceptance, calibrated probability, weighted aggregation, approximate retrieval, or final task performance.

## 10. What R actually changes

R lies in (0,1] for positive energies. It reaches one when the two energies match and approaches zero when one norm becomes very large relative to the other.

Let t = ||v|| / ||u||, with t > 0. Then:

    R = 2t / (1+t^2)

The same R occurs for t and 1/t. The score therefore treats reciprocal norm ratios symmetrically for a fixed angular relationship.

For a fixed R, c ranges from -1 to 1, so:

    R*(1-R)/2 <= S <= R*(1+R)/2

The lower endpoint occurs for opposite directions; the upper endpoint occurs for aligned directions. With R = 1 these become zero and one. For a fixed angular relationship, changing R can change the score in ways that deserve care.

In particular, "energy balancing penalizes every unequal-energy pair" is too broad. For c = -1:

    S = R*(1-R)/2

This is zero at R = 1 but positive for 0 < R < 1. Unequal-energy opposite patterns can receive a larger score than equal-energy opposite patterns. The term is a balance-dependent modulation, not a uniform pointwise penalty relative to every equal-energy case.

## 11. Small examples that expose the distinctions

Use the real query u = (1,0), the realification of one complex coordinate z = 1+0i.

Candidate v = (1,0): c = 1, R = 1, S = 1. Candidate v = (-1,0): c = -1, R = 1, S = 0. Candidate v = (0,1): c = 0, R = 1, S = 0.5.

Now double the aligned candidate: v = (2,0). Cosine remains one, but R = 4/5 and S = 18/25 = 0.72. Double the opposite candidate instead: v = (-2,0). Cosine remains minus one, but S = 2/25 = 0.08.

These exact values make two points. The published score is sensitive to magnitude relationships that ordinary cosine ignores. Also, opposition does not force a zero score at every magnitude: exact cancellation requires matched magnitude as well as opposite direction.

For one complex coordinate with relative phase delta and norm ratio t, the formula becomes:

    S = t * (1+t^2 + 2t*cos(delta)) / (1+t^2)^2

At t = 1 this is (1+cos(delta))/2. A phase difference of pi/2 gives 0.5; a phase difference of pi gives zero. These are geometric statements. Naming delta = pi "negation" requires an additional encoding contract.

## 12. A concrete ranking reversal at unequal norms

Take the same unit query. Candidate A is (10,0), fully aligned but ten times the norm. Candidate B is (0,1), orthogonal and equal in norm.

Cosine ranks A above B:

    c_A = 1
    c_B = 0

For A, R = 20/101. Substituting into the score gives:

    S_A = 1210/10201, approximately 0.118616

For B, R = 1 and S_B = 0.5. The resonance formula ranks B above A.

This example prevents an overclaim: the score is not merely shifted cosine in every dataset. It is shifted-and-scaled cosine with a candidate-dependent energy term. That term can reverse rankings when norms differ.

Whether that reversal is useful depends on what norm means in the application. If norm encodes a calibrated intensity that should match the query, the reversal might be desirable. If norm is an arbitrary artifact of an upstream encoder, it might be harmful. The algebra cannot choose that semantic policy for us.

A practical experiment should therefore vary amplitude calibration independently of the labels it is trying to predict, or clearly state why amplitude carries task-relevant information.

## 13. What phase carries, and what it does not establish

Two patterns can have identical amplitudes and different phases. For example, z = (1,0) and w = (-1,0) have identical amplitude vectors but opposite real directions. Amplitude-only cosine treats their amplitude profiles as identical. A representation retaining their signs or phases distinguishes them.

The information-matched real vector also preserves this difference. Its cosine contains phase explicitly:

    c = sum_j A_j*B_j*cos(phi_j-theta_j) / sqrt(E_z*E_w)

Thus ordinary cosine on these coordinates is phase-sensitive. It is amplitude-only comparison that discards phase. The control is also not cosine on raw angle fields, where the arbitrary phase wrap can cause problems, or the absolute value of a complex inner product, which defines another score.

An ordinary real embedding may already encode some polarity or relational information. Conversely, a complex embedding may encode it poorly. The coordinate type alone does not decide whether a learned representation tracks the intended concepts.

If phase is supplied by an oracle that already knows which text is negated, a downstream retrieval success cannot be attributed wholly to the retrieval mechanism. The oracle's information is part of the system. If a learned encoder supplies phase, its training data, objectives, errors, and transfer behavior become part of the evaluation.

The useful question is not whether phase is allowed to mean something. It is how that meaning is assigned, preserved, and tested on cases that were not used to define the assignment.

## 14. Why logical negation needs more than a sign flip

Multiplying a vector by -1 is a precise algebraic operation. Natural-language negation is often scoped, conditional, or attached to a particular predicate rather than an entire sentence.

Consider "the valve is not open," "the valve was not open yesterday," and "it is not established that the valve is open." These statements differ in time, factual status, and the location of the negation. A global flip of a single sentence vector does not, by itself, specify which distinction is being represented.

Similarly, "not all samples passed" differs from "all samples failed." A representation might learn useful approximations for these cases, but a phase label alone is not a proof that it respects quantifier scope or epistemic uncertainty.

There is also a retrieval-policy issue. If the query asks whether a valve is open, evidence that it is closed can be highly relevant. A score that assigns low agreement to opposite content may be appropriate for finding supporting examples and inappropriate as the only route for evidence checking.

This suggests evaluating scoped transformations and evidence tasks directly. Hand-constructed phase opposites are helpful geometric fixtures. They do not replace a held-out semantic evaluation with independently determined truth conditions and relevance judgments.

## 15. Relevance and agreement need separate treatment

Suppose a working record says, "Batch G6 meets the release limit." A later measurement shows it does not. An agreement-oriented search might favor documents repeating the old conclusion. An evidence-oriented search should retrieve the later measurement, even if it conflicts with the query's wording or current hypothesis.

There are at least three different relationships here:

- Topic relevance: does the record concern the batch and criterion in question?
- Stance or compatibility: does it support, oppose, qualify, or leave the claim unresolved?
- Evidential standing: is it current, attributable, measured, estimated, or superseded?

A scalar similarity might help with one or more of these, but its meaning must be tested. Low compatibility should not automatically mean low topic relevance, and high compatibility should not establish authority.

One possible design is to retrieve broadly for evidence coverage and then classify support, contradiction, and uncertainty with explicit source links. Another is to maintain separate channels or operators. Neither proposal has been validated by this formula experiment.

The immediate lesson is methodological: define what a successful retrieval should return before interpreting a favorable similarity score as successful reasoning.

## 16. Cancellation is not the disappearance of a history

If two equal and opposite patterns are added, their sum is zero. That follows directly from the representation. It can be useful when an application intends to cancel signals.

But compare two collections: one contains no records, and another contains both z and -z. If the only retained state is the unlabelled sum, both collections can produce zero. Their histories are different, and a later question might need that difference.

This is a development witness about a deliberately lossy aggregation rule. We did not establish that ResonanceDB discards individual records this way. Its pairwise score does not require replacing an archive with a single sum.

For our own memory explorations, the witness motivates preserving record identities and provenance alongside any aggregate. An aggregate may be a useful navigation signal while original records remain separately retrievable. If the task requires knowing that a dispute occurred, cancellation should not be treated as evidence that no dispute existed.

The distinction is especially important when a summary says "net effect zero." Zero net effect can coexist with large opposing components, an unresolved contradiction, or no observations at all. Which interpretation is correct depends on the preserved record, not just the aggregate value.

## 17. Unknown is not a measured zero

A related failure occurs if both "no measurement was available" and "the measured quantity was zero" are encoded as the same zero vector, with no separate status information.

No deterministic downstream comparison can recover which input situation occurred from that identical stored representation alone. This is an indistinguishability statement: the input to the comparison is the same in both cases. Additional context, a status bit, an access log, or an original record could resolve it; the score alone cannot.

This does not mean zero is an invalid measurement or that a missing value cannot be modeled probabilistically. It means the missingness policy is part of the representation and should be explicit.

For example, a record could retain a numeric field, an availability flag, units, source identity, and a reason for absence. The right structure depends on the task. A learner may use missingness patterns as informative signals, but that still does not turn missingness into a direct observation of zero.

This connects to our earlier memory work: a faithful summary can still be insufficient for a later question. Faithfulness, available detail, and warranted inference are separate properties.

## 18. What the numerical contact actually did

The saved protocol fixed the checks before the local run. It used Python's standard-library complex arithmetic, real arithmetic, math.fsum, and a fixed pseudorandom seed: 20261025.

Dimensions were 1, 4, 16, and 64. For each dimension, the script generated 100 base pairs with Gaussian real and imaginary coordinates. It reused each pair with second-pattern scale factors 0.25, 1, and 4. This produced 1,200 scored comparisons from 400 base pairs.

Those 1,200 comparisons are not 1,200 independent experiments. The three scales share a base pair, and the checks operate on related mathematical quantities. We use them as implementation fixtures, not as a statistical sample proving a population effect.

The checks compared direct complex-sum evaluation with the expanded real-coordinate expression, tested symmetry and a common phase rotation, checked the equal-norm reduction, and inspected the observed score range. Fixed examples checked opposite phases, amplitude scaling, and cancellation. A separate rational calculation checked the doubled-amplitude scalar case exactly.

The run did not query a language model, build a database, learn phases, measure retrieval accuracy, or time a search engine. The finite checks support the implementation of the algebra. The algebra, with its stated assumptions, supports the general identity.

## 19. Recorded numerical results

The saved run reported the following maximum absolute discrepancies:

| Check | Maximum absolute discrepancy |
|---|---:|
| Direct complex score versus real-coordinate expression | 5.551115123125783e-16 |
| Symmetry under swapping inputs | 0 |
| Common phase rotation applied to both inputs | 5.551115123125783e-16 |
| Equal-norm score versus (1+c)/2 | 2.220446049250313e-16 |

The observed random-case scores ranged from approximately 0.00670809 to 0.99648501. That observed range is not the proof that all scores lie in [0,1]; the formula supplies the relevant bounds. A finite sample that stays inside an interval cannot establish a universal range guarantee by itself.

All eight declared checks passed; the floating-point equivalence checks used tolerance 1e-12. The fixed doubled-amplitude example produced 0.7200000000000001 in floating point. The separate Fraction calculation gave exactly 18/25, or 0.72.

The original run was prepared and checked by the same coordinating assistant. It was not a blinded replication. For this publication, additional AI reviewers were asked to challenge the mathematics and interpretation. That review does not retroactively turn the original run into an independently designed empirical study.

## 20. A small self-contained reproduction

The following code checks the identity on constructed vectors. It uses no database package, model weights, network access, or third-party Python dependency. Save it as a Python script and run it. This is an explanatory reproduction, not a replacement for the original frozen script and its exact random-number sequence.

```python
import math
import random
from fractions import Fraction

def energy(z):
    return math.fsum(abs(x) ** 2 for x in z)

def published_score(z, w):
    if len(z) != len(w):
        raise ValueError("dimensions must match")
    ez, ew = energy(z), energy(w)
    if ez == 0 or ew == 0:
        return 0.0
    r = 2 * math.sqrt(ez * ew) / (ez + ew)
    total = energy([a + b for a, b in zip(z, w)])
    return 0.5 * total / (ez + ew) * r

def real_coordinates(z):
    return [x.real for x in z] + [x.imag for x in z]

def matched_score(z, w):
    if len(z) != len(w):
        raise ValueError("dimensions must match")
    u, v = real_coordinates(z), real_coordinates(w)
    eu = math.fsum(x * x for x in u)
    ev = math.fsum(x * x for x in v)
    if eu == 0 or ev == 0:
        return 0.0
    c = math.fsum(a * b for a, b in zip(u, v))
    c /= math.sqrt(eu * ev)
    r = 2 * math.sqrt(eu * ev) / (eu + ev)
    return r / 2 + r * r * c / 2

rng = random.Random(20261025)
largest_error = 0.0
for d in (1, 4, 16, 64):
    for _ in range(100):
        z = [complex(rng.gauss(0, 1), rng.gauss(0, 1))
             for j in range(d)]
        w = [complex(rng.gauss(0, 1), rng.gauss(0, 1))
             for j in range(d)]
        for scale in (0.25, 1.0, 4.0):
            ws = [scale * x for x in w]
            err = abs(published_score(z, ws)
                      - matched_score(z, ws))
            largest_error = max(largest_error, err)

assert largest_error < 1e-12
assert published_score([1+0j], [-1+0j]) == 0.0
assert abs(published_score([1+0j], [2+0j]) - 0.72) < 1e-12
assert Fraction(1, 2)*Fraction(9, 5)*Fraction(4, 5) == Fraction(18, 25)
print("largest absolute discrepancy:", largest_error)
```

The exact final discrepancy need not match the archived run: this shorter illustration does not consume random numbers for the common-phase checks in the same order. To reproduce the archived sequence, use the versioned check.py, PLAN.md, and RESULTS.json linked below.

For the original script, keep PLAN.md beside it; the script hashes that file. In a new working folder:

```sh
base=https://raw.githubusercontent.com/bruhman680/CERTX/933af8bdb1e9d9f34a037b55e1609f1574a0a83c/FRR/evaluation/resonance-memory-contact-v1
mkdir rm-c1
cd rm-c1
curl -fLO "$base/check.py"
curl -fLO "$base/PLAN.md"
python check.py
```

This writes a local RESULTS.json. Compare its checks and errors with the pinned reference; platform arithmetic can affect final bits.

## 21. Numerical and implementation boundaries

The mathematical identity is exact; two floating-point implementations need not return bit-for-bit equal values. Summation order, conversion from polar coordinates, trigonometric evaluation, dtype, and fused operations can change the last bits.

The code above is intentionally a moderate-input illustration. Directly multiplying energies can overflow for extreme inputs, and tiny energies can underflow. NaN and infinity need an explicit policy. The code is not a production numerical kernel, a security boundary, or a complete input-validation library.

The original archived script also assumes equal dimensions and uses zip, so it would silently truncate an invalid unequal-length pair. All generated test pairs had matching lengths. The explanatory snippet above adds a dimension check rather than suggesting the historical script had already validated every external input.

A production implementation could use scaled norms or other stable arithmetic, then validate against a suitable high-precision reference across the intended range. That is a separate engineering task. We have not claimed that the real-coordinate expression always has better numerical stability or speed than the direct expression.

If two approximate implementations disagree only near ties, examine exact or high-precision scores and tie policies before attributing the difference to a new semantic capacity.

## 22. What would count as a fair comparison

An informative study would give each method the same underlying examples and identify exactly what information reaches each comparison condition. A useful set of conditions could include:

1. Amplitude-only cosine: an explicit phase-removal ablation.
2. Full real-coordinate cosine: real and imaginary parts retained.
3. The published complex formula: amplitude and phase retained.
4. The full real-coordinate formula with the same R term.
5. A task-appropriate metadata or symbolic baseline for status and scope.

Conditions 3 and 4 should agree in exact arithmetic. If they differ substantially, first inspect the implementation or whether the formulas really match. Conditions 2 and 3 test energy modulation when norms vary. Conditions 1 and 2 test what is lost when phase information is removed, provided all other inputs are controlled.

The metadata baseline asks whether a known distinction is better handled explicitly for the intended task. It should not be assumed to win, and it should not be denied information supplied to the phase encoder.

This structure makes several outcomes interpretable. A phase-removal ablation can fail while the information-matched baseline succeeds. That would support retaining the distinction without establishing a uniquely complex-number advantage.

## 23. What should be held fixed, and what may vary

For a scoring comparison, hold the encoded records, query content, available metadata, candidate pool, and evaluation labels fixed. Vary the score or the norm policy deliberately. Report whether vectors were normalized and when.

For an encoding comparison, hold the task and available source information fixed while changing the encoder. Report the encoder's parameter count, supervision, training data, preprocessing, and any external annotations. If two representations have different capacity or scalar storage, say so rather than calling them matched merely because both are named "d-dimensional."

For a database comparison, report index construction, approximation settings, recall targets, filtering, concurrency, hardware, memory, and end-to-end costs. Comparing an exact scan with an approximate index at different recall is a different tradeoff from comparing exact pairwise scores.

For a reader experiment, record which evidence was actually delivered and read. An archive link is not the same as accessible content. An optional retrieval tool is not the same as a successful retrieval, and a retrieved record is not proof that it influenced the answer correctly.

These distinctions need not make every experiment enormous. They let a small experiment answer a small, identifiable question instead of accidentally claiming to answer all four.

## 24. How this changes our next memory experiment

Our earlier short writer-reader contact used two summaries and four fresh reader contexts. Both summaries retained all four fixed task bases. All sixteen final question responses were grounded within the supplied materials. Access to originals corroborated answers rather than rescuing omitted evidence.

That result is useful, but it does not show that compression loss has been solved, that retrieval is unnecessary, or that a particular word budget is optimal. One writer per budget also cannot isolate a causal budget effect. Those limitations remain in the history.

The next proposed contact uses a longer versioned history with corrections, scoped claims, uncertainty, and conflicting observations. Future questions should be prepared independently of the writer outputs and fixed before summaries are seen. Otherwise, we could choose questions afterward merely to manufacture a desired omission or rescue.

The phase-memory analysis adds an equal-information requirement and a distinction between finding agreement and finding relevant evidence. We want to observe whether a reader preserves and applies the needed relationships, rather than rewarding familiar wording or a high similarity score by itself.

This is a design direction. The longer-history agent experiment has not yet run, and this post should not be read as its result.

## 25. Proposed measurements for that contact

Fidelity asks whether a stored summary or representation misstates the source. Sufficiency asks whether it contains enough for the later task. Retrieval coverage asks whether the relevant originals reach the reader. Warrant asks whether the final answer follows from what the reader actually had.

These properties can come apart. A faithful summary can omit a later-needed unit. A sufficient record can remain undiscovered. A correct answer can be an unsupported guess. An unresolved answer can be appropriate when the evidence genuinely fails to establish the requested quantity.

For a versioned history, add source and status selection: did the reader distinguish a correction from a superseded record, an estimate from a measurement, or a contradiction from a missing value? If authority is stipulated by the packet, do not claim the reader independently authenticated a real source.

Costs should include all declared attempts, retrievals, and failures, not only the final accepted output. Actual word-budget violations should be preserved rather than silently trimmed. Repeated questions within one reader context should not be counted as independent participants.

These measurements are practical candidates, not an established universal metric for reasoning. Their value depends on whether they distinguish failure modes that change what we should build or investigate next.

## 26. Objection: "This is just ordinary algebra"

Yes. The paper's appendix already supplies most of the expansion, and realification is standard. We claim no mathematical novelty or priority. The purpose is an explicit experimental control: retaining phase in one arm while removing it from another does not isolate a scoring advantage.

Prior references for this exact normalized expression and its evaluation would improve the record. Rediscovery is useful here if it clarifies the next test.

## 27. Objection: "Complex representations still have advantages"

They can: structured rotations, binding, parameter constraints, training behavior, indexing, or hardware may be useful. This identity concerns one static pairwise function on fully retained coordinates. It does not compare every complex and real model.

If a practical advantage survives matched-information controls, locate and measure it. The score identity leaves those engineering questions open.

## 28. Objection: "The complete system does more"

Agreed. Encoder, routing, storage, filters, and reasoning can change end-to-end behavior. We did not execute the current product kernel. A claim about that system needs a system experiment.

Component controls remain useful: replace only the published score with its exact real expression, verify agreement, then vary encoding or routing separately. This identifies where a useful effect originates.

## 29. Objection: "Are the checks proof?"

The proof is algebra. Finite checks help find transcription and programming errors; they do not establish a universal memory theory or substitute for language evaluation. The original run was coordinator-authored and unblinded. Later AI review is additional scrutiny, not outside empirical replication.

For discrepancies, please share inputs, formula, dtype, norm policy and tolerance. A reproducible boundary case is valuable.

## 30. What would change our interpretation

An exact-arithmetic counterexample under the assumptions challenges the identity. A formula-transcription error changes its target. Overflow challenges a numeric implementation. A newer kernel can compute a different function without contradicting this historical result.

Held-out semantic improvements support the tested encoder or system. Timing gains at matched recall support implementation claims. Update the specific affected claim and preserve the correction path.

## 31. Scope of the conclusion

The supported result is the exact control and its ranking consequences. We have not established general language understanding, physical quantum behavior, FRR efficacy, or an optimal memory policy. Additional metadata and complete archives also have costs and can contain errors.

The proposed next test separates preservation, retrieval, status and application. It remains a proposal, not a result of these formula checks.

## 32. The garden interpretation

Give two gardeners different records and their decisions can differ before arithmetic enters the picture. First ask what each could see, then how they compared it, what evidence they found, and whether it justified the action.

Phase can preserve a useful distinction. Real coordinates can preserve the same supplied distinction. An energy-aware score can express a different preference. None of these ensures that the most relevant contradiction reaches the reader.

Our next growth is to preserve a longer history, prepare future questions before summaries are seen, and observe which relationships survive. Learning why two descriptions compute the same thing is useful growth too.

## 33. Artifacts and invitation

The original contact is preserved at a fixed Git commit. Its report, plan, code, results, source record, and proposed next contact are available together:

[RM-C1 report and linked artifacts](https://github.com/bruhman680/CERTX/blob/933af8bdb1e9d9f34a037b55e1609f1574a0a83c/FRR/evaluation/resonance-memory-contact-v1/REPORT.md)

[Original check.py](https://github.com/bruhman680/CERTX/blob/933af8bdb1e9d9f34a037b55e1609f1574a0a83c/FRR/evaluation/resonance-memory-contact-v1/check.py)

[Recorded RESULTS.json](https://github.com/bruhman680/CERTX/blob/933af8bdb1e9d9f34a037b55e1609f1574a0a83c/FRR/evaluation/resonance-memory-contact-v1/RESULTS.json)

Please challenge the formula, the assumptions, the comparison design, or the proposed application. Especially useful contributions would be an independently implemented check, a prior reference for the exact expression, a well-defined semantic task, or an example where information-matched controls change the interpretation of an apparent improvement.

If an experiment fails, the failure belongs in the record. If a source or assumption changes, the correction should have a visible path back to the claim it affects. This post is one layer of that history, open to revision through evidence rather than a statement that the exploration is finished.
