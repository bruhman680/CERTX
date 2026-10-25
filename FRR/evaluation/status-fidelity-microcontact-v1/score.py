"""Tabulate manual semantic labels and verify the declared packet exposures."""
from collections import Counter
from pathlib import Path
import hashlib
import json

P=Path(__file__).resolve().parent
gold={x['id']:x['answer'] for x in json.loads((P/'GOLD.json').read_text())}
annotations=json.loads((P/'COORDINATOR_REVIEW.json').read_text())['responses']
labels={(x['reader'],x['id']):x for x in annotations}
assert len(labels)==24
packets=json.loads((P/'READER_PACKETS.json').read_text())
totals=Counter();contexts=[]
for row in packets:
    rid=row['id'];f=P/'raw'/f'{rid}.json';r=json.loads(f.read_text())
    assert [a['id'] for a in r['answers']]==list(gold)
    matches=0
    for a in r['answers']:
        assert a['answer'] in {'yes','no','unresolved'}
        assert isinstance(a['basis'],str) and a['basis']
        assert isinstance(a['evidence'],list) and a['evidence']
        match=a['answer']==gold[a['id']]
        assert match==labels[rid,a['id']]['full_source_match']
        matches+=match;totals[labels[rid,a['id']]['category']]+=1
    contexts.append({'id':rid,'access':row['access'],'matches':matches,'answers':12,'raw_json_whitespace_words':len(f.read_text().split()),'under_900_words':len(f.read_text().split())<=900})
frozen=json.loads((P/'FROZEN_HASHES.json').read_text())['files']
bad=[f for f,h in frozen.items() if hashlib.sha256((P/f).read_bytes()).hexdigest()!=h]
bindings=json.loads((P/'TRANSCRIPT_HASHES.json').read_text())
bad_transcripts=[f for f,h in bindings.items() if hashlib.sha256((P/f).read_bytes()).hexdigest()!=h]
result={'scope':'targeted coordinator-authored development contact; aggregation of semantic review, not a semantic evaluator',
        'source_words':435,'writer':json.loads((P/'WRITER_RESULT.json').read_text()),'fresh_reader_contexts':2,'participant_turns':3,'expected_packet_intake_reads':3,
        'answers_clustered':24,'full_source_matches':sum(r['matches'] for r in contexts),'semantic_categories':dict(totals),
        'contexts':contexts,'frozen_mismatches':bad,'transcript_mismatches':bad_transcripts,
        'not_identified':['policy repair','held-out generalization','causal access advantage','optimal budget','long-context durability','group reasoning benefit']}
(P/'RESULTS.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps(result,indent=2,allow_nan=False))
assert not bad and not bad_transcripts
