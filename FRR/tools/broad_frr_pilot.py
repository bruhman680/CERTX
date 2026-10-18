"""Prepare a broad-FRR exploratory pilot and mechanically record its outputs."""
import argparse
import hashlib
import json
from pathlib import Path
import random

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evaluation/broad-frr-pilot-v1'

GENERIC='''General working guidance

Read the request carefully and identify the deliverable the user needs. Keep the answer relevant to that deliverable. Use the information provided in the task and avoid importing unsupported details. Organize your work so that a reader can understand the conclusion and the evidence supporting it.

Before answering, review the facts that matter to the request. Check names, quantities, units, conditions, and any stated restrictions. If a calculation is needed, verify the arithmetic. If a decision is needed, identify the applicable rule and apply it consistently to the relevant facts.

Consider plausible interpretations when the wording allows more than one reading. Use the interpretation best supported by the supplied material, and explain consequential uncertainty briefly. Do not manufacture uncertainty when the task provides a clear answer. A direct, adequately supported response is often more useful than an elaborate discussion.

Use any available additional information selectively. Prefer material that helps resolve the specific question over material that merely repeats what is already known. If necessary information is unavailable, identify what is missing and describe a practical way to obtain it. Do not claim that a proposed check has already been performed.

Review the candidate answer for factual mistakes, omissions, contradictions, and unnecessary complexity. Revise errors when the evidence warrants a correction. Make sure the final recommendation follows from the information actually supplied, and keep any qualifications proportionate to their practical importance.

Communicate plainly and concisely. Explain calculations or decisions sufficiently for the user to assess them. Preserve useful details for any next step, while avoiding repetition. Include an additional observation only when it contributes something meaningful; novelty is not required. If the task is complete, state the result. If it remains incomplete, distinguish a provisional conclusion from the specific information or action still needed.'''

COMMON=('You are participating in a fictional task exercise. Use only supplied task text and any record returned in this conversation. '
        'Do not use tools, filesystem, internet, other agents or external sources. Do not claim real-world execution or retrieval. '
        'You may request at most one record by its exact menu ID. You may also request none. '
        'Return only JSON with exactly response and request_id. response is a natural-language answer of at most 350 words '
        'with your current conclusion, useful next step, and any other observations you judge consequential. '
        'Concise public rationale is welcome; do not provide private internal deliberation. '
        'request_id is a menu ID string or null. You will get one final turn after the requested record or no record. '
        'Do not name experimental conditions.')

