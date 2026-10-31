"""Fixed-budget explicit-status acquisition. Local CPU only, no output-based retry."""
from pathlib import Path
import gc
import json
import os
import sys
import time

os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
import torch
import torch.nn.functional as F
from lora_cpu import inject_lora, save_adapter
from runtime_reference import Guard, GuardStop, parameter_digest, sha, dump_new, append_json

ROOT = Path(__file__).resolve().parent
BASE = Path('/workspace/cache_backend_models/smollm2-135m')

def prompt(case, mapping, plan):
    mapping_text = '; '.join(f'{s}={label}' for s, label in mapping.items())
    return plan['prompt_template'].format(mapping=mapping_text, source=case['source'])

def encoding(tok, case, mapping, plan):
    msg = [{'role': 'user', 'content': prompt(case, mapping, plan)}]
    return msg, tok.apply_chat_template(msg, tokenize=True, add_generation_prompt=True)

def targets(tok, mapping):
    return {state: tok.encode(label, add_special_tokens=False) + [tok.eos_token_id]
            for state, label in mapping.items()}

def summarize_rows(rows):
    from collections import Counter
    report = {}
    for arm in sorted({r['arm'] for r in rows}):
        report[arm] = {}
        for phase in ('base', 'trained'):
            report[arm][phase] = {}
            for split in ('seen', 'primary'):
                rs = [r for r in rows if r['arm'] == arm and r['phase'] == phase and r['split'] == split]
                report[arm][phase][split] = {'n': len(rs),
                    'free_correct': sum(r['free_correct'] for r in rs),
                    'first_token_correct': sum(r['first_token_correct'] for r in rs),
                    'constrained_sum_correct': sum(r['sum_correct'] for r in rs),
                    'constrained_mean_correct': sum(r['mean_correct'] for r in rs),
                    'unresolved': sum(r['free_state'] is None for r in rs),
                    'eos_stops': sum(r['stop'] == 'eos' for r in rs),
                    'predicted_states': dict(Counter(r['free_state'] or 'UNRESOLVED' for r in rs)),
                    'by_state': {s: {'n': sum(r['state'] == s for r in rs),
                         'free_correct': sum(r['state'] == s and r['free_correct'] for r in rs),
                         'sum_correct': sum(r['state'] == s and r['sum_correct'] for r in rs)}
                         for s in ('positive', 'zero', 'missing')}}
    return report

def evaluate(model, tok, cases, mapping, plan, arm, phase, guard):
    model.eval()
    target = targets(tok, mapping)
    rows = []
    for case in cases:
        guard.read('eval_before', arm=arm, phase_label=phase, case=case['id'])
        msg, ids = encoding(tok, case, mapping, plan)
        start = time.perf_counter()
        with torch.inference_mode():
            x = torch.tensor([ids]); mask = torch.ones_like(x)
            out = model(input_ids=x, attention_mask=mask, use_cache=True)
            first = out.logits[0, -1].float().clone()
            cache, logits = out.past_key_values, first
            generated, stop = [], 'token_limit'
            for j in range(plan['max_tokens']):
                token = int(logits.argmax()); generated.append(token)
                if token == tok.eos_token_id:
                    stop = 'eos'; break
                if j + 1 < plan['max_tokens']:
                    out = model(input_ids=torch.tensor([[token]]), past_key_values=cache,
                                attention_mask=torch.ones((1, cache.get_seq_length()+1), dtype=torch.long), use_cache=True)
                    cache, logits = out.past_key_values, out.logits[0, -1]
            del out, cache
            # Three padded teacher-forced completions, actual sequence lengths retained.
            lengths = [len(ids) + len(t) for t in target.values()]
            padded = torch.full((3, max(lengths)), tok.pad_token_id if tok.pad_token_id is not None else tok.eos_token_id)
            attention = torch.zeros_like(padded)
            for k, t in enumerate(target.values()):
                seq = ids + t
                padded[k, :len(seq)] = torch.tensor(seq); attention[k, :len(seq)] = 1
            output = model(input_ids=padded, attention_mask=attention, use_cache=False)
            scores = {}
            for k, (state, t) in enumerate(target.items()):
                logp = F.log_softmax(output.logits[k, len(ids)-1:len(ids)+len(t)-1].float(), dim=-1)
                token_lp = logp.gather(1, torch.tensor(t).view(-1, 1)).flatten().tolist()
                first_id = t[0]
                scores[state] = {'label': mapping[state], 'ids_including_eos': t,
                    'token_logprobs': token_lp, 'sum': sum(token_lp), 'mean': sum(token_lp)/len(t),
                    'first_token_logprob': float(F.log_softmax(first, -1)[first_id]),
                    'first_token_rank': int((first > first[first_id]).sum()) + 1}
            del output, padded, attention
        text = tok.decode(generated, skip_special_tokens=True)
        reverse = {label: state for state, label in mapping.items()}
        state_free = reverse.get(text.strip())
        chosen_sum = max(scores, key=lambda s: scores[s]['sum'])
        chosen_mean = max(scores, key=lambda s: scores[s]['mean'])
        row = {'arm': arm, 'phase': phase, 'id': case['id'], 'split': case['split'],
               'state': case['state'], 'messages': msg, 'input_token_ids': ids,
               'generated_token_ids': generated, 'text': text, 'stop': stop,
               'free_state': state_free, 'free_correct': state_free == case['state'],
               'first_token_correct': generated[0] == target[case['state']][0],
               'sum_state': chosen_sum, 'mean_state': chosen_mean,
               'sum_correct': chosen_sum == case['state'], 'mean_correct': chosen_mean == case['state'],
               'sum_tied': sum(v['sum'] == scores[chosen_sum]['sum'] for v in scores.values()) > 1,
               'mean_tied': sum(v['mean'] == scores[chosen_mean]['mean'] for v in scores.values()) > 1,
               'choice_scores': scores, 'seconds': time.perf_counter()-start}
        append_json(ROOT / 'run' / 'RAW.jsonl', row); rows.append(row)
        guard.read('eval_after', arm=arm, phase_label=phase, case=case['id'])
    return rows

