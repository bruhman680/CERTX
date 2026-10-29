"""Authored typed dependency recursion, not natural-language reasoning."""
import json,hashlib,statistics,copy
from pathlib import Path
P=Path(__file__).resolve().parent

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def evaluate(graph,root,memo=None,max_depth=8):
 memo={} if memo is None else memo
 trace=[]
 def result(value,reason,fp):return {'value':value,'reason':reason,'fingerprint':fp}
 def visit(name,path):
  if name in path:
   r=result(None,'cycle',digest(['cycle',name,path]));trace.append({'node':name,'action':'stop_cycle'});return r
  if len(path)>=max_depth:
   r=result(None,'depth_limit',digest(['depth',name,path]));trace.append({'node':name,'action':'stop_depth'});return r
  if name not in graph:
   r=result(None,'missing_node',digest(['missing',name]));trace.append({'node':name,'action':'stop_missing'});return r
  node=graph[name];children=[visit(x,path+[name]) for x in node.get('deps',[])]
  fp=digest([node,[x['fingerprint'] for x in children]])
  if name in memo and memo[name]['fingerprint']==fp:
   trace.append({'node':name,'action':'reuse'});return copy.deepcopy(memo[name])
  if node['op']=='source':v=node.get('value');reason='supplied_source' if v is not None else 'absent_evidence'
  elif node['op'] in ['median_ge','mean_ge']:
   vals=children[0]['value']
   if vals is None:v=None;reason='missing_measurements'
   else:
    fn=statistics.median if node['op']=='median_ge' else statistics.mean
    v=fn(vals)>=node['threshold'];reason='explicit_numeric_rule'
  elif node['op']=='all':
   vals=[x['value'] for x in children]
   if any(x is False for x in vals):v=False
   elif all(x is True for x in vals):v=True
   else:v=None
   reason='explicit_conjunction'
  else:v=None;reason='unsupported_rule'
  r=result(v,reason,fp);memo[name]=copy.deepcopy(r);trace.append({'node':name,'action':'recompute','reason':reason});return r
 final=visit(root,[])
 return {'verdict':'SUPPORTED' if final['value'] is True else 'CONTRADICTED' if final['value'] is False else 'UNRESOLVED','result':final,'trace':trace},memo

def run():
 cases=json.loads((P/'GRAPH_CASES.json').read_text());out=[]
 for c in cases:
  first,memo=evaluate(c['old'],'release',max_depth=c.get('depth',8))
  stale=copy.deepcopy(first)
  final,_=evaluate(c['new'],'release',memo=memo,max_depth=c.get('depth',8))
  out.append({'id':c['id'],'initial':first,'naive_unchecked_historical_reuse':stale,'reassessed':final,'expected':c['expected'],'matches_expected':final['verdict']==c['expected'],'historical_object_preserved':first==stale})
 result={'scope':'Stipulated graph/rules, typed values, authored development; no agent self-reflection or factual inference','cases':out,'all_expected':all(x['matches_expected'] for x in out)}
 (P/'GRAPH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'cases':len(out),'all_expected':result['all_expected'],'verdicts':[(x['id'],x['initial']['verdict'],x['reassessed']['verdict']) for x in out]}))
 assert result['all_expected']

if __name__=='__main__':run()
