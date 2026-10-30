"""Evaluate a frozen complete path; preserves exact receipts, no LLM or training."""
from pathlib import Path
import argparse,hashlib,json,sys,tempfile,subprocess,time
P=Path(__file__).resolve().parent;R=P.parents[1];TOOLS=R/'tools';sys.path.insert(0,str(TOOLS))
import source_calculation_path as instrument

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def checks(receipt,expected,source):
    errors=[]
    for k in ['stage','answer']:
        if receipt[k]!=expected[k]:errors.append(k)
    if expected.get('variance') is not None:
        for k in ['numerator','denominator']:
            if receipt.get('variance',{}).get(k)!=expected['variance'][k]:errors.append('variance_'+k)
    if expected['stage'] in ['conditional_answer','source_missing','outside_domain']:
        fields=receipt.get('bound_fields',{})
        for field,key,st in [('soil_count','soil_count','soil_state'),('per_soil_observations','observations_per_soil','observations_state')]:
            if fields.get(field,{}).get('value')!=expected[key]:errors.append(field+'_value')
            if fields.get(field,{}).get('state')!=expected[st]:errors.append(field+'_state')
        for field in fields.values():
            if field['quote'] is not None and field['quote'] not in source:errors.append('quote_not_in_source')
    if receipt['status']!=('computed' if expected['stage']=='conditional_answer' else 'withheld'):errors.append('status')
    return errors

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,default=P/'checked_run');args=parser.parse_args()
    freeze=json.loads((P/'EVALUATION_FREEZE.json').read_text())
    for name,h in freeze['sha256'].items():assert sha(P/name)==h,name
    out=args.output_dir;out.mkdir(parents=True,exist_ok=False)
    fixtures=json.loads((P/'data/FIXTURES.json').read_text());gold={x['id']:x for x in json.loads((P/'data/EXPECTED.json').read_text())};byid={x['id']:x for x in fixtures}
    rows=[]
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp)
        for f in fixtures:
            (root/'source.txt').write_text(f['source_text']);begin=time.perf_counter();receipt=instrument.evaluate(f['contract'],root);elapsed=time.perf_counter()-begin
            rows.append({'id':f['id'],'kind':'new_fixture','seconds':elapsed,'errors':checks(receipt,gold[f['id']],f['source_text']),'receipt':receipt})
        for f in json.loads((P/'data/REGRESSIONS.json').read_text()):
            origin=f['origin'];old=P.parent/origin['study']/'CASES.json';assert sha(old)==origin['source_cases_sha256'];case=next(c for c in json.loads(old.read_text()) if c['id']==origin['case_id']);assert hashlib.sha256(case['source'].encode()).hexdigest()==origin['original_body_sha256'];assert f['source_text'].split('\n',1)[1].rstrip('\n')==case['source']
            (root/'source.txt').write_text(f['source_text']);begin=time.perf_counter();receipt=instrument.evaluate(f['contract'],root);elapsed=time.perf_counter()-begin
            rows.append({'id':f['id'],'kind':'historical_body','seconds':elapsed,'errors':checks(receipt,f['expected'],f['source_text']),'receipt':receipt})
        for p in json.loads((P/'data/PROPOSALS.json').read_text()):
            f=byid[p['fixture_id']];(root/'source.txt').write_text(f['source_text']);begin=time.perf_counter();receipt=instrument.evaluate(f['contract'],root,p['proposal']);elapsed=time.perf_counter()-begin
            errors=[]
            if receipt['stage']!=p['expected_stage']:errors.append('stage')
            if receipt['answer']!=p['expected_answer']:errors.append('answer')
            rows.append({'id':p['id'],'kind':'curated_proposal','seconds':elapsed,'errors':errors,'receipt':receipt})
    cli=json.loads(subprocess.check_output([sys.executable,str(TOOLS/'source_calculation_path.py'),str(P/'demo/contract.json'),'--root',str(P/'demo')]))
    assert cli['stage']=='conditional_answer' and cli['answer']=='YES' and cli['variance']['numerator']=='1' and cli['variance']['denominator']=='100'
    (out/'DEMO_RECEIPT.json').write_text(json.dumps(cli,indent=2)+'\n');(out/'RECEIPTS.json').write_text(json.dumps(rows,indent=2)+'\n')
    summary={'new_fixtures':20,'historical_body_regressions':31,'curated_proposal_cases':9,'cases_matched':sum(not r['errors'] for r in rows),'cases_total':len(rows),'failures':[{'id':r['id'],'errors':r['errors']} for r in rows if r['errors']],'new_fixture_computed':sum(r['receipt']['status']=='computed' for r in rows if r['kind']=='new_fixture'),'new_fixture_withheld':sum(r['receipt']['status']=='withheld' for r in rows if r['kind']=='new_fixture'),'library_evaluation_seconds':sum(r['seconds'] for r in rows),'fresh_cli_demo_pass':True,'tool_sha256':instrument.TOOL_SHA256,'scope':'authored deterministic instrument acceptance and exposed regressions, not hidden benchmark/LLM witness production or statistical independence verification'}
    (out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
    if summary['failures']:sys.exit(1)
if __name__=='__main__':main()
