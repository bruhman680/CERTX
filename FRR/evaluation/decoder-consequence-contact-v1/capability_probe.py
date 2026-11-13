"""Operator-written boundary isolation, separate from model output."""
from pathlib import Path
import sys,json,hashlib
H=Path(__file__).resolve().parent;C=H.parent/'minimal-garden-candidate-v1'
sys.path.insert(0,str(C/'world'))
from garden_world import GardenWorld,verify_store
def inv():
    return {str(p.relative_to(C/'run')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (C/'run').rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def main():
    before=inv()
    cells=[('pure_python','print(sum(range(10)))'),
           ('semaphore','import multiprocessing\ns = multiprocessing.Semaphore(1)\nprint("semaphore created")'),
           ('subprocess','import subprocess, sys\nr = subprocess.run([sys.executable, "-c", "print(45)"], capture_output=True, text=True)\nprint(r.returncode, r.stdout.strip())')]
    (H/'CAPABILITY_PLAN.json').write_text(json.dumps({'role':'operator diagnostic only; never model-facing',
      'reason':'isolate sandbox IPC limitation from general Python availability after sampled Pool failed',
      'cells':cells,'parent':'canonical initial world checkpoint 000001; independent copy'},indent=2)+'\n')
    w=GardenWorld.create(H/'capability_world',C/'run/world/bundles/000001.json',C/'run/world/objects')
    rows=[]
    try:
        for label,source in cells:
            event=w.apply('python',source)
            rows.append({'label':label,'source':source,'feedback':event['feedback'],'changed_paths':event['changed_paths']})
    finally:w.close()
    assert before==inv()
    (H/'CAPABILITY_RESULTS.json').write_text(json.dumps({'rows':rows,'canonical_run_unchanged':True,
        'verification':verify_store(H/'capability_world'),'model_calls':0},indent=2)+'\n')
if __name__=='__main__':main()
