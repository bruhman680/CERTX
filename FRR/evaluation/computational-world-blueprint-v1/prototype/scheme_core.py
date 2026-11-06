"""Bounded R7RS-small subset. No host evaluation or guest I/O."""
import re

class Symbol(str):
    pass

class GuestError(Exception):
    def __init__(self, code, message, usage=None):
        super().__init__(message)
        self.code, self.message, self.usage = code, message, usage or {}

def fail(code, message):
    raise GuestError(code, message)

def value_wire(v):
    if type(v) is bool: return ['bool', v]
    if type(v) is int: return ['int', str(v)]
    if type(v) is str: return ['text', v]
    if type(v) is list: return ['list', [value_wire(x) for x in v]]
    fail('UNSUPPORTED_VALUE', 'unsupported value')

def value_from_wire(v):
    tag, x = v
    if tag == 'int': return int(x)
    if tag == 'bool': return bool(x)
    if tag == 'text': return str(x)
    if tag == 'list': return [value_from_wire(y) for y in x]
    fail('UNSUPPORTED_VALUE', 'invalid value encoding')

def canonical(v):
    # Canonical control escaping is uniform, not JSON's short escapes.
    def enc(x):
        if isinstance(x,str):
            return '"'+''.join('\\"' if c=='"' else '\\\\' if c=='\\' else '\\u%04x'%ord(c) if ord(c)<32 else c for c in x)+'"'
        if x is True:return 'true'
        if x is False:return 'false'
        if x is None:return 'null'
        if isinstance(x,list):return '['+','.join(enc(y) for y in x)+']'
        if isinstance(x,dict):return '{'+','.join(enc(k)+':'+enc(x[k]) for k in sorted(x,key=lambda y:y.encode('utf-8')))+'}'
        fail('UNSUPPORTED_VALUE','canonical encoding excludes numbers')
    return enc(v).encode('utf-8')

def value_size(v): return len(canonical(value_wire(v)))

def check_value(v, p):
    todo=[(v,1)]; nodes=0
    while todo:
        x,d=todo.pop(); nodes+=1
        if nodes>p['max_value_nodes'] or d>p['max_value_depth']:fail('VALUE_LIMIT','value nodes/depth exceeded')
        if type(x) is int:
            if max(1,abs(x).bit_length())>p['max_int_bits']:fail('INTEGER_LIMIT','integer magnitude exceeds cap')
        elif type(x) is bool:pass
        elif type(x) is str:
            if len(x)>p['max_string_chars']:fail('VALUE_LIMIT','text scalar cap exceeded')
            if any(0xD800<=ord(c)<=0xDFFF for c in x):fail('SYNTAX','surrogate text')
        elif type(x) is list:todo.extend((y,d+1) for y in x)
        else:fail('UNSUPPORTED_VALUE','unsupported value type')
    return v

_NAME=re.compile(r'[A-Za-z][A-Za-z0-9_?\-]*\Z')
_INT=re.compile(r'[+-]?[0-9]+\Z')
_SPECIAL={'if','let','quote','define'}
PRIMITIVES={'+','-','*','floor-quotient','floor-remainder','=','<','<=','>','>=','equal?','not','integer?','boolean?','string?','list?','list','cons','car','cdr','null?','length','append','string-length','string-append','substring'}
RESERVED=_SPECIAL|PRIMITIVES

