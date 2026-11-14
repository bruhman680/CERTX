"""Shared detached fixtures; no model loading on import."""
from pathlib import Path
import sys,json,hashlib
H=Path(__file__).resolve().parent;E=H.parent
C=E/'minimal-garden-candidate-v1';P=E/'bounded-view-continuation-prototype-v1';V=E/'bounded-view-contact-v1'
sys.path[:0]=[str(C),str(C/'world'),str(V),str(P),str(E/'source-access-three-cycle-v1')]
import candidate
from garden_world import GardenWorld,parse_notebook,verify_store
from view import select_view
MODEL=Path('/workspace/cache_backend_models/smollm2-135m')
def read(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,obj):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    assert not p.exists(),f'Preserve prior artifact: {p}'
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def inventory(root=C):
    return {str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(MODEL,local_files_only=True,trust_remote_code=False)
def base_view(tok=None,before=False):
    tok=tok or tokenizer()
    archive=read(V/'SOURCE_ARCHIVE.json') if before else read(P/'FINAL_ARCHIVE.json')
    return select_view(archive['initial_messages'],archive['exchanges'],tok,max_pairs=8,max_input=7936)
def fixture_bundle(before=False):
    return P/'world/bundles/000001.json' if before else P/'world/bundles'/read(P/'world/STATE.json')['bundle']
def clone(store,before=False):
    w=GardenWorld.create(Path(store),fixture_bundle(before),P/'world/objects',parent_entry=1580 if before else 1583)
    # Declare the diagnostic transport accurately without adding model-facing coaching.
    addition='\n\n## Detached operator-probe transport\nThis copy is a diagnostic fixture. Its model input begins with a selected recent-eight-pair view and may include an explicitly marked operator observation or task. At most one actual reply/receipt followup may be appended. These are controlled context interventions, not a selected live memory policy. The fixture history-copy files remain source data; this probe does not automatically extend them. Actual notebook/cell effects and receipts follow the execution laws above. Authoritative probe records remain outside this world. No behavioral success or retrieval is required.\n'
    source="from pathlib import Path\np=Path('WORLD_RULES.txt')\np.write_text(p.read_text()+"+repr(addition)+",encoding='utf-8')\n"
    event=w.apply('python',source)
    assert event['feedback']['exit_code']==0 and event['feedback']['boundary'] is None
    return w,event
