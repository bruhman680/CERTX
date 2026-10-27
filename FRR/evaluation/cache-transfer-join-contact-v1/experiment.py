"""Authored exact join fixtures; not a sensor parser or C2C implementation."""
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import hashlib, json, math

ROOT = Path(__file__).resolve().parent
STATUSES = ('applicable','absent_assignment','wrong_channel','wrong_date','wrong_unit','conflicting_assignment')

def decide(records):
    data = [r for r in records if 'samples' in r]
    calibrations = [r for r in records if 'correction' in r]
    assignments = [a for r in records for a in r.get('assignments', [])]
    if len(data) != 1 or len(calibrations) != 1:
        return {'action':'UNRESOLVED','reason':'missing measurement or calibration','bound':None}
    d,c = data[0],calibrations[0]
    relevant = [a for a in assignments if a['task'] == 'TASK']
    expected = {'task':'TASK','channel':d['channel'],'date':d['date'],'unit':d['unit']}
    if not relevant:
        reason = 'missing assignment'
    elif any(a != expected for a in relevant):
        reason = 'mismatched or conflicting assignment'
    elif any(c[k] != d[k] for k in ('channel','date','unit')):
        reason = 'inapplicable calibration'
    else:
        x = max(map(F,d['samples'])) + F(c['correction'])
        lo,hi = x-F(c['radius']),x+F(c['radius'])
        action = 'RELEASE' if hi <= F('7.5') else 'HOLD' if lo > F('7.5') else 'UNRESOLVED'
        return {'action':action,'reason':'complete applicable join','bound':[str(lo),str(hi)]}
    return {'action':'UNRESOLVED','reason':reason,'bound':None}

def build(raw, status, layout):
    a = {'task':'TASK','channel':'K9','date':'DAY7','unit':'mm/s'}
    d = {'id':'D','channel':'K9','date':'DAY7','unit':'mm/s','samples':['6.0',raw,'6.2']}
    c = {'id':'C','channel':'K9','date':'DAY7','unit':'mm/s','correction':'0.2','radius':'0.1'}
    assignments = [a]
    if status == 'absent_assignment': assignments = []
    elif status == 'conflicting_assignment': assignments += [dict(a,channel='K8')]
    elif status == 'wrong_channel': c['channel']='K8'
    elif status == 'wrong_date': c['date']='DAY6'
    elif status == 'wrong_unit': c['unit']='cm/s'
    (d if layout == 'split' else c)['assignments'] = assignments
    return [d,c]

def main():
    inputs, outputs = [], []
    counts = {'RELEASE':0,'HOLD':0,'UNRESOLVED':0}
    order_checks = ablations = endpoint_checks = 0
    for raw,status,layout in product(('6.8','7.8'),STATUSES,('split','combined')):
        records = build(raw,status,layout)
        case = f'{raw}/{status}/{layout}'
        inputs.append({'case':case,'records':records})
        expected_action = ('RELEASE' if raw == '6.8' else 'HOLD') if status == 'applicable' else 'UNRESOLVED'
        result = decide(records)
        assert result['action'] == expected_action, (case,result)
        counts[result['action']] += 1
        for order in permutations(records):
            assert decide(order) == result
            order_checks += 1
        for record in records:
            assert decide([record])['action'] == 'UNRESOLVED'
            ablations += 1
        if status == 'applicable':
            # Independent integer-tenths construction of the max interval endpoints.
            values = [int(F(s)*10) for s in records[0]['samples']]
            interval = [str(F(max(values)+1,10)),str(F(max(values)+3,10))]
            assert result['bound'] == interval
            endpoint_checks += 1
        else:
            assert result['bound'] is None
        outputs.append({'case':case,**result})
    assert counts == {'RELEASE':2,'HOLD':2,'UNRESOLVED':20}
    schedules = [{'progress':p,'paper_linear':1 + (.001-1)*p,'code_exponential':.001**p} for p in (0,.5,1)]
    assert math.isclose(schedules[1]['paper_linear'],.5005)
    assert math.isclose(schedules[1]['code_exponential'],math.sqrt(.001))
    (ROOT/'cases.json').write_text(json.dumps(inputs,indent=2)+'\n')
    out = {'scope':'development arithmetic and typed joins only; no reader/C2C run','cases':24,'counts':counts,
           'ordered_evaluations':order_checks,'single_record_ablation_checks':ablations,
           'integer_endpoint_cross_checks':endpoint_checks,'outputs':outputs,'schedule_comparison':schedules}
    (ROOT/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k != 'outputs'},indent=2))

if __name__ == '__main__': main()
