"""External, teacher-forced probability trace; no sampling or garden step."""
from pathlib import Path
import hashlib, json, math, os, sys
for name, value in {'HF_HUB_OFFLINE':'1', 'OMP_NUM_THREADS':'2', 'OPENBLAS_NUM_THREADS':'1', 'MKL_NUM_THREADS':'2'}.items():
    os.environ[name] = value
H = Path(__file__).resolve().parent
P = H.parent / 'final-garden-contract-v1'
sys.path[:0] = [str(P), str(P.parent / 'source-access-three-cycle-v1')]
import runner
from runtime_reference import Guard, parameter_digest
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def dump(name, value):
    with (H / name).open('x') as f:
        json.dump(value, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write('\n')

def main():
    baseline = runner.file_inventory(P)
    assert baseline == runner.read(H / 'CANONICAL_BEFORE.json')
    runner.verify_pins()
    torch.set_num_threads(2)
    guard = Guard(5153960755, H / 'SAMPLER_RESOURCE.jsonl')
    guard.read('before_load')
    tok = AutoTokenizer.from_pretrained(runner.BASE, local_files_only=True, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(runner.BASE, local_files_only=True, trust_remote_code=False,
        use_safetensors=True, torch_dtype=torch.float32, attn_implementation='eager')
    model.requires_grad_(False)
    model.eval()
    tensor_pin = parameter_digest(model, False)
    assert tensor_pin == runner.read(runner.R / 'MODEL_CONDITION.json')['tensor_digest']
    raw = runner.read(runner.R / 'raw/001550.json')
    bundle = runner.read(runner.R / 'bundles/001550.json')
    messages = runner.native_messages(bundle, runner.rows())
    ids = tok.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
    assert ids == raw['input_token_ids']
    targets = raw['generated_token_ids']
    fixtures = [json.dumps({'action':'shell','source':s}) for s in ['pwd', 'cat LAWS.txt', "python3 -I -S -c 'print(6*7)'"]]
    token_budget = [{'text':s, 'tokens_including_eos':len(tok.encode(s, add_special_tokens=False))+1,
                     'within_96':len(tok.encode(s, add_special_tokens=False))+1 <= 96} for s in fixtures]
    steps = []
    log_path_prob = 0.0
    guard.read('before_prefill')
    with torch.inference_mode():
        x = torch.tensor([ids])
        o = model(input_ids=x, attention_mask=torch.ones_like(x), use_cache=True, logits_to_keep=1)
        cache, logits = o.past_key_values, o.logits[0,-1]
        for pos, target in enumerate(targets):
            z = logits.float() / .8
            v, ix = torch.sort(z, descending=True)
            full = torch.softmax(v, dim=-1)
            remove = torch.cumsum(full, 0) - full >= .9
            filtered = torch.softmax(v.masked_fill(remove, float('-inf')), dim=0)
            index = int(torch.nonzero(ix == target, as_tuple=False)[0])
            p = float(filtered[index])
            log_path_prob = log_path_prob + math.log(p) if p > 0 else float('-inf')
            support = torch.nonzero(filtered > 0, as_tuple=False).flatten()
            alternatives = [{'id':int(ix[j]), 'token':tok.decode([int(ix[j])]),
                             'probability_full_temperature_scaled':float(full[j]),
                             'probability_after_top_p':float(filtered[j])} for j in support[:20]]
            steps.append({'position':pos, 'target_id':target, 'target_text':tok.decode([target]),
                'nucleus_size':int((~remove).sum()), 'positive_support_size':len(support),
                'target_rank':index+1, 'target_full_probability':float(full[index]),
                'target_post_top_p_probability':p, 'top_retained':alternatives})
            if pos == 0:
                candidate_ids = sorted({tok.encode(t,add_special_tokens=False)[0] for t in ['{','{"',' {','\n{','\n {',' \n{']})
                starts = []
                for token in candidate_ids:
                    j = int(torch.nonzero(ix == token, as_tuple=False)[0])
                    starts.append({'id':token, 'text':tok.decode([token]), 'rank':j+1,
                        'full_probability':float(full[j]), 'post_top_p_probability':float(filtered[j]),
                        'retained':not bool(remove[j])})
            if pos < len(targets)-1:
                o = model(input_ids=torch.tensor([[target]]), past_key_values=cache,
                    attention_mask=torch.ones((1,cache.get_seq_length()+1),dtype=torch.long),
                    use_cache=True,logits_to_keep=1)
                cache, logits = o.past_key_values, o.logits[0,-1]
    guard.read('after_trace')
    assert parameter_digest(model, False) == tensor_pin
    assert runner.file_inventory(P) == baseline
    summary = {'canonical_entry':1550, 'next_input_identical_to_last_input':True,
        'input_tokens':len(ids), 'input_ids_sha256':hashlib.sha256(json.dumps(ids,separators=(',',':')).encode()).hexdigest(),
        'teacher_forced_target_text':raw['text'], 'target_tokens_including_eos':len(targets),
        'all_positions_singleton_target_support':all(s['positive_support_size']==1 and s['target_post_top_p_probability']==1 for s in steps),
        'positions_with_alternatives':[s['position'] for s in steps if s['positive_support_size']>1],
        'conditional_probability_of_exact_recorded_path':math.exp(log_path_prob),
        'first_token_example_json_starts_not_exhaustive':starts,
        'minimal_action_token_budgets':token_budget,
        'canonical_model_calls':0, 'external_prefills':1, 'external_cached_teacher_forced_forwards':len(targets)-1,
        'generated_or_sampled_tokens':0, 'training_updates':0, 'canonical_inventory_unchanged':True,
        'scope':'Exact current input and exact recorded path under the pinned model, dtype, attention, temperature and top-p implementation. Not a prompt ablation, not a test of independent tool choice, and not a proof about alternate inputs or future infrastructure.',
        'steps':steps}
    dump('SAMPLER_TRACE.json', summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['steps','first_token_example_json_starts_not_exhaustive','minimal_action_token_budgets']}))

if __name__ == '__main__':
    main()
