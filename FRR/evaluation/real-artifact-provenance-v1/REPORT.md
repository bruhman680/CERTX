# Real history, temporal questions, and feedback-source scouting

Session date: **1 November 2026, America/Chicago**. Source access and execution host date:2 November 2026 UTC. Git dates remain verbatim source metadata. This resumed contact includes a real repository-history audit, a tiny temporal fixture, parallel primary-source scouting, the user's SDPO/C2C shares, and intake of Claude's recent branch. There were **no new small-model generations or training updates**. Two role-separated assistants researched/reviewed sources; this is not independent model replication.

## 1. What real repository state was checked

The declared question is exact bytes of `FRR/CURRENT_HANDOFF.md` at a pinned branch-head acquisition cutoff, plus eight bounded first-parent snapshots. The branch is authoritative for this narrow repository-state question, not for scientific truth in its documents.

Repository `bruhman680/CERTX`, branch `codex/frr-progress-2026-10-07`, pinned head `fdb0f707101364121650789912b47ca572e50d93`. This pin precedes publishing this report; the publication will create a later head. The captured document's paused wording describes the old cutoff and remains preserved, while current navigation is updated separately.

Actual commit-object parents were followed rather than assuming adjacent file-log entries are parents. All eight captured commits have one parent; no merge, rename or real deletion is empirically tested. The last parent outside the window is explicitly retained as a frontier, not treated as a genesis root or missing proposition. No full-history/all-branch claim is made.

For each commit, the root tree, FRR directory tree and artifact blob were acquired. All 16 tree object hashes and 8 blob hashes recompute correctly, and the local pre-sync handoff equals the captured head bytes. Nine unit groups and six synthetic negative controls pass. Corrupt content/tree, omitted within-window parent, wrong authority pin, wrong scope and an out-of-window request remain distinct failures. Source collection order does not change selection. Synthetic corruptions are copied controls, not real Git events.

