"""Freeze a subsequent detached cycle only after the preceding readout exists."""
from pathlib import Path
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parent

def freeze(n):
    assert n in (2,3)
    prior=ROOT/f'cycle{n-1}'
    out=json.loads((prior/'READOUT.json').read_text())
    assert out['status']=='pass' and out['actual_model_calls']==6
    assert not any((prior/'run'/p).exists() for p in ('PENDING.json','RUN.lock','PREPARATION_PENDING.json'))
    if n==2:
        cfg={'question':'partition stable mechanics and initial observation between roles',
             'arms':['system_all','split'],'layouts':{'system_all':'system_all','split':'split'},'FRR_arm':None,
             'decision_basis':'cycle1 changes output form under role/position relocation; now separate law text from observed data without adding content or asking for action'}
    else:
        cfg={'question':'compact FRR recontact under explicit law/observation role partition',
             'arms':['control','compact'],'layouts':{'control':'split','compact':'split'},'FRR_arm':'compact',
             'decision_basis':'split layout separates mechanics from initial data; selected for explicit structure, not presumed operational superiority; concurrent matched context contact'}
    cfg.update(planned_calls=6,prior_readout_sha256=hashlib.sha256((prior/'READOUT.json').read_bytes()).hexdigest(),
               physical_parent='actual main1630, not the preceding experimental branch',
               prior_observed={arm:{k:v for k,v in row.items() if k in ('unique_output_token_sequences','complete_cells','incomplete_fences','model_initiated_actions')} for arm,row in out['arms'].items()})
    d=ROOT/f'cycle{n}'/'design';d.mkdir(parents=True,exist_ok=False)
    for name in ('mechanics_user.txt','world_rules.txt','compact_frr.md','full_frr_reference.md'):
        (d/name).write_bytes((ROOT/'cycle1/design'/name).read_bytes())
    (d/'CONDITION.json').write_text(json.dumps(cfg,indent=2)+'\n')
    (d/'PROTOCOL.md').write_text((ROOT/'PLAN.md').read_text()+'\n## Frozen current condition\n\n'+json.dumps(cfg,indent=2)+'\n\nSame fresh main1630 clone, body, literal parser, initial-only sensing, runtime-feedback wrapper, full realized branch history, six-call limit and integrity policy. No behavior or semantic success gate. Role/position/empty-message/continuation cues remain treatment components; cycle3 also adds compact FRR length/content. No claim of pure mechanism or neutral padding. Both supported starting worlds and initial packets must match. Full source FRR remains external.\n')
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.iterdir()) if p.is_file()}
    (d/'DESIGN_FREEZE.json').write_text(json.dumps({'status':'frozen_after_prior_readout_before_current_prepare_or_inference','sha256':hashes},indent=2)+'\n')
    print(json.dumps(cfg))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cycle',type=int,choices=(2,3),required=True);a=p.parse_args();freeze(a.cycle)
