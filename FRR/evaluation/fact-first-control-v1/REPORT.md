# Fact-first proposals need a tested interface

1 November 2026 UTC (workspace date). Prospective primary diagnostic plus explicitly outcome-informed familiar-status follow-up. The user's wider multi-turn exploration idea remains parked; no downstream feedback loop or training is introduced here.

## What this contact establishes

Separating facts from actions did not by itself make this small adapted reader reliable. Its declared fact proposals were poor, and their unchecked controller resolved none of the tested logical worlds. A controller that parses and corrects the visible fields resolves every toy world, but that result belongs to the code plus supplied-record worker, not to model self-correction. The checked controller is structurally equivalent to the mechanical visible-input comparator in this grammar.

A follow-up distinguishes interface trouble from a broad inability to read records: the familiar canonical prompt reads all 18 supplied snippets correctly, including other-plot names. With target/access context included, familiar answer labels reach 18/24 under original access wording and 12/24 under the alternate wording. The literal fact-status interface gives zero recognized outputs. This is a narrow boundary between prompt packages; it neither identifies a neural cause nor proves an internal reasoning shape.

## Primary design and frozen contract

Existing SmolLM2-135M-Instruct canonical LoRA reader, unchanged weights. Target/distractor pairs Aster/Birch, Linden/Juniper, Rowan/Willow differ from earlier lesson/study names but are not globally novel words. Three target statuses, two archive record orders and four observation/access conditions give 72 logical source worlds. Hidden source states/orders can share the same visible observation.

Per name, eight unique observations: three target-visible statuses, three wrong-target visible statuses, no visible record with archive access, no visible record without access. Two access wording packages yield 48 unique observations. Four separate fresh-cache prompts per observation ask for direct action, visible-record identity, visible status, and access: 192 actual main model generations. The three fact replies are assembled externally; they are not one model-authored integrated plan and cost three forwards rather than one.

Access packages are `Archive accessible: yes/no` and `Archive access: available/unavailable`. Field label and value words change together. Rules and visible facts remain equivalent. No examples, new training, candidate projection, prompt search or order selection. Direct prompts allow 24 output tokens; fact prompts allow 12. All end by EOS, not token cap. No input truncation.

Declared fact values are ROLE TARGET/OTHER/ABSENT, STATUS positive/zero/missing/none, ACCESS OPEN/CLOSED. Whole token or last corresponding declaration is accepted after case/outer-whitespace/one-period normalization. A later invalid/negated declaration does not revive an older valid one. No guessed synonyms. The prior declared action decoder is copied unchanged. Four test groups check decoding, hidden-field exclusion, controller dependencies and case/observation counts.

The new literal-status values differ from the answer tokens used in the reader's earlier acquisition; this is a material interface confound. For example `NO` is formally invalid as a literal-status proposal, even though it is the familiar answer label for zero. We preserve that reply, rather than calling invalid formatting proof of absent understanding or retrospectively changing the scoring language.

## Model observations before correction

Each row below counts unique visible observations, not repeated hidden worlds.

| Access wording | Observations | Identity recognized / correct | Literal status recognized / correct | Access recognized / correct | All three facts correct | Direct action matches visible rule |
|---|---:|---:|---:|---:|---:|---:|
| shared_yes_no | 24 | 22 / 9 | 0 / 0 | 17 / 14 | 0 | 6 |
| distinct_words | 24 | 23 / 9 | 0 / 0 | 13 / 9 | 0 | 6 |

Identity outputs are TARGET on 45/48 observations and an observational echo on the remaining three. Every correct identity classification is a target-visible case; no OTHER or ABSENT category is emitted. Status outputs are NO on 42/48, NO VISIBLE RECORD on four, and NO WELCOME STATION / NO STATUS once each. All are invalid under the predeclared literal-status grammar. Access outputs include OPEN, NO, ACCEPTED, empty text and other strings; recognition alone is not correctness.

