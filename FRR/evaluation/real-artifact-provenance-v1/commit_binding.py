"""Supplemental matching reconstructed commit-body check; original audit stays immutable."""
import datetime
from receipt import git_hash,ReceiptError

def check(capture,binding,root):
 if binding['source_sha256'] is None:raise ReceiptError('MISSING_CAPTURE_BINDING')
 by={x['captured_sha']:x for x in binding['results']};results=[]
 for c in capture['commits']:
  item=by[c['sha']]
  if len(item['matches'])!=1:raise ReceiptError('NONUNIQUE_CANDIDATE_MATCH')
  m=item['matches'][0];data=(root/m['published_relative_body']).read_bytes()
  if git_hash('commit',data)!=c['sha']:raise ReceiptError('COMMIT_HASH_MISMATCH')
  def ident(key,offset):
   a=c[key];seconds=int(datetime.datetime.fromisoformat(a['date'].replace('Z','+00:00')).timestamp())
   return f"{key} {a['name']} <{a['email']}> {seconds} {offset}\n"
  candidate=('tree '+c['tree']['sha']+'\n'+''.join('parent '+p['sha']+'\n' for p in c['parents'])+ident('author',m['author_offset'])+ident('committer',m['committer_offset'])+'\n'+c['message']+'\n'*m['appended_newlines']).encode('utf-8')
  if data!=candidate:raise ReceiptError('COMMIT_METADATA_MISMATCH')
  if not m['git_hash_object_match'] or m['git_hash_object_sha']!=c['sha']:raise ReceiptError('INDEPENDENT_GIT_CHECK_MISSING')
  results.append({'commit':c['sha'],'bytes':len(data),'candidate_count':item['attempt_count'],'matching_candidates':1,'wire_raw_object_received':False,'reconstructed_body_hash_matches':True})
 return results
