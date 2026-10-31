"""One fresh curriculum candidate; reuse the fixed prior mean control checkpoint.

No models load on import. No evaluation keys are parsed. Every output root is new.
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
import torch
from runtime import (Guard, GuardStop, LABELS, append_json, balanced_update, dump_new,
                     encode, generate, make_order, parameter_digest, sha)


def validate_freeze(root):
    freeze_path = root / 'FREEZE.json'
    freeze = json.loads(freeze_path.read_text())
    hashes = {}
    for name, expected in freeze['sha256'].items():
        path = (root / name).resolve()
        actual = sha(path)
        if actual != expected:
            raise ValueError(f'Frozen input changed: {path}')
        hashes[str(path)] = actual
    hashes[str(freeze_path.resolve())] = sha(freeze_path)
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--state-root', type=Path, default=Path('/workspace/smollm_curriculum_states_v1'))
    parser.add_argument('--data-dir', type=Path, required=True)
    parser.add_argument('--priorbase', type=Path, default=Path('/workspace/frr/evaluation/lora-state-pilot-v1'))
    parser.add_argument('--control', type=Path, default=Path('/workspace/frr/evaluation/decision-loss-comparison-v1/run/sequence_mean/checkpoint'))
    parser.add_argument('--base', type=Path, default=Path('/workspace/cache_backend_models/smollm2-135m'))
    parser.add_argument('--working-limit-bytes', type=int, default=int(.6 * 8589934592))
    parser.add_argument('--preflight-only', action='store_true')
    parser.add_argument('--tokenize-only', action='store_true', help='Static length checks only; no model load')
    parser.add_argument('--validate-only', action='store_true', help='Hash/schema/control checks only; no model/tokenizer load')
    args = parser.parse_args()
    args.study, args.state_root = args.study.resolve(), args.state_root.resolve()
    args.data_dir, args.control, args.priorbase = args.data_dir.resolve(), args.control.resolve(), args.priorbase.resolve()
    if args.working_limit_bytes <= 0:
        parser.error('working limit must be positive')
    if args.study.exists() or args.state_root.exists():
        raise FileExistsError('Study and cache roots must be new; no overwrite or automatic retry')
    if args.study == args.state_root or args.study in args.state_root.parents or args.state_root in args.study.parents:
        raise ValueError('Use separate nonnested output roots')
    # Accept a fixture package root or its DATA directory. DATA_CHECKS binds all
    # authored files, including gold keys by integrity hash only.
    fixture_data = args.data_dir / 'DATA' if (args.data_dir / 'DATA').is_dir() else args.data_dir
    checks_path = args.data_dir / 'DATA_CHECKS.json'
    if not checks_path.exists():
        checks_path = args.data_dir.parent / 'DATA_CHECKS.json'
    checks = json.loads(checks_path.read_text())
    if checks.get('all_passed') is not True:
        raise ValueError('Fixture author checks did not pass')
    hashes = {str(checks_path): sha(checks_path)}
    for name, expected in checks['sha256'].items():
        path = (fixture_data / name).resolve()
        if fixture_data.resolve() not in path.parents:
            raise ValueError('Fixture hash path escapes DATA directory')
        if sha(path) != expected:
            raise ValueError(f'Fixture changed: {path}')
        hashes[str(path)] = expected
    hashes.update(validate_freeze(args.priorbase))
    for name in ('TRAIN.json', 'PRIMARY_CASES.json', 'DEV_CASES.json', 'GUIDANCE.json'):
        if str((fixture_data / name).resolve()) not in hashes:
            raise ValueError(f'Fixture hash manifest must bind {name}')
    train = json.loads((fixture_data / 'TRAIN.json').read_text())
    dev = json.loads((fixture_data / 'DEV_CASES.json').read_text())
    primary = json.loads((fixture_data / 'PRIMARY_CASES.json').read_text())
    cases = dev + primary
    guidance = json.loads((args.priorbase / 'GUIDANCE.json').read_text())
    if sha(fixture_data / 'GUIDANCE.json') != sha(args.priorbase / 'GUIDANCE.json'):
        raise ValueError('Guidance must be verbatim prior guidance')
    if len(dev) != 12 or len(primary) != 72 or len({c['id'] for c in cases}) != 84:
        raise ValueError('Need exactly12 dev and72 primary source rows, unique IDs')
    if any(c['split'] != 'dev' for c in dev) or any(c['split'] != 'primary' for c in primary):
        raise ValueError('Fixture source split mismatch')
    for case in cases:
        if set(case) != {'id', 'split', 'structure_family', 'source'}:
            raise ValueError('Evaluation rows must have only four source fields')
    if len({c['source'] for c in train}) != 144:
        raise ValueError('Candidate must use144 unique source prompts')
    order = make_order(train, 73103, expected_records=144, epochs=1)
    if len(order) != 48:
        raise ValueError('Expected48 updates')
    control_manifest_path = args.control.parent / 'TRAINING_MANIFEST.json'
    control_manifest = json.loads(control_manifest_path.read_text())
    if (control_manifest['arm'] != 'sequence_mean' or control_manifest['completed_updates'] != 48 or
            control_manifest['planned_updates'] != 48 or control_manifest['trigger'] is not None or
            control_manifest['completed_class_exposure'] != dict.fromkeys(LABELS, 48)):
        raise ValueError('Control must be the complete fixed48-step mean branch')
    control_hashes = {str(control_manifest_path): sha(control_manifest_path)}
    for name, expected in control_manifest['checkpoint_files_sha256'].items():
        path = args.control / name
        if sha(path) != expected:
            raise ValueError('Reused control checkpoint hash mismatch')
        control_hashes[str(path)] = expected
    control_initial = args.control.parent / 'initial_adapter'
    for name, expected in control_manifest['initial_files_sha256'].items():
        path = control_initial / name
        if sha(path) != expected:
            raise ValueError('Control initialization reference changed')
        control_hashes[str(path)] = expected
    preserve = {str(args.priorbase / 'RAW_OUTPUTS.jsonl'): sha(args.priorbase / 'RAW_OUTPUTS.jsonl'), **control_hashes}
    args.study.mkdir(parents=True); args.state_root.mkdir(parents=True)
    dump_new(args.study / 'INPUTS.json', {'source_hashes': hashes, 'control_artifacts': control_hashes,
            'control_manifest_path': str(control_manifest_path), 'control_manifest_sha256': sha(control_manifest_path),
            'prior_preserved': preserve, 'control_retrained': False,
            'seed': 73103, 'lr': .001, 'rank': 4, 'alpha': 8, 'dropout': 0,
            'steps': 48, 'effective_batch': 3, 'microbatch': 1, 'gradient_clip': 1, 'weight_decay': .01,
            'objective': 'sequence_mean', 'candidate_unique_records': 144, 'candidate_epochs': 1,
            'control_unique_records': 72, 'control_epochs': 2,
            'interpretation': 'curriculum package comparison; support/formats/unique records/exposures differ; not a pure position causal test',
            'working_limit_bytes': args.working_limit_bytes, 'wall_seconds_per_arm': 300,
            'max_training_tokens': 256, 'preflight_only': args.preflight_only, 'data_order': [[c['id'] for c in g] for g in order]})
    if args.validate_only:
        dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'inputs_validated_only',
                    'calls': 0, 'primary_forwarded': False, 'model_or_tokenizer_loaded': False})
        return
    sys.path.insert(0, str(args.priorbase))
    from lora_cpu import inject_lora, load_adapter, save_adapter
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from safetensors.torch import load_file
    torch.set_num_threads(2)
    tok = AutoTokenizer.from_pretrained(args.base, local_files_only=True, trust_remote_code=False)
    train_lengths = {c['id']: len(encode(tok, c, guidance, True)[0]) for c in train}
    eval_lengths = {c['id']: len(encode(tok, c, guidance)) for c in cases}
    if max(train_lengths.values()) > 256:
        raise ValueError('Training sequence exceeds declared256-token guard; never truncate')
    longest_group = max(order, key=lambda g: max(train_lengths[c['id']] for c in g))
    tokenization = {'training_lengths': train_lengths, 'evaluation_lengths': eval_lengths,
                    'max_training_tokens': max(train_lengths.values()), 'max_eval_input_tokens': max(eval_lengths.values()),
                    'declared_training_token_guard': 256,
                    'preflight_selected_ids': [c['id'] for c in longest_group],
                    'preflight_selection': 'balanced triple containing maximum-length training sequence',
                    'main_order_unchanged': True, 'preflight_not_warmstart': True}
    dump_new(args.study / 'TOKENIZATION.json', tokenization)
    if args.tokenize_only:
        dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'tokenization_only', 'calls': 0,
                    'primary_forwarded': False, 'model_loaded': False, 'tokenization': tokenization})
        return
    basepin = {'model_id': 'HuggingFaceTB/SmolLM2-135M-Instruct',
               'revision': '12fd25f77366fa6b3b4b768ec3050bf629380bac',
               'weights_sha256': sha(args.base / 'model.safetensors')}
    if basepin != control_manifest['base_pin']:
        raise ValueError('Control pinned base differs')
    guard = Guard(args.working_limit_bytes, args.study / 'RESOURCE_LOG.jsonl')

    def fresh(context):
        guard.read('before_model_load', context=context)
        torch.manual_seed(73103)
        model = AutoModelForCausalLM.from_pretrained(args.base, local_files_only=True,
                trust_remote_code=False, use_safetensors=True, torch_dtype=torch.float32,
                attn_implementation='eager')
        inventory = inject_lora(model, rank=4, alpha=8, dropout=0.)
        if inventory['trainable_parameter_count'] != 230400:
            raise ValueError('Unexpected adapter parameter count')
        guard.read('after_model_load', context=context)
        return model, inventory

    arm_root = args.study / 'candidate'; arm_root.mkdir()
    try:
        model, inventory = fresh('train_candidate')
    except GuardStop as exc:
        dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'model_load_resource_stop', 'calls': 0,
                    'stop': exc.reason, 'trigger': exc.trigger, 'primary_forwarded': False, 'no_automatic_retry': True})
        return
    base_before, init = parameter_digest(model, False), parameter_digest(model, True)
    if base_before != control_manifest['frozen_base_before'] or base_before != control_manifest['frozen_base_after']:
        raise ValueError('Candidate/control frozen base differs')
    if init != control_manifest['initial_adapter_digest']:
        raise ValueError('Candidate initial A/B digest differs from control reference')
    initial = arm_root / 'initial_adapter'
    save_adapter(model, initial, base_pin=basepin)
    init_state = load_file(str(initial / 'adapter.safetensors'))
    if not all(torch.count_nonzero(v) == 0 for k, v in init_state.items() if k.endswith('lora_B')):
        raise ValueError('Initial adapter B must be zero')
    reference_state = load_file(str(control_initial / 'adapter.safetensors'))
    if set(init_state) != set(reference_state) or any(not torch.equal(v, reference_state[k]) for k, v in init_state.items()):
        raise ValueError('Candidate initialization tensors differ from saved control initialization')
    del init_state, reference_state
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(params, lr=.001, weight_decay=.01, foreach=False)
    completed, exposure, completed_ids = 0, dict.fromkeys(LABELS, 0), []
    planned = 1 if args.preflight_only else 48
    stop, trigger = ('fixed_1_preflight_update' if args.preflight_only else 'fixed_48_updates'), None
    begun = time.perf_counter()
    training_groups = [longest_group] if args.preflight_only else order
    for i, group in enumerate(training_groups):
        elapsed = time.perf_counter() - begun
        if elapsed >= 300:
            try:
                point = guard.read('between_updates_wall_cap', arm='candidate', completed_updates=completed,
                                   elapsed_seconds=elapsed, wall_limit_seconds=300)
            except GuardStop as exc:
                point = exc.trigger
            stop, trigger = 'wall_time_cap', point; break
        record = balanced_update(model, tok, optimizer, group, guidance, 'sequence_mean', guard, i+1, resource_arm='candidate')
        record['arm'] = 'candidate'
        append_json(arm_root / 'TRAINING_LOG.jsonl', record)
        if record['completed']:
            completed += 1; completed_ids.extend(record['example_ids'])
            for case in group:
                exposure[case['label']] += 1
        if 'stop' in record:
            stop, trigger = record['stop'], record['trigger']; break
        if completed % 8 == 0 or args.preflight_only:
            print(json.dumps({'arm': 'candidate', 'completed_updates': completed, 'loss': record['loss']}), flush=True)
    training_seconds = time.perf_counter() - begun
    base_after = parameter_digest(model, False)
    if base_after != base_before:
        raise ValueError('Frozen base changed')
    if not all(torch.isfinite(p).all().item() for p in params):
        raise ValueError('Nonfinite adapter is not a clean checkpoint')
    checkpoint = arm_root / 'checkpoint'
    save_adapter(model, checkpoint, base_pin=basepin)
    optimizer_path = arm_root / 'optimizer_state.pt'
    torch.save({'optimizer': optimizer.state_dict(), 'completed_steps': completed,
                'completed_example_ids': completed_ids, 'data_order': [[c['id'] for c in g] for g in order],
                'seed': 73103, 'objective': 'sequence_mean'}, optimizer_path)
    manifest = {'arm': 'candidate', 'completed_updates': completed, 'planned_updates': planned,
                'stop': stop, 'trigger': trigger, 'training_seconds': training_seconds,
                'completed_class_exposure': exposure, 'completed_example_ids': completed_ids,
                'inventory': inventory, 'base_pin': basepin, 'frozen_base_before': base_before,
                'frozen_base_after': base_after, 'initial_adapter_digest': init,
                'initialization_equal_to_control_reference': True, 'tokenization': tokenization,
                'preflight_order_differs_from_main': args.preflight_only,
                'control_manifest_path': str(control_manifest_path), 'control_manifest_sha256': sha(control_manifest_path),
                'control_checkpoint': str(args.control), 'control_checkpoint_files_sha256': control_manifest['checkpoint_files_sha256'],
                'final_adapter_digest': parameter_digest(model, True), 'checkpoint': str(checkpoint),
                'checkpoint_files_sha256': {f.name: sha(f) for f in checkpoint.iterdir()},
                'initial_files_sha256': {f.name: sha(f) for f in initial.iterdir()},
                'optimizer': str(optimizer_path), 'optimizer_sha256': sha(optimizer_path), 'preflight_not_warmstart': True}
    dump_new(arm_root / 'TRAINING_MANIFEST.json', manifest)
    optimizer.zero_grad(set_to_none=True); del optimizer, params, model; gc.collect()
    if completed != planned or trigger is not None:
        dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'bounded_partial_stop', 'calls': 0,
                    'primary_forwarded': False, 'candidate': manifest, 'no_automatic_retry': True})
        return
    if args.preflight_only:
        dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'preflight_only', 'calls': 0,
                    'primary_forwarded': False, 'candidate': manifest, 'not_warmstart': True})
        return
    if exposure != control_manifest['completed_class_exposure'] or len(completed_ids) != 144 or len(set(completed_ids)) != 144:
        raise ValueError('Candidate/control exposure totals differ or candidate repeats a row')
    dump_new(args.study / 'TRAINING_COMPLETE.json', {'candidate_checkpoint_saved': True,
                'control_reused_without_training': True, 'primary_forwarded': False,
                'initial_adapter_equal': True, 'base_digest_equal': True, 'class_exposure_equal': True})
    calls = 0
    try:
        for arm in ('original', 'control', 'candidate'):
            model, _ = fresh('eval_' + arm)
            if parameter_digest(model, False) != base_before or parameter_digest(model, True) != init:
                raise ValueError('Evaluation fresh initialization mismatch')
            if arm != 'original':
                chosen = args.control if arm == 'control' else checkpoint
                expected_digest = control_manifest['final_adapter_digest'] if arm == 'control' else manifest['final_adapter_digest']
                load_adapter(model, chosen, base_pin=basepin)
                if parameter_digest(model, True) != expected_digest:
                    raise ValueError('Loaded adapter digest differs')
            for subset, chosen_cases in [('dev', dev), ('primary', primary)]:
                for case in chosen_cases:
                    row = generate(model, tok, case, guidance, arm, subset, args.state_root, guard)
                    append_json(args.study / 'RAW_OUTPUTS.jsonl', row); calls += 1
                    if 'resource_stop' in row:
                        raise GuardStop(row['resource_stop']['reason'], row['resource_stop']['trigger'])
                    print(json.dumps({'call': calls, 'arm': arm, 'subset': subset,
                                      'id': case['id'], 'text': row['text'], 'stop': row['stop']}), flush=True)
            del model; gc.collect()
    except GuardStop as exc:
        dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'evaluation_resource_stop', 'calls': calls,
                    'stop': exc.reason, 'trigger': exc.trigger, 'candidate_saved_before_primary': True,
                    'control_retrained': False, 'no_automatic_retry': True})
        return
    for path, digest in preserve.items():
        if sha(path) != digest:
            raise ValueError('Preserved original/control artifact changed')
    dump_new(args.study / 'RUN_MANIFEST.json', {'status': 'complete', 'calls': calls, 'expected_calls': 252,
                'subsets': {'dev': 12, 'primary': 72}, 'candidate_saved_before_primary': True,
                'control_retrained': False, 'control_manifest_path': str(control_manifest_path),
                'control_manifest_sha256': sha(control_manifest_path),
                'evaluation_keys_never_parsed': True, 'training_labels_supervised': True,
                'baseline': 'fresh pinned base plus identical zero-product adapters',
                'seed': 73103, 'generation': {'greedy': True, 'max_new_tokens': 8},
                'full_caches': str(args.state_root), 'prior_control_preservation_verified': True,
                'interpretation': 'curriculum package comparison, not pure position causal evidence',
                'default_not_promoted': True})


if __name__ == '__main__':
    main()
