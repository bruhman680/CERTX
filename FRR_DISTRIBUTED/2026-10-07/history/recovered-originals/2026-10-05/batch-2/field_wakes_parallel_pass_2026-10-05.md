# Field persistence: parallel exploration pass

5 October 2026 · FRR working note · Thomas's agent–field seed and Gemini's optimizer/context extension

## The relationship that survived

An action can change what a later action encounters. The strongest common form is a feedback loop: a focal system acts on an accessible field; the changed field affects later choices. What counts as the field and what can reset it differ by substrate. This form alone establishes neither a universal critical parameter nor permanent law.

| Domain | Persistent carrier | Read path | Useful reset or control | What the present evidence supports |
| --- | --- | --- | --- | --- |
| Two-route toy | Two route potentials | Softmax choice from their difference | Reset the route potentials while leaving choice rule intact | Mean-field preference threshold; stochastic routes remain accessible |
| Training optimizer | Parameter weights **and separately** moment estimates | Gradient update conditioned on weights, first and second moments | Reset moments while keeping weights, or restore weights while keeping moments | Proposed controller is currently unsafe on a simple gradient sequence |
| Autoregressive inference | Token prefix, represented computationally by cached keys/values | Model computes next-token logits from accessible prefix | Compare same prefix with cache on/off; edit or remove tokens separately | Context affects future logits; cache alone adds no new behavior |
| Physical erosion | Bed and material geometry | Flow responds to bed and boundary conditions | Prepare the same flow on altered and unaltered beds | Mechanism is plausible but not established by the graph or optimizer equations |

The boundary of the focal system matters. Momentum can be called external memory only relative to a focal parameter coordinate that excludes optimizer state. KV cache is a reusable encoding of context, not an independently written field with its own decay law. A bed alteration is material persistence. These differences are the substance of a cross-domain comparison.

## A real but local threshold

For a deliberately small two-route model, let route potentials be `E1,E2`. Each step chooses route 1 with probability `σ(β(E1-E2))`, decays both potentials by `γ`, and deposits `w` on the chosen route. In the deterministic expectation map for `z=E1-E2`,

`z_next = γ z + w tanh(β z / 2)`.

The derivative at the symmetric fixed difference `z=0` is `γ+wβ/2`. Thus that **mean-field map** changes local stability when `γ_c=1-wβ/2`, provided the parameter range permits it. This is a constructed model-specific result; it does not validate the earlier edge-degree/Laplacian formula. At `β=2,w=0.2`, its value is `0.8`.

One reproducible seeded 200,000-choice run per setting gave:

| γ | Mean-field positive fixed difference | Stochastic field-sign switches | Route choices |
| ---: | ---: | ---: | ---: |
| 0.7 | 0 | 37,503 | 100,129 / 99,871 |
| 0.8 | 0 | 16,637 | 99,736 / 100,264 |
| 0.9 | 1.915 | 31 | 60,130 / 139,870 |

These counts diagnose one finite seeded run, not an estimated phase diagram. For `γ<1`, the field difference is bounded by `w/(1-γ)` after starting at zero. With finite `β`, the disfavored route's conditional probability stays at least `σ(-βw/(1-γ))`, approximately `0.01799` at `γ=0.9`. The rare route remains possible. The stable nonzero branches of an expectation map and the long residence of stochastic paths are different statements. A literal permanent barrier requires a different update, an absorbing rule, or a declared limiting operation. Run `python graph_two_route_probe.py` to reproduce.

## The proposed optimizer fails before a training benchmark

Gemini's `GammaCAdam` computes bias-corrected first and second moments `m̂,v̂` with `β1=0.9, β2=0.999` and proposes `S=m̂²/(v̂+eps)` as a bounded alignment/crystallization score. The different averaging times break the asserted range. Exact scalar reproduction with 10,000 zero gradients followed by one gradient of 1 gives `S=9.99945`. With the proposed default control functions, `η≈0.00025608`, `λ≈1,782,856`, and the claimed retention factor `1-ηλ≈-455.555`. Applied to a nonzero weight, the “decay” flips and amplifies its sign. The parameter need not encounter such a sequence in typical training for this to refute a universal safety guarantee.

Two other controlled sequences locate the measurement problem: a constant gradient yields `S≈1` even for a linear objective with zero curvature; alternating `+1,-1` gives `S≈0.00277` although the update direction oscillates. A first-step gradient of 1 at weight 1 can arise from shifted quadratics with curvature 1, 10, 1000, or 1,000,000. The proposed `sqrt(v̂)/|W|` has almost the same value for every one. It therefore cannot certify the Hessian bound used in the write-up. The plain gradient descent condition `η<2/λmax(H)` is not by itself a theorem for Adam's preconditioned, state-dependent recurrence.

There is also a code-level obstruction: the shown `p.addcdiv_(m_hat, denom, value=-adaptive_lr)` supplies a tensor-valued `adaptive_lr`, while PyTorch documents `value` as a scalar Number. The tensor update could instead be formed elementwise after limiting `S` and enforcing an admissible decay product. We checked the recurrence with standard Python, not with PyTorch, which was unavailable locally; the API issue follows from documentation. The diffusion proposal writes `(1-α)g+α(g*K)` with `K=I+αΔ`, which equals `g+α²Δg`; the implementation instead rolls one tensor axis with wraparound. Neighboring channel indices need not be neighboring functions, since hidden units may be permuted without changing model behavior.

