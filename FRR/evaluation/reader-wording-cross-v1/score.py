from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
J={
'WC_N1_reworded':(False,'2observations per soil substituted for32soils.'),
'WC_N2_reworded':(True,'8independent soil draws stated; target and observations share the value8 so this alone cannot establish role discrimination.'),
'WC_N3_reworded':(False,'32distinctsoils contradicts the source2; later mentioning2 does not repair the false32claim.'),
'WC_N4_reworded':(True,'Explicit missing count, no invented number.'),
'WC_N5_reworded':(False,'Denies both supplied nonzero values.'),
'WC_N6_reworded':(True,'Denies a number for each variable when onlyqAprovided.'),
'WC_N7_reworded':(False,'Denies both supplied zero values.'),
'WC_N8_reworded':(True,'Correctly denies values for both variables.')}
def main():
    raw=[json.loads(l) for l in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()]
    keys={x['id']:x for x in json.loads((P/'KEYS.json').read_text())}
    basis=json.loads((P/'BASIS.json').read_text());pairs={x['id']:x for x in basis['pairs']}
    old={x['id']:x for x in json.loads((P.parent/'clause-reader-three-cycle-v1/SCORES.json').read_text())}
    scores=[]
    for r in raw:
        good,note=J[r['run_id']]; b=old[pairs[r['run_id']]['baseline_id']]
        scores.append({'id':r['run_id'],'record_id':r['record_id'],'family':r['family'],'expected':keys[r['run_id']]['expected'],'text':r['text'],'answer_match':good,'baseline_match':b['unambiguous_whole_response_match'],'transition':('correct' if b['unambiguous_whole_response_match'] else 'wrong')+'->'+('correct' if good else 'wrong'),'strict_format':r['text'].strip() in ('PROVIDED','MISSING','UNKNOWN') or bool(re.fullmatch(r'\d+',r['text'].strip())),'coordinator_note':note})
    summary={'calls':len(raw),'reworded_matches':sum(x['answer_match'] for x in scores),'saved_original_matches':sum(x['baseline_match'] for x in scores),'by_family':{f:{'n':sum(x['family']==f for x in scores),'original':sum(x['baseline_match'] for x in scores if x['family']==f),'reworded':sum(x['answer_match'] for x in scores if x['family']==f)} for f in ['grouping','reset']},'gained':[x['record_id'] for x in scores if x['answer_match'] and not x['baseline_match']],'lost':[x['record_id'] for x in scores if not x['answer_match'] and x['baseline_match']],'strict_format':sum(x['strict_format'] for x in scores),'stops':{s:sum(r['stop']==s for r in raw) for s in ['eos','token_limit']},'input_tokens':sum(r['input_tokens'] for r in raw),'output_tokens':sum(r['output_tokens'] for r in raw),'inference_seconds_excluding_serialization':sum(r['inference_seconds_excluding_serialization'] for r in raw),'serialization_seconds':sum(r['serialization_seconds'] for r in raw),'cache_bytes':sum(r['cache_artifact']['bytes'] for r in raw),'scope':'coordinator whole-response review; paired exposed sources, no population claim or independent review'}
    (P/'SCORES.json').write_text(json.dumps(scores,indent=2)+'\n');(P/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
