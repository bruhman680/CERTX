"""Detached fixed-eight-pair continuation, with ordinary history-copy files."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,hashlib,importlib.util
H=Path(__file__).resolve().parent;E=H.parent;C=E/'minimal-garden-candidate-v1';V=E/'bounded-view-contact-v1'
sys.path[:0]=[str(C),str(C/'world'),str(V),str(E/'source-access-three-cycle-v1')]
import candidate
from view import select_view,ViewCapacity
from garden_world import GardenWorld,verify_store
from runtime_reference import Guard,parameter_digest
spec=importlib.util.spec_from_file_location('unchanged_body',C/'generation.py');body=importlib.util.module_from_spec(spec);spec.loader.exec_module(body)
BASE=Path('/workspace/cache_backend_models/smollm2-135m')
ARCHIVE='conversation_archive_v1'

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inventory(root):return {str(p.relative_to(root)):digest(p) for p in Path(root).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def save(name,obj):
    p=H/name;p.parent.mkdir(parents=True,exist_ok=True)
    assert not p.exists(),f'Preserve prior artifact: {p}'
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def status(obj):
    temp=H/'STATUS.tmp';temp.write_text(json.dumps(obj,indent=2)+'\n');temp.replace(H/'STATUS.json')
def pins():
    return {str(p):digest(p) for p in [Path(__file__),V/'view.py',C/'generation.py',C/'candidate.py',C/'world/garden_world.py',C/'ENVIRONMENT.md',C/'CONTRACT.json']}
def check_pins(expected):
    assert all(digest(p)==sha for p,sha in expected.items()),'Dependency changed'

def new_rules(old):
    begin=old.index('The initial mechanics and existing broad invitation are supplied once')
    end=old.index('\n\nThe observer records outside this world',begin)
    paragraph=("This detached continuation retains the same initial mechanics and broad invitation. Its immediate input contains at most the latest eight complete actual assistant/receipt pairs in chronological order, dropping older whole pairs only if required by the 7936-token input budget. The newest pair and initial framing are never silently truncated; if they cannot fit, generation pauses. The complete authoritative record remains outside this world. This is a changed input-view condition, not untouched full-history token continuity.\n\n"
      "Ordinary writable files under /world/conversation_archive_v1 contain the source condition's initial messages and entries1551-1580, plus later continuation records under entries/<entry>.json. The initial index is a static import index; list entries/ for later records. These copies contain assistant writing and model-action receipts, not a self-referential receipt about their own copying. The original pre1550 conversation is not supplied by this archive. Older inherited notebook writing remains unchanged.\n\n"
      "After a model reply, an operator archive-copy operation attempts exclusive creation of the new entry file under existing ordinary archive directories. Replaced symlink parents or missing directories return an error and are not repaired. Existing files or edits are never overwritten or silently repaired. Known copy failures are returned as actual history_archive receipts alongside model-action receipts; ordinary future cells remain possible. The authoritative external record preserves the final delivered feedback even when an in-world copy is absent, partial, edited or collided. Successful copying is silent in the model-facing feedback. The same finite world/file quotas apply. Retrieval is optional; no action, success or workflow is required.")
    result=old[:begin]+paragraph+old[end:]
    result=result.replace('This is a new version inheriting the supported filesystem state at parent entry 1550. It does not alter that reference version. The model\'s existing pretrained weights remain unchanged.',
        'This detached candidate inherits the exact supported filesystem at immediate parent entry 1580, with original reference1550 preserved in its ancestry. The archive files and this declared body/view description are explicit operator additions in the clone. The existing pretrained weights and environmental execution laws remain unchanged.')
    return result.replace('The first candidate body is the same cached','The retained body is the same cached')

def initialization_source(archive,rules):
    payload={'initial_messages':archive['initial_messages'],'entries':archive['exchanges']}
    return ("from pathlib import Path\nimport json\npayload=json.loads("+repr(json.dumps(payload,ensure_ascii=False))+")\np=Path('"+ARCHIVE+"')\np.mkdir()\n(p/'entries').mkdir()\n(p/'initial_messages.json').write_text(json.dumps(payload['initial_messages'],ensure_ascii=False),encoding='utf-8')\nindex=[]\nfor row in payload['entries']:\n    name='entries/'+str(row['entry']).zfill(6)+'.json'\n    with (p/name).open('x',encoding='utf-8') as f: f.write(json.dumps(row,ensure_ascii=False))\n    index.append({'entry':row['entry'],'path':name})\n(p/'index.json').write_text(json.dumps({'scope':'static initial source import1551-1580; later files are listed from entries/','entries':index}),encoding='utf-8')\nPath('WORLD_RULES.txt').write_text("+repr(rules)+",encoding='utf-8')\nprint(len(index))\n")

def archive_source(entry,text,action_feedback):
    payload={'entry':entry,'assistant':text,'receipt':action_feedback}
    return ("from pathlib import Path\nimport json,hashlib\npayload=json.loads("+repr(json.dumps(payload,ensure_ascii=False))+")\nbase=Path('"+ARCHIVE+"')\nentries=base/'entries'\nif base.is_symlink() or entries.is_symlink() or not base.is_dir() or not entries.is_dir():\n    raise OSError('Archive parents must be existing ordinary directories; no automatic repair')\np=entries/"+repr(f'{entry:06d}.json')+"\nwith p.open('x',encoding='utf-8') as f: f.write(json.dumps(payload,ensure_ascii=False))\nprint(hashlib.sha256(p.read_bytes()).hexdigest())\n")

def combined_feedback(action_feedback,archive_event):
    r=archive_event['feedback']
    if r['exit_code']==0 and r['boundary'] is None:return action_feedback
    data=json.loads(action_feedback) if action_feedback else {'receipts':[],'boundary':None}
    data['receipts'].append({'channel':'history_archive',**{k:r[k] for k in ['stdout','stderr','exit_code','boundary']}})
    return json.dumps(data,ensure_ascii=False,sort_keys=True)

def read_all_source():
    return "from pathlib import Path\nimport json,hashlib\np=Path('"+ARCHIVE+"')\na={'initial_messages':json.loads((p/'initial_messages.json').read_text()),'exchanges':[json.loads(f.read_text()) for f in sorted((p/'entries').glob('*.json'))]}\nprint(hashlib.sha256(json.dumps(a,sort_keys=True,ensure_ascii=False).encode()).hexdigest())\nprint(len(a['exchanges']))\n"

def main():
    assert not (H/'STATUS.json').exists(),'No automatic resume/replay'
    canonical_before=inventory(C);pointer=Path('/workspace/frr/ACTIVE_GARDEN_PHASE.json').read_bytes()
    src=json.loads((V/'SOURCE_ARCHIVE.json').read_text());assert src['canonical_state']['human_entry']==1580
    initial=src['initial_messages'];exchanges=list(src['exchanges']);assert len(exchanges)==30
    parent=C/'run/world/bundles/000031.json';parent_bundle=json.loads(parent.read_text())
    assert not any(x[0]==ARCHIVE or x[0].startswith(ARCHIVE+'/') for x in parent_bundle['entries'])
    old=(C/'ENVIRONMENT.md').read_text();rules=new_rules(old)
    (H/'ORIGINAL_WORLD_RULES.txt').write_text(old);(H/'PROTOTYPE_WORLD_RULES.txt').write_text(rules)
    pinned=pins()
    save('PLAN.json',{'date':'2026-11-13 America/Chicago','status':'detached candidate, not adopted','parent_entry':1580,
      'candidate_entries':[1581,1582,1583],'policy':'fixed8 whole recent pairs;7936 budget fallback; newest mandatory',
      'parent_bundle_sha256':digest(parent),'pins':pinned,'initial_messages_unchanged':True,
      'body':'unchanged cached135M CPU float32 eager2threads greedy256, original generate function',
      'operator_changes':'archive ordinary files and consistent WORLD_RULES body paragraph in clone only',
      'archive_scope':'source1551-1580 then action receipts; copyfailure receipts remain authoritative external/view; no selfreference',
      'model_retrieval_not_required':True,'training':False,'paid_endpoint':False,'canonical_activation':False})
    save('CANONICAL_BEFORE.json',canonical_before);save('INITIAL_ARCHIVE.json',src)
    save('INITIAL_MESSAGES.json',initial)
    status({'stage':'initializing','paused':False,'candidate_entry':1580,'canonical_entry':1580})
    (H/'PENDING.json').write_text(json.dumps({'stage':'operator initialization unknown until committed'}))
    w=GardenWorld.create(H/'world',parent,C/'run/world/objects',parent_entry=1580)
    try:
        before=w.checkpoint();event=w.apply('python',initialization_source(src,rules));save('INITIALIZATION.json',{'actor':'operator','event':event})
        assert event['feedback']['exit_code']==0 and event['feedback']['boundary'] is None
        after=w.checkpoint();oldpaths={x[0]:x for x in before['entries']};newpaths={x[0]:x for x in after['entries']}
        assert all(newpaths[p]==x for p,x in oldpaths.items() if p!='WORLD_RULES.txt')
        assert all(p=='WORLD_RULES.txt' or p==ARCHIVE or p.startswith(ARCHIVE+'/') for p in event['changed_paths'])
        save('INITIAL_WORLD.json',after)
    finally:w.close()
    (H/'PENDING.json').unlink()
    import torch
    from transformers import AutoTokenizer,AutoModelForCausalLM
    torch.set_num_threads(2)
    tok=AutoTokenizer.from_pretrained(BASE,local_files_only=True,trust_remote_code=False)
    model=AutoModelForCausalLM.from_pretrained(BASE,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False);model.eval()
    expected=json.loads((C/'run/MANIFEST.json').read_text())['tensor_digest'];assert parameter_digest(model,False)==expected
    guard=Guard(5153960755,H/'RESOURCE.jsonl');records=[];prev=None
    for loop in range(1,4):
        check_pins(pinned);entry=1580+loop
        try:view=select_view(initial,exchanges,tok,max_pairs=8,max_input=7936)
        except ViewCapacity as error:
            save('CAPACITY_PAUSE.json',{'loop':loop,'error':str(error)});break
        save(f'plans/{loop:02d}.json',{'entry':entry,'view':view,'archive_entries':[x['entry'] for x in exchanges],
             'previous_record_sha256':prev,'world_state':json.loads((H/'world/STATE.json').read_text())})
        (H/'PENDING.json').write_text(json.dumps({'entry':entry,'stage':'generation/model and archive operations unresolved until record committed'}))
        raw=body.generate(model,tok,view['messages'],guard,f'bounded_candidate_{entry}')
        assert raw['input_token_ids']==view['input_token_ids'];save(f'raw/{loop:02d}.json',raw)
        w=GardenWorld.open(H/'world')
        try:
            before=w.checkpoint();batch=w.receive_notebook(raw['text']);save(f'batches/{loop:02d}.json',batch)
            action_feedback=candidate.project_feedback(batch)
            save(f'action_records/{entry}.json',{'entry':entry,'assistant':raw['text'],'receipt':action_feedback})
            arch=w.apply('python',archive_source(entry,raw['text'],action_feedback));save(f'archive_operations/{loop:02d}.json',{'actor':'operator history copy','event':arch})
            feedback=combined_feedback(action_feedback,arch)
            if arch['feedback']['exit_code']==0 and arch['feedback']['boundary'] is None:
                expected_bytes=json.dumps({'entry':entry,'assistant':raw['text'],'receipt':action_feedback},ensure_ascii=False).encode()
                assert arch['feedback']['stdout'].strip()==hashlib.sha256(expected_bytes).hexdigest()
            after=w.checkpoint()
        finally:w.close()
        exchange={'entry':entry,'assistant':raw['text'],'receipt':feedback};save(f'exchanges/{entry}.json',exchange);exchanges.append(exchange)
        row={'candidate_entry':entry,'loop':loop,'included_entries':view['included_entries'],'omitted_entries':view['omitted_entries'],
          'input_tokens':len(view['input_token_ids']),'output_tokens':len(raw['generated_token_ids']),'stop':raw['stop'],
          'input_ids_sha256':hashlib.sha256(json.dumps(view['input_token_ids']).encode()).hexdigest(),
          'model_code_operations':sum(o['channel']!='note' for o in batch['operations']),
          'complete_cells':batch['parsed']['complete_executable_cells'],'action_feedback':action_feedback,'final_feedback':feedback,
          'archive_copy_exit':arch['feedback']['exit_code'],'archive_copy_boundary':arch['feedback']['boundary'],
          'before_id':before['id'],'after_id':after['id'],'previous_record_sha256':prev,
          'raw_sha256':digest(H/f'raw/{loop:02d}.json'),'batch_sha256':digest(H/f'batches/{loop:02d}.json'),
          'archive_operation_sha256':digest(H/f'archive_operations/{loop:02d}.json'),'verification':verify_store(H/'world')}
        save(f'records/{loop:02d}.json',row);prev=digest(H/f'records/{loop:02d}.json');records.append(row)
        (H/'PENDING.json').unlink();status({'stage':'between loops','paused':True,'candidate_entry':entry,'canonical_entry':1580})
        assert canonical_before==inventory(C) and pointer==Path('/workspace/frr/ACTIVE_GARDEN_PHASE.json').read_bytes()
        assert parameter_digest(model,False)==expected
        print(json.dumps({k:row[k] for k in ['candidate_entry','input_tokens','output_tokens','stop','complete_cells','archive_copy_exit']}),flush=True)
    save('FINAL_ARCHIVE.json',{'initial_messages':initial,'exchanges':exchanges})
    w=GardenWorld.open(H/'world')
    try:
        read_event=w.apply('python',read_all_source());save('FINAL_ARCHIVE_READ.json',{'actor':'operator verification','event':read_event})
    finally:w.close()
    archive_success=all(r['archive_copy_exit']==0 and r['archive_copy_boundary'] is None for r in records)
    expected_sha=hashlib.sha256(json.dumps({'initial_messages':initial,'exchanges':exchanges},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    archive_exact=(read_event['feedback']['exit_code']==0 and read_event['feedback']['stdout'].splitlines()==[expected_sha,str(len(exchanges))])
    check_pins(pinned);assert canonical_before==inventory(C);assert pointer==Path('/workspace/frr/ACTIVE_GARDEN_PHASE.json').read_bytes()
    assert parameter_digest(model,False)==expected
    save('RESULTS.json',{'completed_loops':len(records),'candidate_entry':1580+len(records),'canonical_entry':1580,
       'records':records,'world_verification':verify_store(H/'world'),'archive_success_all':archive_success,
       'world_archive_exact_authoritative_at_final_read':archive_exact,
       'archive_comparison_is_observation_not_gate':True,'final_archive_read_exit':read_event['feedback']['exit_code'],
       'distinct_input_token_sequences':len({r['input_ids_sha256'] for r in records}),
       'archive_records':len(exchanges),'canonical_inventory_unchanged':True,'active_pointer_unchanged':True,
       'model_weights_unchanged':True,'source_pins_unchanged':True,'activation':False,'model_retrieval_not_tested':True,
       'power_loss_durability_not_claimed':True,'pending':(H/'PENDING.json').exists()})
    status({'stage':'completed detached pilot','paused':True,'candidate_entry':1580+len(records),'canonical_entry':1580,'activation':False})

if __name__=='__main__':main()
