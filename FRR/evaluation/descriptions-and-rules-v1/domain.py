"""Literal-source next-action task; rule/example order varies, query facts do not."""
from decoder import DESCRIPTIONS
from task_reference import view,example_text,finish_route,observed_rule

ORDER=('UNKNOWN','YES','TARGET','WITHHOLD','NO','FULL')
CLAUSES=(
    'When the visible record names the target, answer its recorded status.',
    'When the target record is not visible and the archive is accessible, request TARGET.',
    'When the target record is not visible and the archive is unavailable, report UNKNOWN.')

def guidance_text(kind,rotation):
    if kind=='none':return ''
    if kind=='rule':
        seq=CLAUSES[rotation:]+CLAUSES[:rotation]
        return ('\n\nRules:\nA visible record belongs to the target only when its plot name matches the target name.\n'+
                '\n'.join(seq))
    blocks=example_text().split('\n\n');assert len(blocks)==6
    return '\n\nWorked examples:\n'+'\n\n'.join(blocks[rotation:]+blocks[:rotation])

def render(case,kind,rotation):
    menu='\n'.join(a+': '+DESCRIPTIONS[a] for a in ORDER)
    return ('Determine the target status. YES=positive; NO=zero; WITHHOLD=recorded missing. '
            'UNKNOWN means insufficient evidence. At most one archive request is allowed.\n\nActions:\n'+
            menu+guidance_text(kind,rotation)+'\n\nCurrent task:\n'+view(case)+
            '\n\nFinish with one ACTION: line. Use an action word or its exact description.\nResponse:')
