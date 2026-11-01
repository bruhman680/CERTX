import unittest
from collections import Counter
from decoder import decode_v1,decode_v2,fixtures
from domain import render,guidance_text

CASE={'target':'Clover','visible_display':None,'archive_available':True}

class DescriptionTests(unittest.TestCase):
    def test_all_declared_positive_and_negative_fixtures(self):
        for x in fixtures():
            with self.subTest(text=x['text']):self.assertEqual(decode_v2(x['text'])['action'],x['expected'])

    def test_last_unsupported_declaration_cannot_revive_earlier_action(self):
        t='ACTION: YES\nACTION: not YES'
        self.assertEqual(decode_v1(t),'YES');self.assertIsNone(decode_v2(t)['action'])

    def test_opposite_meanings_and_bare_menu_echo_not_guessed(self):
        self.assertEqual(decode_v2('ACTION: Report insufficient evidence')['action'],'UNKNOWN')
        self.assertIsNone(decode_v2('ACTION: Report sufficient evidence')['action'])
        self.assertIsNone(decode_v2('YES: answer positive\nNO: answer zero')['action'])

    def test_query_does_not_read_hidden_state_kind_or_source(self):
        c={**CASE,'state':'positive','source':'hidden1','kind':'one'}
        d={**CASE,'state':'missing','source':'hidden2','kind':'two'}
        self.assertEqual(render(c,'rule',0),render(d,'rule',0))

    def test_rule_and_example_rotations_preserve_words(self):
        for kind,n in [('rule',3),('examples',6)]:
            words=Counter(guidance_text(kind,0).split())
            self.assertTrue(all(Counter(guidance_text(kind,k).split())==words for k in range(n)))

if __name__=='__main__':unittest.main()
