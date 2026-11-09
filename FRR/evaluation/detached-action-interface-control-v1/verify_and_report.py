"""Retained-evidence verification and report. No model inference."""
from pathlib import Path
import base64, collections, hashlib, json, sys
H = Path(__file__).resolve().parent
P = H.parent / 'final-garden-contract-v1'
D = H.parent / 'detached-directory-replay-comparison-v1'
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

def data(digest):
    o = read(H / 'objects' / (digest+'.json'))
    b = base64.b64decode(o['base64'],validate=True)
    assert sha(b)==digest==o['sha256'] and len(b)==o['bytes']
    return b

def notebook(bundle):
    e = next(x for x in bundle['entries'] if x[0]=='notebook.txt')
    assert e[1]=='file'
    b = data(e[3])
    assert len(b)==e[4]
    return b

def main():
    plan,done = read(H / 'PLAN.json'),read(H / 'COMPLETED.json')
    assert done['status']=='pass' and len(done['results'])==8
    canonical = runner.file_inventory(P)
    assert canonical==read(H / 'CANONICAL_BEFORE.json')==read(D / 'CANONICAL_BEFORE.json')
    runner.verify_pins()
    assert runner.state()['paused'] and runner.state()['next_entry']==1550
    assert not (runner.R / 'PENDING.json').exists() and not (runner.R / 'RUN.lock').exists()
    base = read(H / 'INITIAL_CHECKPOINT.json')
    assert base==read(runner.R / 'bundles/001550.json')
    src = (H / 'full_distribution_generation.py').read_bytes()
    assert src==(S / 'full_distribution_generation.py').read_bytes()
    assert hashlib.sha256(src).hexdigest()==plan['generation_source_sha256']
    old = read(D / 'conditions/no_replay_no_directory.json')['messages']
    tokens = read(H / 'CONDITION_TOKENS.json')
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False)
    for arm in plan['arms']:
        m = json.loads(json.dumps(old))
        m[-1]['content']+='\n\n'+plan['requests'][arm]
        assert read(H / 'conditions' / (arm+'.json'))=={'request':plan['requests'][arm],'messages':m}
        assert tokens[arm]['input_token_ids']==tok.apply_chat_template(m,tokenize=True,add_generation_prompt=True)
        assert len(tokens[arm]['input_token_ids'])==tokens[arm]['tokens']
    assert plan['seeds']==[runner.entry_seed(n) for n in range(1551,1555)]
    for p in (H / 'objects').glob('*.json'):
        data(p.stem)
    seen = set()
    for row in done['results']:
        key = row['seed'],row['arm']
        assert key not in seen
        seen.add(key)
        name = f"{row['seed']}_{row['arm']}"
        raw = read(H / 'raw' / (name+'.json'))
        result = read(H / 'results' / (name+'.json'))
        after = read(H / 'bundles' / (name+'.json'))
        p = read(H / 'plans' / (name+'.json'))
        assert row==read(H / 'events' / (name+'.json'))
        assert raw['messages']==read(H / 'conditions' / (row['arm']+'.json'))['messages']
        assert raw['input_token_ids']==p['input_token_ids']==tokens[row['arm']]['input_token_ids']
        assert p['before_id']==row['before_id']==base['id']
        assert raw['rng_seed']==row['seed']==p['seed']
        assert raw['temperature']==.8 and raw['top_p'] is None
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True)==raw['text']==row['text']
        assert raw['stop']==row['stop'] and len(raw['generated_token_ids'])==row['output_tokens_including_eos']
        assert (raw['stop']=='eos' and raw['generated_token_ids'][-1]==tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids'])==96)
        assert row['raw_sha256']==sha((H / 'raw' / (name+'.json')).read_bytes())
        try:
            parsed = json.loads(row['text'])
            valid_json = True
        except ValueError:
            parsed,valid_json = None,False
        assert row['json_valid']==valid_json and row['parsed_json']==parsed
        source = action(row['text'])
        assert row['valid_action_envelope']==(source is not None)
        assert row['source_is_requested_pwd']==(source is not None and source.strip()=='pwd')
        assert result['kind']==row['kind']==('shell' if source is not None else 'notebook')
        feedback = runner.model_feedback(result['feedback'])
        assert feedback==row['visible_feedback']
        observed = result['kind']=='shell' and feedback['exit_code']==0 and feedback['boundary'] is None and feedback['stdout']=='/world\n'
        assert row['world_stdout_observed']==observed
        assert row['requested_pwd_executed']==(row['source_is_requested_pwd'] and observed)
        assert after['id']==row['after_id']==sha(stable({'entries':after['entries'],'root_mode':after['root_mode']}))
        if result['kind']=='notebook' and feedback is None:
            assert notebook(after)==notebook(base)+(row['text']+'\n').encode()
            assert {x[0]:x for x in after['entries'] if x[0]!='notebook.txt'}=={x[0]:x for x in base['entries'] if x[0]!='notebook.txt'}
    assert seen=={(seed,arm) for seed in plan['seeds'] for arm in plan['arms']}
    metrics = {}
    for arm in plan['arms']:
        rows = [r for r in done['results'] if r['arm']==arm]
        metrics[arm] = {'trials':len(rows),'input_tokens':tokens[arm]['tokens'],
            'json_valid':sum(r['json_valid'] for r in rows),'valid_action_envelopes':sum(r['valid_action_envelope'] for r in rows),
            'requested_pwd_executed':sum(r['requested_pwd_executed'] for r in rows),
            'shell_calls':sum(r['kind']=='shell' for r in rows),'distinct_texts':len({r['text'] for r in rows}),
            'non_notebook_state_changes':sum(bool(r['non_notebook_changed_paths']) for r in rows),
            'stops':dict(collections.Counter(r['stop'] for r in rows)),
            'forms':dict(collections.Counter(r['text'] for r in rows))}
    save('SUMMARY.json',{'metrics':metrics,'results':done['results'],'canonical_paused_at':1550})
    verification = {'status':'pass','observer_model_calls':0,'external_generation_calls_verified':8,
        'canonical_generation_calls':0,'canonical_inventory_unchanged':True,'canonical_files_checked':len(canonical),
        'paused_at':1550,'prompt_reconstruction':True,'tokens_and_stops':True,'seeds_and_sampling':True,
        'parser_and_target_metrics':True,'world_hashes_and_appends':True,'training_updates':0,
        'scope':'Retained-evidence checks using pinned tokenizer and original parser/checkpoint format; no independent neural replication.'}
    save('VERIFICATION.json',verification)
    table = '\n'.join(f"| {arm} | {m['trials']} | {m['json_valid']} | {m['valid_action_envelopes']} | {m['requested_pwd_executed']} | {m['stops'].get('eos',0)} | {m['stops'].get('token_limit',0)} |" for arm,m in metrics.items())
    examples = '\n\n'.join(f"Seed {r['seed']}; {r['arm']}; {r['stop']}; {r['kind']}:\n\n```text\n{r['text']}\n```" for r in done['results'])
    report = f'''# Explicit action-interface diagnostic control

9 November 2026 UTC. The canonical garden remains paused at **1550**. All {len(canonical)} canonical phase files remain unchanged. Eight new model calls occurred only in disposable diagnostic conditions.

## Purpose and setup

Earlier authored fixtures established that valid actions execute in this runtime, but open-ended model trials produced no valid action. This check asks whether explicit requests can elicit the minimal pwd action. It is deliberately prompted; it is not a test of spontaneous curiosity, independent interface discovery, learning or emergence.

The plan was retained before inference. The same four predetermined seeds {plan['seeds']} were used for each of two conditions. Both started from the previous no-replay/no-directory input: explicit empty system, mechanical notice and original curiosity invitation. The fixed model, tokenizer, unfiltered sampler, temperature 0.8, two CPU threads, float32 eager inference, fresh KV, 96-token limit, initial world and action parser were unchanged. These were eight independent one-step trials, not a continuation or eight new entries.

The formulation request was:

> {plan['requests']['formulate']}

The copy request supplied the complete target:

```text
{plan['requests']['copy_exact']}
```

These prompts differ in wording and supplied information, not just one matched-length token. Their purpose is a limited competence diagnostic, not a pure causal measure of copying ability. No adaptive hints, retries or extra seeds were added.

## Observed results

| Condition | Trials | Parseable JSON | Valid action envelopes | Requested pwd executed | EOS | Token caps |
| --- | --- | --- | --- | --- | --- | --- |
{table}

Each reply was passed unchanged through the original receive() function on its own exact checkpoint restoration. An action was counted only if the full raw reply parsed as the declared two-key envelope. The requested command was separately checked for source equal to pwd after outer whitespace removal and a successful real receipt containing /world followed by a newline. This separates syntax, requested operation, and actual execution. No prose or fenced command was promoted to execution.

Actual shell calls: {sum(m['shell_calls'] for m in metrics.values())}. Trials with non-notebook changes: {sum(m['non_notebook_state_changes'] for m in metrics.values())}. Real receipts and all resulting snapshots are retained. World restoration passed after every trial; successful notebook writes were reconstructed directly from bytes.

## Limits and consequence

The results establish only the behavior of these prompts, this model and sampler, these four seeds, and this short action. A supplied target is easier to reproduce than independently formulating a command, but neither success nor failure generalizes to all tool use. Failure of a copy control under this presentation does not establish an intrinsic permanent inability. Earlier runtime fixtures remain evidence about the machinery, not the model's independent use of it.

The 96-token cap can interrupt writing. An already non-JSON prose prefix would not become a valid whole-reply action merely by appending more text, although a different prompt or sampling condition could produce a different prefix. No length comparison, alternate system framing, or instruction-only control was run here.

No newly generated receipt was fed into a second model turn, so reaction to feedback is untested. These prompted outputs did not become part of the canonical garden's notebook, short-context replay or world. No live repair, training, adapter, resource expansion or new invitation was introduced. The user requested wind-down after this check; no further runs are scheduled.

## Verification and preserved evidence

Frozen pins, model tensor digest and canonical inventory passed. External verification checked exact prompt assembly, tokenization/decoding, seed and stop records, unchanged sampler code, JSON/parser metrics, actual receipts, object hashes and applicable notebook appends. It made zero model calls and uses the pinned tokenizer and checkpoint representation rather than a separately implemented simulator.

PLAN.json records prospective requests and scope; COMPLETED.json, SUMMARY.json and VERIFICATION.json record outcomes and checks. All eight raw replies follow. Prior studies and history remain unchanged. See REST_SYNC.md for the pause and next-session orientation.

## All eight replies

{examples}

Sources: [directory/replay comparison](../detached-directory-replay-comparison-v1/REPORT.md), [sampler comparison](../detached-sampler-comparison-v1/REPORT.md), [runtime and support audit](../frozen-garden-tool-path-audit-v1/REPORT.md), [world map](../garden-state-laws-contact-map-v1/WORLD_MAP.md).
'''
    with (H / 'REPORT.md').open('x') as f:
        f.write(report)
    print(json.dumps({'status':'pass','metrics':metrics,'canonical_paused_at':1550},ensure_ascii=False))

if __name__=='__main__':
    main()
