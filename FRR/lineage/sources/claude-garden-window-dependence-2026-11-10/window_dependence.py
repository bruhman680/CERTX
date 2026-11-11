# Post-hoc exploratory reading of saved garden events 851-1550 (final-garden-contract-v1/run/events).
# Usage: python3 window_dependence.py <path to .../final-garden-contract-v1/run/events>  (events live on Codex branch codex/frr-progress-2026-10-07, not on this branch)
import json,glob,collections,sys
p=sorted(glob.glob(sys.argv[1].rstrip('/')+'/*.json'))
T=[json.load(open(f))['text'] for f in p]
L=[1 if 'Laws' in t else 0 for t in T]   # 1 = "Laws.txt" (not the real spelling), 0 = "LAWS.txt" (real spelling)
tab=collections.defaultdict(lambda:[0,0])
for i in range(12,len(L)):
    tab[sum(L[i-12:i])][L[i]]+=1
print("k = number of 'Laws' replies among the previous 12 | n | P(next reply = 'Laws')")
for k in sorted(tab):
    n=sum(tab[k]); print(k,n,round(tab[k][1]/n,3))
last=max(i for i,x in enumerate(L) if x==1)
print("last 'Laws' reply at entry",851+last,"; window before it:",L[last-12:last])
