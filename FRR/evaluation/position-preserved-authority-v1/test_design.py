import unittest,os
os.environ['HF_HUB_OFFLINE']='1'
from transformers import AutoTokenizer
from design import build,cases,MAP
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False);cls.qs,cls.audit=build(cls.tok)
 def test_counts_balance(self):
  self.assertEqual(len(self.qs),151);self.assertEqual(len({q['prompt'] for q in self.qs}),151)
  for split in ('discovery','confirmation'):
   cs=[c for c in cases() if c['split']==split];self.assertEqual(len(cs),8)
   for state in MAP:self.assertEqual(sum(c['state']==state for c in cs),2)
 def test_positions_and_prefix(self):
  for c in cases():
   for content in ('duplicate','filler'):
    for family in ('memo','paper'):
     rows=[q for q in self.qs if q['case_id']==c['id'] and q['content']==content and q['family']==family];self.assertEqual(len(rows),2)
     self.assertEqual(rows[0]['prompt'].split(c['prompt'])[0],rows[1]['prompt'].split(c['prompt'])[0])
     a=[x for x in self.audit['record_spans'] if x['case_id']==c['id'] and any(x['condition']==q['condition'] for q in rows)];self.assertEqual(a[0]['record_span'],a[1]['record_span'])
 def test_lengths_observation(self):
  by={c['id']:c for c in cases()}
  for q in self.qs:
   if q['condition']=='legacy_anchor':continue
   self.assertIn(by[q['case_id']]['prompt'],q['prompt'])
   if q['condition']!='original':self.assertEqual(len(self.tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)),self.audit['matched_tokens'])
if __name__=='__main__':unittest.main()
