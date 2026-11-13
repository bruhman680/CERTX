"""Independent read-only audit of saved framing-pair effects and source."""
from pathlib import Path
import ast, base64, json
from audit_retained import audit_store, read

H = Path(__file__).resolve().parent
C = H.parents[1] / 'minimal-garden-candidate-v1'
F = C / 'diagnostics/framing_pair'

def memory(store, step):
    bundle = read(store/'world/bundles'/f'{step:06d}.json')
    e = next((r for r in bundle['entries'] if r[0]=='memory.txt'),None)
    if e is None:
        return None
    assert e[1]=='file'
    obj = read(store/'world/objects'/(e[3]+'.json'))
    return base64.b64decode(obj['base64'],validate=True).decode()

result = {'date':'2026-11-09 America/Chicago','review_model_calls':0,'new_guest_actions':0,'arms':{}}
for arm in ['minimal','standard']:
    store = F/arm/'run'
    audit = audit_store(store)
    timeline = []
    for turn in range(1,4):
        batch = read(store/'batches'/f'{turn:06d}.json')
        for op in batch['operations']:
            if 'cell_index' not in op:
                continue
            timeline.append({'turn':turn,'step':op['step'],'source':op['source'],
                'stdout':op['receipt']['stdout'],'stderr':op['receipt']['stderr'],
                'exit_code':op['receipt']['exit_code'],'memory_after':memory(store,op['step'])})
    result['arms'][arm]={'chain_audit':audit,'cell_timeline':timeline}

minimal = result['arms']['minimal']['cell_timeline']
standard = result['arms']['standard']['cell_timeline']
assert [t['memory_after'] for t in minimal]==[None,'37','37','37','37','37']
assert [t['memory_after'] for t in standard]==[None,'37','','','37','','','5','']
assert 'FileNotFoundError' in minimal[0]['stderr'] and minimal[1]['exit_code']==0
reads = [t for t in minimal if t['turn'] in [2,3] and t['stdout']=='37\n']
assert len(reads)==2
for t in reads:
    tree = ast.parse(t['source'])
    assert len(tree.body)==1 and isinstance(tree.body[0],ast.With)
    block = tree.body[0]
    opening = block.items[0].context_expr
    assert isinstance(opening,ast.Call) and isinstance(opening.func,ast.Name) and opening.func.id=='open'
    assert [a.value for a in opening.args]==['memory.txt','r']
    assign,printed = block.body
    assert isinstance(assign,ast.Assign) and assign.targets[0].id=='contents'
    assert isinstance(assign.value,ast.Call) and assign.value.func.attr=='read'
    assert assign.value.func.value.id=='file'
    assert isinstance(printed,ast.Expr) and printed.value.func.id=='print' and printed.value.args[0].id=='contents'
assert all('TypeError' in standard[i]['stderr'] and standard[i]['exit_code']==1 for i in [2,5,8])
result.update(status='pass',minimal_persistent_nonempty_file_readback=True,
    minimal_requested_add_five=False,standard_intermediate_writes_then_truncations=True,
    scope='Prompted operational file I/O established. Same declared world/body; initial framing differs. No robustness, independent motivation, autonomous repair or emergence claim.')
with (H/'FRAMING_PAIR_RETAINED_AUDIT.json').open('x') as f:
    json.dump(result,f,indent=2)
    f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k!='arms'}))
