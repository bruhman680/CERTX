# Three research cycles: foundations for a persistent computational world

5 November 2026, America/Chicago (host UTC advanced to 6 November during research). **Research, counterexample analysis and design review only. No new model runs, interpreter implementation, installations, training or activation.** Three authorized scouts plus root contributed. Their reports preserve initial proposals and subsequent disagreement; this report and [DESIGN.md](DESIGN.md) describe the resulting candidate.

## Main finding

We have enough foundation to write a precise first specification. More broad scouting is not the strongest next step. The intended garden is a computational medium: durable data and executable constructions under inspectable operational rules. It need not simulate plants, tools or rooms. The [previous world scout](../persistent-world-scout-v1/REPORT.md) remains useful for persistence and feedback patterns, but its physical workshop examples are not the intended world ontology.

Leading design: a small Lisp-like source language with explicit parameters, positional arguments, names, lists, text, conditions and recursive named procedures; an explicit deterministic evaluator underneath; versioned persistent artifacts; bounded computation; and optional seeds. This is a design preference, not a benchmark winner or evidence of 135M model competence. We can define operational rules precisely without predicting every possible construction or knowing the model's internal reasoning.

## Cycle 1 — foundations and source extraction

Three scouts examined complementary primary sources, with root reviewing observation/testing methods:

