"""Construct/install a versioned primary adapter. Default inspection makes no primary writes."""
from pathlib import Path
from dataclasses import asdict
import argparse,hashlib,json,sys,subprocess
PACKAGE=Path(__file__).resolve().parent;ROOT=PACKAGE.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';DEFAULT_ENV=G/'cycle3/environment';sys.path.insert(0,str(G))
from world import Rules
from journal import immutable

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def check_bundle():
 for rel,h in json.loads((PACKAGE/'BUNDLE_FREEZE.json').read_text())['files'].items():
  if sha(PACKAGE/rel)!=h:raise ValueError('Prepared bundle changed:'+rel)
def candidate_source(env):
 env=Path(env).resolve();s=(G/'boundary_routine.py').read_text()
 def replace(a,b,count=1):
  nonlocal s
  if s.count(a)!=count:raise ValueError('Unexpected source revision:'+a)
  s=s.replace(a,b)
 replace("ENV=R/'cycle3/environment'",f'ENV=Path({str(env)!r})')
 replace("NEW_VERSION='generation-boundary-view-v1'\nNEW_MANIFEST='ENVIRONMENT_BOUNDARY_V1.json'","BOUND_VERSION='generation-boundary-view-v1'\nBOUND_MANIFEST='ENVIRONMENT_BOUNDARY_V1.json'\nNEW_VERSION='discovery-play-patch-v1'\nNEW_MANIFEST='ENVIRONMENT_DISCOVERY_PATCH_V1.json'")
 # Source/legacy dependencies keep their actual frozen locations; data and verification target only selected environment.
 replace('R=Path(__file__).resolve().parent;',f'R=Path({str(G)!r});')
 s='import sys\nsys.path.insert(0,'+repr(str(G))+')\nsys.path.insert(0,'+repr(str(PACKAGE))+')\n'+s
 insertion='''from primary_adapter import Binding as PatchBinding
from world import Rules as PatchRules

def patch_binding():
 config=json.loads((ENV/NEW_MANIFEST).read_text())
 return PatchBinding(config['world_activation_step'],PatchRules(**config['world_rules']))
def world_view_render(events):return patch_binding().render(boundary_view_render(events),events)
def world_dispatch(text,events):return patch_binding().dispatch(text,events,boundary_dispatch)
'''
 replace('def recorded_render(events,version):',insertion+'def recorded_render(events,version):')
 replace(' if version==NEW_VERSION:return boundary_view_render(events)',' if version==NEW_VERSION:return world_view_render(events)\n if version==BOUND_VERSION:return boundary_view_render(events)')
 replace(' if version==NEW_VERSION:return boundary_dispatch(text,events)',' if version==NEW_VERSION:return world_dispatch(text,events)\n if version==BOUND_VERSION:return boundary_dispatch(text,events)')
 start=s.index('def run(');end=s.index('def verify():');part=s[start:end].replace('q=boundary_view_render(events)','q=world_view_render(events)').replace("host_result=boundary_dispatch(row['text'],events)","host_result=world_dispatch(row['text'],events)");s=s[:start]+part+s[end:]
 replace("version in ('seed-shelf-capacity-v1','archive-view-v1',FUND_VERSION,NEW_VERSION)","version in ('seed-shelf-capacity-v1','archive-view-v1',FUND_VERSION,BOUND_VERSION,NEW_VERSION)")
 replace("{NEW_VERSION:NEW_MANIFEST,FUND_VERSION:FUND_MANIFEST","{NEW_VERSION:NEW_MANIFEST,BOUND_VERSION:BOUND_MANIFEST,FUND_VERSION:FUND_MANIFEST")
 replace("version in ('archive-view-v1',FUND_VERSION,NEW_VERSION)","version in ('archive-view-v1',FUND_VERSION,BOUND_VERSION,NEW_VERSION)",2)
 replace('def wait_pacing(path,delay):'," for p,h in json.loads((ENV/'POLICY_WORLD_FREEZE.json').read_text())['files'].items():assert sha(Path(p))==h,p\ndef wait_pacing(path,delay):")
 s=s.replace("R/'cycle3/CURRENT_VERIFY.json'","ENV.parent/'CURRENT_VERIFY.json'").replace("R/'cycle3'/","ENV.parent/").replace("R/'cycle3/verification'","ENV.parent/'verification'").replace("R/f'cycle3/{name}.json'","ENV.parent/f'{name}.json'")
 compile(s,'prepared_world_routine.py','exec');return s

