from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
def main():
    raw=[json.loads(l) for l in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()];keys={k['id']:k for k in json.loads((P/'KEYS.json').read_text())};scores=[]
    for r in raw:
        text=r['text'].strip();assert text in ['Yes','No'],'Unexpected full response requires further semantic review'
        label=text.upper();key=keys[r['run_id']]['expected']
        scores.append({'id':r['run_id'],'record_id':r['record_id'],'polarity':r['arm'],'expected':key,'text':r['text'],'explicit_label':label,'answer_match':label==key,'strict_format':text in ['YES','NO'],'case_insensitive_format':True,'coordinator_note':'Bare label matches the frozen presence key; this does not certify its reasoning path.' if label==key else 'Bare label contradicts the explicit count-present/absent state of the source.'})
    pairs=[]
    for rid in [r['id'] for r in json.loads((P/'RECORDS.json').read_text())]:
        a=next(s for s in scores if s['record_id']==rid and s['polarity']=='recorded');b=next(s for s in scores if s['record_id']==rid and s['polarity']=='unrecorded')
        pairs.append({'record_id':rid,'recorded_label':a['explicit_label'],'unrecorded_label':b['explicit_label'],'complement_consistent':a['explicit_label']!=b['explicit_label'],'both_answers_correct':a['answer_match'] and b['answer_match']})
    summary={'calls':16,'semantic_matches':sum(s['answer_match'] for s in scores),'by_polarity':{p:{'n':8,'matches':sum(s['answer_match'] for s in scores if s['polarity']==p)} for p in ['recorded','unrecorded']},'pairs':pairs,'fully_correct_pairs':sum(p['both_answers_correct'] for p in pairs),'complement_consistent_pairs':sum(p['complement_consistent'] for p in pairs),'same_label_inconsistent_pairs':sum(not p['complement_consistent'] for p in pairs),'strict_format':sum(s['strict_format'] for s in scores),'case_insensitive_format':16,'stops':{s:sum(r['stop']==s for r in raw) for s in ['eos','token_limit']},'input_tokens':sum(r['input_tokens'] for r in raw),'output_tokens':sum(r['output_tokens'] for r in raw),'inference_seconds_excluding_serialization':sum(r['inference_seconds_excluding_serialization'] for r in raw),'serialization_seconds':sum(r['serialization_seconds'] for r in raw),'cache_bytes':sum(r['cache_artifact']['bytes'] for r in raw),'scope':'coordinator whole-response scoring; bare-label matches are not source-reasoning-path certificates; independent contexts not one joined report'}
    (P/'SCORES.json').write_text(json.dumps(scores,indent=2)+'\n');(P/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
