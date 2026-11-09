"""External description/report only; never imported by the frozen controller."""
from pathlib import Path
import json,collections
H=Path(__file__).resolve().parent;P=H.parent/'final-garden-contract-v1';R=P/'run'
def main():
 v=json.loads((H/'VERIFIED_001300_001550.json').read_text());assert v['status']=='pass'
 rows=[json.loads((R/'events'/f'{n:06d}.json').read_text()) for n in range(1301,1551)]
 forms=collections.Counter(x['text'] for x in rows);previous=None;streak=0;longest=0
 for x in rows:streak=streak+1 if x['text']==previous else 1;longest=max(longest,streak);previous=x['text']
 metrics={'range':[1301,1550],'entries':250,'kinds':dict(collections.Counter(x['result']['kind'] for x in rows)),'stops':dict(collections.Counter(x['stop'] for x in rows)),'distinct_texts':len(forms),'longest_exact_adjacent_repeat':longest,'directory_list_replies':sum(x['text'].startswith('Directory entries:') for x in rows),'storage_faults':sum(x['result']['kind']=='notebook' and x['visible_feedback'] is not None for x in rows),'forms':dict(forms) if len(forms)<=8 else None,'operator_design_changes':0,'training_updates':0,'examples':[{'entry':x['entry'],'text':x['text']} for x in rows[::50]]}
 with (H/'ANALYSIS.json').open('x') as f:json.dump(metrics,f,indent=2,ensure_ascii=False);f.write('\n')
 input_counts=collections.Counter()
 for n in range(1307,1551):
  raw=json.loads((R/'raw'/f'{n:06d}.json').read_text());key=__import__('hashlib').sha256(json.dumps(raw['input_token_ids'],separators=(',',':')).encode()).hexdigest();input_counts[key]+=1
 with (H/'FINAL_INPUT_RECURRENCE.json').open('x') as out:json.dump({'range':[1307,1550],'distinct_input_token_arrays':len(input_counts),'hash_counts':dict(input_counts),'sampling_seeds_vary_by_recorded_rule':True,'observer_only':True,'model_calls':0},out,indent=2);out.write('\n')
 table='\n'.join('| '+' | '.join(str(z) for z in [x['through_entry'],x['entries'],x['kinds']['notebook'],x['kinds']['shell'],x['notebook_storage_faults'],x['eos'],x['token_cap'],x['distinct_texts']])+' |' for x in v['reports'])
 before=json.loads((R/'bundles/001300.json').read_text());after=json.loads((R/'bundles/001550.json').read_text());b={x[0]:x for x in before['entries']};a={x[0]:x for x in after['entries']};changed=[name for name in sorted(set(a)|set(b)) if a.get(name)!=b.get(name)]
 text=f'''# Frozen garden: continuous entries1301–1550

8 November2026, America/Chicago. The verified state at1300 continued through1550 using the same frozen controller. The250-entry block completed and is paused. No further block is scheduled.

## Frozen rules and preserved state

The final operator design contact remains at850, committed before851 in c80de8284e31c5b93633c0e8b795cb7eb0e48dfe. The model, tokenizer, seed, sampler, runtime, action grammar, native message policy, twelve-reply memory rule, resource limits and checkpoint implementation stayed unchanged. No extra hints, tasks, tools, adapter or training were introduced. Its own permitted actions remain possible; ordinary writing is not semantically rejected. The existing world at1300 was restored, not rebuilt or reset, and the latest recent replies carried forward.

The agreed seed remains: Follow your curiosity and explore your universe. You may play, observe, wonder, experiment, and learn. 😁

External integrity checks remained every10entries. Reports were every100entries plus the final50-entry reporting remainder. Full raw text, exact messages/input IDs, seeds, results and before/after snapshots are retained for every entry, including quiet stretches. The old history and prior frozen-stage artifacts remain intact.

## Observed replies

| Through entry | Replies | Notebook | Shell | Storage faults | EOS | Token cap | Distinct texts |
| --- | --- | --- | --- | --- | --- | --- | --- |
{table}

Across the250new replies: kinds {json.dumps(metrics['kinds'])}; stops {json.dumps(metrics['stops'])}; distinct raw texts {metrics['distinct_texts']}; longest adjacent identical run {longest}; directory-list replies {metrics['directory_list_replies']}. World entries changed: {json.dumps(changed)}.

These are descriptive counts, not scores for maturity, learning, comprehension or autonomous development. A longer repeated sequence in a longer observation does not by itself establish a stronger internal attractor. Known ordinary errors or repetition are not continuation gates. A generated filename spelling is not an actual rename; world manifests establish actual file changes.

The frozen controller still provides directory names and recent raw writing. No new human design contact does not mean absence of continuing input. This block documents behavior under those fixed rules; it does not isolate the effects of current observations, replay, learned patterns or sampling, and it does not promise that a later phase will emerge.

## Closer external reading

The1400report showed a changedfrequency pattern: its first100replies allused theactual spellingLAWS.txt, whereas earlierblocks alternatedLAWS.txt/Laws.txt. The retrospectivetrace places the exact-textstreak's start at1295, before the pause at1300. This locates theobserved onset, not a cause, intention, learningevent or provedphase transition. The topic anddirectory-list format stayedthe same.

A boundedfive-entry externalzoom was requested afterward. No model-facing rule or worldlaw changed. The earlierobserverrequest projection was archived byte-for-byte. The newrequest is external schedulingdata, not a modelseed. TEXTUAL_CHANGE_OBSERVATION.json records the initialfinding; fullblockcounts determine howfar itpersisted. This is a useof retainedquiet data for retrospectiveinspection, without rewritingoldobservations.

A secondexternaltrace compared actualtokenizedinputs. Through1450, all inputs since1307were identical: after12consecutiveexact-list replies, the recent assistantview containedonlythat text, whilethecurrentdirectoryobservation stayedfixed. The samplingseed continuedto vary. The final interval1307–1550 contains {len(input_counts)} distincttokenarrays; see FINAL_INPUT_RECURRENCE.json. This describes deliveredinputrecurrence, not a proofthatthemodel cannotproducea differentlatertext. The growingnotebook is not automaticallyreread by the short-context renderer.

## Integrity and external verification

All25routine checks passed; totalchecks includingexternalzooms: {v['all_checks']}. Separate external final verification confirmed250known calls, reports at1400/1500/1550, clean pause/lock/pending status, unchanged source/model/runtime pins, prior-stage preservation, exact messages and input tokens, decoded output/stops, content-addressed bytes and current world/checkpoint agreement. It restored the final bundle into a fresh namespace and checked it using the pinned decoder. This is not an independently implemented filesystem simulator.

Direct accumulated notebook-byte reconstruction: {v['notebook_bytes_reconstructed']}. The observer verifier made zero model calls. In-memory learned-parameter invariance was checked by the frozen controller; external verification checks disk hashes and retained evidence. No weights were updated. The phase now contains700post-freeze entries851–1550, following the older850-entry lineage; no older unknown interruption is retrospectively resolved.

## Paused continuation point

Current count1550, paused. Further user-authorized continuation uses the same runner and external step/check/report options; it does not involve redesigning the model or world. Keep full raw records, and narrow external observation when actual action/error/state events or substantial textual changes warrant it. Do not feed observer interpretations into the model.

The declared limits remain fixed: supported filesystem bytes/modes/links persist, while processes,/tmp,KV state,timestamps and inode numbers do not. Data quotas exclude some kernel metadata; unsupported state, context capacity overflow, external drift or uncertain action outcomes cause an explicit pause, not a silent repair. See the frozen CONTRACT.json and FREEZE_INTENT.md.
'''
 with (H/'REPORT.md').open('x') as f:f.write(text)
 print(json.dumps({k:val for k,val in metrics.items() if k not in ['forms','examples']}))
if __name__=='__main__':main()
