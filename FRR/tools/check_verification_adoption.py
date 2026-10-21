"""Live integration and source-binding regression checks."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from verification_layer import evaluate,validate_ledger,digest
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evaluation/verification-adoption-v1';OLD=ROOT/'evaluation/verification-layer-v1'
LINKS=['README.md','CURRENT_HANDOFF.md','sync/CURRENT_ORIENTATION.md','modules/evidence-gated-feedback.md','modules/bounded-experiment-loop.md','modules/artifact-execution-harness.md','evaluation/PROTOCOL.md','examples/bounded-trial-card.md']


def prepare():
    p=OUT/'MANIFEST.json'
    if p.exists():raise ValueError('Preparation exists')
    paths=['tools/verification_layer.py','tools/check_verification_adoption.py','evaluation/verification-adoption-v1/PROTOCOL.md',*LINKS]
    paths += ['evaluation/verification-layer-v1/FIXTURES.json','evaluation/verification-layer-v1/KEYS.json']
    p.write_text(json.dumps({'hashes':{n:digest((ROOT/n).read_bytes()) for n in paths}},indent=2)+'\n');print('prepared')


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def run():
    manifest=json.loads((OUT/'MANIFEST.json').read_text());assert all(digest((ROOT/n).read_bytes())==h for n,h in manifest['hashes'].items())
    fixtures=json.loads((OLD/'FIXTURES.json').read_text());keys=json.loads((OLD/'KEYS.json').read_text());replay=[]
    for version in ['0.1','0.2']:
        for c in fixtures:
            receipt=evaluate(c,OLD,version);assert receipt['verdict']==keys[c['claim_id']][version];replay.append(receipt)
    malformed=[[],None,True,{'metadata':float('nan')}]
    malformed_results=[evaluate(x,OLD) for x in malformed];assert all(x['verdict']=='unresolved' for x in malformed_results)
    links={n:'verification-layer.md' in (ROOT/n).read_text() for n in LINKS};assert all(links.values())
    c=next(c for c in fixtures if c['claim_id']=='literal_correct')
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp);path=tmp/'checker.py';path.write_bytes((ROOT/'tools/verification_layer.py').read_bytes());module=load(path,'loaded_checker')
        before=module.evaluate(c,OLD);path.write_text(path.read_text()+'\n# Changed after import for regression.\n');after=module.evaluate(c,OLD)
        fresh=load(path,'fresh_checker').evaluate(c,OLD)
        assert before['verdict']=='supported' and after['verdict']=='unresolved' and fresh['verdict']=='supported'
        assert before['checker_sha256']==after['checker_sha256'] and fresh['checker_sha256']!=before['checker_sha256']
        ledger=tmp/'concurrent.jsonl'
        code="import sys;sys.path.insert(0,sys.argv[1]);from verification_layer import append_receipt;[append_receipt(sys.argv[2],{'claim_id':sys.argv[3]+'-'+str(i)}) for i in range(5)]"
        procs=[subprocess.Popen([sys.executable,'-c',code,str(ROOT/'tools'),str(ledger),str(i)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for i in range(4)]
        proc_results=[]
        for p in procs:
            stdout,stderr=p.communicate(timeout=15);assert p.returncode==0;proc_results.append({'returncode':p.returncode,'stdout':stdout,'stderr':stderr})
        rows=[json.loads(x) for x in ledger.read_text().splitlines()];validate_ledger(rows);assert len(rows)==20
        with ledger.open('a') as h:h.write('{"incomplete":')
        damaged=ledger.read_bytes()
        try:module.append_receipt(ledger,{'claim_id':'later'})
        except json.JSONDecodeError:rejected=True
        else:rejected=False
        assert rejected and ledger.read_bytes()==damaged
    old_hashes=json.loads((OLD/'INITIAL_OUTPUT_HASHES.json').read_text());preserved={n:digest((OLD/n).read_bytes())==h for n,h in old_hashes.items()};assert all(preserved.values())
    result={'scope':'Live integration and engineering checks, not consistent long-term habit or agent efficacy','replayed_dispositions':len(replay),'all_dispositions_matched':True,'links':links,'malformed_contract_receipts':malformed_results,'source_drift':{'before':before,'after':after,'fresh':fresh},'concurrent_events':len(rows),'concurrent_processes':proc_results,'incomplete_tail_rejected_without_change':rejected,'initial_output_preservation':preserved,'checker_sha256':digest((ROOT/'tools/verification_layer.py').read_bytes()),'model_calls':0}
    (OUT/'REPLAY_RECEIPTS.jsonl').write_text(''.join(json.dumps(x,sort_keys=True)+'\n' for x in replay));(OUT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','run']);args=p.parse_args();prepare() if args.mode=='prepare' else run()
