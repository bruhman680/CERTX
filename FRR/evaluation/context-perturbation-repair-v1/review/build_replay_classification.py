from pathlib import Path
P=Path(__file__).resolve().parent
s=(P/'replay_audit.py').read_text()
s=s.replace("(O/'REPLAY_SELECTION.json').write_text", "(O/'REPLAY_SELECTION_CLASSIFICATION.json').write_text").replace("(O/'REPLAY_RESULT.json').write_text", "(O/'REPLAY_CLASSIFICATION_RERUN.json').write_text")
insert='''
details={}
def detail(k,qi,fields,top,scores,labels,reasons,v,z):
 savedtop=POOL[fields['top']][qi];ours=top[qi];savedscore=POOL[fields['scores']][qi];ourset=set(map(int,ours));savedset=set(map(int,savedtop));changed=list(sorted(ourset.symmetric_difference(savedset)));union=sorted(ourset|savedset)
 # Every reversed top-order pair, and every exchanged included/excluded pair.
 pairs=[]
 for a in union:
  for b in union:
   if a>=b:continue
   op={int(j):i for i,j in enumerate(ours)};sp={int(j):i for i,j in enumerate(savedtop)}
   reversed_order=a in op and b in op and a in sp and b in sp and ((op[a]<op[b])!=(sp[a]<sp[b]))
   exchanged=(a in ourset-savedset and b in savedset-ourset) or (b in ourset-savedset and a in savedset-ourset)
   if reversed_order or exchanged:pairs.append({'ids':[a,b],'reversed_order':reversed_order,'exchanged_membership':exchanged,'saved_score_gap':float(abs(savedscore[a]-savedscore[b])),'independent_score_gap':float(abs(scores[qi,a]-scores[qi,b]))})
 fixed={f:bool(np.array_equal(a,POOL[fields[f]][qi])) for f,a in {'labels':labels[qi],'reasons':reasons[qi],'valid':v[qi]}.items()}
 details[k+f'/q{qi}']={'condition':k,'query_index':qi,'independent_top':ours.tolist(),'saved_top':savedtop.tolist(),'same_order':bool(np.array_equal(ours,savedtop)),'same_membership':ourset==savedset,'independent_only_ids':sorted(ourset-savedset),'saved_only_ids':sorted(savedset-ourset),'changed_pairs':pairs,'fixed_id_exact':fixed,'fixed_id_products_max_abs':float(np.max(np.abs(z[qi]-POOL[fields['products']][qi]))),'fixed_id_scores_max_abs':float(np.max(np.abs(scores[qi]-savedscore))),'max_changed_saved_score_gap':max((p['saved_score_gap'] for p in pairs),default=0),'max_changed_independent_score_gap':max((p['independent_score_gap'] for p in pairs),default=0)}
'''
s=s.replace('ledger={}\n',insert+'\nledger={}\n')
s=s.replace("row=ledger[(k,qi)];sel.append", "row=ledger[(k,qi)];detail(k,qi,fields,top,scores,labels,reasons,v,z);sel.append")
s+='''
original=json.load(open(O/'REPLAY_ORIGINAL_FAILURE'/'REPLAY_RESULT.json'))
classified=[]
for i,e in enumerate(original['errors']):
 key,field=e[0].split(':');rows=[key] if '/q' in key else [key+'/q0',key+'/q31'];affected=[details[r] for r in rows if not details[r]['same_order']]
 classified.append({'original_error_index':i,'original_error':e,'field':field,'classification':'membership_change' if any(not r['same_membership'] for r in affected) else 'ordering_only','affected_rows':[r['condition']+f"/q{r['query_index']}" for r in affected],'fixed_id_exact':all(all(r['fixed_id_exact'].values()) for r in affected),'max_changed_saved_score_gap':max((r['max_changed_saved_score_gap'] for r in affected),default=0),'max_changed_independent_score_gap':max((r['max_changed_independent_score_gap'] for r in affected),default=0)})
from collections import Counter
summary={'original_errors':len(original['errors']),'classified_errors':len(classified),'classes':dict(Counter(c['classification'] for c in classified)),'selected_rows':len(details),'rows_order_changed':sum(not r['same_order'] for r in details.values()),'rows_membership_changed':sum(not r['same_membership'] for r in details.values()),'all_fixed_id_categorical_exact':all(all(r['fixed_id_exact'].values()) for r in details.values()),'candidate_readouts':len(details)*48,'max_changed_saved_score_gap':max(r['max_changed_saved_score_gap'] for r in details.values()),'max_changed_independent_score_gap':max(r['max_changed_independent_score_gap'] for r in details.values()),'no_new_error_fields':set(e[0].split(':')[-1] for e in err)==set(e[0].split(':')[-1] for e in original['errors'])}
(O/'REPLAY_ERROR_CLASSIFICATION.json').write_text(json.dumps({'summary':summary,'errors':classified,'rows':details},indent=2)+'\\n');print('CLASSIFICATION',json.dumps(summary,indent=2))
'''
(P/'replay_classification.py').write_text(s)
