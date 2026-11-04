"""Bounded direct view over a complete retained archive; no model-authored fact promotion."""
import json,re,hashlib
RECENT=12
MAX_HISTORY_ENTRIES=2
def view_steps(events):return [e['step'] for e in events[-RECENT:]]
def dispatch(text,events,old_dispatch):
 match=re.fullmatch(r'READ HISTORY\s+(\d+)\s+(\d+)',text.strip(),flags=re.IGNORECASE)
 if not match:return old_dispatch(text,events)
 lo,hi=map(int,match.groups())
 if not (0<=lo<hi<=len(events) and hi-lo<=MAX_HISTORY_ENTRIES):return dict(kind='history_error',executed=True,message='Use READ HISTORY start end with end exclusive, at most two existing entries.',available_range=[0,len(events)])
 records=[]
 for e in events[lo:hi]:
  h=e.get('host_result');small={k:v for k,v in (h or {}).items() if k in ('kind','executed','result','message','status','range') and isinstance(v,(str,int,float,bool,type(None),list))}
  records.append(dict(step=e['step'],observation=e['observation'],reply=e['reply'],reply_status='unverified_model_output',feedback=e['feedback'],feedback_status='recorded_host_feedback',host_result_projection=small,full_host_result_omitted=h is not None,full_host_result_canonical_sha256=hashlib.sha256(json.dumps(h,sort_keys=True).encode()).hexdigest() if h is not None else None))
 return dict(kind='history_receipt',executed=True,range=[lo,hi],scope='Exact original observation/reply/feedback, plus selected scalar host fields; full raw records retained externally. Replies/notes are not verified facts. Nested tool payloads are not recursively copied.',records=records)
def render(events,base_renderer):
 visible=events[-RECENT:];n=len(events);start=n-len(visible)
 info=f'\n\nARCHIVE ACCESS (host metadata): Full external history retains entries 0 through {n-1}. This direct view shows entries {start} through {n-1}. Earlier entries remain archived, not erased. Optional READ HISTORY start end returns at most two entries, end exclusive; valid existing range is 0 to {n}. Their replies remain unverified model text. This is access, not a required task.\n'
 # Keep the unchanged seed shelf and charter, adding explicit archive navigation.
 body=base_renderer(visible).removesuffix('\n\nYour next move:')
 return body+info+'\nYour next move:'
def require_checked(current,latest,checks,steps):
 assert 0<steps<=5,'Routine windows are at most five replies'
 assert latest['next_step']==current and checks['status']=='pass','Verify the current saved cursor before another window'
