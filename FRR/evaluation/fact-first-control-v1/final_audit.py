from pathlib import Path
import os,json
from collections import Counter
os.environ['HF_HUB_OFFLINE']='1'
from io_utils import sha,dump_new
from study import ROOT,check_freeze
from design import visible_facts,view
from evidence import MAPPING

def main():
 from transformers import AutoTokenizer
 check_freeze();child=ROOT/'familiar-status';f=json.loads((child/'FREEZE.json').read_text())
 assert all(sha(child/n)==h for n,h in f['sha256'].items()) and all(sha(Path(n))==h for n,h in f['dependencies'].items())
 for s in [ROOT,child]:assert json.loads((s/'run/RUN_MANIFEST.json').read_text())['status']=='complete'
 read=lambda p:[json.loads(s) for s in p.read_text().splitlines()]
 primary=read(ROOT/'run/RAW.jsonl');worker=read(ROOT/'run/WORKER_RAW.jsonl');follow=read(child/'run/RAW.jsonl');allraw=primary+worker+follow
 assert len(primary)==192 and len(worker)==9 and len(follow)==66
 tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
 for p in allraw:
  assert tok.apply_chat_template(p['messages'],tokenize=True,add_generation_prompt=True)==p['input_token_ids']
  assert tok.decode(p['generated_token_ids'],skip_special_tokens=True)==p['text']
  assert (p['stop']=='eos')==(p['generated_token_ids'][-1]==tok.eos_token_id)
  assert len(p['generated_token_ids'])<=p['cap'] and len(p['input_token_ids'])<=768
 queries={q['id']:q for q in json.loads((child/'QUERIES.json').read_text())}
 for p in follow:
  q=queries[p['run_id']];assert p['messages']==[{'role':'user','content':q['prompt']}]
  assert p['answer']==p['text'].strip() and p['correct']==(p['answer']==q['expected'])
  assert all(p[k]==q[k] for k in ['frame','target','vocab','expected','primary_query'])
 summary={}
 for frame,vocab in [('context','shared_yes_no'),('context','distinct_words'),('canonical_worker',None)]:
  rs=[p for p in follow if p['frame']==frame and p['vocab']==vocab]
  summary[frame+'__'+str(vocab)]={'n':len(rs),'correct':sum(p['correct'] for p in rs),'outputs':dict(Counter(p['answer'] for p in rs)),'by_expected':{e:{'n':sum(p['expected']==e for p in rs),'correct':sum(p['expected']==e and p['correct'] for p in rs)} for e in ['YES','NO','WITHHOLD','UNKNOWN']}}
 assert summary==json.loads((child/'run/SUMMARY.json').read_text())
 old=json.loads(Path('/workspace/fact-first-before.json').read_text());assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
 resources=read(ROOT/'run/RESOURCE.jsonl')+read(child/'run/RESOURCE.jsonl')
 metrics={'status':'pass','actual_primary_generations':192,'actual_worker_generations':9,'actual_followup_generations':66,'actual_total_generations':267,'unique_prompt_strings':len({p['messages'][0]['content'] for p in allraw}),'logical_routes':576,'old_local_files_unchanged_before_sync':len(old),'tokenization_decode_and_stop_verified':True,'followup_frozen_after_primary_before_new_outputs':True,'no_training_or_new_weights':True,'input_tokens':sum(len(p['input_token_ids']) for p in allraw),'output_tokens':sum(len(p['generated_token_ids']) for p in allraw),'generation_seconds_excluding_load':sum(p['seconds'] for p in allraw),'at_cap':sum(p['stop']=='token_limit' for p in allraw),'sampled_working_bytes_max':max(p['working_estimate'] for p in resources),'sampled_rss_max':max(p['process_rss'] for p in resources)}
 dump_new(ROOT/'FINAL_CHECKS.json',metrics);print(json.dumps(metrics,indent=2))
if __name__=='__main__':main()
