# Counterbalanced curriculum and wider pressure sweep

30 October2026 America/Chicago. User requested the strongest next curriculum step and asked whether other areas need attention. One fresh candidate completed48updates; a fixed prior control was reused. Main evaluation252generations, followed by a separately declared12seen-source diagnostic. No model/default promotion, paid API/rental or package install. Original model and prior branches remain intact.

## Result and interpretation

The curriculum changed the answer preference, without demonstrating the intended selection skill.

| Cohort | Original | Reused control | New candidate |
|---|---:|---:|---:|
| Familiar-format dev |0/12|4/12,allYES|4/12,allNO|
| Primary |0/72|24/72,allYES|24/72,allNO|
| Discordant primary cases |0/48|16/48|16/48|
| Fully correct discordant header pairs |0/24|0/24|0/24|

Constant-label baseline is24/72; always reading the first/last sampled-soils field scores48/72. Both trained branches finish atEOS, while the original baseline produces84unfinished capped responses. Completion/formatting and semantic correctness therefore remain distinct. Every trained missing primary case is wrong (0/24); the candidate gets only the24zero cases correct and the control only the24positive cases. No header-pair label switches occur. [SUMMARY.json](SUMMARY.json) retains all class/family/role/position breakdowns and paired comparisons.

After these results, a small [posthoc acquisition check](ACQUISITION_PLAN.md) was frozen before its forwards: first balanced training triple from each of four formats,12exactly seen sources. The same final candidate, with zero additional updates, returnsNO12times and scores4/12. [ACQUISITION_SUMMARY.json](ACQUISITION_SUMMARY.json) records that slice separately. This does not assess all144training examples or replace held-out results, but it prevents us from calling the observed failure purely a transfer problem: acquisition on these checked seen sources is not demonstrated.

## The curriculum package

[Fixtures](fixtures/README.md) contain144unique training records arranged as48balanced triples: four formats×three target states×three distractor states×two target identities×two target positions. Both named batches have full records. Training namesBirch/Cedar, positive count11; irrelevant observations5,damagedplots0,inspectionsunavailable for both. Other/distractor state is independent of target state, identity and order. No literal target/other role term in record bodies; the header selects the named batch.

The72primary sources use held-out XML/bullet formats, training-unseen namesHazel/Larch, positive13; these names are not globally unseen in the research history. There are36fixed ordered fact bodies, each asked with both target headers. Body bytes are identical within a pair; only the header changes. Twenty-four pairs have different record states (48cases),12have the same state (24cases). All three labels occur24times. Familiar-format development12 uses positive17 and is secondary, not checkpoint-selection data.

A [separate-agent review](DATA_REVIEW.md) parsed every228source body, checked all metadata/keys/factorial cells and exact header pairs before training. The generator author also ran separate parsers/checks. These are source-consistency reviews of coordinator-requested synthetic data, not independent real-world ground-truth collection or experimental replication. The original dated review is preserved alongside a client/UTC-context copy.

This is a whole training-support package: full-record wording/formats, unique examples and role support change together. It is **not** a pure position-only causal intervention. Paired cases share repeated facts/templates; no independent population-sampling claim is made.

## Reference policies and scope of the pairs

For the fully crossed72cases, a constant class scores24; always choosing the first field, last field or one fixed named record scores48. Those header-blind policies score0/24fullycorrect discordant pairs, since each fixed fact body asks for two different labels. On the48discordant individual cases, first/last/fixed-record score24; constant scores16.

A post-design metadata enumeration of the nine static header-identity label policies adds an important limit: such policies still score24/72 and can accidentally get4/24discordant pairs fully correct. [HEADER_ONLY_REFERENCE_CHECKS.json](HEADER_ONLY_REFERENCE_CHECKS.json) explicitly records this analysis as after design/model start, before structured scoring, not a preregistered metric change. Thus even a few correct pairs would not alone prove reading the facts. The observed trained result is0correct discordant pairs, so no such positive claim is warranted. Different labels after a header change and correctly grounded labels are separately measured.

## Matched budget, reused control and execution

Control is the immutable prior sequence_mean adapter from [decision-loss comparison](../decision-loss-comparison-v1/REPORT.md), trained on72unique sources twice. It was not retrained or counted as a second training replicate. Its actual checkpoint/base pin/initial tensors were hash-checked. Candidate uses144unique sources once. Both have144supervised example presentations,48effective updates,48exposures perclass, identical initial adapter tensors and frozen base numerical digest. Data order differs with the package; no pure position/one-factor effect is inferred.

Both use the pinned HuggingFaceTB/SmolLM2-135M-Instruct revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, rank4/alpha8/dropout0q/vLoRA,230400trainable parameters, sequence-mean assistant-label+EOS loss, seed73103, AdamWlr0.001/weightdecay0.01,clip1,microbatch1accumulation3. Original base is frozen. The output labels stay YES/NO/WITHHOLD; no alias experiment occurred.

Static tokenization was consumed before model launch: maximum training213tokens, evaluation input271; no truncation. The separate resource preflight selects the LONGEST balanced training triple rather than an easy first row. It makes one update, saves separately and supplies no warm-start. Main candidate completes48updates in163.788seconds. Sampled maximum working estimate3619184640bytes and processRSS1259470848bytes; these phase samples are not continuously monitored peaks or account billing evidence. The300second training cap and memory guards did not trigger. [RESOURCE_SUMMARY.json](RESOURCE_SUMMARY.json) retains costs.

