"""Contact-policy checks; no neural generation or original-world mutation."""
from pathlib import Path
import json, tempfile, unittest
from unittest.mock import patch
import candidate

class ContactTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = Path(self.tmp.name)
        (self.r/'events').mkdir()
        self.initial = [{'role':'system','content':''},{'role':'user','content':'physical rules\n'+candidate.SEED}]
        (self.r/'INITIAL_MESSAGES.json').write_text(json.dumps(self.initial))
        (self.r/'CONTROL_TASKS.json').write_text('{}')

    def tearDown(self):
        self.tmp.cleanup()

    def test_open_context_preserves_all_actual_turns_and_feedback(self):
        rows = [{'text':'one','feedback':''},{'text':'two','feedback':'actual stderr'}]
        actual = candidate.messages(self.r,rows)
        self.assertEqual(actual,self.initial+[
            {'role':'assistant','content':'one'},{'role':'user','content':''},
            {'role':'assistant','content':'two'},{'role':'user','content':'actual stderr'}])
        self.assertEqual(sum(candidate.SEED in x['content'] for x in actual),1)
        self.assertFalse(any('Directory entries:' in x['content'] for x in actual))

    def test_control_tasks_attach_to_correct_receipt_without_rewriting_history(self):
        (self.r/'CONTROL_TASKS.json').write_text(json.dumps({'1':'first task','2':'second task'}))
        before = candidate.messages(self.r,[])
        self.assertEqual(before[-1]['content'],self.initial[-1]['content']+'\n\nfirst task')
        after = candidate.messages(self.r,[{'text':'raw result','feedback':'actual receipt'}])
        self.assertEqual(after[-3]['content'],before[-1]['content'])
        self.assertEqual(after[-1]['content'],'actual receipt\n\nsecond task')

    def test_known_note_error_and_cell_error_remain_truthful(self):
        def op(channel,stderr,exit_code):
            return {'channel':channel,'feedback':{'stdout':'','stderr':stderr,'exit_code':exit_code,
                'boundary':None,'seconds':10,'observer_judgment':'irrelevant'}}
        batch = {'boundary':None,'operations':[op('note','File too large',1),op('python','ZeroDivisionError',1)]}
        observed = json.loads(candidate.project_feedback(batch))
        self.assertEqual([r['stderr'] for r in observed['receipts']],['File too large','ZeroDivisionError'])
        self.assertTrue(all('seconds' not in r and 'observer_judgment' not in r for r in observed['receipts']))
        self.assertEqual(candidate.project_feedback({'boundary':None,'operations':[{'feedback':None}]}),'')

    def test_capacity_reserves_output_space(self):
        self.assertEqual(candidate._body.MAX_INPUT+candidate._body.MAX_OUTPUT,8192)
        class Tokenizer:
            def apply_chat_template(self,*a,**kw):
                return [1]*(candidate._body.MAX_INPUT+1)
        class Model:
            def __call__(self,*a,**kw):
                raise AssertionError('Model must not run past exact capacity')
        with self.assertRaisesRegex(ValueError,'capacity'):
            candidate._body.generate(Model(),Tokenizer(),[],None,'capacity-test')

    def test_competing_resume_cannot_remove_owners_lock(self):
        (self.r/'RUN.lock').write_text('{"token":"existing owner"}')
        with self.assertRaises(FileExistsError):
            candidate.run(self.r,1)
        self.assertEqual((self.r/'RUN.lock').read_text(),'{"token":"existing owner"}')
        self.assertEqual(list((self.r/'events').iterdir()),[])

if __name__=='__main__':
    unittest.main(verbosity=2)
