from pathlib import Path
import subprocess,json,hashlib,time,sys,platform
import numpy,scipy
P=Path(__file__).resolve().parent
script=sys.argv[1];assert script in ['soil_dispersion_diag.py','soil_iidwin_floor_check.py']
for n,h in json.loads((P/'FREEZE.json').read_text())['sha256'].items():assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,n
outdir=P/'reproduction';outdir.mkdir(exist_ok=True);prefix=outdir/script.removesuffix('.py');stdout=prefix.with_suffix('.stdout.txt');stderr=prefix.with_suffix('.stderr.txt');receipt=prefix.with_suffix('.receipt.json');assert not stdout.exists() and not stderr.exists() and not receipt.exists()
begin=time.perf_counter()
with stdout.open('w') as a,stderr.open('w') as b:r=subprocess.run([sys.executable,str(P/'run_original.py'),script],stdout=a,stderr=b,timeout=180)
expected=P/'originals'/(script.removesuffix('.py')+'_output.txt');observed=stdout.read_bytes();original=expected.read_bytes()
record={'script':script,'exit_code':r.returncode,'seconds':time.perf_counter()-begin,'stdout_exactly_matches_saved_output':observed==original,'saved_output_sha256':hashlib.sha256(original).hexdigest(),'reproduced_stdout_sha256':hashlib.sha256(observed).hexdigest(),'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__,'adaptation':'only exact hardcoded sourcepath remap; unchanged archived script, same seeds and parameters','independent_model_replication':False}
receipt.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record));assert r.returncode==0