| Commit snapshot | Artifact blob | Bytes | Signature status reported by API |
|---|---|---:|---|
| [fdb0f70710](https://github.com/bruhman680/CERTX/blob/fdb0f707101364121650789912b47ca572e50d93/FRR/CURRENT_HANDOFF.md) | `29acd0c9ffd8d0f766df1ce90c50c94a1c9e8af5` | 2913 | unsigned |
| [a6687963ee](https://github.com/bruhman680/CERTX/blob/a6687963ee55d19f59e581fb28569a3e141af54f/FRR/CURRENT_HANDOFF.md) | `5e7942e963e76641845bc9afe0dd2ac464fff721` | 2860 | unsigned |
| [defbe7d689](https://github.com/bruhman680/CERTX/blob/defbe7d6892a16b90785587e1f65d7b9d8692b9b/FRR/CURRENT_HANDOFF.md) | `97408254a31c45b97ccba45133e835189a6f9e8b` | 4043 | unsigned |
| [3010deae56](https://github.com/bruhman680/CERTX/blob/3010deae5640b43017a7adca01b4499b7ace2d9f/FRR/CURRENT_HANDOFF.md) | `d34821af9b7b8739acfc72a3f07f2b95ea6ed6da` | 3418 | unsigned |
| [093f60cd9c](https://github.com/bruhman680/CERTX/blob/093f60cd9cc91512597f68966d55bb2fd4a3a933/FRR/CURRENT_HANDOFF.md) | `465043b9c5467377b6d12a996b56693b63692683` | 3982 | unsigned |
| [fb48d83c1a](https://github.com/bruhman680/CERTX/blob/fb48d83c1ae9ef82edff082495630daaa90125f2/FRR/CURRENT_HANDOFF.md) | `516736359e6a59a3aab747538c9260ac3569f85a` | 5503 | unsigned |
| [9a794f1266](https://github.com/bruhman680/CERTX/blob/9a794f12668a8385bc8b9de000acd9cf3cd6058d/FRR/CURRENT_HANDOFF.md) | `f5a1b4ede3440e0e48f614bdcb77a659b5c21354` | 5058 | unsigned |
| [0a7a7b103c](https://github.com/bruhman680/CERTX/blob/0a7a7b103c746f11826cff3f29bfd17c1f9701a1/FRR/CURRENT_HANDOFF.md) | `ba854ef6be583107db1c85f472a2a032aa32c54f` | 4265 | unsigned |

[Captured metadata/bytes](CAPTURE.json) · [initial policy](POLICY.json) · [initial receipt](RECEIPT.json) · [negative controls](MUTATION_CONTROLS.json) · [initial checks](CHECKS.json).

The initial frozen audit explicitly did not hash raw commit objects. A separate review then reconstructed matching unsigned commit bodies from captured tree/ordered-parent/author/committer/message fields. **All 8 match their Git commit IDs**, independently checked by Python's object hash and `git hash-object`. API UTC timestamps omit original serialization offsets; matching candidates require -0500 for author/committer and zero appended message newlines. UTC candidates fail. This is a useful distinction between equivalent timestamp instants and byte-identical serialization.

The original audit stays unchanged. [Supplemental binding](COMMIT_BINDING.json), [matching reconstructed bodies](commit-bodies), [review](scouts/COMMIT_BINDING_REVIEW.md), [binding checker](commit_binding.py) and [final checks](FINAL_CHECKS.json) add the stronger result. Changed commit-to-tree metadata is rejected by the supplement. These bodies are reconstructed matches, not raw wire payloads. All 8 are reported unsigned; content-address consistency does not authenticate a person, establish externally mandated authority, or prove factual claims.

The full 269,664-candidate failed/matching enumeration is 53.9 MB and remains local; its exact bytes/hash/path are recorded in COMMIT_BINDING.json. Compact counts/matches,24initial failed UTC candidates and the observed reconstruction reference are published. The deterministic reference can regenerate the search, but its original paths must be copied/adjusted before a new run; it is not automatically executed. No claim is made that every local artifact or model binary has a new independent backup.

## 2. A bounded lateral temporal contact

A primary-source scout identified a separate question the previous revision toy did not represent: what was received by cutoff K versus what was asserted effective at V. The following fixture uses ordinal coordinates, not inferred real Git timestamps or verified real-world validity.

Two immutable claims: e1 arrives at K1 and says ready from V1; e2 arrives at K3 and explicitly corrects e1 to blocked from V2. Under that declared interval policy:

| Receipt cutoff | Effective point | Answer | Witness |
|---|---|---|---|
| K1 | V1 | ready | e1 |
| K1 | V2 | ready | e1 |
| K2 | V1 | ready | e1 |
| K2 | V2 | ready | e1 |
| K3 | V1 | ready | e1 |
| K3 | V2 | blocked | e2 |

After e2 arrives, replaying K2,V2 still returns ready/e1; K3,V2 returns blocked/e2; K3,V1 remains ready/e1. The six answers and the complete earlier receipt pass a second-agent functional review. This shows the declared distinction on one two-claim fixture, not a full temporal database, general source authority resolver, or model temporal skill. Finite interval ends, arbitrary correction graphs and authentication are not implemented.

The initial rows retain coordinates/eligible IDs/witnesses, with correction edges recoverable from immutable claims. A separate [edge projection](TEMPORAL_EDGE_RECEIPTS.json) makes those links explicit without rewriting the initial [result](TEMPORAL_CONTACT.json). [Review](scouts/TEMPORAL_REVIEW.md).

## 3. New uploaded SDPO paper: useful, with capability boundaries

The upload identifies **Reinforcement Learning via Self-Distillation**, arXiv 2601.20802v2, 16 February 2026. [Detailed extraction](scouts/SDPO_EXTRACTION.md) checks the uploaded 50-page manuscript, versioned primary paper and official repository. The attachment's hash/version are in [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json); the PDF itself is not republished.

SDPO optimizes model weights by matching the original policy's token distributions to feedback-conditioned distributions, with stopped-gradient/regularized self-teacher variants. It is not just an extra reflection turn or a saved note. External execution/verifier information or successful same-model rollouts supply feedback; no stronger separate teacher does not mean no external information. The paper's smaller-model failures, misleading-feedback limitation and teacher-regularization ablations matter to this garden.

The screenshot numbers are supported as scoped author claims: Olmo3-7B chemistry reaches the specified 5h-GRPO accuracy after 50 minutes (initialization/validation excluded); the approximately threefold reduction in attempts concerns 22% discovery on 9 selected very-hard coding tasks, not a general wallclock speedup. Reported experiments use 4 GH200 GPUs, not established minimum requirements. We did not reproduce the benchmarks or implement SDPO on the 135M reader.

**Important qualification:** a teacher need not initially produce a complete correct answer to supply useful token-level credit. The hard-task experiment reports initial whole-answer teacher accuracy below 1% in most cases while iterative training later helps. Our reader's failed evidence notes do not by themselves prove that feedback-conditioned logits would be useless. Conversely, the paper does not establish useful retrospective signal at 135M. Replaying the original failed attempt also hurts one reported ablation, so more history is not automatically more useful feedback.

The strongest direct next small-model contact is a **frozen-weight feedback-quality probe**: original context, verified feedback, irrelevant feedback and misleading feedback; measure correct-answer probability changes and actual correction separately, retaining exactly which evidence was supplied. This is not run here and would not by itself establish training, dense-credit transfer, or source truth. Any later weight-updating study needs its own frozen protocol/checkpoints/holdouts within the user's standing local-work authorization; no new approval gate is introduced by this source note.

## 4. C2C refresh and the newly linked AKV lead

[Primary-source refresh](scouts/C2C_AKV_REFRESH.md) identifies the screenshot as the already contacted C2C paper, arXiv2510.03215v2. New C2C head 5eac72b90faf7b3dc2638e874fe7cba1e74c8bcf is one README-only commit after the earlier pin; runtime/projector code is unchanged. Paper v2 and README headline metrics differ and remain source/version-specific. No benchmark or cross-model fuser was reproduced.

The README now links AKV. Bounded source inspection at c567a429a058f1abce3b2879e69978b09e0fda4c finds selective KV Drop and RoPE-based Reposition, with retained V/nonrotary content copied. **Inference:** retained later states can still carry information from removed context; deleting direct KV access is not demonstrated counterfactual forgetting, factual retraction or exact fresh-forward equivalence. C2C's trained cross-model fuser and AKV's within-model cache editing are different mechanisms.

The inspected AKV backend requires CUDA/modified SGLang and excludes LoRA in its documented context-operation scope; SmolLM2 is not in its documented supported list. The actual project venv has Torch 2.6.0+cpu and Transformers, CUDA unavailable, SGLang unavailable. A separate ambient-Python probe must not be mistaken for Torch absence from the whole environment. No packages, server, checkpoints or GPU service were installed. Agent-side policy ideas are a lead; no runtime capability or chat-KV access is adopted here.

## 5. Claude branch: preserved intake and exact analytical correction

The most recent relevant branch among the inspected candidates is `claude/pam-scoped-negation-2026-10-25`, pinned b82724c2427151d38f5d0c45cd7cc87e9359565a. [Bounded intake](scouts/CLAUDE_LATEST_RELAY.md) reads its claim-scored procedure relay/code/printed outputs and adjacent error/success scripts; finite-sample/dispersion contacts are relay-depth only. No branch merge or untrusted script execution occurred.

Useful lessons are narrower than general FRR success: a procedure's restraint depends on its ambiguity detector's calibration, and within-trajectory stability can conceal between-trajectory shared conditions. Printed results are author-reported; no per-trial/RNG receipts were found in the inspected directory, no Monte Carlo reproduction occurred, and oracle-style probe responses are not implemented physical source repairs.

One exact generator-law check is reproduced with standard-library fractions. True marginal p=.2, independent symmetric flag error epsilon=.05, and true joint .08(DIFF)/.2(COMMON) give observed q=.23 and joints .0853/.1825. Thus:

- DIFF conditional agreement =853/2300=**.3708695652**, not the relay's approximately .42.
- COMMON/COPY =73/92=**.7934782609**.
- Midpoint =1339/2300=**.5821739130**; .6 is that midpoint rounded to one decimal and still separates these population values.

[Exact calculation](CLAUDE_GUARD_ALGEBRA.json) and [reference check](CLAUDE_GUARD_ALGEBRA.py) preserve the source pin and limits. This corrects analytical justification, not the executable threshold or reported finite-sample results. The intake also records a stale 90%-guard description versus executable .6conditional agreement, residual wrong claims alongside withholding, heuristic uncertainty widths, absolute-/tmp portability problems, and a high/low word-index convention mismatch that current reversible toy laws may hide. The saved decomposition results are **not** declared invalid without checking that symmetry; a nonreversible extension needs an explicit indexing audit.

Original claims and failures remain in Claude's pinned branch; this record adds a dated intake rather than overwriting them or importing the procedures as runtime defaults.

## 6. Refinements and next directions

The useful infrastructure refinement is a clearer receipt boundary: **stored bytes/ancestry → declared interpretation and temporal scope → authentication/authority → warranted claim → demonstrated model change**. One layer passing does not prove the next. [Optional practice note](../../examples/content-history-and-feedback.md) records these distinctions; no core/schema/default model/module is replaced.

Priority next: the small frozen-weight feedback-quality probe above, using verified evidence and untouched counterexamples before any distillation claim. Parallel formal work can test alternative versus jointly necessary supports before source withdrawal: a flat contributor set loses AND/OR dependency structure. This is a separate unexecuted lead from provenance-semiring research, not an implemented general retraction mechanism. Claude's guard also needs an outside-family/sham-calibration check before broad attribution claims.

Wider multi-turn autonomous feedback/exploration remains parked from the earlier user choice; one-step diagnostic proposals do not silently activate it. Broader memory/handoff/planning directions and the parked Grok relay remain history. These sources guide questions rather than become compulsory gates blocking unrelated exploration.

## Preservation and source access

Nine tests, six initial mutation controls, six temporal queries,8 blob/16 tree checks and 8 supplemental commit reconstructions pass. The initial freeze/checks remain unchanged; new extension/review records are separate.3,977older local files were unchanged before navigation sync. All source snapshots, control results, reconstructed matching bodies and scoped extraction notes are retained. The full 53.9 MB candidate enumeration and existing dense model/runtime/binary capsules remain local; compact manifest/reproducer is published, not a new all-workspace backup.

Current handoff/orientation/research map are updated from paused to resumed; original versions archived. The old settling checkpoint stays immutable. No new small-model inference, training, installs/model downloads, paid API/rental, merge into main, automatic source-branch adoption, default/core/schema/general-tool/queue change or scheduled task. Two scouts completed their bounded tasks; no model/agent experiment remains running. Billing/usage is not visible.

Primary documentary sources and exact inspected scope are linked in the seven scout/review notes. Git/PROV consistency is not truth; bitemporal applicability is asserted; C2C/SDPO gains are paper claims; code inspection is not benchmark execution. Captured data were observed before this functional audit's freeze, so this is not blind empirical validation. The checker is specifically scoped to FRR/CURRENT_HANDOFF.md and the eight captured first-parent commits, not an arbitrary-path verifier.
