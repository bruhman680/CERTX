"""Post-run RR2 arithmetic and HG1 fixture checks; no actor/model calls."""
import hashlib
import json
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'evaluation/reset-reader-rr2'


def fraction_stationary(kernel):
    # Separately construct the h=1 chain and solve by rational elimination.
    p=[[F(0) for _ in range(4)] for _ in range(4)]
    for y in (0,1):
        for e in (0,1):
            for yn in (0,1):
                p[2*y+e][2*yn+y]=kernel[e][y][yn]
    matrix=[[p[i][j]-F(i==j) for i in range(4)]+[F(0)] for j in range(3)]
    matrix.append([F(1)]*5)
    for j in range(4):
        pivot=next(i for i in range(j,4) if matrix[i][j])
        matrix[j],matrix[pivot]=matrix[pivot],matrix[j]
        divisor=matrix[j][j];matrix[j]=[x/divisor for x in matrix[j]]
        for i in range(4):
            if i!=j:
                factor=matrix[i][j];matrix[i]=[a-factor*b for a,b in zip(matrix[i],matrix[j])]
    return [row[-1] for row in matrix]


def decimal(x):
    return Decimal(x.numerator)/Decimal(x.denominator)


def exact_one_step(kernel, weights):
    pi=fraction_stationary(kernel)
    natural=[x/sum(pi[:2]) for x in pi[:2]]
    priors=[natural,[pi[0]+pi[2],pi[1]+pi[3]],[F(1),F(0)],[F(0),F(1)],[F(1,2)]*2]
    emissions=[kernel[e][0] for e in (0,1)]
    marginal=[sum(weights[z]*priors[z][e] for z in range(5)) for e in (0,1)]
    q=[sum(marginal[e]*emissions[e][y] for e in (0,1)) for y in (0,1)]
    qz=[[sum(priors[z][e]*emissions[e][y] for e in (0,1)) for y in (0,1)] for z in range(5)]
    with localcontext() as context:
        context.prec=60
        kl=lambda p,q:sum(decimal(p[y])*(decimal(p[y])/decimal(q[y])).ln() for y in (0,1))
        group=[sum(decimal(priors[z][e])*kl(emissions[e],q) for e in (0,1)) for z in range(5)]
        metadata=sum(decimal(weights[z])*sum(decimal(priors[z][e])*kl(emissions[e],qz[z]) for e in (0,1)) for z in range(5))
        population=sum(decimal(weights[z])*group[z] for z in range(5))
        return dict(metadata=float(metadata),population=float(population),fixed_e0=float(group[2]))


def main():
    result=json.loads((OUT/'RESULTS.json').read_text());summary=result['summary']
    manifest=json.loads((OUT/'LAUNCH_MANIFEST.json').read_text())
    if manifest['files']!=summary['input_sha256']:
        raise ValueError('Launch/result hash disagreement')
    for f,sha in manifest['files'].items():
        if hashlib.sha256((ROOT/f).read_bytes()).hexdigest()!=sha:raise ValueError('Changed input: '+f)
    if len(result['aggregate'])!=405 or len(result['components'])!=2025 or not summary['algebraic_and_integrity_checks_pass']:
        raise ValueError('RR2 checks failed')
    if json.loads((OUT/'RUN_STDOUT.txt').read_text())!=summary or (OUT/'RUN_STDERR.txt').read_text():
        raise ValueError('Run log mismatch')
    models=json.loads((ROOT/'evaluation/reset-reader-study/MODELS.json').read_text())
    kernel=[[[F(str(x)) for x in row] for row in env] for env in models['transfer_b']['kernel']]
    witnesses=[]
    for name,weights in [('balanced',[F(1,5)]*5),('fixed_e1_heavy',[F(1,20)]*3+[F(4,5),F(1,20)])]:
        values=exact_one_step(kernel,weights)
        observed=next(r for r in result['aggregate'] if r['model']=='transfer_b' and r['h']==1 and r['population']==name and r['t']==0)
        for key in ['metadata','population']:
            if abs(values[key]-observed['risks_nats'][key])>1e-14:raise ValueError('Exact witness mismatch')
        component=next(r for r in result['components'] if r['model']=='transfer_b' and r['h']==1 and r['population']==name and r['t']==0 and r['preparation']=='fixed_e0')
        if abs(values['fixed_e0']-component['risks_nats']['population'])>1e-14:raise ValueError('Conditional witness mismatch')
        witnesses.append(dict(population=name,values=values))
    fixtures=ROOT/'evaluation/hpgm-gates-study/development-fixtures'
    fm=json.loads((fixtures/'MANIFEST.json').read_text())
    for f,sha in fm['files'].items():
        if hashlib.sha256((fixtures/f).read_bytes()).hexdigest()!=sha:raise ValueError('Fixture changed')
    keys=json.loads((fixtures/'ANSWER_KEYS.json').read_text())
    updates=json.loads((fixtures/'READER_UPDATES.json').read_text())
    if set(keys)!=set(updates) or len(keys)!=8:raise ValueError('Fixture coverage mismatch')
    for i in keys:
        packet=json.loads((fixtures/(i+'.json')).read_text())
        if set(packet)!={'case_id','exposure','family','task','evidence'}:raise ValueError('Actor packet contains unexpected fields')
    arms=json.loads((fixtures/'ARM_TEMPLATES.json').read_text())
    a,b=arms['functional'],arms['hpgm']
    for stage in ['first','second']:
        normalize=lambda s:'\n'.join(line.split(': ',1)[-1] if ': ' in line and line.split(': ',1)[0] in ['Stage 1','Stage 2','Stage 3','Stage 4','Stage 5','Stage 6','COUPLE','OBSERVE','ORIENT','PLAY','PRACTICE','DREAM'] else line for line in s.splitlines())
        if normalize(a[stage])!=normalize(b[stage]):raise ValueError('Operation contrast differs beyond labels')
    for f,sha in json.loads((ROOT/'evaluation/PRE_REFINEMENT_BASELINE_HASHES.json').read_text()).items():
        if hashlib.sha256((ROOT/f).read_bytes()).hexdigest()!=sha:raise ValueError('Core changed')
    receipt=dict(scope='Post-run selected rational/60-digit arithmetic check and authored-fixture integrity; shared model definitions, not independent replication or actor efficacy.',
        protocol_commit_before_execution='dd40eba8523ea5654a919fbd7554276f3794ca9e',main_run_exit_code=0,
        aggregate_cells=405,component_cells=2025,primary_run_seconds=summary['elapsed_seconds'],
        launch_hashes_match=True,selected_post_run_witnesses=witnesses,fixture_packets=8,
        actor_packets_exclude_key_and_future_update_fields=True,functional_operations_equal_after_heading_removal=True,
        core_hashes_unchanged=True,actor_or_reader_runs=0,
        remaining_hg1=['Independent task families or explicit authored-pilot amendment','Final scoring/parser review','Model/settings/cost and access setup','Prospective launch'])
    (OUT/'VALIDATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    main()
