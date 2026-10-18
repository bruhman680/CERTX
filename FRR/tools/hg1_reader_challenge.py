"""Prepare and evaluate six authored reader challenges using the frozen scorer."""
import argparse
import hashlib
import json
from pathlib import Path
import random
from hg1_reader_scoring import fact, score, unique_object

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'evaluation/hpgm-gates-study/reader-challenge-v1'


def load(p):
    return json.loads(p.read_text(), object_pairs_hook=unique_object)


def prepare():
    if (OUT/'SETTINGS.json').exists():
        raise SystemExit('Refusing to overwrite frozen settings')
    common = ('You are a fresh continuation reader. Use only the supplied evidence facts and update. '
              'Do not use tools, filesystem, internet, other agents or external sources. '
              'No original source or answer key is assigned to you. Each equality has coefficients for a,b,c and rhs. '
              'Find a+c. Return only JSON with exactly status, value, support_ids. '
              'status is answer, missing_info, or conflicting_evidence. '
              'For answer, value is a number; otherwise value is null. '
              'support_ids lists relevant equality IDs actually in your packet; do not invent facts or IDs. '
              'If available evidence cannot determine the requested value, report missing_info; '
              'if evidence is inconsistent, report conflicting_evidence. '
              'Use the supplied facts as your premises; no external source verification is available.')
    a = fact('r1',[1,1,0],8)
    c = fact('r2',[0,1,1],11)
    compressed = fact('r3',[1,2,1],19)
    bad = fact('r4',[1,2,1],20)
    u = fact('u1',[0,1,0],3,'update')
    specs = [
        ('complete',[a,c,u],dict(status='answer',value=13,support_ids=['r1','r2','u1'])),
        ('compressed',[compressed,u],dict(status='answer',value=13,support_ids=['r3','u1'])),
        ('missing_all',[u],dict(status='missing_info',value=None,support_ids=['u1'])),
        ('missing_one',[a,u],dict(status='missing_info',value=None,support_ids=['r1','u1'])),
        ('conflict',[compressed,bad,u],dict(status='conflicting_evidence',value=None,support_ids=['r3','r4'])),
        ('corrupted_consistent',[bad,u],dict(status='answer',value=14,support_ids=['r4','u1']))]
    random.Random(1903).shuffle(specs)
    trials=[]
    for i,(condition,facts,expected) in enumerate(specs,1):
        trial_id=f'R{i:02}'
        packet=dict(trial_id=trial_id,facts=facts,request='Find a+c from these premises.')
        prompt=common+'\n\nPACKET:\n'+json.dumps(packet,sort_keys=True)
        expected_score=score(dict(case_id='LINEAR-2',facts=facts,response=expected))
        trials.append(dict(trial_id=trial_id,condition=condition,packet=packet,prompt=prompt,
                           prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
                           expected_status=expected['status'],expected_value=expected['value'],
                           expected_score=expected_score))
    settings=dict(study='HG1-RC1',max_completions=6,seed=1903,trials=trials,
                  prediction='All six readers will behave appropriately to the packet; corrupt-consistent answer is expected to be objectively wrong.',
                  model='inherited session model; no override',sampling=None,token_cost=None,dollar_cost=None,
                  access='Assigned supplied-packet-only; shared tool/filesystem access not physically blocked')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'SETTINGS.json').write_text(json.dumps(settings,indent=2)+'\n')
    paths=['tools/hg1_reader_challenge.py','tools/hg1_reader_scoring.py',
           'evaluation/hpgm-gates-study/reader-challenge-v1/PROTOCOL.md',
           'evaluation/hpgm-gates-study/reader-challenge-v1/SETTINGS.json']
    manifest=dict(status='prospective before reader outputs',hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths})
    (OUT/'LAUNCH_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(prepared=True,order=[t['condition'] for t in trials],max_completions=6)))


def evaluate():
    settings=load(OUT/'SETTINGS.json');manifest=load(OUT/'LAUNCH_MANIFEST.json')
    checks={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in manifest['hashes'].items()}
    if not all(checks.values()):
        raise ValueError('Launch artifact changed')
    rows=[]
    for t in settings['trials']:
        path=OUT/(t['trial_id']+'_reader.txt')
        row=dict(trial_id=t['trial_id'],condition=t['condition'],expected_status=t['expected_status'],expected_value=t['expected_value'])
        if not path.exists():
            row.update(outcome='missing_response',score=None)
        else:
            row['response_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
            try:
                response=load(path)
                result=score(dict(case_id='LINEAR-2',facts=t['packet']['facts'],response=response))
                row.update(outcome='scored',response=response,score=result,
                           predicted_status_value_matched=response['status']==t['expected_status'] and response['value']==t['expected_value'])
            except (ValueError,TypeError,KeyError) as exc:
                row.update(outcome='parse_or_schema_failure',error=str(exc),score=None)
        rows.append(row)
    summary=dict(study='HG1-RC1',assigned=6,received=sum((OUT/(t['trial_id']+'_reader.txt')).exists() for t in settings['trials']),
                 scored=sum(r['outcome']=='scored' for r in rows),
                 packet_appropriate=sum(bool(r['score'] and r['score']['epistemically_appropriate_to_packet']) for r in rows),
                 objective_correct_answers=sum(bool(r['score'] and r['score']['objective_correct']) for r in rows),
                 grounded_completions=sum(bool(r['score'] and r['score']['grounded_completion']) for r in rows),
                 predicted_status_value_matched=sum(r.get('predicted_status_value_matched',False) for r in rows),
                 launch_hashes_unchanged=all(checks.values()),scope='Six exposed authored packet conditions; no instruction-style comparison or independent replication')
    output=dict(summary=summary,trials=rows,hash_checks=checks,
                usage=dict(max_completions=6,actual_token_usage=None,actual_dollar_cost=None,elapsed_time=None),
                limitations=['One reader per condition','Shared model provenance','Instruction-only access limits',
                             'Exact equality scoring only','Output payloads transcribed from final messages',
                             'No inference that cited support caused the answer','No general FRR or HPGM efficacy estimate'])
    (OUT/'RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('mode',choices=['prepare','evaluate'])
    args=parser.parse_args();prepare() if args.mode=='prepare' else evaluate()
