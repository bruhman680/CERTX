# AS-C2: peripheral source weave from two screenshot leads

The user requested a broader sweep for indirectly related foundations. Three existing scouts were reassigned to control/fault diagnosis, decision-focused compression and collective learning. The coordinator checked the two screenshot papers. Eight primary sources were selected. This is a bounded exploratory weave, not a systematic review, novelty claim, paper reproduction or validation of FRR. [SOURCES.json](SOURCES.json) records versions, dates and reading depth.

## Screenshot leads: useful work, bounded claims

**[Terminal-RSI, 2610.22192v1](https://arxiv.org/html/2610.22192v1), October2026.** Root read methods, reward definitions and limitations. It alternates verified trajectory rewriting with actor–critic refinement and recalibrates inherited values. This is a finite five-stage training sequence on one27B backbone, not evidence of unbounded autonomous improvement. Compute-matched component controls and independent training seeds remain needed; stage settings change together. Verifiers cover only enforced requirements. Borrow the separation between partial progress and completed task acceptance, plus revalidation after a policy/reward change. These practices do not implement its training algorithm or establish its gains in our harness.

**[LittleBit, 2506.13771v5](https://arxiv.org/html/2506.13771v5), February2026 revision of2025 work.** Root read architecture, evaluation, latency and storage accounting. Sub-bit figures describe effective storage through low-rank binary factors and learned scales, not fractional storage of each independent original coefficient. Some components remain FP16; task fidelity degrades under extreme compression. The11.6× figure is an A100 GPU kernel result for a specified layer, not guaranteed end-to-end Mac/Ollama/LMStudio acceleration. Borrow task-dependent preservation tests; weight factorization does not itself validate semantic-summary compression. The screenshots were treated as search leads, not independent evidence.

Both papers connect to our work through questions about preserved behavior and evaluation, not by proving that model weights, context records and environmental memory share one mechanism.

## Peripheral lane1: active fault diagnosis

[Scott et al., Input design for guaranteed fault diagnosis using zonotopes](https://web.mit.edu/braatzgroup/input_design_for_guaranteed_fault_diagnosis_using_zonotopes.pdf), Automatica2014, selects inputs that separate possible output sets for listed faults, including process and sensor/actuator changes. Disturbance bounds, candidate coverage and feasible separating inputs are required. A large response is not enough: rival models must be unable to explain it under the stated uncertainty.

[Ni et al., Safe, Real-Time Active Model Discrimination and Fault Diagnosis for Nonlinear Systems via Differentiable Reachability, 2606.19590v1](https://arxiv.org/html/2606.19590v1), June2026, extends active discrimination using conservative reachable-output approximations for nonlinear systems. Process versus observation-map faults, model coverage and tractable inverse-set assumptions matter. Conservative overlap can leave diagnosis unresolved.

**Transfer:** put uncertainty envelopes around reset success, off-target effects, initial mixtures and readout distortion. Choose probes for worst-case separation among those probability envelopes. Preserve retained-state change, readout change, both and none-of-the-listed-models as possible outcomes. Deterministic output-set guarantees do not transfer directly to finite Bernoulli samples with overlapping support; statistical error control is still needed.

## Peripheral lane2: preserving decisions under compression

[van Rooyen & Williamson, Le Cam meets LeCun: Deficiency and Generic Feature Learning, 1402.4884v2](https://arxiv.org/html/1402.4884v2), February2014, connects information lost by feature extraction with attainable decision risk under bounded losses. A representation adequate for one decision loss can fail when costs change. Strong generic preservation requires low probability of reconstruction **error**, not merely a small average geometric distortion. These statements concern optimal decision rules; a fixed bounded reader might use a shorter representation better even though it contains less information.

[Wang et al., Task-Oriented Lossy Compression with Data, Perception, and Classification Constraints, 2405.04144v3](https://arxiv.org/html/2405.04144v3), January2025 revision, separates reconstruction, perceptual distribution and classification objectives. Their binary/scalar-Gaussian results and image experiments depend on which constraints are active and whether the source is degraded. Conditional entropy is not the same as one deployed classifier's error. Text and weight compression need their own mappings and tests.

**Transfer:** evaluate a task-and-loss matrix, including a rare exception that matters little to reconstruction but changes the correct action. Separate ideal attainable decision risk from what a fixed reader actually achieves. Change the task or error costs after compression to test whether a previously adequate summary remains adequate. Preserve a route to the original record when future tasks are unknown.

## Peripheral lane3: collective influence and evidence quality

[Almaatouq et al., When social influence promotes the wisdom of crowds, 2006.12471v3](https://arxiv.org/html/2006.12471v3), April2021 revision, studies weighted initially iid estimates and reanalyzes human estimation groups. Whether concentrated influence helps depends on the initial error distribution and chosen outcome metric. Communication edges do not directly reveal influence weights. Probability of beating an average need not rank systems like expected squared error or tail loss.

[Joseph et al., When Influence Misleads: Informational and Strategic Limits of Social Learning in Trading Networks, 2507.01817v2](https://arxiv.org/html/2507.01817v2), July2025, examines actual trade/copy provenance. Popularity and measured performance differ; adaptive copying associations are observational. Its selected data window is2013, so publication recency is not data recency. Simulated platform changes do not turn those associations into randomized causal effects.

**Transfer:** preserve pre-discussion answers, then vary popularity versus independently scored past-performance/freshness cues under matched evidence and communication budgets. Evaluate on new items and include changed-reliability cases. Measure answer movement, accuracy, correlated co-failure and tails separately. Do not generate a displayed quality cue from the same outcomes used to evaluate it, or infer that frequently copying a recent winner must help.

## What this changes in the next-contact designs

The immediate recommendation remains the different-parameterization/leaky-reset contact from [AS-C1](../arxiv-scout-v1/NEXT_CONTACTS_DRAFT.md). This weave strengthens its uncertainty treatment and fault/readout rivals rather than replacing it with a new grand theory.

[DESIGN_REFINEMENTS.md](DESIGN_REFINEMENTS.md) also preserves compression/loss-transfer and influence-quality controls as optional later contacts. No draft was launched or promoted to a completed experiment. Related queue families remain LEGACY-01, PID-01, ARCHIVE-01, MEM-04, LEGACY-06 and LEGACY-07; counts/statuses do not change.

A practical question unites the sweep: **what distinction must survive for the next useful decision, and does our measuring process actually observe it?** The papers answer different mathematical and empirical questions; this shared engineering question is not proof of one physical substrate law.

## Audit of this scout

The coordinator read both seed papers' primary methods/limits and cross-checked selected peripheral primary records. Six other method readings were delegated; SOURCES.json distinguishes those paths. No paper's code, training, hardware benchmark or human experiment was rerun. A scout sentence inverted “low probability of reconstruction error” into “low probability of exact reconstruction”; root checked the primary introduction and corrected the wording before this report. That was a source-summary repair, not a new paper result.

The screenshot files are retained locally, with hashes and nonpublication scope in SCREENSHOT_RECEIPT.json. Historical reports and earlier source weaves remain untouched. No model/provider API access, training or local quantization was started.
