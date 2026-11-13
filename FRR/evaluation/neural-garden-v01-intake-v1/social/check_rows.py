from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H/'sources'))
import SOCIAL2_LAG_probe as lag
d=json.loads((H/'sources/SOCIAL2_LAG_results.json').read_text())
a=lag.aggregate(d['rows'],2000)
assert a==d['summary']
counts={}
for rate in [.06,.055]:
    rows=[r for r in d['rows'] if r['regrowth']==rate]
    assert sorted(r['seed'] for r in rows)==list(range(11000,11012))
    counts[str(rate)]={
        'neighbor_previous_over_own_previous':sum(r['arms']['neighbor_previous']['2000']['mean_energy']>r['arms']['own_previous']['2000']['mean_energy'] for r in rows),
        'neighbor_previous_over_global_previous':sum(r['arms']['neighbor_previous']['2000']['mean_energy']>r['arms']['global_previous']['2000']['mean_energy'] for r in rows)}
out={'status':'pass','rows':len(d['rows']),'seed_regime_arm_deployments':len(d['rows'])*len(lag.ARMS),
     'summary_exactly_recomputed':True,'paired_seed_wins':counts,
     'scope':'Arithmetic recomputation on supplied source rows, not independent simulation replication of all192deployments.'}
(H/'ROW_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
