"""Finite, deterministic, goal-free numeric world. No filesystem or model dependencies."""
from dataclasses import dataclass,asdict
import hashlib,json,re
VERSION='numeric-play-patch-v1'
CONTROLS=('LOOK','TOUCH A','TOUCH B')
@dataclass(frozen=True)
class Rules:
 version:str=VERSION
 lower:int=-8
 upper:int=8
 initial:int=0
 a_rule:str='increment_one'
 b_rule:str='negate'
 def validate(self):
  if self.version!=VERSION or self.a_rule!='increment_one' or self.b_rule!='negate':raise ValueError('Unsupported rules/version')
  if any(type(v) is not int for v in (self.lower,self.upper,self.initial)):raise ValueError('Integer bounds required')
  if not (-8<=self.lower<0<self.upper<=8 and self.lower==-self.upper and self.lower<=self.initial<=self.upper):raise ValueError('Symmetric finite bounds within[-8,8]required')
 def fingerprint(self):self.validate();return digest(asdict(self))
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def validate_state(value,rules):
 rules.validate()
 if type(value) is not int or not rules.lower<=value<=rules.upper:raise ValueError('World state outside declared domain')
def parse(reply):
 if not isinstance(reply,str):raise TypeError('Text reply required')
 t=reply.strip()
 if len(t)>4096:return 'INVALID' if re.match(r'^(?:LOOK|TOUCH)(?:\s|$)',t,re.I) else None
 if re.fullmatch(r'LOOK',t,re.I):return 'LOOK'
 m=re.fullmatch(r'TOUCH[ \t]+([AB])',t,re.I)
 if m:return 'TOUCH '+m.group(1).upper()
 if re.match(r'^(?:LOOK|TOUCH)(?:\s|$)',t,re.I):return 'INVALID'
 return None

def transition(value,reply,rules=Rules()):
 validate_state(value,rules);action=parse(reply);out=value;executed=False;status='no_world_action';message='Text recorded without a world action.'
 if action=='LOOK':executed=True;status='observed';message='Observed the current number.'
 elif action=='TOUCH A':
  executed=True
  if value==rules.upper:status='blocked';message='This action cannot change the number here. Other controls remain available.'
  else:out=value+1;status='changed';message='The number changed.'
 elif action=='TOUCH B':
  executed=True;out=-value;status='changed' if out!=value else 'unchanged';message='The number changed.' if out!=value else 'The action was accepted; the number stayed the same.'
 elif action=='INVALID':status='invalid_action';message='Use one complete LOOK, TOUCH A, or TOUCH B reply. Other text can be recorded without a world action.'
 receipt=dict(kind='play_patch_receipt',world_version=rules.version,rules_sha256=rules.fingerprint(),recognized_world_action=action is not None,executed=executed,action=action,status=status,before=dict(number=value),after=dict(number=out),message=message)
 validate_state(out,rules);return out,receipt

def view(value,rules=Rules()):
 validate_state(value,rules)
 # Deliberately no formulas,worked examples,hidden-rule names or rewards in model-facing text.
 return ('OPTIONAL PLAY PATCH (actual host world)\n'
         f'Current number: {value}. Its range is {rules.lower} to {rules.upper}. Objects: A and B.\n'
         'Controls: LOOK, TOUCH A, TOUCH B. Use one complete command as a reply, or write ordinary text.\n'
         'The number persists between entries and pauses. Accepted actions return actual observations. There is no target or score.')
