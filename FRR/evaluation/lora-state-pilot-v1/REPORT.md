# LoRA resource fit, narrow-state pilot, and six scoped stations

30 October2026. User authorized the next directions plus assistants and research scouting. Three connected stages completed: validated lower-memory probe; fixed adapter pilot and paired audit; integration with a read-only station registry. The original model remains the default. No paid API, rental, package install or automatic promotion occurred.

## Outcome first

**The lower-memory setup completed all48planned updates. The intended semantic skill remains weak.** On48new structural-holdout cases, the zero-adapter baseline matched1/48 exact labels; the adapted branch matched19/48. Every constant-label predictor scores16/48. Adapted recall was positive13/16, zero6/16, missing0/16. This is a small descriptive gain above a constant baseline on one authored split, mostly accompanied by much better answer completion. It is not a reliable three-way classifier or a broad reasoning result.

The other direction also became usable: [station_registry.py](../../tools/station_registry.py) indexes byte-bound scoped receipts without computing pooled truth, votes or confidence. The [six-station registry receipt](REGISTRY_RECEIPT.json) preserves old and new outcomes separately and flags eight shared-hash relationships. It does not turn the two arms of one experiment into independent corroboration.

## What changed in training

Earlier [full-weight pilot](../narrow-training-pilot-v1/REPORT.md): one AdamW update before its memory-headroom stop, two examples, no missing-class update, all-NO adapted outputs. That partial checkpoint is preserved. This new experiment uses fresh rank4/alpha8/dropout0 LoRA adapters on q_proj and v_proj across all30layers of the pinned SmolLM2-135M-Instruct model.

For each wrapped matrix:

    output = W_base*x + (alpha/rank) * B*A*x

The base is frozen. A starts random and B starts zero, so the initial adapter product is zero. The optimizer receives only120adapter tensors containing230400scalars, rather than all134515008base parameters. There are60wrapped projections. This reduces trainable parameter and optimizer-state demand; it does not remove the resident base model, its forward compute or all training activations.

An implementation assistant built [lora_cpu.py](lora_cpu.py) and [five synthetic/architecture checks](test_lora_cpu.py). Coordinator reviewed and used the code. A separate scout read primary papers; an implementation contributor performed a [read-only runtime/accounting review](RUNTIME_REVIEW.md). These roles do not constitute independent experimental replication or independent gold review.

## Resource probe before the pilot

[PROBE_FREEZE.json](PROBE_FREEZE.json) bound data, primary keys, protocol and probe implementation before the probe update. The first real-model balanced update used one example per class with microbatch1 and accumulation3. Measured time2.616seconds; largest sampled working estimate2844262400bytes. Probe checked:

- Zero-product adapters preserve a diagnostic base forward exactly.
- The frozen-base numerical digest remains unchanged through the update.
- Actual optimizer allocation is included in phase measurements.
- The resource/finite checks meet the declared eligibility rule.

The probe adapter and optimizer are preserved separately at `/workspace/lora_resource_probe_v1`. The main pilot did not warm-start from them. The probe tokenized evaluation sources only for length, with no model forward or gold-label parsing. Maximum training length196tokens fit the declared256token bound; no truncation was performed.

The eligibility thresholds were less than8seconds per effective probe update and sampled working estimate below60%of8GiB. Working estimate is cgroup current minus inactive_file, an approximation that discounts some reclaimable file cache. It is not the account's free-compute balance, an exact physical-memory measure, or a guarantee against transient peaks.

## Frozen task, class balance and fresh test

The [plan](PLAN.md), data, runner, scorer, probe result and tool dependencies were fixed in [FREEZE.json](FREEZE.json) before main-pilot generation/update. Task: for a named batch, classify its explicitly recorded sampled-soil count as positive (YES), zero (NO), or unavailable (WITHHOLD). `null`, `unavailable`, `not recorded` are explicitly defined missing markers. Other batches/fields cannot supply the target count. WITHHOLD is source missingness, not epistemic confidence rejection; UNRESOLVED is the separate scoring category for unsupported output.

Data:72training records (24perclass),12familiar-structure development cases (4perclass),48new structural-holdout test cases (16perclass). Training formats are fields, prose, flat JSON and table; test formats are scoped row tables, nested record lists, register notation and interleaved clauses. Scope selection and distracting batch/field counts appear in training; the entire four test structures are withheld. Names/positive values differ by split. Every record has irrelevant zero and missing fields. Source strings are disjoint across splits and the new test is not the previously exposed48-case test. [Data checks](DATA_CHECKS.json) record these constraints.

