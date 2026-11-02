"""Two-claim, six-query declared temporal fixture; not an implementation of XTDB."""
CLAIMS=[{'id':'e1','received':1,'effective_from':1,'state':'ready','corrects':None},
        {'id':'e2','received':3,'effective_from':2,'state':'blocked','corrects':'e1'}]
EXPECT={(1,1):'ready',(1,2):'ready',(2,1):'ready',(2,2):'ready',(3,1):'ready',(3,2):'blocked'}
def query(claims,cutoff,effective):
 eligible=[c for c in claims if c['received']<=cutoff and c['effective_from']<=effective]
 superseded={c['corrects'] for c in eligible if c['corrects'] is not None}
 heads=[c for c in eligible if c['id'] not in superseded]
 if len(heads)!=1:raise ValueError('Outside this two-claim temporal contract')
 c=heads[0]
 return {'cutoff':cutoff,'effective':effective,'state':c['state'],'witness':c['id'],'eligible':[c['id'] for c in eligible]}
def contact():
 rows=[]
 for (cutoff,effective),expected in EXPECT.items():
  r=query(CLAIMS,cutoff,effective);assert r['state']==expected;rows.append(r)
 before=query(CLAIMS[:1],2,2);after=query(CLAIMS,2,2);assert before==after
 return {'scope':'authored functional example; no model calls, no real effective dates inferred','claims':CLAIMS,'queries':rows,'frozen_earlier_view_preserved':True,'no_timestamps_inferred_from_git':True}
