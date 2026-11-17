"""Operator fixtures only; temporary stores, no model or protected garden imports."""
import hashlib
import json
import random
import tempfile
from pathlib import Path
from medium import create, complete, recover_pending, read, evolve, inverse, encode, LIMIT

passed=[]
def check(name, predicate):
    assert predicate, name
    passed.append(name)

def run():
    for x in range(65536):
        data=x.to_bytes(2,'little')
        assert inverse(evolve(data))==data and evolve(inverse(data))==data
    check('all 65536 two-byte states invert both ways', True)
    rng=random.Random(20261117)
    for length in [0,1,2,3,4,5,6,14,16,60,62,63,64,126,1024,65535,65536]:
        for _ in range(8):
            data=rng.randbytes(length)
            assert inverse(evolve(data))==data and evolve(inverse(data))==data
            assert len(evolve(data))==length
            if length%2:assert evolve(data)[-1]==data[-1]
    check('136 seeded variable-length inverse/length/tail cases', True)
    check('absence is not recreated',evolve(None) is None)
    initial=bytes([1,0])+bytes(60)
    def orbit(data, limit=4096):
        start=data
        for n in range(1,limit+1):
            data=evolve(data)
            if data==start:return {'return_tick':n,'search_limit':limit}
        return {'return_tick':None,'search_limit':limit}
    samples={'single_perturbation_31_pairs':orbit(initial),'seeded_bytes_31_pairs':orbit(random.Random(19).randbytes(62)),
             'all_zero_31_pairs':orbit(bytes(62)),'uniform_pair_31_pairs':orbit(bytes([3,7])*31)}
    # A change at one even byte reaches its paired odd byte first, then neighbors.
    check('local causal effect agrees with declared XOR rule', evolve(initial)==bytes([0,1])+bytes(60))
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); a=td/'static.json';b=td/'changing.json'
        create(a,'static',initial);create(b,'changing',initial)
        check('matched initial material',read(a)['material']==read(b)['material'])
        snapshot=b.read_bytes()
        for _ in range(3):read(b)
        check('reads/paused wall time do not tick',snapshot==b.read_bytes())
        ea=complete(a,'r1',[]);eb=complete(b,'r1',[])
        check('no-action completion ticks once in both conditions',ea['tick']==eb['tick']==1 and ea['operation_count']==eb['operation_count']==0)
        check('only declared dynamic law changes idle material',ea['after']==encode(initial) and eb['after']==encode(evolve(initial)))
        saved=b.read_bytes();retry=complete(b,'r1',[])
        check('identical retry does not replay or tick',saved==b.read_bytes() and retry==eb)
        try:complete(b,'r1',[{'kind':'delete'}])
        except ValueError:pass
        else:raise AssertionError('conflicting retry accepted')
        check('conflicting identity refuses unchanged',saved==b.read_bytes())
        ops=[{'kind':'delete'},{'kind':'append','bytes':encode(b'x')},{'kind':'write','bytes':encode(b'abc')}, {'kind':'append','bytes':encode(b'd')}]
        ev=complete(b,'r2',ops)
        check('ordinary error allows later write/append', [r['status'] for r in ev['receipts']]==['ok','error','ok','ok'] and ev['pre_tick']==encode(b'abcd') and ev['after']==encode(evolve(b'abcd')))
        ev=complete(b,'r3',[{'kind':'delete'}]); ev2=complete(b,'r4',[])
        check('deleted material stays absent across ticks',ev['after'] is None and ev2['after'] is None)
        ev=complete(b,'r5',[{'kind':'write','bytes':encode(b'') }])
        check('empty material is valid',ev['after']==encode(b''))
        ev=complete(b,'r6',[{'kind':'write','bytes':encode(bytes(LIMIT+1))}])
        check('capacity error preserves material but completion ticks',ev['receipts'][0]['status']=='error' and ev['after']==encode(b'') and ev['tick']==6)
        saved=b.read_bytes()
        try:complete(b,'r7',[{'kind':'write','bytes':encode(b'xyz')}],fail_at='before_replace')
        except InterruptedError:pass
        else:raise AssertionError('crash missing')
        check('pre-replace interruption leaves committed state intact',b.read_bytes()==saved)
        try:complete(b,'r7',[])
        except RuntimeError:pass
        else:raise AssertionError('pending overwritten')
        check('unknown pending refuses automatic overwrite',b.read_bytes()==saved)
        recovery=recover_pending(b); check('explicit pending recovery commits one recomputed tick',read(b)['tick']==7 and recovery['after']==encode(evolve(b'xyz')))
        saved=b.read_bytes();complete(b,'r7',[{'kind':'write','bytes':encode(b'xyz')}])
        check('recovery retry is idempotent',saved==b.read_bytes())
        try:complete(b,'r8',[],fail_at='after_replace')
        except InterruptedError:pass
        else:raise AssertionError('crash missing')
        saved=b.read_bytes();complete(b,'r8',[])
        check('post-replace process interruption does not duplicate tick',saved==b.read_bytes() and read(b)['tick']==8)
        # Reopen through independent reads, without an in-memory world object.
        check('reopen retains exact material and counters',read(b)['material']==encode(evolve(evolve(b'xyz'))) and read(b)['tick']==8 and read(b)['operation_count']==8)
        try:complete(b,'r9',[],fail_at='before_replace')
        except InterruptedError:pass
        pending=b.with_name(b.name+'.pending');bad=json.loads(pending.read_text());bad['material']=encode(b'forged');pending.write_text(json.dumps(bad))
        saved=b.read_bytes()
        try:recover_pending(b)
        except ValueError:pass
        else:raise AssertionError('corrupt pending accepted')
        check('altered pending proposal refuses with evidence retained',saved==b.read_bytes() and pending.exists())
    return {'checks_passed':len(passed),'checks':passed,'orbit_samples':samples,
            'model_calls':0,'candidate_world_actions':0,'scope':'pure material and single-writer atomic state fixture; not subprocess execution integration or OS power-loss coverage'}

if __name__=='__main__':
    out=run();Path(__file__).with_name('RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