def main():
    plan, cases = json.loads((ROOT / 'PLAN.json').read_text()), json.loads((ROOT / 'DATA.json').read_text())
    freeze = json.loads((ROOT / 'FREEZE.json').read_text())
    assert all(sha(ROOT / name) == h for name, h in freeze['sha256'].items())
    assert sha(BASE / 'model.safetensors') == plan['base_weights_sha256']
    out = ROOT / 'run'; out.mkdir()  # no overwrite or automatic retry
    dump_new(out / 'INPUTS.json', {'freeze_sha256': sha(ROOT / 'FREEZE.json'),
         'base_files_sha256': {p.name: sha(p) for p in BASE.iterdir() if p.is_file()},
         'torch_version': torch.__version__, 'full_kv_caches_retained': False})
    from transformers import AutoTokenizer, AutoModelForCausalLM
    torch.set_num_threads(2)
    tok = AutoTokenizer.from_pretrained(BASE, local_files_only=True, trust_remote_code=False)
    tokenization = {}
    for arm, mapping in plan['mappings'].items():
        target = targets(tok, mapping)
        assert len({tuple(v) for v in target.values()}) == 3
        if arm.startswith('alias'):
            assert all(len(v) == 2 for v in target.values()), 'aliases must each be exactly one token plus EOS'
        lengths = [len(encoding(tok, c, mapping, plan)[1]) + len(target[c['state']]) for c in cases]
        assert max(lengths) <= plan['train_token_guard']
        tokenization[arm] = {'targets': target, 'max_full_tokens': max(lengths)}
    dump_new(out / 'TOKENIZATION.json', tokenization)
    guard = Guard(plan['working_limit_bytes'], out / 'RESOURCE.jsonl')
    rows, manifests, initial_reference = [], {}, None
    byid = {c['id']: c for c in cases}
    for arm, mapping in plan['mappings'].items():
        guard.read('before_load', arm=arm)
        torch.manual_seed(plan['seed'])
        model = AutoModelForCausalLM.from_pretrained(BASE, local_files_only=True, trust_remote_code=False,
            use_safetensors=True, torch_dtype=torch.float32, attn_implementation='eager')
        inventory = inject_lora(model, rank=4, alpha=8, dropout=0.)
        assert inventory['trainable_parameter_count'] == 230400
        frozen_before, initial = parameter_digest(model, False), parameter_digest(model, True)
        if initial_reference is None:
            initial_reference = initial
        assert initial == initial_reference
        pin = {'model_id': 'HuggingFaceTB/SmolLM2-135M-Instruct', 'revision': plan['base_revision'],
               'weights_sha256': plan['base_weights_sha256']}
        armdir = out / arm; armdir.mkdir()
        save_adapter(model, armdir / 'initial', base_pin=pin)
        rows.extend(evaluate(model, tok, cases, mapping, plan, arm, 'base', guard))
        params = [p for p in model.parameters() if p.requires_grad]
        optimizer = torch.optim.AdamW(params, lr=plan['lr'], weight_decay=plan['weight_decay'], foreach=False)
        target = targets(tok, mapping)
        begun = time.perf_counter(); completed = 0
        for step, group in enumerate(plan['order'], 1):
            if time.perf_counter()-begun >= plan['training_wall_seconds_per_arm']:
                raise TimeoutError(f'{arm} training cap; preserve partial output, no automatic retry')
            optimizer.zero_grad(set_to_none=True); model.train()
            micros = []
            for cid in group:
                c = byid[cid]; assert c['split'] == 'seen'
                guard.read('train_before', arm=arm, step=step, case=cid)
                _, ids = encoding(tok, c, mapping, plan); t = target[c['state']]
                x = torch.tensor([ids + t]); assert x.shape[1] <= plan['train_token_guard']
                output = model(input_ids=x, attention_mask=torch.ones_like(x), use_cache=False)
                logits = output.logits[0, len(ids)-1:len(ids)+len(t)-1]
                loss = F.cross_entropy(logits.float(), torch.tensor(t))
                assert torch.isfinite(loss)
                micros.append({'id': cid, 'state': c['state'], 'loss': float(loss.detach())})
                (loss/3).backward()
                del output, logits, x, loss
                guard.read('train_after_backward', arm=arm, step=step, case=cid)
            norm = torch.nn.utils.clip_grad_norm_(params, 1., foreach=False)
            assert torch.isfinite(norm)
            optimizer.step(); completed += 1
            guard.read('train_after_step', arm=arm, step=step)
            assert all(torch.isfinite(p).all() for p in params)
            record = {'arm': arm, 'step': step, 'micro': micros, 'gradient_norm': float(norm),
                      'loss': sum(m['loss'] for m in micros)/3}
            append_json(armdir / 'TRAINING.jsonl', record)
            if step % 12 == 0:
                print(json.dumps({'arm': arm, 'step': step, 'loss': record['loss']}), flush=True)
        training_seconds = time.perf_counter()-begun
        optimizer.zero_grad(set_to_none=True)
        assert parameter_digest(model, False) == frozen_before
        save_adapter(model, armdir / 'final', base_pin=pin)
        torch.save({'optimizer': optimizer.state_dict(), 'completed_updates': completed,
                    'order': plan['order'], 'seed': plan['seed']}, armdir / 'optimizer_state.pt')
        manifest = {'arm': arm, 'completed_updates': completed, 'training_seconds': training_seconds,
            'initial_digest': initial, 'base_digest_before': frozen_before,
            'base_digest_after': parameter_digest(model, False), 'final_digest': parameter_digest(model, True),
            'mapping': mapping, 'base_pin': pin, 'trainable_parameters': inventory['trainable_parameter_count'],
            'binary_sha256': {str(p.relative_to(armdir)): sha(p) for p in armdir.rglob('*') if p.is_file()}}
        dump_new(armdir / 'MANIFEST.json', manifest); manifests[arm] = manifest
        del optimizer, params; gc.collect()
        rows.extend(evaluate(model, tok, cases, mapping, plan, arm, 'trained', guard))
        del model; gc.collect()
        print(json.dumps({'arm': arm, 'finished': True}), flush=True)
    assert len(rows) == 192
    assert sha(BASE / 'model.safetensors') == plan['base_weights_sha256']
    dump_new(out / 'SUMMARY.json', summarize_rows(rows))
    dump_new(out / 'RUN_MANIFEST.json', {'status': 'complete', 'rows': len(rows),
        'generation_calls': 192, 'candidate_scoring_batch_calls': 192, 'candidate_sequences': 576,
        'training_examples': 576, 'updates': 192, 'arms': manifests,
        'base_weights_unchanged': True, 'freeze_still_matches': all(sha(ROOT / n) == h for n, h in freeze['sha256'].items()),
        'raw_sha256': sha(out / 'RAW.jsonl')})

if __name__ == '__main__':
    main()