This rejects the stated guarantee and the supplied code, not every alignment-based optimizer. A repair candidate must at minimum define the bounded signal, constrain `0≤ηλ<1`, choose a meaningful coupling geometry, and separate first/second moments from parameter shrinkage. Then compare matched-budget AdamW, alignment-controlled learning rate only, decay only, both, diffusion, and a randomized-signal control. Measure stability, training loss, held-out behavior, curvature proxies that actually test curvature, and sensitivity to a function-preserving neuron permutation. Run `python gamma_c_optimizer_audit.py` for the counterexamples.

## Context conditions the next token, but it has two different softmaxes

At fixed model weights and prefix, internal attention uses query/key scores (scaled by key dimension and masks), while a sampling temperature rescales **output vocabulary logits after the model computation**. Raising sampling temperature does not make the attention distribution uniform at that same prefix. A KV cache reuses keys and values computed for prefix tokens. For the same intact prefix and positional handling, cache enabled versus full recomputation should produce effectively the same raw logits within numerical tolerances. Context eviction changes which prefix information is available; it is not multiplication by one scalar `γ` at every step. High attention on an initial token, including an attention sink, does not establish an absorbing repetition loop.

A compact discriminating experiment uses one frozen model: keep the generated prefix fixed, edit or remove an earlier pattern while controlling length/position, compare low and high sampling temperatures, record raw logits and attention **before** sampling, and separately sample continuations over seeds. Repeat cache enabled and disabled. Context edit effects on raw logits that survive cache toggling support a context-conditioned wake; changes only in sampling outcomes as temperature varies locate the effect in decoding. This has not yet been run on a model in this pass.

## A common test, then a translation boundary

For each domain define a focal state `x`, accessible carrier `e`, read rule `R`, write rule `U`, and declared observation `Y` over horizon `H`. Compare these controlled cases:

1. Same focal reset, retain the altered carrier.
2. Same focal reset, restore the original carrier.
3. Same carrier, disable or replace its read path.
4. Same visible outcome, vary the action that wrote the carrier.

If case 1 differs from 2, environmental persistence is implicated relative to the chosen boundary. If case 3 removes the effect, the read path matters. These comparisons locate a possible wake; they do not automatically establish a unique mechanism or a law. Define an **effective constraint** with an escape probability, horizon, intervention family, and tolerance. Reserve “invariant” for a property proven to survive the claimed operations and horizons. The two-route result itself shows why a very small escape probability cannot be silently replaced by zero.

The HPGM synthetic lineage snippet fits the same evidence rule: its phase alphabet, transition generator, history length, JS threshold, and evaluator were supplied before `nd=13`, `ncs≈5–6`, and related outputs were obtained. Those outputs can check execution and sensitivity of the chosen construction; independent support for the prior phase ontology requires observations or tests built without inheriting it.

## Literature contact and claim lineage

- Grassé's [1959 stigmergy paper](https://doi.org/10.1007/BF02223791) and Dorigo's [Ant System research lineage](https://iridia.ulb.ac.be/~mdorigo/ACO/publications.html) are established relatives of action-modified environments guiding later behavior. They do not imply the same mechanism in neural weights or token context.
- [Adam](https://arxiv.org/abs/1412.6980) already uses first and second moment estimates; [AdamW](https://arxiv.org/abs/1711.05101) treats weight decay as a separate update. [AdaBelief](https://proceedings.neurips.cc/paper/2020/hash/d9d4f495e875a2e075a1a4a6e1b9770f-Abstract.html) is a neighboring functional attempt to adjust step sizes from gradient agreement. These are comparison targets, not evidence for GammaC-Adam's guarantees.
- [Neural network permutation symmetry](https://proceedings.mlr.press/v139/simsek21a.html) makes raw tensor-index adjacency an assumption to test, while [PyTorch's `addcdiv` documentation](https://docs.pytorch.org/docs/stable/generated/torch.addcdiv.html) constrains the proposed implementation. [SAM](https://research.google/pubs/sharpness-aware-minimization-for-efficiently-improving-generalization/) explicitly optimizes for neighborhood loss, a different mechanism from scaling weight decay by `S`.
- The original [Transformer paper](https://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf), the [KV cache guide](https://huggingface.co/docs/transformers/main/cache_explanation), and [generation controls](https://huggingface.co/docs/transformers/main_classes/text_generation) separate internal attention, cached computation, and output decoding. [Streaming attention sinks](https://arxiv.org/abs/2309.17453) and [text degeneration](https://arxiv.org/abs/1904.09751) are different phenomena that should not be identified through a single peak attention weight.

## What remains open in this inquiry

The feedback pattern survives as a generative relational structure. The graph's mean-field threshold is a bounded model result. Optimizer performance and context intervention effects are untested here. No shared critical `γ_c`, universal “law from wake” transition, or measured generalization gain has been established. The next pass should use the same carrier/reset/read/write questions across domains while giving each domain its own dynamics and evidence.
