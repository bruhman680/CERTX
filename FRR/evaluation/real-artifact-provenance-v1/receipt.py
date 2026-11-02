"""Byte/path/first-parent evidence, independent of file claims or timestamps."""
import hashlib
class ReceiptError(Exception):
 def __init__(self,code):self.code=code;super().__init__(code)
def fail(code):raise ReceiptError(code)
def git_hash(kind,data):return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()
def tree_hash(t):
 def order(e):return (e['path']+('/' if e['type']=='tree' else '')).encode()
 entries=sorted(t['tree'],key=order)
 if len({e['path'] for e in entries})!=len(entries):fail('DUPLICATE_TREE_PATH')
 data=b''.join(e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']) for e in entries)
 return git_hash('tree',data)
def unique(items):
 d={}
 for x in items:
  if x['sha'] in d and x!=d[x['sha']]:fail('CONFLICTING_OBJECT_RECORD')
  d[x['sha']]=x
 return d

def verify(bundle,policy):
 if (bundle['repository'],bundle['branch'],bundle['artifact_path'])!=(policy['repository'],policy['branch'],policy['artifact_path']):fail('SCOPE_MISMATCH')
 if bundle['pinned_head']!=policy['pinned_head']:fail('AUTHORITY_PIN_MISMATCH')
 cs=unique(bundle['commits']);trees=unique(bundle['root_trees']+bundle['frr_trees']);blobs=unique(bundle['blobs'])
 current=policy['pinned_head'];seen=set();snapshots=[]
 for i in range(policy['first_parent_depth']):
  if current in seen:fail('PARENT_CYCLE')
  if current not in cs:fail('INCOMPLETE_CAPTURE')
  seen.add(current);c=cs[current];root_id=c['tree']['sha']
  if root_id not in trees:fail('MISSING_TREE')
  root=trees[root_id]
  if tree_hash(root)!=root_id:fail('TREE_HASH_MISMATCH')
  entry=next((x for x in root['tree'] if x['path']=='FRR'),None)
  if entry is None or entry['type']!='tree':fail('PATH_UNAVAILABLE')
  if entry['sha'] not in trees:fail('MISSING_TREE')
  directory=trees[entry['sha']]
  if tree_hash(directory)!=directory['sha']:fail('TREE_HASH_MISMATCH')
  file=next((x for x in directory['tree'] if x['path']=='CURRENT_HANDOFF.md'),None)
  if file is None:fail('PATH_UNAVAILABLE')
  if file['type']!='blob' or file['mode'] not in ('100644','100755'):fail('INELIGIBLE_PATH_MODE')
  if file['sha'] not in blobs:fail('MISSING_BLOB')
  text=blobs[file['sha']]['text'];data=text.encode('utf-8')
  if git_hash('blob',data)!=file['sha']:fail('BLOB_HASH_MISMATCH')
  snapshots.append({'commit':current,'tree':root_id,'directory_tree':directory['sha'],'path':policy['artifact_path'],'blob':file['sha'],'bytes':len(data),'parents':[p['sha'] for p in c['parents']],'committer_date':c.get('committer',{}).get('date'),'signature_api_verified':c.get('verification',{}).get('verified'),'signature_api_reason':c.get('verification',{}).get('reason')})
  if i+1<policy['first_parent_depth']:
   if not c['parents']:fail('INCOMPLETE_CAPTURE')
   current=c['parents'][0]['sha']
 return {'status':'content_and_path_verified','question':policy['question'],'selected_commit':policy['pinned_head'],'selected_blob':snapshots[0]['blob'],'snapshots':snapshots,'capture_depth':len(snapshots),'full_history_claim':False,'boundary_parent_ids':snapshots[-1]['parents'],'commit_raw_bytes_rehashed':False,'trees_and_blobs_rehashed':True,'semantic_truth_verified':False,'source_author_authenticated':False}
def materialize(bundle,policy,commit):
 receipt=verify(bundle,policy)
 snapshot=next((s for s in receipt['snapshots'] if s['commit']==commit),None)
 if snapshot is None:fail('OUTSIDE_CAPTURE')
 return next(b['text'] for b in bundle['blobs'] if b['sha']==snapshot['blob'])
