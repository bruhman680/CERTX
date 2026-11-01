# Command meaning and conditional choice need separate evidence

31 October 2026, America/Chicago (client date). Completed prospective description interface, order-balanced guidance contact and targeted name-transfer check. Original model weights and prior scores remain unchanged.

The declared language interface works on its stated positive/negative cases and recognizes historical descriptions that the older word-only parser rejected. That did not create new policy competence: both decoders produce exactly the same actions on all 80 fresh router replies. One of six example arrangements produces useful evidence requests on the original test name, but that request does not survive two new target names. Explicit rule text does not yield useful requests in any tested rule order.

We have a usable small interface component and a narrow, arrangement-sensitive request behavior. We do not have evidence for a robust independent controller, autonomous understanding of uncertainty, or general FRR efficacy.

## A. Declare the action language before new model outputs

The new declared_v2 decoder accepts six action words, their exact offered descriptions, and two explicitly named unpriced request phrases. Case, whitespace and one trailing period normalize. It does not infer arbitrary synonyms or intended actions. Last ACTION: declaration governs even if unsupported; it never revives an earlier valid command after a later negation. Bare responses must match an entire declared word/phrase. Extra non-declaration text after a recognized tag is retained and flagged, not interpreted as intent.

Examples: “report insufficient evidence” maps to UNKNOWN; “report sufficient evidence” remains unsupported. “do not request target record,” mixed YES-or-NO, wrong declared prices and negated last commands remain unsupported. A recognizable command is still only a proposal; source support is assessed separately.

All 43 authored fixture expectations pass, including 15 negative/unsupported cases. The earlier strict parser accepts 4 of those negative cases through prefix/earlier-tag behavior; declared_v2 accepts 0. These are development/instrument checks, not independent empirical validation or a universal natural-language safety claim.

Regression replay recognizes 76/96 earlier outputs under strict_v1 and 91/96 under declared_v2. The extra fifteen are the previously observed insufficient-evidence descriptions. This is historical interface coverage, not fresh model improvement; old scores are untouched. In the new 80 router probes, action interpretations differ on 0 cases. The added descriptions simply were not emitted, so the new decoder has no fresh end-to-end score advantage here.

[Decoder source](decoder.py), [fixture data](DECODER_FIXTURES.json), [historical replay](HISTORICAL_DECODER_REPLAY.json), [tests](TEST.stderr). Five focused test groups cover all fixtures, last-invalid declarations, opposite meanings, hidden-key exclusion and rotation content preservation. No global/default decoder or tool implementation is replaced.

## B. Conditional rules versus order-balanced worked examples

Fixed adapted canonical reader, new target Clover/distractor Heather, three target states, both record orders and four observation/access conditions.24 logical worlds, eight distinct visible observations. Source names differ from the lesson names Iris/Moss; this is study-held-out naming, not globally novel tokens. The distractor is a cyclic alternative, always conflicting. Only line-format source displays are tested.

Common prompt explicitly permits action words/descriptions. It is held fixed across no guidance, three cyclic rule-clause orders and six cyclic example-block orders. The rule states target-name matching, retrieval when the target is absent but archive accessible, and UNKNOWN when neither target evidence nor archive access exists. Worked examples retain their facts and attached numbers while changing position. Rule/example packages differ in length/content/format; these are whole guidance comparisons, not an isolated teaching mechanism. Rotations do not cover all permutations.

| Guidance/order | Grounded answers /24 | Justified unknown /24 | Formal task terminals /24 | Requests | Unavailable requests |
|---|---:|---:|---:|---:|---:|
| none__0 | 4 | 0 | 4 | 0 | 0 |
| rule__0 | 4 | 0 | 4 | 0 | 0 |
| rule__1 | 4 | 0 | 4 | 0 | 0 |
| rule__2 | 4 | 0 | 4 | 0 | 0 |
| examples__0 | 4 | 0 | 4 | 0 | 0 |
| examples__1 | 4 | 0 | 4 | 0 | 0 |
| examples__2 | 4 | 0 | 4 | 0 | 0 |
| examples__3 | 4 | 0 | 4 | 0 | 0 |
| examples__4 | 4 | 0 | 4 | 0 | 0 |
| examples__5 | 12 | 0 | 12 | 8 | 0 |

Strict_v1 and declared_v2 results are identical on these new outputs. Every order is shown rather than selecting the best as the aggregate result. Formal task terminals combine source-supported answers and justified lack-of-access unknowns; components remain separate. No universal reward score is imposed.

Example order 5 generates TARGET on two distinct visible observations: no visible record with archive access, and one wrong-target record. Those two real free outputs drive eight logical retrievals, six from the repeated source-free observation and two from the wrong-record observation. All eight obtain a correctly selected source and the unchanged worker reads it correctly. This is useful behavior in one local arrangement; it is neither eight independent discoveries nor a reliable general policy.

Other five example orders make no requests. No rule order makes a request. No new primary reply uses UNKNOWN, even with absent evidence and no access. The older UNKNOWN pattern therefore fails to transfer under this prompt/name package; changed names, invitation wording and output allowance cannot be separately blamed. Maximum24tokens is the same in every new cell and all replies end by EOS before reaching it.

## C. Does the selected request survive a name change?

After observing order 5, freeze a targeted check with original order 0 as comparator. Pair archive-accessible yes/no with no visible record under Clover (old control), Marigold and Sorrel (new relative to these lessons/primary prompts).12 actual new router probes, four old-prompt replications. No tool/worker actions execute in this follow-up; it tests the proposed next action only. Candidate order selection is explicit and outcome-informed, so this is a limited transfer diagnostic, not independent policy confirmation.

