from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
ANS={'SF_B1_passive_digit':2,'SF_B1_passive_word':2,'SF_B1_there_are_digit':32,'SF_B1_there_are_word':32,'SF_B2_passive_digit':32,'SF_B2_passive_word':12,'SF_B2_there_are_digit':2,'SF_B2_there_are_word':2}
def main():
    raw=[json.loads(l) for l in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()]
    cases={c['id']:c for c in json.loads((P/'CASES.json').read_text())};keys={c['id']:c for c in json.loads((P/'KEYS.json').read_text())}
    scores=[]
    for r in raw:
        c=cases[r['run_id']];k=keys[r['run_id']];answer=ANS[r['run_id']];good=answer==int(k['expected'])
        scores.append({'id':r['run_id'],'record_id':r['record_id'],'frame':c['source_frame'],'target_format':c['target_format'],'text':r['text'],'expected':k['expected'],'explicit_answer':answer,'answer_match':good,'foil_answer':answer==k['foil_value'],'other_wrong_number':not good and answer!=k['foil_value'],'strict_format':bool(re.fullmatch(r'\d+|UNKNOWN',r['text'].strip())),'coordinator_note':'Whole sentence states the correct soil count with no extra false assertion.' if good else ('Observation count substituted for soil count.' if answer==k['foil_value'] else 'Invents12soils, neither supplied target nor foil.')})
    prior=[json.loads(l) for l in (P.parent/'reader-wording-cross-v1/RAW_OUTPUTS.jsonl').read_text().splitlines()]
    old=next(r for r in prior if r['run_id']=='WC_N1_reworded');new=next(r for r in raw if r['run_id']=='SF_B1_passive_word')
    repeat={'old_id':old['run_id'],'new_id':new['run_id'],'same_input_token_ids':old['input_token_ids']==new['input_token_ids'],'same_generated_token_ids':old['generated_token_ids']==new['generated_token_ids']}
    assert repeat['same_input_token_ids'] and repeat['same_generated_token_ids']
    summary={'calls':8,'semantic_matches':sum(s['answer_match'] for s in scores),'by_frame':{f:{'n':sum(s['frame']==f for s in scores),'matches':sum(s['answer_match'] for s in scores if s['frame']==f)} for f in ['passive','there_are']},'by_target_format':{f:{'n':sum(s['target_format']==f for s in scores),'matches':sum(s['answer_match'] for s in scores if s['target_format']==f)} for f in ['digit','word']},'foil_answers':sum(s['foil_answer'] for s in scores),'other_wrong_numbers':sum(s['other_wrong_number'] for s in scores),'strict_format':sum(s['strict_format'] for s in scores),'exposed_repeat':repeat,'stops':{s:sum(r['stop']==s for r in raw) for s in ['eos','token_limit']},'input_tokens':sum(r['input_tokens'] for r in raw),'output_tokens':sum(r['output_tokens'] for r in raw),'inference_seconds_excluding_serialization':sum(r['inference_seconds_excluding_serialization'] for r in raw),'serialization_seconds':sum(r['serialization_seconds'] for r in raw),'cache_bytes':sum(r['cache_artifact']['bytes'] for r in raw),'scope':'Coordinator whole-response review. Two base value pairs; exposed repeat not independent confirmation. Frame package changes several surface features; not an internal mechanism proof or universal rewrite repair.'}
    (P/'SCORES.json').write_text(json.dumps(scores,indent=2)+'\n');(P/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