def parse_one(source, profile):
    p=profile
    try: raw=source.encode('utf-8')
    except (UnicodeError,AttributeError):fail('SYNTAX','source must be scalar UTF-8 text')
    if len(raw)>p['max_source_bytes']:fail('SOURCE_LIMIT','source byte cap exceeded')
    tokens=[];i=0;n=len(source)
    while i<n:
        c=source[i]
        if c in ' \t\r\n':i+=1;continue
        if c in "()'":tokens.append(c);i+=1;continue
        if c=='"':
            i+=1;out=[]
            while i<n and source[i]!='"':
                c=source[i];i+=1
                if c=='\\':
                    if i>=n:fail('SYNTAX','unfinished string escape')
                    c=source[i];i+=1
                    esc={'a':'\a','b':'\b','t':'\t','n':'\n','r':'\r','"':'"','\\':'\\'}
                    if c in esc:out.append(esc[c])
                    elif c=='x':
                        j=source.find(';',i)
                        if j<0 or not re.fullmatch('[0-9A-Fa-f]+',source[i:j]):fail('SYNTAX','bad hex escape')
                        digits=source[i:j].lstrip('0') or '0'
                        if len(digits)>6:fail('SYNTAX','hex escape out of range')
                        code=int(digits,16)
                        if code>0x10ffff or 0xd800<=code<=0xdfff:fail('SYNTAX','not a Unicode scalar')
                        out.append(chr(code));i=j+1
                    else:fail('SYNTAX','unsupported string escape')
                else:
                    if ord(c)<32 or ord(c)==127:fail('SYNTAX','raw control in string')
                    out.append(c)
            if i>=n:fail('SYNTAX','unfinished string')
            i+=1;value=''.join(out);check_value(value,p);tokens.append(('atom',value));continue
        j=i
        while i<n and source[i] not in " \t\r\n()'\"":i+=1
        token=source[j:i]
        if token in ('#t','#f'):v=token=='#t'
        elif _INT.fullmatch(token):
            # Bit cap implies a bounded decimal reader; a few extra digits allow signs/zeroes.
            significant=token.lstrip('+-').lstrip('0') or '0'
            if len(significant)>(p['max_int_bits']*30103)//100000+2:fail('INTEGER_LIMIT','integer literal too large')
            v=int(significant)*(-1 if token.startswith('-') else 1);check_value(v,p)
        elif _NAME.fullmatch(token) or token in PRIMITIVES:v=Symbol(token)
        else:fail('SYNTAX','unsupported token '+token[:32])
        tokens.append(('atom',v))
    pos=0;nodes=0
    def read(depth):
        nonlocal pos,nodes
        nodes+=1
        if nodes>p['max_ast_nodes'] or depth>p['max_parse_depth']:fail('SYNTAX','reader nodes/depth exceeded')
        if pos>=len(tokens):fail('SYNTAX','unexpected end')
        t=tokens[pos];pos+=1
        if t=='(':
            out=[]
            while pos<len(tokens) and tokens[pos]!=')':out.append(read(depth+1))
            if pos>=len(tokens):fail('SYNTAX','unclosed list')
            pos+=1;return out
        if t==')':fail('SYNTAX','unexpected closing parenthesis')
        if t=="'":return [Symbol('quote'),read(depth+1)]
        return t[1]
    result=read(1)
    if pos!=len(tokens):fail('SYNTAX','one form required')
    return result

def _quoted_value(value, profile):
    todo=[value]
    while todo:
        x=todo.pop()
        if isinstance(x,Symbol):fail('SYNTAX','symbol datum excluded')
        if type(x) is list:todo.extend(x)
    return check_value(value,profile)

def literal_value(node,profile):
    if type(node) in (int,bool,str):return check_value(node,profile)
    if type(node) is list and len(node)==2 and isinstance(node[0],Symbol) and node[0]==Symbol('quote'):
        return _quoted_value(node[1],profile)
    fail('SYNTAX','put requires a supported literal')

def encode_ast(node):
    if isinstance(node,Symbol):return ['symbol',str(node)]
    if type(node) is list:return ['syntax',[encode_ast(x) for x in node]]
    return ['value',value_wire(node)]

def decode_ast(node):
    if node[0]=='symbol':return Symbol(node[1])
    if node[0]=='syntax':return [decode_ast(x) for x in node[1]]
    if node[0]=='value':return value_from_wire(node[1])
    fail('SYNTAX','invalid AST encoding')

def _binder(x, self_name=None):
    if not isinstance(x,Symbol) or not _NAME.fullmatch(x):fail('SYNTAX','identifier required')
    if x in RESERVED or x==self_name:fail('NAME_CONFLICT','reserved or self-shadowing binder')
    return str(x)

