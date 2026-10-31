from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parent))
from plain import first_action,plain_prompt

class PlainTests(unittest.TestCase):
    def test_prefix_allows_extra_text_and_case(self):
        self.assertEqual(first_action('  target: fetch the record'),'TARGET')
        self.assertEqual(first_action('YES\nexplanation'),'YES')

    def test_complete_word_boundary_and_no_interior_guess(self):
        self.assertIsNone(first_action('NOW is the time'))
        self.assertIsNone(first_action('I choose TARGET'))
        self.assertIsNone(first_action('WITHHOLDING'))

    def test_hidden_state_does_not_enter_plain_prompt(self):
        c={'target':'Rowan','visible':None,'archive_available':True,'source':'hidden1','state':'positive'}
        self.assertEqual(plain_prompt(c,'forward'),plain_prompt({**c,'source':'hidden2','state':'zero'},'forward'))

if __name__=='__main__':unittest.main()
