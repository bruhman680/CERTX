# Cycle 3: final language coherence review

5 November 2026 (client date). Read DESIGN.md and all three CYCLE2 review files; no new source scout or execution. Research only.

**Judgment:** the candidate is coherent enough to enter specification after the small corrections below. It consistently selects an expression surface, pure bounded evaluation, pinned named procedures, and explicit data checkpoints. It is not yet an executable language contract, and does not claim to be one.

## Blocking ambiguities to correct in DESIGN.md

1. **Computation versus publication still conflicts.** §2 says successful output *can* be published and lists `run` and `publish` separately. §3 instead says normal completion triggers atomic publication before success. Replace §3's normal-completion paragraph with: “Normal completion returns `COMPUTED` and a bounded candidate result. A separate explicit `publish`, or a declared `run-and-publish` action, validates quotas and atomically stores the artifact and corresponding receipt before returning `PUBLISHED`. Pure `run` does not publish its result. Every action records a bounded receipt; result retention between actions has an explicit cap and expiry rule. Errors publish no successful result.” Add that defining/revising a valid procedure is itself a durable publication action; drafts remain ordinary data. Receipts are distinct from guest results. This resolves an observable difference, not a stylistic preference.

2. **Symbols are half-present.** §1 lists symbols as distinct values, but core expressions omit quotation/symbol construction and examples require no symbols. Simplest correction: “Identifiers are source syntax, distinct from runtime strings; runtime symbol values and quotation are deferred. Tags can be text inside lists.” Alternatively retain symbols, but add literal syntax, equality and serialization explicitly. Do not imply arbitrary quoted lists are callable. Procedure revisions are host-addressed artifacts, not first-class callable runtime values in this v1.

3. **“Explicit named arguments” suggests keyword application.** Replace with “explicit parameters and positional arguments.” The examples show positional calls; no keyword-call mechanism is proposed. Specify lexical scope of `let`, parameter binding, arity checking and reserved primitive names in the next specification.

## Exact example improvements

- Mark walkthroughs as pseudocode until the grammar is frozen; `twice@1(x) = ...` is an illustrative definition notation, not yet accepted syntax. Its arithmetic is consistent: 3 → 6 and 3 → 12. Explicitly say the `twice@1` references in `four@1` are dependency bindings, not strings resolved at each invocation.
- Make the repair concrete: `first@2(xs) = (if (empty? xs) (list "absent") (list "present" (head xs)))`. Empty input produces `["absent"]`; `[7]` produces `["present", 7]` in illustrative result notation. This shows branch laziness, stable return tagging and revision identity. It requires the core's list constructor to include `list`, or the example must use the selected constructor spelling.
- Give checkpointing one actual data shape, e.g. `[remaining-input, accumulated-output]`, and identify a procedure that accepts and returns that shape. The current walkthrough is semantically plausible but lacks enough detail to expose ordering or duplication mistakes. A hand-worked two-chunk example suffices in specification; no need to invent a domain simulator.

## Decisions that can wait for specification or implementation

Choose integer width, Unicode index unit, complete error names, exact grammar, canonical serialization, cost table, pagination and stage expiry during specification. Measure numerical quotas and editing ergonomics during host work. These are legitimate open choices provided implementation does not silently choose incompatible semantics. Fix Unicode meaning before calling byte strings Unicode text; valid UTF-8 storage alone does not define character slicing.

Dependency publication should validate a bounded transitive graph, with self recursion bound locally to the current immutable revision and other calls pinned to existing revisions. Rebinding aliases cannot change those edges. Defer mutually recursive groups explicitly, as DESIGN.md already does. Define whether revisions can lose retained dependencies under deletion/compaction before offering those actions.

Omitting first-class closures, general `eval`, macros and mutual recursion is coherent. It narrows direct higher-order and metaprogramming conveniences; it does not invalidate ordinary arithmetic/text/list algorithms or explicit state transformation. Accordingly retain the existing language-family wording and avoid “minimal basis,” “full Scheme,” unbounded-universality, or model-usability claims. No source reviewed establishes that this exact kernel is sufficient for every desired domain or that the fixed 135M model can use it. Domain breadth remains a property to demonstrate through ordinary constructions, followed separately by model behavior.

**Recommendation:** resolve the three blocking wording conflicts now, then write one short grammar/type/dependency/effect contract with the concrete walkthroughs. Further broad research is not needed to begin that phase.
