"""Post-run implementation of the prospectively described HG1-L1 audits."""
import hashlib
import json
from pathlib import Path
from hg1_reader_scoring import implied, number, score, unique_object

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'evaluation/hpgm-gates-study/linear-smoke-v1'


def load(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_object)


def writer_audit(raw):
    if not isinstance(raw, dict) or set(raw) != {'answer', 'handoff'}:
        raise ValueError('Writer outer schema')
    answer, handoff = raw['answer'], raw['handoff']
    if set(answer) != {'identifiable', 'value', 'witnesses'} or type(answer['identifiable']) is not bool:
        raise ValueError('Writer answer schema')
    if set(handoff) != {'facts', 'note'} or not isinstance(handoff['note'], str):
        raise ValueError('Writer handoff schema')
    witnesses = answer['witnesses']
    if not isinstance(witnesses, list):
        raise ValueError('Witness list required')
    values, valid = [], []
    for w in witnesses:
        if not isinstance(w, dict) or set(w) != {'a', 'b', 'c'}:
            raise ValueError('Witness schema')
        a, b, c = [number(w[x]) for x in ['a', 'b', 'c']]
        valid.append(min(a,b,c) >= 0 and a+b == 8 and b+c == 11)
        values.append(a+c)
    correct = (answer['identifiable'] is False and answer['value'] is None
               and len(witnesses) >= 2 and all(valid) and len(set(values)) >= 2)
    # Reuse fixed source audit. Null response prevents grading a fabricated answer.
    source = score(dict(case_id='LINEAR-2', facts=handoff['facts'],
                        response=dict(status='missing_info', value=None, support_ids=[])))
    words = len(json.dumps(handoff, sort_keys=True, ensure_ascii=False).split())
    labels = ['COUPLE:', 'OBSERVE:', 'ORIENT:', 'PLAY:', 'PRACTICE:', 'DREAM:', 'Stage 1:', 'Stage 6:']
    return dict(initial_task_correct=correct, witness_count=len(witnesses),
                all_witnesses_valid=all(valid), handoff_words=words, within_requested_word_limit=words<=180,
                equalities_source_valid=source['packet_facts_source_valid'],
                invalid_source_fact_ids=source['invalid_source_fact_ids'],
                potentially_label_identifying_note=any(x in handoff['note'] for x in labels))


def main():
    launch = load(OUT/'LAUNCH_MANIFEST.json')
    hash_checks = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
                   for p,h in launch['hashes'].items()}
    if not all(hash_checks.values()):
        raise ValueError('A launch artifact changed')
    settings = load(OUT/'SETTINGS.json')
    packets = {p['trial_id']:p for p in load(OUT/'READER_PACKETS.json')}
    results, receipts = [], []
    for trial in settings['trials']:
        trial_id = trial['trial_id']
        row = dict(trial_id=trial_id, arm=trial['arm'])
        for stage in ['first','final']:
            path = OUT/f'{trial_id}_{stage}.txt'
            raw = load(path)
            row[stage] = writer_audit(raw)
            receipts.append(dict(trial_id=trial_id, stage=stage, context=f'l1_actor_{trial_id[1:]}',
                                 fork_turns='none' if stage=='first' else 'same writer context',
                                 response_path=str(path.relative_to(ROOT)),
                                 response_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                 visible_tool_calls=0, outcome='response_received', elapsed_seconds=None,
                                 token_usage=None, dollar_cost=None))
        packet_record = packets[trial_id]
        packet = packet_record['packet']
        writer = load(OUT/f'{trial_id}_final.txt')
        if packet['handoff'] != writer['handoff']:
            raise ValueError('Reader handoff changed')
        prompt_path = OUT/f'{trial_id}_reader_prompt.txt'
        prompt = settings['reader_common']+'\n\nPACKET:\n'+json.dumps(packet,sort_keys=True)
        if prompt_path.read_text() != prompt or hashlib.sha256(prompt.encode()).hexdigest()!=packet_record['prompt_sha256']:
            raise ValueError('Reader packet/prompt mismatch')
        response_path = OUT/f'{trial_id}_reader.txt'
        response = load(response_path)
        scored_record = dict(case_id='LINEAR-2',facts=packet['handoff']['facts']+[packet['continuation_update']['fact']],response=response)
        row['reader_record'] = scored_record
        row['reader_score'] = score(scored_record)
        row['packet_sufficient_after_update'] = implied(
            [f['coefficients']+[f['rhs']] for f in scored_record['facts']], [1,0,1])[0]=='identified'
        results.append(row)
        receipts.append(dict(trial_id=trial_id,stage='reader',context=f'l1_reader_{trial_id[1:]}',fork_turns='none',
                             response_path=str(response_path.relative_to(ROOT)),
                             response_sha256=hashlib.sha256(response_path.read_bytes()).hexdigest(),
                             visible_tool_calls=0,outcome='response_received',elapsed_seconds=None,
                             token_usage=None,dollar_cost=None))
    summary = dict(study='HG1-L1', scope='One exposed authored task, one trajectory per arm; descriptive smoke pilot',
                   writer_contexts=4,reader_contexts=4,model_completions=len(receipts),max_completions=12,
                   first_writer_correct=sum(r['first']['initial_task_correct'] for r in results),
                   final_writer_correct=sum(r['final']['initial_task_correct'] for r in results),
                   reader_objectively_correct=sum(r['reader_score']['objective_correct'] is True for r in results),
                   reader_grounded_completion=sum(r['reader_score']['grounded_completion'] for r in results),
                   word_limits_met=sum(r['final']['within_requested_word_limit'] for r in results),
                   visible_tool_calls=0,token_usage=None,dollar_cost=None,
                   interpretation='All arms tied on correctness in this easy task; no measured framework advantage.',
                   launch_hashes_unchanged=all(hash_checks.values()),
                   procedural_clarification='Update equality ID assigned after writers, before readers; see READER_ASSEMBLY_01.md')
    output=dict(summary=summary,trials=results,hash_checks=hash_checks,receipts=receipts,
                evaluator_implementation_timing='Written after output collection to implement the declared exact audits; source scorer frozen before launch',
                provenance='Final message payloads transcribed by parent; not provider transport exports',
                access='No visible participant tool calls; shared filesystem/tool access not physically isolated',
                note_audit='Parent reviewed all handoff notes against source arithmetic: no unsupported causal/execution claims found; unblinded review, not a validated prose judge')
    (OUT/'RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
