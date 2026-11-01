"""Supplied record status is invariant; surround it with declared field packages."""
from itertools import product
MAP={'positive':'YES','zero':'NO','missing':'WITHHOLD'}
HEADERS={
 'canonical':'Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.',
 'explicit_visible':'Map only the visible record status to its answer, even if it belongs to another plot. missing=WITHHOLD; positive=YES; zero=NO. If there is no visible record return UNKNOWN. Return only the answer.'}
NAMES=(('Maple','Fir'),('Cedar','Elm'),('Hazel','Ash'))
ACCESS={'yes':'Archive accessible: yes','no':'Archive accessible: no','available':'Archive access: available','unavailable':'Archive access: unavailable'}

def records():
 return [{'id':f's_{i*3+j:02d}','name':name,'other':other,'state':state,'expected':MAP[state], 'record':f'Plot: {name}\nStatus: {state}'} for i,(name,other) in enumerate(NAMES) for j,state in enumerate(MAP)]

def conditions():
 rows=[{'id':'no_fields','kind':'none','match':None,'access':None}]
 for kind in ('relevant','unrelated'):
  rows +=[{'id':kind+'_target_'+m,'kind':kind,'match':m,'access':None} for m in ('same','different')]
  rows +=[{'id':kind+'_access_'+v,'kind':kind,'match':None,'access':v} for v in ACCESS]
  rows +=[{'id':kind+'_both_'+m+'_'+v,'kind':kind,'match':m,'access':v} for m,v in product(('same','different'),ACCESS)]
 assert len(rows)==29
 return rows

def fields(rec,cond):
 before=[];after=[]
 if cond['match']:
  name=rec['name'] if cond['match']=='same' else rec['other']
  before=[('Target plot: ' if cond['kind']=='relevant' else 'Label plot: ')+name]
 if cond['access']:
  line=ACCESS[cond['access']]
  after=[line if cond['kind']=='relevant' else line.replace('Archive','Window')]
 return before,after

def render(rec,cond,header):
 before,after=fields(rec,cond)
 body='\n'.join(before+['Visible record:',rec['record']]+after)
 return HEADERS[header]+'\n\n'+body

def anchor(rec):return HEADERS['canonical']+'\n\n'+rec['record']

def queries():
 rows=[]
 for r in records():
  rows.append({'id':f'q_{len(rows):04d}','source_id':r['id'],'header':'canonical','condition':'bare_anchor','kind':'anchor','match':None,'access':None,'prompt':anchor(r),'expected':r['expected'],'state':r['state'],'name':r['name']})
  for header,cond in product(HEADERS,conditions()):
   rows.append({'id':f'q_{len(rows):04d}','source_id':r['id'],'header':header,'condition':cond['id'],'kind':cond['kind'],'match':cond['match'],'access':cond['access'],'prompt':render(r,cond,header),'expected':r['expected'],'state':r['state'],'name':r['name']})
 assert len(rows)==531 and len({r['prompt'] for r in rows})==531
 return rows
