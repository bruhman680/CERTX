# Decision-token loss comparison and declared evidence ancestry

30 October2026 America/Chicago. Resumed the prepared PhaseA objective test and scouted the user's lowest-common-ancestor idea in parallel. Two48-update adapter branches completed, followed by360actual generations. No model/default promotion, paid API, rental or package install. Original model, older branches and their records remain intact.

## Result first

Reweighting the first output decision **did not solve missingness**. The losses tie8/24 on the frozen prepared primary set. The decision-balanced branch improves the counterbalanced challenge10/36→15/36, but both remain below a first/last sampled-field reference of24/36. Regression accuracy changes19/48→18/48 with a substantial positive/zero tradeoff. No general reasoning or FRR benefit follows.

| Cohort | Original zero-adapter | Sequence mean | Decision balanced | Reference |
|---|---:|---:|---:|---|
| Familiar development |0/12|5/12|6/12|constant4/12|
| Prepared primary |0/24|8/24|8/24|constant8/24; last sampled field24/24|
| Counterbalanced challenge |0/36|10/36|15/36|constant12/36; first/last sampled field24/36|
| Challenge discordant states |0/24|6/24|10/24|constant8/24; first/last field12/24|
| Exposed old regressions |1/48|19/48|18/48|constant16/48|

Primary missing recall is0/8 in both trained branches; challenge missing recall0/12; regression missing recall0/16. Decision-balanced dev correctly labels one missing case of four. It can emit WITHHOLD: two dev emissions (one correct) and one incorrect primary emission. Thus complete-label generation is possible, but missing-state decisions do not transfer reliably. All trained responses finish at EOS; the original baseline has119unfinished capped outputs and one exact label across120cases. Its score is an interface-completion result, not proof of absent latent semantic knowledge.

## Matched intervention

The [prepared protocol](../decision-token-preparation-v1/PROTOCOL.md) proposed a controlled loss change without altering semantic labels. Here both branches use the same pinned SmolLM2-135M-Instruct revision `12fd25f77366fa6b3b4b768ec3050bf629380bac`, fresh rank4/alpha8/dropout0 q/v LoRA adapters, seed73103, identical adapter initial digest,72training examples, shuffled two-pass order,48effective updates, microbatch1 with accumulation3, AdamWlr0.001/weightdecay0.01/clip1. Each completed update includes positive, zero and missing. Base parameters are frozen; only230400adapter scalars train.

For supervised target-token CE values includingEOS:

    sequence_mean = mean(all target-token CE)
    decision_balanced = 0.5*CE(first decision token)
                        +0.5*mean(remaining label tokens and EOS)

Prompt tokens are masked. YES/NO/WITHHOLD target lengths includingEOS are3/2/5. The first-token coefficient per balanced update changes from1/9,1/6,1/15 to1/6for each class. NO's per-example formula is unchanged, but shared optimization/clipping means NO behavior can still change when the other examples' gradients change. This identifies the full first/suffix loss-allocation intervention in this fixed run; it does not isolate token length from every mechanism. No alias-label training occurred.

[Eight synthetic checks](UNIT_TESTS.stderr) validate independent objective values/gradients, causal shifting/prompt masking/EOS inclusion, balanced order, accumulation equivalence and exact resource-stop accounting. An assistant implemented the runtime; coordinator reviewed/copied/froze it. Separate data-review assistant checked source/key consistency before main training. These are contributor/coordinator reviews, not independent empirical replication or external ground truth.

## Data review found a pre-training confound

A [separate review](PREP_DATA_REVIEW.md) verified all24prepared keys and binding hashes, but found that every target batch appears second and its sampled-soil field is last. Other count also equals observations per soil. The set can assess this loss/readout comparison under those conditions; it cannot establish arbitrary batch selection. It shares four settings across two formats, not24independent population draws.

The original frozen24cases were preserved. Before main training, a [prospective amendment](CHALLENGE_BASELINES.md) added [36challenge cases](CHALLENGE_CASES.json) with [separate keys](CHALLENGE_KEYS.json): two formats×three target states×three independently crossed Other states×two record orders. Target observations are fixed7 and Other observations2, so those counts no longer encode target state. All sources/keys/factorial cells were [reviewed](CHALLENGE_DATA_REVIEW.md) before model evaluation. They remain authored repeated structures with fixed target nameRowan, not a general entity-resolution dataset.

On this construction, always reading the first or last sampled-soils field scores24/36: half positions are correct, plus same-state cells rescue6more. AlwaysOther scores12/36. The24discordant-state cases remove that rescue; first/last score12/24 and wrongOther0/24. These are construction-reference policies derived from reviewed metadata, not discovered algorithms inside the model. Future claims of binding need to exceed these shortcuts, not merely beat a constant label.

The original development12 and regression48sources remain unchanged and exposed. Newprimary/challenge data are now exposed too and should become regressions for subsequent tuning. No cross-cohort pooling or treating the360calls as360independent observations.

## Execution, resources and stopping

One separate fresh resource-preflight update completed with no generation and no warm-start into the main comparison. The [PREFLIGHT_FREEZE](PREFLIGHT_FREEZE.json) binds preflight code/data; [FREEZE](FREEZE.json) binds amended main protocol, reviews, scorer and dependencies before main training. Both48-update branches and checkpoints finished **before any evaluation forward**, including primary/challenge/development. No checkpoint, prompt, learning-rate or case selection depended on outcomes.

