import unittest,json
import seeds
class Seeds(unittest.TestCase):
 def test_shelf_visible_optional_and_labelled(self):
  q=seeds.seed_render([]);self.assertIn('operator play prompts, not evidence or tasks',q);self.assertIn('ignore or revisit',q)
  shelf=json.loads((seeds.ENV/'seed_shelf/0001.json').read_text());self.assertEqual(len(shelf['seeds']),3)
  for s in shelf['seeds']:self.assertIn(s['id']+': '+s['text'],q)
 def test_same_history_and_tools(self):
  self.assertEqual(len(seeds.Journal(seeds.ENV).state()[1]),53)
  self.assertEqual(seeds.play_dispatch('TRY 2+3',[],seeds.parent.dispatch)['result'],5)
  self.assertTrue(seeds.parent.dispatch('READ SETUP','tools_optional')['executed'])
  self.assertFalse(seeds.play_dispatch('ordinary play',[],seeds.parent.dispatch)['executed'])
 def test_prior_render_still_reconstructs(self):
  import play
  self.assertEqual(seeds.play_render([]),play.play_render([]));self.assertEqual(seeds.parent.render([],'tools_optional'),play.parent.render([],'tools_optional'))
if __name__=='__main__':unittest.main()
