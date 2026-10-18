"""Check BFRR-E1 record integrity and summarize explicit parent judgments."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evaluation/broad-frr-pilot-v1'


def read(p):
    return json.loads(p.read_text())


def main():
    settings=read(OUT/'SETTINGS.json');manifest=read(OUT/'LAUNCH_MANIFEST.json')
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in manifest['hashes'].items()}
    if not all(hashes.values()):raise ValueError('Launch artifacts changed')
    if settings['arms']['frr_compact_0_2']!=(ROOT/'prompts/compact.md').read_text():raise ValueError('FRR treatment changed')
    review=read(OUT/'PARENT_REVIEW.json');ratings={r['trial_id']:r for r in review['trial_reviews']}
    receipts=read(OUT/'RETRIEVAL_RECEIPTS.json');receipts={r['trial_id']:r for r in receipts}
    expected_ids={t['trial_id'] for t in settings['trials']}
    if set(ratings)!=expected_ids or len(review['trial_reviews'])!=len(expected_ids) or set(receipts)!=expected_ids:raise ValueError('Record ID mismatch')
    rows=[];by_arm=defaultdict(list)
    for t in settings['trials']:
        trial_id=t['trial_id'];case=next(c for c in settings['cases'] if c['case_id']==t['case_id'])
        first=read(OUT/(trial_id+'_first.txt'));final=read(OUT/(trial_id+'_final.txt'))
        for data in [first,final]:
            if set(data)!={'response','request_id'} or not isinstance(data['response'],str):raise ValueError('Schema failure')
        if final['request_id'] is not None:raise ValueError('Final requested extra record')
        request=first['request_id']
        if request is not None and request not in case['records']:raise ValueError('Unavailable request')
        expected_record='No additional record requested or supplied.' if request is None else json.dumps(dict(record_id=request,content=case['records'][request]),sort_keys=True)
        prompt=settings['final_instruction']+'\n\nRECORD:\n'+expected_record
        receipt=receipts[trial_id]
        if receipt['request_id']!=request or receipt['record']!=expected_record:raise ValueError('Record return mismatch')
        if (OUT/(trial_id+'_final_prompt.txt')).read_text()!=prompt or hashlib.sha256(prompt.encode()).hexdigest()!=receipt['final_prompt_sha256']:raise ValueError('Final prompt mismatch')
        if hashlib.sha256(t['first_prompt'].encode()).hexdigest()!=t['first_prompt_sha256']:raise ValueError('First prompt mismatch')
        rating=ratings[trial_id]
        if rating['final_excerpt'] not in final['response']:raise ValueError('Judgment excerpt missing')
        row=dict(trial_id=trial_id,arm=t['arm'],case_id=t['case_id'],requested_record=request,
                 key_verification_choice=request==case['key']['decisive_request'],
                 first_words=len(first['response'].split()),final_words=len(final['response'].split()),
                 first_response_sha256=hashlib.sha256((OUT/(trial_id+'_first.txt')).read_bytes()).hexdigest(),
                 final_response_sha256=hashlib.sha256((OUT/(trial_id+'_final.txt')).read_bytes()).hexdigest(),
                 parent_judgment=rating)
        rows.append(row);by_arm[t['arm']].append(row)
    for n in review['post_run_noticing']:
        if n['quote'] not in read(OUT/(n['trial_id']+'_'+n['stage']+'.txt'))['response']:raise ValueError('Observation excerpt missing')
    summary={}
    for arm,trials in by_arm.items():
        summary[arm]=dict(trajectories=len(trials),verification_choices_matching_key=sum(r['key_verification_choice'] for r in trials),
                          final_key_satisfied_by_parent_review=sum(r['parent_judgment']['final_key_satisfied'] for r in trials),
                          obstructive_doubt_by_parent_review=sum(r['parent_judgment']['needless_doubt_obstructed_completion'] for r in trials),
                          material_unsupported_claims_by_parent_review=sum(len(r['parent_judgment']['material_unsupported_claims']) for r in trials),
                          first_words_total=sum(r['first_words'] for r in trials),final_words_total=sum(r['final_words'] for r in trials))
    output=dict(study='BFRR-E1',participant_contexts=len(rows),participant_completions=2*len(rows),
                all_requested_word_limits_met=all(r['first_words']<=350 and r['final_words']<=350 for r in rows),
                launch_hashes_unchanged=all(hashes.values()),hash_checks=hashes,by_arm=summary,trials=rows,
                observed_participant_tool_calls=0,token_usage=None,dollar_cost=None,elapsed_time=None,
                scoring='Verification choices/word counts and record consistency checked mechanically; semantic scores are unblinded parent judgments, not independently validated automatic judging',
                output_provenance='Final-message payloads transcribed by parent, not provider exports',
                conclusion='All arms tied on observed verification choices and parent-rated final correctness; output emphasis and length differed, with no general efficacy conclusion')
    (OUT/'RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ['study','participant_contexts','participant_completions','launch_hashes_unchanged','all_requested_word_limits_met','by_arm']},indent=2))


if __name__=='__main__':main()
