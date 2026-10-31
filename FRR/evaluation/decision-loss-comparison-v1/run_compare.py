"""Explicit, single-attempt local run. Never imports evaluation gold keys.

Run with the existing torch/transformers virtualenv. Every output root must be new.
No model is instantiated until main() and the frozen inputs have been verified.
"""
import argparse
import gc
import json
import os
from pathlib import Path
import sys
import time

os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['HF_HUB_DISABLE_PROGRESS_BARS'] = '1'
from runtime import (Guard, GuardStop, LABELS, OBJECTIVES, append_json, balanced_update,
                     dump_new, generate, make_order, parameter_digest, sha)
import torch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--state-root', type=Path, default=Path('/workspace/smollm_decision_compare_states_v1'))
    parser.add_argument('--prior', type=Path, default=Path('/workspace/frr/evaluation/lora-state-pilot-v1'))
    parser.add_argument('--preparation', type=Path, default=Path('/workspace/frr/evaluation/decision-token-preparation-v1'))
    parser.add_argument('--base', type=Path, default=Path('/workspace/cache_backend_models/smollm2-135m'))
    parser.add_argument('--include-regression', action='store_true')
    parser.add_argument('--challenge-cases', type=Path, help='Prospectively frozen source-only challenge file, never keys')
    parser.add_argument('--working-limit-bytes', type=int, default=int(.6 * 8589934592))
    parser.add_argument('--preflight-only', action='store_true', help='One fresh first update, save separately, no evaluation; never reused')
    args = parser.parse_args()
    if args.working_limit_bytes <= 0:
        parser.error('working limit must be positive')
    args.study, args.state_root = args.study.resolve(), args.state_root.resolve()
    if args.study.exists() or args.state_root.exists():
        raise FileExistsError('Both study and state root must be new; no retries or overwrite')
    if args.study == args.state_root or args.study in args.state_root.parents or args.state_root in args.study.parents:
        raise ValueError('Study and state root must be separate nonnested paths')
    # Frozen preparation and prior inputs include keys hashes, never their contents.
    source_hashes = {}
    for root in (args.preparation, args.prior):
        freeze = json.loads((root / 'FREEZE.json').read_text())
        for name, expected in freeze['sha256'].items():
            actual = sha(root / name)
            if actual != expected:
                raise ValueError(f'Frozen source changed: {root / name}')
            source_hashes[str(root / name)] = actual
    bindings = json.loads((args.preparation / 'SOURCE_BINDINGS.json').read_text())
    for name, expected in bindings['reuse_without_edit'].items():
        # Binding paths identify prior filenames; prevent traversal/unrelated resolution.
        path = args.prior / Path(name).name
        if sha(path) != expected:
            raise ValueError(f'Source binding mismatch: {path}')
    preserved = {str(args.prior / name): sha(args.prior / name) for name in
                 ('RAW_OUTPUTS.jsonl', 'TRAINING_LOG.jsonl', 'TRAINING_MANIFEST.json', 'RUN_MANIFEST.json')}
    train = json.loads((args.prior / 'TRAIN.json').read_text())
    oldcases = json.loads((args.prior / 'EVAL_CASES.json').read_text())
    primary = json.loads((args.preparation / 'NEW_PRIMARY_CASES.json').read_text())
    guidance = json.loads((args.prior / 'GUIDANCE.json').read_text())
    challenge = json.loads(args.challenge_cases.read_text()) if args.challenge_cases else []
    if args.challenge_cases:
        if len(challenge) != 36 or any(c.get('split') != 'challenge' for c in challenge):
            raise ValueError('Expected frozen 36-row challenge split')
        source_hashes[str(args.challenge_cases.resolve())] = sha(args.challenge_cases)
    dev = [c for c in oldcases if c['split'] == 'dev']
    regression = [c for c in oldcases if c['split'] == 'test']
    if (len(dev), len(primary), len(regression)) != (12, 24, 48):
        raise ValueError('Unexpected evaluation counts')
    # Reject gold-bearing input records, even if a future file uses a wrong schema.
    for case in dev + primary + regression + challenge:
        if set(case) != {'id', 'split', 'structure_family', 'source'}:
            raise ValueError('Evaluation source schema changed or contains non-source fields')
    order = make_order(train, 73103)
    args.study.mkdir(parents=True); args.state_root.mkdir(parents=True)
    dump_new(args.study / 'INPUTS.json', {'source_hashes': source_hashes, 'prior_preserved': preserved,
              'preparation_freeze_sha256': sha(args.preparation / 'FREEZE.json'),
              'prior_freeze_sha256': sha(args.prior / 'FREEZE.json'),
              'seed': 73103, 'steps': 48, 'lr': .001, 'rank': 4, 'alpha': 8, 'dropout': 0,
              'weight_decay': .01, 'gradient_clip': 1, 'microbatch': 1, 'effective_batch': 3,
              'working_limit_bytes': args.working_limit_bytes, 'wall_seconds_per_arm': 300,
              'preflight_only': args.preflight_only, 'regression_included': args.include_regression,
              'challenge_included': bool(challenge),
              'data_order': [[c['id'] for c in group] for group in order]})
    sys.path.insert(0, str(args.prior))
    from lora_cpu import inject_lora, load_adapter, save_adapter
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from safetensors.torch import load_file
    torch.set_num_threads(2)
    tok = AutoTokenizer.from_pretrained(args.base, local_files_only=True, trust_remote_code=False)
    basepin = {'model_id': 'HuggingFaceTB/SmolLM2-135M-Instruct',
               'revision': '12fd25f77366fa6b3b4b768ec3050bf629380bac',
               'weights_sha256': sha(args.base / 'model.safetensors')}
    guard = Guard(args.working_limit_bytes, args.study / 'RESOURCE_LOG.jsonl')

    def fresh(context):
        guard.read('before_model_load', context=context)
        torch.manual_seed(73103)
        model = AutoModelForCausalLM.from_pretrained(args.base, local_files_only=True,
                    trust_remote_code=False, use_safetensors=True, torch_dtype=torch.float32,
                    attn_implementation='eager')
        inventory = inject_lora(model, rank=4, alpha=8, dropout=0.)
        if inventory['trainable_parameter_count'] != 230400:
            raise ValueError('Unexpected adapter trainable size')
        guard.read('after_model_load', context=context)
        return model, inventory

    manifests = {}
    common_base, common_init = None, None
    for arm in OBJECTIVES[:1] if args.preflight_only else OBJECTIVES:
        arm_root = args.study / arm; arm_root.mkdir()
        try:
            model, inventory = fresh('train_' + arm)
        except GuardStop as exc:
            dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'model_load_resource_stop',
                        'calls': 0, 'primary_forwarded': False, 'manifests': manifests,
                        'stop': exc.reason, 'trigger': exc.trigger, 'no_automatic_retry': True})
            return
        base_before = parameter_digest(model, False)
        init = parameter_digest(model, True)
        if common_base is None:
            common_base, common_init = base_before, init
        if (base_before, init) != (common_base, common_init):
            raise ValueError('Fresh arm base or initial adapter differs')
        initial = arm_root / 'initial_adapter'
        save_adapter(model, initial, base_pin=basepin)
        # Zero product guarantees an exact original baseline mathematical function.
        init_state = load_file(str(initial / 'adapter.safetensors'))
        if not all(torch.count_nonzero(v) == 0 for k, v in init_state.items() if k.endswith('lora_B')):
            raise ValueError('Initial LoRA B is not zero')
        del init_state
        params = [p for p in model.parameters() if p.requires_grad]
        optimizer = torch.optim.AdamW(params, lr=.001, weight_decay=.01, foreach=False)
        completed, exposure, stop, trigger = 0, dict.fromkeys(LABELS, 0), ('fixed_1_preflight_update' if args.preflight_only else 'fixed_48_updates'), None
        completed_ids = []
        begun = time.perf_counter()
        planned = 1 if args.preflight_only else 48
        for i, group in enumerate(order[:planned]):
            # The wall cap is checked between updates; a running update is never killed.
            elapsed = time.perf_counter() - begun
            if elapsed >= 300:
                try:
                    point = guard.read('between_updates_wall_cap', arm=arm, completed_updates=completed,
                                       elapsed_seconds=elapsed, wall_limit_seconds=300)
                except GuardStop as exc:
                    point = exc.trigger
                stop, trigger = 'wall_time_cap', point
                break
            record = balanced_update(model, tok, optimizer, group, guidance, arm, guard, i+1)
            record['arm'] = arm
            append_json(arm_root / 'TRAINING_LOG.jsonl', record)
            if record['completed']:
                completed += 1; completed_ids.extend(record['example_ids'])
                for case in group:
                    exposure[case['label']] += 1
            if 'stop' in record:
                stop, trigger = record['stop'], record['trigger']; break
            if completed % 8 == 0 or args.preflight_only:
                print(json.dumps({'arm': arm, 'completed_updates': completed, 'loss': record['loss']}), flush=True)
        training_seconds = time.perf_counter() - begun
        base_after = parameter_digest(model, False)
        if base_after != base_before:
            raise ValueError('Frozen base parameters changed')
        if not all(torch.isfinite(p).all().item() for p in params):
            raise ValueError('Nonfinite adapter cannot be published as a clean checkpoint')
        checkpoint = arm_root / 'checkpoint'
        save_adapter(model, checkpoint, base_pin=basepin)
        optimizer_path = arm_root / 'optimizer_state.pt'
        if optimizer_path.exists():
            raise FileExistsError(optimizer_path)
        torch.save({'optimizer': optimizer.state_dict(), 'completed_steps': completed,
                    'completed_example_ids': completed_ids, 'data_order': [[c['id'] for c in g] for g in order],
                    'seed': 73103, 'objective': arm}, optimizer_path)
        manifest = {'arm': arm, 'completed_updates': completed, 'planned_updates': planned,
                    'stop': stop, 'trigger': trigger, 'training_seconds': training_seconds,
                    'completed_class_exposure': exposure, 'completed_example_ids': completed_ids,
                    'inventory': inventory, 'base_pin': basepin, 'frozen_base_before': base_before,
                    'frozen_base_after': base_after, 'initial_adapter_digest': init,
                    'final_adapter_digest': parameter_digest(model, True),
                    'checkpoint': str(checkpoint), 'optimizer': str(optimizer_path),
                    'checkpoint_files_sha256': {f.name: sha(f) for f in checkpoint.iterdir()},
                    'initial_files_sha256': {f.name: sha(f) for f in initial.iterdir()},
                    'optimizer_sha256': sha(optimizer_path), 'preflight_not_warmstart': True}
        dump_new(arm_root / 'TRAINING_MANIFEST.json', manifest); manifests[arm] = manifest
        optimizer.zero_grad(set_to_none=True)
        del optimizer, params, model; gc.collect()
        # A clean partial stop closes the experiment without starting another attempt/arm/test.
        if completed != planned or trigger is not None:
            dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'bounded_partial_stop',
                        'manifests': manifests, 'calls': 0, 'primary_forwarded': False,
                        'no_automatic_retry': True})
            return
    if args.preflight_only:
        dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'preflight_only', 'calls': 0,
                    'primary_forwarded': False, 'manifests': manifests, 'not_warmstart': True})
        return
    if manifests[OBJECTIVES[0]]['completed_example_ids'] != manifests[OBJECTIVES[1]]['completed_example_ids']:
        raise ValueError('Arm completed exposure/order differs')
    # Every baseline/trained forward, including dev, is deferred until both checkpoints exist.
    dump_new(args.study / 'TRAINING_COMPLETE.json', {'arms': list(manifests),
                'both_checkpoints_saved': True, 'primary_forwarded': False,
                'initial_adapter_digest_equal': True, 'base_digest_equal': True,
                'exposure_and_order_equal': True})
    sets = [('dev', dev), ('primary', primary)]
    if challenge:
        sets.append(('challenge', challenge))
    if args.include_regression:
        sets.append(('regression', regression))
    calls = 0
    try:
        for arm in ('original',) + OBJECTIVES:
            model, _ = fresh('eval_' + arm)
            if parameter_digest(model, False) != common_base or parameter_digest(model, True) != common_init:
                raise ValueError('Evaluation fresh initialization mismatch')
            if arm != 'original':
                load_adapter(model, Path(manifests[arm]['checkpoint']), base_pin=basepin)
                if parameter_digest(model, True) != manifests[arm]['final_adapter_digest']:
                    raise ValueError('Loaded checkpoint parameter digest mismatch')
            for subset, cases in sets:
                for case in cases:
                    row = generate(model, tok, case, guidance, arm, subset, args.state_root, guard)
                    append_json(args.study / 'RAW_OUTPUTS.jsonl', row); calls += 1
                    if 'resource_stop' in row:
                        raise GuardStop(row['resource_stop']['reason'], row['resource_stop']['trigger'])
                    print(json.dumps({'call': calls, 'arm': arm, 'subset': subset,
                                      'id': case['id'], 'text': row['text'], 'stop': row['stop']}), flush=True)
            del model; gc.collect()
    except GuardStop as exc:
        dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'evaluation_resource_stop',
                    'calls': calls, 'stop': exc.reason, 'trigger': exc.trigger,
                    'both_training_branches_saved_before_primary': True, 'no_automatic_retry': True})
        return
    for path, digest in preserved.items():
        if sha(path) != digest:
            raise ValueError('Prior pilot artifact changed')
    dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'complete', 'calls': calls,
                'expected_calls': 3 * sum(len(cases) for _, cases in sets),
                'subsets': {name: len(cases) for name, cases in sets},
                'both_training_branches_saved_before_primary': True,
                'evaluation_keys_never_parsed': True, 'training_labels_supervised': True,
                'baseline': 'fresh pinned base plus identical zero-product adapter initialization',
                'seed': 73103, 'generation': {'greedy': True, 'max_new_tokens': 8},
                'full_caches': str(args.state_root), 'prior_preservation_verified': True,
                'default_not_promoted': True})


if __name__ == '__main__':
    main()
