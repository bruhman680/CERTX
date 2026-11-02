import copy,json,unittest
from pathlib import Path
from receipt import verify,materialize,ReceiptError
from temporal import contact
ROOT=Path(__file__).resolve().parent
class Checks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.b=json.loads((ROOT/'CAPTURE.json').read_text());cls.p=json.loads((ROOT/'POLICY.json').read_text())
 def test_original_snapshots(self):
  r=verify(self.b,self.p);self.assertEqual(len(r['snapshots']),8)
  for s in r['snapshots']:
   actual=materialize(self.b,self.p,s['commit']);expected=next(x['text'] for x in self.b['blobs'] if x['sha']==s['blob']);self.assertEqual(actual,expected)
 def test_list_order_not_authority(self):
  b=copy.deepcopy(self.b)
  for key in ['commits','root_trees','frr_trees','blobs']:b[key].reverse()
  self.assertEqual(verify(b,self.p),verify(self.b,self.p))
 def test_corrupt_content(self):
  b=copy.deepcopy(self.b);b['blobs'][0]['text']+='x'
  with self.assertRaisesRegex(ReceiptError,'BLOB_HASH_MISMATCH'):verify(b,self.p)
 def test_missing_parent(self):
  b=copy.deepcopy(self.b);b['commits'].pop(3)
  with self.assertRaisesRegex(ReceiptError,'INCOMPLETE_CAPTURE'):verify(b,self.p)
 def test_corrupt_tree(self):
  b=copy.deepcopy(self.b);b['frr_trees'][0]['tree'][0]['path']+='x'
  with self.assertRaisesRegex(ReceiptError,'TREE_HASH_MISMATCH'):verify(b,self.p)
 def test_authority_pin(self):
  b=copy.deepcopy(self.b);b['pinned_head']=b['commits'][1]['sha']
  with self.assertRaisesRegex(ReceiptError,'AUTHORITY_PIN_MISMATCH'):verify(b,self.p)
 def test_scope(self):
  b=copy.deepcopy(self.b);b['artifact_path']='FRR/README.md'
  with self.assertRaisesRegex(ReceiptError,'SCOPE_MISMATCH'):verify(b,self.p)
 def test_outside_capture(self):
  old=self.b['commits'][-1]['parents'][0]['sha']
  with self.assertRaisesRegex(ReceiptError,'OUTSIDE_CAPTURE'):materialize(self.b,self.p,old)
 def test_two_time_dimensions(self):
  self.assertEqual(len(contact()['queries']),6)
if __name__=='__main__':unittest.main()
