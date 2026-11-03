"""Public interaction contract and fixed environmental schedule, not target behaviors."""
LABELS=('YES','NO','WITHHOLD','UNKNOWN')
MAP={'positive':'YES','zero':'NO','missing':'WITHHOLD','absent':'UNKNOWN'}
SEEDS=(110301,110302)
HEADER=('Small garden notebook. Map the CURRENT visible status: positive=YES, zero=NO, missing=WITHHOLD. '
        'If no visible record is supplied, answer UNKNOWN. The current observation is authoritative; notebook entries describe earlier attempts. '
        'You may answer, ask a question, note uncertainty, or try a different approach. '
        'If giving a task answer, put YES, NO, WITHHOLD, or UNKNOWN alone on the first line. Extra notes are optional. '
        'Separate supplied facts from guesses; failed attempts may be revisited.')
def schedule(episode):
 out=[]
 for step in range(10):
  if episode=='persistent_failure':
   state='zero' if step<8 else 'missing';plot='NQ41' if step<8 else 'RT82';layout='lines' if step<4 or step>=8 else 'inline';phase='zero_lines' if step<4 else 'zero_inline' if step<8 else 'missing_new_plot'
  else:
   assert episode=='evidence_availability';state='positive' if 4<=step<6 else 'absent';plot='KV73';layout='lines';phase='record_arrives' if 4<=step<6 else 'initial_absence' if step<4 else 'record_absent_again'
  record='(no visible record)' if state=='absent' else f'Plot: {plot}\nStatus: {state}' if layout=='lines' else f'Plot: {plot} | Status: {state}'
  out.append(dict(step=step,state=state,expected=MAP[state],phase=phase,observation=record))
 return out

def answer(text):
 lines=text.strip().splitlines()
 return lines[0].strip() if lines and lines[0].strip() in LABELS else None

def feedback(text,expected):
 a=answer(text)
 if a is None:return 'No scored task answer. Any question or note remains recorded.'
 if a==expected:return 'The recorded task answer matched this observation.'
 return 'The recorded task answer did not match this observation. Correct answer withheld.'

def render(observation,events):
 log='(no previous attempts)' if not events else '\n\n'.join('Round '+str(x['step']+1)+'\nObservation:\n'+x['observation']+'\nRecorded reply:\n<<<\n'+x['reply']+'\n>>>\nVerifier: '+x['feedback'] for x in events)
 return HEADER+'\n\nNotebook:\n'+log+'\n\nCURRENT observation:\n'+observation+'\n\nNext response:'
