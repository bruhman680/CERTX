from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
def main():
    raw=[json.loads(l) for l in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()];keys={k['id']:k for k in json.loads((P/'KEYS.json').read_text())};scores=[]
    for r in raw:
        key=keys[r['run_id']];hasfoil=key['foil_value'] is not None
        scores.append({'id':r['run_id'],'arm':r['arm'],'expected':'UNKNOWN','text':r['text'],'answer_match':False,'explicit_numeric_answer':key['foil_value'] if hasfoil else 12,'copies_foil_value':hasfoil,'strict_format':r['text'].strip()=='UNKNOWN','coordinator_note':'Unrecorded soil count replaced by supplied observation quantity.' if hasfoil else 'Invents12soils and also says the count is absent; contradiction is not a supported unknown answer.'})
    previous={r['run_id']:r for r in map(json.loads,(P.parent/'frame-generalization-missing-v1/RAW_OUTPUTS.jsonl').read_text().splitlines())};repeats=[]
    for m,rid in [(9,'F5'),(18,'F6')]:
        old=previous['FG_'+rid+'_there_are'];new=next(r for r in raw if r['run_id']==f'MF_{m}_digit')
        assert old['input_token_ids']==new['input_token_ids'] and old['generated_token_ids']==new['generated_token_ids']
        repeats.append({'old_id':old['run_id'],'new_id':new['run_id'],'same_input_and_output_token_ids':True})
    summary={'calls':9,'semantic_matches':0,'by_condition':{'digit':{'n':4,'matches':0,'foil_answers':4},'word':{'n':4,'matches':0,'foil_answers':4},'no_foil':{'n':1,'matches':0,'invented_answer':12}},'exposed_repeats':repeats,'strict_format':0,'stops':{s:sum(r['stop']==s for r in raw) for s in ['eos','token_limit']},'input_tokens':sum(r['input_tokens'] for r in raw),'output_tokens':sum(r['output_tokens'] for r in raw),'inference_seconds_excluding_serialization':sum(r['inference_seconds_excluding_serialization'] for r in raw),'serialization_seconds':sum(r['serialization_seconds'] for r in raw),'cache_bytes':sum(r['cache_artifact']['bytes'] for r in raw),'review':'coordinator whole-response review; all9explicit unsupported numerical answers, not independent/masked review'}
    (P/'SCORES.json').write_text(json.dumps(scores,indent=2)+'\n');(P/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
