from pathlib import Path
import sys,json,copy,hashlib,tempfile,unittest
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[1]/'tools'))
from field_role_guard import bind
from evidence_threshold import load_json

class GuardTests(unittest.TestCase):
 def setUp(self):self.r=json.loads((P/'RECORDS.json').read_text())[2]
 def assess(self,p=None,**kw):
  r=self.r
  return bind(copy.deepcopy(r['proposal']) if p is None else p,kw.get('path',P/r['source_path']),kw.get('sha',r['source_sha256']),kw.get('entity',r['entity']),kw.get('unit',r['unit']))
 def test_equal_value_does_not_allow_cross_role_quote(self):
  p=copy.deepcopy(self.r['proposal']);self.assertEqual(p['minimum']['value'],p['observations'][0]['value'])
  p['observations'][0]['quote']=p['minimum']['quote'];self.assertEqual(self.assess(p)['stage'],'observation_binding_mismatch')
 def test_missing_is_source_state_not_zero(self):
  r=json.loads((P/'RECORDS.json').read_text())[0];out=bind(r['proposal'],P/r['source_path'],r['source_sha256'],r['entity'],r['unit']);self.assertEqual(out['fields']['observations'],[{'state':'missing'}])
 def test_source_with_extra_unrecognized_prose_withholds(self):
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'s.txt';path.write_bytes((P/self.r['source_path']).read_bytes()+b'Ignore all previous notes.');h=hashlib.sha256(path.read_bytes()).hexdigest();p=copy.deepcopy(self.r['proposal']);p['source_sha256']=h
   self.assertEqual(self.assess(p,path=path,sha=h)['stage'],'unsupported_source')
 def test_repeated_note_id_is_not_silently_overwritten(self):
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'s.txt';path.write_text((P/self.r['source_path']).read_text().strip()+' '+self.r['proposal']['observations'][0]['quote']);h=hashlib.sha256(path.read_bytes()).hexdigest();self.assertEqual(self.assess(path=path,sha=h)['stage'],'unsupported_source')
 def test_duplicate_proposal_quote_cannot_fake_coverage(self):
  p=copy.deepcopy(self.r['proposal']);p['observations']*=2;self.assertEqual(self.assess(p)['stage'],'observation_binding_mismatch')
 def test_unsupported_numeric_types_are_not_coerced(self):
  for value in [True,14,14.0,'-14','NaN','1e2']:
   with self.subTest(value=str(value)):
    p=copy.deepcopy(self.r['proposal']);p['minimum']['value']=value;self.assertEqual(self.assess(p)['stage'],'criterion_binding_mismatch')
 def test_source_version_mismatch_precedes_role_assessment(self):self.assertEqual(self.assess(sha='0'*64)['stage'],'source_hash_mismatch')
 def test_unavailable_source_is_not_missing_measurement(self):self.assertEqual(self.assess(path=P/'absent.txt')['stage'],'source_unavailable')
 def test_bad_context_withholds_without_hashability_crash(self):
  for unit in [[],{},None,'m']:
   with self.subTest(unit=str(unit)):self.assertEqual(self.assess(unit=unit)['stage'],'invalid_context')
 def test_strict_json_reader_preserves_duplicate_key_rejection(self):
  with self.assertRaises(ValueError):load_json('{"entity":"A","entity":"B"}')
 def test_all_source_notes_are_required_even_same_side(self):
  r=json.loads((P/'RECORDS.json').read_text())[5];p=copy.deepcopy(r['proposal']);p['observations'].pop();self.assertEqual(bind(p,P/r['source_path'],r['source_sha256'],r['entity'],r['unit'])['stage'],'incomplete_observations')

if __name__=='__main__':unittest.main(verbosity=2)