FINAL='This is your final turn. Use the supplied record, if any, to finalize or revise your answer. Return only JSON with exactly response (at most 350 words) and request_id (null). Do not request another record. No other evidence is supplied.'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def prepare():
    if (OUT/'SETTINGS.json').exists():raise SystemExit('Refusing to overwrite settings')
    frr=(ROOT/'prompts/compact.md').read_text()
    if not .9 <= len(GENERIC.split())/len(frr.split()) <= 1.1:
        raise ValueError('Generic guidance not within 10% whitespace-word length')
    cases=[dict(case_id='CONFIG',task='For job J42 determine which input values were selected, and distinguish what actually ran from what should have run.',
        evidence='Inputs for J42: [95,110,125]. Select each value greater than or equal to the loaded threshold. Configuration CFG-A has threshold100 and note release candidate. Configuration CFG-B has threshold120 and note approved settings. Handoff: J42 used the release settings; selected count should be two. There is no trustworthy loading history or ordering in these records.',
        menu={'job_manifest_J42':'configuration fingerprint recorded at loading','release_discussion':'comments about intended release settings'},
        records={'job_manifest_J42':'Job J42 loaded fingerprint CFG-B. Inputs [95,110,125]. This execution record does not establish which settings policy intended.',
                 'release_discussion':'One participant preferred threshold100, another threshold120. No execution receipt is included.'},
        key={'decisive_request':'job_manifest_J42','initial':'actual loaded config undetermined; A selects110,125; B selects125',
             'after_decisive':'selected[125],count1; intended policy remains unknown','unsupported':'approval or policy correctness from execution alone'}),
        dict(case_id='UNITS',task='Do these matched requests establish that mean end-to-end latency increased after release? State the supported conclusion and limits.',
        evidence='Export E17: before[100,200,300]ticks, after[200,400,600]ticks for three matched requests. Dashboard says mean increased200ms to400ms. Release review says twofold slowdown confirmed, citing dashboard from E17. Incident summary says independent review agrees, citing release review using E17. No tick-to-time calibration is supplied.',
        menu={'clock_manifest_E17':'tick frequencies used for both measurements','additional_summary_E17':'another summary of E17'},
        records={'clock_manifest_E17':'Before1000ticks/second; after2000ticks/second. Both measure the same end-to-end interval. Dashboard applied old1ms/tick conversion to both columns.',
                 'additional_summary_E17':'Mean count doubled200to400ticks. Uses E17, no independent timing measurement or calibration.'},
        key={'decisive_request':'clock_manifest_E17','initial':'physical time change unknown; summaries share E17 ancestry',
             'after_decisive':'both means200ms, matched observations show no increase; dashboard unit conversion explains claimed doubling',
             'unsupported':'population equivalence or release causal effect from three matched observations'}),
        dict(case_id='DECISIVE',task='Should J43 proceed under the supplied release rules? Give GO or NO-GO and selected input values.',
        evidence='For this exercise these records are authoritative and complete for the requested decision. Release policy v3: J43 may proceed if it loaded CFG-B, threshold120, on inputs[95,110,125]; no other prerequisites apply. Execution manifest J43 records exactly CFG-B,threshold120,inputs[95,110,125]. Selection rule includes every value >=threshold. No authenticity dispute or other policy condition is stated.',
        menu={'policy_background':'historical explanation for choosing the threshold'},
        records={'policy_background':'Earlier discussions considered thresholds100and120. Current policy v3 remains authoritative and unchanged.'},
        key={'decisive_request':None,'initial':'GO; selected[125]; current complete policy satisfied',
             'after_decisive':'GO; selected[125]','unsupported':'invented missing prerequisites or refusal to decide despite authoritative sufficient evidence'})]
    arms={'baseline':'','generic':GENERIC,'frr_compact_0_2':frr}
    order=[(c['case_id'],a) for c in cases for a in arms];random.Random(2071).shuffle(order)
    trials=[]
    for i,(case_id,arm) in enumerate(order,1):
        case=next(c for c in cases if c['case_id']==case_id)
        packet={k:case[k] for k in ['case_id','task','evidence','menu']}
        prompt=COMMON+('\n\nWORKING GUIDANCE:\n'+arms[arm] if arms[arm] else '')+'\n\nTASK PACKET:\n'+json.dumps(packet,sort_keys=True)
        trials.append(dict(trial_id=f'B{i:02}',case_id=case_id,arm=arm,first_prompt=prompt,
                           first_prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
    settings=dict(study='BFRR-E1',max_participant_completions=18,replicates=1,seed=2071,
                  common=COMMON,final_instruction=FINAL,arms=arms,
                  guidance_word_counts={a:len(s.split()) for a,s in arms.items()},cases=cases,trials=trials,
                  model='inherited session model; no override',sampling=None,token_cost=None,dollar_cost=None)
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'SETTINGS.json').write_text(json.dumps(settings,indent=2)+'\n')
    paths=['tools/broad_frr_pilot.py','prompts/compact.md','evaluation/broad-frr-pilot-v1/PROTOCOL.md','evaluation/broad-frr-pilot-v1/SETTINGS.json']
    (OUT/'LAUNCH_MANIFEST.json').write_text(json.dumps(dict(status='prospective',hashes={p:digest(ROOT/p) for p in paths}),indent=2)+'\n')
    print(json.dumps(dict(prepared=True,guidance_words=settings['guidance_word_counts'],order=order,max_participant_completions=18)))


def assemble():
    settings=json.loads((OUT/'SETTINGS.json').read_text());receipts=[]
    for t in settings['trials']:
        raw=(OUT/(t['trial_id']+'_first.txt')).read_text();response=json.loads(raw)
        if set(response)!={'response','request_id'} or not isinstance(response['response'],str):raise ValueError('First response schema')
        case=next(c for c in settings['cases'] if c['case_id']==t['case_id']);request=response['request_id']
        if request is None:record='No additional record requested or supplied.'
        elif isinstance(request,str) and request in case['records']:record=json.dumps(dict(record_id=request,content=case['records'][request]),sort_keys=True)
        else:record='Requested record unavailable: invalid menu ID. No additional evidence supplied.'
        prompt=settings['final_instruction']+'\n\nRECORD:\n'+record
        (OUT/(t['trial_id']+'_final_prompt.txt')).write_text(prompt)
        receipts.append(dict(trial_id=t['trial_id'],request_id=request,record=record,
                             final_prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest()))
    (OUT/'RETRIEVAL_RECEIPTS.json').write_text(json.dumps(receipts,indent=2)+'\n')
    print(json.dumps(receipts,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['prepare','assemble']);args=p.parse_args()
    prepare() if args.mode=='prepare' else assemble()
