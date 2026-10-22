"""Recompute summaries and interval decisions from recorded contrasts (no resampling)."""
from pathlib import Path
import json,hashlib,itertools
import numpy as np
D=Path(__file__).resolve().parent
p=D.parent/'cycle1'/'RESULTS.json'; raw=p.read_bytes();j=json.loads(raw)
cs={'shadow':(0.,0.),'echo':(.064,0.),'wake':(0.,.072),'mixed':(.064,.072)}
xs={'diverse':np.array([[1.,1.],[.2,.9],[.9,.2]]),'redundant':np.array([[1.,1.],[.4,.4],[.4,.4]])}
errors=[]; rankdef=[];maxerr=0.;rngkeys={};ranks={}
for z in j['replicates']:
    d=np.array(z['observed_contrasts']);e=(np.log(480)/(2*z['n']))**.5
    key=(z['design'],z['n'],z['world'],z['rep'])
    current=(z['observed_contrasts'],z['witness_survival'])
    if key in rngkeys and rngkeys[key]!=current:errors.append('mode changes data')
    rngkeys[key]=current
    mode=z['mode'];out=[]
    if mode=='absent':out=list(cs)
    else:
        x=xs[z['design']] if mode=='known' else np.array(z['witness_survival'])
        rank=int(np.linalg.matrix_rank(x,tol=1e-12));ranks[(z['design'],mode,rank)]=ranks.get((z['design'],mode,rank),0)+1
        for label,c in cs.items():
            admit=True
            for arm in range(3):
                lower=upper=0.
                for coord in range(2):
                    center=x[arm,coord];rad=e if mode=='estimated' else 0.
                    lower+=max(0,center-rad)*c[coord]
                    upper+=min(1,center+rad)*c[coord]
                if not(upper>=d[arm]-2*e and lower<=d[arm]+2*e):admit=False
            if admit:out.append(label)
        if z['design']=='diverse':
            if rank<2:rankdef.append(key+(mode,))
            else:
                # Normal-equation solve instead of the implementation's pseudoinverse.
                L=np.linalg.solve(x.T@x,x.T);est=L@d
                radius=np.sum(abs(L),axis=1)*(2*e+(.6*e if mode=='estimated' else 0))
                maxerr=max(maxerr,float(np.max(abs(est-np.array(z['allocation'])))),float(np.max(abs(2*radius-np.array(z['width'])))))
                covered=all(abs(est[k]-cs[z['world']][k])<=radius[k]+1e-12 for k in range(2))
                if covered!=z['covered']:errors.append('coverage')
    if out!=z['candidate_set']:errors.append('candidate_set')
    if bool(len(out)==1)!=z['point_identified']:errors.append('singleton field')
    if z['design']=='redundant' and z['allocation'] is not None:errors.append('rank1 allocation')
    if z['cost_draws']!=12*z['n']:errors.append('cost per analysis row')
for g in j['summary']:
    rows=[z for z in j['replicates'] if all(z[k]==g[k] for k in ['design','n','mode'])]
    metrics={'true_candidate_retention':sum(z['true_candidate_retained'] for z in rows)/len(rows),'singleton_fraction':sum(len(z['candidate_set'])==1 for z in rows)/len(rows),'mean_candidate_count':sum(len(z['candidate_set']) for z in rows)/len(rows)}
    for k,v in metrics.items():
        if abs(v-g[k])>1e-12:errors.append('summary '+k)
assert not errors,errors
out={'scope':'Separate scalar candidate checks/normal-equation interval replay over saved data; same authored model, not independent calibration validation','source_sha256':hashlib.sha256(raw).hexdigest(),'unique_stochastic_datasets':len(rngkeys),'analysis_rows':len(j['replicates']),'draw_total_unique_datasets':sum(12*k[1] for k in rngkeys),'source_protocol_hash_matches':hashlib.sha256((D.parent/'cycle1'/'PROTOCOL.md').read_bytes()).hexdigest()==j['protocol_sha256'],'max_estimate_or_width_difference':maxerr,'observed_diverse_rank_deficient_cases':rankdef,'observed_design_mode_matrix_ranks':{'|'.join(map(str,k)):v for k,v in ranks.items()},'errors':errors,'method_limits':['Current Cycle1 implementation has no rank guard for diverse estimated matrices. No rank deficiency was observed; add guard and exercise singular input as a separate Cycle3 repair, preserving original results.','point_identified is a finite-library singleton flag, not generic continuous point identification.','Hoeffding coverage is conditional on stipulated witness validity/independence and model class; empirical coverage here is conservative, not validation of real calibration.','Three inference modes share each sampled dataset; do not multiply their measurement costs.']}
(D/'CYCLE1_AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
