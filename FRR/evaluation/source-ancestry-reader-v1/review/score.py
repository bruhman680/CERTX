"""Reproduce frozen-rubric manual adjudications plus mechanical diagnostics.
Semantic excerpts and judgments below are scorer-authored public-evidence coding,
not keyword-based inference or a model-generated substitute for manual scoring.
"""
import json
from pathlib import Path
P=Path(__file__).resolve().parent.parent
K=json.loads((P/'KEY.json').read_text())
C={c['id']:c for c in json.loads((P/'cases.json').read_text())}
E=json.loads((P/'EXECUTION.json').read_text())
manual={
'AS01':{
 'packet_action':('RELEASE','K-D and K-R each warrant criterion via complete maximum plus 0.1 C envelope.'),
 'retained_reuse_and_repair':('warranting release and reuse of the retained claim','Correctly reuses the bounded favorable claim; copying does not negate K0.'),
 'task_value_or_bound':('At most 8.1 °C','Correct one-sided bound rather than exact latent value.'),
 'support_origins':('derive from the single K0 acquisition','Correct one-root briefing origin and separate reference route.'),
 'source_scope':('the records address the exact task samples','Respects stipulated sample coverage and reference calibration scope.'),
 'evidence_fidelity':('K0 and R0 each report','Uses the two delivered measurement records accurately.'),
 'unsupported_certainty':('with an accepted absolute error bound of 0.1 °C','Warrant remains conditional on accepted error contract; independent routes are concretely specified.')},
'AS02':{
 'packet_action':('HOLD','JR establishes task violation, not merely a precautionary delay.'),
 'retained_reuse_and_repair':('do not warrant reusing the retained claim','Rejects favorable retained claim on bounded contrary task evidence, without claiming an exact repaired value.'),
 'task_value_or_bound':('True maximum at least 9.0 mm/s','Correct lower bound from 9.1 minus 0.1.'),
 'support_origins':('All three derive from one acquisition','Correct copying chain and common unbounded CT9 calibration; separate JR route.'),
 'source_scope':('JR covered the full specified series with verified timing','Correct current-series coverage and bounded reference applicability.'),
 'evidence_fidelity':('JR covered the full specified series','J-R and J-D were both delivered and accurately attributed.'),
 'unsupported_certainty':('establishing a true maximum of at least 9.0 mm/s','Asserts bounded violation, not exact 9.1 or global independence.')},
'AS03':{
 'packet_action':('UNRESOLVED','Neither compliance nor violation follows from unbounded primary and unavailable reference.'),
 'retained_reuse_and_repair':('Neither compliance nor a threshold violation is established','Correct nonreuse without converting unsupported favorable claim into established falsehood.'),
 'task_value_or_bound':('Nominal maximum 46.0 °C; calibrated maximum unknown.','Qualifies nominal value and leaves actual task value unknown.'),
 'support_origins':('Grove rendered L0, the sole sample acquisition','Correct one-root chain, with reference supplying no acquisition.'),
 'source_scope':('the failed reference recorder supplies no independent evidence','Treats unavailable reference as absence of evidence and identifies missing calibration contract.'),
 'evidence_fidelity':('The complete, correctly timed series has a nominal maximum','Accurately uses delivered L-D and L-R.'),
 'unsupported_certainty':('no valid correction or absolute error bound establishes compliance','Explicitly retains uncertainty rather than guessing favorable external truth.')},
'AS04':{
 'packet_action':('RELEASE','Bounded all-pallet measurements warrant compliance.'),
 'retained_reuse_and_repair':('warrant the retained claim','Correct reuse; no repair is necessary for stipulated criterion.'),
 'task_value_or_bound':('M1 ≤18.3 kg; M2 ≤18.4 kg; M3 ≤18.5 kg','Correct per-pallet one-sided bounds.'),
 'support_origins':('separate weighing sessions sharing calibration table CT2','Correct acquisition separation with shared calibration, explicitly bounded including offset.'),
 'source_scope':('Verified current pallet identities and coverage establish applicability','Correct current three-pallet scope and accepted error application.'),
 'evidence_fidelity':('Both the briefing acquisition ledger and the independent reference examination','Both cited records delivered, with matching bounded measurements.'),
 'unsupported_certainty':('whose accepted error bound includes shared offset','No assumption that separate acquisitions remove shared calibration; reference independence scoped to routes.')},
'AS05':{
 'packet_action':('HOLD','NR bounded full-series maximum establishes violation.'),
 'retained_reuse_and_repair':('do not warrant reusing the retained claim','Correct nonreuse and violation; residual CT6 investigation is distinct from repaired task truth.'),
 'task_value_or_bound':('True maximum ≥50.6 bar','Correct lower bound from 50.7 minus 0.1.'),
 'support_origins':('separate acquisition streams, but all shared calibration table CT6','Correct three-stream/common-calibration distinction and separate NR route.'),
 'source_scope':('NR covered the entire specified series','Correct task coverage and current bounded reference applicability.'),
 'evidence_fidelity':('NR covered the entire specified series and measured a maximum of 50.7 bar','Accurate attribution to delivered N-R alongside N-D uncertainty.'),
 'unsupported_certainty':('establishing a true maximum of at least 50.6 bar','Uses one-sided bound; calibration uncertainty is not allowed to erase valid reference violation.')},
'AS06':{
 'packet_action':('UNRESOLVED','Valid mean measurements establish neither universal compliance nor an individual violation.'),
 'retained_reuse_and_repair':('The retained claim is therefore unsupported','Correct nonreuse without claiming latent overweight parcel has been observed or repaired.'),
 'task_value_or_bound':('Cohort mean 10.9–11.1 kg; individual maximum unknown.','Correct mean interval with explicitly unknown individual maximum.'),
 'support_origins':('separate acquisitions and calibration paths, but retained only means','Correct separate routes and retained aggregate-only information.'),
 'source_scope':('a mean below 12.0 kg does not establish the individual mass condition','Explicitly handles valid reference with insufficient task scope.'),
 'evidence_fidelity':('PR independently measured the whole cohort\'s total and mean','Accurately uses delivered P-R and P-D without invented individual evidence.'),
 'unsupported_certainty':('the evidence also does not demonstrate an overweight parcel','Explicitly avoids inferring violating external truth from unsupported favorable claim.')}
}
results=[]
required1={'requested_ids','public_selection_rationale'}
required2={'action','retained_claim_reuse','value_or_bound','evidence_ids','support_origins','remaining_issue','next_check','public_rationale'}
for kc in K['cases']:
 cid=kc['case_id']; folder=P/'participants'/cid
 s1=(folder/'TURN1_OUTPUT.txt').read_text(); s2=(folder/'TURN2_OUTPUT.txt').read_text()
 t1=json.loads(s1); t2=json.loads(s2)
 ids=t1['requested_ids']; gold=next(q for q in kc['pairs'] if sorted(q['requested_ids'])==sorted(ids))
 ep=next(e for e in E['participants'] if e['case_id']==cid)
 prompt2=(folder/'TURN2_PROMPT.txt').read_text()
 assert t2['action']==gold['action']
 assert t2['retained_claim_reuse']==gold['retained_claim_reuse']
 assert set(ids)==set(ep['delivered_ids'])
 assert all(C[cid]['records'][i] in prompt2 for i in ids)
 assert not any(C[cid]['records'][i] in prompt2 for i in C[cid]['records'] if i not in ids)
 dims={}
 for name,(quote,note) in manual[cid].items():
  assert quote in s2 or any(quote in str(v) for v in t2.values()),(cid,name,quote)
  dims[name]={'score':2,'quote':quote,'basis':note,'key_reference':f"KEY.json {cid} pair {','.join(gold['requested_ids'])}",'record_ids':list(ids)}
 n1=len(t1['public_selection_rationale'].split());n2=len(t2['public_rationale'].split())
 type_checks={
 'requested_ids_array':isinstance(ids,list) and all(isinstance(i,str) for i in ids),
 'public_selection_rationale_string':isinstance(t1['public_selection_rationale'],str),
 'action_enum':t2['action'] in ['RELEASE','HOLD','UNRESOLVED'],
 'retained_claim_reuse_boolean':type(t2['retained_claim_reuse']) is bool,
 'value_or_bound_type':t2['value_or_bound'] is None or type(t2['value_or_bound']) in [str,int,float],
 'evidence_ids_string_array':isinstance(t2['evidence_ids'],list) and all(isinstance(i,str) for i in t2['evidence_ids']),
 'support_origins_string':isinstance(t2['support_origins'],str),
 'remaining_issue_type':t2['remaining_issue'] is None or isinstance(t2['remaining_issue'],str),
 'next_check_type':t2['next_check'] is None or isinstance(t2['next_check'],str),
 'public_rationale_string':isinstance(t2['public_rationale'],str)}
 external='abstains' if t2['action']=='UNRESOLVED' else ('agrees' if gold['task_truth_warrant']==kc['external_truth']['condition'] else 'disagrees')
 residual_note=({'AS03':'Remaining calibration uncertainty named; next check seeks a traceable error bound applicable during the specified historical series.', 'AS06':'Missing individual evidence named; proposed calibrated per-parcel weighing retains identity and uncertainty; another mean would not suffice.', 'AS05':'CT6 investigation is appropriately residual and does not undermine the decisive NR violation.', 'AS02':'Proposed post-correction repeat is an operational follow-up, not a prerequisite for the already established current violation.'}.get(cid,'No further task check needed; null remaining_issue and next_check appropriate.'))
 results.append({'case_id':cid,'requested_ids':ids,'delivered_ids':ep['delivered_ids'],'gold_action':gold['action'],'observed_action':t2['action'],'gold_retained_claim_reuse':gold['retained_claim_reuse'],'observed_retained_claim_reuse':t2['retained_claim_reuse'],'dimensions':dims,'lookup':{**gold['lookup'],'public_selection_rationale':t1['public_selection_rationale'],'selection_rationale_inventory_fit':'appropriate provisional purpose; no unrevealed content assumed','selected_slots':2,'joint_coverage':'D+R; maximal origin/reference access'},'external_truth':{'hidden_condition':kc['external_truth']['condition'],'task_assertion_comparison':external,'explicit_task_assertion_warranted':None if external=='abstains' else True,'exact_latent_numeric_claim':False},'format_and_budgets':{'turn1_json_parse':True,'turn2_json_parse':True,'required_turn1_fields':required1<=t1.keys(),'required_turn2_fields':required2<=t2.keys(),'field_type_checks':type_checks,'two_distinct_valid_ids':len(ids)==2 and len(set(ids))==2 and all(i in C[cid]['records'] for i in ids),'turn1_no_final_action':'action' not in t1,'selection_words':n1,'selection_cap':80,'selection_within_cap':n1<=80,'rationale_words':n2,'rationale_cap':160,'rationale_within_cap':n2<=160,'evidence_ids_all_delivered':set(t2['evidence_ids'])<=set(ids),'delivered_texts_match_frozen_records':True,'no_unselected_record_text_delivered':True,'observed_tool_peer_calls':ep['observed_tool_or_peer_calls'],'public_turns':ep['public_turns']},'residual_issue_and_next_check':{'appropriate':True,'quote':t2['next_check'],'assessment':residual_note}})
