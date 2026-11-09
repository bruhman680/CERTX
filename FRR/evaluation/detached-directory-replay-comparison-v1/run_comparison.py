"""Detached 2x2 input-policy comparison; never changes the frozen garden."""
from pathlib import Path
import copy, hashlib, importlib.util, json, os, sys
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():
    os.environ[k] = v
H = Path(__file__).resolve().parent
P = H.parent / 'final-garden-contract-v1'
S = H.parent / 'detached-sampler-comparison-v1'
sys.path[:0] = [str(P),str(P.parent / 'source-access-three-cycle-v1')]
import runner
from world import World, receive
from runtime_reference import Guard, parameter_digest

ARMS = [
    {'id':'replay12_directory','replay':True,'directory':True},
    {'id':'replay12_no_directory','replay':True,'directory':False},
    {'id':'no_replay_directory','replay':False,'directory':True},
    {'id':'no_replay_no_directory','replay':False,'directory':False},
]

def save(path,value):
    p = H / path
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:
        json.dump(value,f,indent=2,ensure_ascii=False,allow_nan=False)
        f.write('\n')

def rendered_condition(baseline,suffix,arm):
    if arm['replay']:
        messages = copy.deepcopy(baseline)
        assert messages[-1] == {'role':'user','content':suffix}
        if not arm['directory']:
            messages[-1]['content'] = ''
    else:
        messages = copy.deepcopy(baseline[:2])
        if arm['directory']:
            messages[-1]['content'] += suffix
    return messages

