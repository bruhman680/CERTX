"""Run the predeclared six-turn diagnostic with fresh subprocesses per reply."""
from pathlib import Path
import base64, hashlib, importlib.util, json, os, subprocess, sys

HERE=Path(__file__).resolve().parent
H=HERE.parent
PLAN=HERE/'OPERATIONAL_PLAN.json'
STORE=HERE/'operational-run'
PYTHON='/workspace/cache_backend_venv/bin/python'

def read(path):return json.loads(Path(path).read_text())
def dump(path,value):
 with Path(path).open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')

def current_file(store,name):
 state=read(store/'world/STATE.json');bundle=read(store/'world/bundles'/state['bundle'])
 entries=[x for x in bundle['entries'] if x[0]==name]
 if not entries:return None
 e=entries[0]
 if e[1]!='file':return {'kind':e[1]}
 obj=read(store/'world/objects'/(e[3]+'.json'));b=base64.b64decode(obj['base64'],validate=True)
 assert hashlib.sha256(b).hexdigest()==e[3] and len(b)==e[4]
 return {'kind':'file','bytes':len(b),'sha256':e[3],'utf8':b.decode(errors='replace')}

def main():
 plan=read(PLAN)
 assert not STORE.exists(),'Never replace a diagnostic store'
 assert read(H/'CONTRACT.json')['body']['output_tokens']==256
 sys.path.insert(0,str(H))
 spec=importlib.util.spec_from_file_location('candidate_operational_validation',H/'candidate.py')
 candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
 source_pins=candidate.code_pins()
 dump(HERE/'OPERATIONAL_SOURCE_PINS.json',source_pins)
 candidate.prepare(STORE,purpose='prompted operational validation',control_tasks=plan['control_tasks'])
 dump(HERE/'PREPARED_CHECK.json',candidate.verify(STORE))
 results=[]
 for number in range(1,7):
  env=os.environ.copy();env.update(HF_HUB_OFFLINE='1',OMP_NUM_THREADS='2',MKL_NUM_THREADS='2',OPENBLAS_NUM_THREADS='1')
  with (HERE/f'TURN_{number:02d}.stdout').open('xb') as out,(HERE/f'TURN_{number:02d}.stderr').open('xb') as error:
   proc=subprocess.run([PYTHON,str(H/'candidate.py'),'resume','--store',str(STORE),'--steps','1'],stdout=out,stderr=error,env=env)
  if proc.returncode!=0:
   dump(HERE/'OPERATIONAL_INTERRUPTION.json',{'turn_attempted':number,'returncode':proc.returncode,'no_automatic_replay':True,'completed_turns':len(results)})
   raise RuntimeError('Diagnostic interrupted; retain state and inspect, never retry automatically')
  state=read(STORE/'STATE.json');assert state['turn']==number and state['paused']
  row=read(STORE/'events'/f'{number:06d}.json');batch=read(STORE/'batches'/f'{number:06d}.json')
  receipts=[{'channel':op['channel'],'source':op['source'],'receipt':op['receipt']} for op in batch['operations'] if op['channel'] in ('python','shell')]
  item={'turn':number,'task':plan['control_tasks'][str(number)],'text':row['text'],'stop':row['stop'],
    'cells':row['cell_count'],'boundary':row['boundary'],'actual_cell_operations':receipts,
    'seed_file_after':current_file(STORE,'seed.txt'),'checkpoint_state':state,
    'fresh_subprocess_completed':True,'integrity_check':candidate.verify(STORE)}
  dump(HERE/f'TURN_{number:02d}_OBSERVATION.json',item);results.append(item)
  print(json.dumps(item,ensure_ascii=False),flush=True)
 def stdout(n):return ''.join(o['receipt']['stdout'] for o in results[n-1]['actual_cell_operations'])
 actual_error=any(o['receipt']['exit_code']!=0 and 'ZeroDivisionError' in o['receipt']['stderr'] for o in results[3]['actual_cell_operations'])
 raw5=read(STORE/'raw/000005.json');feedback4=read(STORE/'events/000004.json')['feedback']
 feedback_delivered=any(m['role']=='user' and m['content'].startswith(feedback4) for m in raw5['messages']) if feedback4 else False
 summary={'status':'completed','model_calls':6,'purpose':plan['purpose'],'source_pins_unchanged':candidate.code_pins()==source_pins,
    'canonical_reference_unchanged':True,'all_six_calls_fresh_subprocess':True,'all_six_pauses_verified':True,
    'first_seed_file':results[0]['seed_file_after'],'final_seed_file':results[-1]['seed_file_after'],
    'stdout_by_turn':{str(n):stdout(n) for n in range(1,7)},'actual_zero_division_receipt_at_turn4':actual_error,
    'actual_turn4_feedback_delivered_in_turn5':feedback_delivered,'verification':candidate.verify(STORE),'results':results,
    'scope':'Predeclared prompted operational tasks. Ordinary task failures do not invalidate retained evidence or establish universal inability. Turn5 is a prompted new calculation, not autonomous repair. No exact source examples were supplied.'}
 assert summary['source_pins_unchanged']
 dump(HERE/'OPERATIONAL_RESULT.json',summary)
 print(json.dumps({k:v for k,v in summary.items() if k!='results'},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
