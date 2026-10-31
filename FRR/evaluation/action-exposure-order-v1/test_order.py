import unittest
from collections import Counter
from study import render,ACTIONS,DESCRIPTIONS,command

CASE={'target':'Rowan','visible':'Plot: Rowan\nStatus: positive','archive_available':True}

class OrderTests(unittest.TestCase):
    def test_every_fixed_item_visits_every_position(self):
        for a in ACTIONS:
            self.assertEqual(sorted((ACTIONS[k:]+ACTIONS[:k]).index(a)+1 for k in range(6)),list(range(1,7)))

    def test_order_changes_keep_all_words_and_labels(self):
        texts=[render(CASE,k,o) for k in range(6) for o in ('evidence_first','menu_first')]
        self.assertTrue(all(Counter(t.split())==Counter(texts[0].split()) for t in texts))
        self.assertTrue(all(all(a+': '+DESCRIPTIONS[a] in t for a in ACTIONS) for t in texts))

    def test_hidden_scoring_metadata_not_in_prompt(self):
        self.assertEqual(render({**CASE,'desired_action':'UNKNOWN','state':'missing'},0,'evidence_first'),render(CASE,0,'evidence_first'))
        self.assertIsNone(command('NOW'))

if __name__=='__main__':unittest.main()
