"""Fresh-process source reproductions and arithmetic receipt audit; no source edits."""
from pathlib import Path
import collections, difflib, hashlib, importlib.util, json, os, subprocess, sys, time

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
GROUP=ROOT/'lineage/sources/claude-group-vote-soil-2026-10-27'
SOIL=ROOT/'lineage/sources/claude-soil-budget-2026-10-27'

def main():
    (HERE/'reproduction').mkdir()
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
    rows=[]
    for script, expected in [(GROUP/'group_vote_soil.py',GROUP/'group_vote_soil_output.txt'),
                             (HERE/'adapted/soil_budget.py',SOIL/'soil_budget_output.txt'),
                             (HERE/'adapted/soil_budget_length.py',SOIL/'soil_budget_length_output.txt')]:
        start=time.monotonic()
        r=subprocess.run([sys.executable,'-I',str(script)],cwd=HERE,capture_output=True,env=env,timeout=120)
        output=HERE/'reproduction'/script.name
        output.with_suffix('.stdout.txt').write_bytes(r.stdout)
        output.with_suffix('.stderr.txt').write_bytes(r.stderr)
        match=r.stdout==expected.read_bytes()
        output.with_suffix('.diff.txt').write_text(''.join(difflib.unified_diff(expected.read_text().splitlines(True),r.stdout.decode().splitlines(True),fromfile='supplied',tofile='reproduced')))
        rows.append({'script':str(script.relative_to(ROOT)),'seconds':time.monotonic()-start,'exit_code':r.returncode,
                     'stdout_matches_supplied_bytes':match,'stderr_bytes':len(r.stderr),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest()})
    receipts=GROUP/'verification_receipts'
    ledger=[json.loads(s) for s in (receipts/'ledger.jsonl').read_text().splitlines() if s]
    spec=importlib.util.spec_from_file_location('local_verification_checker',ROOT/'tools/verification_layer.py')
    checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
    chain_end=checker.validate_ledger(ledger)
    old={e['receipt']['claim_id']:e['receipt'] for e in ledger}
    receipt_rows=[]
    for c in sorted((receipts/'contracts').glob('*.json')):
        start=time.monotonic()
        r=subprocess.run([sys.executable,'-I',str(ROOT/'tools/verification_layer.py'),str(c),'--root',str(receipts/'root'),'--version','0.2'],capture_output=True,env=env,timeout=15)
        (HERE/'reproduction'/(c.stem+'.receipt.stdout.txt')).write_bytes(r.stdout)
        (HERE/'reproduction'/(c.stem+'.receipt.stderr.txt')).write_bytes(r.stderr)
        assert r.returncode==0,(c,r.stderr)
        new=json.loads(r.stdout);previous=old[new['claim_id']]
        assert new==previous,(c,new,previous)
        receipt_rows.append({'claim_id':new['claim_id'],'verdict':new['verdict'],'exit_code':r.returncode,'receipt_exactly_matches_ledger':True,'seconds':time.monotonic()-start})
    failed=json.loads((receipts/'contracts/vote_shasym_n3.json').read_text())
    artifact=json.loads((receipts/'root'/failed['artifact']['path']).read_text())
    try:
        checker.expression_value(artifact['expression'])
        parser_failure=None
    except Exception as exc:
        parser_failure={'exception':type(exc).__name__,'message':str(exc)}
    frozen=json.loads((HERE/'FREEZE.json').read_text())['source_and_dependency_files']
    for path,h in frozen.items():
        f=ROOT/path.removeprefix('FRR/');assert hashlib.sha256(f.read_bytes()).hexdigest()==h,path
    out={'scripts':rows,'receipts':receipt_rows,'ledger_events':len(ledger),'ledger_chain_end':chain_end,
         'receipt_verdict_counts':dict(collections.Counter(x['verdict'] for x in receipt_rows)),
         'unresolved_original_expression_diagnostic':parser_failure,'all_frozen_sources_unchanged':True,
         'scope':'Source execution reproduction, path-only adaptation for budget scripts, unchanged checker receipt/chain audit; not independent model replication'}
    (HERE/'REPRODUCTION.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
