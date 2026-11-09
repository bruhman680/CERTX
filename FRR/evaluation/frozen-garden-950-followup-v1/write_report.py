"""External report only; no changes to the frozen controller or model inputs."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent;PHASE=H.parent/'final-garden-contract-v1';R=PHASE/'run'
def main():
 a=json.loads((H/'ANALYSIS_THROUGH_001300.json').read_text());v1=json.loads((H/'VERIFIED_000950_001050.json').read_text());v2=json.loads((H/'VERIFIED_001050_001300.json').read_text())
 assert v1['status']==v2['status']=='pass' and a['current_entry']==1300
 table='\n'.join('| '+' | '.join(str(t) for t in [r['through_entry'],r['entries'],r['kinds']['notebook'],r['kinds']['shell'],r['notebook_storage_faults'],r['eos'],r['token_cap'],r['distinct_texts']])+' |' for r in a['reports'])
 blocks='\n'.join('- Entries '+str(b['range'][0])+'–'+str(b['range'][1])+': '+str(b['entries'])+' replies; kinds '+json.dumps(b['kinds'])+'; stops '+json.dumps(b['stops'])+'; '+str(b['distinct_texts'])+' distinct texts.' for b in a['blocks'])
 before=json.loads((R/'bundles/000950.json').read_text());after=json.loads((R/'bundles/001300.json').read_text())
 files_before={x[0]:x for x in before['entries']};files_after={x[0]:x for x in after['entries']};changed=[name for name in sorted(set(files_before)|set(files_after)) if files_before.get(name)!=files_after.get(name)]
 text=f'''# Frozen garden continuation: 951–1050, then wider1051–1300

8 November2026, America/Chicago. The user's100-entry request completed at1050. Its operational stability and continuity checks passed, so the conditional first250-entry block proceeded through1300. The garden is now paused at **1300**. No further block is scheduled or authorized by this report.

## Frozen setup stayed fixed

The final design contact remains at850, committed before851 in c80de8284e31c5b93633c0e8b795cb7eb0e48dfe. The seed, model/tokenizer, action interface, world laws/resource limits, sampler, native-message rendering, twelve-reply memory policy and checkpoint code were unchanged. No hint, new tool, task material, training, adapter, or operator assessment was inserted. Earlier histories remain retained as immutable lineage parents. Continuing loaded the same pinned base weights and restored the existing world checkpoint, rather than rebuilding its contents or resetting the entry count.

Only external scheduling changed at1050: the block budget increased100→250, and the report interval widened50→100. Routine integrity checks remained every10; additional observation windows remain available for actual events without changing model inputs. All raw replies, receipts and checkpoints are retained regardless of reporting frequency.

The qualifying condition was operational: known completed calls, clean checkpoints and hash/record verification, no outstanding action, no storage problem. Repetition was not a failure, and novelty, task success or useful output was not required. The pre-run plan, first-block verification and cadence-transition record are retained separately.

## Observations

{blocks}

| Through entry | Replies in report | Notebook | Shell | Storage faults | EOS | Token cap | Distinct texts |
| --- | --- | --- | --- | --- | --- | --- | --- |
{table}

Across the350new entries, there were {a['overall']['distinct_texts']} distinct raw texts, {a['overall']['directory_list_replies']} directory-list replies and a longest adjacent exact repeat of {a['overall']['longest_exact_adjacent_repeat']}. Changed world entries from950to1300: {json.dumps(changed)}. These are descriptive observations, not scores for learning, maturity, understanding, preference or useful novelty.

The prior frozen block had already shown a narrow directory-list pattern. This continuation was left under the same model-facing conditions. Surface repetition was not repaired or redirected. EOS endings are actual model end tokens; cap endings, if any, are recorded separately. Generated filenames/spellings do not constitute actual file creation or renaming unless the world manifests show it.

The frozen controller still provides the current directory observation each turn and replays up to twelve recent raw replies in native conversation roles. Thus no new human design contact does not mean absence of recurring input. The record can describe persistence under these conditions; it does not isolate the causal contributions of the current observation, replayed writing, pretrained tendencies or sampling. This continuation is not an intervention to prove or disprove the user's developmental analogy.

## Integrity and continuity

The100-entry block had {v1['regular_checks']} routine integrity checks and {len(v1['reports'])} reports. The250-entry block had {v2['regular_checks']} routine integrity checks and {len(v2['reports'])} reports (including its final partial reporting window). All passed. Separate external verification restored each final world in a fresh namespace, verified the unchanged design/model/runtime pins and earlier stages, reconstructed exact messages/input IDs/decoded output/stops, checked retained byte objects and record chains, and confirmed a clean pause with no lock or pending action.

Direct notebook-byte reconstruction for the first block: {v1['notebook_bytes_reconstructed']}; for the second block: {v2['notebook_bytes_reconstructed']}. These observer verifiers made no model calls. In-memory learned-parameter invariance was checked by the frozen runner while the model was loaded; external verification independently checks disk hashes and retained records. Fresh filesystem reconstruction shares the pinned decoder and is not an independently implemented Linux model.

All350new model calls are counted in the continuing951–1300history. The final frozen phase now has450entries851–1300, following the older850-entry lineage. No older unknown interruption is retrospectively reconstructed or declared solved.

## Paused state and future routine

The same frozen runner can resume from1300 only for another user-authorized budget. It supports bounded steps up to250 and external report intervals50/100. Use checks10 initially and narrower external inspection on action/error/unexpected-state events; quiet or repetitive writing does not require intervention. The wider cadence has now been exercised, not merely proposed. No new seed or universe redesign is part of ordinary continuation.

Known boundaries remain as declared in the contract: finite input capacity with no silent truncation, supported filesystem-state reconstruction rather than process/KV/timestamp persistence, and explicit pauses for integrity/uncertain-effect or unsupported-state faults. The data-block quota is not a bound on all kernel metadata. The freeze is operator-controlled and hash-checked, not a guarantee that external cloud infrastructure never changes.

Garden view: the extra100entries kept the same ground, then the observation window widened for250more. We kept the full trail while stepping back from frequent reports. What repeated was retained; nothing was required to become a different kind of plant.
'''
 with (H/'REPORT.md').open('x') as f:f.write(text)
 print('External report written through1300')
if __name__=='__main__':main()
