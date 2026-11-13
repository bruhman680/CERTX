"""Recover exact Git blob bytes from intake copies, checking each blob ID."""
from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent
tree=json.loads(Path('/workspace/neural_garden_exact_branch_search.json').read_text())
nodes={n['path']:n for b in tree if b['branch']=='codex/frr-v05-explorations' for n in b['matches']}
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
rows=[]
for p in (H/'sources').iterdir():
 if not p.is_file():continue
 n=nodes['NEURAL_GARDEN_V01/'+p.name];b=p.read_bytes()
 candidates=[b,b[:-1]] if b.endswith(b'\n') else [b]
 exact=next((v for v in candidates if blob(v)==n['sha']),None)
 if exact is None:raise RuntimeError('No exact Git blob match: '+p.name)
 rows.append({'file':p.name,'git_blob_sha':n['sha'],'removed_terminal_newlines':len(b)-len(exact),
              'acquired_sha256':hashlib.sha256(b).hexdigest(),'exact_sha256':hashlib.sha256(exact).hexdigest()})
 p.write_bytes(exact)
with (H/'COPY_BYTE_CORRECTION.json').open('x') as f:json.dump({'reason':'apply_patch intake added a terminal newline; corrected only when exact pinned Git blob verifies','files':rows},f,indent=2);f.write('\n')
print('verified exact Git blobs:',len(rows))
