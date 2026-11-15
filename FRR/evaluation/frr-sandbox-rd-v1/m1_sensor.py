"""Separate initial-directory perception contrast; no new task or main activation."""
from pathlib import Path
import json,importlib.util,hashlib
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('unchanged_frr_pilot_engine',ROOT/'pilot.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
H=ROOT/'m1'

def main():
    assert (ROOT/'pilot/REPORT.md').exists() and p.c.read(ROOT/'pilot/AUDIT.json')['status']=='pass'
    assert not (H/'INTERVENTION_PLAN.json').exists(),'No replay into old M1'
    ms=p.c.read(p.M/'run/world/STATE.json')
    assert p.c.read(p.M/'run/world/bundles'/ms['bundle'])==p.c.read(ROOT/'pilot/PARENT_WORLD.json')
    initial=p.c.read(ROOT/'pilot/branches/control/world/bundles/000001.json')
    for arm in ['compact','full']:
        assert p.c.read(ROOT/'pilot/branches'/arm/'world/bundles/000001.json')==initial
    entries=[{'name':x[0],'type':x[1],'bytes':x[4] if x[1]=='file' else None} for x in initial['entries']]
    assert len(entries)==5
    packet={'snapshot':'initial, before model replies','directory':'/world','entries':entries}
    H.mkdir()
    for folder in ['interface','frr']:(H/folder).mkdir()
    (H/'interface/mechanics_user.txt').write_text((ROOT/'interface/mechanics_user.txt').read_text()+'\n\n'+json.dumps(packet,ensure_ascii=False,sort_keys=True))
    for src,dest in [('interface/world_rules.txt','interface/world_rules.txt'),('frr/candidate.md','frr/candidate.md'),('frr/full_source_reference.md','frr/full_source_reference.md')]:
        (H/dest).write_bytes((ROOT/src).read_bytes())
    p.c.save(H/'INITIAL_SNAPSHOT.json',{'actor':'operator-derived observation','source_bundle_id':initial['id'],'source_bundle':'../pilot/branches/control/world/bundles/000001.json','packet':packet,'initial_only':True,'future_changes_not_updated':True})
    p.c.save(H/'INTERVENTION_PLAN.json',{'date':'2026-11-14 America/Chicago','question':'What changes when every arm receives the same actual initial directory snapshot in addition to the same mechanical description?','decision_after_M0':True,'M0_results_frozen':True,'justification':'separate explicit perception factor already identified in design; not a semantic failure gate or proof of plateau','model_calls_planned':9,'arms':['control','compact','full'],'turns_per_arm':3,'changed_input':'append shared JSON initial snapshot listing all five actual file names/types/byte sizes; no file contents, selected target, command, task or hint','physical_world':'same pre-model M0 supported world after common mechanical rule replacement, not post-M0 notebooks','history':'fresh in all arms, then all actual branch pairs; no pruning/coaching','unchanged':'weights,decoder,outputcap,mechanics prefix,FRR strings,world rules,physical limits','confounds':'added names,information,JSONform,length and position all change; whole presentation/perception effect, not pure semantics or independent replication','same_engine':str(ROOT/'pilot.py'),'same_engine_sha256':p.c.sha(ROOT/'pilot.py'),'wrapper_sha256':p.c.sha(Path(__file__)),'no_automatic_escalation':True,'main_entry':1630,'activation':False})
    p.H=H
    p.main()
    checks=p.c.read(H/'pilot/PREPARATION_CHECKS.json')
    assert all(x['world_id']==initial['id'] for x in checks['conditions'])
    assert p.c.sha(Path(__file__))==p.c.read(H/'INTERVENTION_PLAN.json')['wrapper_sha256']

if __name__=='__main__':main()