Training times: sequence mean154.370sec, decision balanced147.819sec. Each receives48completed exposures per class and exactly the same ordered144example presentations. These are one-run timings, not evidence of algorithm speed superiority. Sampled maximum working estimate3540590592bytes; sampled process RSS1269166080bytes. Working estimate discounts inactive file cache and is not continuously measured peak/free billing quota. Per-arm300second cap and memory guard were never triggered. Resource readings are logged before checking, retaining exact offending records on the handled stop paths; after-optimizer resource stops count completed updates. Ordinary exceptions/nonfinite save failures remain bounded by script failure rather than a universal recovery service.

The average training first-token CE over the final12matched updates changes: YES1.125→1.161, NO0.746→1.207, WITHHOLD1.662→1.111. This common training diagnostic shows the objective reallocating fit; it is not held-out accuracy or semantic confidence. Different objective scalar losses are not directly interchangeable. Lower missing first-token CE did not produce missing-class transfer on primary/challenge/regression in this configuration.

The initial/final adapters and optimizer states remain under `run/{sequence_mean,decision_balanced}` locally, with actual hashes/digests in each TRAINING_MANIFEST. The preflight branch is separate. Large/tensor/pickle binaries are not published as Git text; source/data/token metadata/hashes are. Local workspace retention is not an independent archival guarantee.

## Scoring and preservation

[Scorer](score.py) was frozen before training and checks all360ordered unique run IDs before making12arm/cohort views. The unchanged [stored-run auditor](../../tools/stored_run_audit.py) binds raw/key bytes and identities, checks cohort completeness, and uses whole-response stripping/uppercasing only. Unsupported outputs remainUNRESOLVED in the denominator. No likelihood/forced-choice score is substituted for generation. Selected log outputs were seen before structured scoring; coordinator review is not blinded.

[SUMMARY.json](SUMMARY.json) retains class confusion, family/position strata and paired transitions. Challenge target-first matches change5/18→9/18; target-last5/18→6/18. Primary paired changes are2mean-only and2balanced-only with6both correct; net zero. Regression loses9mean-only and gains8balanced-only; its class recalls shift positive13/16→4/16,zero6/16→14/16,missing0/16→0/16. The change mainly exchanges answer tendencies rather than delivering reliable three-way behavior.

There were73461inputtokens and1579generatedtokens includingEOS. All360newterminal caches are retained under `/workspace/smollm_decision_compare_states_v1`,3443018472bytes total. [Artifact checks](ARTIFACT_CHECKS.json) verify all360prompt/token/output/cache byte-shape-prefix bindings, all628older recorded external files unchanged, both frozen base digests unchanged, initial adapters identical, data order/exposure identical and checkpoint/optimizer hashes matching. The original baseline repeats all48older regression token sequences exactly; that is an exposed repeatability check, not independent new evidence. No default model changes, base overwrite, old state deletion or paid resources.

## Lowest common ancestor: useful provenance, carefully scoped

The parallel [LCA contact](../lca-ancestry-contact-v1/README.md) adds optional [evidence_ancestry.py](../../tools/evidence_ancestry.py). In a rooted tree, shared ancestors form a chain and its lowest member is unique. A general DAG, including merged histories, may have several incomparable best common ancestors. [Git's primary merge-base manual](https://raw.githubusercontent.com/git/git/master/Documentation/git-merge-base.adoc) explicitly allows multiple best bases; source snapshots/read-depth/fetch failures and upstream licenses are preserved by the scout.

The tool follows declared child→parent edges, includes each node itself among its ancestors, and returns every maximal common ancestor by reachability rather than arbitrary path depth. It validates all graph components, rejects cycles/unknown parents, and byte-binds optional artifacts. Bounded256nodes; no production-scale performance claim.

The real four-node/four-edge query compares two LoRA DERIVATION records that literally declare shared raw/key parent hashes. It returns **both shared raw and shared key parents**. This is a partial recorded-ancestry graph; terminal nodes are not asserted actual roots. Shared archive parentage is not proof of a shared error cause or statistical dependence of every contained observation. Missing common ancestors do not prove independence. Existing registry remains unchanged; no automatic graph is invented from its flat shared hashes.

Twelve authored test methods pass; coordinator replay passes. A separate Boolean-closure oracle agrees on640queries over all64four-node DAGs with a fixed topological order. These are bounded algorithm checks, not640evidence observations. Contributor/coordinator checks are not independent experimental replication. UTC source records31October correspond to client-local30October; the context note preserves both.

## What to carry forward

High confidence within scope: the loss-allocation comparison executed as frozen, data review exposed positional vulnerabilities before training, old state is preserved, and the optional ancestry query behaves correctly on its authored/bounded checks. Low confidence: any claim that loss weighting alone explains missingness or that a modest class-bias shift is useful general reasoning.

Strong next design move: counterbalance target role/position and Other-state within the training curriculum, reserve new names/compositions for primary testing, and keep output-label/interface controls separate. The planned cyclic single-token alias experiment remains a candidate, not performed or silently substituted. Current failures and all previously frozen records remain visible. No additional training sweep or background task was started after these results.