| Target | Original identity / access correct, each out of 8 | Alternate identity / access correct, each out of 8 |
|---|---:|---:|
| Aster | 3 / 4 | 3 / 4 |
| Linden | 3 / 5 | 3 / 4 |
| Rowan | 3 / 5 | 3 / 1 |

No target has a correct joint tuple. Original wording yields 14/24 correct access facts versus 9/24 for alternate wording. That is evidence against adopting this alternate wording as a repair here; it does not prove that shared labels never cause errors or that one wording is globally better. Direct action has the same number of grounded outcomes under both packages despite differing raw replies. Alternate direct prompts emit two UNKNOWN replies, both inappropriate deferrals with accessible evidence, not justified absent-evidence recognition.

## Execution and attribution

The proposed-facts controller uses a recognized status when ROLE is TARGET, otherwise recognized access when ROLE is OTHER/ABSENT. Missing required facts yield an invalid action. It never consults hidden source truth. The checked-facts controller compares each proposal to values parsed from the visible record/target/access field; incorrect or invalid fields are replaced explicitly and discrepancies saved. This is deterministic delegated repair, not a second model review or model learning from failure.

| Wording / policy | Logical worlds | Grounded answers | Justified unknown | Resolved | Requests | Unavailable requests | Nominal query units |
|---|---:|---:|---:|---:|---:|---:|---:|
| shared_yes_no / direct | 72 | 12 | 0 | 12 | 0 | 0 | 0 |
| shared_yes_no / proposed_facts | 72 | 0 | 0 | 0 | 0 | 0 | 0 |
| shared_yes_no / checked_facts | 72 | 54 | 18 | 72 | 36 | 0 | 36 |
| shared_yes_no / observed_input | 72 | 54 | 18 | 72 | 36 | 0 | 36 |
| distinct_words / direct | 72 | 12 | 0 | 12 | 0 | 0 | 0 |
| distinct_words / proposed_facts | 72 | 0 | 0 | 0 | 0 | 0 | 0 |
| distinct_words / checked_facts | 72 | 54 | 18 | 72 | 36 | 0 | 36 |
| distinct_words / observed_input | 72 | 54 | 18 | 72 | 36 | 0 | 36 |

Direct action supplies 12 grounded answers per 72 worlds, no useful requests and no justified unknown. Unchecked facts yield 72 invalid actions per wording. Checked/observed policies each supply 54 grounded answers plus 18 justified unknowns, with 36 target-record requests and no unavailable request. Nominal units are toy accounting, not dollars; model forward costs are additional and must not be hidden behind that metric.

The 576 logical routes arise from 72 worlds × two wordings × four policies. All model-policy choices and receipts are preserved. Across checked/observed routes, 144 logical tool deliveries share nine actual selected-record worker generations (nine misses, 135 within-run cache hits). Those nine workers read the three statuses for each target correctly. This reuse is explicit, not 144 independent successes. No full-source request is generated in this contact. Source receipt identity/label checks assess support in the authored grammar, not external truth or an independent judge.

The checked policy does not need the model proposals to implement its action rule: it can reconstruct all visible facts itself. Its perfect toy score therefore supplies no evidence that adding three fact-generation calls improves over the simpler mechanical comparator. Keep that cost and attribution visible.

## Outcome-informed familiar-status follow-up

After the primary run exposed zero valid literal-status replies, freeze a separate diagnostic before all new outputs: 48 contextual prompts now request familiar YES/NO/WITHHOLD labels (UNKNOWN if no visible record), plus 18 unique visible snippets under the exact canonical worker format. No old invalid output is re-scored, and no policy or model is retrained.

| Prompt package | Correct / actual probes | Positive | Zero | Recorded missing | No visible record |
|---|---:|---:|---:|---:|---:|
| Context + original access wording | 18/24 | 6/6 | 6/6 | 6/6 | 0/6 |
| Context + alternate access wording | 12/24 | 6/6 | 0/6 | 6/6 | 0/6 |
| Canonical worker, supplied snippet only | 18/18 | 6/6 | 6/6 | 6/6 | not tested |

