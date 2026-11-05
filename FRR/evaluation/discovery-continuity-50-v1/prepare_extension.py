"""Prepare the separately recorded30-entry extension only after a passing review at370."""
from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';ENV=G/'cycle3/environment';OUT=ROOT/'evaluation/discovery-continuity-to-400-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 review=json.loads((R/'REVIEW_370.json').read_text());assert review['continue_to_400'] is True and review['integrity_status']=='pass'
 s=json.loads((ENV/'STATE.json').read_text());v=json.loads((ENV.parent/'CURRENT_VERIFY.json').read_text());assert s['next_step']==370==v['next_step'] and (ENV/'PAUSE').exists() and not (ENV/'RUN.lock').exists();assert json.loads((ENV.parent/v['checks']).read_text())['status']=='pass'
 OUT.mkdir();(OUT/'before').mkdir()
 for p in (ROOT/'CURRENT_HANDOFF.md',ROOT/'sync/CURRENT_ORIENTATION.md',ROOT/'evaluation/CURRENT_RESEARCH_MAP.md'):shutil.copy2(p,OUT/'before'/p.name)
 (OUT/'PRIMARY_BEFORE.json').write_text(json.dumps({str(p.relative_to(ROOT)):sha(p) for p in G.rglob('*') if p.is_file() and '__pycache__' not in p.parts},indent=2)+'\n')
 source=(R/'run_block.py').read_text();replacements=[('320→370','370→400'),("x['step']>=320","x['step']>=370"),('target-320','target-370'),('[:320]','[:370]'),('start=320','start=370'),('old_320_notebook_exact_prefix','old_370_notebook_exact_prefix'),('if target in (340,360,370):','if target in (390,400):'),('new entries since320','new entries since370'),('default=370','default=400'),('range(325,371,5)','range(375,401,5)'),('range(320,371,5)','range(370,401,5)'),('current!=320','current!=370')]
 for a,b in replacements:
  assert source.count(a)==1,(a,source.count(a));source=source.replace(a,b)
 compile(source,'extension_run_block.py','exec');(OUT/'run_block.py').write_text(source)
 (OUT/'PLAN.json').write_text(json.dumps({'start':370,'target':400,'entries':30,'windows':list(range(375,401,5)),'broad_reports':[390,400],'condition_changes':[],'same_primary':True,'environment_version':'discovery-play-patch-v1','authorization':'Conditional user extension after ordinary observations and passing review at370','review_path':'../discovery-continuity-50-v1/REVIEW_370.json','original_driver_sha256':sha(R/'run_block.py'),'driver_transformations':replacements,'source_world_activation_stays':305,'stop':'400or earlier integrity/resource failure; no retries'},indent=2)+'\n')
 print('Prepared separate370→400continuation; no model generation performed by preparation.')
if __name__=='__main__':main()
