"""Eight detached one-step trials. Never calls or alters the canonical runner."""
from pathlib import Path
import difflib, hashlib, importlib.util, json, math, os, sys
for k,v in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():
    os.environ[k] = v
H = Path(__file__).resolve().parent
P = H.parent / 'final-garden-contract-v1'
A = H.parent / 'frozen-garden-tool-path-audit-v1'
sys.path[:0] = [str(P),str(P.parent / 'source-access-three-cycle-v1')]
import runner
from world import World, receive
from generation import generate as original_generate
from runtime_reference import Guard, parameter_digest

def save(path, value):
    p = H / path
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x') as f:
        json.dump(value,f,indent=2,ensure_ascii=False,allow_nan=False)
        f.write('\n')

def main():
    canonical = runner.file_inventory(P)
    assert canonical == runner.read(A / 'CANONICAL_BEFORE.json')
    state = runner.state()
    assert state['paused'] and state['next_entry'] == 1550
    assert not (runner.R / 'PENDING.json').exists() and not (runner.R / 'RUN.lock').exists()
    runner.verify_pins()
    base = runner.read(runner.R / 'bundles/001550.json')
    messages = runner.native_messages(base,runner.rows())
    assert messages == runner.read(runner.R / 'raw/001550.json')['messages']
    original = (P / 'generation.py').read_text()
    mask = "   remove=torch.cumsum(p,0)-p>=.9;v=v.masked_fill(remove,float('-inf'))"
    metadata = 'temperature=.8,top_p=.9)'
    assert original.count(mask) == original.count(metadata) == 1
    alternative = original.replace(mask,'   # Experimental condition: omit nucleus filtering; retain full softmax.')
    alternative = alternative.replace(metadata,'temperature=.8,top_p=None)')
    for name, text in [('original_generation_reference.py',original),('full_distribution_generation.py',alternative)]:
        with (H / name).open('x') as f:
            f.write(text)
    with (H / 'SAMPLER_CHANGE.diff').open('x') as f:
        f.writelines(difflib.unified_diff(original.splitlines(True),alternative.splitlines(True),
            fromfile='frozen/generation.py',tofile='detached/full_distribution_generation.py'))
    spec = importlib.util.spec_from_file_location('detached_full_distribution_generation',H / 'full_distribution_generation.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    seeds = [runner.entry_seed(n) for n in range(1551,1555)]
    trace = runner.read(A / 'SAMPLER_TRACE.json')
    log_repeat = sum(math.log(s['target_full_probability']) for s in trace['steps'])
    repeat = math.exp(log_repeat)
    plan = {'version':'detached-sampler-comparison-v1','canonical_paused_at':1550,
        'design':'Four matched seed pairs; eight independent one-step restorations of the same checkpoint and input; no rolling continuation',
        'seeds':seeds,'seed_selection':'Frozen absolute-entry rule evaluated for 1551 through 1554 before outcomes; these are not canonical entries',
        'arms':['original_top_p_0.9','nucleus_filter_removed'],
        'order':'For each seed: original then unfiltered. Each trial gets a fresh model KV and independent world restoration.',
        'temperature':.8,'output_tokens':96,'input_limit':8096,
        'changed_factor':'Only the nucleus mask is removed in the alternative; metadata identifies top_p as null. Sorting, softmax, RNG, temperature, model and input remain unchanged.',
        'model':runner.read(P / 'CONTRACT.json')['model'],
        'source_generator_sha256':hashlib.sha256(original.encode()).hexdigest(),
        'alternative_generator_sha256':hashlib.sha256(alternative.encode()).hexdigest(),
        'checkpoint_id':base['id'],'canonical_generation_calls':0,'planned_external_generation_calls':8,
        'training_updates':0,'new_prompts_or_demonstrations':False,
        'world_effects':'Dispatch each generated reply through unchanged receive() on a separate disposable checkpoint; preserve actual receipts and snapshots. No outcome or fixture is fed to canonical model.',
        'feedback_response_limit':'These are single-step trials. No subsequent response to any new receipt is measured.',
        'outcomes':['exact bytes and tokens','EOS versus token cap','same text as baseline','whole-reply action dispatch','actual effects and feedback','non-notebook state changes'],
        'limits':'Four seeds on one input are descriptive; no inference about long-run exploration, learning or general model ability. No adaptive extra trials.',
        'prior_trace_prediction':{'full_softmax_probability_of_exact_baseline_path':repeat,
            'probability_all_four_repeat_if_independent_draws':repeat**4,
            'scope':'Calculated from previously retained temperature-scaled probabilities before new trials. Ideal sampling interpretation; seeds are deterministic PRNG inputs, not guaranteed independent physical draws.'}}
    save('PLAN.json',plan)
    save('CANONICAL_BEFORE.json',canonical)
    save('INITIAL_CHECKPOINT.json',base)
    save('INITIAL_MESSAGES.json',messages)
    print(json.dumps({'planned_trials':8,'seeds':seeds,'prior_exact_path_probability_unfiltered':repeat}),flush=True)

    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    torch.set_num_threads(2)
    guard = Guard(5153960755,H / 'RESOURCE.jsonl')
    guard.read('before_load')
    tok = AutoTokenizer.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False,
        use_safetensors=True,torch_dtype=torch.float32,attn_implementation='eager')
    model.requires_grad_(False)
    model.eval()
    tensor_pin = runner.read(runner.R / 'MODEL_CONDITION.json')['tensor_digest']
    assert parameter_digest(model,False) == tensor_pin
    ids = tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
    expected_raw = runner.read(runner.R / 'raw/001550.json')
    assert ids == expected_raw['input_token_ids']
    results = []
    for seed in seeds:
        for arm, generate in [('original_top_p_0.9',original_generate),('nucleus_filter_removed',mod.generate)]:
            name = f'{seed}_{arm}'
            save('plans/'+name+'.json',{'seed':seed,'arm':arm,'input_token_ids':ids,'before_id':base['id']})
            raw = generate(model,tok,messages,guard,'detached_'+name,seed)
            assert raw['input_token_ids'] == ids and raw['messages'] == messages
            assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True) == raw['text']
            assert raw['rng_seed'] == seed and 0 < len(raw['generated_token_ids']) <= 96
            assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==96)
            if arm == 'original_top_p_0.9':
                assert raw['generated_token_ids'] == expected_raw['generated_token_ids']
            save('raw/'+name+'.json',raw)
            w = World()
            try:
                w.restore(base,runner.R / 'objects')
                before = w.capture(H / 'objects')
                assert before == base
                # Actual generated text is dispatched without repair or extraction.
                result = receive(w,raw['text'])
                after = w.capture(H / 'objects')
                restore = World()
                try:
                    restore.restore(after,H / 'objects')
                    assert restore.capture(H / 'objects') == after
                finally:
                    restore.close()
            finally:
                w.close()
            save('results/'+name+'.json',result)
            save('bundles/'+name+'.json',after)
            b = {x[0]:x for x in before['entries']}
            a = {x[0]:x for x in after['entries']}
            changed = [n for n in sorted(set(a)|set(b)) if a.get(n) != b.get(n)]
            record = {'seed':seed,'arm':arm,'text':raw['text'],'stop':raw['stop'],
                'tokens_including_eos':len(raw['generated_token_ids']),
                'same_text_as_baseline':raw['text']==expected_raw['text'],
                'same_tokens_as_baseline':raw['generated_token_ids']==expected_raw['generated_token_ids'],
                'kind':result['kind'],'visible_feedback':runner.model_feedback(result['feedback']),
                'changed_paths':changed,'non_notebook_changed_paths':[n for n in changed if n!='notebook.txt'],
                'before_id':before['id'],'after_id':after['id'],'restoration_passed':True,
                'raw_sha256':hashlib.sha256((H / 'raw' / (name+'.json')).read_bytes()).hexdigest()}
            save('events/'+name+'.json',record)
            results.append(record)
            assert parameter_digest(model,False) == tensor_pin
            assert runner.file_inventory(P) == canonical
            print(json.dumps(record,ensure_ascii=False),flush=True)
    assert len(results) == 8 and runner.file_inventory(P) == canonical
    runner.verify_pins()
    assert runner.state() == state
    save('COMPLETED.json',{'status':'pass','canonical_inventory_unchanged':True,
        'canonical_files_checked':len(canonical),'canonical_paused_at':1550,
        'canonical_generation_calls':0,'external_generation_calls':len(results),
        'source_generator_unchanged':(P / 'generation.py').read_text()==original,
        'training_updates':0,'weights_tensor_digest_unchanged':True,
        'all_inputs_identical':True,'all_trials_restored_same_checkpoint':True,
        'all_trial_checkpoints_restorable':True,'planned_seeds_completed':seeds,
        'results':results})
    print(json.dumps({'status':'pass','completed_external_calls':len(results),'canonical_paused_at':1550}),flush=True)

if __name__ == '__main__':
    main()
