"""Bounded comparison helpers. Importing this module never loads a model."""
from pathlib import Path
import hashlib
import json
import math
import resource
import time

import torch
import torch.nn.functional as F

LABELS = ('YES', 'NO', 'WITHHOLD')
OBJECTIVES = ('sequence_mean', 'decision_balanced')


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def dump_new(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def append_json(path, value):
    with Path(path).open('a') as stream:
        stream.write(json.dumps(value, sort_keys=True, allow_nan=False) + '\n')
        stream.flush()


def parameter_digest(model, trainable):
    h = hashlib.sha256()
    for name, value in model.named_parameters():
        if value.requires_grad == trainable:
            h.update(name.encode() + b'\0')
            h.update(str(value.dtype).encode() + b'\0')
            h.update(json.dumps(list(value.shape)).encode() + b'\0')
            h.update(value.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def messages(case, guidance):
    # Only source is read from evaluation records.
    return [{'role': 'user', 'content': guidance['instruction'] + '\n\nRecord:\n' +
             case['source'] + '\n\n' + guidance['question']}]


def encode(tok, case, guidance, training=False):
    ids = tok.apply_chat_template(messages(case, guidance), tokenize=True,
                                  add_generation_prompt=True)
    if not training:
        return ids
    target = tok.encode(case['label'], add_special_tokens=False) + [tok.eos_token_id]
    if len(target) < 2 or tok.eos_token_id is None:
        raise ValueError('Require label tokens and explicit EOS remainder')
    return ids + target, [-100] * len(ids) + target


def objective(logits, labels, kind):
    """One sequence, causally shifted, with prompt masked and terminal EOS retained."""
    if kind not in OBJECTIVES:
        raise ValueError(kind)
    if logits.ndim != 3 or logits.shape[0] != 1 or labels.shape != logits.shape[:2]:
        raise ValueError('microbatch must be exactly one matching sequence')
    targets = labels[:, 1:].reshape(-1)
    valid = targets != -100
    positions = torch.nonzero(valid, as_tuple=False).flatten()
    if len(positions) < 2 or not torch.equal(positions, torch.arange(
            int(positions[0]), len(targets), device=positions.device)):
        raise ValueError('Need contiguous label suffix including EOS (>=2 tokens)')
    ce = F.cross_entropy(logits[:, :-1, :].reshape(-1, logits.shape[-1])[valid],
                         targets[valid], reduction='none')
    first, suffix, mean = ce[0], ce[1:].mean(), ce.mean()
    loss = mean if kind == 'sequence_mean' else .5 * first + .5 * suffix
    return loss, {'first_token_ce': float(first.detach()),
                  'suffix_mean_ce': float(suffix.detach()),
                  'sequence_mean_ce': float(mean.detach()),
                  'decision_balanced_ce': float((.5 * first + .5 * suffix).detach()),
                  'target_tokens_including_eos': len(ce)}


def memory_point(stage, working_limit):
    stat = dict(line.split() for line in Path('/sys/fs/cgroup/memory.stat').read_text().splitlines())
    current = int(Path('/sys/fs/cgroup/memory.current').read_text())
    status = dict(line.split(':', 1) for line in Path('/proc/self/status').read_text().splitlines() if ':' in line)
    working = current - int(stat.get('inactive_file', 0))
    return {'phase': stage, 'cgroup_current': current,
            'inactive_file': int(stat.get('inactive_file', 0)),
            'working_estimate': working,
            'process_rss': int(status['VmRSS'].split()[0]) * 1024,
            'process_peak_rss': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024,
            'working_limit': working_limit}


class GuardStop(Exception):
    def __init__(self, reason, trigger):
        super().__init__(reason)
        self.reason, self.trigger = reason, trigger


class Guard:
    def __init__(self, working_limit, log_path):
        self.working_limit, self.log_path = working_limit, log_path

    def read(self, stage, **context):
        point = memory_point(stage, self.working_limit)
        point.update(context)
        # Record before checking, so the exact first offending reading survives.
        append_json(self.log_path, point)
        if point['working_estimate'] >= self.working_limit:
            raise GuardStop('memory_headroom', point)
        return point


def balanced_update(model, tok, optimizer, examples, guidance, kind, guard, update):
    """Three backwards, one optimizer update. Interrupted gradients are discarded."""
    if len(examples) != 3 or {c['label'] for c in examples} != set(LABELS):
        raise ValueError('Effective update requires one example per class')
    result = {'completed': False, 'optimizer_applied': False, 'effective_update': update,
              'example_ids': [c['id'] for c in examples], 'micro_losses': []}
    started = time.perf_counter()
    try:
        guard.read('before_update', arm=kind, update=update)
        optimizer.zero_grad(set_to_none=True)
        model.train()
        for micro, case in enumerate(examples):
            guard.read('before_forward', arm=kind, update=update, micro=micro, record_id=case['id'])
            ids, labels = encode(tok, case, guidance, True)
            if len(ids) > 256:
                raise ValueError('No truncation permitted')
            x, y = torch.tensor([ids]), torch.tensor([labels])
            output = model(input_ids=x, attention_mask=torch.ones_like(x), use_cache=False)
            guard.read('after_forward', arm=kind, update=update, micro=micro, record_id=case['id'])
            loss, components = objective(output.logits, y, kind)
            if not torch.isfinite(loss):
                raise GuardStop('nonfinite_loss', {'phase': 'loss', 'update': update, 'micro': micro})
            components.update({'id': case['id'], 'label': case['label'], 'objective_loss': float(loss.detach())})
            result['micro_losses'].append(components)
            guard.read('before_backward', arm=kind, update=update, micro=micro, record_id=case['id'])
            (loss / 3).backward()
            guard.read('after_backward', arm=kind, update=update, micro=micro, record_id=case['id'])
            del output, loss, x, y
        params = [p for p in model.parameters() if p.requires_grad]
        norm = torch.nn.utils.clip_grad_norm_(params, 1., foreach=False)
        if not torch.isfinite(norm):
            raise GuardStop('nonfinite_gradient', {'phase': 'clip_grad', 'update': update})
        guard.read('before_optimizer', arm=kind, update=update)
        optimizer.step()
        result['optimizer_applied'] = True
        # An after-optimizer resource stop still counts this completed update.
        result['completed'] = True
        result['gradient_norm'] = float(norm)
        result['loss'] = sum(v['objective_loss'] for v in result['micro_losses']) / 3
        guard.read('after_optimizer', arm=kind, update=update)
        if not all(torch.isfinite(p).all().item() for p in params):
            result['completed'] = False
            raise GuardStop('nonfinite_adapter', {'phase': 'after_optimizer_finite', 'update': update})
    except GuardStop as exc:
        result.update({'stop': exc.reason, 'trigger': exc.trigger})
    finally:
        optimizer.zero_grad(set_to_none=True)
        result['seconds'] = time.perf_counter() - started
    return result


def make_order(train, seed):
    import random
    if len(train) != 72 or len({c['id'] for c in train}) != 72:
        raise ValueError('Need 72 unique frozen training rows')
    groups = [train[i:i+3] for i in range(0, 72, 3)]
    if not all({c['label'] for c in group} == set(LABELS) for group in groups):
        raise ValueError('Each frozen triple must contain all three labels')
    rng = random.Random(seed)
    indices = []
    for _ in range(2):
        epoch = list(range(24)); rng.shuffle(epoch); indices.extend(epoch)
    order = []
    for i, group_id in enumerate(indices):
        group = groups[group_id]
        order.append(group[i % 3:] + group[:i % 3])
    return order


def generate(model, tok, case, guidance, arm, subset, state_root, guard):
    from safetensors.torch import save_file
    guard.read('before_eval', arm=arm, subset=subset, record_id=case['id'])
    model.eval()
    msg = messages(case, guidance)
    ids = torch.tensor([encode(tok, case, guidance)])
    started = time.perf_counter()
    with torch.inference_mode():
        output = model(input_ids=ids, attention_mask=torch.ones_like(ids), use_cache=True)
        cache, logits = output.past_key_values, output.logits[:, -1, :]
        new, stop = [], 'token_limit'
        for i in range(8):
            token = int(logits.argmax(-1).item()); new.append(token)
            if token == tok.eos_token_id:
                stop = 'eos'; break
            if i == 7:
                break
            output = model(input_ids=torch.tensor([[token]]), past_key_values=cache,
                           attention_mask=torch.ones((1, cache.get_seq_length()+1), dtype=torch.long),
                           use_cache=True)
            cache, logits = output.past_key_values, output.logits[:, -1, :]
    elapsed = time.perf_counter() - started
    resource_stop = None
    try:
        guard.read('after_eval_forward', arm=arm, subset=subset, record_id=case['id'])
    except GuardStop as exc:
        # Preserve the completed call and its full cache before cleanly stopping.
        resource_stop = {'reason': exc.reason, 'trigger': exc.trigger}
    run_id = case['id'] + '__' + arm + '__' + subset
    path = state_root / (run_id + '.safetensors')
    if path.exists():
        raise FileExistsError(path)
    tensors = {f'layer{j}_{kind}': v.detach().cpu().contiguous()
               for j, pair in enumerate(cache.to_legacy_cache())
               for kind, v in zip(('k', 'v'), pair)}
    serialization_start = time.perf_counter(); save_file(tensors, str(path))
    allids, count = ids[0].tolist()+new, int(cache.get_seq_length())
    row = {'run_id': run_id, 'record_id': case['id'], 'arm': arm, 'subset': subset,
           'family': 'decision_loss_compare', 'facet': 'state_label', 'cycle': 'DLC1',
           'structure_family': case['structure_family'], 'messages': msg,
           'rendered_prompt': tok.apply_chat_template(msg, tokenize=False, add_generation_prompt=True),
           'input_token_ids': ids[0].tolist(), 'generated_token_ids': new,
           'text': tok.decode(new, skip_special_tokens=True), 'stop': stop,
           'input_tokens': int(ids.shape[1]), 'output_tokens': len(new),
           'inference_seconds_excluding_serialization': elapsed,
           'serialization_seconds': time.perf_counter()-serialization_start,
           'cache_artifact': {'local_path': str(path), 'sha256': sha(path),
                              'bytes': path.stat().st_size, 'cache_token_count': count,
                              'all_sequence_token_ids': allids,
                              'cached_token_prefix_sha256': hashlib.sha256(json.dumps(
                                  allids[:count], separators=(',', ':')).encode()).hexdigest()}}
    if resource_stop is not None:
        row['resource_stop'] = resource_stop
    return row
