"""Check REV-C1 record integrity and summarize the two retained blind reviews."""
from collections import defaultdict
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evaluation/revision-continuity-v1'
DIMENSIONS=['current_history','evidence_uncertainty','open_questions','next_action']


def read(p):
    return json.loads(p.read_text())


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    settings=read(OUT/'SETTINGS.json');manifest=read(OUT/'LAUNCH_MANIFEST.json')
    launch_checks={p:digest(ROOT/p)==h for p,h in (manifest['hashes']|manifest['prompt_files']).items()}
    if not all(launch_checks.values()):raise ValueError('Frozen launch artifact changed')
    if settings['frr_text']!=(ROOT/'prompts/compact.md').read_text():raise ValueError('FRR text differs')
    repair=OUT/'review-repair-v1';rmanifest=read(repair/'MANIFEST.json')
    if digest(OUT/'REVIEW_PACKET.json')!=rmanifest['original_packet_sha256'] or digest(OUT/'REVIEW_PROMPT.txt')!=rmanifest['original_prompt_sha256']:
        raise ValueError('Original review packet changed')
    split=[]
    for name,h in rmanifest['parts'].items():
        text=(repair/name).read_text()
        if digest(repair/name)!=h:raise ValueError('Review part changed')
        prefix,body=text.split(' OF 2:\n',1)
        if not prefix.startswith(settings['review_rubric']+'\n\nREVIEW PACKET PART '):raise ValueError('Review rubric changed')
        split.extend(json.loads(body))
    packet=read(OUT/'REVIEW_PACKET.json')
    if split!=packet['cases'] or packet['rubric']!=settings['review_rubric']:raise ValueError('Lossy split')
    expected=set(settings['review_mapping'])
    reviews={}
    for reviewer in ['C','E']:
        raw=read(OUT/f'REVIEW_{reviewer}.json')
        if set(raw)!={'reviews'} or len(raw['reviews'])!=len(expected):raise ValueError('Review outer schema')
        by_id={r['review_id']:r for r in raw['reviews']}
        if set(by_id)!=expected:raise ValueError('Review IDs missing/duplicate')
        for r in by_id.values():
            if set(r)!={'review_id','scores','evidence','unsupported_claims','unexpected_observation'}:raise ValueError('Review schema')
            if set(r['scores'])!=set(DIMENSIONS) or set(r['evidence'])!=set(DIMENSIONS):raise ValueError('Dimensions changed')
            if any(type(v) is not int or v not in range(3) for v in r['scores'].values()):raise ValueError('Invalid ordinal score')
            if any(not isinstance(v,str) or not v for v in r['evidence'].values()):raise ValueError('Missing review evidence')
            if not isinstance(r['unsupported_claims'],list) or any(not isinstance(v,str) for v in r['unsupported_claims']):raise ValueError('Unsupported-claim schema')
            if not isinstance(r['unexpected_observation'],str):raise ValueError('Observation schema')
        reviews[reviewer]=by_id
    failures=[]
    for reviewer in ['A','B']:
        raw=read(OUT/f'REVIEW_{reviewer}_ORIGINAL.json')
        if raw.get('reviews')!=[] or not raw.get('error'):raise ValueError('Original failed review lost')
        failures.append(dict(reviewer=reviewer,status='truncated_packet_no_scores',error=raw['error']))
    failures.append(dict(reviewer='D',status='usage_limit_no_scores',error=(OUT/'REVIEW_D_USAGE_ERROR.txt').read_text().strip()))
    by_trial={t['trial_id']:t for t in settings['trials']}
    if set(settings['review_mapping'].values())!=set(by_trial):raise ValueError('Trial mapping mismatch')
    rows=[];by_arm=defaultdict(list);memos={}
    for review_id,trial_id in settings['review_mapping'].items():
        t=by_trial[trial_id];first=(OUT/(trial_id+'_first.txt')).read_text();final=(OUT/(trial_id+'_final.txt')).read_text()
        if not first.strip() or not final.strip():raise ValueError('Empty participant memo')
        for stage in ['first','final']:
            if (OUT/(trial_id+'_'+stage+'_prompt.txt')).read_text()!=t[stage+'_prompt']:raise ValueError('Prompt file mismatch')
            if hashlib.sha256(t[stage+'_prompt'].encode()).hexdigest()!=t[stage+'_prompt_sha256']:raise ValueError('Prompt hash mismatch')
        p=next(p for p in split if p['review_id']==review_id)
        case=next(c for c in read(OUT/'CASES.json') if c['case_id']==t['case_id'])
        if p['initial_memo']!=first.strip() or p['final_memo']!=final.strip():raise ValueError('Reviewer memo differs')
        if (p['task'],p['history'],p['later_record'],p['authored_key'])!=(case['task'],case['history'],case['update'],case['key']):raise ValueError('Reviewer source/key differs')
        row=dict(trial_id=trial_id,review_id=review_id,arm=t['arm'],case_id=t['case_id'],replicate=t['replicate'],
                 first_words=len(first.split()),final_words=len(final.split()),first_sha256=digest(OUT/(trial_id+'_first.txt')),final_sha256=digest(OUT/(trial_id+'_final.txt')),
                 reviews={j:reviews[j][review_id] for j in reviews})
        rows.append(row);by_arm[t['arm']].append(row);memos[trial_id]=dict(first=first,final=final)
    observations=read(OUT/'PARENT_NOTICINGS.json')
    for n in observations['observations']:
        if n['quote'] not in memos[n['trial_id']][n['stage']]:raise ValueError('Parent observation quote missing')
    summary={}
    for arm,trials in by_arm.items():
        summary[arm]=dict(trajectories=len(trials),first_words_total=sum(t['first_words'] for t in trials),final_words_total=sum(t['final_words'] for t in trials),
            by_reviewer={j:dict(dimension_totals={d:sum(t['reviews'][j]['scores'][d] for t in trials) for d in DIMENSIONS},
                               secondary_total=sum(sum(t['reviews'][j]['scores'].values()) for t in trials),
                               material_unsupported_claims=sum(len(t['reviews'][j]['unsupported_claims']) for t in trials)) for j in reviews})
    differences=[]
    for row in rows:
        for d in DIMENSIONS:
            a,b=[row['reviews'][j]['scores'][d] for j in ['C','E']]
            if a!=b:differences.append(dict(trial_id=row['trial_id'],dimension=d,C=a,E=b))
    paired=[]
    for case in ['COLD','TUTOR']:
        for rep in [1,2]:
            pair={r['arm']:r for r in rows if r['case_id']==case and r['replicate']==rep}
            paired.append(dict(case_id=case,replicate=rep,FRR_minus_ordinary={j:{d:pair['frr_compact_0_2']['reviews'][j]['scores'][d]-pair['ordinary']['reviews'][j]['scores'][d] for d in DIMENSIONS} for j in reviews}))
    output=dict(study='REV-C1',participant_contexts=8,participant_task_turns=16,review_attempts=5,completed_reviewers=['C','E'],failed_review_attempts=failures,
                assigned_prompt_loader_reads=8,assigned_completed_reviewer_part_reads=4,comprehensive_tool_access_audit=False,
                all_launch_hashes_unchanged=all(launch_checks.values()),all_requested_word_limits_met=all(t['first_words']<=300 and t['final_words']<=300 for t in rows),
                launch_checks=launch_checks,review_split_lossless=True,by_arm=summary,trials=rows,reviewer_score_disagreements=differences,paired_differences=paired,
                token_usage=None,dollar_cost=None,elapsed_time=None,
                score_scope='Two same-model-family, arm-label-blind subjective reviews; record checks do not validate semantic judgments',
                interpretation='Both conditions received full rubric credit in these authored cases; no observed score advantage, with ceiling and order/input-length confounds retained')
    (OUT/'RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ['study','participant_contexts','participant_task_turns','review_attempts','completed_reviewers','all_launch_hashes_unchanged','all_requested_word_limits_met','by_arm','reviewer_score_disagreements']},indent=2))


if __name__=='__main__':main()
