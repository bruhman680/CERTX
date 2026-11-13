"""Read-only retained-byte audit; all writes stay in this review directory."""
from pathlib import Path
import base64, hashlib, json

H = Path(__file__).resolve().parent
C = H.parents[1] / 'minimal-garden-candidate-v1'
P = H.parents[1] / 'final-garden-contract-v1'

def read(path):
    return json.loads(Path(path).read_text())

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def bundle_id(bundle):
    return hashlib.sha256(json.dumps({'entries':bundle['entries'],'root_mode':bundle['root_mode']},
        sort_keys=True,separators=(',',':')).encode()).hexdigest()

def audit_store(store):
    store = Path(store)
    s = read(store/'STATE.json')
    assert s['paused'] and not (store/'RUN.lock').exists() and not (store/'PENDING.json').exists()
    manifest = read(store/'MANIFEST.json')
    for path,pin in manifest['pins'].items():
        assert digest(path)==pin,path
    w = store/'world'
    ws = read(w/'STATE.json')
    assert ws['paused'] and not ws['faulted']
    assert not any((w/n).exists() for n in ['LOCK.json','PENDING.json','BATCH_PENDING.json'])
    previous = read(w/'bundles/000000.json')
    assert previous==read(P/'run/bundles/001550.json')
    last = None
    for step in range(1,ws['step']+1):
        e = read(w/'events'/f'{step:06d}.json')
        receipt = read(w/'events'/f'{step:06d}_RECEIPT.json')
        after = read(w/'bundles'/f'{step:06d}.json')
        assert e['step']==step and e['before_id']==previous['id'] and e['parent_event_sha256']==last
        assert e['after_id']==after['id']==bundle_id(after)
        assert e['receipt']==receipt['receipt']
        assert all(e[k]==receipt['operation'][k] for k in ['step','channel','source','raw_text','before_id','parent_event_sha256'])
        previous,last = after,digest(w/'events'/f'{step:06d}.json')
    assert ws['last_event_sha256']==last and ws['bundle']==f"{ws['step']:06d}.json"
    for path in (w/'objects').glob('*.json'):
        o = read(path)
        raw = base64.b64decode(o['base64'],validate=True)
        assert len(raw)==o['bytes'] and hashlib.sha256(raw).hexdigest()==o['sha256']==path.stem
    last = None
    cells,nonzero = 0,0
    initial = read(store/'INITIAL_WORLD.json')
    world_before = initial
    for turn in range(1,s['turn']+1):
        e = read(store/'events'/f'{turn:06d}.json')
        raw = read(store/'raw'/f'{turn:06d}.json')
        batch = read(store/'batches'/f'{turn:06d}.json')
        assert e['parent_event_sha256']==last and e['turn']==turn and e['human_entry']==1550+turn
        assert e['raw_sha256']==digest(store/'raw'/f'{turn:06d}.json')
        assert raw['text']==e['text']==batch['raw_text']
        assert batch==read(w/'batches'/(batch['batch_id']+'.json'))
        assert e['before_id']==world_before['id']
        feedback=[]
        for op in batch['operations']:
            plain = {k:v for k,v in op.items() if k not in ['cell_index','source_start','source_end']}
            assert plain==read(w/'events'/f"{op['step']:06d}.json")
            if 'cell_index' in op:
                cell = batch['parsed']['cells'][op['cell_index']]
                assert op['source']==cell['source'] and cell['executable']
                assert op['source_start']==cell['source_start'] and op['source_end']==cell['source_end']
                cells+=1
                nonzero+=int(op['receipt']['exit_code']!=0)
            if op['feedback'] is not None:
                q=op['feedback']
                feedback.append({'channel':op['channel'],**{k:q[k] for k in ['stdout','stderr','exit_code','boundary']}})
        expected = '' if not feedback and batch['boundary'] is None else json.dumps({'receipts':feedback,'boundary':batch['boundary']},ensure_ascii=False,sort_keys=True)
        assert e['feedback']==expected
        if batch['operations']:
            world_before=read(w/'bundles'/f"{batch['operations'][-1]['step']:06d}.json")
        assert e['after_id']==world_before['id']
        last=digest(store/'events'/f'{turn:06d}.json')
    assert s['last_event_sha256']==last and s['world_step']==ws['step']
    assert world_before==previous
    return {'status':'pass','turns':s['turn'],'world_operations':ws['step'],'actual_code_cells':cells,
        'nonzero_cell_receipts':nonzero,'source_pins':True,'paused':True,
        'source_batch_event_chain':True,'objects_verified':len(list((w/'objects').glob('*.json')))}

def main():
    before=read(C/'diagnostics/operational-run/REFERENCE_INVENTORY.json')
    actual={str(p.relative_to(P)):digest(p) for p in P.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    assert actual==before
    state=read(P/'run/STATE.json')
    assert state['paused'] and state['next_entry']==1550
    result={'date':'2026-11-09 America/Chicago','review_model_calls':0,
        'canonical_files_unchanged':len(actual),'canonical_paused_at':1550,
        'candidate_source_sha256':digest(C/'candidate.py'),'world_source_sha256':digest(C/'world/garden_world.py'),
        'original_six_turn_diagnostic':audit_store(C/'diagnostics/operational-run'),
        'scope':'Independent retained-byte and chain checks. No neural rerun, guest action, tokenization recomputation or simulator independence claim.'}
    with (H/'RETAINED_AUDIT.json').open('x') as f:
        json.dump(result,f,indent=2)
        f.write('\n')
    print(json.dumps(result))

if __name__=='__main__':
    main()
