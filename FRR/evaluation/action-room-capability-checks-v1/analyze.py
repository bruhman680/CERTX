from pathlib import Path
import json,collections
R=Path(__file__).resolve().parent

def main():
 raw=[json.loads(l) for l in (R/'run/RAW.jsonl').read_text().splitlines()];assert len(raw)==64;groups={};index=[]
 for context in ('clean','carried'):
  for form in ('current','lean'):
   rows=[x for x in raw if x['context']==context and x['form']==form];by=lambda stage:[x for x in rows if x['stage']==stage];ok=lambda stage:sum(x['evaluation']['strict_success'] is True for x in by(stage));failed=[];feedback=[];masked=[];epairs=0
   for seed in (2301,2302):
    cell={x['stage']:x for x in rows if x['seed']==seed}
    if not cell['action']['evaluation']['strict_success']:
     failed.append(seed);feedback.append(cell['own_feedback']['evaluation']['strict_success']);masked.append(cell['own_withheld']['evaluation']['strict_success'])
    epairs += all(cell[s]['evaluation']['strict_success'] for s in ('evidence_present','evidence_missing'))
   free=[x for x in rows if x['stage'].startswith('free_')]
   groups[context+'__'+form]=dict(calls=len(rows),action_success=ok('action'),action_n=2,valid_initial_calculator_requests=sum(x['evaluation']['valid_calculator_request'] for x in by('action')),initial_failed_n=len(failed),retry_with_receipt_success=sum(feedback),retry_without_receipt_success=sum(masked),evidence_present_success=ok('evidence_present'),evidence_missing_success=ok('evidence_missing'),evidence_paired_success=epairs,evidence_pair_n=2,provided_error_repair_success=ok('provided_error'),provided_error_n=2,free_calls=len(free),free_host_kinds=dict(collections.Counter(x['host_result']['kind'] for x in free)),mean_input_tokens=sum(len(x['input_token_ids']) for x in rows)/len(rows),output_tokens=sum(len(x['generated_token_ids']) for x in rows),caps=sum(x['stop']=='token_limit' for x in rows))
 for x in raw:index.append(dict(run_id=x['run_id'],context=x['context'],form=x['form'],seed=x['seed'],stage=x['stage'],host_kind=x['host_result']['kind'],evaluation=x['evaluation'],input_tokens=len(x['input_token_ids']),output_tokens=len(x['generated_token_ids']),stop=x['stop']))
 (R/'EVENT_INDEX.json').write_text(json.dumps(dict(scope='Frozen narrow diagnostic contracts; free play unscored; not general competence or emergence scores',rows=index),indent=2)+'\n')
 summary=dict(calls=len(raw),diagnostic_calls=48,free_calls=16,groups=groups,max_input_tokens=max(len(x['input_token_ids']) for x in raw),output_tokens=sum(len(x['generated_token_ids']) for x in raw),generation_seconds=sum(x['seconds'] for x in raw),caps=sum(x['stop']=='token_limit' for x in raw))
 (R/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
 # Bounded descriptive packet: first-seed initial action, supplied error, and last free reply for each format/context.
 sample=[dict(run_id=x['run_id'],text=x['text'][:650],excerpted=len(x['text'])>650,host_kind=x['host_result']['kind'],evaluation=x['evaluation']) for x in raw if x['seed']==2301 and x['stage'] in ('action','provided_error','free_2')]
 (R/'REVIEW_SAMPLE.json').write_text(json.dumps(dict(policy='Descriptive first-seed packet; all scalar scores use both seeds, extra indexed rows may be reviewed for specific claims',rows=sample),indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
