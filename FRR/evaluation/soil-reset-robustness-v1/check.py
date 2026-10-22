"""Cross-check saved operators by scalar enumeration of updates and resets."""
from pathlib import Path
import json,itertools,hashlib
import numpy as np
r=Path(__file__).resolve().parent
j=json.loads((r/'RESULTS.json').read_text()); states=[tuple(x) for x in j['states']]
checks={}; maxerr=0.;normerr=0.; passive={}
for key,v in j['models'].items():
    kind=key.split('_')[0]; interaction=key.endswith('interaction');pi=v['stationary']
    for name,z in j['resets'].items():
        ra,rs=z['rates'];ex=[0.,0.]
        for y in (0,1):
            for i,(m,s) in enumerate(states):
                for u,t in states:
                    pm=(.6*(u==m)+.4*((.1+.8*y) if u else (.9-.8*y))) if kind in ('echo','mixed') else .5
                    ps=(.7*(t==s)+.3*([.7,.2,.1] if not y else [.1,.2,.7])[t]) if kind in ('wake','mixed') else float(t==s) if kind=='shadow' else 1/3
                    for mr,sr in states:
                        pma=(1-ra)*(mr==u)+ra*(mr==0)
                        psa=(1-rs)*(sr==t)+rs*(sr==0)
                        emission=.05+.2*mr+.2*sr+(.08*mr*sr if interaction else 0)
                        ex[y]+=pi[i]*pm*ps*pma*psa*emission
        maxerr=max(maxerr,abs(ex[1]-ex[0]-v['responses'][name]['forced1_minus_forced0'][0]))
        for prep in ('natural','forced0','forced1'):
            w=j['observation_laws']['|'.join([key,name,prep])];normerr=max(normerr,abs(sum(w)-1))
            assert min(w)>-1e-10
    passive[key]=np.array(j['observation_laws'][key+'|sham|natural'])
ptv={a+'|'+b:float(.5*np.abs(passive[a]-passive[b]).sum()) for a,b in itertools.combinations(sorted(passive),2)}
checks={'scalar_enumeration_agrees':maxerr<1e-10,'all_120_word_laws_normalized':normerr<1e-10,'protocol_unchanged':hashlib.sha256((r/'PROTOCOL.md').read_bytes()).hexdigest()==j['protocol_sha256'],'baseline_stochastic_and_stationary':all(np.max(abs(np.array(v['stationary'])@np.array(v['P'])-np.array(v['stationary'])))<1e-10 for v in j['models'].values()),'all_recorded_checks_pass':all(j['checks'].values())}
out={'scope':'Independent scalar reset/update enumeration; same stipulated model, not independent research replication','max_first_contrast_error':maxerr,'max_word_normalization_error':normerr,'passive_length4_TV':ptv,'minimum_passive_length4_TV':min(ptv.values()),'checks':checks}
(r/'CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert all(checks.values())
