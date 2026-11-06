"""Isolated SQLite world prototype. No guest access to SQLite or the host.

The normative documents state the target contract; this prototype's limits are
fixture values, not a measured sandbox/security guarantee.
"""
from __future__ import annotations
import hashlib
import fcntl
import json
import sqlite3
import threading
import uuid
from pathlib import Path
import scheme_core as sc


def canonical(value):
    """Canonical scalar-JSON bytes: sorted UTF-8 keys, minimal control escapes."""
    if value is None:
        return b'null'
    if value is True:
        return b'true'
    if value is False:
        return b'false'
    if isinstance(value, str):
        # json.dumps uses short control escapes; canonical contract uses \\u00hh.
        out = ['"']
        for c in value:
            n = ord(c)
            if 0xD800 <= n <= 0xDFFF:
                raise ValueError('non-scalar text')
            out.append('\\"' if c == '"' else '\\\\' if c == '\\' else '\\u%04x' % n if n < 32 else c)
        return (''.join(out) + '"').encode('utf-8')
    if isinstance(value, (list, tuple)):
        return b'[' + b','.join(canonical(x) for x in value) + b']'
    if isinstance(value, dict):
        return b'{' + b','.join(canonical(k)+b':'+canonical(value[k]) for k in sorted(value, key=lambda x: x.encode('utf-8'))) + b'}'
    raise TypeError('canonical records use decimal strings, not JSON numbers')


def ident(kind, record):
    return kind + ':' + hashlib.sha256(('cw-v1/'+kind).encode() + b'\0' + canonical(record)).hexdigest()


def _safe(value):
    """Convert implementation counters to the decimal-string record domain."""
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return value
    if isinstance(value, int):
        return str(value)
    if isinstance(value, (list, tuple)):
        return [_safe(x) for x in value]
    if isinstance(value, dict):
        return {str(k): _safe(v) for k, v in value.items()}
    raise TypeError(type(value).__name__)


class StoreError(Exception):
    def __init__(self, code, message=''):
        self.code, self.message = code, message
        super().__init__(message or code)


