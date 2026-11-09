"""Record an external documentation review and prepare its publication payload."""
from pathlib import Path
import hashlib, json, re, shutil

H = Path(__file__).resolve().parent
F = H.parent.parent
P = H.parent / 'final-garden-contract-v1'
A = H.parent / 'frozen-garden-tool-path-audit-v1'

def sha(b):
    return hashlib.sha256(b).hexdigest()

before = json.loads((A / 'CANONICAL_BEFORE.json').read_text())
current = {str(p.relative_to(P)):sha(p.read_bytes()) for p in P.rglob('*')
           if p.is_file() and '__pycache__' not in p.parts}
assert before == current, 'Canonical phase drift; stop without altering it'
state = json.loads((P / 'run/STATE.json').read_text())
assert state['paused'] and state['next_entry'] == 1550
assert not (P / 'run/PENDING.json').exists() and not (P / 'run/RUN.lock').exists()
links = []
for name in ['WORLD_MAP.md', 'BOUNDARY_REVIEW.md']:
    for target in re.findall(r'\]\(([^)]+)\)', (H / name).read_text()):
        assert not target.startswith(('http:', 'https:'))
        assert (H / target).exists(), target
        links.append({'document':name,'target':target,'exists':True})
provenance = {
    'date_utc':'2026-11-09', 'status':'pass', 'scope':'External map and boundary review only',
    'canonical_paused_at':1550, 'canonical_inventory_unchanged':True,
    'canonical_files_checked':len(current),
    'canonical_inventory_sha256':sha(json.dumps(current,sort_keys=True,separators=(',',':')).encode()),
    'canonical_generation_calls':0, 'external_model_calls':0, 'new_experiments':0,
    'training_updates':0, 'proposed_changes_implemented':False,
    'canonical_phase_source_sha256':{n:current[n] for n in ['runner.py','world.py','server.py','generation.py','CONTRACT.json']},
    'evidence_source':'../frozen-garden-tool-path-audit-v1/REPORT.md',
    'links_checked':links,
    'one_page_map_words':len((H / 'WORLD_MAP.md').read_text().split()),
}
with (H / 'REVIEW_PROVENANCE.json').open('x') as f:
    json.dump(provenance,f,indent=2)
    f.write('\n')

navs = ['CURRENT_HANDOFF.md','sync/CURRENT_ORIENTATION.md','evaluation/CURRENT_RESEARCH_MAP.md']
for rel in navs:
    old = (F / rel).read_bytes()
    dest = H / 'before' / rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    assert not dest.exists()
    dest.write_bytes(old)
    link = ('evaluation/' if rel == 'CURRENT_HANDOFF.md' else '../evaluation/' if rel.startswith('sync/') else '') + H.name + '/WORLD_MAP.md'
    prefix = f'''# Current design review: state, laws and contact mapped; paused at 1550

9 November 2026 UTC. [One-page world map]({link}) and its linked boundary review distinguish persistent state, world transitions, observations, continuity, model generation, and experimental bounds. This is documentation only: zero model calls, zero new experiments, and no proposed redesign implemented. All canonical phase files match the preceding audit inventory.

The current world inherits a broad shell/Python runtime. Its presentation and memory rules are additional design choices. Preserve isolation, truthful consequences and external history; inspect optional repetition, action grammar and sampling separately. Removing replay also removes its automatic short-term memory, so simplification must account for that function. The map does not assert that a small law set guarantees emergence or exposes every pretrained capability.

The original garden remains paused at 1550, with the freeze at 850 intact. No continuation or alteration is scheduled. Detached comparisons remain prospective; read the preceding tool-path audit for the measured singleton-nucleus finding. Earlier history and interpretations follow unchanged.

---

'''
    (F / rel).write_bytes(prefix.encode() + old)

out = Path('/workspace/garden_map_publication')
out.mkdir()
files = [p for p in H.rglob('*') if p.is_file() and '__pycache__' not in p.parts] + [F / rel for rel in navs]
rows, hashes = [], {}
for p in sorted(files):
    b = p.read_bytes()
    path = 'FRR/' + str(p.relative_to(F))
    hashes[path] = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
    rows.append({'path':path,'mode':'100644','type':'blob','content':b.decode()})
(out / 'PAYLOAD.json').write_text(json.dumps(rows))
(out / 'HASHES.json').write_text(json.dumps(hashes))
print(json.dumps({'status':'pass','paused_at':1550,'canonical_files_checked':len(current),
                  'map_words':provenance['one_page_map_words'],'publication_files':len(files),
                  'payload_bytes':(out / 'PAYLOAD.json').stat().st_size}))
