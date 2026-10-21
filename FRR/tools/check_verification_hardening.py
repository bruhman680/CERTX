"""Disclosed post-run parser repair checks and full instrument replay."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from verification_layer import evaluate,rational,digest

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evaluation/verification-layer-v1'


def prepare():
    p=OUT/'HARDENING_MANIFEST.json'
    if p.exists():raise ValueError('Refusing to overwrite repair preparation')
    paths=['tools/verification_layer.py','tools/check_verification_hardening.py','evaluation/verification-layer-v1/AMENDMENT_01.md','evaluation/verification-layer-v1/FIXTURES.json','evaluation/verification-layer-v1/KEYS.json']
    paths += ['evaluation/verification-layer-v1/'+str(x.relative_to(OUT)) for x in sorted((OUT/'artifacts').glob('*.json'))]
    p.write_text(json.dumps({'status':'Repaired checker frozen before expanded replay; initial results preserved','hashes':{name:digest((ROOT/name).read_bytes()) for name in paths}},indent=2)+'\n')
    print('repair prepared')


def run():
    manifest=json.loads((OUT/'HARDENING_MANIFEST.json').read_text())
    unchanged=all(digest((ROOT/p).read_bytes())==h for p,h in manifest['hashes'].items())
    assert unchanged
    fixtures=json.loads((OUT/'FIXTURES.json').read_text());keys=json.loads((OUT/'KEYS.json').read_text());rows=[]
    for version in ['0.1','0.2']:
        for c in fixtures:
            receipt=evaluate(c,OUT,version);rows.append({'receipt':receipt,'expected':keys[c['claim_id']][version]})
    rejected=[]
    for value in ['1e999999999','1e-999999999','1e-1','.4','nan','inf','9'*257,True]:
        try:rational(value)
        except ValueError:rejected.append(repr(value))
        else:raise AssertionError('Invalid numeric form accepted')
    valid={value:str(rational(value)) for value in ['0','-2','3/4','-0.4','+12','1.25']}
    assert valid=={'0':'0','-2':'-2','3/4':'3/4','-0.4':'-2/5','+12':'12','1.25':'5/4'}
    contract_dir=OUT/'examples';contract_dir.mkdir(exist_ok=True);cli=[]
    for name in ['literal_correct','literal_incorrect']:
        c=next(c for c in fixtures if c['claim_id']==name);path=contract_dir/(name+'.json');path.write_text(json.dumps(c,indent=2)+'\n')
        result=subprocess.run([sys.executable,str(ROOT/'tools/verification_layer.py'),str(path),'--root',str(OUT),'--version','0.2'],capture_output=True,text=True,timeout=10)
        receipt=json.loads(result.stdout);assert result.returncode==0 and receipt['verdict']==keys[name]['0.2']
        cli.append({'claim_id':name,'returncode':result.returncode,'stdout_receipt':receipt,'stderr':result.stderr})
    (OUT/'HARDENING_RECEIPTS.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in rows))
    result={'scope':'Parser repair, authored disposition replay and local CLI contact; not independent behavioral confirmation','replay_evaluations':len(rows),'all_expected_verdicts_matched':all(x['receipt']['verdict']==x['expected'] for x in rows),'rejected_number_forms':rejected,'valid_number_controls':valid,'cli_checks':cli,'repaired_checker_sha256':digest((ROOT/'tools/verification_layer.py').read_bytes()),'repair_hashes_unchanged':unchanged,'initial_protocol_and_results_preserved':True,'model_calls':0}
    (OUT/'HARDENING_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['all_expected_verdicts_matched']


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','run']);args=p.parse_args();prepare() if args.mode=='prepare' else run()
