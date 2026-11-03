import unittest,tempfile,json
from pathlib import Path
import continuous as c
class Persistence(unittest.TestCase):
 def setup_journal(self,d):
  p=Path(d);(p/'events').mkdir();(p/'ORIGIN.jsonl').write_text('');(p/'ENVIRONMENT.json').write_text('{}');return c.Journal(p)
 def test_immutable_commit_and_stale_cursor_recovery(self):
  with tempfile.TemporaryDirectory() as d:
   j=self.setup_journal(d);row=dict(step=0,text='READ SETUP',host_result=dict(kind='source_receipt'))
   j.commit(row);before=(Path(d)/'events/000000.json').read_bytes();(Path(d)/'STATE.json').write_text('{}');j.project();self.assertEqual(json.loads((Path(d)/'STATE.json').read_text())['next_step'],1)
   with self.assertRaises(FileExistsError):c.immutable(Path(d)/'events/000000.json',row)
   self.assertEqual(before,(Path(d)/'events/000000.json').read_bytes())
 def test_pause_does_not_change_notebook_or_prompt(self):
  with tempfile.TemporaryDirectory() as d:
   j=self.setup_journal(d);j.project();before=(Path(d)/'NOTEBOOK.jsonl').read_bytes();q=c.parent.render([],'tools_optional');(Path(d)/'PAUSE').touch();self.assertFalse(c.wait_pacing(d,0));j.project();self.assertEqual(before,(Path(d)/'NOTEBOOK.jsonl').read_bytes());self.assertEqual(q,c.parent.render([],'tools_optional'))
 def test_existing_branch_and_sampler(self):
  self.assertEqual(c.BRANCH,'tools_optional_1201');self.assertEqual(len((c.P/'run/notebooks'/f'{c.BRANCH}.jsonl').read_text().splitlines()),48)
  expected=(c.R/'generate.py').read_text().replace('len(ids)>4096','len(ids)>6144');self.assertEqual(expected,(c.R/'generate_continuous.py').read_text())
if __name__=='__main__':unittest.main()
