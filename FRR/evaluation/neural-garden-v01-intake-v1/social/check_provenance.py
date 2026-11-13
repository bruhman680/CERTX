from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
branches=json.loads(Path('/workspace/neural_garden_exact_branch_search.json').read_text())
branch=next(x for x in branches if x['branch']=='codex/frr-v05-explorations')
entries={x['path']:x for x in branch['matches']}
rows=[]
for p in (H/'sources').glob('*'):
    if not p.is_file():continue
    b=p.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()
    old=entries['NEURAL_GARDEN_V01/'+p.name]
    rows.append({'file':p.name,'expected_git_blob_sha':old['sha'],'local_git_blob_sha':blob,
                 'exact':blob==old['sha'],'sha256':hashlib.sha256(b).hexdigest()})
payload={'repository':'bruhman680/CERTX','branch':branch['branch'],'commit':branch['sha'],'sources':rows}
(H/'PROVENANCE.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps({'files':len(rows),'exact':sum(r['exact'] for r in rows),'mismatches':[r['file'] for r in rows if not r['exact']]}))
