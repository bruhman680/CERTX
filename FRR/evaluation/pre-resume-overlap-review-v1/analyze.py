"""Read-only runtime/pin audit and lexical input-overlap description. No model inference."""
from pathlib import Path
import os,sys,json,re,hashlib,statistics
R=Path(__file__).resolve().parent;ROOT=R.parent.parent;G=ROOT/'evaluation/source-access-three-cycle-v1';E=G/'cycle3/environment';sys.path.insert(0,str(G));import fundamental_routine as f
N=5
def words(t):return re.findall(r"\w+(?:['’]\w+)?",t.casefold())
def grams(ts):return {tuple(ts[i:i+N]) for i in range(max(0,len(ts)-N+1))}
def covered(ts,gs):
 if len(ts)<N:return None
 hit=set()
 for i in range(len(ts)-N+1):
  if tuple(ts[i:i+N]) in gs:hit.update(range(i,i+N))
 return len(hit)
def canonical(t):return ' '.join(t.casefold().split())
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
 f.freeze_check();state=json.loads((E/'STATE.json').read_text());latest=json.loads((G/'cycle3/CURRENT_VERIFY.json').read_text());assert state['next_step']==latest['next_step']==305 and latest['verification']=='0054' and (E/'PAUSE').exists() and not (E/'RUN.lock').exists();assert json.loads((G/'cycle3'/latest['checks']).read_text())['status']=='pass';assert state['manifest_sha256']==f.sha(E/f.NEW_MANIFEST)
 manifest=json.loads((E/f.NEW_MANIFEST).read_text());assert f.sha(f.parent.BASE/'model.safetensors')==manifest['model_base_pin']['weights_sha256'];assert f.sha(f.parent.ACQ/'final/adapter.safetensors')==manifest['adapter_sha256']
 tok=AutoTokenizer.from_pretrained(f.parent.BASE,local_files_only=True,trust_remote_code=False);events=[json.loads(x) for x in (E/'NOTEBOOK.jsonl').read_text().splitlines()];assert len(events)==305;out=[]
 for step in range(205,305):
  x=json.loads((E/'events'/f'{step:06d}.json').read_text());q=x['prompt'];es=events[:step];assert q==f.fundamental_view_render(es);assert x['history_steps']==list(range(step-12,step));assert x['host_result']==f.view_dispatch(x['text'],es);assert x['input_token_ids']==tok.apply_chat_template([{'role':'user','content':q}],tokenize=True,add_generation_prompt=True);assert x['text']==tok.decode(x['generated_token_ids'],skip_special_tokens=True)
  assert (x['stop']=='eos' and x['generated_token_ids'][-1]==tok.eos_token_id) or (x['stop']=='token_limit' and len(x['generated_token_ids'])==96)
  hb=history_block(es[-12:]);assert q.count(hb)==1;pos=q.index(hb);static_grams=grams(words(q[:pos]))|grams(words(q[pos+len(hb):]));prior_grams=set()
  for e in es[-12:]:prior_grams|=grams(words(e['reply']))
  ts=words(x['text']);a=covered(ts,grams(words(q)));b=covered(ts,static_grams);c=covered(ts,prior_grams);norm=canonical(x['text']);exact=bool(norm) and norm in canonical(q)
  out.append(dict(step=step,stop=x['stop'],output_model_tokens=len(x['generated_token_ids']),lexical_words=len(ts),eligible=len(ts)>=N,input_covered_words=a,scaffold_covered_words=b,visible_prior_reply_covered_words=c,input_coverage=None if a is None else a/len(ts),normalized_reply_is_input_substring=exact,host_kind=x['host_result']['kind']))
 def group(xs):
  eligible=[x for x in xs if x['eligible']];den=sum(x['lexical_words'] for x in eligible)
  return dict(replies=len(xs),eligible_replies=len(eligible),short_replies=len(xs)-len(eligible),eligible_lexical_words=den,input_word_coverage=None if not den else sum(x['input_covered_words'] for x in eligible)/den,scaffold_word_coverage=None if not den else sum(x['scaffold_covered_words'] for x in eligible)/den,visible_reply_word_coverage=None if not den else sum(x['visible_prior_reply_covered_words'] for x in eligible)/den,median_eligible_reply_input_coverage=statistics.median(x['input_coverage'] for x in eligible) if eligible else None,eligible_replies_coverage_ge_80pct=sum(x['input_coverage']>=.8 for x in eligible),normalized_full_reply_input_substrings=sum(x['normalized_reply_is_input_substring'] for x in xs))
 summary=dict(definition='Union of output word positions covered by a matching contiguous5lexical-wordgram in actual input; casefold/punctuationignored. Short<5separate. Nonexclusive scaffold/prior categories. Posthoc descriptive compatibility with reuse, not proof of copying or absence of thought.',all=group(out),capped=group([x for x in out if x['stop']=='token_limit']),eos=group([x for x in out if x['stop']=='eos']),blocks=[dict(start=a,end=a+20,**group([x for x in out if a<=x['step']<a+20])) for a in range(205,305,20)])
 for name,obj in [('SUMMARY',summary),('ROW_METRICS',out)]:
  with (R/(name+'.json')).open('x') as fh:json.dump(obj,fh,indent=2);fh.write('\n')
 for rel,h in json.loads((R/'INPUTS_BEFORE.json').read_text()).items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
 git=json.loads((R/'GIT_CHECK.json').read_text());assert not git['mismatches'] and not git['not_in_published_tree']
 with (R/'CHECKS.json').open('x') as fh:json.dump(dict(status='pass',local_published_files_match=git['matching_published_files'],all100_prompt_token_dispatch_reconstructions=True,base_and_adapter_file_pins_pass=True,active_policy_freeze_pass=True,all_pinned_inputs_unchanged=True,primary_paused305_no_lock=True,verification_pointer_unchanged='0054',new_model_calls=0),fh,indent=2);fh.write('\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
