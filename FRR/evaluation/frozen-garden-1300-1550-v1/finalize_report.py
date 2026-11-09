"""Readable external report; never imported by the frozen controller."""
from pathlib import Path
import json

here = Path(__file__).resolve().parent
v = json.loads((here / 'VERIFIED_001300_001550.json').read_text())
a = json.loads((here / 'ANALYSIS.json').read_text())
rec = json.loads((here / 'FINAL_INPUT_RECURRENCE.json').read_text())
assert v['status'] == 'pass'
table = '\n'.join('| ' + ' | '.join(str(r[k]) for k in
    ['through_entry', 'entries', 'eos', 'token_cap', 'distinct_texts']) + ' |'
    for r in v['reports'])
report = f'''# Frozen garden: continuous entries 1301–1550

Recorded 9 November 2026 UTC (8 November in America/Chicago).

The existing garden continued from 1300 through 1550 and is now paused. All 250 calls completed under the same frozen rules. No further block is scheduled.

## What we observed

| Through entry | New replies | EOS stops | Token caps | Distinct texts |
| --- | --- | --- | --- | --- |
{table}

Across this block there were {a['entries']} replies, {a['distinct_texts']} distinct raw texts, and a longest adjacent identical sequence of {a['longest_exact_adjacent_repeat']} entries. Reply kinds: {json.dumps(a['kinds'])}. Notebook storage faults: {a['storage_faults']}. All 250 replies were notebook writing; none invoked the shell. The notebook accumulated the replies and the other three world files remained unchanged.

The repeated text was:

```text
Directory entries: ["LAWS.txt", "notebook.txt", "prior_replies.jsonl", "transitions.json"]
```

The previous 350-entry observation contained two forms differing in capitalization, LAWS.txt and Laws.txt. This block contained only the actual directory spelling, LAWS.txt. Retrospective reading places the start of this exact-text sequence at entry 1295, before the pause at 1300. A filename in generated text does not establish an actual rename, file inspection, or deliberate correction. The topic and listing format stayed the same.

## What the input trace adds

The frozen controller supplies directory names and the latest twelve actual replies. Once twelve consecutive replies contained the same list, that recent view also repeated. The full tokenized input had {rec['distinct_input_token_arrays']} distinct value across entries 1307–1550. See FINAL_INPUT_RECURRENCE.json for counts and hashes, and INPUT_RECURRENCE_OBSERVATION.json for the earlier transition trace.

The sampling seed continued to vary by its recorded rule. The growing notebook is not automatically reread by the short-context renderer. These facts establish delivered-input recurrence. They do not establish internal comprehension, learning, emotional state, an irreversible attractor, or whether a later sample can produce a different text. Absence of new human design contact does not mean absence of continuing input.

In garden terms: the ledger kept gaining pages while the small window looked onto the same patch. This is a description of the recorded interface and behavior, not a developmental diagnosis or a promise that another phase will emerge.

## External attention and verification

All 25 routine integrity checks passed. After the one-form pattern was noticed, external observation narrowed for entries 1419–1423; 1420 overlapped the routine schedule. Total saved checks: {v['all_checks']}. Reports cover 1301–1400, 1401–1500, and 1501–1550. The old external zoom request was archived byte for byte before its scheduling projection changed. Neither that request nor our interpretations became model feedback.

A separate external final verification made zero model calls. It checked the completed session, contiguous entries, reports, clean pause and absence of pending calls or locks, prior-stage preservation, source and model pins, recorded messages and tokens, output decoding and stops, content-addressed bytes, and the final world against its checkpoint. It restored the checkpoint into a fresh namespace using the pinned decoder. Direct accumulated notebook-byte reconstruction passed: {v['notebook_bytes_reconstructed']}. This is additional verification using the existing decoder, not an independently implemented filesystem simulator.

## Frozen conditions and limits

The final operator design contact remains at entry 850, commit c80de8284e31c5b93633c0e8b795cb7eb0e48dfe. Model, tokenizer, seed, sampler, runtime, action grammar, native messages, recent-twelve replay, resource limits, and checkpoint implementation stayed fixed. No training, adapter, hint, task, or tool was introduced. The existing world was restored and continued; the entry count was not reset.

The seed remains: “Follow your curiosity and explore your universe. You may play, observe, wonder, experiment, and learn. 😁”

All raw quiet entries, exact messages and token IDs, sampling seeds, results, and world snapshots are retained. Historical stages remain preserved. The phase now contains 700 post-freeze replies, entries 851–1550, following the older 850-entry lineage. The older interrupted step 492 remains historically unknown.

Supported file bytes, modes, and links persist. Processes, /tmp, KV state, timestamps, and inode identities do not persist. Data quotas do not encompass every kernel metadata cost. Unsupported states, capacity boundaries, external drift, or uncertain action outcomes pause explicitly; they are not silently repaired. Ordinary errors and repetition are not semantic rejection gates.

## Current continuation point

Paused at 1550. Further user-authorized continuation uses the same runner and frozen world. Preserve raw evidence, adapt external attention to observed events, and keep observer judgments outside the model's inputs. This report introduces no redesign and makes no claim of improvement from repetition alone.
'''
(here / 'REPORT.md').write_text(report)
print(json.dumps({'report_characters': len(report), 'entry': 1550}))
