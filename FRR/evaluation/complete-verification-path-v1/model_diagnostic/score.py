from pathlib import Path
import json
P=Path(__file__).resolve().parent
def main():
    raw=[json.loads(l) for l in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()];keys={r['id']:r for r in json.loads((P/'KEYS.json').read_text())};scores=[]
    for r in raw:
        assert r['text']=='Yes','Unexpected response requires further whole-response review'
        k=keys[r['run_id']];good=k['expected']=='YES'
        scores.append({'id':r['run_id'],'record_id':r['record_id'],'expected':k['expected'],'text':r['text'],'semantic_label_match':good,'whole_response_supported':good,'strict_format':False,'case_insensitive_format':True,'coordinator_note':'Correct bare label; no source reasoning or arithmetic path was shown.' if good else 'Unsupported YES: '+('calculation should withhold for '+k['path_stage'] if k['expected']=='WITHHOLD' else 'valid variance exceeds the criterion')})
    summary={'calls':10,'semantic_label_matches':sum(s['semantic_label_match'] for s in scores),'whole_response_matches':sum(s['whole_response_supported'] for s in scores),'constant_yes_baseline_matches':4,'model_answers':'allYES','numeric_tasks':{'n':6,'label_matches':4},'missing_or_domain_tasks':{'n':4,'label_matches':0},'strict_format':0,'case_insensitive_format':10,'stops':{st:sum(r['stop']==st for r in raw) for st in ['eos','token_limit']},'input_tokens':sum(r['input_tokens'] for r in raw),'output_tokens':sum(r['output_tokens'] for r in raw),'inference_seconds_excluding_serialization':sum(r['inference_seconds_excluding_serialization'] for r in raw),'serialization_seconds':sum(r['serialization_seconds'] for r in raw),'new_cache_bytes':sum(r['cache_artifact']['bytes'] for r in raw),'scope':'untrusted direct model candidate answers, no witness production or input authorization; coordinator review, not independent/masked; no model improvement established'}
    (P/'SCORES.json').write_text(json.dumps(scores,indent=2)+'\n');(P/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
