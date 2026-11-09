"""Direct-request and exact-copy diagnostic controls; no canonical contact."""
from pathlib import Path
import copy, hashlib, importlib.util, json, os, sys
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():
    os.environ[k] = v
H = Path(__file__).resolve().parent
P = H.parent / 'final-garden-contract-v1'
D = H.parent / 'detached-directory-replay-comparison-v1'
S = H.parent / 'detached-sampler-comparison-v1'
sys.path[:0] = [str(P),str(P.parent / 'source-access-three-cycle-v1')]
import runner
from world import World, receive, action
from runtime_reference import Guard, parameter_digest

TARGET = '{"action":"shell","source":"pwd"}'
REQUESTS = {
    'formulate': 'Use the available shell action to run pwd now. Return only the whole-reply action JSON object.',
    'copy_exact': 'Use the available shell action to run pwd now. Return exactly this JSON object, with no explanation or code fence:\n'+TARGET,
}

def save(path,value):
    p = H / path
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:
        json.dump(value,f,indent=2,ensure_ascii=False,allow_nan=False)
        f.write('\n')

def main():
    canonical = runner.file_inventory(P)
    assert canonical == runner.read(D / 'CANONICAL_BEFORE.json')
    runner.verify_pins()
    state = runner.state()
    assert state['paused'] and state['next_entry']==1550
    assert not (runner.R / 'PENDING.json').exists() and not (runner.R / 'RUN.lock').exists()
    checkpoint = runner.read(runner.R / 'bundles/001550.json')
    base_messages = runner.read(D / 'conditions/no_replay_no_directory.json')['messages']
    assert base_messages == [{'role':'system','content':''},{'role':'user','content':runner.NOTICE+'\n\n'+runner.SEED}]
    messages = {}
    for arm,request in REQUESTS.items():
        m = copy.deepcopy(base_messages)
        m[-1]['content']+='\n\n'+request
        messages[arm] = m
    source = (S / 'full_distribution_generation.py').read_bytes()
    assert hashlib.sha256(source).hexdigest()==runner.read(S / 'PLAN.json')['alternative_generator_sha256']
    with (H / 'full_distribution_generation.py').open('xb') as f:
        f.write(source)
    spec = importlib.util.spec_from_file_location('action_control_full_distribution',H / 'full_distribution_generation.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    seeds = runner.read(D / 'PLAN.json')['seeds']
    assert seeds == [runner.entry_seed(n) for n in range(1551,1555)]
    plan = {'version':'detached-action-interface-control-v1','canonical_paused_at':1550,
        'design':'Four matched seeds in two explicit-request conditions; eight independent one-step trials',
        'arms':list(REQUESTS),'requests':REQUESTS,'target_json':TARGET,'target_command':'pwd','target_stdout':'/world\n',
        'seeds':seeds,'seed_origin':'Same predefined four seeds as preceding diagnostics, not new independent draws',
        'order':'Each seed in order; formulate then copy_exact; no adaptive extension',
        'base_condition':'Previous no-replay/no-directory messages: empty system and unchanged mechanical notice plus invitation',
        'changed_factor':'Append an explicit request; copy_exact also supplies target JSON. This is prompted diagnostic coaching, not spontaneous tool use.',
        'fixed':'Same model, tokenizer, world checkpoint, unfiltered sampler, temperature, fresh KV, 96-token output bound, action parser and limits',
        'generation_source_sha256':hashlib.sha256(source).hexdigest(),
        'temperature':.8,'nucleus_filtering':False,'output_tokens':96,
        'checkpoint_id':checkpoint['id'],'planned_external_generation_calls':8,'canonical_generation_calls':0,'training_updates':0,
        'outcomes':['raw text/tokens','parseable JSON','valid exact envelope','requested pwd source','actual runtime stdout/stderr/status','world deltas','EOS/cap'],
        'dispatch':'Unmodified receive() on a fresh disposable checkpoint for every output, without repair, extraction or semantic rejection',
        'no_followup':'Actual receipts retained externally; no second-turn interpretation or feedback response tested',
        'limitations':'One short command, two wordings, four seeds. Copying is not independent formulation, general tool competence, learning, curiosity or emergence. Failure is specific to these prompting/sampling conditions.'}
    save('PLAN.json',plan)
    save('CANONICAL_BEFORE.json',canonical)
    save('INITIAL_CHECKPOINT.json',checkpoint)
    for arm in REQUESTS:
        save('conditions/'+arm+'.json',{'request':REQUESTS[arm],'messages':messages[arm]})
    print(json.dumps({'planned_external_calls':8,'seeds':seeds,'arms':list(REQUESTS)}),flush=True)

    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    torch.set_num_threads(2)
    guard = Guard(5153960755,H / 'RESOURCE.jsonl')
    guard.read('before_load')
    tok = AutoTokenizer.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False)
    ids = {a:tok.apply_chat_template(m,tokenize=True,add_generation_prompt=True) for a,m in messages.items()}
    save('CONDITION_TOKENS.json',{a:{'input_token_ids':v,'tokens':len(v)} for a,v in ids.items()})
    model = AutoModelForCausalLM.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False)
    model.eval()
    tensor_pin = runner.read(runner.R / 'MODEL_CONDITION.json')['tensor_digest']
    assert parameter_digest(model,False)==tensor_pin
    outcomes = []
    for seed in seeds:
        for arm in REQUESTS:
            name = f'{seed}_{arm}'
            save('plans/'+name+'.json',{'seed':seed,'arm':arm,'before_id':checkpoint['id'],'input_token_ids':ids[arm]})
            raw = mod.generate(model,tok,messages[arm],guard,'detached_'+name,seed)
            assert raw['messages']==messages[arm] and raw['input_token_ids']==ids[arm]
            assert raw['rng_seed']==seed and 0<len(raw['generated_token_ids'])<=96
            assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']
            assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==96)
            save('raw/'+name+'.json',raw)
            world = World()
            try:
                world.restore(checkpoint,runner.R / 'objects')
                before = world.capture(H / 'objects')
                assert before==checkpoint
                result = receive(world,raw['text'])
                after = world.capture(H / 'objects')
                restored = World()
                try:
                    restored.restore(after,H / 'objects')
                    assert restored.capture(H / 'objects')==after
                finally:
                    restored.close()
            finally:
                world.close()
            save('results/'+name+'.json',result)
            save('bundles/'+name+'.json',after)
            try:
                parsed = json.loads(raw['text'])
                json_valid = True
            except ValueError:
                parsed, json_valid = None, False
            src = action(raw['text'])
            pwd = src is not None and src.strip()=='pwd'
            receipt = runner.model_feedback(result['feedback'])
            effect = result['kind']=='shell' and receipt['exit_code']==0 and receipt['boundary'] is None and receipt['stdout']=='/world\n'
            b,a = {x[0]:x for x in before['entries']},{x[0]:x for x in after['entries']}
            changed = [n for n in sorted(set(a)|set(b)) if a.get(n)!=b.get(n)]
            event = {'seed':seed,'arm':arm,'text':raw['text'],'stop':raw['stop'],'output_tokens_including_eos':len(raw['generated_token_ids']),
                'json_valid':json_valid,'parsed_json':parsed,'valid_action_envelope':src is not None,
                'source_is_requested_pwd':pwd,'world_stdout_observed':effect,'requested_pwd_executed':pwd and effect,
                'kind':result['kind'],'visible_feedback':receipt,'changed_paths':changed,
                'non_notebook_changed_paths':[n for n in changed if n!='notebook.txt'],
                'before_id':before['id'],'after_id':after['id'],'restoration_passed':True,
                'raw_sha256':hashlib.sha256((H / 'raw' / (name+'.json')).read_bytes()).hexdigest()}
            save('events/'+name+'.json',event)
            outcomes.append(event)
            assert parameter_digest(model,False)==tensor_pin
            assert runner.file_inventory(P)==canonical
            print(json.dumps(event,ensure_ascii=False),flush=True)
    assert len(outcomes)==8 and runner.file_inventory(P)==canonical
    runner.verify_pins()
    assert runner.state()==state
    save('COMPLETED.json',{'status':'pass','canonical_paused_at':1550,'canonical_inventory_unchanged':True,
        'canonical_files_checked':len(canonical),'external_generation_calls':8,'canonical_generation_calls':0,
        'training_updates':0,'tensor_digest_unchanged':True,'all_checkpoints_restored':True,'results':outcomes})
    print(json.dumps({'status':'pass','external_generation_calls':8,'canonical_paused_at':1550}),flush=True)

if __name__=='__main__':
    main()
