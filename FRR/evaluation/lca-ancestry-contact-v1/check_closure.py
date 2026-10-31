"""Bounded coordinator oracle: four-node topological DAGs, Boolean closure."""
from pathlib import Path
import itertools,json,sys
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tools'))
from evidence_ancestry import query
edges=[(j,i) for j in range(4) for i in range(j)];cases=0
for mask in range(1<<len(edges)):
 parents={i:[] for i in range(4)};reach=[[i==j for j in range(4)] for i in range(4)]
 for k,(child,parent) in enumerate(edges):
  if mask>>k&1:parents[child].append(parent);reach[child][parent]=True
 for k in range(4):
  for i in range(4):
   for j in range(4):reach[i][j]=reach[i][j] or(reach[i][k] and reach[k][j])
 for u,v in itertools.combinations_with_replacement(range(4),2):
  common={c for c in range(4) if reach[u][c] and reach[v][c]};expected=sorted(str(c) for c in common if not any(c!=d and reach[d][c] for d in common))
  manifest={'graph_id':'closurecheck','edge_semantics':'declaredchildtoparent','nodes':[{'id':str(i),'parents':[str(x) for x in parents[i]]} for i in range(4)],'query':[str(u)] if u==v else[str(u),str(v)]}
  assert query(manifest,R)['maximal_common_ancestors']==expected;cases+=1
print(json.dumps({'four_node_topological_dags':64,'queries_compared_to_boolean_transitive_closure':cases,'all_match':True,'scope':'boundedalgorithmconsistencychecks,notindependentprovenance/truthevidence'},indent=2))
