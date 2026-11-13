"""Verify exact pinned Git blobs, removing only an intake-added final blank line."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
tree=json.loads(Path('/workspace/neural_garden_exact_branch_search.json').read_text())
branch=next(x for x in tree if x['branch']=='codex/frr-v05-explorations')
expected={x['path'].split('/')[-1]:x['sha'] for x in branch['matches'] if x['type']=='blob'}
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+bytes([0])+b).hexdigest()
rows=[]
for p in (H/'sources').iterdir():
    if not p.is_file():continue
    raw=p.read_bytes();wanted=expected[p.name]
    if blob(raw)==wanted:change=False
    else:
        assert raw.endswith(b'\n') and blob(raw[:-1])==wanted,p.name
        p.write_bytes(raw[:-1]);change=True
    rows.append({'file':p.name,'git_blob_sha':wanted,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                 'removed_one_intake_added_final_newline':change})
with (H/'SOURCE_PROVENANCE.json').open('x') as f:
    json.dump({'repository':'bruhman680/CERTX','commit':'3204c81ebc6922d66b0ae2623ee83d629f11f3b8',
        'directory':'NEURAL_GARDEN_V01','exact_git_blob_bytes_verified':True,'files':rows},f,indent=2);f.write('\n')
print(json.dumps({'exact_sources':len(rows)}))
