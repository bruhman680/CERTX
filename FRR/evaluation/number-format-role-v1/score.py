"""Post-result whole-response review; all responses use the same explicit supported template."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent

def main():
    raw=[json.loads(l) for l in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()]
    keys={x['id']:x for x in json.loads((P/'KEYS.json').read_text())};cases={x['id']:x for x in json.loads((P/'CASES.json').read_text())}
    scores=[]
    for r in raw:
        key=keys[r['run_id']];c=cases[r['run_id']]
        expected=f'The given record documents {key["expected"]} independently sampled soils.'
        assert r['text']==expected,'Unexpected response requires new whole-response review'
        scores.append({'id':r['run_id'],'record_id':r['record_id'],'target_format':c['target_format'],'observation_format':c['observation_format'],'expected':key['expected'],'text':r['text'],'answer_match':True,'wrong_foil_answer':False,'strict_format':bool(re.fullmatch(r'\d+|UNKNOWN',r['text'].strip())),'review':'coordinator examined whole response; explicit correct target with no added false claim'})
    summary={'calls':len(raw),'semantic_matches':sum(s['answer_match'] for s in scores),'strict_format':sum(s['strict_format'] for s in scores),'by_rendering':{arm:{'n':sum(cases[r['run_id']]['arm']==arm for r in raw),'matches':sum(s['answer_match'] for s in scores if s['target_format']+'_'+s['observation_format']==arm)} for arm in ['digit_digit','word_digit','digit_word','word_word']},'foil_answers':0,'all_four_outputs_identical_within_each_base_record':all(len({r['text'] for r in raw if r['record_id']==b})==1 for b in {r['record_id'] for r in raw}),'stops':{s:sum(r['stop']==s for r in raw) for s in ['eos','token_limit']},'input_tokens':sum(r['input_tokens'] for r in raw),'output_tokens':sum(r['output_tokens'] for r in raw),'inference_seconds_excluding_serialization':sum(r['inference_seconds_excluding_serialization'] for r in raw),'serialization_seconds':sum(r['serialization_seconds'] for r in raw),'cache_bytes':sum(r['cache_artifact']['bytes'] for r in raw),'scope':'Four authored base records,16form variants; no difference detected in generated correctness here, not a proof of global invariance or internal-state equality.'}
    (P/'SCORES.json').write_text(json.dumps(scores,indent=2)+'\n');(P/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
