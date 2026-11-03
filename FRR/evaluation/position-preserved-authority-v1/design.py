from itertools import product
from legacy_design import cases as old_cases
LABELS=('YES','NO','WITHHOLD','UNKNOWN')
MAP={'positive':'YES','zero':'NO','missing':'WITHHOLD','absent':'UNKNOWN'}
HEADER=('Map only the visible record status to its answer, even if it belongs to another plot. missing=WITHHOLD; positive=YES; zero=NO. If there is no visible record return UNKNOWN. Return only the answer.')
AUTH='Answer from the original observation.'
def cases():
 out=[]
 for split,name in [('discovery','JW64'),('confirmation','PL27')]:
  for layout in ('lines','inline'):
   for state in MAP:
    record='(no visible record)' if state=='absent' else (f'Plot: {name}\nStatus: {state}' if layout=='lines' else f'Plot: {name} | Status: {state}')
    obs='Target plot: '+name+('\nVisible record:\n' if layout=='lines' else ' | Visible record: ')+record
    out.append(dict(id=f'c{len(out):02d}',split=split,name=name,layout=layout,state=state,expected=MAP[state],record=record,prompt=HEADER+'\n\n'+obs))
 return out

def render(c,content,family,prefix_n,slot):
 evidence=c['record'] if content=='duplicate' else 'Reference material.'
 return 'Evidence note:\n'+evidence+'\nReference text:'+(' '+family)*prefix_n+'\n\n'+c['prompt']+'\n\n'+slot+'\n\nReturn only the answer.'
def tokens(tok,p):return tok.apply_chat_template([{'role':'user','content':p}],tokenize=True,add_generation_prompt=True)
def record_span(tok,p,c):
 text=tok.apply_chat_template([{'role':'user','content':p}],tokenize=False,add_generation_prompt=True);e=tok(text,add_special_tokens=False,return_offsets_mapping=True);assert e['input_ids']==tokens(tok,p)
 start=text.index(c['prompt'])+c['prompt'].index(c['record']);end=start+len(c['record']);hit=[i for i,(a,b) in enumerate(e['offset_mapping']) if b>a and b>start and a<end];return [min(hit),max(hit)+1]
def build(tok):
 cs=cases();target=max(len(tokens(tok,render(c,k,f,0,AUTH))) for c in cs for k,f in product(('duplicate','filler'),('memo','paper')))+4;out=[];audit=[]
 for c in cs:
  out.append(dict(case_id=c['id'],split=c['split'],layout=c['layout'],state=c['state'],expected=c['expected'],condition='original',content=None,authority=None,family=None,placement=None,padding_units=0,prompt=c['prompt']))
  for k,f in product(('duplicate','filler'),('memo','paper')):
   for n in range(257):
    p=render(c,k,f,n,AUTH)
    if len(tokens(tok,p))==target:break
   else:raise ValueError('prefix match failed')
   for m in range(64):
    neutral='Reference text:'+(' '+f)*m
    p0=render(c,k,f,n,neutral)
    if len(tokens(tok,p0))==target:break
   else:raise ValueError('slot match failed')
   assert record_span(tok,p,c)==record_span(tok,p0,c)
   for a,text in [(False,p0),(True,p)]:
    condition=f'{k}__{f}__authority_{int(a)}';out.append(dict(case_id=c['id'],split=c['split'],layout=c['layout'],state=c['state'],expected=c['expected'],condition=condition,content=k,authority=a,family=f,placement='before',padding_units=n,slot_units=None if a else m,prompt=text));audit.append(dict(case_id=c['id'],condition=condition,record_span=record_span(tok,text,c),input_tokens=target))
 for c in old_cases():
  if c['name']=='Tansy':out.append(dict(case_id=c['id'],split='legacy',layout=c['frame'],state=c['state'],expected=c['expected'],condition='legacy_anchor',content=None,authority=None,family=None,placement=None,padding_units=0,prompt=c['prompt']))
 for i,q in enumerate(out):q['run_id']=f'q{i:03d}'
 assert len(out)==151 and len({q['prompt'] for q in out})==151
 return out,{'matched_tokens':target,'record_spans':audit,'scope':'before-placement only; fixed-width authority/control slot; memo and paper are not assumed neutral'}
