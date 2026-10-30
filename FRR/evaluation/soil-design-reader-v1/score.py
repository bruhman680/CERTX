"""Post-run aggregation of explicit coordinator judgments against frozen keys."""
from pathlib import Path
import json,re
P=Path(__file__).resolve().parent
NOTES={
'G1_reading':('unresolved','Copies a source prefix and stops before stating k; 64 observations is not an explicit soil-count answer.'),
'G1_calculation':('wrong','Final 0.00025 differs from 0.0025; displayed equality also adds 0.032+0.128 incorrectly.'),
'G1_conclusion':('correct','YES matches independent soil per observation; no derivation was requested or demonstrated.'),
'G2_reading':('unresolved','Same truncated source prefix, without a k answer.'),
'G2_calculation':('wrong','Final 0.00068 is not 0.0100; the written expression also changes the supplied denominator roles.'),
'G2_conclusion':('wrong','YES conflicts with sixteen observations per soil under the explicit iid criterion.'),
'G3_reading':('unresolved','Same truncated source prefix, without a k answer.'),
'G3_calculation':('wrong','Final 0.00025 is not 0.0340; does not retain the one-soil variance.'),
'G3_conclusion':('wrong','YES conflicts with sixty-four observations sharing one soil under the explicit criterion.'),
'G4_reading':('wrong','Invents k=64 from the total observations although grouping is unrecorded.'),
'G4_calculation':('wrong','Gives a numerical variance without recorded k; displayed arithmetic is also false.'),
'G4_conclusion':('wrong','YES supplies certainty where the sampling criterion is undetermined.'),
'R1_reading':('correct','Sentence means PROVIDED, agreeing with supplied qA=.50 and qS=.75.'),
'R1_calculation':('wrong','Calls reset effectiveness values .50 and .75 the compatible pi values, then repeats to the cap; neither is pi=.40.'),
'R1_conclusion':('wrong','NO rejects the uniquely reconstructed pi=.40.'),
'R2_reading':('wrong','Asserts both effectiveness values are supplied although both are absent.'),
'R2_calculation':('wrong','Uses readouts .160 and .088 as pi bounds, in reversed order; correct interval is [.20,.55].'),
'R2_conclusion':('correct','NO matches a nonsingleton feasible set; no supported calculation or reasoning path is demonstrated.'),
'R3_reading':('correct','Sentence means PROVIDED; zero values remain provided values.'),
'R3_calculation':('wrong','Repeats only pi=0.00 rather than the complete [0,1] feasible interval.'),
'R3_conclusion':('wrong','YES asserts a point where ineffective resets leave every pi feasible.'),
'R4_reading':('wrong','Asserts both effectiveness values are supplied although absent.'),
'R4_calculation':('wrong','Uses readouts .096 and .064 as pi bounds, reversed, instead of singleton [.40,.40].'),
'R4_conclusion':('wrong','NO misses point identification from the constraints despite missing effectiveness values.')}

def strict(text,key):
    text=text.strip(); expected=key['expected']
    if key['type']=='number': return bool(re.fullmatch(r'\d+(?:\.\d+)?',text))
    if key['type']=='interval':return bool(re.fullmatch(r'\d+\.\d{2}\.\.\d+\.\d{2}',text))
    return text in (('YES','NO','UNKNOWN') if expected in ('YES','NO','UNKNOWN') else ('PROVIDED','MISSING'))

def main():
    raw=[json.loads(l) for l in (P/'RAW_OUTPUTS.jsonl').read_text().splitlines()]
    keys={r['id']:r for r in json.loads((P/'KEYS.json').read_text())}
    assert len(raw)==24 and set(NOTES)==set(keys)=={r['run_id'] for r in raw}
    scores=[]
    for r in raw:
        ident=r['run_id']; status,note=NOTES[ident];key=keys[ident]
        scores.append({'id':ident,'record_id':r['record_id'],'family':r['family'],'facet':r['facet'],'expected':key['expected'],'text':r['text'],'semantic_status':status,'answer_match':status=='correct','no_added_material_error_when_matched':status=='correct','strict_requested_format':strict(r['text'],key),'format_case_insensitive_only':strict(r['text'].upper(),key),'stop':r['stop'],'coordinator_reason':note})
    facets={f:{'correct':sum(x['answer_match'] for x in scores if x['facet']==f),'total':8,'unresolved':sum(x['semantic_status']=='unresolved' for x in scores if x['facet']==f)} for f in ('reading','calculation','conclusion')}
    records={rid:{'matched_facets':[x['facet'] for x in scores if x['record_id']==rid and x['answer_match']],'all_three_match':all(x['answer_match'] for x in scores if x['record_id']==rid)} for rid in sorted({x['record_id'] for x in scores})}
    summary={'generations':24,'semantic_correct':sum(x['answer_match'] for x in scores),'semantic_wrong':sum(x['semantic_status']=='wrong' for x in scores),'unresolved':sum(x['semantic_status']=='unresolved' for x in scores),'strict_format':sum(x['strict_requested_format'] for x in scores),'format_case_insensitive_only':sum(x['format_case_insensitive_only'] for x in scores),'facets':facets,'records':records,'records_all_three_match':sum(x['all_three_match'] for x in records.values()),'stops':{s:sum(r['stop']==s for r in raw) for s in ('eos','token_limit')},'input_tokens':sum(r['input_tokens'] for r in raw),'output_tokens':sum(r['output_tokens'] for r in raw),'inference_seconds_excluding_serialization':sum(r['inference_seconds_excluding_serialization'] for r in raw),'serialization_seconds':sum(r['serialization_seconds'] for r in raw),'new_cache_bytes':sum(r['cache_artifact']['bytes'] for r in raw),'review_scope':'coordinator whole-response semantic review, not independent or masked; no internal reasoning inferred from bare label matches'}
    (P/'SCORES.json').write_text(json.dumps(scores,indent=2)+'\n')
    (P/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
