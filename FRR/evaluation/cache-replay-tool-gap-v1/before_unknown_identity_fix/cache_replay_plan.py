"""Plan full-attention same-model prefix reuse. No tensor or semantic verification.

CLI: python tools/cache_replay_plan.py request.json
Input: {cached:{token_ids,cache_token_count,prefix_sha256,execution_identity},
        requested:{token_ids,execution_identity}}
Unknown identity forces rebuild; invalid structure raises ValueError.
"""
import hashlib
import json
import sys

IDENTITY_FIELDS = ('model_revision', 'tokenizer_revision', 'position_config',
                   'attention_policy', 'kv_layout', 'dtype', 'adapter_identity',
                   'multimodal_identity', 'namespace')

def token_digest(ids):
    return hashlib.sha256(json.dumps(ids, separators=(',', ':')).encode()).hexdigest()

def _tokens(value):
    if not isinstance(value, list) or any(type(x) is not int or x < 0 for x in value):
        raise ValueError('token_ids must be a list of nonnegative integers')
    return value

def plan(cached, requested):
    if not isinstance(cached, dict) or not isinstance(requested, dict):
        raise ValueError('cached and requested must be objects')
    old = _tokens(cached.get('token_ids'))
    new = _tokens(requested.get('token_ids'))
    count = cached.get('cache_token_count')
    if type(count) is not int or not 0 <= count <= len(old):
        raise ValueError('cache_token_count must be an integer within token history')
    reasons = []
    a, b = cached.get('execution_identity'), requested.get('execution_identity')
    if not isinstance(a, dict) or not isinstance(b, dict):
        reasons.append('missing_execution_identity')
    else:
        for field in IDENTITY_FIELDS:
            if not isinstance(a.get(field), str) or not a[field] or not isinstance(b.get(field), str) or not b[field]:
                reasons.append('unknown_identity:' + field)
        if a != b:
            reasons.append('execution_identity_changed')
        if a.get('attention_policy') != 'causal_full' or b.get('attention_policy') != 'causal_full':
            reasons.append('unsupported_attention_policy')
    if cached.get('prefix_sha256') != token_digest(old[:count]):
        reasons.append('cached_prefix_digest_mismatch')
    keep = 0
    if not reasons:
        for x, y in zip(old[:count], new):
            if x != y:
                break
            keep += 1
    return {'reuse_prefix_tokens': keep, 'discard_cached_tokens': count - keep,
            'replay_token_ids': new[keep:], 'replay_tokens': len(new) - keep,
            'reasons': reasons, 'requires_backend_truncate': count > keep,
            'scope': 'Caller-declared metadata consistency only; no tensor authentication, semantics or backend execution.'}

if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as f:
            request = json.load(f)
        print(json.dumps(plan(request['cached'], request['requested']), sort_keys=True))
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        sys.exit(2)
