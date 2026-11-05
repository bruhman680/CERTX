"""Ready pure bridge: primary event receipts, not a second mutable world log, own live state."""
from dataclasses import dataclass
from world import Rules,transition,parse,view,digest
@dataclass(frozen=True)
class Binding:
 activation_step:int
 rules:Rules=Rules()
 def __post_init__(self):
  self.rules.validate()
  if type(self.activation_step) is not int or self.activation_step<0:raise ValueError('Explicit activation boundary required')
 def replay(self,events):
  if len(events)<self.activation_step:raise ValueError('History does not reach world boundary')
  if any(e['step']!=i for i,e in enumerate(events)):raise ValueError('Noncontiguous primary history')
  value=self.rules.initial
  for step,e in enumerate(events[self.activation_step:],self.activation_step):
   if e['step']!=step:raise ValueError('Noncontiguous primary history')
   reply=e['reply'];host=e['host_result'];after,expected=transition(value,reply,self.rules)
   if parse(reply) is not None:
    if host!=expected:raise ValueError('Missing/forged/stale world receipt')
    value=after
   elif host.get('kind')=='play_patch_receipt':raise ValueError('World receipt without world command')
  return value
 def dispatch(self,reply,events,legacy_dispatch):
  value=self.replay(events)
  if parse(reply) is not None:return transition(value,reply,self.rules)[1]
  return legacy_dispatch(reply,events)
 def render(self,base_prompt,events):
  value=self.replay(events);suffix='\nYour next move:'
  if not base_prompt.endswith(suffix):raise ValueError('Unexpected prompt boundary')
  return base_prompt.removesuffix(suffix)+'\n\n'+view(value,self.rules)+'\n\nYour next move:'
 def snapshot(self,events):
  return dict(number=self.replay(events),activation_step=self.activation_step,rules_sha256=self.rules.fingerprint(),primary_entries=len(events),authority='Derived from immutable primary world receipts; not an independent source of state')
