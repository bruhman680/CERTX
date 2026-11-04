import unittest,json
import capacity,seeds
class Capacity(unittest.TestCase):
 def test_native_budget_and_unchanged_sampler(self):
  self.assertEqual(capacity.LIMIT+96,json.loads((capacity.parent.BASE/'config.json').read_text())['max_position_embeddings'])
  old=(capacity.R/'generate_continuous.py').read_text();self.assertEqual((capacity.R/'generate_capacity.py').read_text(),old.replace('len(ids)>6144','len(ids)>8096'))
 def test_identical_prompt_and_preserved_origin(self):
  events=capacity.Journal(capacity.ENV).state()[1];self.assertEqual(len(events),65);self.assertEqual(capacity.seed_render(events),seeds.seed_render(events))
  self.assertEqual(capacity.parent.FEEDBACK,seeds.parent.FEEDBACK);self.assertEqual((capacity.ENV/'seed_shelf/0001.json').read_bytes(),(seeds.ENV/'seed_shelf/0001.json').read_bytes())
 def test_same_reader_and_play_actions(self):
  self.assertEqual(capacity.play_dispatch('TRY 2 + 3',[],capacity.parent.dispatch),seeds.play_dispatch('TRY 2 + 3',[],seeds.parent.dispatch));self.assertTrue(capacity.parent.dispatch('READ SETUP','tools_optional')['executed'])
if __name__=='__main__':unittest.main()