def _arity(name,n):
    if name in ('+','*','list','append','string-append'):return
    if name=='-' and n>=1:return
    if name in ('=','<','<=','>','>=') and n>=2:return
    count=3 if name=='substring' else 2 if name in ('floor-quotient','floor-remainder','equal?','cons') else 1
    if n!=count:fail('ARITY','wrong argument count for '+name)

def _resolve(node,env,namespace,loader,p,self_name=None,self_arity=None,bindings=None):
    if type(node) in (int,bool,str):return ['lit',value_wire(check_value(node,p))]
    if isinstance(node,Symbol):
        name=str(node)
        if name in env:return ['var',name]
        if name in PRIMITIVES or name==self_name:fail('UNSUPPORTED_VALUE','procedure is not a guest value')
        ref=namespace.get(name)
        if not ref:fail('UNBOUND_NAME','unbound '+name)
        if ref['kind']!='data':fail('DEPENDENCY_KIND','expected data '+name)
        if bindings is not None:bindings[name]=dict(ref)
        return ['data',ref['id']]
    if type(node) is not list or not node or not isinstance(node[0],Symbol):fail('SYNTAX','named call or special form required')
    name=str(node[0]);args=node[1:]
    if len(args)>p['max_argument_count']:fail('VALUE_LIMIT','argument count exceeded')
    recur=lambda x,e=env:_resolve(x,e,namespace,loader,p,self_name,self_arity,bindings)
    if name=='quote':
        if len(args)!=1:fail('SYNTAX','quote requires one datum')
        return ['lit',value_wire(_quoted_value(args[0],p))]
    if name=='if':
        if len(args)!=3:fail('SYNTAX','if requires three expressions')
        return ['if']+[recur(x) for x in args]
    if name=='let':
        if len(args)!=2 or type(args[0]) is not list or len(args[0])!=1 or type(args[0][0]) is not list or len(args[0][0])!=2:fail('SYNTAX','single-binding let required')
        binder,init=args[0][0];binder=_binder(binder,self_name)
        if len(env|{binder})>p['max_environment_bindings']:fail('VALUE_LIMIT','environment binding cap exceeded')
        return ['let',binder,recur(init),recur(args[1],env|{binder})]
    if name in _SPECIAL:fail('SYNTAX','unsupported nested definition')
    if name in env:fail('NOT_CALLABLE','lexical value cannot be called')
    if name in PRIMITIVES:
        _arity(name,len(args));return ['prim',name,[recur(x) for x in args]]
    if name==self_name:
        if len(args)!=self_arity:fail('ARITY','wrong self call arity')
        return ['self',[recur(x) for x in args]]
    ref=namespace.get(name)
    if not ref:fail('UNBOUND_NAME','unbound '+name)
    if ref['kind']!='procedure':fail('DEPENDENCY_KIND','expected procedure '+name)
    artifact=loader(ref['id'])
    if len(args)!=len(artifact['payload']['params']):fail('ARITY','wrong procedure arity')
    if bindings is not None:bindings[name]=dict(ref)
    return ['call',ref['id'],[recur(x) for x in args]]

def compile_definition(define_ast,namespace,load_artifact,profile):
    n=define_ast
    if type(n) is not list or len(n)!=3 or not isinstance(n[0],Symbol) or n[0]!=Symbol('define') or type(n[1]) is not list or not n[1]:fail('SYNTAX','one named definition required')
    name=_binder(n[1][0]);params=[_binder(x,name) for x in n[1][1:]]
    if len(set(params))!=len(params):fail('NAME_CONFLICT','duplicate parameter')
    if len(params)>profile['max_argument_count'] or len(params)>profile['max_environment_bindings']:fail('VALUE_LIMIT','parameter count exceeded')
    bindings={};body=_resolve(n[2],set(params),namespace,load_artifact,profile,name,len(params),bindings)
    return {'name':name,'params':params,'body':body,'bindings':bindings}

