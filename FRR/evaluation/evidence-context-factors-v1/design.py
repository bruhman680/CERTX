"""Input-only renderers. Token matching is fitted before any model output."""
from itertools import product
from legacy_design import cases as old_cases
LABELS=('YES','NO','WITHHOLD','UNKNOWN')
MAP={'positive':'YES','zero':'NO','missing':'WITHHOLD','absent':'UNKNOWN'}
HEADER=('Map only the visible record status to its answer, even if it belongs to another plot. '
        'missing=WITHHOLD; positive=YES; zero=NO. If there is no visible record return UNKNOWN. Return only the answer.')
PAIRS=(('discovery','QT58'),('confirmation','RX93'))
def cases():
 out=[]
 for split,name in PAIRS:
  for layout in ('lines','inline'):
   for state in MAP:
    record='(no visible record)' if state=='absent' else (f'Plot: {name}\nStatus: {state}' if layout=='lines' else f'Plot: {name} | Status: {state}')
    obs=('Target plot: '+name+'\nVisible record:\n'+record if layout=='lines' else 'Target plot: '+name+' | Visible record: '+record)
    out.append(dict(id=f'c{len(out):02d}',split=split,name=name,layout=layout,state=state,expected=MAP[state],record=record,prompt=HEADER+'\n\n'+obs))
 return out

def render(c,content,authority,placement,padding):
 original=c['prompt']
 if content=='padded':
  return original+'\n\nReference text:\n'+padding+'\n\nReturn only the answer.'
 assert content in ('duplicate','filler') and authority in (False,True) and placement in ('before','after')
 evidence=c['record'] if content=='duplicate' else 'Reference material.'
 block='Evidence note:\n'+evidence+'\nReference text:'+padding
 body=block+'\n\n'+original if placement=='before' else original+'\n\n'+block
 return body+('\n\nAnswer from the original observation.' if authority else '')+'\n\nReturn only the answer.'

def tokens(tok,text):return tok.apply_chat_template([{'role':'user','content':text}],tokenize=True,add_generation_prompt=True)

def build(tok):
 cs=cases();templates=[]
 for c in cs:
  templates.append((c,'padded',None,None))
  templates.extend((c,k,a,p) for k,a,p in product(('duplicate','filler'),(False,True),('before','after')))
 target=max(len(tokens(tok,render(c,k,a,p,''))) for c,k,a,p in templates)+4
 out=[];pad_rows=[]
 for c in cs:
  out.append(dict(case_id=c['id'],split=c['split'],layout=c['layout'],state=c['state'],expected=c['expected'],condition='original',content=None,authority=None,placement=None,padding_units=0,prompt=c['prompt']))
  for cc,k,a,p in (t for t in templates if t[0]['id']==c['id']):
   for n in range(257):
    text=render(c,k,a,p,' memo'*n)
    if len(tokens(tok,text))==target:break
   else:raise ValueError(('Cannot token-match',c['id'],k,a,p,target))
   condition='padded' if k=='padded' else f'{k}__authority_{int(a)}__{p}'
   out.append(dict(case_id=c['id'],split=c['split'],layout=c['layout'],state=c['state'],expected=c['expected'],condition=condition,content=k,authority=a,placement=p,padding_units=n,prompt=text))
   pad_rows.append(dict(case_id=c['id'],condition=condition,units=n,tokens=target))
 for c in old_cases():
  if c['name']=='Tansy':out.append(dict(case_id=c['id'],split='legacy',layout=c['frame'],state=c['state'],expected=c['expected'],condition='legacy_anchor',content=None,authority=None,placement=None,padding_units=0,prompt=c['prompt']))
 for i,q in enumerate(out):q['run_id']=f'q{i:03d}'
 assert len(out)==167 and len({q['prompt'] for q in out})==167
 return out,{'global_matched_token_count':target,'padding':pad_rows,'filler':' memo repeated; no claim of semantic neutrality'}
