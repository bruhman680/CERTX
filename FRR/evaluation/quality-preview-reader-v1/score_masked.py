import json,hashlib
from pathlib import Path
p=Path(__file__).parent
src=json.loads((p/'SCORER_INPUT.json').read_text()); key=json.loads((p/'KEY.json').read_text())
dims=['delivered_packet_action','retained_reuse_and_repair','task_value_or_bound','source_join_fidelity','briefing_origins','calibration_and_role_scope','evidence_fidelity','unsupported_certainty','residual_issue_and_next_check']
# Public-output manual judgments, deposited before assignment inspection.
rows=[]
for q in src['readers']:
 rid=q['reader_id'];f=q['final_output'];ids=list(q['delivered_records']);cg=key['cases'][q['case_id']];sg=cg['states']['+'.join(ids)];path=cg['ordered_paths'][' -> '.join(ids)]
 values=dict.fromkeys(dims,2); notes={}
 quotes={
 'delivered_packet_action':f['action'],
 'retained_reuse_and_repair':str(f['retained_claim_reuse']).lower()+'; '+f['public_rationale'],
 'task_value_or_bound':f['value_or_bound'],
 'source_join_fidelity':f['support_origins'],
 'briefing_origins':f['support_origins'],
 'calibration_and_role_scope':f['public_rationale'],
 'evidence_fidelity':f['support_origins'],
 'unsupported_certainty':f['value_or_bound'],
 'residual_issue_and_next_check':f['next_check'] if f['next_check'] else 'remaining_issue=null; next_check=null'}
 # None explicitly checks that both raw extrema are within the calibration range.
 values['calibration_and_role_scope']=1
 notes['calibration_and_role_scope']='Correct sampled scope, correction and residual bound are stated; raw-range applicability is not explicitly checked. This omission is incomplete handling, not a wrong bound.'
 if rid in ['R01','R03']:
  for dim in ['source_join_fidelity','calibration_and_role_scope','evidence_fidelity']:
   values[dim]=0
   quotes[dim]=f['remaining_issue']
   notes[dim]='Incorrectly adds a missing housing/channel scope premise. Initial defines OS as the complete housing-vibration task; D identifies the same check/object and assigns complete OS acquisition Oa to physical channel OK-6. C joins that exact channel. The primary route is complete but straddling, not unassigned. The correct action/bound are scored separately.'
  values['residual_issue_and_next_check']=1
  notes['residual_issue_and_next_check']='Correctly identifies the physical straddle and asks for tighter warranted measurement bounds, but also requests an already-established housing/channel assignment.'
 if rid=='R06':
  values['residual_issue_and_next_check']=1
  notes['residual_issue_and_next_check']='Tightening the 15.1-bar raw sample can establish a violation, but a compliant result for that sample alone does not establish compliance of all PS: the third sample remains [14.9,15.8] bar, crossing 15.7, and residuals may vary by sample. The next check is potentially discriminating but incomplete for resolving the full maximum in both directions.'
 if rid in ['R02','R05']:
  notes['residual_issue_and_next_check']='Decisive RELEASE needs no next check.'
 if rid=='R04':notes['residual_issue_and_next_check']='Tighter warranted bounds or independent calibrated measurements explicitly for the task samples is an adequate prospective next check; no unseen reference numbers are required.'
 if rid=='R06':notes['evidence_fidelity']='PCC is a certificate identifier explicitly embedded in delivered P-C, not an extra lookup or undelivered evidence. All numeric per-sample intervals match P-D/P-C.'
 scores={d:{'score':values[d],'quote':quotes[d],'gold_reference':q['case_id']+'/'+ '+'.join(ids),'reason':notes.get(d,'Public claim agrees with the frozen delivered-packet gold and record content.')} for d in dims}
 caps={f'turn{i}':len(q[f'turn{i}_output']['public_selection_rationale'].split()) for i in (1,2)};caps['turn3']=len(f['public_rationale'].split())
 expected={'action','retained_claim_reuse','value_or_bound','evidence_ids','support_origins','remaining_issue','next_check','public_rationale'}
 rows.append({'reader_id':rid,'case_id':q['case_id'],'selected_order':ids,'gold_action':sg['action'],'observed_action':f['action'],'scores':scores,'diagnostics':{'external_truth':'agrees' if f['action']=='RELEASE' else 'abstains','lookup_cost':2,'completed_routes':sg['complete_routes'],'reachable_decisive_second_ids':path['reachable_decisive_second_ids'],'missed_available_decisive_second':path['missed_available_decisive_second'],'initial_choice_left_decisive_second':bool(path['reachable_decisive_second_ids']),'selection_judgment':'D then matching C is prospective-plausible from inventory/current D; no unseen calibration numbers are required. QP02 D-first leaves no decisive second record, separately from its correct final UNRESOLVED.','forecast_use':q['turn1_output']['public_selection_rationale'],'forecast_treated_as_authoritative':False,'delivered_record_bytes_match_cases':all(v==next(c for c in json.loads((p/'cases.json').read_text()) if c['id']==q['case_id'])['records'][k] for k,v in q['delivered_records'].items()),'designated_rationale_word_counts':caps,'caps_pass':caps['turn1']<=60 and caps['turn2']<=60 and caps['turn3']<=180,'structured_output_fields_pass':set(f)==expected,'distinct_valid_requests_pass':len(set(ids))==2 and [q['turn1_output']['requested_id'],q['turn2_output']['requested_id']]==ids,'evidence_ids_note':'PCC is observed within P-C and does not consume an extra slot.' if rid=='R06' else 'All listed evidence IDs are the two delivered records.'}})
out={'masking':'Scored only neutral SCORER_INPUT, frozen KEY/SCORING and literal cases. No ASSIGNMENT or participant prompts inspected before this deposit. Guidance blocks were seen during prospective preparation; no neutral-ID mapping was seen. Shared-workspace instructional masking, not technical blinding.','no_aggregate':True,'gold_unchanged':True,'input_sha256':hashlib.sha256((p/'SCORER_INPUT.json').read_bytes()).hexdigest(),'key_sha256':hashlib.sha256((p/'KEY.json').read_bytes()).hexdigest(),'dimensions':dims,'readers':rows}
(p/'SCORES_MASKED.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('Deposited six readers with nine separate dimensions; no aggregate.')
