"""Notebook is the default; only an exact explicit action envelope is executed.

No inference or primary-history changes on import. Old shell-every-reply pilot
remains an immutable earlier experiment.
"""
from pathlib import Path
import importlib.util, json
P=Path(__file__).resolve().parent.parent/'persistent-cloud-workspace-v1/workspace.py'
spec=importlib.util.spec_from_file_location('isolated_workspace',P)
world=importlib.util.module_from_spec(spec);spec.loader.exec_module(world)
NOTICE='''Ordinary replies are notebook writing and are not executed. Writing may remain unfinished or take any form. To execute a shell script instead, the whole reply must be a JSON object with exactly these two fields: "action": "shell", "source": a string containing the script. All other replies remain notebook writing. Files in /world persist. Shell actions return their actual stdout, stderr and exit status. No action is required.'''

def interpret(text):
    try: value=json.loads(text)
    except (ValueError,TypeError): return None
    if (isinstance(value,dict) and set(value)=={'action','source'}
        and value['action']=='shell' and isinstance(value['source'],str)):
        return value['source']
    return None

def receive(home, observer, entry, text):
    """Caller retains authoritative evidence outside the guest mount.

    The model may edit its notebook file; that cannot rewrite the external raw
    record. An existing entry is never executed again automatically.
    """
    home=Path(home).resolve(strict=True);observer=Path(observer).resolve(strict=True)
    if observer==home or home in observer.parents:
        raise ValueError('Observer records must be outside the model workspace')
    if not isinstance(entry,int) or entry<0: raise ValueError('Invalid entry')
    raw=observer/f'{entry:06d}_RAW.json'
    # Durable external record precedes notebook append or action side effects.
    with raw.open('x') as f:
        json.dump({'entry':entry,'text':text},f,ensure_ascii=False);f.write('\n');f.flush()
        import os;os.fsync(f.fileno())
    source=interpret(text)
    if source is None:
        # Append through the same sandbox: a guest symlink cannot redirect a
        # host-side notebook write into protected host files.
        append="python3 -c "+__import__('shlex').quote(
            "with open('notebook.txt','a',encoding='utf-8') as f: f.write("+repr(text+'\n')+")")
        effect=world.execute(home,append)
        result={'kind':'notebook','execution_requested':False,
                'storage_effect':effect}
        # Storage faults are actual environment consequences, not invalid thought.
        visible='' if effect['exit_code']==0 and not effect['boundary'] else effect['stderr']
    else:
        effect=world.execute(home,source)
        result={'kind':'shell','execution_requested':True,'effect':effect}
        visible=json.dumps({k:effect[k] for k in ['stdout','stderr','exit_code','boundary']})
    result['visible_feedback']=visible
    with (observer/f'{entry:06d}_RESULT.json').open('x') as f:
        json.dump(result,f,ensure_ascii=False);f.write('\n')
    return result
