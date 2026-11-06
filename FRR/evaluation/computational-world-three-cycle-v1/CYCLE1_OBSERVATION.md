# Cycle 1: observation and verification foundations

5 November 2026. Root scout, primary-source reading only. This is a research/design contact; no simulator, model, training pipeline or test framework was installed or run.

## Sources inspected

- [Hypothesis stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html), introduction, rule/bundle example, preconditions and invariants. It generates action sequences with data dependencies, compares a real implementation with a simpler model, and can reduce a failing sequence to a short reproduction. **Transfer:** test combinations of create/define/run/inspect/save/reload, not only isolated functions. Check invariants after each transition. Tests exercise a declared sample space; passing samples do not establish universal correctness. No Hypothesis tests were executed here.
- [Lamport's TLA+ tools page](https://lamport.org/tla/tools.html), complete tools overview, dated March 2022. It distinguishes explicit-state model checking, symbolic bounded checking and mechanically checked proofs. **Transfer:** enumerate a tiny finite configuration of our state machine and assert scope/resource/commit invariants; keep the chosen bounds and assumptions in the result. Checking a specification does not automatically verify a separate interpreter implementation. No model checker was installed or invoked.

## Design implications

Keep four independent ledgers: (1) intended language semantics, (2) actual engine transitions and committed artifacts, (3) the model's observations and emitted actions, and (4) claims or interpretations. A prose claim of discovery, a completed evaluation and a verified general property belong in different categories.

An eventual host evaluation should compare an implementation with a simpler reference for small expressions, and generate action sequences that cross persistence boundaries. Useful invariants include exact reconstruction of committed state, immutable version IDs, no world mutation from inspection, no publish on failed transaction, controlled revision of names, and limits on every allocation path. Tests must include malformed syntax, recursive loops, oversized values, stale references, save/reload and duplicate requests. This is a proposed verification plan, not completed coverage.

For model evaluation, distinguish syntax-valid, executable, result-correct, corrected-after-feedback, reused-later and transferred-to-new-input. Include an optional-seed-free condition. Keep direct-command or menu assistance visible in attribution. A sophisticated engine cannot supply the small model's missing semantic ability.

## Known local constraint

The prior [padding/prediction diagnostics](../padding-and-prediction-v1/REPORT.md) provide a practical warning: the active 135M+LoRA configuration's integer-only formatting did not imply arithmetic or rule application. Its limited output allowance also argues for incremental artifact editing and short actions rather than one long program per reply. This is a design motivation, not evidence that a particular new syntax works.

Do not require a natural-language explanation before accepting an otherwise valid action. Explanations can be retained as optional hypotheses and checked against actual traces, without promoting them into causal accounts of the model's internal computation.