class World:
    def __init__(self, path, profile):
        self.profile = dict(profile)
        required={'max_capture_bytes','max_metadata_bytes','max_visit_fuel','max_visit_allocation','max_delivery_bytes'}
        missing=required-self.profile.keys()
        if missing: raise ValueError('missing required storage profile keys: '+','.join(sorted(missing)))
        self.owner_file = None
        if str(path) != ':memory:':
            self.owner_file = open(str(path)+'.owner.lock','a+b')
            try:
                fcntl.flock(self.owner_file.fileno(),fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                self.owner_file.close()
                raise StoreError('WORLD_BUSY','world already has a live owner')
        self.lock = threading.RLock()
        self.db = sqlite3.connect(str(path), isolation_level=None, timeout=5)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS artifacts(id TEXT PRIMARY KEY, kind TEXT NOT NULL, record TEXT NOT NULL, size INTEGER NOT NULL);
          CREATE TABLE IF NOT EXISTS aliases(name TEXT PRIMARY KEY, id TEXT NOT NULL REFERENCES artifacts(id));
          CREATE TABLE IF NOT EXISTS snapshots(id TEXT PRIMARY KEY, record TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY, hash TEXT NOT NULL, envelope TEXT NOT NULL,
            state TEXT NOT NULL, before_id TEXT NOT NULL, receipt TEXT, reserved INTEGER NOT NULL);
          CREATE TABLE IF NOT EXISTS events(sequence INTEGER PRIMARY KEY, id TEXT UNIQUE NOT NULL, record TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS captures(id TEXT PRIMARY KEY, request_id TEXT UNIQUE NOT NULL, record TEXT NOT NULL);
          CREATE TABLE IF NOT EXISTS capture_links(request_id TEXT PRIMARY KEY, capture_id TEXT NOT NULL REFERENCES captures(id));
        ''')
        if self._meta('world_id') is None:
            self.db.execute('BEGIN IMMEDIATE')
            for k,v in {'world_id':uuid.uuid4().hex,'profile':json.dumps(self.profile,sort_keys=True),
                        'actions':'0','audit_bytes':'0','sequence':'0','head':'GENESIS',
                        'visit_fuel':'0','visit_alloc':'0','delivery_bytes':'0'}.items():
                self._set(k,v)
            self._persist_snapshot()
            self.db.commit()
        elif json.loads(self._meta('profile')) != self.profile:
            self.close()
            raise ValueError('profile differs from retained world profile')
        self.verify_integrity()
        # Conservative restart recovery; no evaluator is ever resumed.
        for row in self.db.execute("SELECT * FROM requests WHERE state!='TERMINAL'").fetchall():
            self._finish(row, 'FAILED_HOST_ABORT', error={'code':'HOST_RESTART','limit':None,'source_span':None,'details':{}})

    def close(self):
        self.db.close()
        if self.owner_file is not None:
            fcntl.flock(self.owner_file.fileno(),fcntl.LOCK_UN)
            self.owner_file.close()
            self.owner_file = None

    def _meta(self, key):
        row = self.db.execute('SELECT value FROM meta WHERE key=?',(key,)).fetchone()
        return row['value'] if row else None

    def _set(self, key, value):
        self.db.execute('INSERT OR REPLACE INTO meta VALUES (?,?)',(key,str(value)))

    def _namespace(self):
        return {r['name']:{'kind':r['kind'],'id':r['id']} for r in self.db.execute('SELECT name,aliases.id,kind FROM aliases JOIN artifacts ON aliases.id=artifacts.id ORDER BY name')}

    def _snapshot_record(self):
        return {'schema':'cw-snapshot-1','world_id':self._meta('world_id'),
                'artifacts':[r['id'] for r in self.db.execute('SELECT id FROM artifacts ORDER BY id')],
                'aliases':[[r['name'],r['id']] for r in self.db.execute('SELECT name,id FROM aliases ORDER BY name')]}

    def _persist_snapshot(self):
        record = self._snapshot_record()
        sid = ident('snapshot',record)
        self.db.execute('INSERT OR IGNORE INTO snapshots VALUES (?,?)',(sid,canonical(record).decode()))
        self._set('snapshot',sid)
        return sid

    def snapshot(self):
        with self.lock:
            return {'id':self._meta('snapshot'),'aliases':self._namespace()}

    def load_artifact(self, aid):
        row = self.db.execute('SELECT record FROM artifacts WHERE id=?',(aid,)).fetchone()
        if not row:
            raise StoreError('MISSING_ARTIFACT',aid)
        record = json.loads(row['record'])
        if ident('art',record)!=aid or canonical(record).decode()!=row['record']:
            raise StoreError('INTEGRITY_ERROR','artifact hash or canonical bytes mismatch')
        if record['kind'] == 'data':
            record['payload'] = sc.value_from_wire(record['payload'])
        return record

    def _metadata_bytes(self):
        return sum(self.db.execute('SELECT COALESCE(SUM(length(CAST(record AS BLOB))),0) FROM '+table).fetchone()[0]
                   for table in ('snapshots','captures')) + self.db.execute('SELECT COALESCE(SUM(length(CAST(envelope AS BLOB))),0) FROM requests').fetchone()[0]

    def _capture(self, request_id, before, compiled):
        direct=sorted({ref['id'] for ref in compiled['bindings'].values()})
        pending=list(direct); seen=set()
        while pending:
            aid=pending.pop()
            if aid in seen: continue
            seen.add(aid)
            if len(seen)>self.profile['max_dependency_nodes']: raise StoreError('DEPENDENCY_LIMIT')
            art=self.load_artifact(aid)
            if art['kind']=='procedure': pending.extend(ref['id'] for ref in art['payload']['bindings'].values())
        record={'schema':'cw-capture-1','snapshot_id':before,'root_procedure_id':None,
                'resolved_ast':compiled['body'],'arguments':[], 'direct_dependencies':direct,
                'reachable_dependencies':sorted(seen),'versions':{'language':'cw-scheme-1','evaluator':'cw-eval-1','cost':'cw-cost-1'},
                'limits':_safe(self.profile)}
        raw=canonical(record)
        if len(raw)>self.profile['max_capture_bytes']: raise StoreError('CAPTURE_BYTES')
        cid=ident('capture',record)
        self.db.execute('INSERT OR IGNORE INTO captures VALUES (?,?,?)',(cid,request_id,raw.decode()))
        self.db.execute('INSERT INTO capture_links VALUES (?,?)',(request_id,cid))
        return cid

    def verify_integrity(self):
        """Bounded by retained store caps; no mutation, no guest execution."""
        for row in self.db.execute('SELECT id FROM artifacts').fetchall(): self.load_artifact(row['id'])
        for row in self.db.execute('SELECT id,record FROM snapshots').fetchall():
            record=json.loads(row['record'])
            if ident('snapshot',record)!=row['id'] or canonical(record).decode()!=row['record']:
                raise StoreError('INTEGRITY_ERROR','snapshot hash mismatch')
        head='GENESIS'; sequence=0
        for row in self.db.execute('SELECT * FROM events ORDER BY sequence').fetchall():
            core=json.loads(row['record']); sequence+=1
            if (row['sequence']!=sequence or ident('event',core)!=row['id'] or core['audit_before']!={'sequence':str(sequence-1),'head':head}
                or core['audit_after_sequence']!=str(sequence) or canonical(core).decode()!=row['record']):
                raise StoreError('INTEGRITY_ERROR','audit chain mismatch')
            head=row['id']
        if head!=self._meta('head') or sequence!=int(self._meta('sequence')):
            raise StoreError('INTEGRITY_ERROR','audit head mismatch')
        for row in self.db.execute('SELECT * FROM requests').fetchall():
            envelope=json.loads(row['envelope'])
            if ident('request',envelope)!=row['hash']: raise StoreError('INTEGRITY_ERROR','request hash mismatch')
            if row['state']=='TERMINAL':
                receipt=json.loads(row['receipt'])
                if ident('event',receipt['event'])!=receipt['receipt_id'] or receipt['event']['request_hash']!=row['hash']:
                    raise StoreError('INTEGRITY_ERROR','request receipt mismatch')
        for row in self.db.execute('SELECT id,record FROM captures').fetchall():
            if ident('capture',json.loads(row['record']))!=row['id']: raise StoreError('INTEGRITY_ERROR','capture hash mismatch')
        if self._meta('snapshot')!=ident('snapshot',self._snapshot_record()): raise StoreError('INTEGRITY_ERROR','current world snapshot mismatch')
        return {'artifacts':self.db.execute('SELECT COUNT(*) FROM artifacts').fetchone()[0],'events':sequence,'snapshot':self._meta('snapshot')}

    def audit(self):
        return [json.loads(r['record']) for r in self.db.execute('SELECT record FROM events ORDER BY sequence')]

    def _transport(self, status, request_id, **fields):
        return {'schema':'cw-transport-1','status':status,'request_id':request_id,
                'error':{'code':status if status!='NOT_ADMITTED' else fields.get('reason','NOT_ADMITTED')},
                'value':None,'world_snapshot':self._meta('snapshot'),**fields}

    def _artifact(self, kind, payload):
        record = {'schema':'cw-artifact-1','kind':kind,'payload':sc.value_wire(payload) if kind=='data' else payload}
        data = canonical(record)
        if len(data)>self.profile['max_artifact_bytes']:
            raise StoreError('ARTIFACT_BYTES')
        aid = ident('art',record)
        old = self.db.execute('SELECT record FROM artifacts WHERE id=?',(aid,)).fetchone()
        if old and old['record'] != data.decode():
            raise StoreError('HASH_COLLISION')
        total = self.db.execute('SELECT COALESCE(SUM(size),0),COUNT(*) FROM artifacts').fetchone()
        if not old and (total[0]+len(data)>self.profile['max_world_bytes'] or total[1]+1>self.profile['max_artifacts']):
            raise StoreError('ARTIFACT_BYTES')
        return aid,record,data,not bool(old)

    def _target(self, node):
        if not isinstance(node, sc.Symbol):
            raise StoreError('SYNTAX','expected alias name')
        return str(node)

    def _projection(self, ast, namespace, before):
        command = str(ast[0])
        if command=='help':
            if len(ast)>2:
                raise StoreError('ARITY')
            return {'commands':['put','define','run','run-save','inspect','list','drop','help','page','page-run'],
                    'language':'R7RS-small restricted subset','profile':self.profile}
        if command in ('page', 'page-run'):
            from paging import make_page
            if len(ast) != (5 if command == 'page' else 4):
                raise StoreError('ARITY')
            if command == 'page':
                key, field, cursor, count = str(ast[1]), str(ast[2]), ast[3], ast[4]
                if not isinstance(cursor, str) or isinstance(cursor, sc.Symbol):
                    raise StoreError('CURSOR')
                aid = namespace[key]['id'] if key in namespace else key
                artifact = self.load_artifact(aid)
                if field == 'source' and artifact['kind'] == 'procedure':
                    text, encoding = artifact['payload']['source'], 'scheme-source'
                elif field == 'value' and artifact['kind'] == 'data':
                    text, encoding = canonical(sc.value_wire(artifact['payload'])).decode(), 'canonical-tagged-json'
                else:
                    raise StoreError('UNKNOWN_FIELD')
                return make_page(before, aid, field, text, encoding, cursor, count, self.profile, StoreError)
            request, cursor, count = ast[1], ast[2], ast[3]
            if type(request) is not str or type(cursor) is not str:
                raise StoreError('SYNTAX')
            row = self.db.execute('SELECT receipt FROM requests WHERE id=?', (request,)).fetchone()
            if not row or not row['receipt']:
                raise StoreError('MISSING_RESULT')
            receipt = json.loads(row['receipt'])
            if receipt['status'] != 'COMPUTED':
                raise StoreError('MISSING_RESULT')
            text = canonical(receipt['event']['result']['value']).decode()
            return make_page(before, receipt['receipt_id'], 'run-result', text,
                             'canonical-tagged-json', cursor, count, self.profile, StoreError)
        if command=='inspect':
            if len(ast) not in (2,3):
                raise StoreError('ARITY')
            key = str(ast[1])
            aid = namespace[key]['id'] if key in namespace else key
            artifact = self.load_artifact(aid)
            if len(ast)==3:
                field = str(ast[2])
                if field not in artifact and not (isinstance(artifact['payload'],dict) and field in artifact['payload']):
                    raise StoreError('UNKNOWN_FIELD')
                return artifact.get(field,artifact['payload'].get(field) if isinstance(artifact['payload'],dict) else None)
            return {'id':aid,**artifact}
        if command=='list':
            if len(ast) not in (1,2,3):
                raise StoreError('ARITY')
            offset=0
            if len(ast)>=2 and ast[1]!='':
                if not isinstance(ast[1],str) or isinstance(ast[1],sc.Symbol):
                    raise StoreError('CURSOR')
                try:
                    cur=json.loads(ast[1])
                    if cur['snapshot']!=before or cur['query']!='aliases' or not isinstance(cur['offset'],int) or cur['offset']<0:
                        raise ValueError()
                    offset=cur['offset']
                except (ValueError,KeyError,TypeError):
                    raise StoreError('CURSOR')
            count=self.profile['max_page_items'] if len(ast)<3 else ast[2]
            if isinstance(count,bool) or not isinstance(count,int) or not 1<=count<=self.profile['max_page_items']:
                raise StoreError('PAGE_LIMIT')
            rows=[{'name':n,**namespace[n]} for n in sorted(namespace)]
            if offset>len(rows):
                raise StoreError('CURSOR')
            end=min(offset+count,len(rows))
            cursor=json.dumps({'snapshot':before,'query':'aliases','offset':end},sort_keys=True,separators=(',',':')) if end<len(rows) else None
            return {'snapshot':before,'items':rows[offset:end],'next_cursor':cursor}
        raise StoreError('UNKNOWN_COMMAND')

    def submit(self, request_id, expected_world_snapshot, source):
        with self.lock:
            try:
                return self._submit(request_id,expected_world_snapshot,source)
            except sqlite3.Error:
                # A failed statement can leave SQLite in a live transaction.
                # Clear it before reconciliation; do not infer commit failure.
                try:
                    if self.db.in_transaction: self.db.rollback()
                    row=self.db.execute('SELECT receipt,envelope,hash FROM requests WHERE id=?',(request_id,)).fetchone()
                    if row:
                        supplied=json.loads(row['envelope'])
                        supplied.update(command=source,expected_world_snapshot=expected_world_snapshot,
                                        profile_id=self.profile['profile_id'],limits=_safe(self.profile),
                                        language_version='cw-scheme-1',evaluator_version='cw-eval-1',cost_version='cw-cost-1')
                        supplied_hash=ident('request',supplied)
                        if supplied_hash!=row['hash']:
                            return self._transport('REQUEST_ID_CONFLICT',request_id,stored_request_hash=row['hash'],
                                                   supplied_request_hash=supplied_hash,commit_certainty='existing_request_only')
                        if row['receipt']: return json.loads(row['receipt'])
                except sqlite3.Error:
                    pass
                return self._transport('UNKNOWN_COMMIT',request_id,commit_certainty='unknown')

    def _submit(self, request_id, expected, source):
        envelope={'schema':'cw-request-1','world_id':self._meta('world_id'),'request_id':request_id,
                  'expected_world_snapshot':expected,'command':source,'language_version':'cw-scheme-1',
                  'evaluator_version':'cw-eval-1','cost_version':'cw-cost-1',
                  'profile_id':self.profile['profile_id'],'limits':_safe(self.profile)}
        if not isinstance(source,str):
            return self._transport('NOT_ADMITTED',request_id,reason='SYNTAX',commit_certainty='not_admitted')
        try:
            source_bytes=source.encode('utf-8')
        except UnicodeEncodeError:
            return self._transport('NOT_ADMITTED',request_id,reason='SYNTAX',commit_certainty='not_admitted')
        if len(source_bytes)>self.profile['max_source_bytes']:
            return self._transport('NOT_ADMITTED',request_id,reason='SUBMISSION_BYTES',commit_certainty='not_admitted')
        rhash=ident('request',envelope)
        self.db.execute('BEGIN IMMEDIATE')
        row=self.db.execute('SELECT * FROM requests WHERE id=?',(request_id,)).fetchone()
        if row:
            self.db.rollback()
            if row['hash']!=rhash:
                return self._transport('REQUEST_ID_CONFLICT',request_id,stored_request_hash=row['hash'],supplied_request_hash=rhash,commit_certainty='existing_request_only')
            return json.loads(row['receipt']) if row['state']=='TERMINAL' else self._transport('PENDING',request_id)
        if self.db.execute("SELECT 1 FROM requests WHERE state!='TERMINAL'").fetchone():
            self.db.rollback()
            return self._transport('NOT_ADMITTED',request_id,reason='WORLD_BUSY',commit_certainty='not_admitted')
        reserved=self.profile['max_receipt_bytes']+len(canonical(envelope))
        if int(self._meta('actions'))>=self.profile['max_actions'] or int(self._meta('audit_bytes'))+reserved>self.profile['max_audit_bytes']:
            self.db.rollback()
            return self._transport('NOT_ADMITTED',request_id,reason='AUDIT_OR_ACTION_LIMIT',commit_certainty='not_admitted')
        metadata_reserve=len(canonical(envelope))+self.profile['max_capture_bytes']+len(canonical(self._snapshot_record()))+512
        if self._metadata_bytes()+metadata_reserve>self.profile['max_metadata_bytes']:
            self.db.rollback()
            return self._transport('NOT_ADMITTED',request_id,reason='AUDIT_METADATA_LIMIT',commit_certainty='not_admitted')
        before=self._meta('snapshot')
        self.db.execute('INSERT INTO requests VALUES (?,?,?,?,?,NULL,?)',(request_id,rhash,canonical(envelope).decode(),'ADMITTED',before,reserved))
        self._set('actions',int(self._meta('actions'))+1)
        self._set('audit_bytes',int(self._meta('audit_bytes'))+len(canonical(envelope)))
        self.db.commit()
        row=self.db.execute('SELECT * FROM requests WHERE id=?',(request_id,)).fetchone()
        usage={}; evaluating=False
        try:
            if expected!=before:
                raise StoreError('SNAPSHOT_MISMATCH')
            ast=sc.parse_one(source,self.profile)
            if not isinstance(ast,list) or not ast or not isinstance(ast[0],sc.Symbol):
                raise StoreError('SYNTAX')
            command=str(ast[0]); namespace=self._namespace()
            artifact=None; alias=None; value=None; projection=None; status='PUBLISHED'
            if command=='put':
                if len(ast)!=3: raise StoreError('ARITY')
                alias=self._target(ast[1]); value=sc.literal_value(ast[2],self.profile)
                artifact=self._artifact('data',value)
            elif command=='define':
                payload=sc.compile_definition(ast,namespace,self.load_artifact,self.profile)
                alias=payload['name']; payload={**payload,'source':source,'language_version':'cw-scheme-1','evaluator_version':'cw-eval-1'}
                artifact=self._artifact('procedure',payload)
            elif command in ('run','run-save'):
                if len(ast)!=(2 if command=='run' else 3): raise StoreError('ARITY')
                alias=self._target(ast[1]) if command=='run-save' else None
                expr=ast[-1]
                compiled=sc.compile_expression(expr,namespace,self.load_artifact,self.profile)
                self._capture(request_id,before,compiled)
                self.db.execute("UPDATE requests SET state='STARTED' WHERE id=?",(request_id,))
                evaluating=True
                effective=dict(self.profile)
                effective['eval_fuel']=min(effective['eval_fuel'], max(0,self.profile['max_visit_fuel']-int(self._meta('visit_fuel'))))
                effective['max_allocation_bytes']=min(effective['max_allocation_bytes'], max(0,self.profile['max_visit_allocation']-int(self._meta('visit_alloc'))))
                result=sc.evaluate(expr,namespace,self.load_artifact,effective)
                value=result['value']; usage={k:v for k,v in result.items() if k!='value'}
                if len(canonical(sc.value_wire(value)))>self.profile['max_result_bytes']:
                    raise StoreError('RESULT_BYTES')
                if command=='run-save': artifact=self._artifact('data',value)
                else: status='COMPUTED'
            elif command=='drop':
                if len(ast)!=2: raise StoreError('ARITY')
                alias=self._target(ast[1]); status='ALIAS_DROPPED'
            elif command in ('inspect','list','help','page','page-run'):
                projection=self._projection(ast,namespace,before); status='OBSERVED'
                usage['observation_bytes'] = len(json.dumps(projection, ensure_ascii=False).encode())
            else:
                raise StoreError('UNKNOWN_COMMAND')
            if alias and alias not in namespace and status!='ALIAS_DROPPED' and len(namespace)>=self.profile['max_aliases']:
                raise StoreError('ALIAS_LIMIT')
            return self._finish(row,status,value=value if command in ('run','run-save') else None,projection=projection,
                                artifact=artifact,alias=alias,usage=usage)
        except (sc.GuestError,StoreError) as exc:
            code=exc.code
            usage=getattr(exc,'usage',None) or usage
            if code=='SNAPSHOT_MISMATCH': status='FAILED_PRECONDITION'
            elif any(x in code for x in ('LIMIT','FUEL','BYTES','DEPTH','FRAMES','NODES','STEPS','WORK')): status='FAILED_LIMIT'
            elif evaluating: status='FAILED_EVALUATION'
            else: status='REJECTED_VALIDATION'
            return self._finish(row,status,error={'code':code,'limit':code if status=='FAILED_LIMIT' else None,'source_span':None,'details':{'message':str(exc)[:256]}},usage=usage)
        except Exception:
            # A Python bug is an infrastructure failure, not a guest diagnosis.
            return self._finish(row,'FAILED_HOST_ABORT',error={'code':'HOST_EXCEPTION','limit':None,'source_span':None,'details':{}},usage=usage)

    def _finish(self,row,status,value=None,projection=None,artifact=None,alias=None,error=None,usage=None):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            before=row['before_id']; changes=[]; aids=[]; added=0
            if artifact:
                aid,record,data,is_new=artifact
                self.db.execute('INSERT OR IGNORE INTO artifacts VALUES (?,?,?,?)',(aid,record['kind'],data.decode(),len(data)))
                aids=[aid]; added=len(data) if is_new else 0
            if alias:
                old=self.db.execute('SELECT id FROM aliases WHERE name=?',(alias,)).fetchone()
                old=old['id'] if old else None
                new=None if status=='ALIAS_DROPPED' else artifact[0]
                if new: self.db.execute('INSERT OR REPLACE INTO aliases VALUES (?,?)',(alias,new))
                else: self.db.execute('DELETE FROM aliases WHERE name=?',(alias,))
                changes=[{'name':alias,'before':old,'after':new}]
            after=self._persist_snapshot()
            seq=int(self._meta('sequence'))+1
            consumed=usage or {}
            counters={'eval_fuel':consumed.get('fuel_used',consumed.get('steps',0)+consumed.get('work_units',0)),
                      'logical_alloc_bytes':consumed.get('allocation_bytes',0),'peak_frames':consumed.get('peak_frames',0),
                      'host_work':None,'artifact_bytes_added':added,'observation_bytes':0,**consumed}
            # An interrupted process did not return its counters. Preserve that
            # unknown, and bill a conservative allowance separately from measured
            # work so repeated infrastructure aborts cannot supply free compute.
            fuel_charge = counters['eval_fuel']
            alloc_charge = counters['logical_alloc_bytes']
            if status == 'FAILED_HOST_ABORT' and not usage:
                fuel_charge = min(self.profile['eval_fuel'], max(0, self.profile['max_visit_fuel'] - int(self._meta('visit_fuel'))))
                alloc_charge = min(self.profile['max_allocation_bytes'], max(0, self.profile['max_visit_allocation'] - int(self._meta('visit_alloc'))))
                for key in ('eval_fuel', 'logical_alloc_bytes', 'peak_frames', 'steps', 'work_units', 'fuel_used', 'allocation_bytes'):
                    counters[key] = None
                counters['interrupted_counters_available'] = False
            counters['quota_fuel_charged'] = fuel_charge
            counters['quota_allocation_charged'] = alloc_charge
            core={'schema':'cw-event-1','world_id':self._meta('world_id'),'request_id':row['id'],'request_hash':row['hash'],
                  'status':status,'phase':'commit','commit_certainty':'committed','before_world':before,'after_world':after,
                  'audit_before':{'sequence':self._meta('sequence'),'head':self._meta('head')},'audit_after_sequence':str(seq),
                  'capture_id':(lambda r:r['id'] if r else None)(self.db.execute('SELECT capture_id AS id FROM capture_links WHERE request_id=?',(row['id'],)).fetchone()),'versions':{'language':'cw-scheme-1','evaluator':'cw-eval-1','cost':'cw-cost-1','profile':self.profile['profile_id']},
                  'limits':_safe(self.profile),'usage':_safe(counters),
                  'result':{'value':sc.value_wire(value) if status=='COMPUTED' else None,'artifact_ids':aids,'alias_changes':changes,'projection':_safe(projection)},
                  'error':error,'trace':{'retained_bytes':'0','truncated':False},'host_outcome':{'watchdog':False,'interruption':'HOST' if status=='FAILED_HOST_ABORT' else None}}
            eid=ident('event',core)
            receipt={'schema':'cw-receipt-1','receipt_id':eid,'event':core,'audit_after':{'sequence':str(seq),'head':eid},
                     'status':status,'value':value if status in ('COMPUTED','PUBLISHED') else projection,'error':error,'world_snapshot':after}
            encoded=json.dumps(receipt,ensure_ascii=False,sort_keys=True,separators=(',',':'))
            if len(encoded.encode())>self.profile['max_receipt_bytes']:
                self.db.rollback()
                if error and error['code']=='RECEIPT_BYTES': raise RuntimeError('failure receipt reserve too small')
                return self._finish(row,'FAILED_LIMIT',error={'code':'RECEIPT_BYTES','limit':'RECEIPT_BYTES','source_span':None,'details':{}},usage=usage)
            self.db.execute('INSERT INTO events VALUES (?,?,?)',(seq,eid,canonical(core).decode()))
            self.db.execute("UPDATE requests SET state='TERMINAL',receipt=? WHERE id=?",(encoded,row['id']))
            self._set('sequence',seq); self._set('head',eid)
            self._set('audit_bytes',int(self._meta('audit_bytes'))+len(encoded.encode()))
            self._set('visit_fuel',int(self._meta('visit_fuel'))+int(fuel_charge))
            self._set('visit_alloc',int(self._meta('visit_alloc'))+int(alloc_charge))
            self.db.commit()
            return receipt
        except sqlite3.Error:
            self.db.rollback()
            found=self.db.execute('SELECT receipt FROM requests WHERE id=?',(row['id'],)).fetchone()
            if found and found['receipt']: return json.loads(found['receipt'])
            return self._transport('UNKNOWN_COMMIT',row['id'],commit_certainty='unknown')