def main():
    canonical = runner.file_inventory(P)
    assert canonical == runner.read(S / 'CANONICAL_BEFORE.json')
    runner.verify_pins()
    state = runner.state()
    assert state['paused'] and state['next_entry'] == 1550
    assert not (runner.R / 'PENDING.json').exists() and not (runner.R / 'RUN.lock').exists()
    initial = runner.read(runner.R / 'bundles/001550.json')
    baseline = runner.native_messages(initial,runner.rows())
    assert baseline == runner.read(S / 'INITIAL_MESSAGES.json')
    names = sorted(set(x[0].split('/')[0] for x in initial['entries']))
    suffix = '\nDirectory entries: '+json.dumps(names,ensure_ascii=False)
    assert baseline[-1]['content'] == suffix
    generator_source = (S / 'full_distribution_generation.py').read_bytes()
    previous_plan = runner.read(S / 'PLAN.json')
    assert hashlib.sha256(generator_source).hexdigest() == previous_plan['alternative_generator_sha256']
    with (H / 'full_distribution_generation.py').open('xb') as f:
        f.write(generator_source)
    spec = importlib.util.spec_from_file_location('directory_replay_full_distribution',H / 'full_distribution_generation.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    seeds = previous_plan['seeds']
    assert seeds == [runner.entry_seed(n) for n in range(1551,1555)]
    conditions = {arm['id']:rendered_condition(baseline,suffix,arm) for arm in ARMS}
    plan = {'version':'detached-directory-replay-comparison-v1','canonical_paused_at':1550,
        'design':'2x2 directory/replay input-policy comparison, four matched seeds, sixteen independent one-step trials',
        'arms':ARMS,'seeds':seeds,'order':'Each seed in order, all four arms in declared order; no adaptive extension',
        'seed_origin':'Same four seeds as preceding sampler comparison; controls are reproducibility checks, not new independent seeds',
        'temperature':.8,'nucleus_filtering':False,'output_tokens':96,'input_limit':8096,
        'generation_source_sha256':hashlib.sha256(generator_source).hexdigest(),
        'model':runner.read(P / 'CONTRACT.json')['model'],'checkpoint_id':initial['id'],
        'planned_external_generation_calls':16,'canonical_generation_calls':0,'training_updates':0,
        'fixed':'Same initial world bytes, model, tokenizer, invitation, mechanics notice, empty system, full-softmax sampler, limits and parser',
        'directory_ablation':'Remove only automatic current directory suffix. Historical listings in replay and filename mentions in NOTICE remain where otherwise present.',
        'replay_ablation':'Remove all twelve assistant/user history pairs. Directory suffix, when enabled, follows the unchanged initial user notice/seed. This changes turn count and positions as part of the delivery-policy ablation; not a token-length- or role-position-matched psychology experiment.',
        'both_removed':'Only explicit empty system and original user notice/seed remain; no new task or hint',
        'world_dispatch':'Unmodified receive() applied to each raw output on an independently restored disposable checkpoint; capture and restore actual effects without semantic grading',
        'feedback_scope':'Single-step trials; no followup response to newly generated feedback is tested',
        'interpretation_limits':'One checkpoint and four seeds. Surface variety is not learning or better exploration. Removing replay removes automatic short-term context; these arms are not an adopted persistent-memory policy.'}
    save('PLAN.json',plan)
    save('CANONICAL_BEFORE.json',canonical)
    save('INITIAL_CHECKPOINT.json',initial)
    save('INITIAL_MESSAGES.json',baseline)
    for arm in ARMS:
        save('conditions/'+arm['id']+'.json',{'arm':arm,'messages':conditions[arm['id']]})
    print(json.dumps({'planned_external_trials':16,'seeds':seeds,'arms':[a['id'] for a in ARMS]}),flush=True)

    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    torch.set_num_threads(2)
    guard = Guard(5153960755,H / 'RESOURCE.jsonl')
    guard.read('before_model_load')
    tok = AutoTokenizer.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False)
    ids = {arm['id']:tok.apply_chat_template(conditions[arm['id']],tokenize=True,add_generation_prompt=True) for arm in ARMS}
    assert ids['replay12_directory'] == runner.read(runner.R / 'raw/001550.json')['input_token_ids']
    save('CONDITION_TOKENS.json',{name:{'input_token_ids':values,'tokens':len(values),
        'sha256':hashlib.sha256(json.dumps(values,separators=(',',':')).encode()).hexdigest()} for name,values in ids.items()})
    model = AutoModelForCausalLM.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False)
    model.eval()
    tensor_pin = runner.read(runner.R / 'MODEL_CONDITION.json')['tensor_digest']
    assert parameter_digest(model,False) == tensor_pin
    reference_text = runner.read(runner.R / 'raw/001550.json')['text']
    outcomes = []
    for seed in seeds:
        for arm in ARMS:
            name = f"{seed}_{arm['id']}"
            save('plans/'+name+'.json',{'seed':seed,'arm':arm,'before_id':initial['id'],'input_token_ids':ids[arm['id']]})
            raw = mod.generate(model,tok,conditions[arm['id']],guard,'detached_'+name,seed)
            assert raw['input_token_ids'] == ids[arm['id']] and raw['messages'] == conditions[arm['id']]
            assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True) == raw['text']
            assert raw['rng_seed'] == seed and 0<len(raw['generated_token_ids'])<=96
            assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==96)
            if arm['id']=='replay12_directory':
                prior = runner.read(S / 'raw' / f'{seed}_nucleus_filter_removed.json')
                assert raw['generated_token_ids'] == prior['generated_token_ids']
            save('raw/'+name+'.json',raw)
            world = World()
            try:
                world.restore(initial,runner.R / 'objects')
                before = world.capture(H / 'objects')
                assert before == initial
                result = receive(world,raw['text'])
                after = world.capture(H / 'objects')
                second = World()
                try:
                    second.restore(after,H / 'objects')
                    assert second.capture(H / 'objects') == after
                finally:
                    second.close()
            finally:
                world.close()
            save('results/'+name+'.json',result)
            save('bundles/'+name+'.json',after)
            b,a = {x[0]:x for x in before['entries']},{x[0]:x for x in after['entries']}
            changed = [n for n in sorted(set(a)|set(b)) if a.get(n)!=b.get(n)]
            event = {'seed':seed,'arm':arm['id'],'text':raw['text'],'stop':raw['stop'],
                'output_tokens_including_eos':len(raw['generated_token_ids']),'input_tokens':len(raw['input_token_ids']),
                'same_text_as_directory_baseline':raw['text']==reference_text,
                'kind':result['kind'],'visible_feedback':runner.model_feedback(result['feedback']),
                'changed_paths':changed,'non_notebook_changed_paths':[n for n in changed if n!='notebook.txt'],
                'before_id':before['id'],'after_id':after['id'],'restoration_passed':True,
                'raw_sha256':hashlib.sha256((H / 'raw' / (name+'.json')).read_bytes()).hexdigest()}
            save('events/'+name+'.json',event)
            outcomes.append(event)
            assert parameter_digest(model,False) == tensor_pin
            assert runner.file_inventory(P) == canonical
            print(json.dumps(event,ensure_ascii=False),flush=True)
    assert len(outcomes)==16 and runner.file_inventory(P)==canonical
    runner.verify_pins()
    assert runner.state()==state
    save('COMPLETED.json',{'status':'pass','canonical_paused_at':1550,'canonical_inventory_unchanged':True,
        'canonical_files_checked':len(canonical),'canonical_generation_calls':0,'external_generation_calls':16,
        'training_updates':0,'tensor_digest_unchanged':True,'all_checkpoints_restored':True,
        'all_reference_outputs_reproduced':True,'seeds':seeds,'results':outcomes})
    print(json.dumps({'status':'pass','external_generation_calls':16,'canonical_paused_at':1550}),flush=True)

if __name__ == '__main__':
    main()
