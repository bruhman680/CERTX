"""Post-result explicit coordinator judgments; frozen keys are unchanged."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
J={
'C1_G1_full':('unresolved','Source prefix copied, cap reached before a soil-count answer.'),
'C1_G2_full':('unresolved','Same source prefix, no count answer before cap.'),
'C1_G3_full':('unresolved','Same source prefix, no count answer before cap.'),
'C1_G4_full':('wrong','Invents64independentsoils although grouping is missing.'),
'C1_R1_full':('correct','States both numerical efficacies supplied, true.'),
'C1_R2_full':('wrong','States both supplied when neither is supplied.'),
'C1_R3_full':('correct','Zero effectiveness values are supplied values.'),
'C1_R4_full':('wrong','States both supplied when neither is supplied.'),
'C1_G1_clause':('wrong','Denies soil-count information while quoting64independentsoils; contradictory to the requested count.'),
'C1_G2_clause':('wrong','Denies any independent soil draws despite4independentsoils.'),
'C1_G3_clause':('correct','States1independentsoildraw and64observations in their correct roles.'),
'C1_G4_clause':('qualified_target_match','Explicitly says number not recorded, but extra no-observations-that-share-a-soil wording is ambiguous between absence of documentation and absence of sharing. Conservative whole-response score withholds; target-only sensitivity counts it.'),
'C1_R1_clause':('correct','Both supplied, as source states.'),
'C1_R2_clause':('correct','Neither supplied; correctly recognizes absent values.'),
'C1_R3_clause':('correct','Both zero-valued efficacies correctly treated as supplied.'),
'C1_R4_clause':('correct','Neither supplied; exact same selected input as R2, not independent evidence.'),
'C2_G1_reworded':('correct','States64independentlysampledsoils.'),
'C2_G2_reworded':('correct','States4independentsoils and16observations per soil in correct roles.'),
'C2_G3_reworded':('correct','States1soil with64observations in correct roles.'),
'C2_G4_reworded':('qualified_target_match','Count explicitly unrecorded; extra no-documented-sharing clause has the same interpretation sensitivity as C1_G4. Conservative whole-response score withholds; target-only sensitivity counts it.'),
'C2_R1_reworded':('wrong','Denies supplied numbers and contradicts itself; both values are present.'),
'C2_R2_reworded':('correct','Denies numbers supplied, as source states.'),
'C2_R3_reworded':('wrong','Denies supplied numerical values despite both being0.'),
'C2_R4_reworded':('correct','Denies numbers supplied; duplicate R2 selected input.'),
'C3_N1_new_clause':('wrong','Copies32soil/2observations facts then explicitly answers2, the wrong role.'),
'C3_N2_new_clause':('wrong','AnswersUNKNOWN despite explicit eight independent soil draws.'),
'C3_N3_new_clause':('wrong','Answers32draws instead of2, swapping observations per soil into the count.'),
'C3_N4_new_clause':('correct','States independent-soil count absent; no invented numerical count.'),
'C3_N5_new_clause':('correct','Correctly states both numerical values supplied.'),
'C3_N6_new_clause':('wrong','Claims both supplied when only qA is supplied.'),
'C3_N7_new_clause':('correct','Both zero values correctly recognized as supplied.'),
'C3_N8_new_clause':('correct','Neither numerical value recorded, matching source.')}
def main():
    rows=[json.loads(l) for l in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()]
    cases={r['id']:r for r in json.loads((P/'CASES.json').read_text())}
    keys={r['id']:r for r in json.loads((P/'KEYS.json').read_text())}
    assert len(rows)==32 and set(J)==set(cases)==set(keys)=={r['run_id'] for r in rows}
    scores=[]
    for r in rows:
        ident=r['run_id'];status,note=J[ident];k=keys[ident];c=cases[ident]
        fmt=bool(re.fullmatch(r'\d+|UNKNOWN',r['text'].strip())) if c['family']=='grouping' else r['text'].strip() in ('PROVIDED','MISSING')
        scores.append({'id':ident,'record_id':r['record_id'],'family':r['family'],'cycle':c['cycle'],'arm':c['arm'],'expected':k['expected'],'text':r['text'],'status':status,'unambiguous_whole_response_match':status=='correct','target_only_sensitivity_match':status in ('correct','qualified_target_match'),'strict_format':fmt,'stop':r['stop'],'coordinator_note':note})
    groups={}
    for cycle,arm in [('C1','full'),('C1','clause'),('C2','clause_reworded_question'),('C3','new_clause_original_question')]:
        a=[r for r in rows if cases[r['run_id']]['cycle']==cycle and cases[r['run_id']]['arm']==arm]
        b=[s for s in scores if s['cycle']==cycle and s['arm']==arm]
        groups[cycle+'_'+arm]={'n':len(a),'distinct_prompts':len({r['rendered_prompt'] for r in a}),'unambiguous_matches':sum(s['unambiguous_whole_response_match'] for s in b),'target_only_sensitivity_matches':sum(s['target_only_sensitivity_match'] for s in b),'by_family':{f:{'n':sum(s['family']==f for s in b),'unambiguous_matches':sum(s['unambiguous_whole_response_match'] for s in b if s['family']==f),'target_only_matches':sum(s['target_only_sensitivity_match'] for s in b if s['family']==f)} for f in ('grouping','reset')},'input_tokens':sum(r['input_tokens'] for r in a),'output_tokens':sum(r['output_tokens'] for r in a),'inference_seconds':sum(r['inference_seconds_excluding_serialization'] for r in a),'token_limit':sum(r['stop']=='token_limit' for r in a)}
    old={r['run_id']:r for r in map(json.loads,(P.parent/'soil-design-reader-v1/RAW_OUTPUTS.jsonl').read_text().splitlines())}
    repeats=[]
    for r in rows:
        c=cases[r['run_id']]
        if c['cycle']=='C1' and c['arm']=='full':
            o=old[c['record_id']+'_reading'];repeats.append({'record':c['record_id'],'same_input_ids':r['input_token_ids']==o['input_token_ids'],'same_generated_ids':r['generated_token_ids']==o['generated_token_ids'],'same_text':r['text']==o['text']})
    assert all(r['same_input_ids'] and r['same_generated_ids'] and r['same_text'] for r in repeats)
    summary={'generations':32,'groups':groups,'status_totals':{s:sum(x['status']==s for x in scores) for s in ('correct','wrong','qualified_target_match','unresolved')},'strict_format_matches':sum(s['strict_format'] for s in scores),'old_full_arm_repeats':repeats,'input_tokens':sum(r['input_tokens'] for r in rows),'output_tokens':sum(r['output_tokens'] for r in rows),'inference_seconds_excluding_serialization':sum(r['inference_seconds_excluding_serialization'] for r in rows),'serialization_seconds':sum(r['serialization_seconds'] for r in rows),'new_cache_bytes':sum(r['cache_artifact']['bytes'] for r in rows),'stops':{s:sum(r['stop']==s for r in rows) for s in ('eos','token_limit')},'scope':'Coordinator whole-response judgments, not independent or masked; exposed records; duplicate selected R2/R4 prompts counted as slots with distinct-prompt totals shown.'}
    (P/'SCORES.json').write_text(json.dumps(scores,indent=2)+'\n')
    (P/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
