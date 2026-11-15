"""External descriptive readout; never included in the inhabitant's input."""
from pathlib import Path
import json, hashlib

H = Path(__file__).resolve().parent

def read(p):
    return json.loads(p.read_text())

def describe():
    run = H / 'run'
    result = read(run / 'RESULTS.json')
    assert result['status'] == 'pass' and result['actual_model_calls'] == 6
    arms = {}
    for arm in ('prose', 'json'):
        rows = [read(run / 'records' / f'{arm}_t{n}.json') for n in range(1, 4)]
        raw = [read(run / 'raw' / f'{arm}_t{n}.json') for n in range(1, 4)]
        assert all(r['feedback_for_next_input'] == '{"runtime_feedback":null}' for r in rows)
        arms[arm] = {
            'input_tokens': [r['input_tokens'] for r in rows],
            'output_tokens': [r['output_tokens'] for r in rows],
            'unique_input_token_sequences': len({tuple(r['input_token_ids']) for r in raw}),
            'unique_output_token_sequences': len({tuple(r['generated_token_ids']) for r in raw}),
            'output_sha256': [hashlib.sha256(r['text'].encode()).hexdigest() for r in raw],
            'complete_cells': sum(r['complete_cells'] for r in rows),
            'incomplete_fences': sum(r['incomplete_fences'] for r in rows),
            'model_initiated_actions': sum(len(r['model_initiated_actions']) for r in rows),
            'automatic_note_operations': sum(len(r['automatic_note_operations']) for r in rows),
            'stop_reasons': [r['stop'] for r in rows],
            'note_byte_growth': sum(len(r['text'].encode()) for r in raw),
            'action_error_response_opportunity': 'not elicited',
            'artifact_reuse_opportunity': 'not elicited',
        }
    return {'status': 'pass', 'arms': arms, 'actual_model_calls': 6,
            'cross_arm_first_outputs_equal': read(run/'raw/prose_t1.json')['generated_token_ids'] == read(run/'raw/json_t1.json')['generated_token_ids'],
            'interpretation_scope': 'two finite path-dependent greedy trajectories; changing inputs, possibly repeated outputs; not independent replicates or a permanent fixed-point proof',
            'main_entry': 1630, 'main_unchanged': result['main_unchanged'],
            'weights_unchanged': result['weights_unchanged'], 'training_updates': 0}

if __name__ == '__main__':
    out = describe()
    with (H/'READOUT.json').open('x') as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(json.dumps(out))