[Ten synthetic runtime checks](UNIT_TESTS.stderr) cover objective/gradient/masking/order/resource-stop accounting. Data, code, scorer, prior bindings and protocol were [frozen](FREEZE.json) before main update/evaluation. The candidate checkpoint was saved before any newprimary forward. All generations are fresh-context, greedy8token-cap; each correct complete label can fit within that cap. Gold metadata/IDs carry answers, but prompts contain only the unchanged guidance and source. [Artifact checks](ARTIFACT_CHECKS.json) verify rendered prompts/tokenization/decodes and source selection. No output-dependent retry, optimizer sweep or checkpoint selection occurred. Selected completion logs were seen before structured scoring; review is not blinded.

The unchanged [stored-run auditor](../../tools/stored_run_audit.py) binds each source/key cohort and keepsUNRESOLVEDin the denominator. Across main252calls:57972inputtokens,1092generatedtokens includingEOS,2711293472bytes of terminal caches. The acquisition diagnostic adds12calls and108346752cachebytes, not another training step. Main and posthoc results remain separate.

## Preservation improvement: a real adapter capsule

The pressure audit identified local-only binaries as a material dependency. We built a [standard-library capsule utility](capsule/README.md) with six toy integrity/safety checks, then created and reread a local portable archive:

- Path:`/workspace/frr_capsules/counterbalanced-curriculum-v1.tar.gz`
- Size:6286976bytes,13fixed regular members.
- SHA256:`9de2597270823bf5165cf6d47366dc2cede21fe816549ab7f54765df03fa84bc`.
- Includes control/candidate initial and final adapters, their manifests, optimizer-state bytes, training manifests and pinned-base identity.

[Build receipt](CAPSULE_RECEIPT.json) and [verification receipt](CAPSULE_VERIFY.json) confirm hashes, completeF32tensor shapes/finiteness and bounded member inventory. The utility never loads optimizer pickle data, never overwrites/deletes source or destination, and checks archive members without extracting paths. This is a local research capsule, not a universal hostile-archive service.

The capsule excludes dense original weights, older full-weight checkpoints, allterminalKVcaches and other code/data/history. It requires the pinned base and compatible runtime. **It is not an independent backup until copied off workspace.** No external upload or paid storage was invoked. A filesystem failure can leave a partial newly created archive; the utility does not delete history to clean up. No model or archive is promoted to truth/authority because its hash matches.

All997previously recorded runtime artifacts verified unchanged, plus264newcache/prompt/token/output checks and current checkpoint/optimizer/capsule hashes. All old FRR source/history files are checked before navigation sync. New binaries remain local, with hashes/manifests published; source/data/logs are recorded in Git. Current original model remains default.

## Are other areas under pressure?

The [read-only sweep](PRESSURE_SWEEP.md) inspected the current handoff/map/queue/recentreports and a capacity snapshot. Its references are point-in-time; the prior orientation is archived here. It found no immediate memory/disk/OOM blocker for a comparable bounded local run. It did not establish that the entire research garden is clear or audit every historical branch.

1. **Learning acquisition and source binding:** immediate scientific priority. The counterbalanced package removed known data cues, but the checked seen-source slice still produces a constant answer. Do not spend larger transfer budgets assuming the basic lesson was acquired. A small balanced acquisition diagnostic should precede further complexity; it remains separate from held-out evidence.
2. **Missing-state/output interface:** unresolved. Candidate0/24missing on primary, despite exposure. Single-token aliases with counterbalanced mappings remain a possible capability-isolation control, not performed here and not an explanation already proved. Source missingness is not epistemic confidence rejection.
3. **Preservation and resource boundaries:** no current emergency, but local binaries and growing caches matter. The capsule makes a scoped copy practical; it does not complete independent archival. Guards are sampled/local and ordinary failures are not a universal recovery service. Nothing was deleted to relieve disk use.
4. **Longer reuse and source revision:** strongest distinct broader research branch. Have a writer make an actual compressed handoff, revise the underlying source, and test whether a reader retrieves/reopens the correct current evidence. Include stale/wrong-source controls and measured retrieval/token/time costs. This can advance the harness without making the small model the authority.
5. **Ancestry versus authority:** registry/LCA can trace declared byte lineage and shared parents, not truth, error cause or independence. Versioned-source/receipt selection remains a useful operational contact.
6. **Physical-pressure metaphor:** still unvalidated as a general law. Particular blocked claims need their own raw timeseries/formal variables/nulls; none is required to improve the present local workflow.

## What changes in practice

Optional [seen-acquisition-before-transfer guidance](../../examples/seen-source-acquisition-before-transfer.md) records the lesson: a constant-answer seen-source result means acquisition is not yet demonstrated on that slice; it does not prove universal incapacity or replace fresh tests. The module link is optional guidance, not a new core/default policy or a universal numerical pass threshold.

Next strong work should isolate a learnable readout on a simple balanced acquisition slice before another complex transfer curriculum. In parallel, longer compressed handoff/source-revision experiments are well-motivated by the queue. Existing verifiers, registry/LCA code, core/schema, broadqueue statuses and earlier failed reading gate remain unchanged. Assistants authored/reviewed data/code/preservation; coordinator froze, ran, checked and integrated. No independent empirical replication or broadFRRefficacy claim. No further training/model promotion/background task was started after this result.
