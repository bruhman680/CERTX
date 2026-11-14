"""Actual sandbox fault paths, operator diagnostics only; no model inference."""
from pathlib import Path
import json
import prototype as p

def main():
    before=p.inventory(p.C);src=json.loads((p.V/'SOURCE_ARCHIVE.json').read_text())
    parent=p.C/'run/world/bundles/000031.json'
    rules=p.new_rules((p.C/'ENVIRONMENT.md').read_text());rows=[]
    for label in ['file_collision','symlink_parent']:
        store=p.H/'fault_worlds'/label;store.parent.mkdir(exist_ok=True)
        w=p.GardenWorld.create(store,parent,p.C/'run/world/objects',parent_entry=1580)
        try:
            init=w.apply('python',p.initialization_source(src,rules));p.save(f'faults/{label}_initialization.json',init)
            assert init['feedback']['exit_code']==0
            if label=='file_collision':
                setup="from pathlib import Path\np=Path('conversation_archive_v1/entries/001581.json')\np.write_text('model-owned collision')\n"
            else:
                setup="from pathlib import Path\np=Path('conversation_archive_v1')\n(p/'entries').rename(p/'saved_entries')\n(p/'entries').symlink_to('saved_entries',target_is_directory=True)\n"
            event=w.apply('python',setup);p.save(f'faults/{label}_setup.json',event);assert event['feedback']['exit_code']==0
            failed=w.apply('python',p.archive_source(1581,'unwritten new assistant','actual model-action feedback'))
            p.save(f'faults/{label}_archive_failure.json',failed)
            assert failed['feedback']['exit_code']!=0 and failed['changed_paths']==[]
            combined=p.combined_feedback('',failed);data=json.loads(combined)
            assert len(data['receipts'])==1 and data['receipts'][0]['channel']=='history_archive'
            assert data['receipts'][0]['stderr']==failed['feedback']['stderr']
            following=w.apply('python',"from pathlib import Path\nPath('following_cell.txt').write_text('5')\nprint(5)\n")
            p.save(f'faults/{label}_following_cell.json',following)
            assert following['feedback']['exit_code']==0 and following['feedback']['stdout']=='5\n'
        finally:w.close()
        w=p.GardenWorld.open(store)
        try:
            if label=='file_collision':
                read="from pathlib import Path\nassert Path('conversation_archive_v1/entries/001581.json').read_text()=='model-owned collision'\nassert Path('following_cell.txt').read_text()=='5'\nprint('collision retained')\n"
            else:
                read="from pathlib import Path\np=Path('conversation_archive_v1')\nassert (p/'entries').is_symlink()\nassert not (p/'saved_entries/001581.json').exists()\nassert len(list((p/'saved_entries').glob('*.json')))==30\nassert Path('following_cell.txt').read_text()=='5'\nprint('symlink retained; target unchanged')\n"
            read_event=w.apply('python',read);p.save(f'faults/{label}_read_after_reopen.json',read_event)
            assert read_event['feedback']['exit_code']==0 and read_event['changed_paths']==[]
        finally:w.close()
        rows.append({'case':label,'copy_failed_known':True,'no_overwrite_or_repair':True,
          'actual_failure_in_combined_feedback':True,'following_cell_succeeded':True,'reopen_check_passed':True,
          'world_verification':p.verify_store(store)})
    assert before==p.inventory(p.C)
    p.save('FAULT_TEST_RESULTS.json',{'status':'pass','cases':rows,'canonical_unchanged':True,
       'model_calls':0,'scope':'operator-created collision/symlink faults on independent worlds; not hard crash/power loss'})
    print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
