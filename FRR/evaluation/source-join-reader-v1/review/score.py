import json,pathlib,hashlib
P=pathlib.Path(__file__).resolve().parents[1]
load=lambda p:json.loads(p.read_text())
key=load(P/'KEY.json'); fixtures=load(P/'cases.json'); templates=load(P/'INSTRUCTIONS.json'); freeze=load(P/'FREEZE.json'); execution=load(P/'EXECUTION.json')
checks={name:hashlib.sha256((P/name).read_bytes()).hexdigest()==digest for name,digest in freeze['files'].items()}
assert all(checks.values()),checks
notes={
'SJ01':{
'delivered_packet_action':(2,'"action":"RELEASE"','D+C upper bound 31.15 is below 31.6.'),
'retained_reuse_and_repair':(2,'"retained_claim_reuse":true','Explicitly warrants retained condition; no exact repair invented.'),
 'task_value_or_bound':(2,'Maximum chamber temperature ≤ 31.15 °C','Correct sufficient upper bound.'),
'source_join_fidelity':(2,'30.9 + 0.18 + 0.07 = 31.15 °C','Joins V-D raw maximum and VX-4 assignment to V-C correction/error.'),
'briefing_origins':(1,'Saffron, Topaz, and Umber derive from that same acquisition','Correct Va root and lack of three measurements; omits Saffron → Topaz → Umber copy-edge detail.'),
'calibration_and_role_scope':(2,'The acquired raw range, 30.4–30.9 °C, falls within VX-4’s calibration range.','Explicit raw-domain and three-sample scope; no unseen reference claims.'),
'evidence_fidelity':(2,'"evidence_ids":["V-D","V-C"]','Both delivered records used for their actual content.'),
'unsupported_certainty':(2,'Applying the correction and maximum positive residual gives an upper bound','No exact physical-center claim; source independence statement limited to shared acquisition.'),
'residual_issue_and_next_check':(2,'"remaining_issue":null,"next_check":null','Task is decisive; no further task check required.')},
'SJ02':{
'delivered_packet_action':(2,'"action":"UNRESOLVED"','Selected D+C interval straddles 6.4; latent violation cannot replace warrant.'),
'retained_reuse_and_repair':(2,'neither RELEASE nor HOLD is warranted, and the retained claim cannot be reused','Correct withholding without asserting verified falsity.'),
 'task_value_or_bound':(2,'Maximum physical vibration is bounded by 5.8–6.7 mm/s.','Correct two-sided maximum interval.'),
'source_join_fidelity':(2,'Applying the +0.25 correction and ±0.45 residual bound','Joins current Wa/WK-8 raw maximum to its row with correct sign.'),
'briefing_origins':(1,'All three reports derive from the single acquisition Wa on WK-8','Correct sole root and shared evidence; omits Amber → Cobalt → Ivory copy edges.'),
'calibration_and_role_scope':(2,"All readings fall within W-C's calibration range.",'Full WS scope and applicable bounded residual; correctly retains straddle.'),
'evidence_fidelity':(2,'"evidence_ids":["W-D","W-C"]','Uses delivered data only; does not assert unseen reference result.'),
'unsupported_certainty':(2,'establishing neither compliance nor violation','No unsupported definite truth or exact value.'),
'residual_issue_and_next_check':(2,'Obtain a tighter calibrated measurement or residual bound for WK-8 over the specified samples.','Task-specific uncertainty reduction rather than more copies; valid alternative to scoped reference.')},
'SJ03':{
'delivered_packet_action':(2,'"action":"RELEASE"','Selected D+C upper bound 71.73 below 72.3.'),
'retained_reuse_and_repair':(2,'warranting release and reuse of the retained claim','Correct warranted reuse; no false retained claim repair asserted.'),
 'task_value_or_bound':(2,'Maximum core temperature ≤ 71.73 °C','Correct sufficient physical upper bound.'),
'source_join_fidelity':(2,'71.4 °C on XB-5a, XB-5b, and XB-5c','Actual acquisition-channel keys joined to shared correction/error row.'),
'briefing_origins':(2,'Three physical channels independently acquired complete XS readings; their calibrations share certificate XCC. Each acquisition supplies one briefing.','Correct separate acquisition/one-to-one export structure; names of every root/briefing need not be restated.'),
'calibration_and_role_scope':(2,'their calibrations share certificate XCC','Keeps shared certificate explicit; uses full +0.09 bound without independence reduction.'),
'evidence_fidelity':(2,'"evidence_ids":["X-D","X-C"]','All claimed keys, extrema, coverage and shared certificate delivered.'),
'unsupported_certainty':(2,'giving a maximum upper bound of 71.73 °C','Independent acquisition language is scoped by physical channels and shared certificate; no statistical error independence asserted.'),
'residual_issue_and_next_check':(2,'"remaining_issue":null,"next_check":null','Decisive task bound; no new check required.')},
'SJ04':{
'delivered_packet_action':(2,'"action":"HOLD"','Scoped reference lower bound 23.90 exceeds 23.6.'),
'retained_reuse_and_repair':(2,'The condition is violated, so the retained claim cannot be reused.','Correct refutation from delivered task evidence; no invented exact repair.'),
 'task_value_or_bound':(2,'YS maximum is between 23.90 and 23.98 bar.','Correct bounded physical task maximum.'),
'source_join_fidelity':(2,'Y-M assigns Yr17 to Hydraulic rack Yarrowgate and all three aligned YS samples','Exact current capture join; preceding Yr28 not misapplied.'),
'briefing_origins':('NA','Yr17 uses the reference route YRP → YRR → YRC','No claim about briefing root count or export edges; D unavailable. Required support_origins field is populated with the observed reference route.'),
'calibration_and_role_scope':(2,'independently of the acquisitions and channels named in Y-M','Scoped route separation is warranted by M; no statistical/global independence claim. Current task alignment and reference error preserved.'),
'evidence_fidelity':(2,'"evidence_ids":["Y-M","Y-R"]','Only delivered scope/reference evidence cited.'),
'unsupported_certainty':(2,'Thus the physical maximum is at least 23.90 bar','Correct lower bound and warranted violation; does not pretend briefing ancestry known.'),
'residual_issue_and_next_check':(2,'Investigate the briefing reports’ discrepancy and verify manifold pressure after corrective action.','Task already decided; optional operational follow-up does not claim a cause or verified correction.')}
}
rows=[]
for fixture,kg in zip(fixtures,key['cases']):
 cid=fixture['id']; folder=P/'participants'/cid
 out=[load(folder/f'TURN{i}_OUTPUT.txt') for i in range(1,4)]
 selected=[x['requested_id'] for x in out[:2]]
 gold=next(x for x in kg['sets'] if x['selected_ids']==sorted(selected))
 path=next(x for x in kg['ordered_paths'] if [x['first_id'],x['second_id']]==selected)
 rationale_words=[len(x['public_selection_rationale' if i<2 else 'public_rationale'].split()) for i,x in enumerate(out)]
 prompts=[(folder/f'TURN{i}_PROMPT.txt').read_text() for i in range(1,4)]
 expected=[templates['turn1_prefix']+fixture['initial'],templates['turn2_prefix']+selected[0]+':\n'+fixture['records'][selected[0]],templates['turn3_prefix']+selected[1]+':\n'+fixture['records'][selected[1]]]
 prompt_matches=[a.rstrip('\n')==b.rstrip('\n') for a,b in zip(prompts,expected)]
 required={'action','retained_claim_reuse','value_or_bound','evidence_ids','support_origins','remaining_issue','next_check','public_rationale'}
 types_ok=isinstance(out[2]['retained_claim_reuse'],bool) and isinstance(out[2]['evidence_ids'],list) and isinstance(out[2]['support_origins'],str) and all(out[2][f] is None or isinstance(out[2][f],str) for f in ['remaining_issue','next_check'])
 intermediate=[dict(turn=1,quote=out[0]['public_selection_rationale'],judgment='Prospective selection purpose; no final task decision or unseen factual assertion. Acquisition ledger request fits inventory.' if cid!='SJ04' else 'Prospective expectation overstates M: scope map does not identify which primary channel or calibration contract applies. It does identify current capture/sample scope; this is an imprecise request rationale, not a claim that missing measurements were observed.',material_error=False),dict(turn=2,quote=out[1]['public_selection_rationale'],judgment='Correct delivered-ledger facts and a valid conditional need for C; no early task decision.' if cid not in ['SJ03','SJ04'] else 'Independent raw readings means distinct physical acquisition here; no statistical calibration independence asserted. C requested before task decision.' if cid=='SJ03' else 'Correctly identifies delivered M capture/current scope; requests missing R measurement/error contract before deciding.',material_error=False)]
 row=dict(case_id=cid,selected_order=selected,final_action=out[2]['action'],gold_action=gold['action'],dimensions={name:dict(score=v[0],quote=v[1],judgment=v[2],key_reference=f"KEY.json:{cid}:{','.join(sorted(selected))}; "+'/'.join(selected)) for name,v in notes[cid].items()},intermediate_public_claims=intermediate,lookup=dict(cost=2,delivered_ids=selected,completed_join=gold['completed_join'],decisive_second_choices_given_first=path['decisive_second_choices_given_first'],missed_achievable_decisive_second_choice=path['missed_achievable_decisive_second_choice'],one_remaining_slot_can_decide_after_first=path['one_remaining_slot_can_decide_after_first'],missed_task_decisive_sets=gold['lookup']['missed_task_decisive_sets'],judgment='D first cannot be made decisive with one remaining slot in this fixture; C was a reasonable candidate before its hidden straddle was delivered. R+M was an unselected achievable pair. This selection limitation is separate from correct final warrant.' if cid=='SJ02' else 'Selected complement completes a decisive join; unselected alternative route is not a task-access failure.'),external_truth=dict(condition=kg['external_truth']['condition'],comparison='abstains' if out[2]['action']=='UNRESOLVED' else 'agrees',quote=out[2]['action'],warranted=True),protocol_format_caps=dict(parseable_json=[True]*3,required_final_fields_present=required<=out[2].keys(),field_types_valid=types_ok,one_valid_string_id_per_request=all(isinstance(i,str) and i in fixture['records'] for i in selected),distinct_requests=len(set(selected))==2,no_final_decision_before_turn3=all('action' not in x for x in out[:2]),rationale_words=rationale_words,caps=[60,60,180],caps_pass=all(n<=cap for n,cap in zip(rationale_words,[60,60,180])),prompt_matches_frozen_rendering=prompt_matches,observed_tool_peer_calls=0,quote=' | '.join(json.dumps(x,ensure_ascii=False) for x in out[:2]),access_limit='Execution log reports zero observed calls; instructional isolation does not technically prove absence of unobserved access.'),resource_observability=dict(selected_record_utf8_bytes=sum(len(fixture['records'][i].encode()) for i in selected),time_tokens_compute='Unavailable; not fabricated.'))
 assert out[2]['action']==gold['action'] and out[2]['retained_claim_reuse']==gold['retained_claim_reuse']
 assert all(prompt_matches) and row['protocol_format_caps']['caps_pass'] and types_ok
 rows.append(row)
result=dict(scoring_basis='Frozen KEY.json and SCORING.md unchanged. Public content only; each dimension separate, no aggregate score.',frozen_file_checks=checks,execution_source='EXECUTION.json at contact root; four contexts, twelve turns, zero retries/rescues and observed tool/peer calls per log.',case_scores=rows,limitations=['Four authored fictional development cases; no statistical or causal inference.','Three D+C selections do not test those readers on actual reference capture joins.','Appropriate SJ02 uncertainty is not truth error; missed alternative pair is not a false final decision.','Independent acquisition/route wording is read in local stated scope; no private confidence inferred.'])
(P/'SCORES.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'frozen_files_verified':len(checks),'cases':[{'id':r['case_id'],'words':r['protocol_format_caps']['rationale_words'],'prompt_matches':r['protocol_format_caps']['prompt_matches_frozen_rendering']} for r in rows]},indent=2))
