"""Declared six-action language, version2; no fuzzy meaning or action execution."""
import re

ACTIONS=('YES','NO','WITHHOLD','FULL','TARGET','UNKNOWN')
DESCRIPTIONS={'YES':'answer positive','NO':'answer zero','WITHHOLD':'answer explicitly missing',
              'FULL':'request full source, cost2','TARGET':'request target record, cost1',
              'UNKNOWN':'report insufficient evidence'}

def normalize(text):
    value=' '.join(text.strip().split()).casefold()
    return value[:-1].rstrip() if value.endswith('.') else value

ALIASES={normalize(a):a for a in ACTIONS}
ALIASES.update({normalize(v):a for a,v in DESCRIPTIONS.items()})
ALIASES.update({'request full source':'FULL','request target record':'TARGET'})

def decode_v2(text):
    declarations=list(re.finditer(r'^[ \t]*ACTION:[ \t]*(.*)$',text,re.I|re.M))
    if declarations:
        last=declarations[-1];surface=last[1]
        action=ALIASES.get(normalize(surface))
        return {'action':action,'method':'declaration' if action else 'unsupported_declaration',
            'surface':surface,'declarations':len(declarations),
            'trailing_text':bool(text[last.end():].strip())}
    action=ALIASES.get(normalize(text))
    return {'action':action,'method':'bare' if action else 'unsupported',
            'surface':text.strip(),'declarations':0,'trailing_text':False}

def decode_v1(text):
    # Exact frozen earlier command behavior, retained as a comparison view.
    matches=list(re.finditer(r'^\s*ACTION:\s*(YES|NO|WITHHOLD|FULL|TARGET|UNKNOWN)\b',text,re.I|re.M))
    if matches:return matches[-1][1].upper()
    m=re.match(r'^\s*(YES|NO|WITHHOLD|FULL|TARGET|UNKNOWN)\b',text,re.I)
    return m[1].upper() if m else None

def fixtures():
    data=[]
    for a in ACTIONS:
        for t in (a,'ACTION: '+a,DESCRIPTIONS[a],'ACTION: '+DESCRIPTIONS[a]):
            data.append({'text':t,'expected':a,'kind':'declared_positive'})
    for t,a in [('  action: REPORT INSUFFICIENT EVIDENCE.  ','UNKNOWN'),
                ('ACTION: request target record','TARGET'),('ACTION: request full source','FULL'),
                ('ACTION: YES\nACTION: UNKNOWN','UNKNOWN')]:data.append({'text':t,'expected':a,'kind':'declared_positive'})
    for t in ['ACTION: Report sufficient evidence','ACTION: do not report insufficient evidence',
              'ACTION: not UNKNOWN','ACTION: UNKNOWN is not appropriate','ACTION: answer not positive',
              'ACTION: do not request target record','ACTION: request wrong record',
              'ACTION: request target record, cost9','ACTION: YES or NO','ACTION: YES\nACTION: not YES',
              'ACTION: report insufficient evidence\nACTION: report sufficient evidence',
              'UNKNOWNish','I might request target record','UNKNOWN?','']:
        data.append({'text':t,'expected':None,'kind':'unsupported_or_negative'})
    return data
