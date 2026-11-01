"""Instruction factors and a short public evidence note, not internal reasoning access."""
import re
from itertools import product
LABELS=('YES','NO','WITHHOLD','UNKNOWN')
MAPPING={'positive':'YES','zero':'NO','missing':'WITHHOLD','absent':'UNKNOWN'}
CONTEXTS={'none':None,'archive_yes':'Archive accessible: yes','archive_no':'Archive accessible: no','archive_available':'Archive access: available','archive_unavailable':'Archive access: unavailable','window_available':'Window access: available','window_unavailable':'Window access: unavailable'}

def render(name,state,context,clarify,absence,note):
 first=('Map only the visible record status to its answer, even if it belongs to another plot.' if clarify else 'Map the status to its answer.')
 header=first+' missing=WITHHOLD; positive=YES; zero=NO.'
 if absence:header+=' If there is no visible record return UNKNOWN.'
 if note:header+=' Give the answer first on its own line. Then write NOTE: and one short sentence naming the visible evidence or the specific evidence that is missing.'
 else:header+=' Return only the answer.'
 record='(no visible record)' if state=='absent' else f'Plot: {name}\nStatus: {state}'
 body='Visible record:\n'+record
 if CONTEXTS[context] is not None:body+='\n'+CONTEXTS[context]
 return header+'\n\n'+body

def queries():
 out=[]
 for name,state,context,clarify,absence,note in product(('Maple','Cedar','Hazel'),MAPPING,CONTEXTS,(False,True),(False,True),(False,True)):
  out.append({'id':f'q_{len(out):04d}','name':name,'state':state,'present':state!='absent','context':context,'clarify':clarify,'absence':absence,'note_requested':note,'expected':MAPPING[state], 'prompt':render(name,state,context,clarify,absence,note)})
 assert len(out)==672
 # Absent records intentionally contain no plot name and deduplicate across nominal names.
 return out

def decode(text):
 lines=text.strip().splitlines();first=lines[0].strip() if lines else ''
 m=re.fullmatch(r'(?:ANSWER:\s*)?(YES|NO|WITHHOLD|UNKNOWN)\.?',first,re.I)
 answer=m[1].upper() if m else None
 notes=list(re.finditer(r'^\s*NOTE:\s*(.*)$',text,re.M|re.I))
 note=''
 if notes:
  n=notes[-1];note=(n[1]+'\n'+text[n.end():]).strip()
 strict=text.strip() if text.strip() in LABELS else None
 return {'answer':answer,'strict_whole_answer':strict,'note_tag':bool(notes),'note_text':note,
  'later_answer_lines':re.findall(r'^\s*(?:ANSWER:\s*)?(YES|NO|WITHHOLD|UNKNOWN)\.?\s*$', '\n'.join(lines[1:]),re.M|re.I),
  'status_quotes':re.findall(r'\bstatus:\s*(positive|zero|missing)\b',note,re.I),
  'absence_cues':re.findall(r'\b(?:no visible record|no record|not provided|record (?:is )?(?:absent|unavailable))\b',note,re.I)}