Keys are coordinator-authored using typed state generation, not independently reviewed real-world labels. This is one synthetic diagnostic split, not a deployment population or proof of every kind of composition. Case IDs contain state names for bookkeeping but are never placed in model prompts; [artifact checks](ARTIFACT_CHECKS.json) verify exact rendered prompts and token sequences.

## Actual schedule and preservation

Runtime: local CPUfloat32/eager,2threads; no remote code/network/model API. Base: HuggingFaceTB/SmolLM2-135M-Instruct revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`. Fresh main initialization seed73103, rank4,alpha8,dropout0, AdamWlr0.001,weightdecay0.01,gradientclip1. These are fixed exploratory choices, not literature-certified optima.

Each effective update accumulates three sequence-normalized supervised losses, one perclass, then clips and steps once. Each group is counterbalanced by class; group order is shuffled with a fixed seed and class order rotates. Forty-eight updates cover two passes through72examples,48completed exposures perclass. Prompt tokens/padding are not supervised; only assistant target label plus EOS. [Training log](TRAINING_LOG.jsonl) records every completed update and its memory phases.

Actual training-loop time164.091seconds; no time/memory stop. First/last average target-token losses2.7292/0.3602. Different batches were used, so this endpoint comparison is not a controlled monotonic learning curve. The sampled maximum working estimate was3517308928bytes and sampled maximum process RSS1488506880bytes. Measurements do not continuously bound between-phase memory. The300second cap is checked between updates and excludes generation, checkpoint writes and digest work.

Saved adapter file:934144bytes; optimizer state:1942978bytes. The final adapter/optimizer are separate at `/workspace/lora_state_checkpoint_v1`; initial adapters at `/workspace/lora_state_initial_v1`; hashes in [TRAINING_MANIFEST.json](TRAINING_MANIFEST.json). All120adapter tensors changed numerically; all frozen-base parameter bytes retain the same runtime numerical digest. The original disk files and prior partial checkpoint are unchanged. A fresh base plus reloaded adapter reproduces a diagnostic next-token logit vector exactly. These are state/preservation checks, not proof that unrelated behavior is unchanged while adapters are active.

Known runtime bounds from contributor review: a narrow race at the helper's initial guard can replace an inner triggering reading with a later exception reading; no such stop occurred here. Checkpointing/evaluation do not share the training loop's guard. Nonfinite post-step adapters could abort saving rather than yield a clean stop manifest. These remain implementation limitations; the frozen run was not silently edited to hide them.

## Evaluation: completion improved; missingness did not

Fresh contexts, greedy8token cap, no retries/continuations or output-dependent prompt changes. Original development was evaluated before training. Final development and both test arms were forwarded only after training/checkpoint creation. Original means the fresh base plus zero-product adapters; the probe verified exact diagnostic equality to the unwrapped base. One original diagnostic is not an independent model implementation.

| Arm | Exact matches | Output labels | EOS / cap |
|---|---:|---|---:|
| Original dev |0/12 |12UNRESOLVED |0 /12|
| Adapted dev |5/12 |7YES,5NO |12 /0|
| Original test |1/48 |1YES,47UNRESOLVED |1 /47|
| Adapted test |19/48 |34YES,14NO |48 /0|

Adapted test class recalls: YES13/16,NO6/16,WITHHOLD0/16. By structural family: interleaved4/12; nested-list, register and scoped-table each5/12. Paired changes:18adapted-only matches,1both match,29neither,0original-only. The new branch no longer outputs one constant label, but its39.6%exact-label score is only3cases above the33.3%constant baseline. No seed uncertainty or population effect is estimated. [SUMMARY.json](SUMMARY.json) retains the full confusion matrices and paired cases.

The baseline's47capped test responses are unresolved under this exact-label interface, not proven semantic errors in the unfinished explanations. The adapted branch's completion improvement therefore contributes strongly to the raw score difference. It would be misleading to headline a19-fold reasoning gain. No calibration, reliable missingness handling, general FRR benefit, unrelated-task retention or deployment readiness is established. Earlier failed source-reading gates remain failed and model answers do not authorize verifier inputs.

There were120actual generations:23050inputtokens,635generatedtokens includingEOS. All120newterminal caches are retained under `/workspace/smollm_lora_state_states_v1`,1086462720bytes total. [Artifact checks](ARTIFACT_CHECKS.json) verify tokenization/decoded outputs and cache byte/shape/prefix bindings, all500prior recorded files unchanged, probe/initial/final checkpoint hashes, equal class exposure, unchanged base numerical digest and frozen inputs/raw results. Local model/cache binaries are not pushed as Git blobs; workspace retention is not an independent archive guarantee.

## Emerging upstream question: what does the loss reward?

A post-result [objective note](LOSS_OBJECTIVE_NOTE.md) identifies a concrete candidate for the next controlled experiment. The pinned tokenizer encodes YES in2tokens, NO in1, WITHHOLD in4. IncludingEOS, target lengths are3,2,5. The implemented equal-sequence objective gives each example equal total weight, but gives the first decision-token CE term coefficients1/9,1/6,1/15 respectively in a three-example update. Equal class exposure therefore does not imply equal weight on the first generated decision. Later suffix/EOS prediction under teacher forcing can reduce average loss without fixing that first decision.

This algebra is exact; its causal explanation of the missing-class failure is **untested**. Source parsing, representation, hyperparameters and insufficient optimization remain alternatives. All complete labels fit the8token cap. No posthoc rescoring or label substitution is applied.

Strong next controlled direction: a one-token class-interface/label-mapping control with counterbalanced mappings and new primary cases. Keep ordinary generation, forced-choice diagnostics and semantic source-state claims distinct. The current48cases are now regression material, not a fresh test for future tuning.

## Read-only station registry: a usable second direction

The [standalone registry contact](../station-registry-v1/REPORT.md) built an optional read-only CLI over four earlier stations. Coordinator review found two shape-validation edges: Boolean/float label counts could compare equal to integers, and source field state tags could be swapped. The first code/results were byte-archived under [before_review](../station-registry-v1/before_review/ARCHIVE.json); revised code and tests were frozen before rerun. Fourteen challenge tests pass, including those regressions. Coordinator replay uses the same authored tests; it is not14additional independent experiments.

The integrated [six-station manifest](REGISTRY_MANIFEST.json) keeps those four entries and appends original/adapted LoRA test receipts. [Registry checks](REGISTRY_CHECKS.json) confirm six indexed stations and eight shared-hash warnings. The paired arms share sources/keys/training summaries and are not independent corroboration. Distinct arm key hashes and full reported receipts remain visible. [Registry freeze](REGISTRY_FREEZE.json) binds all inputs/tool before the first six-station execution.

The registry preserves caller question, recipe, state, receipt bytes and declared ancestry. It supports only narrow computed receipt schemas; unsupported/withheld shapes remain unresolved rather than being guessed. It does not rerun underlying audits, authenticate source truth or causal ancestry, pool scores, vote, calculate universalconfidence, or infer contradiction from unlike questions. Absence of a shared hash does not establish independence.

## Research weave and next confidences

The [primary-paper scout](RESEARCH_SCOUT.md) read bounded portions of [LoRA Learns Less and Forgets Less](https://arxiv.org/abs/2405.09673), [Fine-Tuning Pretrained Language Models: Weight Initializations, Data Orders, and Early Stopping](https://arxiv.org/abs/2002.06305), and [BitFit](https://arxiv.org/abs/2106.10199). Read depths/transfer limits are explicit. Useful lessons: separate resource fit, semantic acquisition and retention; log configuration and per-completed-update exposure; parameter location and data order matter. Findings in larger/different models are not135MCPU guarantees. BitFit is lateral context, not implemented here.

High confidence within this run: this LoRA configuration fits the chosen sampled-memory guard and completes48balanced updates; original/frozen-base state is preserved; the read-only registry works on six scoped receipts. Lower confidence: the adapted branch has limited source-state discrimination beyond output-format change on this one split. Clear unresolved gap: missing-class generation0/16 despite48training exposures. No universal reasoning or physical-pressure law is tested.

The next largest useful move is a controlled objective/readout experiment, while the registry keeps failures and scopes visible. No additional training sweep, model promotion, irreversible history rewrite, paid resource or background task was started after these results.
