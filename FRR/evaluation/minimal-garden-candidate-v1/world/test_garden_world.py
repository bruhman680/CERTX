"""Real disposable sandbox tests; no neural inference or canonical writes."""
from pathlib import Path
import json, tempfile, unittest
from unittest.mock import patch
from garden_world import GardenWorld, WorldFault, PendingOutcome, parse_notebook, verify_store, FROZEN, read

class ParserTests(unittest.TestCase):
    def test_exact_sources_offsets_and_unicode(self):
        text = '🌱 prose\r\n```python\r\nprint(6*7)\r\n```\r\nend'
        result = parse_notebook(text)
        self.assertEqual(result['complete_executable_cells'],1)
        cell = result['cells'][0]
        self.assertEqual(cell['source'],'print(6*7)\r\n')
        self.assertEqual(text[cell['source_start']:cell['source_end']],cell['source'])
        raw = text.encode()
        self.assertEqual(raw[cell['source_start_utf8']:cell['source_end_utf8']],cell['source'].encode())

    def test_unknown_fences_shield_inner_cells(self):
        for opener,closer in [('```json','```'),('```text example','```'),('````python','````'),('```python ','```')]:
            text = opener+'\n```python\nprint(42)\n```\n'+closer+'\n'
            self.assertEqual(parse_notebook(text)['complete_executable_cells'],0)

    def test_incomplete_indented_and_wrong_case_are_literal(self):
        for text in ['```python\nprint(42)',' ```python\nprint(42)\n ```','```Python\nprint(42)\n```']:
            self.assertEqual(parse_notebook(text)['complete_executable_cells'],0)

    def test_fence_close_must_be_exact(self):
        for close in ['``` ','````',' ```']:
            self.assertEqual(parse_notebook('```python\nprint(42)\n'+close)['complete_executable_cells'],0)

class WorldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Path(self.temp.name)/'world'
        self.w = GardenWorld.create(self.store,FROZEN/'run/bundles/001550.json',FROZEN/'run/objects')

    def tearDown(self):
        if self.w is not None:
            try:
                self.w.close()
            except WorldFault:
                pass
        self.temp.cleanup()

    def test_inherited_world_and_real_command(self):
        self.assertEqual(self.w.step,0)
        self.assertEqual(self.w.bundle,read(FROZEN/'run/bundles/001550.json'))
        result = self.w.apply('python','print(6*7)')
        self.assertEqual(result['receipt']['stdout'],'42\n')
        self.assertEqual(result['receipt']['exit_code'],0)
        self.assertEqual(verify_store(self.store)['step'],1)

    def test_note_and_legacy_receive_do_not_extract(self):
        text = '```python\nopen("should_not_run","w").write("bad")\n```'
        self.assertEqual(self.w.receive(text)['kind'],'notebook')
        names = [x[0] for x in self.w.bundle['entries']]
        self.assertNotIn('should_not_run',names)
        action = self.w.receive('{"action":"shell","source":"pwd"}')
        self.assertEqual(action['receipt']['stdout'],'/world\n')

    def test_notebook_executes_order_errors_and_persistence(self):
        text = '''prose remains writing
```python
open('memory.txt','w').write('17')
print('planted')
```
```python
1/0
```
```sh
cat memory.txt
```
'''
        result = self.w.receive_notebook(text)
        self.assertEqual(result['status'],'completed')
        self.assertEqual(len(result['operations']),4)
        self.assertEqual(result['operations'][1]['receipt']['stdout'],'planted\n')
        self.assertIn('ZeroDivisionError',result['operations'][2]['receipt']['stderr'])
        self.assertEqual(result['operations'][3]['receipt']['stdout'],'17')
        step = self.w.step
        bundle = self.w.checkpoint()
        self.w.close()
        self.w = GardenWorld.open(self.store)
        self.assertEqual(self.w.step,step)
        self.assertEqual(self.w.bundle,bundle)
        self.assertEqual(self.w.apply('shell','cat memory.txt')['receipt']['stdout'],'17')

    def test_each_cell_has_new_process_and_stdout_is_not_executed(self):
        result = self.w.receive_notebook('''```python
x=17
print("```sh\\ntouch should_not_run\\n```")
```
```python
print(x)
```
''')
        self.assertIn('NameError',result['operations'][2]['receipt']['stderr'])
        self.assertNotIn('should_not_run',[x[0] for x in self.w.bundle['entries']])

    def test_count_boundary_has_no_guest_effect(self):
        before = self.w.bundle
        result = self.w.receive_notebook('```sh\necho x\n```\n'*9)
        self.assertEqual(result['boundary'],'cell_count_limit')
        self.assertEqual(result['operations'],[])
        self.assertEqual(self.w.step,0)
        self.assertEqual(self.w.bundle,before)

    def test_full_notebook_reports_error_but_cleanup_cell_runs(self):
        self.assertEqual(self.w.apply('python',"open('notebook.txt','wb').write(b'x'*262144)")['receipt']['exit_code'],0)
        result = self.w.receive_notebook('```python\nopen("notebook.txt","w").write("recovered")\nprint("recovered")\n```')
        self.assertEqual(result['status'],'completed')
        self.assertFalse(result['note_stored'])
        self.assertIsNotNone(result['note_storage_fault'])
        self.assertNotEqual(result['operations'][0]['receipt']['exit_code'],0)
        self.assertEqual(result['operations'][1]['receipt']['stdout'],'recovered\n')
        self.assertEqual(self.w.apply('shell','cat notebook.txt')['receipt']['stdout'],'recovered')

    def test_notebook_symlink_cannot_write_host(self):
        victim = Path(self.temp.name)/'victim'
        victim.write_text('safe')
        source = 'rm notebook.txt; ln -s '+str(victim)+' notebook.txt'
        self.assertEqual(self.w.apply('shell',source)['receipt']['exit_code'],0)
        result = self.w.receive_notebook('```python\nprint(42)\n```')
        self.assertIsNotNone(result['note_storage_fault'])
        self.assertEqual(result['operations'][1]['receipt']['stdout'],'42\n')
        self.assertEqual(victim.read_text(),'safe')

    def test_isolation_and_tmp_clearing(self):
        self.assertNotEqual(self.w.apply('shell','cat /workspace/frr/CURRENT_HANDOFF.md')['receipt']['exit_code'],0)
        network = "import socket;socket.create_connection(('1.1.1.1',443),.1)"
        self.assertNotEqual(self.w.apply('python',network)['receipt']['exit_code'],0)
        self.assertEqual(self.w.apply('shell','echo temporary > /tmp/x')['receipt']['exit_code'],0)
        self.assertNotEqual(self.w.apply('shell','cat /tmp/x')['receipt']['exit_code'],0)

    def test_actual_output_and_time_limits(self):
        self.assertEqual(self.w.apply('shell','yes hello')['receipt']['boundary'],'output_limit')
        self.assertEqual(self.w.apply('shell','sleep 10')['receipt']['boundary'],'wall_time')
        self.assertEqual(self.w.apply('shell','echo alive')['receipt']['stdout'],'alive\n')

    def test_world_file_and_memory_limits(self):
        file = self.w.apply('shell','head -c 1000000 /dev/zero > limited')
        self.assertNotEqual(file['receipt']['exit_code'],0)
        entry = next(x for x in self.w.bundle['entries'] if x[0]=='limited')
        self.assertEqual(entry[4],262144)
        memory = self.w.apply('python','x=bytearray(100000000)')
        self.assertIn('MemoryError',memory['receipt']['stderr'])
        quota = self.w.apply('python',"from pathlib import Path\nfor i in range(40):\n Path('fill'+str(i)).write_bytes(b'x'*262144)")
        self.assertNotEqual(quota['receipt']['exit_code'],0)
        self.assertIn('No space left',quota['receipt']['stderr'])
        self.assertLessEqual(sum(x[4] for x in self.w.bundle['entries'] if x[1]=='file'),8388608)

    def test_unknown_partial_outcome_is_not_replayed(self):
        real = self.w._guest.execute
        def uncertain(source):
            real('echo partial > partial.txt')
            raise RuntimeError('fixture: response lost after action')
        with patch.object(self.w._guest,'execute',side_effect=uncertain):
            with self.assertRaises(WorldFault):
                self.w.apply('shell','echo requested')
        self.assertTrue((self.store/'PENDING.json').exists())
        self.assertTrue(read(self.store/'STATE.json')['faulted'])
        self.assertEqual(self.w.step,0)
        self.w.close()
        self.w = None
        with self.assertRaises(PendingOutcome):
            GardenWorld.open(self.store)
        self.assertFalse((self.store/'LOCK.json').exists())
        captures = list((self.store/'faults').glob('*_WORLD.json'))
        self.assertTrue(captures)
        self.assertIn('partial.txt',[x[0] for x in read(captures[0])['entries']])

    def test_close_checkpoint_failure_still_stops_runtime(self):
        pid = self.w._guest.p.pid
        self.w._guest.execute('echo uncommitted > drift.txt')
        with self.assertRaises(WorldFault):
            self.w.close()
        self.assertIsNotNone(self.w._guest.p.poll())
        self.assertTrue(read(self.store/'STATE.json')['paused'])
        self.assertTrue(read(self.store/'STATE.json')['faulted'])
        self.assertFalse((self.store/'LOCK.json').exists())
        self.w = None

    def test_notebook_partial_batch_blocks_resume_without_replay(self):
        real = self.w._guest.execute
        calls = []
        def uncertain(source):
            calls.append(source)
            result = real(source)
            if len(calls)==3:
                raise RuntimeError('fixture: lost response for second cell')
            return result
        text = '```sh\necho first > first.txt\n```\n```sh\necho second > second.txt\n```\n```sh\necho third > third.txt\n```'
        with patch.object(self.w._guest,'execute',side_effect=uncertain):
            with self.assertRaises(WorldFault):
                self.w.receive_notebook(text)
        self.assertEqual(len(calls),3)  # note, first cell, uncertain second; no third.
        self.assertEqual(self.w.step,2)
        self.assertEqual(len(read(self.store/'BATCH_PENDING.json')['operations']),2)
        self.assertTrue((self.store/'PENDING.json').exists())
        captures = list((self.store/'faults').glob('*_WORLD.json'))
        names = [x[0] for x in read(captures[0])['entries']]
        self.assertIn('first.txt',names)
        self.assertIn('second.txt',names)
        self.assertNotIn('third.txt',names)
        self.w.close()
        self.w = None
        with self.assertRaises(PendingOutcome):
            GardenWorld.open(self.store)

    def test_owned_lock_and_committed_history(self):
        self.w.apply('shell','echo honest')
        with self.assertRaises(FileExistsError):
            GardenWorld.open(self.store)
        self.assertTrue((self.store/'LOCK.json').exists())
        self.w.close()
        self.w = None
        event = self.store/'events/000001.json'
        value = read(event)
        value['source']='tampered'
        event.write_text(json.dumps(value))
        with self.assertRaises(WorldFault):
            GardenWorld.open(self.store)
        self.assertFalse((self.store/'LOCK.json').exists())

if __name__=='__main__':
    unittest.main(verbosity=2)
