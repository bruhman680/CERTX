# ETH scout: shared summaries, exact reconstruction and verification boundaries

27 October 2026, America/Chicago. User requested a deeper scout for the Exponential Time Hypothesis breakthrough and useful connections to FRR. This contact identifies the release, reads selected primary mathematical/formal artifacts, and runs a small independent-development illustration. It is not a proof audit, Lean rebuild, practical SAT implementation, or validation of the claimed refutation.

## Release and claim

[OpenAI's 26 October announcement](https://openai.com/index/building-scientific-understanding-with-academic-communities/) reports an ETH refutation and Lean verification, while organizing external examination led by Russell Impagliazzo, Ramamohan Paturi and Ryan Williams. The announcement treats the manuscripts as raw research output requiring scientific understanding. We have not established completed community consensus or reproduced that verification.

Primary repository pinned to `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a` at access. [Manuscript directory](https://github.com/openai/math/tree/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026), dated 17 October, revised 25 October. [Readable mathematical source](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/build/main_full_version.tex).

For each fixed clause width k, the main theorem claims exact counting of satisfying assignments in time

`poly_k(n,m) * 2^[O_k(n log log n / sqrt(log n))]`

and polynomial space. At fixed clause density the claimed exponent improves to `O_k,D(n/sqrt(log n))`. A positive count decides satisfiability. Both exponents are o(n), so the stated result would refute ETH. They are not polynomial-time bounds. Constants, polynomial overheads, reductions and implementation costs matter; no usable speedup for our current tools is established. Fixed k is consequential: do not silently let it grow with n. A removed ETH-based conditional lower bound does not itself supply a fast algorithm for every affected problem.

## Selected mechanism, without claiming the proof is checked

The exposition writes a formula's count as a sum, over all Boolean assignments, of products of local clause polynomials. Direct evaluation is still exhaustive. It then introduces a polynomial deformation that restores the original target at zero. At chosen nonzero points, transformed factors can be assigned to groups, with interactions across groups mediated by shared bounded linear measurements. Once those measurements are fixed, local sums factor; interpolation from sufficient values/Taylor data recovers the target.

The sharpened appendix uses recursive Boolean tensor contraction, arithmetic modulo powers of two and truncated polynomial rings. Divisibility makes selected omitted terms exactly vanish at the working precision. This is an exact algebraic condition, not an instruction to ignore numerically small influences. The reconstruction argument, degree/multiplicity bounds, measurement-range bounds and arithmetic bit costs are essential obligations. The full construction and its proof have not been verified here.

A particularly transferable condition is in Definition `def:layout`: each factor's dependence on another group must be constant along the kernel of that group's summary map. Otherwise two locally indistinguishable states can give different factor values, and the factorization is invalid. Shared measurements also require bounded coefficient size/range; rank by itself does not bound how many states must be enumerated.

## Formal artifact scope

The [formalization manifest](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/formalization.yaml) identifies `OAI.Algorithms.SubexponentialSAT.SqrtLogSpace.exact_count_and_sat` in [Final.lean](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/OAI/Algorithms/SubexponentialSAT/SqrtLogSpace/Final.lean). Its statement chooses a fixed primitive machine per fixed k, gives exact count/decision outputs, bounds run time and visited space at all execution prefixes.

The inspected [comparator target](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/ComparatorChallenges/SubexponentialSAT.lean) explicitly defines exponent scale `n*(log(log(n+16)))^2/sqrt(log(n+16))`. This is the weaker squared-log-log bound, still subexponential, rather than a direct check here of the manuscript's sharper appendix theorem. Do not promote one endpoint's verification claim to every strengthened result.

[Comparator configuration](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/lean/ComparatorChallenges/SubexponentialSAT.json) names that theorem and permits `propext`, `Quot.sound`, `Classical.choice`; `enable_nanoda` is false. These are configuration contents, not a successful run log. The comparator challenge's `sorry` is a target placeholder; it is not evidence that the submitted solution uses an unproved premise. Conversely, inspecting a proof file and its `#print axioms` commands does not establish the dependency closure is clean or the build passes. Neither Lean nor comparator was run. Toolchain declares Lean v4.34.1.

## Useful extraction for our work: proposals and independently elementary consequences

1. **Task-relative sufficiency.** A handoff should preserve distinctions that can change its intended downstream decisions. Define the target before judging compression. This extends our joined-premise tests: two records may carry the same number while differing in the assignment that makes it applicable.
2. **Account for the interface.** Decomposing work into many small groups only helps when the shared interface is manageable. Count interface states, precision, origin/version dependencies, local cost and reconstruction cost; agent count or representation rank alone cannot establish efficiency.
3. **Preserve reconstruction obligations.** If a transformed task is easier, record how answers transfer back and the hypotheses required. Similar-looking transformed outputs or embeddings are insufficient. This directly matches our earlier representation/access/readout distinctions.
4. **Keep exactness separate from useful approximation.** Modular divisibility, bounded interval arithmetic and semantic uncertainty have different warrants. No universal semantic threshold or analogue of the paper's exact vanishing rule is derived.
5. **Pair search with a distinct check.** If we later encode finite evidence constraints as SAT, first verify the encoding preserves task meaning, then independently check assignments/certificates. A solver can correctly solve an incorrectly encoded task. Formal proof remains about its formal statement and trusted foundations, with a separate bridge to the intended research question.

These transfers are our interpretations and proposals, not empirical FRR benefits or additional claims made by the authors.

## Executed finite witness

[Protocol](WITNESS_PROTOCOL.md), [code](summary_witness.py), [full results](WITNESS_RESULTS.json), [execution receipt](EXECUTION.json). One exact enumeration of 4,368 Boolean assignments across n=4,8,12; exit zero; inputs unchanged. No sampling, trained model or independent reviewer.

Two rank-one maps are compared: sum of bits, versus binary-place-value weighted sum. At n=12 their image cardinalities are 13 and 4,096. The count summary exactly determines parity, but 11 of its 13 fibers contain both first-bit values. The binary summary determines both targets by encoding every vector separately. This illustrates two elementary facts: low row rank need not mean a small state space; and useful compression depends on which downstream question must survive. It neither reproduces nor tests ETH's claimed general algorithm.

## Access, confidence and next contact

Read scope: main theorem, selected overview sections on encoding/deformation/shared measurements/interpolation, layout and separation lemma, quantitative tensor interface and selected precision/recursion sections, circuit corollary; static formal endpoint/target/config/manifest and documentation. Four TeX sources fetched and hashed, not audited line by line. Original documents remain in their upstream repository; only hashes and source locations are recorded here.

Access limits: browser rejected pinned PDF as octet-stream; switched to available TeX. Recursive Lean tree fetch failed; used directory/manifest-specific reads. One guessed `SqrtLog/Statement.lean` path failed; followed the final file's actual `StatementCanonical` import. No unexplored absence is a novelty claim. No authors contacted, software installed, external API inference, or proof checker run.

Confidence high in release identity, inspected statements and finite witness arithmetic; moderate in conceptual transfer; unestablished for full proof correctness, practical speedup and improved reader behavior. Next strongest remains fresh joined-premise reader cases. Add mirrored same-summary/different-warrant cases and require explicit scope: a summary can be adequate for one question and inadequate for another. Lateral formal-methods contact: a tiny independently checkable evidence-constraint encoding with a deliberately wrong encoding control. No framework/core/queue status changes are warranted by this scout.