def compile_expression(expr_ast,namespace,load_artifact,profile):
    bindings={}
    body=_resolve(expr_ast,set(),namespace,load_artifact,profile,bindings=bindings)
    return {'body':body,'bindings':bindings}

def _primitive(name,a,p,charge,reserve):
    ints={'+','-','*','floor-quotient','floor-remainder','=','<','<=','>','>='}
    if name in ints and any(type(x) is not int for x in a):fail('TYPE','integer arguments required')
    if name in ('length','car','cdr') and type(a[0]) is not list:fail('TYPE','list required')
    if name=='cons' and type(a[1]) is not list:fail('UNSUPPORTED_VALUE','improper pairs excluded')
    if name=='append' and any(type(x) is not list for x in a):fail('TYPE','proper lists required')
    if name in ('string-length','substring') and type(a[0]) is not str:fail('TYPE','text required')
    if name=='string-append' and any(type(x) is not str for x in a):fail('TYPE','text arguments required')
    if name=='substring' and any(type(x) is not int for x in a[1:]):fail('TYPE','integer indices required')
    if name in ('floor-quotient','floor-remainder') and a[1]==0:fail('DIVIDE_BY_ZERO','zero divisor')
    if name in ('car','cdr') and not a[0]:fail('EMPTY_LIST','empty list')
    if name=='substring' and not 0<=a[1]<=a[2]<=len(a[0]):fail('INDEX_RANGE','substring bounds')
    upper=sum(value_size(x) for x in a)+32+len(a) if name in ('list','cons','append','string-append','car','cdr','substring') else (p['max_int_bits']*30103)//100000+32
    reserve(upper)
    b=lambda x:max(1,abs(x).bit_length())
    if name in ('+','-','*'):
        if name=='-' and len(a)==1:
            charge(work=1+b(a[0]));result=-a[0];check_value(result,p)
        elif name=='*':
            result=1
            if not a:charge(work=1)
            for x in a:
                charge(work=1+b(result)*b(x));result*=x;check_value(result,p)
        elif not a:
            charge(work=1);result=0
        elif len(a)==1:
            charge(work=1);result=a[0]
        else:
            result=a[0]
            for x in a[1:]:
                charge(work=1+max(b(result),b(x)));result=result+x if name=='+' else result-x;check_value(result,p)
        return 0,lambda:result
    S=sum(value_size(x) for x in a)
    if name in ('floor-quotient','floor-remainder'):cost=1+(b(a[0])+1)*(b(a[1])+1)
    elif name in ('=','<','<=','>','>='):cost=1+sum(max(b(x),b(y)) for x,y in zip(a,a[1:]))
    elif name=='equal?':cost=1+S
    elif name in ('cdr','length','string-length','substring'):cost=1+S
    elif name in ('list','cons','append','string-append'):cost=1+len(a)+S
    else:cost=1
    # Cost computation is metadata-only except bounded integer-fold planning.
    def compute():
        if name=='floor-quotient':return a[0]//a[1]
        if name=='floor-remainder':return a[0]%a[1]
        if name in ('=','<','<=','>','>='):
            tests={'=':lambda x,y:x==y,'<':lambda x,y:x<y,'<=':lambda x,y:x<=y,'>':lambda x,y:x>y,'>=':lambda x,y:x>=y}
            return all(tests[name](x,y) for x,y in zip(a,a[1:]))
        if name=='equal?':return value_wire(a[0])==value_wire(a[1])
        if name=='not':return a[0] is False
        if name in ('integer?','boolean?','string?','list?'):return type(a[0]) is {'integer?':int,'boolean?':bool,'string?':str,'list?':list}[name]
        if name=='null?':return type(a[0]) is list and not a[0]
        if name=='list':return list(a)
        if name=='cons':return [a[0]]+a[1]
        if name=='car':return a[0][0]
        if name=='cdr':return a[0][1:]
        if name in ('length','string-length'):return len(a[0])
        if name=='append':return [x for xs in a for x in xs]
        if name=='string-append':return ''.join(a)
        if name=='substring':return a[0][a[1]:a[2]]
        fail('SYNTAX','unknown primitive')
    return cost,compute

