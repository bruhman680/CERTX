"""Nondominated energy-vs-floor review of pre-existing matched welfare results."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

PATH=Path(__file__).parent

def run():
    learned=json.loads((PATH/'NEXT_WELFARE_deterministic_results.json').read_text())
    rules=json.loads((PATH/'NEXT_WELFARE_rule_controls_results.json').read_text())
    out={}
    for regime in ('stable','mild'):
        arms={}
        for key,z in learned['summary'].items():
            tag,obj=key.split('/')
            if tag==regime:arms['neural/'+obj]={'energy':z['energy'],'floor':z['floor']}
        for key,z in rules['summary'].items():
            tag,obj=key.split('/')
            if tag==regime:arms['manual/'+obj]={'energy':z['energy'],'floor':z['floor']}
        nondom=[]
        for name,point in arms.items():
            dominated_by=[other for other,q in arms.items() if other!=name and
                q['energy']>=point['energy'] and q['floor']<=point['floor'] and
                (q['energy']>point['energy'] or q['floor']<point['floor'])]
            if not dominated_by:nondom.append(name)
            arms[name]['dominated_by']=dominated_by
        out[regime]={'nondominated':nondom,'arms':arms}
    return {'scope':'aggregate mean energy and fraction energy<=.01 only, two competing burdens',
            'results':out,'source_sha256':{f:hashlib.sha256((PATH/f).read_bytes()).hexdigest()
              for f in ('NEXT_WELFARE_deterministic_results.json',
                         'NEXT_WELFARE_rule_controls_results.json',Path(__file__).name)}}

if __name__=='__main__':
    z=run();(PATH/'NEXT_WELFARE_pareto_results.json').write_text(json.dumps(z,indent=2)+'\n')
    for regime,x in z['results'].items():print(regime,x['nondominated'])