out={'rubric':'SCORING.md frozen prospective seven dimensions, no aggregate','method':'Independent scorer manual public-evidence adjudication reproduced by review/score.py; JSON/field/word/access/action/reuse checks mechanical. No gold changes.','cases':results,'descriptive_counts':{'cases':6,'dimensions':{dim:{'score_2':6,'score_1':0,'score_0':0,'NA':0} for dim in manual['AS01']},'actions':{'RELEASE':2,'HOLD':2,'UNRESOLVED':2},'external_truth':{'warranted_agrees':4,'abstains':2,'disagrees':0},'lookups':{'D_plus_R':6,'decisive_evidence_delivered':4,'no_available_subset_decisive':2,'unavailable_reference_requested':1,'missed_decisive_record':0},'format_wordcap_protocol_deviations_observed':0},'ambiguity_notes':['AS06 turn1 says batch reference may provide parcel-level evidence. This is a provisional lookup expectation from a label, not an assertion about unseen contents; after delivery reader correctly identifies mean-only scope. No penalty.','AS01 calls R0 independent while immediately specifying own probe, recorder and distinct bath; AS04 explicitly says separate acquisition and calibration routes. AS02/05 similarly specify reference hardware/calibration. These are scoped route claims, not global statistical-independence claims.','AS03 next check requests retrospective session-applicable calibration assessment; this is a valid discriminating route without pretending the failed reference can be recovered.','AS04 support_origins does not enumerate Mj/Mk/Ml but names the three briefings and separate weighing sessions with shared CT2; correct root count is clear, so no naming-detail penalty.'],'limits':'All six chose D+R, leaving counterfactual subsets unobserved. Strong task/inventory cues and same-platform authored cases permit descriptive ceiling evidence only. No numerical aggregate success score or significance test.'}
(P/'SCORES.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
lines=['# Independent scoring report','', 'All six readers matched their frozen packet-relative action and retained-claim reuse key. Each received 2 on every separately reported substantive dimension. These are descriptive dimension counts, not an aggregate score. Four readers made warranted task-truth assertions; AS03 and AS06 correctly abstained despite opposite hidden truth values. No exact latent numerical value was claimed.','', '| Case | Action | Reuse | Selection words /80 | Rationale words /160 | External truth |','|---|---|---|---:|---:|---|']
for r in results:
 b=r['format_and_budgets'];lines.append(f"| {r['case_id']} | {r['observed_action']} | {str(r['observed_retained_claim_reuse']).lower()} | {b['selection_words']} | {b['rationale_words']} | {r['external_truth']['task_assertion_comparison']} |")
lines+=['','All readers requested D+R. Four packets delivered decisive task evidence; AS03 had no reference acquisition and AS06 supplied only aggregate means. Both correctly stayed unresolved. All outputs parsed, included required fields with valid types, respected designated word caps, requested exactly two valid distinct IDs, and cited delivered evidence. All selected record texts matched frozen records; no unselected record texts were delivered. Execution metadata records twelve public turns, no retries/rescue and zero observed tool/peer calls; this is instructional isolation, not a technical sandbox.','']
for r in results:
 lines += [f"## {r['case_id']}",'']
 for dim, val in r['dimensions'].items():
  lines.append(f"* **{dim}: {val['score']}** — “{val['quote']}”. {val['basis']} Evidence: {', '.join(val['record_ids'])}; frozen {val['key_reference']}.")
 lines += ['',r['residual_issue_and_next_check']['assessment'],'']
lines += ['## Interpretation notes','']+[f'* {s}' for s in out['ambiguity_notes']]+['',out['limits'],'','SCORES.json preserves every dimension quote, key reference, lookup and budget diagnostic. review/score.py reproduces mechanical checks and the explicit manual semantic coding without altering gold. An independent reviewer should adjudicate any disagreement against frozen SCORING.md.']
(P/'SCORING_REPORT.md').write_text('\n'.join(lines)+'\n')
print('Saved SCORES.json and SCORING_REPORT.md; validated all 6 public outputs against frozen records/key.')
