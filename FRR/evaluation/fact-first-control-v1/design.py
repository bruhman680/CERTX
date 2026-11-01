"""Facts are proposals; their validator reads visible fields only, never hidden source."""
import re
from evidence import MAPPING,STATES
from task_reference import normalized_visible
from decoder import decode_v2,DESCRIPTIONS

FIELDS={'role':('TARGET','OTHER','ABSENT'),'status':('positive','zero','missing','none'),'access':('OPEN','CLOSED')}

def visible_facts(c):
 text=normalized_visible(c)
 if text is None:role,status='ABSENT','none'
 else:
  n,status=re.fullmatch(r'Plot: ([A-Za-z]+)\nStatus: (positive|zero|missing)',text).groups()
  role='TARGET' if n==c['target'] else 'OTHER'
 return {'role':role,'status':status,'access':'OPEN' if c['archive_available'] else 'CLOSED'}

def action_from_facts(f):
 if f['role']=='TARGET':return MAPPING.get(f['status'])
 if f['role'] in ('OTHER','ABSENT'):
  return {'OPEN':'TARGET','CLOSED':'UNKNOWN'}.get(f['access'])
 return None

def decode_fact(text,field):
 # Last declaration is authoritative even when invalid; bare whole token also allowed.
 matches=list(re.finditer(r'^\s*'+field.upper()+r':\s*(.*?)\s*$',text,re.M|re.I))
 value=matches[-1][1] if matches else text.strip()
 value=value.strip().removesuffix('.').strip()
 choices={v.casefold():v for v in FIELDS[field]}
 return choices.get(value.casefold())

def view(c,vocab):
 access=('Archive accessible: '+('yes' if c['archive_available'] else 'no') if vocab=='shared_yes_no'
   else 'Archive access: '+('available' if c['archive_available'] else 'unavailable'))
 return 'Target plot: '+c['target']+'\nVisible record:\n'+(c['visible_display'] or '(no visible record)')+'\n'+access

def render(c,vocab,task):
 v=view(c,vocab)
 if task=='action':
  menu='\n'.join(a+': '+DESCRIPTIONS[a] for a in ('UNKNOWN','YES','TARGET','WITHHOLD','NO','FULL'))
  return ('Determine the target status. YES=positive; NO=zero; WITHHOLD=recorded missing. UNKNOWN means insufficient evidence. At most one archive request is allowed.\n\nActions:\n'+menu+
  '\n\nRules:\nA visible record belongs to the target only when its plot name matches the target name.\nWhen the visible record names the target, answer its recorded status.\nWhen the target record is not visible and the archive is accessible, request TARGET.\nWhen the target record is not visible and the archive is unavailable, report UNKNOWN.'+
  '\n\nCurrent task:\n'+v+'\n\nFinish with one ACTION: line. Use an action word or its exact description.\nResponse:')
 question={
 'role':'Classify only the visible record identity. TARGET means its plot name matches the target plot. OTHER means its plot name differs. ABSENT means no visible record. Return only ROLE: TARGET, ROLE: OTHER, or ROLE: ABSENT.',
 'status':'Copy only the status of the visible record, even if it belongs to another plot. If there is no visible record use none. Return only STATUS: positive, STATUS: zero, STATUS: missing, or STATUS: none.',
 'access':'Classify only archive access. OPEN means accessible (yes or available). CLOSED means inaccessible (no or unavailable). Return only ACCESS: OPEN or ACCESS: CLOSED.'}[task]
 return question+'\n\nCurrent observation:\n'+v+'\n\nResponse:'

def cases():
 rows=[]
 for target,other in [('Aster','Birch'),('Linden','Juniper'),('Rowan','Willow')]:
  for i,state in enumerate(STATES):
   for order in range(2):
    records=[(target,state),(other,STATES[(i+1)%3])]
    if order:records.reverse()
    source='Target plot: '+target+'\n\n'+'\n\n'.join(f'Record {j+1}:\nPlot: {n}\nStatus: {s}' for j,(n,s) in enumerate(records))
    for kind in ['selected_visible','none_available','other_visible','none_unavailable']:
     display=(f'Plot: {target}\nStatus: {state}' if kind=='selected_visible' else f'Plot: {other}\nStatus: {STATES[(i+1)%3]}' if kind=='other_visible' else None)
     rows.append({'id':f'c_{len(rows):03d}','target':target,'source':source,'state':state,'kind':kind,'visible_display':display,'archive_available':kind!='none_unavailable'})
 return rows
