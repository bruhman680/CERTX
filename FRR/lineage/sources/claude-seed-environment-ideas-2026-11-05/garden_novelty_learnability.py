"""
GARDEN NOVELTY/LEARNABILITY PROXY (Claude, 2026-11-05). Crude, observer-side, model-free reading of Hughes et al. (arXiv 2406.04268): an artifact stream is 'novel' if later items stay hard to predict from the past, 'learnable' if a longer past makes them easier.
Observer model = zlib with the preceding text as preset dictionary (last 32 KB). For each block of 50 consecutive primary-garden replies (steps 50..499, events/*.json 'text' field) compute
   c = len(zlib(block | prior text)) / len(zlib(block alone))      (conditional / unconditional compressed size; lower = more predictable from the past)
plus the number of distinct exact replies in the block. Read-only on Codex's saved events; no model, no generation.
Scope: zlib is a weak observer model and the stream is one dependent trajectory from a 135M model; this is a descriptive signature, not a test of curiosity or emergence.
PREDICTIONS (written before running):
 N1 c in blocks 400-499 is at least 1.5x lower than c in blocks 50-149 (late stream is far more predictable from its past).
 N2 distinct replies per block of 50 is lower in 400-499 than in 50-149.
 N3 c is not monotone: some block in 150-399 has c higher than the first block's (new material arrives when the scaffold changes, e.g. the 305 world introduction or the 225 invitation).
"""
import json,glob,zlib
D='/home/claude/bruhman680/certx/FRR/evaluation/source-access-three-cycle-v1/cycle3/environment/events/'
ev=sorted((json.load(open(f)) for f in glob.glob(D+'*.json')),key=lambda d:d['step'])
txt=[(d['step'],d['text']) for d in ev if d['step']>=50]
def comp(b): return len(zlib.compress(b,9))
rows=[]; hist=b''
for i in range(0,len(txt),50):
    blk=txt[i:i+50]; raw='\n<<>>\n'.join(t for _,t in blk).encode(); 
    zd=zlib.compressobj(9,zlib.DEFLATED,15,9,zlib.Z_DEFAULT_STRATEGY,hist[-32768:]) if hist else None
    cond=len(zd.compress(raw)+zd.flush()) if zd else comp(raw)
    c=cond/comp(raw); dist=len(set(t for _,t in blk)); rows.append((blk[0][0],blk[-1][0],c,dist,comp(raw)/max(len(raw),1)))
    hist+=raw+b'\n'
print("block steps   cond/uncond   distinct/50   uncond compress ratio")
for a,b,c,d,u in rows: print(f"{a:3d}-{b:3d}     {c:6.3f}        {d:3d}          {u:5.3f}")
early=[r for r in rows if 50<=r[0]<150]; late=[r for r in rows if r[0]>=400]; mid=[r for r in rows if 150<=r[0]<400]
import statistics as st
me=st.mean(r[2] for r in early); ml=st.mean(r[2] for r in late)
print(f"\nN1 mean c early(50-149) {me:.3f} vs late(400-499) {ml:.3f}; ratio early/late = {me/ml:.2f}")
print(f"N2 mean distinct/50 early {st.mean(r[3] for r in early):.1f} vs late {st.mean(r[3] for r in late):.1f}")
first=rows[0][2]; print(f"N3 first block c {first:.3f}; mid-period blocks with c above that: {[ (r[0],round(r[2],3)) for r in mid if r[2]>first]}")
