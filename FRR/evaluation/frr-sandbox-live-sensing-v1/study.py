"""Matched initial-only/live sensing; preparation and fixtures never invoke a model."""
import os
for key, value in {'HF_HUB_OFFLINE':'1','OMP_NUM_THREADS':'2','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'2'}.items():
    os.environ[key] = value
from pathlib import Path
import argparse, copy, importlib.util, json, sys, traceback, uuid

H = Path(__file__).resolve().parent
E = H.parent
M = E/'bounded-main-continuation-v1'
RD = E/'frr-sandbox-rd-v1'
INSTRUMENT = RD/'interface/instrument/snapshot_packet.py'
sys.path[:0] = [str(E/'observability-three-contact-v1'), str(INSTRUMENT.parent)]
import common as c
from snapshot_packet import make_snapshot, PacketCapacityError

_spec = importlib.util.spec_from_file_location('live_sensing_fixed_body', c.C/'generation.py')
body = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(body)
ARMS = ('initial_only', 'live')
TURNS = 4
BYTE_LIMIT = 8192
INPUT_LIMIT = 7936
DATE = '2026-11-15 America/Chicago'


def save(path, value):
    c.candidate.immutable(Path(path), value)


def atomic(path, value):
    c.candidate.atomic(Path(path), value)


def pin_paths():
    return [Path(__file__), H/'mechanics_user.txt', H/'world_rules.txt', INSTRUMENT,
            RD/'interface/mechanics_user.txt', RD/'interface/world_rules.txt',
            c.H/'common.py', c.C/'generation.py', c.C/'candidate.py',
            c.C/'world/garden_world.py', E/'final-garden-contract-v1/world.py',
            E/'final-garden-contract-v1/server.py', c.MODEL/'config.json',
            c.MODEL/'tokenizer.json', c.MODEL/'tokenizer_config.json']


def guard(run):
    run = Path(run)
    assert c.inventory(M) == c.read(run/'MAIN_BEFORE.json'), 'Selected main files changed'
    assert c.inventory() == c.read(run/'SOURCE_BEFORE.json'), 'Original source phase changed'
    assert c.sha(E.parent/'ACTIVE_GARDEN_PHASE.json') == c.read(run/'MANIFEST.json')['active_pointer_sha256']
    assert all(c.sha(Path(p)) == sha for p, sha in c.read(run/'MANIFEST.json')['pins'].items()), 'Pinned source/input drift'


def render_snapshot(run, arm, bundle, *, timing, world_step, reply_index, byte_limit=BYTE_LIMIT):
    """Save full known snapshot even when its projected model packet cannot fit."""
    run = Path(run)
    label = arm + ('_initial' if timing == 'initial' else f'_t{reply_index}')
    snapshot_path = run/'snapshots'/(label+'_bundle.json')
    save(snapshot_path, bundle)
    try:
        rendered = make_snapshot(bundle, timing=timing, world_step=world_step,
                                 reply_index=reply_index, max_packet_bytes=byte_limit)
        observation = {'status':'complete', 'model_packet':rendered.model_packet,
                       'model_text':rendered.model_text, 'observer_record':rendered.observer_record}
    except PacketCapacityError as error:
        observation = {'status':'packet_capacity', 'model_packet':None, 'model_text':None,
                       'observer_record':{'source_bundle_id':bundle['id'], 'timing':timing,
                         'world_step':world_step, 'reply_index':reply_index,
                         'required_bytes':error.required_bytes, 'limit_bytes':error.limit_bytes,
                         'entry_count':error.entry_count, 'partial_packet_emitted':False}}
    save(run/'observations'/(label+'.json'), observation)
    return observation, snapshot_path


def prepare(run, purpose='model_study'):
    run = Path(run)
    run.mkdir(parents=True, exist_ok=False)
    assert purpose in ('model_study', 'fixture_no_inference')
    state = c.read(M/'run/STATE.json')
    assert state['human_entry'] == 1630 and state['paused']
    assert not (M/'run/RUN.lock').exists() and not (M/'run/PENDING.json').exists()
    assert c.verify_store(M/'run/world')['status'] == 'pass'
    assert (H/'mechanics_user.txt').read_bytes() == (RD/'interface/mechanics_user.txt').read_bytes()
    pins = {str(path):c.sha(path) for path in pin_paths()}
    save(run/'MAIN_BEFORE.json', c.inventory(M))
    save(run/'SOURCE_BEFORE.json', c.inventory())
    save(run/'PARENT_STATE.json', state)
    save(run/'BEFORE_ACTIVE_POINTER.json', c.read(E.parent/'ACTIVE_GARDEN_PHASE.json'))
    manifest = {'date':DATE, 'date_basis':'root relayed updated developer client date; not host date',
        'purpose':purpose, 'version':'frr-sandbox-live-sensing-v1', 'arms':list(ARMS),
        'turns_per_arm':TURNS, 'planned_model_calls':8 if purpose == 'model_study' else 0,
        'FRR':False, 'system':'empty in both arms', 'source_main_entry':1630,
        'initial_messages':'same M0 mechanical user plus same new-instrument initial packet',
        'world_delta':'common WORLD_RULES replacement only; all other source files retained',
        'feedback':'common typed runtime_feedback field; live alone adds world_observation',
        'observation_bytes':BYTE_LIMIT, 'whole_input_tokens':INPUT_LIMIT, 'output_tokens':256,
        'history':'all actual branch pairs, no pruning/truncation',
        'observation_capacity':'live pauses; initial_only records auxiliary failure and continues if actual input fits',
        'semantics':'names/types/logical bytes and counters are partial observations, not file contents or full world/mental state',
        'confounds':'extra feedback text, JSON fields, length, counters, timing; changed initial schema gives a new matched baseline, not historical M1 latency-only contrast',
        'stop':'bounded4reply budget, user pause, whole-input or selected-observation capacity, unknown effects/dependency drift; no productivity gate',
        'pins':pins, 'tensor_digest':c.read(c.C/'run/MANIFEST.json')['tensor_digest'],
        'active_pointer_sha256':c.sha(E.parent/'ACTIVE_GARDEN_PHASE.json'),
        'training_updates':0, 'activation':False}
    save(run/'MANIFEST.json', manifest)
    parent_store = M/'run/world'
    parent_bundle = parent_store/'bundles'/c.read(parent_store/'STATE.json')['bundle']
    parent = c.read(parent_bundle)
    save(run/'PARENT_WORLD.json', parent)
    import base64
    old_rule = next(x for x in parent['entries'] if x[0] == 'WORLD_RULES.txt')
    (run/'PARENT_WORLD_RULES.txt').write_bytes(base64.b64decode(c.read(parent_store/'objects'/(old_rule[3]+'.json'))['base64']))
    tok = c.tokenizer()
    checks = []
    for arm in ARMS:
        store = run/'branches'/arm/'world'
        save(run/'PREPARATION_PENDING.json', {'arm':arm, 'stage':'initialization unresolved'})
        world = c.GardenWorld.create(store, parent_bundle, parent_store/'objects', parent_entry=1630)
        try:
            before = world.checkpoint()
            rules = (H/'world_rules.txt').read_text()
            code = "from pathlib import Path\nPath('WORLD_RULES.txt').write_text("+repr(rules)+",encoding='utf-8')"
            op = world.apply('python', code)
            save(run/'preparation'/(arm+'.json'), {'actor':'operator', 'source':code, 'event':op})
            assert op['feedback']['exit_code'] == 0 and op['feedback']['boundary'] is None
            assert op['changed_paths'] == ['WORLD_RULES.txt']
            after = world.checkpoint()
        finally:
            world.close()
        a, b = {x[0]:x for x in before['entries']}, {x[0]:x for x in after['entries']}
        assert set(a) == set(b) and all(a[p] == b[p] for p in a if p != 'WORLD_RULES.txt')
        assert b['WORLD_RULES.txt'][3] == c.sha(H/'world_rules.txt')
        assert c.verify_store(store)['status'] == 'pass'
        observation, snapshot_path = render_snapshot(run, arm, after, timing='initial', world_step=1, reply_index=None)
        assert observation['status'] == 'complete', 'Both complete initial packets must fit before inference'
        messages = [{'role':'system', 'content':''}, {'role':'user', 'content':(H/'mechanics_user.txt').read_text()+'\n\n'+observation['model_text']}]
        tokens = tok.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
        assert len(tokens) <= INPUT_LIMIT
        save(run/'inputs'/(arm+'.json'), {'messages':messages, 'input_token_ids':tokens,
             'initial_snapshot_sha256':c.sha(snapshot_path), 'prepared_world_id':after['id']})
        atomic(store.parent/'STATE.json', {'turn':0, 'paused':True, 'last_record_sha256':None,
             'world_step':1, 'world_id':after['id'], 'stop_reason':None, 'actual_model_calls':0})
        checks.append({'arm':arm, 'world_id':after['id'], 'input_tokens':len(tokens)})
        (run/'PREPARATION_PENDING.json').unlink()
    assert checks[0]['world_id'] == checks[1]['world_id']
    assert c.read(run/'inputs/initial_only.json')['input_token_ids'] == c.read(run/'inputs/live.json')['input_token_ids']
    guard(run)
    save(run/'PREPARATION_CHECKS.json', {'status':'pass', 'conditions':checks,
         'same_initial_world_and_input':True, 'model_calls':0, 'main_unchanged':True})
    return preflight(run, tok)


def branch_rows(run, arm):
    return [c.read(p) for p in sorted((Path(run)/'records').glob(arm+'_t*.json'))]


def messages_for(run, arm):
    messages = copy.deepcopy(c.read(Path(run)/'inputs'/(arm+'.json'))['messages'])
    for row in branch_rows(run, arm):
        if row['feedback_for_next_input'] is None:
            raise ValueError('No complete next feedback exists for this paused branch')
        messages += [{'role':'assistant','content':row['text']},
                     {'role':'user','content':row['feedback_for_next_input']}]
    return messages


def feedback_text(actual_runtime_feedback, observation_packet=None):
    data = {'runtime_feedback':json.loads(actual_runtime_feedback) if actual_runtime_feedback else None}
    if observation_packet is not None:
        data['world_observation'] = observation_packet['world_snapshot']
    return json.dumps(data, ensure_ascii=True, sort_keys=True, separators=(',', ':'))


def preflight(run, tok=None):
    run = Path(run)
    guard(run)
    assert not (run/'PENDING.json').exists() and not (run/'PREPARATION_PENDING.json').exists()
    tok = tok or c.tokenizer()
    checks = []
    for arm in ARMS:
        state = c.read(run/'branches'/arm/'STATE.json')
        assert state['paused'] and state['turn'] == 0 and state['stop_reason'] is None
        source = c.read(run/'inputs'/(arm+'.json'))
        assert tok.apply_chat_template(source['messages'], tokenize=True, add_generation_prompt=True) == source['input_token_ids']
        world = c.verify_store(run/'branches'/arm/'world')
        assert world['bundle_id'] == source['prepared_world_id']
        checks.append({'arm':arm, 'world':world, 'input_tokens':len(source['input_token_ids'])})
    return {'status':'pass', 'prepared':checks, 'model_calls':0, 'main_entry':1630, 'activation':False}


def begin_reply(run, arm, tok):
    run = Path(run)
    assert arm in ARMS
    assert not (run/'PENDING.json').exists()
    base = run/'branches'/arm
    state = c.read(base/'STATE.json')
    assert state['paused'] and state['turn'] < TURNS and state['stop_reason'] is None
    messages = messages_for(run, arm)
    tokens = tok.apply_chat_template(messages, tokenize=True, add_generation_prompt=True)
    n = state['turn']+1
    if len(tokens) > INPUT_LIMIT:
        save(run/'capacity_events'/(arm+f'_before_t{n}.json'), {'reason':'input_capacity', 'input_tokens':len(tokens), 'limit':INPUT_LIMIT, 'model_generation':False})
        state['stop_reason'] = 'input_capacity'; atomic(base/'STATE.json', state)
        return None
    label = arm+f'_t{n}'
    plan = {'arm':arm, 'turn':n, 'label':label, 'messages':messages, 'input_token_ids':tokens,
            'before_id':state['world_id'], 'world_step':state['world_step'],
            'parent_record_sha256':state['last_record_sha256']}
    save(run/'plans'/(label+'.json'), plan)
    save(run/'PENDING.json', {'arm':arm, 'turn':n, 'stage':'generation and effects unresolved; no automatic replay'})
    return plan


def commit_reply(run, arm, raw, tok, *, fixture_packet_limit=None, fixture_input_limit=None):
    """Commit known effects before any selected-observation/input capacity pause."""
    run = Path(run); base = run/'branches'/arm; store = base/'world'
    old = c.read(base/'STATE.json'); n = old['turn']+1; label = arm+f'_t{n}'
    pending = c.read(run/'PENDING.json')
    assert pending['arm'] == arm and pending['turn'] == n
    purpose = c.read(run/'MANIFEST.json')['purpose']
    assert purpose == 'fixture_no_inference' or (fixture_packet_limit is None and fixture_input_limit is None)
    packet_limit = BYTE_LIMIT if fixture_packet_limit is None else fixture_packet_limit
    input_limit = INPUT_LIMIT if fixture_input_limit is None else fixture_input_limit
    plan = c.read(run/'plans'/(label+'.json'))
    assert raw['messages'] == plan['messages'] and raw['input_token_ids'] == plan['input_token_ids']
    assert raw['decoder'] == 'greedy_argmax' or (purpose == 'fixture_no_inference' and raw['decoder'] == 'fixture_no_inference')
    save(run/'raw'/(label+'.json'), raw)
    assert tok.decode(raw['generated_token_ids'], skip_special_tokens=True) == raw['text']
    assert 0 < len(raw['generated_token_ids']) <= 256
    assert (raw['stop'] == 'eos' and raw['generated_token_ids'][-1] == tok.eos_token_id) or (raw['stop'] == 'token_limit' and len(raw['generated_token_ids']) == 256)
    world = c.GardenWorld.open(store)
    try:
        before = world.checkpoint(); assert before['id'] == plan['before_id']
        batch = world.receive_notebook(raw['text']); save(run/'batches'/(label+'.json'), batch)
        after = world.checkpoint(); world_step = world.step
    finally:
        world.close()
    verification = c.verify_store(store)
    assert verification['bundle_id'] == after['id']
    observation, snapshot_path = render_snapshot(run, arm, after, timing='after_reply',
           world_step=world_step, reply_index=n, byte_limit=packet_limit)
    actual = c.candidate.project_feedback(batch)
    selected = arm == 'live' and observation['status'] == 'complete'
    feedback = None if arm == 'live' and not selected else feedback_text(actual, observation['model_packet'] if selected else None)
    pause = 'observation_capacity' if arm == 'live' and feedback is None else None
    next_tokens = None
    if feedback is not None:
        following = plan['messages']+[{'role':'assistant','content':raw['text']},{'role':'user','content':feedback}]
        next_tokens = len(tok.apply_chat_template(following, tokenize=True, add_generation_prompt=True))
        if next_tokens > input_limit: pause = 'input_capacity'
    row = {'arm':arm, 'turn':n, 'label':label, 'model_generation':raw['decoder'] != 'fixture_no_inference',
       'text':raw['text'], 'stop':raw['stop'], 'input_tokens':len(raw['input_token_ids']),
       'output_tokens':len(raw['generated_token_ids']), 'before_id':before['id'], 'after_id':after['id'],
       'world_step':world_step, 'parent_record_sha256':old['last_record_sha256'],
       'source_main_last_event_sha256':c.read(run/'PARENT_STATE.json')['last_event_sha256'],
       'raw_sha256':c.sha(run/'raw'/(label+'.json')), 'batch_sha256':c.sha(run/'batches'/(label+'.json')),
       'snapshot_sha256':c.sha(snapshot_path), 'observation_status':observation['status'],
       'observation_capacity_event':observation['observer_record'] if observation['status'] != 'complete' else None,
       'runtime_feedback_raw':actual, 'feedback_for_next_input':feedback,
       'observation_selected_for_next_input':selected, 'next_input_tokens':next_tokens,
       'whole_input_limit_used':input_limit, 'packet_byte_limit_used':packet_limit,
       'fixture_limit_override':fixture_packet_limit is not None or fixture_input_limit is not None,
       'pause_reason':pause, 'boundary':batch['boundary'], 'complete_cells':batch['parsed']['complete_executable_cells'],
       'incomplete_fences':sum(not x['complete'] for x in batch['parsed']['cells']),
       'model_initiated_actions':[{'channel':x['channel'],'source':x['source'], 'feedback':x['feedback'],'changed_paths':x['changed_paths']} for x in batch['operations'] if x['channel'] in ('python','shell')],
       'automatic_note_operations':[{'feedback':x['feedback'],'changed_paths':x['changed_paths']} for x in batch['operations'] if x['channel'] == 'note'],
       'world_verification':verification, 'known_action_committed':True}
    path = run/'records'/(label+'.json'); save(path, row)
    atomic(base/'STATE.json', {'turn':n, 'paused':True, 'last_record_sha256':c.sha(path),
        'world_step':world_step, 'world_id':after['id'], 'stop_reason':pause,
        'actual_model_calls':old['actual_model_calls']+int(row['model_generation'])})
    (run/'PENDING.json').unlink()
    return row


def run_model(run):
    run = Path(run)
    assert not (run/'RUN_STARTED.json').exists() and not (run/'RESULTS.json').exists(), 'Existing attempt; never replay automatically'
    assert c.read(run/'MANIFEST.json')['purpose'] == 'model_study'
    token = uuid.uuid4().hex
    save(run/'RUN.lock', {'token':token, 'pid':os.getpid()})
    try:
        tok = c.tokenizer(); preflight(run, tok)
        save(run/'RUN_STARTED.json', {'planned_model_calls':8, 'no_automatic_resume':True})
        import torch
        from transformers import AutoModelForCausalLM
        from runtime_reference import parameter_digest, Guard
        torch.set_num_threads(2)
        resource = Guard(5153960755, run/'RESOURCE.jsonl'); resource.read('before_model_load')
        model = AutoModelForCausalLM.from_pretrained(c.MODEL, local_files_only=True, trust_remote_code=False,
            use_safetensors=True, torch_dtype=torch.float32, attn_implementation='eager')
        model.requires_grad_(False); model.eval()
        expected = c.read(run/'MANIFEST.json')['tensor_digest']; assert parameter_digest(model, False) == expected
        resource.read('model_loaded')
        for n in range(1, TURNS+1):
            for arm in ARMS:
                state = c.read(run/'branches'/arm/'STATE.json')
                if state['stop_reason'] is not None: continue
                if (run/'PAUSE_REQUEST').exists():
                    state['stop_reason'] = 'user_pause'; atomic(run/'branches'/arm/'STATE.json', state); continue
                guard(run)
                plan = begin_reply(run, arm, tok)
                if plan is None: continue
                assert plan['turn'] == n
                raw = body.generate(model, tok, plan['messages'], resource, 'live_sensing_'+plan['label'])
                row = commit_reply(run, arm, raw, tok)
                assert parameter_digest(model, False) == expected; guard(run)
                print(json.dumps({k:row[k] for k in ('arm','turn','input_tokens','output_tokens','complete_cells','observation_status','pause_reason')}), flush=True)
        result = audit(run, tok, save_result=False)
        result.update(weights_unchanged=parameter_digest(model, False) == expected, training_updates=0)
        save(run/'RESULTS.json', result)
        print(json.dumps({'actual_model_calls':result['actual_model_calls'],'planned_model_calls':8,'main_entry':1630,'activation':False}), flush=True)
    except BaseException as error:
        save(run/('ERROR_'+uuid.uuid4().hex+'.json'), {'type':type(error).__name__, 'message':str(error),
             'traceback':traceback.format_exc(), 'pending':(run/'PENDING.json').exists()})
        raise
    finally:
        if (run/'RUN.lock').exists() and c.read(run/'RUN.lock').get('token') == token:
            (run/'RUN.lock').unlink()


def audit(run, tok=None, *, save_result=True):
    run = Path(run); guard(run); tok = tok or c.tokenizer()
    assert not (run/'PENDING.json').exists() and not (run/'PREPARATION_PENDING.json').exists()
    counts = {}; rows_all = []; consumed = {}
    for arm in ARMS:
        messages = copy.deepcopy(c.read(run/'inputs'/(arm+'.json'))['messages']); last = None
        rows = branch_rows(run, arm); consumed[arm] = 0
        previous_bundle = c.read(run/'snapshots'/(arm+'_initial_bundle.json'))
        world_store = run/'branches'/arm/'world'
        assert previous_bundle == c.read(world_store/'bundles/000001.json')
        assert previous_bundle['id'] == c.read(run/'inputs'/(arm+'.json'))['prepared_world_id']
        previous_step = 1
        for n, row in enumerate(rows, 1):
            label = arm+f'_t{n}'; plan = c.read(run/'plans'/(label+'.json')); raw = c.read(run/'raw'/(label+'.json'))
            batch = c.read(run/'batches'/(label+'.json')); snap = c.read(run/'snapshots'/(label+'_bundle.json'))
            observation = c.read(run/'observations'/(label+'.json'))
            assert row['turn'] == n and row['parent_record_sha256'] == plan['parent_record_sha256'] == last
            assert plan['messages'] == raw['messages'] == messages
            assert tok.apply_chat_template(messages, tokenize=True, add_generation_prompt=True) == raw['input_token_ids'] == plan['input_token_ids']
            assert tok.decode(raw['generated_token_ids'], skip_special_tokens=True) == raw['text'] == row['text'] == batch['raw_text']
            assert row['raw_sha256'] == c.sha(run/'raw'/(label+'.json')) and row['batch_sha256'] == c.sha(run/'batches'/(label+'.json'))
            assert row['snapshot_sha256'] == c.sha(run/'snapshots'/(label+'_bundle.json')) and snap['id'] == row['after_id']
            assert row['before_id'] == plan['before_id'] == previous_bundle['id']
            assert row['world_step'] == (batch['operations'][-1]['step'] if batch['operations'] else previous_step)
            assert snap == c.read(world_store/'bundles'/f"{row['world_step']:06d}.json")
            assert batch == c.read(world_store/'batches'/(batch['batch_id']+'.json'))
            for op in batch['operations']:
                event = {k:v for k,v in op.items() if k not in ('cell_index','source_start','source_end')}
                assert event == c.read(world_store/'events'/f"{op['step']:06d}.json")
            assert row['boundary'] == batch['boundary'] and row['complete_cells'] == batch['parsed']['complete_executable_cells']
            assert row['runtime_feedback_raw'] == c.candidate.project_feedback(batch)
            assert batch['parsed'] == c.parse_notebook(raw['text'])
            if observation['status'] == 'complete':
                expected = make_snapshot(snap, timing='after_reply', world_step=row['world_step'], reply_index=n, max_packet_bytes=row['packet_byte_limit_used'])
                assert observation['model_text'] == expected.model_text and observation['model_packet'] == expected.model_packet
                assert observation['observer_record'] == expected.observer_record
            else:
                try: make_snapshot(snap, timing='after_reply', world_step=row['world_step'], reply_index=n, max_packet_bytes=row['packet_byte_limit_used'])
                except PacketCapacityError: pass
                else: raise AssertionError('Claimed capacity event not reproduced')
            feedback = row['feedback_for_next_input']
            if feedback is not None:
                parsed = json.loads(feedback)
                assert parsed['runtime_feedback'] == (json.loads(row['runtime_feedback_raw']) if row['runtime_feedback_raw'] else None)
                assert set(parsed) == ({'runtime_feedback','world_observation'} if arm == 'live' else {'runtime_feedback'})
                if arm == 'live':
                    assert parsed['world_observation'] == observation['model_packet']['world_snapshot']
                assert feedback == feedback_text(row['runtime_feedback_raw'], observation['model_packet'] if arm == 'live' else None)
                messages += [{'role':'assistant','content':row['text']},{'role':'user','content':feedback}]
            else: assert arm == 'live' and row['pause_reason'] == 'observation_capacity'
            if row['model_generation'] and n > 1 and 'world_observation' in json.loads(plan['messages'][-1]['content']): consumed[arm] += 1
            previous_bundle = snap; previous_step = row['world_step']
            last = c.sha(run/'records'/(label+'.json'))
        state = c.read(run/'branches'/arm/'STATE.json')
        assert state['turn'] == len(rows) and state['last_record_sha256'] == last
        assert state['actual_model_calls'] == sum(x['model_generation'] for x in rows)
        verified = c.verify_store(run/'branches'/arm/'world')
        assert verified['bundle_id'] == state['world_id'] and verified['step'] == state['world_step']
        counts[arm] = {'completed_replies':len(rows), 'actual_model_calls':sum(x['model_generation'] for x in rows),
            'stop_reason':state['stop_reason'], 'world':verified}
        rows_all += rows
    result = {'status':'pass','planned_model_calls':8 if c.read(run/'MANIFEST.json')['purpose'] == 'model_study' else 0,
       'actual_model_calls':sum(x['model_generation'] for x in rows_all), 'completed_notebook_replies':len(rows_all),
       'conditions':counts, 'after_reply_snapshots':len(rows_all), 'post_reply_observations_consumed_by_generation':consumed,
       'complete_cells':sum(x['complete_cells'] for x in rows_all), 'main_entry':1630,
       'main_unchanged':True, 'activation':False, 'pending':False}
    if save_result: save(run/'AUDIT.json', result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare','preflight','run','audit'])
    parser.add_argument('--store', type=Path, default=H/'run')
    args = parser.parse_args()
    if args.command == 'prepare': print(json.dumps(prepare(args.store)))
    elif args.command == 'preflight': print(json.dumps(preflight(args.store)))
    elif args.command == 'run': run_model(args.store)
    else: print(json.dumps(audit(args.store)))
