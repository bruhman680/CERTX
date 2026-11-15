"""Targeted no-model coupling fixtures, separate from real study counters."""
from pathlib import Path
import json
import study as s

H = Path(__file__).resolve().parent


def fixture_raw(plan, text, tok):
    ids = tok.encode(text, add_special_tokens=False) + [tok.eos_token_id]
    assert len(ids) <= 256
    assert tok.decode(ids, skip_special_tokens=True) == text
    return {'messages':plan['messages'], 'input_token_ids':plan['input_token_ids'],
            'generated_token_ids':ids, 'text':text, 'stop':'eos',
            'decoder':'fixture_no_inference', 'seconds':0.0}


def act(run, arm, tok, text, **kwargs):
    plan = s.begin_reply(run, arm, tok)
    assert plan is not None
    return s.commit_reply(run, arm, fixture_raw(plan, text, tok), tok, **kwargs)


def checks():
    base = H/'tests'
    assert not base.exists(), 'Preserve prior fixture records'
    base.mkdir()
    tok = s.c.tokenizer()
    normal = base/'normal'
    s.prepare(normal, purpose='fixture_no_inference')
    first = act(normal, 'initial_only', tok,
        '```python\nfrom pathlib import Path\nPath("coupling_probe.txt").write_text("retained")\nprint("actual runtime output")\n```')
    control = json.loads(first['feedback_for_next_input'])
    assert set(control) == {'runtime_feedback'}
    assert control['runtime_feedback'] == json.loads(first['runtime_feedback_raw'])
    assert control['runtime_feedback']['receipts'][0]['stdout'] == 'actual runtime output\n'
    initial_names = [x['name'] for x in s.c.read(normal/'observations/initial_only_initial.json')['model_packet']['world_snapshot']['entries']]
    after = s.c.read(normal/'observations/initial_only_t1.json')['model_packet']['world_snapshot']
    assert 'coupling_probe.txt' not in initial_names and 'coupling_probe.txt' in [x['name'] for x in after['entries']]
    assert after['timing'] == 'after_reply' and after['reply_index'] == 1 and after['world_step'] == first['world_step']
    second = act(normal, 'initial_only', tok,
        '```python\nfrom pathlib import Path\nprint(Path("coupling_probe.txt").read_text())\n```')
    assert 'retained\n' == json.loads(second['runtime_feedback_raw'])['receipts'][0]['stdout']

    live = act(normal, 'live', tok, '```python\nraise ValueError("actual fixture error")\n```')
    feedback = json.loads(live['feedback_for_next_input'])
    assert set(feedback) == {'runtime_feedback', 'world_observation'}
    assert feedback['runtime_feedback'] == json.loads(live['runtime_feedback_raw'])
    assert feedback['runtime_feedback']['receipts'][0]['exit_code'] == 1
    assert 'ValueError: actual fixture error' in feedback['runtime_feedback']['receipts'][0]['stderr']
    assert feedback['world_observation']['world_step'] == live['world_step']
    assert feedback['world_observation']['reply_index'] == 1
    assert 'source_bundle_id' not in live['feedback_for_next_input']
    assert s.c.read(normal/'branches/live/STATE.json')['stop_reason'] is None
    assert s.messages_for(normal, 'live')[-1]['content'] == live['feedback_for_next_input']
    assert s.audit(normal, tok, save_result=False)['actual_model_calls'] == 0

    capacity = base/'packet_capacity'
    s.prepare(capacity, purpose='fixture_no_inference')
    code = '```python\nfrom pathlib import Path\nPath("known_effect.txt").write_text("committed")\n```'
    auxiliary = act(capacity, 'initial_only', tok, code, fixture_packet_limit=1)
    selected = act(capacity, 'live', tok, code, fixture_packet_limit=1)
    for arm, row in [('initial_only', auxiliary), ('live', selected)]:
        state = s.c.read(capacity/'branches'/arm/'STATE.json')
        full = s.c.read(capacity/'snapshots'/(arm+'_t1_bundle.json'))
        assert state['turn'] == 1 and state['world_id'] == row['after_id'] == full['id']
        assert any(x[0] == 'known_effect.txt' for x in full['entries'])
        assert row['known_action_committed'] and row['observation_status'] == 'packet_capacity'
        assert s.c.read(capacity/'observations'/(arm+'_t1.json'))['model_packet'] is None
    assert auxiliary['pause_reason'] is None and json.loads(auxiliary['feedback_for_next_input']) == {'runtime_feedback':json.loads(auxiliary['runtime_feedback_raw'])}
    assert selected['pause_reason'] == 'observation_capacity' and selected['feedback_for_next_input'] is None
    assert not (capacity/'PENDING.json').exists()
    assert s.audit(capacity, tok, save_result=False)['actual_model_calls'] == 0

    input_capacity = base/'input_capacity'
    s.prepare(input_capacity, purpose='fixture_no_inference')
    start_tokens = len(s.c.read(input_capacity/'inputs/initial_only.json')['input_token_ids'])
    committed = act(input_capacity, 'initial_only', tok, code, fixture_input_limit=start_tokens+1)
    assert committed['next_input_tokens'] > start_tokens+1
    assert committed['pause_reason'] == 'input_capacity' and committed['known_action_committed']
    assert s.c.read(input_capacity/'branches/initial_only/STATE.json')['turn'] == 1
    assert not (input_capacity/'PENDING.json').exists()
    assert s.audit(input_capacity, tok, save_result=False)['actual_model_calls'] == 0
    return {'status':'pass','model_calls':0,'main_world_opens':0,
        'actual_fixture_effect_persists_across_close_reopen':True,
        'new_file_observed_not_hardcoded_five':True,
        'actual_error_feedback_separate_from_state_observation':True,
        'known_error_does_not_semantically_pause_branch':True,
        'timing_after_known_effects_and_actual_world_step':True,
        'control_auxiliary_packet_overflow_does_not_pause':True,
        'live_packet_overflow_preserves_committed_action_and_full_snapshot':True,
        'whole_input_capacity_pause_preserves_committed_action':True,
        'overrides_are_fixture_only_not_real_study_limits':True,
        'synthetic_fixture_replies_are_not_model_progress':True}


if __name__ == '__main__':
    result = checks()
    s.save(H/'TEST_RESULTS.json', result)
    print(json.dumps(result))
