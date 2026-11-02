"""POST HOC: fixed-artifact nearest selector versus compatibility withholding."""
import hashlib
import json
from pathlib import Path
import numpy as np

r = Path(__file__).resolve().parent
source = r.parent/'evaluations.npz'
inputs = {'analysis':'POST HOC saved-artifact selector comparison; no new samples',
          'input_npz_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
          'input_summary_sha256':hashlib.sha256((r.parent/'SUMMARY.json').read_bytes()).hexdigest(),
          'analysis_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(r/'INPUTS.json').write_text(json.dumps(inputs,indent=2)+'\n')
z = np.load(source,allow_pickle=False)
base = json.loads((r.parent/'SUMMARY.json').read_text())
classes = np.array(['IND','DIFF','SHARED'])
rows = []
for cell in base['rows']:
    M,world,truth = cell['M'],cell['world'],cell['truth']
    key = f'M{M}_{world}'
    d = z[key+'_distances']
    nearest = classes[d.argmin(1)].astype('<U16')
    nearest[d.min(1)>1] = 'UNKNOWN'
    sets = z[key+'_set']
    multiple = (d<=1).sum(1)>1
    # Changes must be confined to multiple candidates; neither rule changes UNKNOWN.
    assert np.array_equal(nearest=='UNKNOWN',sets=='UNKNOWN')
    assert np.array_equal(nearest!=sets,multiple)
    row = {'M':M,'world':world,'truth':truth,'n':len(sets),'multiple_candidates':int(multiple.sum())}
    for name,labels in [('nearest',nearest),('compatibility',sets)]:
        wrong = np.isin(labels,classes)&(labels!=truth)
        row[name] = {'fractions':{label:float((labels==label).mean()) for label in ['IND','DIFF','SHARED','UNKNOWN','UNRESOLVED']},
            'wrong_specific':float(wrong.mean()),'correct_specific':None if truth is None else float((labels==truth).mean())}
    row['multiple_case_nearest_counts'] = {label:int((multiple&(nearest==label)).sum()) for label in classes}
    row['multiple_case_nearest_wrong_count'] = int((multiple&np.isin(nearest,classes)&(nearest!=truth)).sum())
    row['multiple_case_nearest_correct_count'] = None if truth is None else int((multiple&(nearest==truth)).sum())
    rows.append(row)
(r/'SUMMARY.json').write_text(json.dumps({'inputs':inputs,'rows':rows},indent=2)+'\n')
report = ['# Nearest-selector comparison: post hoc','',
'This analysis reuses the existing 27,000 evaluation runs and their three class-normalized distances. It draws no new samples and performs no model calls. It was requested after inspecting the frozen control results; it is explicitly post hoc. The parent protocol, runner and output artifacts remain untouched.','',
'The nearest rule returns UNKNOWN when every normalized distance exceeds one; otherwise it selects the lowest normalized-distance candidate. Compatibility uses the identical fitted bands and distances, but withholds as UNRESOLVED when more than one candidate is accepted. Thus every difference between these two arms is precisely one of those multiple-candidate cases. This selector rule minimizes distance divided by its class threshold, matching the source’s normalized selection convention.','',
'## All cells','',
'Rates use 1,000 evaluations per cell. For outside worlds any familiar specific claim is scored wrong under the parent authored-category convention; COMMON and UPSTREAM are descriptively SHARED.','',
'| M | World | Multiple count | Nearest wrong | Set wrong | Nearest correct | Set correct | Shared UNKNOWN |',
'|---:|---|---:|---:|---:|---:|---:|---:|']
for x in rows:
    show = lambda v:'—' if v is None else f'{v:.3f}'
    report.append(f"| {x['M']} | {x['world']} | {x['multiple_candidates']} | {x['nearest']['wrong_specific']:.3f} | {x['compatibility']['wrong_specific']:.3f} | {show(x['nearest']['correct_specific'])} | {show(x['compatibility']['correct_specific'])} | {x['nearest']['fractions']['UNKNOWN']:.3f} |")
report+=['','## Interpretation and limits','',
'At M=1600 every world has zero multiple-candidate cases. On known DIFF both selectors make zero wrong-specific claims, return correct DIFF .988, and UNKNOWN .012. Original F_care made wrong-specific claims .728 on these same runs. The DIFF repair at this M therefore comes from replacing the original decision geometry with the calibrated feature-distance bands; it cannot be attributed to withholding multiple candidates. This does not isolate which component of that geometric replacement is responsible.','',
'At smaller M withholding can remove both correct and wrong nearest selections. The per-cell correct rates quantify that cost. On the authored outside worlds, every withheld familiar label mechanically reduces the wrong-specific rate, so that reduction alone does not validate useful recognition. Neither selector identifies a causal route.','',
'Specifically, M=100 IND nearest selects correctly .763 and wrongly .233; the set rule retains correct .083 and wrong .015 while withholding .898. Those withheld cases include 680 correct and 218 wrong nearest selections. DIFF nearest correct/wrong is .835/.165, versus set .239/.003; withholding removes 596 correct and 162 wrong nearest selections. The calibrated nearest arm also has more wrong-specific claims than original F_care at M=100 on IND (.233 versus .032) and DIFF (.165 versus .097). Geometry replacement is therefore not a uniform improvement across sample sizes.','',
'The analysis fixes the earlier fitted means, scales, empirical thresholds, seeds, worlds and feature choices. It isolates selector behavior conditional on those artifacts, not calibration-seed sensitivity, metric choice, independent scientific replication, coverage guarantees, or population performance. The two rules have identical UNKNOWN by construction; zero observed errors are not zero-risk guarantees.','',
'[INPUTS.json](INPUTS.json) records the exact NPZ, parent summary and analysis-script hashes. [SUMMARY.json](SUMMARY.json) includes all cell rates and the nearest labels, correct counts and wrong counts among cases withheld by the set rule. The script asserts that changed labels equal precisely the multiple-candidate mask and that all UNKNOWN masks match. Run `python analyze.py` from this directory to reproduce.']
(r/'REPORT.md').write_text('\n'.join(report)+'\n')
print(json.dumps({'cells':len(rows),'assertions':'all selector differences exactly multiple-candidate cases; UNKNOWN masks identical','M100': [x for x in rows if x['M']==100 and x['world'] in ['IND','DIFF'] ]},indent=2))
