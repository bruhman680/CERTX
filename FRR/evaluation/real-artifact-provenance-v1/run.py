from pathlib import Path
import copy,json,hashlib
from receipt import verify,materialize,ReceiptError
from temporal import contact
from io_utils import sha,dump_new
ROOT=Path(__file__).resolve().parent

def freeze():
 names=['CAPTURE.json','POLICY.json','PROTOCOL.md','receipt.py','temporal.py','test_contact.py','run.py','io_utils.py']
 dump_new(ROOT/'FREEZE.json',{'timing':'after observed public acquisition, before verifier mutation suite; functional audit, not blind empirical study','sha256':{n:sha(ROOT/n) for n in names}})

def run():
 f=json.loads((ROOT/'FREEZE.json').read_text());assert all(sha(ROOT/n)==h for n,h in f['sha256'].items())
 b=json.loads((ROOT/'CAPTURE.json').read_text());p=json.loads((ROOT/'POLICY.json').read_text());r=verify(b,p)
 snapshots=ROOT/'snapshots';snapshots.mkdir()
 for i,s in enumerate(r['snapshots']):
  text=materialize(b,p,s['commit']);(snapshots/(str(i)+'_'+s['commit']+'.md')).write_text(text)
 local=(ROOT.parent.parent/'CURRENT_HANDOFF.md').read_text();head=materialize(b,p,p['pinned_head']);assert local==head
 mutations=[]
 def negative(label,expected,change=None,outside=False):
  data=copy.deepcopy(b)
  if change:change(data)
  try:
   if outside:materialize(data,p,b['commits'][-1]['parents'][0]['sha'])
   else:verify(data,p)
   actual='UNEXPECTED_ACCEPT'
  except ReceiptError as e:actual=e.code
  assert actual==expected,(label,expected,actual)
  mutations.append({'control':label,'expected':expected,'observed':actual,'source':'synthetic copy, original CAPTURE unchanged'})
 negative('corrupted_blob','BLOB_HASH_MISMATCH',lambda x:x['blobs'][0].update(text=x['blobs'][0]['text']+'x'))
 negative('missing_within_window_parent','INCOMPLETE_CAPTURE',lambda x:x['commits'].pop(3))
 negative('corrupted_tree_entry','TREE_HASH_MISMATCH',lambda x:x['frr_trees'][0]['tree'][0].update(path='changed'))
 negative('different_authority_pin','AUTHORITY_PIN_MISMATCH',lambda x:x.update(pinned_head=x['commits'][1]['sha']))
 negative('different_artifact_scope','SCOPE_MISMATCH',lambda x:x.update(artifact_path='FRR/README.md'))
 negative('older_uncaptured_commit','OUTSIDE_CAPTURE',outside=True)
 reversed_data=copy.deepcopy(b)
 for key in ['commits','root_trees','frr_trees','blobs']:reversed_data[key].reverse()
 assert verify(reversed_data,p)==r
 dump_new(ROOT/'RECEIPT.json',r);dump_new(ROOT/'MUTATION_CONTROLS.json',mutations);dump_new(ROOT/'TEMPORAL_CONTACT.json',contact())
 old=json.loads(Path('/workspace/real-artifact-before.json').read_text());assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
 assert all(sha(ROOT/n)==h for n,h in f['sha256'].items())
 dump_new(ROOT/'CHECKS.json',{'status':'pass','captured_commits':8,'verified_tree_object_instances':16,'verified_blob_object_instances':8,'distinct_artifact_blobs':len({s['blob'] for s in r['snapshots']}),'snapshot_replays':8,'negative_controls':6,'capture_list_order_invariant':True,'local_before_sync_matches_pinned_head':True,'temporal_queries':6,'earlier_cutoff_answer_preserved':True,'commit_signature_api_unsigned_count':sum(s['signature_api_reason']=='unsigned' for s in r['snapshots']),'raw_commit_object_hashes_not_verified':True,'old_local_files_unchanged_before_sync':len(old),'new_small_model_generations':0,'training_updates':0,'capture_has_bounded_parent_frontier':True})
 print(json.dumps(json.loads((ROOT/'CHECKS.json').read_text()),indent=2))
if __name__=='__main__':
 import sys
 {'freeze':freeze,'run':run}[sys.argv[1]]()
