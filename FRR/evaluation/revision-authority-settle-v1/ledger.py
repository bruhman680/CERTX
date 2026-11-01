"""Literal single-field revision contract; authority is a supplied assumption, not authentication."""
import copy
STATES={'positive','zero','missing'}
class Hold(Exception):
 def __init__(self,verdict,reason):self.verdict=verdict;self.reason=reason

def resolve(events,target,allowed=('owner',)):
 def hold(v,r):raise Hold(v,r)
 try:
  if not isinstance(events,list):hold('FORMAT_ERROR','not a ledger list')
  if not events:return {'verdict':'SOURCE_ABSENT','reason':'empty ledger','state':None,'heads':[],'history':[],'ignored':[],'status_events':[]}
  accepted=[];ignored=[]
  for e in events:
   if not isinstance(e,dict) or 'source' not in e:hold('PROVENANCE_MISSING','missing source attribution')
   if e['source'] not in allowed:ignored.append(e.get('id'));continue
   if e.get('plot')!=target:ignored.append(e.get('id'));continue
   accepted.append(e)
  if not accepted:return {'verdict':'NO_AUTHORIZED_EVIDENCE','reason':'no allowed target claims','state':None,'heads':[],'history':[],'ignored':sorted(ignored,key=str),'status_events':[]}
  by={}
  for e in accepted:
   if set(e)!={'id','source','plot','rev','parents','op','payload'}:hold('FORMAT_ERROR','unsupported schema')
   if not isinstance(e['id'],str) or not e['id'] or not isinstance(e['parents'],list) or any(not isinstance(x,str) for x in e['parents']) or len(e['parents'])!=len(set(e['parents'])):hold('FORMAT_ERROR','invalid identity/parents')
   if type(e['rev']) is not int or e['rev']<1 or e['op'] not in ('replace','patch','delete'):hold('FORMAT_ERROR','invalid revision/operation')
   payload=e['payload']
   if not isinstance(payload,dict) or set(payload)-{'status'}:hold('FORMAT_ERROR','unsupported payload')
   if 'status' in payload and not (isinstance(payload['status'],str) and payload['status'] in STATES) and not (payload['status'] is None and e['op']=='patch'):hold('FORMAT_ERROR','invalid status value')
   if e['op']=='delete' and payload:hold('FORMAT_ERROR','record deletion has payload')
   if e['id'] in by and by[e['id']]!=e:hold('ID_CONFLICT','same authorized ID has different contents')
   by[e['id']]=copy.deepcopy(e)
  for e in by.values():
   if any(p not in by for p in e['parents']):hold('LINEAGE_ERROR','parent missing, foreign, or unauthorized')
  visiting=set();done=set();order=[]
  def visit(i):
   if i in visiting:hold('LINEAGE_ERROR','parent cycle')
   if i in done:return
   visiting.add(i)
   for p in sorted(by[i]['parents']):visit(p)
   visiting.remove(i);done.add(i);order.append(i)
  for i in sorted(by):visit(i)
  snapshots={}
  for i in order:
   e=by[i];parents=e['parents']
   if any(e['rev']<=by[p]['rev'] for p in parents):hold('LINEAGE_ERROR','revision does not advance parent')
   if not parents and e['op']!='replace':hold('LINEAGE_ERROR','no replacement base')
   if e['op']=='delete':snap={'kind':'deleted','value':None,'status_event':i}
   elif e['op']=='replace':snap={'kind':'known' if 'status' in e['payload'] else 'partial','value':e['payload'].get('status'),'status_event':i}
   else:
    if len(parents)!=1:hold('LINEAGE_ERROR','patch requires exactly one base; explicit merge required')
    base=snapshots[parents[0]]
    if base['kind']=='deleted':hold('LINEAGE_ERROR','patch cannot resurrect a deleted record')
    snap=copy.deepcopy(base)
    if 'status' in e['payload']:snap={'kind':'partial' if e['payload']['status'] is None else 'known','value':e['payload']['status'],'status_event':i}
   snapshots[i]=snap
  referenced={p for e in by.values() for p in e['parents']};heads=sorted(set(by)-referenced)
  sig={(snapshots[i]['kind'],snapshots[i]['value']) for i in heads}
  verdict='CONCURRENT_CONFLICT' if len(sig)>1 else {'known':'KNOWN','partial':'PARTIAL','deleted':'DELETED'}[next(iter(sig))[0]]
  value=next(iter(sig))[1] if verdict=='KNOWN' else None
  return {'verdict':verdict,'reason':'declared authorized lineage, no display-order precedence','state':value,'heads':heads,'history':[{'id':i,'event':by[i],'snapshot':snapshots[i]} for i in order],'ignored':sorted(ignored,key=str),'status_events':sorted({snapshots[i]['status_event'] for i in heads})}
 except Hold as h:return {'verdict':h.verdict,'reason':h.reason,'state':None,'heads':[],'history':[],'ignored':[],'status_events':[]}

def shortcut(events,target,mode):
 es=[e for e in events if e.get('source')=='owner' and e.get('plot')==target]
 if not es:return None
 e=es[-1] if mode=='arrival_last' else max(enumerate(es),key=lambda pair:(pair[1].get('rev',0),pair[0]))[1]
 v=e.get('payload',{}).get('status')
 return v if isinstance(v,str) and v in STATES else None
