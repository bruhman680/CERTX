"""Task-relative summary witnesses, not an ETH algorithm or reproduction."""
from collections import defaultdict
from pathlib import Path
import json

rows=[]
for n in (4,8,12):
    by_count=defaultdict(list)
    by_binary=defaultdict(list)
    for x in range(1<<n):
        bits=tuple((x>>i)&1 for i in range(n))
        by_count[sum(bits)].append(bits)
        by_binary[sum((1<<i)*b for i,b in enumerate(bits))].append(bits)
    def mixed(groups,target):
        return sum(len({target(b) for b in members})>1 for members in groups.values())
    record={'n':n,'assignments':1<<n,'row_rank_both_maps':1,
            'count_summary_states':len(by_count),'binary_summary_states':len(by_binary),
            'count_row_l1':n,'binary_row_l1':(1<<n)-1,
            'count_first_bit_mixed_classes':mixed(by_count,lambda b:b[0]),
            'count_parity_mixed_classes':mixed(by_count,lambda b:sum(b)%2),
            'binary_first_bit_mixed_classes':mixed(by_binary,lambda b:b[0])}
    assert record['count_summary_states']==n+1
    assert record['binary_summary_states']==1<<n
    assert record['count_first_bit_mixed_classes']==n-1
    assert record['count_parity_mixed_classes']==0
    assert record['binary_first_bit_mixed_classes']==0
    rows.append(record)
out={'scope':'authored finite witnesses; exact enumeration; no learned encoder, SAT solver or proof rebuild',
     'rows':rows,'assignments_enumerated':sum(r['assignments'] for r in rows)}
p=Path(__file__).resolve().parent
(p/'WITNESS_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