| Contact | What we extracted | What it does not establish |
|---|---|---|
| [R7RS-small Scheme](https://small.r7rs.org/attachment/r7rs.pdf), [Forth standard](https://forth-standard.org/standard/core), [Joy author tutorial](https://hypercubed.github.io/joy/html/j01tut.html), [SICP register machines](https://mitp-content-server.mit.edu/books/content/sectbyfn/books_pres_0/6515/sicp.zip/full-text/book/book-Z-H-31.html) | Composition, procedure naming, control, code/data distinctions, explicit machine state | A tiny syntax is not necessarily easy for the current model; our dialect would not be full Scheme/Forth |
| [Software Foundations evaluator](https://softwarefoundations.cis.upenn.edu/lf-current/ImpCEvalFun.html), [Wasmtime interruption](https://github.com/bytecodealliance/wasmtime/blob/main/docs/examples-interrupting-wasm.md) and [security](https://github.com/bytecodealliance/wasmtime/blob/main/docs/security.md), [SQLite transactions](https://www.sqlite.org/lang_transaction.html) | Bounded evaluation, authority boundaries, host work versus guest fuel, explicit durable effects | Depth fuel is not exact step count; a trap is not a durable rollback or resumable pause |
| [Papert/Harel](https://web.eecs.umich.edu/~mjguz/csl/home.cc.gatech.edu/allison/uploads/4/papert91.html), [Papert Logo notes](https://dailypapert.com/notes-on-the-future-of-logo/), [DreamCoder](https://arxiv.org/html/2006.08381), [Avida configuration](https://github.com/devosoft/avida/blob/master/avida-core/support/config/environment.cfg) | Constructible media, reusable abstractions, computational environments and explicit incentives | Human educational theory is not evidence of machine curiosity; library optimization/training/rewards are additional mechanisms |
| [Hypothesis stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html), [TLA+ tools](https://lamport.org/tla/tools.html) | Action-sequence tests, reference comparisons, invariants, small finite state models | Tests or bounded models do not automatically prove our future implementation correct |

Read depth and failed-access limitations are documented in [primitives](CYCLE1_PRIMITIVES.md), [execution](CYCLE1_EXECUTION.md), [construction](CYCLE1_CONSTRUCTION.md) and [observation](CYCLE1_OBSERVATION.md). Some historical author texts were available through mirrors/transcriptions; this was not an exhaustive computer-science survey or reproduction of published results. No model or dataset was downloaded. These sources support specific mechanisms, not FRR as a whole.

## Cycle 2 — cross-review and counterexamples

The scouts read one another's reports and challenged the proposals. The strongest counterexamples were:

- An unchanged saved program produces a different result after a helper's friendly name is rebound. **Response:** immutable revision identities and pinned dependency bindings; aliases are not program identity.
- A run reaches its limit after writing part of a result, or resumes against a changed world. **Response:** failed invocation publishes no partial artifact. A successfully completed chunk can explicitly publish algorithm progress for another call; that is different from saving a running VM.
- One concatenation or equality operation hides large allocation/work behind a single instruction. **Response:** account for input size and allocation, with separate bounds for parsing, rendering, hashing and storage.
- Logging failure itself exhausts storage, leaving no reliable receipt. **Response:** separate reserved audit capacity, admission checks and idempotent request IDs; stop visibly when full.
- An assembly-only world consumes the small model's output budget in bookkeeping. **Response:** separate the source interface from the implementation's machine transitions. Compact source is a hypothesis to test, not an established advantage.
- Continuing supplied seeds, rewards or selective pruning manufactures apparent self-directed growth. **Response:** disclose interventions, retain failures, make seeds optional and compare against no-seed/free-choice conditions.

See [primitive review](CYCLE2_PRIMITIVE_REVIEW.md), [execution review](CYCLE2_EXECUTION_REVIEW.md) and [agency review](CYCLE2_AGENCY_REVIEW.md). These are manually reasoned design counterexamples, not executed failures of a built system.

## Cycle 3 — integrated candidate and final challenge

Root drafted the candidate; each scout reviewed it. [Language review](CYCLE3_LANGUAGE_REVIEW.md), [execution review](CYCLE3_EXECUTION_REVIEW.md) and [agency review](CYCLE3_AGENCY_REVIEW.md) identified concrete inconsistencies. The final [design](DESIGN.md) incorporates these corrections:

1. Explicit positional arguments, not an accidentally implied keyword-argument mechanism. Runtime symbols/quotation are deferred rather than half specified.
2. `run` returns `COMPUTED` without a guest artifact; declared `run-and-publish` atomically publishes and returns `PUBLISHED`. Receipts remain distinct from artifacts. No unlimited result-staging cache.
3. Definition publication pins dependencies; invocation resolves aliases from a recorded snapshot; alias updates use expected prior revisions. First-class closures, dynamic eval and mutual-recursion groups are explicitly deferred.
4. Limits have separate scopes for actions, visits/experiments, values, procedures, dependency graphs, libraries and audit storage. Old artifacts are not silently pruned to accommodate a run.
5. Discoverable procedure signatures/source, explicit seed-free snapshots and successful checkpoint chunks preserve room for self-chosen construction.

The design includes three concrete **unexecuted pseudocode walkthroughs**: compose two doubling calls while preserving dependency versions; repair an empty-list failure with a guarded revision; and continue a two-chunk transformation across a pause. They check the design narrative, not interpreter correctness or model behavior. The reports do not constitute unanimous proof: choices about syntax, numeric representation, closure convenience and practical capacity remain empirical or specification decisions.

## What the proposed world permits

The model could build representations and algorithms using generic primitives rather than a menu of subjects. A computational seed might be a pattern, a flawed procedure, a relation, an incomplete construction or an open question. It can be ignored or reworked. A tool can emerge as an ordinary reusable procedure. Within-world learning algorithms could represent learned parameters as world data; that would still be separate from updating the deployed language model's weights. No such algorithm or behavior was implemented or observed here.

Effective freedom is not unlimited computation. The deployed machine is finite, and a run that exhausts its allowance is incomplete under that allowance—not proven divergent, wrong or uninteresting. The environment can expose reliable consequences while leaving project selection and constructions open. External scientific claims require suitable grounding beyond successful execution.

## Confidence and next strongest step

**High confidence:** separate a compositional authoring language, explicit evaluator, durable state and observations. Preserve source/dependency versions, make failures visible and distinguish execution from publication. These are supported engineering patterns.

**Moderate confidence:** a tiny Lisp-like surface is a reasonable first candidate. Stack languages remain legitimate alternatives. No tokenizer/corpus-familiarity study or interface comparison was performed; punctuation count alone cannot select the winner.

**Unknown:** whether this fixed 135M+LoRA model can construct useful procedures, pursue a project, repair after feedback or use a retained library under this interface. Prior arithmetic/control/context limitations remain relevant. More invitations or a richer substrate do not establish those abilities.

**Next:** write the operational specification: exact grammar/types and scope; numeric/text rules; publication/status and retry behavior; dependency/revision semantics; resource cost model and retention; observation/paging; and the complete example transcripts. Then build and host-test an isolated prototype, followed by short matched-budget model trials only after the host checks pass. Numerical limits should be measured and then held fixed within conditions. Another long primary block or a migration is not scheduled by this report.

## Preservation and history

The original continuing garden remains `discovery-play-patch-v1`, paused at entry **500**, number **0**, current verifier **0096**. No new model generation, primary entry, projection, verification pointer, policy or model/adapter change was made. [Primary preservation](PRIMARY_PRESERVATION.json) records a comparison of all **1,504 non-bytecode files**. Hash coverage starts with root's pre-record capture; scouts report no primary access before that capture. The earlier interrupted-session digest unknown remains unknown.

Previous navigation bytes are preserved in `before/`. Initial source proposals are retained as historical cycle records even where final design choices differ. This is three research/design cycles with explicit cross-review, not three model-development runs, a formal proof, or a completed computational environment.
