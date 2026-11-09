"""External retained-evidence verification and descriptive report; no model calls."""
from pathlib import Path
import base64, collections, hashlib, json, math, sys
H = Path(__file__).resolve().parent
P = H.parent / 'final-garden-contract-v1'
sys.path.insert(0,str(P))
import runner
from world import action, stable, sha

def save(name,value):
    with (H / name).open('x') as f:
        json.dump(value,f,indent=2,ensure_ascii=False,allow_nan=False)
        f.write('\n')

def read(p):
    return json.loads(Path(p).read_text())

def object_bytes(digest):
    obj = read(H / 'objects' / (digest+'.json'))
    b = base64.b64decode(obj['base64'],validate=True)
    assert len(b) == obj['bytes'] and sha(b) == digest == obj['sha256']
    return b

def notebook_bytes(bundle):
    ent = next(x for x in bundle['entries'] if x[0] == 'notebook.txt')
    assert ent[1] == 'file'
    b = object_bytes(ent[3])
    assert len(b) == ent[4]
    return b

def main():
    done, plan = read(H / 'COMPLETED.json'), read(H / 'PLAN.json')
    assert done['status'] == 'pass'
    canonical = runner.file_inventory(P)
    assert canonical == read(H / 'CANONICAL_BEFORE.json')
    runner.verify_pins()
    s = runner.state()
    assert s['paused'] and s['next_entry'] == 1550
    assert not (runner.R / 'PENDING.json').exists() and not (runner.R / 'RUN.lock').exists()
    base = read(H / 'INITIAL_CHECKPOINT.json')
    assert base == read(runner.R / 'bundles/001550.json')
    messages = read(H / 'INITIAL_MESSAGES.json')
    assert messages == runner.native_messages(base,runner.rows())
    original = (P / 'generation.py').read_text()
    assert (H / 'original_generation_reference.py').read_text() == original
    expected = original.replace("   remove=torch.cumsum(p,0)-p>=.9;v=v.masked_fill(remove,float('-inf'))",'   # Experimental condition: omit nucleus filtering; retain full softmax.').replace('temperature=.8,top_p=.9)','temperature=.8,top_p=None)')
    assert (H / 'full_distribution_generation.py').read_text() == expected
    assert plan['source_generator_sha256'] == hashlib.sha256(original.encode()).hexdigest()
    assert plan['alternative_generator_sha256'] == hashlib.sha256(expected.encode()).hexdigest()
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(runner.BASE,local_files_only=True,trust_remote_code=False)
    ids = tok.apply_chat_template(messages,tokenize=True,add_generation_prompt=True)
    known = read(runner.R / 'raw/001550.json')
    assert ids == known['input_token_ids']
    assert plan['seeds'] == [runner.entry_seed(n) for n in range(1551,1555)]
    assert len(done['results']) == 8
    for q in (H / 'objects').glob('*.json'):
        object_bytes(q.stem)
    seen = set()
    for row in done['results']:
        key = (row['seed'],row['arm'])
        assert key not in seen
        seen.add(key)
        name = f"{row['seed']}_{row['arm']}"
        saved = read(H / 'events' / (name+'.json'))
        raw = read(H / 'raw' / (name+'.json'))
        result = read(H / 'results' / (name+'.json'))
        before = read(H / 'plans' / (name+'.json'))
        after = read(H / 'bundles' / (name+'.json'))
        assert saved == row
        assert raw['messages'] == messages and raw['input_token_ids'] == before['input_token_ids'] == ids
        assert raw['rng_seed'] == before['seed'] == row['seed']
        assert before['before_id'] == row['before_id'] == base['id']
        assert raw['temperature'] == .8
        assert raw['top_p'] == (.9 if row['arm'] == 'original_top_p_0.9' else None)
        assert tok.decode(raw['generated_token_ids'],skip_special_tokens=True) == row['text'] == raw['text']
        assert raw['stop'] == row['stop']
        assert (raw['stop']=='eos' and raw['generated_token_ids'][-1] == tok.eos_token_id) or (raw['stop']=='token_limit' and len(raw['generated_token_ids']) == 96)
        assert row['raw_sha256'] == sha((H / 'raw' / (name+'.json')).read_bytes())
        assert result['kind'] == row['kind'] == ('shell' if action(row['text']) is not None else 'notebook')
        assert runner.model_feedback(result['feedback']) == row['visible_feedback']
        assert after['id'] == row['after_id'] == sha(stable({'entries':after['entries'],'root_mode':after['root_mode']}))
        if row['arm'] == 'original_top_p_0.9':
            assert raw['generated_token_ids'] == known['generated_token_ids']
        if row['kind'] == 'notebook' and result['feedback'] is None:
            assert notebook_bytes(after) == notebook_bytes(base) + (row['text']+'\n').encode()
            assert {x[0]:x for x in after['entries'] if x[0]!='notebook.txt'} == {x[0]:x for x in base['entries'] if x[0]!='notebook.txt'}
    assert seen == {(seed,arm) for seed in plan['seeds'] for arm in plan['arms']}
    summary = {}
    for arm in plan['arms']:
        rows = [r for r in done['results'] if r['arm'] == arm]
        summary[arm] = {'trials':len(rows),'distinct_texts':len({r['text'] for r in rows}),
            'exact_baseline_repeats':sum(r['same_text_as_baseline'] for r in rows),
            'shell_calls':sum(r['kind']=='shell' for r in rows),
            'notebook_replies':sum(r['kind']=='notebook' for r in rows),
            'visible_errors_or_receipts':sum(r['visible_feedback'] is not None for r in rows),
            'non_notebook_state_changes':sum(bool(r['non_notebook_changed_paths']) for r in rows),
            'stops':dict(collections.Counter(r['stop'] for r in rows)),
            'forms':dict(collections.Counter(r['text'] for r in rows))}
    save('SUMMARY.json',{'canonical_paused_at':1550,'arms':summary,'results':done['results'],
        'observer_model_calls':0,'source_trace_repeat_probability':plan['prior_trace_prediction'],
        'no_feedback_followup_trials':True})
    verification = {'status':'pass','observer_model_calls':0,'external_generation_calls_verified':8,
        'four_matched_seed_pairs':True,'all_inputs_equal':True,'same_initial_checkpoint':True,
        'tokenization_and_decoding':True,'exact_original_control_outputs':True,
        'exact_nucleus_only_source_difference':True,'object_hashes_verified':True,
        'notebook_effects_reconstructed_when_applicable':True,
        'canonical_inventory_unchanged':True,'canonical_files_checked':len(canonical),
        'paused_at':1550,'training_updates':0,
        'scope':'Retained-evidence verification with pinned tokenizer and shared checkpoint format. Does not independently re-run neural inference or implement a second filesystem simulator.'}
    save('VERIFICATION.json',verification)
    table = '\n'.join(f"| {arm} | {x['trials']} | {x['exact_baseline_repeats']} | {x['distinct_texts']} | {x['shell_calls']} | {x['non_notebook_state_changes']} |" for arm,x in summary.items())
    examples = '\n\n'.join(f"Seed {r['seed']}, {r['arm']}, {r['stop']}:\n\n```text\n{r['text']}\n```" for r in done['results'])
    base_metrics = summary['original_top_p_0.9']
    alt_metrics = summary['nucleus_filter_removed']
    different = 4-alt_metrics['exact_baseline_repeats']
    report = f'''# Detached sampler comparison: four matched seed pairs

9 November 2026 UTC. Canonical garden remains paused at **1550**, with all {len(canonical)} canonical phase files unchanged. This study is a separate diagnostic condition, not entries 1551–1554 or a continuation of the garden.

## Question and design

Does removing nucleus filtering alone change the generated reply or produce tool use on the exact repeated input?

The plan was saved before inference. Seeds {plan['seeds']} were selected by evaluating the frozen entry-seed rule at 1551–1554, without inspecting outcomes. There were eight independent one-step trials: each seed paired an original top-p 0.9 control with an unfiltered condition. Each trial started from the same entry-1550 checkpoint and identical 756-token input. No result from one trial entered another trial's input or world.

The original generator ran unchanged for controls. The alternative copied that generator and removed only the line applying the nucleus mask, plus output metadata declaring top_p null. See SAMPLER_CHANGE.diff. Temperature 0.8, float32 CPU eager inference, two threads, fixed model/tokenizer, sorting, RNG mechanism, fresh KV, 96-token output limit, seed wording, twelve-reply replay, directory observation, action parser and world limits stayed the same. There were no prompts, demonstrations, rewards, new tasks, adapters or training updates.

## Observations

| Arm | Trials | Exact baseline repeats | Distinct texts | Shell actions | Non-notebook state changes |
| --- | --- | --- | --- | --- | --- |
{table}

The unfiltered condition produced **{different} of 4** replies different from the exact baseline. Full forms, token IDs, messages, stop reasons, receipts and snapshots are retained, including repeated results. Source text is writing unless the unchanged parser recognizes the whole-reply action envelope; nothing was repaired or extracted for execution.

Every generated reply was dispatched through receive() on its own fresh disposable restoration. Resulting state was captured and independently restored using the pinned checkpoint decoder. Notebook appends were also reconstructed directly from retained bytes where no storage fault occurred. Model-facing feedback from these trials was not supplied to the canonical garden. There are no second-turn trials here: if a receipt occurred, this design does not measure how the model would respond to it.

## Interpretation and scope

The preceding audit established singleton support under top-p 0.9 on all 32 tokens of the baseline path. Removing the mask gives alternatives nonzero probability where the full float32 softmax supports them. It does not flatten the distribution, remove replay, or change the directory cue.

Before the new trials, the retained trace predicted the exact listing with probability approximately {plan['prior_trace_prediction']['full_softmax_probability_of_exact_baseline_path']:.6f} under unfiltered sampling on this input. Under an ideal independent-draw interpretation, the chance of all four repeating is approximately {plan['prior_trace_prediction']['probability_all_four_repeat_if_independent_draws']:.6f}. These are calculations from earlier probabilities; the deterministic PRNG seeds are not a proof of statistical independence. Repetition across four trials would therefore be unsurprising and would not refute restored alternative support.

This small comparison describes one-step behavior for one highly repetitive context. Variety alone is not learning, grounding or improvement. A missing action is not proof that the model cannot use tools. No conclusion about long-run trajectories, emergence, internal experience, or a better live configuration follows from four pairs.

The baseline's deterministic restriction is established by the earlier support trace; the present control calls confirm its output for the four planned seeds. This comparison does not isolate the causal contributions of replay, directory observation, model scale, or prior training. Those remain separate questions.

## Preservation and verification

Eight external generation calls; zero canonical generation calls. All planned seeds completed. Model tensor digests and frozen disk/source/runtime pins passed. Canonical file inventory, pause, lock and pending state remained unchanged. External evidence verification checked inputs, token decoding and EOS/caps, seeds, exact generator difference, parser categories, object hashes and reconstructable notebook effects. Verification made zero model calls.

The original garden remains a preserved baseline at 1550. No sampler setting or other model-facing rule was changed there. No additional trials, ablations or continuation were started automatically. The next distinct diagnostic, if pursued, is a directory-cue comparison while explicitly declaring its sampler and holding the remaining conditions fixed.

## All eight replies

{examples}

Sources: [earlier tool and sampler audit](../frozen-garden-tool-path-audit-v1/REPORT.md), [world map](../garden-state-laws-contact-map-v1/WORLD_MAP.md), PLAN.json, COMPLETED.json, SUMMARY.json and VERIFICATION.json. Earlier findings and history remain intact.
'''
    with (H / 'REPORT.md').open('x') as f:
        f.write(report)
    print(json.dumps({'verification':'pass','summary':summary,'canonical_paused_at':1550}))

if __name__ == '__main__':
    main()
