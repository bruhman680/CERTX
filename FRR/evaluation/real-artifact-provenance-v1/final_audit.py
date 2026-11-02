from pathlib import Path
import json,copy
from io_utils import sha,dump_new
from receipt import verify,ReceiptError
from commit_binding import check
ROOT=Path(__file__).resolve().parent

def main():
 f=json.loads((ROOT/'FREEZE.json').read_text());assert all(sha(ROOT/n)==h for n,h in f['sha256'].items())
 b=json.loads((ROOT/'CAPTURE.json').read_text());p=json.loads((ROOT/'POLICY.json').read_text());assert verify(b,p)==json.loads((ROOT/'RECEIPT.json').read_text())
 binding=json.loads((ROOT/'COMMIT_BINDING.json').read_text());assert sha(ROOT/'CAPTURE.json')==binding['source_sha256'];rs=check(b,binding,ROOT);assert len(rs)==8
 corrupt=copy.deepcopy(b);corrupt['commits'][0]['tree']['sha']=corrupt['commits'][1]['tree']['sha']
 try:check(corrupt,binding,ROOT);raise AssertionError('changed commit metadata accepted')
 except ReceiptError as e:assert e.code=='COMMIT_METADATA_MISMATCH'
 old=json.loads(Path('/workspace/real-artifact-before.json').read_text());assert all(sha(Path('/workspace/frr')/n)==h for n,h in old.items())
 dump_new(ROOT/'FINAL_CHECKS.json',{'status':'pass','initial_audit_inputs_unchanged':True,'supplemental_reconstructed_commit_matches':8,'supplemental_git_hash_object_matches':8,'changed_commit_tree_metadata_rejected':True,'wire_raw_commit_payloads_received':False,'signed_authorship_verified':False,'scientific_truth_verified':False,'full_first_parent_history_claim':False,'bounded_first_parent_snapshots':8,'old_files_unchanged_before_sync':len(old),'new_model_generations':0,'new_training_updates':0,'full_candidate_ledger_local_only':True})
 print('Final audit passes:8commit reconstructions,16trees,8blobs,scope boundaries retained')
if __name__=='__main__':main()
