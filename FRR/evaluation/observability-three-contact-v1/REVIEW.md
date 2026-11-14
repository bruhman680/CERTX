# Independent review of the three observability contacts

Plan dated13 November2026, America/Chicago. Retrospective source, tokenizer, provenance and retained-artifact review. No model weights were loaded, no inference or world operation was repeated, and no canonical garden file was changed by this reviewer.

## Audit result and scope

`audit.py` completed with **PASS** in `AUDIT.json`. It verifies twelve declared cases and fifteen actual generations: three retrieval cases with two turns each, three one-turn observation cases, and six one-turn sampling cases. The additional profile is one teacher-forced forward pass, not another generated trajectory. The main garden remains paused at1580 and its823-file non-cache inventory matches the retained pre-contact inventory.

All actual inputs are reconstructed solely from the declared job messages and, for the three retrieval followups, the preceding actual assistant reply and projected receipt. Exact tokenizer IDs, raw decoding, input/output counts and hashes, stop rules, parsed fences, batch copies, operation/event copies, world before/after links, receipt projection and aggregate result rows agree. Every case world is cleanly paused, without pending operations or locks, and its read-only store verifier passes. No job world lies outside the detached study path.

The worker and shared source hashes still equal WORKER_PLAN.json. The recorded body uses the same cached135M model, CPU float32/eager mode, two threads, fresh KV and256-token upper output bound. The worker is a separately pinned implementation of those greedy mechanics with an added declared nucleus option; it is not a literal call to the original generation.py function. Weight preservation is the worker's successful parameter-digest assertion, not an independently repeated weight load.

This audit establishes record consistency and protocol provenance. It does not independently recompute the probability profile, rerun inference, trace every syscall, establish power-loss durability or prove any internal reasoning mechanism.

## Hidden-file and supplied-read controls

The two hidden conditions have exactly identical first messages and tokenizer IDs. Neither expected value appears anywhere in those prompt messages. Their pre-inference supported filesystem snapshots differ only at probe_value.json, whose decoded JSON values match the two declared targets. The expected-value fields in job metadata remain outside the model messages: worker.generate renders only its messages argument. Case labels, metadata, host file paths and expected answers are not interpolated into the model input. All next-turn inputs contain only the actual preceding reply and receipt, so any later exposure of a value would have to appear through those retained consequences.

The supplied-read condition has the same supported filesystem as hiddenA. Its added receipt exactly matches an operator-originated read event: the read exits0, prints the value and changes no supported path. The actor is explicitly marked operator. That supplies information to the prompt; it is not model-chosen retrieval and changes input length/content as well as information availability.

The hiddenA/B generated token sequences match on both turns. The executed cells call json.loads on the literal filename string rather than opening the target file. Their JSONDecodeError is caught, so the process prints an invalid-JSON message and None while exiting0. This is not evidence that the valid fixture file is unreadable or malformed. The source and actual operator read show otherwise. The second-turn description changes value to boundary, but the same unperformed file access remains. That visible correspondence to receipt vocabulary does not itself establish an internal causal explanation.

The supplied-read case produces unfinished network-program writing on both turns, no executable cell and no target value in its output. These six selected responses show no successful exact retrieval or use of the supplied value. They do not establish general incapacity under other contexts, prompts, models or horizons.

A complete fence, a zero process exit, a filename mention, an answer copied from a supplied receipt, actual target-dependent file access and task success are separate observations. The companion retrieval report correctly separates them. A static call inventory is an aid to reading these known sources, not universal dynamic I/O instrumentation.

## Factual observations and control framing

The before and after eight-pair base messages are exactly identical despite different external entry IDs. Each observation replaces only the last empty user receipt with an explicitly operator-authored observation object. The label-only and before-value cases use the same supported world; the label carries an empty object. Supplied notebook-byte and archive-record counts match metadata measured from each prepared snapshot. The common diagnostic rules appendix does not change those measured fields.

The three complete input token sequences differ. All three output token sequences are nevertheless exactly identical to the retained old unfinished program. This is output invariance across these particular observation changes, not an exact-input fixed point in this experiment. Literal unchanged input is sufficient for the previous conditional argument, but it is not necessary for a repeated greedy output.

The before and after factual prompts have equal token counts, which removes a gross length difference for that pair. They still change two numeric fields and use two points on one physical lineage, so no single-field semantic effect or independent environmental replication is isolated. Label-only versus factual input also differs in length and content. There is one deterministic call per prompt, and free writing has no count-dependent correct action specified. An unchanged output therefore does not by itself show failure of a task, absence of perception, an unchanged internal representation or insensitivity to every possible observation.

The old empty-observation greedy result is retained earlier evidence, not a new independent baseline generation. No observation transport is adopted into the main garden by this contact.

## Decoder comparison and probability-path profile

The six sampling cases share exactly the same initial messages and token IDs. They cross the three declared seeds27401–27403 with top-p0.9/1.0 while holding temperature0.8 fixed. The generator is reinitialized per case. Paired seed integers do not guarantee distinct replies or create six independent worlds of evidence; early EOS can also shorten the number of subsequent draws.

The implementation sorts temperature-scaled logits, applies conventional shifted nucleus removal for p<1, retains the threshold-crossing token, renormalizes and samples with the explicit CPU generator. At p1 it omits that cutoff. There is no hidden minimum length, repetition penalty, forced fence closure, added novelty instruction or output repair. The audit finds one exact output sequence among the three p0.9 cases and three distinct sequences among the p1 cases. None contains a complete executable cell. Variation is observed; improved action, correctness or reasoning is not.

The teacher-forced profile is correctly aligned: prompt IDs plus the saved target prefix except its last token produce256 final logits, each predicting the corresponding saved output token. It reports all256 argmax matches to that reference,255 singleton p0.9 supports and one two-choice support. The counts and probability ranges are internally consistent in the retained artifact. I did not repeat the numerical forward pass.

This profile concerns one saved greedy path. It uses a parallel prefill, whereas sampling uses incremental cache steps; normalization/reduction ordering also differs slightly because the profile softmaxes before sorting while the sampler sorts before softmax. Near-threshold floating-point decisions may differ. The result does not describe every alternative sampled prefix, full entropy, or universal sampler determinism. It supports a narrow explanation of the limited opportunity for variation along this particular path, with the stated numerical qualification.

## Diagnostic transport and preservation

Each copied world explicitly declares that it is a diagnostic fixture. It begins from a selected eight-pair view with an operator observation/task where specified, and permits at most one actual followup. The second retrieval input therefore grows by one real pair; this laboratory transport is not the live bounded-view runner's per-turn reselection policy. Its world-side history-copy files are source fixtures and are not automatically extended by these tests. The declaration prevents confusing their unchanged index with a silently failed synchronizer.

All complete generated cells execute unchanged through the existing sandbox. Their actual receipts are retained without a task-success gate or semantic repair. The main world, source condition and separate prototype histories remain untouched. The worker refuses prior completion artifacts and leaves pending evidence if interrupted, but it is not a general crash-safe experiment-resume service. No such interruption occurred in the completed run.

The strongest supported synthesis is a separation of evidence layers: exact input availability, output variation, valid execution, intended file access, use of a delivered value and useful action. These contacts expose where those layers diverged in this chosen setup. They do not by themselves justify a new live policy, a global capability ranking, a claim of maturation or an internal-state narrative.
