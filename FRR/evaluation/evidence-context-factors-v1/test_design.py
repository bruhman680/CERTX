import unittest
from collections import Counter
from pathlib import Path
import os
os.environ['HF_HUB_OFFLINE']='1'
from transformers import AutoTokenizer
from design import cases,build,render,MAP
class Contracts(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tok=AutoTokenizer.from_pretrained('/workspace/cache_backend_models/smollm2-135m',local_files_only=True,trust_remote_code=False);cls.qs,cls.padding=build(cls.tok)
 def test_balance_and_untouched_original(self):
  cs=cases();self.assertEqual(len(cs),16)
  for split in ('discovery','confirmation'):self.assertEqual(Counter(c['expected'] for c in cs if c['split']==split),{v:2 for v in MAP.values()})
  by={c['id']:c for c in cs}
  for q in self.qs:
   if q['condition']=='legacy_anchor':continue
   c=by[q['case_id']];self.assertIn(c['prompt'],q['prompt'])
   if q['content']=='duplicate':self.assertEqual(q['prompt'].count(c['record']),2)
   if c['state']=='absent':self.assertNotIn('Status:',c['record'])
 def test_factor_pairs_and_padding(self):
  qs=[q for q in self.qs if q['condition'] not in ('original','legacy_anchor')]
  self.assertEqual(len(qs),144)
  for q in qs:
   ids=self.tok.apply_chat_template([{'role':'user','content':q['prompt']}],tokenize=True,add_generation_prompt=True)
   self.assertEqual(len(ids),self.padding['global_matched_token_count'])
  for c in cases():
   rows=[q for q in self.qs if q['case_id']==c['id'] and q['content'] in ('duplicate','filler')];self.assertEqual(len(rows),8)
   self.assertEqual({(q['content'],q['authority'],q['placement']) for q in rows},{(k,a,p) for k in ('duplicate','filler') for a in (False,True) for p in ('before','after')})
 def test_no_filler_answer_content_and_counts(self):
  self.assertEqual(len(self.qs),167);self.assertEqual(len({q['prompt'] for q in self.qs}),167)
  for q in self.qs:
   if q['content']=='filler':self.assertIn('Evidence note:\nReference material.',q['prompt'])
if __name__=='__main__':unittest.main()
