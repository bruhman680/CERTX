"""Post-hoc bounded checks of a Claude relay; no model generation."""
from pathlib import Path
import hashlib
import json
import statistics
import zlib

HERE = Path(__file__).resolve().parent
PRIMARY = HERE.parent / 'source-access-three-cycle-v1/cycle3/environment/events'


def compressed(raw, dictionary=None):
    if dictionary is None:
        return len(zlib.compress(raw, 9))
    obj = zlib.compressobj(9, zlib.DEFLATED, 15, 9, zlib.Z_DEFAULT_STRATEGY,
                           dictionary[-32768:])
    return len(obj.compress(raw) + obj.flush())


def compression_check():
    events = sorted((json.loads(p.read_text()) for p in PRIMARY.glob('*.json')),
                    key=lambda row: row['step'])
    events = [row for row in events if 50 <= row['step'] < 500]
    assert [row['step'] for row in events] == list(range(50, 500))
    history, rows = b'', []
    for offset in range(0, len(events), 50):
        block = events[offset:offset + 50]
        raw = '\n<<>>\n'.join(row['text'] for row in block).encode()
        plain = compressed(raw)
        conditional = compressed(raw, history) if history else plain
        rows.append({'start': block[0]['step'], 'end': block[-1]['step'],
                     'ratio': conditional / plain,
                     'distinct': len({row['text'] for row in block}),
                     'raw_bytes': len(raw), 'unconditional_bytes': plain})
        history += raw + b'\n'
    early = statistics.mean(row['ratio'] for row in rows[:2])
    late = statistics.mean(row['ratio'] for row in rows[-2:])
    raw = bytes(range(128, 256))
    no_help = compressed(raw, b'A' * 512) / compressed(raw)
    return {'rows': rows, 'early_mean': early, 'late_mean': late,
            'early_over_late': early / late,
            'exclude_history_free_first_block_over_late': rows[1]['ratio'] / late,
            'nonhelpful_dictionary_counterexample': {
                'unconditional_bytes': compressed(raw),
                'conditional_bytes': compressed(raw, b'A' * 512), 'ratio': no_help,
                'above_one': no_help > 1},
            'interpretation': 'Ratios reproduce a descriptive compressor statistic. Ratios above1 are possible; no curiosity or learnability test.'}


def affine_count(maximum, length):
    # Independent packed-byte representation; values are all below256.
    words = set()
    for modulus in range(2, maximum + 1):
        for multiplier in range(modulus):
            for intercept in range(modulus):
                for initial in range(modulus):
                    values, value = [initial], initial
                    for _ in range(length - 1):
                        value = (multiplier * value + intercept) % modulus
                        values.append(value)
                    words.add(bytes(values))
    return len(words)


def affine_check():
    rows = []
    for maximum, alphabet in ((30, 100), (60, 100), (10, 10)):
        # At length2, m=M,a=0,b=x1 realizes every pair in [0,M)^2.
        # No smaller modulus produces a value outside that square.
        cells = [{'length': 2, 'distinct': maximum ** 2,
                  'probability': maximum ** 2 / alphabet ** 2}]
        length = 3
        while cells[-1]['probability'] >= .05:
            count = affine_count(maximum, length)
            cells.append({'length': length, 'distinct': count,
                          'probability': count / alphabet ** length})
            length += 1
            assert length <= 7
        rows.append({'maximum_modulus': maximum, 'alphabet': alphabet,
                     'first_length_below_point05': cells[-1]['length'], 'cells': cells})
    return rows


def tokenizer_check():
    from transformers import AutoTokenizer
    root = Path('/workspace/cache_backend_models/smollm2-135m')
    paths = [root / 'tokenizer.json', root / 'tokenizer_config.json']
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    tokenizer = AutoTokenizer.from_pretrained(str(root), local_files_only=True)
    examples = ['7', '99', '100', '123456789', '123,456,789',
                '1 2 4 8 16', '-12', '+003', '(+ 12 34)']
    rows = []
    for text in examples:
        ids = tokenizer.encode(text, add_special_tokens=False)
        rows.append({'text': text, 'ids': ids,
                     'tokens': tokenizer.convert_ids_to_tokens(ids),
                     'pieces': [tokenizer.decode([i]) for i in ids],
                     'decoded': tokenizer.decode(ids)})
    after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    assert before == after
    return {'rows': rows, 'files_sha256': after, 'files_unchanged': True,
            'pre_tokenizer': json.loads((root / 'tokenizer.json').read_text())['pre_tokenizer'],
            'local_files_only': True, 'model_weights_loaded': False,
            'interpretation': 'Token splits are observed, not arithmetic or exploration competence.'}


if __name__ == '__main__':
    out = {'schema': 'claude-seed-recheck-v1', 'post_hoc_not_blind': True,
           'model_generations': 0,
           'compression': compression_check(), 'affine_thresholds': affine_check(),
           'tokenizer': tokenizer_check()}
    (HERE / 'RECHECK.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'compression_early_late': out['compression']['early_over_late'],
                      'ratio_above_one_exists': out['compression']['nonhelpful_dictionary_counterexample']['above_one'],
                      'affine_thresholds': [x['first_length_below_point05'] for x in out['affine_thresholds']],
                      'tokenizer_pieces_123456789': out['tokenizer']['rows'][3]['pieces']}))