| Target | Example order | Accessible archive | Inaccessible archive |
|---|---:|---|---|
| Clover | 0 | NO | NO |
| Clover | 5 | TARGET | NO |
| Marigold | 0 | NO | NO |
| Marigold | 5 | NO | NO |
| Sorrel | 0 | NO | NO |
| Sorrel | 5 | YES | NO |

All four Clover baseline input/output token sequences match the primary run. TARGET survives only for Clover/order 5/archive yes. It disappears for both new names, and no case gives the stronger request-when-available / UNKNOWN-when-unavailable pair. Only the target-name text and access flag change in this check. This establishes a narrow surface/context dependence in these prompts, not a cause in particular neurons, a linear-thinking law, or inability across all prompts/models.

[Transfer protocol](availability-transfer/PROTOCOL.md), [freeze](availability-transfer/FREEZE.json), [raw](availability-transfer/run/RAW.jsonl), [summary](availability-transfer/run/SUMMARY.json), [checks](availability-transfer/CHECKS.json). New names do not make these independent seeds or end-to-end ground-truth tasks; no source status is exposed or answered by the follow-up.

## What is working, and what remains distinct

The available-input rule implemented in code resolves this literal toy:18 source-supported answers plus 6justified unknowns out of 24,12 nominal query units, no unavailable requests. Always TARGET also resolves 24 but spends 24units and attempts 6unavailable requests. Always FULL resolves 15(9 answers+6 tool-unknowns),cost 48; always UNKNOWN resolves 6 and defers 18 accessible cases. Nominal units are declared comparisons, not dollars. An unavailable-tool backstop differs from a model recognizing insufficient evidence.

A conditional rule written in a prompt is not the same as a rule executed by the controller. The fixed worker remains effective with a supplied selected record; its new routing role has not acquired stable conditional behavior from these prompts. There is no weight training in this contact. The archived source-selected readout skill and earlier error/repair results remain intact.

An independently useful noticing: some invalid commands are observations, for example “(no visible record).” That may echo a real provided fact while failing to choose an action. It is not automatically equivalent to UNKNOWN: if an archive is accessible, retrieval is possible. A future pipeline could verify source-bound fact proposals and let a separate controller apply the rule. That would be delegated interpretation/control, not proof that the little model chose the action itself. We have not run that fact-first variant here.

One speculative next explanation to test is role/label collision: the input’s access flag says yes/no while answer actions YES/NO mean positive/zero. The Sorrel follow-up emits YES for accessible and NO for inaccessible under one arrangement. That alone does not establish the cause. A countertest could change only access-field wording while preserving its meaning, keeping target-status labels fixed, and compare role extraction with full action choice. Do not promote a lexical rewrite without those tests.

## Execution and preservation

[Protocol](PROTOCOL.md), [freeze](FREEZE.json), [sources](DATA.json), [queries](QUERIES.json), [raw router replies](run/ROUTER_RAW.jsonl), [worker probes](run/WORKER_RAW.jsonl), [actual route traces](run/ROUTES.jsonl), [summary](run/SUMMARY.json), [audit](CHECKS.json), [final bindings](FINAL_CHECKS.json). No forced action projection; both decoders process identical new replies and all chosen requests, mistakes and unavailable outcomes are retained. Source receipts use the authored literal grammar, not external-world truth or source authenticity.

Primary: 80 actual router generations+9 actual worker generations,576 logical policy routes under paired decoders and fixed controls. Router tokens25638input/229output; worker tokens828input/30output. Readout time68.679seconds excludes loading/other work. Sampled working maximum1947881472bytes,RSS914194432bytes; not continuous peaks or billing. Duplicate worker prompts cache within the run with exact IDs/hashes, not independent inference.

Follow-up:12 actual router generations,4588input/27output tokens,11.355generation seconds,zero new tool/worker actions. Overall 101 actual generation probes,97distinct prompt strings. Historical 96-output replay adds no model call and is not mixed into prospective outcomes. Same pinned base/final adapter,eagerfloat32,twoCPUthreads,last-logit head bound to prior scoped calibration,max768input/no truncation,24outputcap,working guard. No new candidate scoring/optimizer updates,weights,packages,downloads,paidAPI or rental.

All 43 decoder fixture expectations, transcript/tokenization/decoding checks, action/source/tool/cache outcomes and frozen/checkpoint hashes pass. 3,698 earlier local files unchanged before navigation sync. Four old navigation/method-note documents are byte-archived here. No core/schema/general tools/default model or queue change. Full new KV tensors are not retained; historical caches/model states remain intact. Existing local adapter capsule and older desktop capsule remain different; no new independent backup or clean-environment/optimizer-resume claim.

## Confident next directions — unexecuted

1. Keep the declared action interface available as a narrow study component, with unsupported phrases preserved rather than guessed. It recognizes specified descriptions; it does not teach a policy or reveal private beliefs.
2. Compare a fact-first reader plus explicit controller with direct action choice. Verify target-match/access proposals against source fields while allowing provisional mistakes into a bounded repair branch. This tests the recognition/decision boundary without making an action-format failure block all exploration.
3. Countertest access-flag wording and source-role binding before blaming a unique mechanism or training a larger router. Fresh names/layouts and order-balanced replication matter before adopting the selected example order.
Broader writer-produced handoff, source-revision/retrieval, matched-length neighbor and planning/interactions branches remain open. The parked Grok substrate-depth/neural-criticality relay remains unvetted/unadopted. No broader branch is held hostage to this small router’s performance. No independent empirical replication, FRR/no-FRR efficacy or general semantic verification claim.