def plan(env=DEFAULT_ENV):
 check_bundle();env=Path(env).resolve();s=json.loads((env/'STATE.json').read_text());base=env/'ENVIRONMENT_BOUNDARY_V1.json';latest=json.loads((env.parent/'CURRENT_VERIFY.json').read_text())
 if s['next_step']!=305 or latest['next_step']!=305 or s['manifest_sha256']!=sha(base):raise ValueError('Requires exact prepared boundary305and active boundary-visible policy; prepare a new version if it advanced')
 if not (env/'PAUSE').exists() or (env/'RUN.lock').exists() or (env/'plans/000305.json').exists():raise ValueError('Primary not safely paused/clear')
 if json.loads((env.parent/latest['checks']).read_text())['status']!='pass':raise ValueError('Passing saved verification required')
 return dict(scope='PREPARED ONLY; no primary writes/modelcalls',activation_step=305,base_manifest_sha256=sha(base),world_rules_sha256=Rules().fingerprint(),public_controls=['LOOK','TOUCH A','TOUCH B'],private_rules='Observer artifacts/code only; not rendered to model',canonical_state_authority='Primary immutable action receipts, no second world journal',candidate_sha256=hashlib.sha256(candidate_source(env).encode()).hexdigest())

def activate(env=DEFAULT_ENV,destination=None):
 env=Path(env).resolve();info=plan(env);destination=Path(destination) if destination else G/'world_routine.py'
 if destination.exists() or (env/'ENVIRONMENT_DISCOVERY_PATCH_V1.json').exists() or (env/'POLICY_WORLD_FREEZE.json').exists():raise FileExistsError('Activation artifacts already exist; no overwrite/reinitialization')
 # All validation before mutation. New files use exclusive creation; existing event/history bytes never edited.
 old=json.loads((env/'ENVIRONMENT_BOUNDARY_V1.json').read_text());rules=Rules();manifest=dict(old,version='discovery-play-patch-v1',previous_manifest_sha256=info['base_manifest_sha256'],transition_step=305,world_activation_step=305,world_rules=asdict(rules),world_rules_sha256=rules.fingerprint(),world_package=str(PACKAGE),change_scope='Optional deterministic stateful numeric patch plus minimal controls/observable receipts; no rule formulas in model view. Prior stop visibility and all older inputs preserved.')
 with destination.open('x') as f:f.write(candidate_source(env))
 immutable(env/'ENVIRONMENT_DISCOVERY_PATCH_V1.json',manifest)
 files={str(PACKAGE/rel):h for rel,h in json.loads((PACKAGE/'BUNDLE_FREEZE.json').read_text())['files'].items()};files[str(env/'ENVIRONMENT_DISCOVERY_PATCH_V1.json')]=sha(env/'ENVIRONMENT_DISCOVERY_PATCH_V1.json');files[str(destination)]=sha(destination);immutable(env/'POLICY_WORLD_FREEZE.json',dict(scope='Frozen world policy before any modelcalls; old primary integrity enforced by inherited freezes',files=files))
 code="import importlib.util,sys; sys.path.insert(0,"+repr(str(G))+"); s=importlib.util.spec_from_file_location('prepared_world',"+repr(str(destination))+"); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.freeze_check(); m.Journal(m.ENV).project(); m.verify()"
 subprocess.run(['/workspace/cache_backend_venv/bin/python','-c',code],check=True,capture_output=True,text=True)
 return dict(status='activated_paused_no_model_generation',environment=str(env),runner=str(destination),next_step=305,verification=json.loads((env.parent/'CURRENT_VERIFY.json').read_text())['verification'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--activate',action='store_true');a=p.parse_args();print(json.dumps(activate() if a.activate else plan(),indent=2))
