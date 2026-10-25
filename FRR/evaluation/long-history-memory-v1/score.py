"""Tabulate reviewed answers; do not mistake schema checks for semantic evaluation."""
from collections import Counter
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent
gold = {x['id']: x['answer'] for x in json.loads((P/'GOLD.json').read_text())}
manual = json.loads((P/'COORDINATOR_SEMANTIC_REVIEW.json').read_text())
ann = {(x['reader'], x['stage'], x['question']): x for x in manual['rows']}
assert len(ann) == 64
contexts = json.loads((P/'READER_PACKETS.json').read_text())
second = {x['id']: x for x in json.loads((P/'SECOND_PACKETS.json').read_text())}
categories = {'FIRST': Counter(), 'FINAL': Counter()}
known = {'FIRST': 0, 'FINAL': 0}
rows = []
for c in contexts:
    rid = c['id']
    first = json.loads((P/'raw'/f'{rid}_FIRST.json').read_text())
    final = json.loads((P/'raw'/f'{rid}_FINAL.json').read_text())
    assert type(first['request_original']) is bool
    s = second[rid]
    assert s['delivered_original'] == (c['access'] == 'original' and first['request_original'])
    turns = {}
    for stage, data in [('FIRST', first), ('FINAL', final)]:
        assert [a['id'] for a in data['answers']] == list(gold)
        matches = 0
        for a in data['answers']:
            assert a['answer'] in {'yes','no','unresolved'}
            assert isinstance(a['basis'], str) and a['basis']
            assert isinstance(a['evidence'], list) and a['evidence']
            label = ann[rid, stage, a['id']]
            match = a['answer'] == gold[a['id']]
            assert match == label['full_source_match']
            matches += match
            categories[stage][label['category']] += 1
        known[stage] += matches
        words = len((P/'raw'/f'{rid}_{stage}.json').read_text().split())
        turns[stage] = {'known_task_matches': matches, 'answers':8, 'raw_json_whitespace_words':words, 'under_700_words':words<=700}
    changes = [a['id'] for a,b in zip(first['answers'],final['answers']) if a['answer'] != b['answer']]
    rows.append({'reader':rid,'writer':c['writer'],'access':c['access'],'requested_original':first['request_original'],'delivered_original':s['delivered_original'],'answer_label_changes':changes,'turns':turns})

frozen = json.loads((P/'FROZEN_HASHES.json').read_text())['files']
freeze_mismatches = [f for f,h in frozen.items() if hashlib.sha256((P/f).read_bytes()).hexdigest()!=h]
bindings = json.loads((P/'TRANSCRIPT_HASHES.json').read_text())
transcript_mismatches = [f for f,h in bindings.items() if hashlib.sha256((P/f).read_bytes()).hexdigest()!=h]
result = {'scope':'authored single-handoff/longer-input contact; schema/count aggregation of separately reviewed semantic labels',
          'source_words':3064,'source_records':60,'writers':2,'fresh_reader_contexts':4,
          'participant_turns':10,'expected_packet_intake_reads':10,'intake_policy':'one exact file read per turn; instructional restriction, no complete telemetry or attention guarantee',
          'final_answers_clustered':32,'known_task_matches':known,'semantic_categories':{k:dict(v) for k,v in categories.items()},
          'original_requests':sum(x['requested_original'] for x in rows),'original_deliveries':sum(x['delivered_original'] for x in rows),
          'label_changes':sum(len(x['answer_label_changes']) for x in rows),
          'writer_outputs':json.loads((P/'WRITER_OUTPUTS.json').read_text()),'contexts':rows,
          'frozen_mismatches':freeze_mismatches,'transcript_mismatches':transcript_mismatches,
          'not_identified':['causal word-budget effect','causal access effect','compression-loss recovery','natural source authentication','index-search efficacy','FRR advantage','longitudinal durability']}
(P/'RESULTS.json').write_text(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False))
assert not freeze_mismatches and not transcript_mismatches
