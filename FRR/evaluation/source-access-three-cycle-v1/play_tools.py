"""Local optional affordances: no eval, shell, arbitrary files or network."""
import ast,math

def calculate(expression):
 if len(expression)>100:raise ValueError('Expression too long')
 tree=ast.parse(expression,mode='eval')
 if len(list(ast.walk(tree)))>40:raise ValueError('Expression too large')
 def walk(n):
  if isinstance(n,ast.Constant) and type(n.value) in (int,float):
   if not math.isfinite(n.value) or abs(n.value)>1e6:raise ValueError('Number outside limit')
   return n.value
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):v=walk(n.operand);return v if isinstance(n.op,ast.UAdd) else -v
  if isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub,ast.Mult,ast.Div)):
   a,b=walk(n.left),walk(n.right)
   if isinstance(n.op,ast.Add):v=a+b
   elif isinstance(n.op,ast.Sub):v=a-b
   elif isinstance(n.op,ast.Mult):v=a*b
   else:v=a/b
   if not math.isfinite(v) or abs(v)>1e12:raise ValueError('Result outside limit')
   return v
  raise ValueError('Only bounded numeric + - * / expressions are supported')
 return walk(tree.body)
def dispatch(text,events,reader):
 t=text.strip();cmd=t.upper()
 if cmd.startswith('NOTE '):
  body=t[5:]
  if len(body)>1024:return dict(kind='note_error',executed=False,message='Note exceeds local size limit; original reply remains recorded.')
  return dict(kind='note_recorded',executed=True,note=body,status='unverified_model_note')
 if cmd=='READ NOTES':
  notes=[e['host_result']['note'] for e in events if e.get('host_result',{}).get('kind')=='note_recorded']
  return dict(kind='note_receipt',executed=True,notes=notes[-8:],status='unverified_model_notes',earlier_count=max(0,len(notes)-8))
 if cmd.startswith('TRY '):
  try:return dict(kind='calculation',executed=True,expression=t[4:],result=calculate(t[4:]),scope='bounded arithmetic only; no reasoning or task score')
  except (ValueError,SyntaxError,ZeroDivisionError,OverflowError,RecursionError):return dict(kind='calculation_error',executed=True,expression=t[4:],message='Invalid or out-of-bounds arithmetic; no result claimed.')
 return reader(t,'tools_optional')