def evaluate(expr_ast,namespace,load_artifact,profile):
    p=profile;usage={'steps':0,'work_units':0,'fuel_used':0,'allocation_bytes':0,'peak_frames':1};cache={}
    stack=[];env={};current_proc=None
    if p['max_frames']<1:fail('FRAME_LIMIT','initial environment exceeds frame cap')
    def charge(steps=0,work=0):
        if usage['steps']+steps>p['max_steps'] or usage['work_units']+work>p['max_work'] or usage['fuel_used']+steps+work>p['eval_fuel']:fail('OUT_OF_FUEL','execution fuel exhausted')
        usage['steps']+=steps;usage['work_units']+=work;usage['fuel_used']+=steps+work
    def allocate(v):
        check_value(v,p);size=value_size(v)
        cap=p['max_allocation_bytes']
        if usage['allocation_bytes']+size>cap:fail('ALLOCATION_LIMIT','logical allocation exhausted')
        usage['allocation_bytes']+=size
        return v
    def reserve(amount):
        if usage['allocation_bytes']+amount>p['max_allocation_bytes']:fail('ALLOCATION_LIMIT','primitive reservation exhausted')
    def push(frame):
        if len(stack)+2>p['max_frames']:fail('FRAME_LIMIT','continuation cap exceeded')
        stack.append(frame);usage['peak_frames']=max(usage['peak_frames'],len(stack)+1)
    try:
        expr=_resolve(expr_ast,set(),namespace,load_artifact,p)
        mode='eval';value=None
        while True:
            if mode=='eval':
                charge(steps=1);tag=expr[0]
                if tag=='lit':value=allocate(value_from_wire(expr[1]));mode='return'
                elif tag=='var':value=env[expr[1]];mode='return'
                elif tag=='data':
                    ident=expr[1]
                    if ident not in cache:
                        data=load_artifact(ident)['payload']
                        if type(data) is dict and 'value' in data:data=value_from_wire(data['value'])
                        cache[ident]=allocate(data)
                    value=cache[ident];mode='return'
                elif tag=='if':push(('if',expr[2],expr[3],env,current_proc));expr=expr[1]
                elif tag=='let':push(('let',expr[1],expr[3],env,current_proc));expr=expr[2]
                else:
                    args=expr[1] if tag=='self' else expr[2]
                    callee=(tag,current_proc if tag=='self' else expr[1])
                    if args:push(('args',callee,args[1:],[],env,current_proc));expr=args[0]
                    else:pending=(callee,[]);mode='invoke'
            elif mode=='invoke':
                (kind,target),values=pending
                if kind=='prim':
                    cost,compute=_primitive(target,values,p,charge,reserve);charge(work=cost);value=allocate(compute());mode='return'
                else:
                    proc=target if kind=='self' else load_artifact(target)['payload']
                    charge(steps=1);env=dict(zip(proc['params'],values));current_proc=proc;expr=proc['body'];mode='eval'
            else:
                if not stack:
                    if value_size(value)>p['max_result_bytes']:fail('VALUE_LIMIT','result byte cap exceeded')
                    return {'value':value,**usage}
                frame=stack.pop();kind=frame[0]
                if kind=='if':_,yes,no,env,current_proc=frame;expr=no if value is False else yes;mode='eval'
                elif kind=='let':_,name,body,old_env,current_proc=frame;env={**old_env,name:value};expr=body;mode='eval'
                else:
                    _,callee,remaining,values,env,current_proc=frame;values=values+[value]
                    if remaining:push(('args',callee,remaining[1:],values,env,current_proc));expr=remaining[0];mode='eval'
                    else:pending=(callee,values);mode='invoke'
    except GuestError as error:
        error.usage=dict(usage);raise

# Public artifact helpers.
encode_value = value_wire
decode_value = value_from_wire
