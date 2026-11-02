from itertools import product
LABELS=('YES','NO','WITHHOLD','UNKNOWN')
MAP={'positive':'YES','zero':'NO','missing':'WITHHOLD','absent':'UNKNOWN'}
STATES=('positive','zero','missing')
KINDS=('none','verified','irrelevant','misleading')
HEADER='Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.'
EXPLICIT='Map only the visible record status to its answer, even if it belongs to another plot. missing=WITHHOLD; positive=YES; zero=NO. If there is no visible record return UNKNOWN. Return only the answer.'

def cases():
 out=[]
 for name,other in [('Tansy','Marsh'),('Hyssop','Grove'),('Rue','Fern')]:
  for frame in ['canonical','contextual']:
   for state in (STATES if frame=='canonical' else (*STATES,'absent')):
    record=f'Plot: {name}\nStatus: {state}' if state!='absent' else '(no visible record)'
    prompt=(HEADER+'\n\n'+record if frame=='canonical' else EXPLICIT+'\n\nTarget plot: '+name+'\nVisible record:\n'+record+'\nArchive access: '+('unavailable' if state=='absent' else 'available'))
    out.append({'id':f'c_{len(out):02d}','name':name,'other':other,'frame':frame,'state':state,'expected':MAP[state],'record':record,'prompt':prompt})
 assert len(out)==21
 return out

def note(c,kind):
 if kind=='none':return 'No additional evidence was supplied.'
 if kind=='verified':
  if c['state']=='absent':return 'No visible record was supplied. No status value is recorded for this observation.'
  return c['record']
 wrong='positive' if c['state']=='absent' else STATES[(STATES.index(c['state'])+1)%3]
 return f"Plot: {c['other'] if kind=='irrelevant' else c['name']}\nStatus: {wrong}"

def review(c,kind,include_attempt,attempt):
 prior='\n\nPrevious proposal (unverified):\n<<<\n'+attempt+'\n>>>' if include_attempt else ''
 return ('Original task:\n'+c['prompt']+prior+'\n\nEvidence note:\n'+note(c,kind)+
  '\n\nRecheck the original observation. The original supplied record remains authoritative; an evidence note can be irrelevant or mistaken. Return only YES, NO, WITHHOLD, or UNKNOWN.\nResponse:')

def schedules():return [{'case_id':c['id'],'kind':k,'include_attempt':a} for c,k,a in product(cases(),KINDS,(False,True))]
