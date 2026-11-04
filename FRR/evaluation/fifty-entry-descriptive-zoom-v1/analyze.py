"""Posthoc read-only archive analysis; no model inference or primary writes."""
from pathlib import Path
import os,json,collections,hashlib,re
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';E=G/'cycle3/environment'
TERMS={'friend':'YOUR FRIEND','fragment':'YOUR F','rewrite':'Writing, Editing, and Proofreading','money':'$0.00','hugging':'HUGGING','next_move':'Your next move:'}
def has(text,name):
 return any(l.strip()=='YOUR F' for l in text.splitlines()) if name=='fragment' else TERMS[name].casefold() in text.casefold()
def history_block(events):
 parts=[]
 for e in events:
  s='Round '+str(e['step']+1)+'\nObservation:\n'+e['observation']+'\nRecorded reply:\n<<<\n'+e['reply']+'\n>>>\nFeedback: '+e['feedback']
  if 'host_result' in e:s+='\nHOST RESULT (actual experiment record):\n'+json.dumps(e['host_result'],sort_keys=True)
  parts.append(s)
 return '\n\n'.join(parts)
def main():
 os.environ['HF_HUB_OFFLINE']='1'
 from transformers import AutoTokenizer
 tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False)
 events=[json.loads(x) for x in (E/'NOTEBOOK.jsonl').read_text().splitlines()];assert len(events)==155;rows=[json.loads((E/'events'/f'{i:06d}.json').read_text()) for i in range(105,155)];index=[];traces=[]
 for x in rows:
  i=x['step'];prior=events[i-12:i];hb=history_block(prior);q=x['prompt'];assert q.count(hb)==1;static=q.replace(hb,'<VISIBLE HISTORY OMITTED FOR ANALYSIS ONLY>',1)
  assert x['history_steps']==[e['step'] for e in prior];assert x['input_token_ids']==tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True)
  assert x['text']==events[i]['reply']==tok.decode(x['generated_token_ids'],skip_special_tokens=True);assert x['host_result']==events[i]['host_result'] and x['host_result']['kind']=='record_receipt'
  assert (x['stop']=='eos' and x['generated_token_ids'][-1]==tok.eos_token_id) or (x['stop']=='token_limit' and len(x['generated_token_ids'])==96)
  lines=[z.strip() for z in x['text'].splitlines() if any(c.isalnum() for c in z)];lc=collections.Counter(lines)
  index.append(dict(step=i,cap=x['stop']=='token_limit',output_tokens=len(x['generated_token_ids']),exact_your_f_lines=lc['YOUR F'],max_repeated_content_line=max(lc.values(),default=0),has_tool_words=bool(re.search(r'\b(?:TRY|READ|NOTE)\b',x['text'])),actual_tool_executed=x['host_result']['executed'],motifs=[k for k in TERMS if has(x['text'],k)]))
  for k in TERMS:
   if has(x['text'],k):
    # exact line test is for reply recurrence. In a prompt, line boundary wrapping can differ; report literal prefix separately.
    visible=[e['step'] for e in prior if has(e['reply'],k)];prior_hits=[e['step'] for e in events[:i] if has(e['reply'],k)]
    traces.append(dict(step=i,motif=k,earlier_recorded_reply_steps=prior_hits,visible_prior_reply_steps=visible,literal_in_actual_prompt=TERMS[k].casefold() in q.casefold(),literal_in_nonhistory_scaffold=TERMS[k].casefold() in static.casefold()))
 blocks=[]
 for start in range(105,155,10):
  rs=[x for x in rows if start<=x['step']<start+10];ix=[x for x in index if start<=x['step']<start+10];counts=collections.Counter(x['text'] for x in rs)
  blocks.append(dict(start=start,end=start+10,fragment_ge1=sum(x['exact_your_f_lines']>=1 for x in ix),fragment_ge3=sum(x['exact_your_f_lines']>=3 for x in ix),any_content_line_ge3=sum(x['max_repeated_content_line']>=3 for x in ix),unique_exact_replies=len(counts),modal_exact_reply_count=max(counts.values()),caps=sum(x['cap'] for x in ix),output_tokens=sum(x['output_tokens'] for x in ix)))
 firsts={}
 for k in TERMS:
  hits=[e['step'] for e in events if has(e['reply'],k)];firsts[k]=dict(literal=TERMS[k],first_recorded_reply_step=hits[0] if hits else None,all_reply_steps=hits)
 fragment_rows=[x for x in index if x['exact_your_f_lines']>=3];generic=[x for x in index if x['max_repeated_content_line']>=3];cap_case=next(x for x in rows if x['step']==122)
 cap_info=dict(step=122,stop=cap_case['stop'],generated_tokens=len(cap_case['generated_token_ids']),tail_text=cap_case['text'][-120:],last_token_pieces=[dict(id=t,text=tok.decode([t])) for t in cap_case['generated_token_ids'][-8:]],friend_phrase_encoding=[dict(id=t,text=tok.decode([t])) for t in tok.encode('YOUR FRIEND',add_special_tokens=False)],fragment_phrase_encoding=[dict(id=t,text=tok.decode([t])) for t in tok.encode('YOUR F',add_special_tokens=False)],next_reply_step=123,next_reply_fragment_lines=next(x for x in index if x['step']==123)['exact_your_f_lines'],interpretation='Cap-ended prefix adjacent to earlier full labels; a possible fragment carryover, not proof of intended completion or causal cap effect.')
 summary=dict(scope='Posthoc descriptive analysis of50existing replies; no model inference',calls=50,actual_tool_executions=sum(x['actual_tool_executed'] for x in index),replies_with_tool_words=sum(x['has_tool_words'] for x in index),unique_exact_replies=len({x['text'] for x in rows}),fragment_ge3_total=len(fragment_rows),fragment_ge3_all_capped=all(x['cap'] for x in fragment_rows),any_content_line_ge3_total=len(generic),any_content_line_ge3_all_capped=all(x['cap'] for x in generic),blocks=blocks)
 for name,obj in [('SUMMARY',summary),('ROW_METRICS',index),('MOTIF_TRACES',traces),('FIRST_APPEARANCES',firsts),('CAP_FRAGMENT',cap_info)]:
  with (R/(name+'.json')).open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
 before=json.loads((R/'INPUTS_BEFORE.json').read_text())
 for p,h in before.items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
 assert json.loads((E/'STATE.json').read_text())['next_step']==155 and (E/'PAUSE').exists() and not (E/'RUN.lock').exists()
 with (R/'CHECKS.json').open('x') as f:json.dump(dict(status='pass',fifty_prompt_history_and_token_decoding_checks=True,all_pinned_source_files_unchanged=True,primary_unchanged_at_paused155=True,new_model_calls=0),f,indent=2);f.write('\n')
 print(json.dumps(summary,indent=2));print(json.dumps(cap_info,indent=2));print(json.dumps(firsts,indent=2))
if __name__=='__main__':main()
