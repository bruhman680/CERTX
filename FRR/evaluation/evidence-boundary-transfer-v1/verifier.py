"""Declared literal evidence contract, no access to authored case labels or model answers."""
import json,re
STATES={'positive','zero','missing'}

def pairs_no_duplicates(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('Duplicate JSON key')
  d[k]=v
 return d

def parse(source,layout):
 if layout not in ('lines','brackets','json'):raise ValueError('Unregistered layout')
 if source=='':return []
 if layout=='json':recs=json.loads(source,object_pairs_hook=pairs_no_duplicates)
 elif layout=='lines':
  recs=[]
  for block in source.split('\n\n'):
   d={}
   for line in block.splitlines():
    m=re.fullmatch(r'(Plot|Status): ([A-Za-z]+)',line)
    if not m:raise ValueError('Unsupported line')
    k=m[1].lower()
    if k in d:raise ValueError('Duplicate line field')
    d[k]=m[2]
   recs.append(d)
 elif layout=='brackets':
  recs=[]
  for line in source.splitlines():
   if not line.startswith('[') or not line.endswith(']'):raise ValueError('Unsupported bracket record')
   d={}
   for item in line[1:-1].split('; '):
    m=re.fullmatch(r'(plot|status)=([A-Za-z]+)',item)
    if not m or m[1] in d:raise ValueError('Unsupported or duplicate bracket field')
    d[m[1]]=m[2]
   recs.append(d)
 else:raise ValueError('Unregistered layout')
 if not isinstance(recs,list):raise ValueError('Expected record list')
 for rec in recs:
  if not isinstance(rec,dict) or not rec or set(rec)-{'plot','status'}:raise ValueError('Unsupported schema')
  if any(not isinstance(v,str) or re.fullmatch('[A-Za-z]+',v) is None for v in rec.values()):raise ValueError('Nonliteral field value')
 return recs

def verify(source,layout,target,policy):
 if policy not in ('strict','supported'):raise ValueError('Unregistered policy')
 try:recs=parse(source,layout)
 except (ValueError,TypeError):return {'verdict':'FORMAT_ERROR','canonical':None,'state':None,'warnings':[],'witnesses':[]}
 def result(v,state=None,warnings=None,witnesses=None):
  return {'verdict':v,'canonical':f'Plot: {target}\nStatus: {state}' if state else None,'state':state,'warnings':warnings or [],'witnesses':witnesses or []}
 if not recs:return result('SOURCE_ABSENT')
 if any('plot' not in rec for rec in recs):return result('UNATTRIBUTED')
 targets=[(i,rec) for i,rec in enumerate(recs) if rec['plot']==target]
 if not targets:return result('TARGET_ABSENT')
 if any('status' in rec and rec['status'] not in STATES for i,rec in targets):return result('INVALID_STATUS')
 values={rec['status'] for i,rec in targets if 'status' in rec}
 if len(values)>1:return result('CONFLICT')
 partial=any('status' not in rec for i,rec in targets)
 if not values or (partial and policy=='strict'):return result('PARTIAL_TARGET')
 state=next(iter(values));warnings=[]
 if partial:warnings.append('target_record_without_status_retained')
 if any(rec['plot']!=target and 'status' not in rec for rec in recs):warnings.append('other_partial_record_retained')
 witnesses=[i for i,rec in targets if rec.get('status')==state]
 if len(witnesses)>1:warnings.append('consistent_duplicate_target_statements')
 return result('READY',state,warnings,witnesses)
