"""Two small visible-record grammars, policy affordances and public response parsing."""
import re
from evidence import MAPPING,parse
from routing_reference import ACTIONS,retrieve,terminal

ORDER=('UNKNOWN','YES','TARGET','WITHHOLD','NO','FULL')
DESCRIPTIONS={'YES':'answer positive','NO':'answer zero','WITHHOLD':'answer explicitly missing',
              'FULL':'request full source, cost2','TARGET':'request target record, cost1',
              'UNKNOWN':'report insufficient evidence'}

def normalized_visible(case):
    text=case['visible_display']
    if text is None:return None
    m=re.fullmatch(r'Plot: ([A-Za-z]+)\nStatus: (positive|zero|missing)',text)
    if m is None:m=re.fullmatch(r'\[plot=([A-Za-z]+); status=(positive|zero|missing)\]',text)
    if m is None:raise ValueError('Visible record outside the two declared formats')
    return f'Plot: {m[1]}\nStatus: {m[2]}'

def view(case):
    return ('Target plot: '+case['target']+'\nVisible record:\n'+
        (case['visible_display'] if case['visible_display'] is not None else '(no visible record)')+
        '\nArchive accessible: '+('yes' if case['archive_available'] else 'no'))

def example_text():
    lessons=[('Iris','Plot: Iris\nStatus: positive',True,'YES'),
             ('Iris','Plot: Iris\nStatus: zero',True,'NO'),
             ('Iris','Plot: Iris\nStatus: missing',True,'WITHHOLD'),
             ('Iris',None,True,'TARGET'),
             ('Iris','Plot: Moss\nStatus: zero',True,'TARGET'),
             ('Iris',None,False,'UNKNOWN')]
    return '\n\n'.join('Example '+str(i+1)+':\n'+view({'target':t,'visible_display':v,'archive_available':a})+
                        '\nACTION: '+action for i,(t,v,a,action) in enumerate(lessons))

def render(case,examples,response):
    header=('Determine the target status. YES=positive; NO=zero; WITHHOLD=recorded missing. '
            'UNKNOWN means insufficient evidence. At most one archive request is allowed.\n')
    menu='\n'.join(a+': '+DESCRIPTIONS[a] for a in ORDER)
    lesson='\n\nWorked examples:\n'+example_text() if examples else ''
    instruction=('Write a brief one-sentence action plan, then finish with ACTION: and one action word.'
        if response=='plan64' else 'Finish with ACTION: and one action word. No explanation is needed.')
    return header+'\nActions:\n'+menu+lesson+'\n\nCurrent task:\n'+view(case)+'\n\n'+instruction+'\nResponse:'

def decode_action(text):
    matches=list(re.finditer(r'^\s*ACTION:\s*(YES|NO|WITHHOLD|FULL|TARGET|UNKNOWN)\b',text,re.I|re.M))
    if matches:
        m=matches[-1]
        return {'action':m[1].upper(),'method':'final_tag','tag_count':len(matches),
                'text_before_final_tag':text[:m.start()].strip()}
    m=re.match(r'^\s*(YES|NO|WITHHOLD|FULL|TARGET|UNKNOWN)\b',text,re.I)
    return {'action':m[1].upper() if m else None,'method':'leading_word' if m else 'invalid',
            'tag_count':0,'text_before_final_tag':''}

def eval_case(case):
    return {**case,'visible':normalized_visible(case)}

def observed_rule(case):
    visible=normalized_visible(case)
    if visible is not None:
        name,status=re.fullmatch(r'Plot: ([A-Za-z]+)\nStatus: (positive|zero|missing)',visible).groups()
        if name==case['target']:return MAPPING[status]
    return 'TARGET' if case['archive_available'] else 'UNKNOWN'

def finish_route(case,action,worker_state=None,tool=None):
    return terminal(eval_case(case),action,worker_state,tool)