All original-context visible statuses are read correctly, including records for a different plot. Neither contextual package handles absent records correctly. Under alternate wording, zero-status recognition also fails. This strengthens the distinction between supplying a readable snippet and asking the model to locate its role, deal with absent evidence, and choose a next step.

Canonical snippet comparisons change instructions, output language and surrounding context as a package. They do not isolate whether vocabulary, task framing, attention to nearby fields, acquisition history, or another factor is the cause. Some canonical prompt strings repeat earlier actual worker calls; these are fresh calls here, not fresh independent models. No novel general control competence is demonstrated.

## Useful refinements and strongest next directions

1. Keep the proven supplied-record worker frame as a reference condition. Do not promote the new fact schema or alternate access wording to defaults. Test unfamiliar observation formats before relying on them in a controller.
2. Make delegation explicit: visible-field identity/access parsing, model record reading, and source receipt verification are separate responsibilities. In this authored domain, the simpler parser/controller comparator is both more reliable and less expensive than generating three unreliable fact proposals before overriding them.
3. A strong next diagnostic is a matched-context worker comparison: keep the same supplied record and familiar output mapping while adding only a target line, only an access line, and their combination, with irrelevant-field controls. Freeze every condition and use fresh names before inspection. This can narrow the context/role boundary; it must not be called a neural mechanism or a universal prompt repair.
4. A later hybrid may use verified identity/access routing plus the proven supplied-record reader, tested on changed layouts and source revisions. Broader writer/handoff/planning/memory branches remain open; a weak tiny-model router is not a universal gate on exploration.
5. The larger recorded downstream loop remains a seed, not implemented. Model error awareness, feedback-driven revision and durable learning are separate untested questions in this contact. Earlier downstream-review results remain historical.

## Reproduction, resources and preservation

Run preparation/tests before generation. `python study.py prepare`; existing environment `/workspace/cache_backend_venv/bin/python study.py run`; `python study.py score`; `python verify.py`. Then child `familiar-status/check.py prepare` and `run`; finally venv `final_audit.py`. All output creation is exclusive: use a new study directory for a repeat, do not overwrite the frozen record. Local model and canonical adapter paths remain in scripts; dense model/runtime are not bundled in GitHub.

Base HuggingFaceTB/SmolLM2-135M-Instruct revision 12fd25f77366fa6b3b4b768ec3050bf629380bac; base SHA256 5af571cbf074e6d21a03528d2330792e532ca608f24ac70a143f6b369968ab8c. Canonical adapter SHA256 4d83525c501f2c68fdfaf127f5f6ffe7d1c30c0bba14ae7168b0cee3aba524e9. CPU float32/eager, two threads, greedy generation, fresh cache per call, fixed seed73103. Base and adapter in-memory digests and saved dependencies remain unchanged.

267 actual generations =192 main probes+9 workers+66 follow-up, 258 distinct prompt strings, 576 logical routes. Input/output tokens 34,675/922. Generation time 120.816 seconds excludes model loading, scoring and documentation; it is not a full wall-time or billing estimate. Sampled working estimate max 1,936,130,048 bytes and RSS max 896,811,008 bytes, below the 5,153,960,755-byte working guard. No call reaches its output cap.

All frozen dependencies, raw prompt/tokenization/decoded outputs/stops, controllers, archive results, worker bindings and source receipts pass audit. 3,753 older local files are unchanged before navigation sync. Four current navigation/method-note originals are archived; historical results are not rewritten. No training, weight changes, installs, downloads, paid API/rental, independent empirical replication, default module/policy or core/schema change. User billing/usage is not visible. No background model task remains. Existing adapter capsule/desktop-copy/restore limitations remain unchanged; no new backup or restore claim.

[Protocol](PROTOCOL.md) · [Primary summary](run/SUMMARY.json) · [All proposals](run/RAW.jsonl) · [All executed routes](run/ROUTES.jsonl) · [Follow-up protocol](familiar-status/PROTOCOL.md) · [Follow-up results](familiar-status/run/SUMMARY.json) · [Checks](CHECKS.json) · [Final token/resource audit](FINAL_CHECKS.json)
