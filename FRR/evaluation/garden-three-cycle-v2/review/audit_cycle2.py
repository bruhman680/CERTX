"""Rational independent decision audit plus final-source replay in owned sandbox."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,subprocess,sys,shutil
D=Path(__file__).resolve().parent;P=D.parent/'cycle2'
j=json.loads((P/'RESULTS.json').read_text());maxerr=0.;records=[]
def pol(q,v):return (1-q)*(1-v)+q*(F(3,20)+F(2,5)*v)
def risk(q,L,U):return max(pol(q,L),pol(q,U))
def reg(q,L,U):return max(pol(q,v)-min(pol(F(0),v),pol(F(1),v)) for v in (L,U))
for r in j['rows']:
 L,U=map(lambda x:F(str(x)),r['interval']);threshold=F(17,28)
 if U<=threshold:qloss=qreg=F(1)
 elif L>=threshold:qloss=qreg=F(0)
 else:
  qloss=F(5,7)
  qreg=(F(17,20)-F(7,5)*L)/(F(7,5)*(U-L))
 expected={'minimax_loss_fallback_probability':qloss,'minimax_loss':risk(qloss,L,U),'pure_minimax_loss':min(risk(F(0),L,U),risk(F(1),L,U)),'minimax_regret_fallback_probability':qreg,'minimax_regret':reg(qreg,L,U),'pure_minimax_regret':min(reg(F(0),L,U),reg(F(1),L,U))}
 for key,value in expected.items():maxerr=max(maxerr,abs(float(value)-r[key]))
 ps=[]
 for p in r['probes']:
  k,d=F(str(p['cost'])),F(str(p['damage_probability']));vals=[]
  for v in (L,U):
   # Direct state/erasure outcomes, with state-specific oracle action.
   total=F(0)
   for s in (0,1):
    for erase in (0,1):
     probability=(v if s else 1-v)*(d if erase else 1-d)
     post=s*(1-erase);cost=k+s*erase+min(F(1-post),F(3,20)+F(2,5)*post)
     total+=probability*cost
   vals.append(total)
  actual=max(vals);maxerr=max(maxerr,abs(float(actual)-p['worst_expected_loss']))
  if bool(actual<risk(qloss,L,U))!=p['prefer_probe_by_worst_loss']:raise AssertionError('probe choice')
  ps.append({'k':str(k),'d':str(d),'exact_worst_expected_loss':str(actual)})
 records.append({'interval':[str(L),str(U)],'exact_q_minimax_loss':str(qloss),'exact_q_minimax_regret':str(qreg),'probe_replay':ps})
# Full final-source replay writes only within owned review sandbox.
sandbox=D/'source_replay';(sandbox/'cycle1').mkdir(parents=True,exist_ok=True);(sandbox/'cycle2').mkdir(exist_ok=True)
for src,dst in [(D.parent/'cycle1/RESULTS.json',sandbox/'cycle1/RESULTS.json'),(P/'PROTOCOL.md',sandbox/'cycle2/PROTOCOL.md'),(P/'run.py',sandbox/'cycle2/run.py')]:shutil.copyfile(src,dst)
proc=subprocess.run([sys.executable,str(sandbox/'cycle2/run.py')],capture_output=True,text=True)
(D/'SOURCE_REPLAY.stdout.txt').write_text(proc.stdout);(D/'SOURCE_REPLAY.stderr.txt').write_text(proc.stderr)
replayed=(sandbox/'cycle2/RESULTS.json').read_bytes();expected_bytes=(P/'RESULTS.json').read_bytes()
checks={'independent_rational_results':maxerr<1e-12,'final_source_exit0':proc.returncode==0,'final_source_replay_byte_identical':replayed==expected_bytes,'protocol_bound':hashlib.sha256((P/'PROTOCOL.md').read_bytes()).hexdigest()==j['protocol_sha256'],'cycle1_bound':hashlib.sha256((D.parent/'cycle1/RESULTS.json').read_bytes()).hexdigest()==j['source_cycle1_sha256'],'main_checks_pass':all(j['checks'].values())}
out={'scope':'Independent rational endpoint/state-enumeration audit plus byte replay; same authored loss/model, no empirical action validation','max_float_difference_from_rational':maxerr,'records':records,'source_replay_sha256':hashlib.sha256(replayed).hexdigest(),'source_replay_returncode':proc.returncode,'checks':checks}
(D/'CYCLE2_AUDIT.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps(out,indent=2,allow_nan=False));assert all(checks.values())
