"""Evidence checks and descriptive 2x2 report. No model inference."""
from pathlib import Path
import base64, collections, hashlib, json, sys
H = Path(__file__).resolve().parent
P = H.parent / 'final-garden-contract-v1'
S = H.parent / 'detached-sampler-comparison-v1'
sys.path.insert(0,str(P))
import runner
from world import action, sha, stable

def read(p):
    return json.loads(Path(p).read_text())

def save(name,value):
    with (H / name).open('x') as f:
        json.dump(value,f,indent=2,ensure_ascii=False,allow_nan=False)
        f.write('\n')

def object_bytes(digest):
    o = read(H / 'objects' / (digest+'.json'))
    b = base64.b64decode(o['base64'],validate=True)
    assert sha(b) == digest == o['sha256'] and len(b) == o['bytes']
    return b

def notebook(b):
    e = next(x for x in b['entries'] if x[0]=='notebook.txt')
    assert e[1]=='file'
    data = object_bytes(e[3])
    assert len(data)==e[4]
    return data

def main():
    plan,done = read(H / 'PLAN.json'),read(H / 'COMPLETED.json')
    assert done['status']=='pass' and len(done['results'])==16
    canonical = runner.file_inventory(P)
    assert canonical == read(H / 'CANONICAL_BEFORE.json') == read(S / 'CANONICAL_BEFORE.json')
    runner.verify_pins()
    assert runner.state()['paused'] and runner.state()['next_entry']==1550
    assert not (runner.R / 'PENDING.json').exists() and not (runner.R / 'RUN.lock').exists()
    original = read(H / 'INITIAL_MESSAGES.json')
    base = read(H / 'INITIAL_CHECKPOINT.json')
    assert base == read(runner.R / 'bundles/001550.json')
    assert original == runner.native_messages(base,runner.rows())
    suffix = '\nDirectory entries: '+json.dumps(sorted(set(e[0].split('/')[0] for e in base['entries'])),ensure_ascii=False)
    assert original[-1] == {'role':'user','content':suffix}
    src = (H / 'full_distribution_generation.py').read_bytes()
    assert src == (S / 'full_distribution_generation.py').read_bytes()
    assert hashlib.sha256(src).hexdigest()==plan['generation_source_sha256']
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False)
    tokens = read(H / 'CONDITION_TOKENS.json')
    for arm in plan['arms']:
        name = arm['id']
        # Reconstruct condition messages independently from the original data.
        if arm['replay']:
            expected = json.loads(json.dumps(original))
            if not arm['directory']:
                expected[-1]['content']=''
        else:
            expected = json.loads(json.dumps(original[:2]))
            if arm['directory']:
                expected[-1]['content']+=suffix
        m = read(H / 'conditions' / (name+'.json'))
        assert m == {'arm':arm,'messages':expected}
        ids = tok.apply_chat_template(expected,tokenize=True,add_generation_prompt=True)
        assert ids == tokens[name]['input_token_ids'] and len(ids) == tokens[name]['tokens']
        assert sha(json.dumps(ids,separators=(',',':')).encode()) == tokens[name]['sha256']
    assert plan['seeds'] == [runner.entry_seed(n) for n in range(1551,1555)]
    assert plan['seeds'] == read(S / 'PLAN.json')['seeds']
    for obj in (H / 'objects').glob('*.json'):
        object_bytes(obj.stem)
    seen = set()
    for e in done['results']:
        key = e['seed'],e['arm']
        assert key not in seen
        seen.add(key)
        name = f"{e['seed']}_{e['arm']}"
        raw = read(H / 'raw' / (name+'.json'))
        result = read(H / 'results' / (name+'.json'))
        after = read(H / 'bundles' / (name+'.json'))
        p = read(H / 'plans' / (name+'.json'))
        assert e == read(H / 'events' / (name+'.json'))
        assert raw['messages']==read(H / 'conditions' / (e['arm']+'.json'))['messages']
        assert raw['input_token_ids']==p['input_token_ids']==tokens[e['arm']]['input_token_ids']
        assert raw['rng_seed']==e['seed']==p['seed']
        assert p['before_id']==e['before_id']==base['id']
        assert raw['temperature']==.8 and raw['top_p'] is None
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==e['text']==raw['text']
        assert raw['stop']==e['stop']
        assert len(raw['generated_token_ids'])==e['output_tokens_including_eos']
        assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==96)
        assert e['raw_sha256']==sha((H / 'raw' / (name+'.json')).read_bytes())
        assert result['kind']==e['kind']==('shell' if action(e['text']) is not None else 'notebook')
        assert runner.model_feedback(result['feedback'])==e['visible_feedback']
        assert after['id']==e['after_id']==sha(stable({'entries':after['entries'],'root_mode':after['root_mode']}))
        if e['arm']=='replay12_directory':
            prior = read(S / 'raw' / f"{e['seed']}_nucleus_filter_removed.json")
            assert raw['input_token_ids']==prior['input_token_ids']
            assert raw['generated_token_ids']==prior['generated_token_ids']
        if e['kind']=='notebook' and result['feedback'] is None:
            assert notebook(after)==notebook(base)+(e['text']+'\n').encode()
            assert {x[0]:x for x in after['entries'] if x[0]!='notebook.txt'} == {x[0]:x for x in base['entries'] if x[0]!='notebook.txt'}
    assert seen == {(seed,a['id']) for seed in plan['seeds'] for a in plan['arms']}
    metrics = {}
    for arm in plan['arms']:
        name = arm['id']
        r = [e for e in done['results'] if e['arm']==name]
        metrics[name] = {'input_tokens':tokens[name]['tokens'],'messages':len(read(H / 'conditions' / (name+'.json'))['messages']),
            'trials':len(r),'distinct_texts':len({e['text'] for e in r}),
            'exact_directory_baseline_repeats':sum(e['same_text_as_directory_baseline'] for e in r),
            'starts_directory_entries':sum(e['text'].startswith('Directory entries:') for e in r),
            'shell_calls':sum(e['kind']=='shell' for e in r),'notebook_replies':sum(e['kind']=='notebook' for e in r),
            'visible_receipts':sum(e['visible_feedback'] is not None for e in r),
            'non_notebook_state_changes':sum(bool(e['non_notebook_changed_paths']) for e in r),
            'stops':dict(collections.Counter(e['stop'] for e in r)),
            'forms':dict(collections.Counter(e['text'] for e in r))}
    lookup = {(e['seed'],e['arm']):e for e in done['results']}
    pairs = []
    for factor,a,b in [('directory with replay','replay12_directory','replay12_no_directory'),
                       ('directory without replay','no_replay_directory','no_replay_no_directory'),
                       ('replay with directory','replay12_directory','no_replay_directory'),
                       ('replay without directory','replay12_no_directory','no_replay_no_directory')]:
        pairs.append({'factor':factor,'arms':[a,b],
            'seeds_with_different_text':[s for s in plan['seeds'] if lookup[s,a]['text']!=lookup[s,b]['text']],
            'interpretation':'Descriptive paired output differences under the declared delivery policies, not a significance test or isolated psychological mechanism.'})
    save('SUMMARY.json',{'canonical_paused_at':1550,'metrics':metrics,'paired_comparisons':pairs,'results':done['results']})
    v = {'status':'pass','observer_model_calls':0,'external_generation_calls_verified':16,
        'canonical_generation_calls':0,'canonical_files_checked':len(canonical),'canonical_inventory_unchanged':True,
        'paused_at':1550,'exact_input_reconstruction':True,'tokens_and_stops_verified':True,
        'same_world_and_generator':True,'all_reference_outputs_reproduced':True,
        'object_hashes_verified':True,'notebook_appends_reconstructed_when_applicable':True,
        'four_matched_seed_groups':True,'training_updates':0,
        'scope':'Retained-evidence verification using the pinned tokenizer/checkpoint format; no neural rerun or independently implemented simulator.'}
    save('VERIFICATION.json',v)
    table = '\n'.join(f"| {arm} | {m['input_tokens']} | {m['exact_directory_baseline_repeats']}/4 | {m['distinct_texts']} | {m['shell_calls']} | {m['stops'].get('eos',0)} | {m['stops'].get('token_limit',0)} |" for arm,m in metrics.items())
    ptable = '\n'.join(f"| {p['factor']} | {len(p['seeds_with_different_text'])}/4 |" for p in pairs)
    excerpts = '\n\n'.join(f"Seed {e['seed']}; {e['arm']}; {e['stop']}; {e['kind']}:\n\n```text\n{e['text']}\n```" for e in done['results'])
    report = f'''# Detached directory and replay comparisons

9 November 2026 UTC. Sixteen one-step trials on disposable copies of entry 1550. The canonical garden remains paused at **1550**, with all {len(canonical)} canonical phase files unchanged. No redesigned condition was adopted.

## Question and fixed conditions

After removing nucleus filtering alone left all four sampled outputs unchanged, does removing the current directory observation, recent self-replay, or both alter the next reply?

A plan was saved before inference. We used the same four deterministic seeds {plan['seeds']} in all four conditions. These are reuses of the earlier seed set, not sixteen new independent random seeds. We re-ran the previous unfiltered reference and reproduced its four exact token sequences.

All conditions used the pinned SmolLM2-135M-Instruct checkpoint, tokenizer, float32 CPU eager inference, two threads, temperature 0.8, **no nucleus filtering**, fresh KV, 96 output tokens, exact original notice/invitation, unchanged action parser and world resource limits. Each trial began from the same entry-1550 filesystem. No reply or resulting world state was carried into another trial.

## Conditions and results

| Condition | Input tokens | Exact directory-list repeats | Distinct texts | Shell calls | EOS | Token caps |
| --- | --- | --- | --- | --- | --- | --- |
{table}

The directory-only change removes the current suffix on the final user message. It does not erase directory listings from historical replies. The replay-only change removes the twelve historical assistant/user pairs; the current directory suffix then follows the unchanged initial user notice/seed. The both-removed condition contains only the explicit empty system and original user notice/seed.

Removing replay therefore changes message count, token length and cue positions as part of the delivery policy. This is not a role-position- or token-length-matched experiment isolating a psychological memory mechanism. Filename mentions in the mechanical notice remain in every condition. The model still receives instructions about available actions and the broad curiosity invitation.

| Paired comparison | Seeds with different next text |
| --- | --- |
{ptable}

Paired differences are descriptive observations about these inputs and seeds, not statistical evidence of population-level improvement. Exact text differences do not establish meaningful exploration.

## Actual world contact

Each raw output was passed unchanged to the original receive() function on its own fresh checkpoint copy. Valid action envelopes would execute under the original limits; every other output remained writing. No command was extracted from prose or code fences, repaired, or semantically graded. Actual receipts and state changes are in each saved result and event.

World effect totals: {sum(m['shell_calls'] for m in metrics.values())} shell calls; {sum(m['non_notebook_state_changes'] for m in metrics.values())} trials with non-notebook changes. All trial checkpoints were captured and restored using the pinned decoder. Where replies were successful notebook writing, their appended bytes were independently reconstructed from the initial notebook and raw reply.

These are single-step trials. They do not measure persistence of a new trajectory, later retrieval, adaptation to feedback, or learning. Removing the automatic replay for one diagnostic call does not provide a replacement continuity mechanism for an ongoing garden. Broader prose and a token cap are not evidence of deeper reasoning. Generated descriptions of files or actions must be distinguished from actual filesystem effects.

## Interpretation boundaries

The original sampler's singleton-support result remains valid for its original input. These tests change input-delivery conditions with filtering off; they do not refute that finding or isolate an interaction with top-p 0.9. The comparison can show whether a changed delivery policy changes a sampled reply under the fixed model and seed. It cannot establish that a particular policy guarantees emergence or that the model's full capabilities have been exposed.

Before treating any variant as a better world, it would need a usable continuity design and observed contact with actual environmental consequences. This study does not add prompts, tasks, demonstrations, training, tool extraction or hidden observer judgments to obtain such a result. The invitation remains unchanged.

## Integrity and preservation

Sixteen external generation calls; zero canonical calls. The model tensor digest, frozen source/runtime/model pins, original phase inventory, state, lock and pending conditions passed. External verification reconstructed condition messages and token IDs, checked raw decoding, stops, seeds, generator identity, reference reproducibility, parser categories, object hashes and applicable notebook effects. Verification made zero model calls.

All outputs, including quiet duplicates and unfinished text, are retained. Reports concern what was written and what actually happened, not private internal reasoning, intention, emotion or maturity. No extra seeds, canonical continuation or new live condition was started automatically.

## All sixteen replies

{excerpts}

Sources: PLAN.json, CONDITION_TOKENS.json, COMPLETED.json, SUMMARY.json, VERIFICATION.json, [sampler comparison](../detached-sampler-comparison-v1/REPORT.md), [tool-path audit](../frozen-garden-tool-path-audit-v1/REPORT.md), [world map](../garden-state-laws-contact-map-v1/WORLD_MAP.md).
'''
    with (H / 'REPORT.md').open('x') as f:
        f.write(report)
    print(json.dumps({'status':'pass','metrics':metrics,'paired_comparisons':pairs,'canonical_paused_at':1550},ensure_ascii=False))

if __name__ == '__main__':
    main()
