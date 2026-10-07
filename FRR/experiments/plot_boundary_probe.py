"""Plot stored results; no new experiments or confidence intervals."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from adaptive_boundary_probe import prepare

ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'evaluation/results/adaptive-boundary-expansion.json').read_text())
fig,axes=plt.subplots(1,3,figsize=(14,4),layout='constrained')
x,w=prepare(64)
axes[0].plot(x,label='Preparation signal')
axes[0].plot(w,label='Learned conductance')
axes[0].set(xlabel='Site on periodic ring',title='Local rule makes four weak links')
axes[0].legend(fontsize=8)
colors=['#667085','#bc5a45','#267f87','#9a79a9']
names=['fixed_uniform','learned_frozen','common_payload_learned','shuffled_learned']
labels=['Uniform write + hold','Learned write + hold','Uniform write, learned hold','Shuffled write + hold']
for name,label,color in zip(names,labels,colors):
 rows=sorted([s for s in r['summary'] if s['size']==64 and s['condition']==name],key=lambda s:s['horizon'])
 axes[1].plot([s['horizon'] for s in rows],[s['mean_bit_accuracy'] for s in rows],marker='o',label=label,color=color)
axes[1].axhline(.5,color='gray',linestyle=':',label='Chance')
axes[1].set(xlabel='Steps since writing stopped',ylabel='Held-out bit accuracy',ylim=(.45,1.03),title='Retention depends on how writing occurred')
axes[1].legend(fontsize=7)
sizes=r['settings']['sizes']
for i,(name,label,color) in enumerate(zip(names[:3],labels[:3],colors[:3])):
 rows=[next(s for s in r['summary'] if s['size']==n and s['condition']==name and s['horizon']==200) for n in sizes]
 axes[2].bar([k+(i-1)*.23 for k in range(len(sizes))],[s['mean_bit_accuracy'] for s in rows],width=.23,label=label,color=color)
axes[2].set(xticks=list(range(3)),xticklabels=sizes,xlabel='Sites (not AI agents)',ylabel='Held-out bit accuracy',ylim=(0,1.02),title='200-step comparison; common writing matters')
fig.suptitle('Constructed substrate experiment: six message/noise seeds, explicit local adaptation',fontsize=12)
out=ROOT/'evaluation/results/adaptive-boundary-expansion.png'
fig.savefig(out,dpi=160)
fig.savefig(out.with_suffix('.svg'))
print(out)
