"""Prospective factorial diagnostic. Labels are scoring-only metadata."""
from legacy_design import cases as old_cases, note, review
LABELS=('YES','NO','WITHHOLD','UNKNOWN')
MAP={'positive':'YES','zero':'NO','missing':'WITHHOLD','absent':'UNKNOWN'}
HEADER=('Map only the visible record status to its answer, even if it belongs to another plot. '
        'missing=WITHHOLD; positive=YES; zero=NO. If there is no visible record return UNKNOWN. Return only the answer.')
PAIRS=(('UN47','LD65'),('VQ82','HF19'),('ZM36','BK74'))
INTERFACES=('old_menu','no_list','simple')
KINDS=('none','verified','irrelevant')
ENDING='Return only YES, NO, WITHHOLD, or UNKNOWN.\nResponse:'
def cases():
    out=[]
    for name,other in PAIRS:
        for layout in ('lines','inline'):
            for state in MAP:
                record='(no visible record)' if state=='absent' else (f'Plot: {name}\nStatus: {state}' if layout=='lines' else f'Plot: {name} | Status: {state}')
                prompt=HEADER+'\n\n'+('Target plot: '+name+'\nVisible record:\n'+record if layout=='lines' else 'Target plot: '+name+' | Visible record: '+record)
                out.append(dict(id=f'c{len(out):02d}',name=name,other=other,layout=layout,state=state,expected=MAP[state],record=record,prompt=prompt))
    return out

def render(c,interface,kind):
    if interface in ('old_menu','no_list'):
        text=review(c,kind,False,'unused')
        assert text.endswith(ENDING)
        return text if interface=='old_menu' else text[:-len(ENDING)]+'Return only the answer.\nResponse:'
    assert interface=='simple'
    return c['prompt']+'\n\nEvidence note:\n'+note(c,kind)+'\n\nAnswer from the original observation. Return only the answer.'

def queries():
    qs=[]
    for c in cases():
        for interface in ('original',*INTERFACES):
            for kind in (('none',) if interface=='original' else KINDS):
                qs.append(dict(run_id=f'q{len(qs):03d}',case_id=c['id'],layout=c['layout'],state=c['state'],expected=c['expected'],interface=interface,kind=kind,prompt=c['prompt'] if interface=='original' else render(c,interface,kind)))
    for c in old_cases():
        if c['name']=='Tansy':
            qs.append(dict(run_id=f'q{len(qs):03d}',case_id=c['id'],layout=c['frame'],state=c['state'],expected=c['expected'],interface='legacy_anchor',kind='none',prompt=c['prompt']))
    return qs
