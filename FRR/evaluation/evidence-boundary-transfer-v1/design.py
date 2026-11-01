import json
from itertools import product
MAP={'positive':'YES','zero':'NO','missing':'WITHHOLD'}
LAYOUTS=('lines','brackets','json')
HEADER='Map the status to its answer. missing=WITHHOLD; positive=YES; zero=NO. Return only the answer.'

def render(records,layout):
 if not records:return ''
 if layout=='json':return json.dumps(records,separators=(',',':'))
 if layout=='lines':return '\n\n'.join('\n'.join(('Plot' if k=='plot' else 'Status')+': '+v for k,v in rec.items()) for rec in records)
 return '\n'.join('['+'; '.join(k+'='+v for k,v in rec.items())+']' for rec in records)

def cases():
 rows=[]
 def add(target,recs,layout,kind,strict,permissive,state=None,order=0,source=None):
  rows.append({'id':f'c_{len(rows):03d}','target':target,'source':render(recs,layout) if source is None else source,'layout':layout,'kind':kind,'order':order,'expected_strict':strict,'expected_supported':permissive,'expected_state':state})
 for target,other in [('Fennel','Pepper'),('Nettle','Bramble'),('Yarrow','Marigold')]:
  for i,state in enumerate(MAP):
   full={'plot':target,'status':state};op={'plot':other,'status':list(MAP)[(i+1)%3]}
   for layout in LAYOUTS:
    add(target,[full],layout,'single','READY','READY',state)
    add(target,[full,full],layout,'duplicate_same','READY','READY',state)
    for order in range(2):
     for kind,recs,strict,permissive,expected in [
      ('pair',[full,op],'READY','READY',state),
      ('conflict',[full,{'plot':target,'status':list(MAP)[(i+1)%3]}],'CONFLICT','CONFLICT',None),
      ('partial_plus_full',[{'plot':target},full],'PARTIAL_TARGET','READY',state)]:
      add(target,recs if order==0 else recs[::-1],layout,kind,strict,permissive,expected,order)
  for layout in LAYOUTS:
   for kind,recs,verdict in [
    ('other_only',[{'plot':other,'status':'zero'}],'TARGET_ABSENT'),
    ('name_only',[{'plot':target}],'PARTIAL_TARGET'),
    ('status_only',[{'status':'zero'}],'UNATTRIBUTED'),
    ('invalid_status',[{'plot':target,'status':'pending'}],'INVALID_STATUS'),
    ('absent',[],'SOURCE_ABSENT')]:add(target,recs,layout,kind,verdict,verdict)
   bad={'lines':f'Plot: {target}\nStatus: zero\nTRAILER: positive','brackets':f'[plot={target}; status=zero; unknown=positive]','json':json.dumps([{'plot':target,'status':'zero','unknown':'positive'}])}[layout]
   add(target,[],layout,'malformed','FORMAT_ERROR','FORMAT_ERROR',source=bad)
   for order in range(2):
    for kind,recs,verdict,state in [
     ('orphan_plus_full',[{'status':'zero'},{'plot':target,'status':'positive'}],'UNATTRIBUTED',None),
     ('conflicting_other',[{'plot':other,'status':'zero'},{'plot':other,'status':'missing'},{'plot':target,'status':'positive'}],'READY','positive'),
     ('partial_other',[{'plot':other},{'plot':target,'status':'positive'}],'READY','positive')]:
     add(target,recs if order==0 else recs[::-1],layout,kind,verdict,verdict,state,order)
 assert len(rows)==324
 return rows

def raw_prompt(c):return 'Read only the record for the target plot.\n'+HEADER+'\n\nTarget plot: '+c['target']+'\n\n'+(c['source'] or '(no records)')
def worker_prompt(record):return HEADER+'\n\n'+record
