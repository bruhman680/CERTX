"""Optional detached512-output contact, runnable only after main pauses at1630."""
import os
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():os.environ[k]=v
from pathlib import Path
import sys,json,hashlib,importlib.util
H=Path(__file__).resolve().parent;E=H.parent;M=E/'bounded-main-continuation-v1';C=E/'minimal-garden-candidate-v1'
sys.path.insert(0,str(M))
import runner as main_runner
import budget_body as body
from garden_world import GardenWorld,verify_store,immutable,read,digest
from runtime_reference import Guard,parameter_digest

def save(name,value):immutable(H/name,value)

def execute():
    assert not (H/'PLAN.json').exists(),'No replay into an existing diagnostic'
    state=read(M/'run/STATE.json');assert state['human_entry']==1630 and state['paused']
    assert not (M/'run/RUN.lock').exists() and not (M/'run/PENDING.json').exists()
    pointer_before=(E.parent/'ACTIVE_GARDEN_PHASE.json').read_bytes()
    assert json.loads(pointer_before)['phase']=='evaluation/bounded-main-continuation-v1'
    parent_before=main_runner.inventory(M);source_before=main_runner.inventory(C)
    tok=main_runner.tokenizer();precheck=main_runner.verify(M/'run',tok)
    assert parent_before==main_runner.inventory(M) and source_before==main_runner.inventory(C)
    view=main_runner.current_view(M/'run',tok)
    assert len(view['input_token_ids'])<=7680,'Do not trim or alter diagnostic input'
    reference_path=M/'run/raw'/f"{state['turn']:06d}.json";reference=read(reference_path)
    source_pins={str(p):digest(p) for p in [Path(__file__),H/'budget_body.py',C/'generation.py',M/'runner.py']}
    save('PLAN.json',{'status':'detached single512-token contact, not main activation','hypothesis':'An unfinished repeated fence may reflect output-budget completion rather than a selected closed program.512 may or may not produce a complete lawful cell.','source_parent_entry':1630,'source_parent_state':state,'main_precheck':precheck,'initial_input':'exact next current main8pair view; no task,hint,selectorchange ortrim','input_tokens':len(view['input_token_ids']),'generation_budget':{'max_input':7680,'max_output':512,'total_positions':8192},'changed_condition':'output budget only in same algorithmic generation body; copied world has explicit matching diagnostic mechanical declaration','model':'cached135M float32CPU eager2threads greedy freshKV; same weights','actual_model_calls_planned':1,'generation_prefix_reference':str(reference_path),'generation_prefix_expected':'first256 IDs may match main reference if exactinputIDs match; record disagreement ratherthan force it','execution':'unchanged raw reply through same existing parser and physical bounds in a detached world copy','main_changes':False,'activation':False,'source_pins':source_pins})
    save('MAIN_PHASE_BEFORE.json',parent_before);save('SOURCE_PHASE_BEFORE.json',source_before);save('INPUT_VIEW.json',view)
    source_world=M/'run/world';world_state=read(source_world/'STATE.json')
    parent_bundle=source_world/'bundles'/world_state['bundle']
    immutable(H/'PENDING.json',{'stage':'diagnostic initialization unresolved'})
    world=GardenWorld.create(H/'world',parent_bundle,source_world/'objects',parent_entry=1630)
    try:
        old=world.checkpoint()
        addition='\n\n## Detached generation-budget contact\nThis copy receives the exact selected input from the paused source1630 phase, with a changed generation budget: at most512 output tokens and7680 input tokens within8192 total positions. Only one reply is planned. This is a detached diagnostic, not an active main continuity change. Exact existing notebook parser, per-file, storage, process and execution limits remain unchanged.\n'
        code="from pathlib import Path\np=Path('WORLD_RULES.txt')\np.write_text(p.read_text()+"+repr(addition)+",encoding='utf-8')"
        op=world.apply('python',code);save('INITIALIZATION.json',{'actor':'operator','source':code,'event':op})
        assert op['feedback']['exit_code']==0 and op['feedback']['boundary'] is None and op['changed_paths']==['WORLD_RULES.txt']
        new=world.checkpoint();oldpaths={x[0]:x for x in old['entries']};newpaths={x[0]:x for x in new['entries']}
        assert set(oldpaths)==set(newpaths) and all(oldpaths[p]==newpaths[p] for p in oldpaths if p!='WORLD_RULES.txt')
        save('INITIAL_WORLD.json',new)
    finally:world.close()
    (H/'PENDING.json').unlink()
    import torch
    from transformers import AutoModelForCausalLM
    torch.set_num_threads(2)
    guard=Guard(5153960755,H/'RESOURCE.jsonl');guard.read('before_model_load')
    model=AutoModelForCausalLM.from_pretrained(main_runner.MODEL,local_files_only=True,trust_remote_code=False,use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False);model.eval();expected=read(M/'run/MANIFEST.json')['tensor_digest'];assert parameter_digest(model,False)==expected
    immutable(H/'PENDING.json',{'stage':'single generation and notebook effects unresolved; no automatic replay'})
    raw=body.generate(model,tok,view['messages'],guard,'detached_completion512_from1630');save('RAW.json',raw)
    assert raw['input_token_ids']==view['input_token_ids']
    world=GardenWorld.open(H/'world')
    try:
        before=world.checkpoint();batch=world.receive_notebook(raw['text']);save('BATCH.json',batch);after=world.checkpoint()
    finally:world.close()
    assert parameter_digest(model,False)==expected
    assert main_runner.inventory(M)==parent_before and main_runner.inventory(C)==source_before
    assert (E.parent/'ACTIVE_GARDEN_PHASE.json').read_bytes()==pointer_before
    assert all(digest(p)==sha for p,sha in source_pins.items())
    receipts=[{'channel':x['channel'],'feedback':x['feedback'],'changed_paths':x['changed_paths']} for x in batch['operations']]
    result={'actual_model_calls':1,'main_entry':1630,'main_unchanged':True,'weights_unchanged':True,'activation':False,'input_token_ids_equal_reference':raw['input_token_ids']==reference['input_token_ids'],'first256_output_ids_equal_reference':raw['generated_token_ids'][:256]==reference['generated_token_ids'],'output_tokens':len(raw['generated_token_ids']),'stop':raw['stop'],'complete_cells':batch['parsed']['complete_executable_cells'],'incomplete_fences':sum(not c['complete'] for c in batch['parsed']['cells']),'before_id':before['id'],'after_id':after['id'],'operations':receipts,'world_verification':verify_store(H/'world'),'training_updates':0,'interpretation_scope':'Single larger-budget generation, not evidence of repaired capability, developmental change, learning, or a selected main policy.'}
    save('RESULTS.json',result);(H/'PENDING.json').unlink();print(json.dumps(result),flush=True)

if __name__=='__main__':execute()
