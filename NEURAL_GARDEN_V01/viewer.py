"""Create a portable offline HTML replay from Garden snapshot JSON files.

Usage: python viewer.py RUN_DIRECTORY [--output garden_replay.html]
"""

import argparse
import json
from pathlib import Path


HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Neural Garden — Replay</title>
<style>
:root{color-scheme:dark}body{font-family:ui-sans-serif,system-ui;background:#081411;color:#d8ebd8;margin:0;padding:24px}
main{max-width:970px;margin:auto}h1{font-weight:500;letter-spacing:.04em}small,.muted{color:#90aaa0}
.panel{background:#10241f;border:1px solid #28483c;border-radius:16px;padding:18px;margin:15px 0}
.layout{display:grid;grid-template-columns:minmax(260px,1fr) minmax(210px,280px);gap:20px}
canvas{width:100%;height:auto;image-rendering:pixelated;border-radius:10px;background:#07100f}
label{display:block;font-size:13px;color:#a7c7b5;margin:10px 0}input[type=range]{width:100%}
button,select{background:#183e33;color:#ddf2dc;border:1px solid #36765b;border-radius:9px;padding:9px 12px;cursor:pointer}
.buttons{display:flex;gap:8px;flex-wrap:wrap}.metric{display:flex;justify-content:space-between;border-bottom:1px solid #244238;padding:7px 0;font-size:13px}
@media(max-width:650px){.layout{grid-template-columns:1fr}}
</style></head><body><main>
<h1>🌱 Neural Garden <small>recorded world states</small></h1>
<p class="muted">Independent neural controllers in each cell · snapshots captured from a reproducible simulation · replay is read-only</p>
<div class="panel layout"><div><canvas id="world" width="640" height="640" aria-label="Garden grid"></canvas>
<label>Recorded step <span id="position"></span><input id="timeline" type="range" min="0" step="1" value="0"></label>
<div class="buttons"><button id="play">▶ Play</button><button id="back">←</button><button id="forward">→</button><select id="layer"><option value="resource">Resources</option><option value="energy">Cell energy</option><option value="activity">Cell activity</option></select></div></div>
<div><h3>Current snapshot</h3><div id="metrics"></div><p class="muted">Colors show each cell's recorded value. This viewer does not run the neural networks or modify the experiment.</p></div></div>
<p class="muted" id="count"></p></main>
<script>const snapshots=__DATA__;const canvas=document.getElementById('world'),cx=canvas.getContext('2d');const timeline=document.getElementById('timeline'),layer=document.getElementById('layer');let idx=0,timer=null;
timeline.max=Math.max(0,snapshots.length-1);document.getElementById('count').textContent=snapshots.length+' recorded snapshots';
function render(){if(!snapshots.length)return;const s=snapshots[idx],grid=s[layer.value];if(!grid)return;const n=s.size||grid.length,cell=canvas.width/n;cx.fillStyle='#07100f';cx.fillRect(0,0,640,640);
const values=grid.flat(),min=Math.min(...values),max=Math.max(...values),range=max-min||1;
for(let y=0;y<n;y++)for(let x=0;x<n;x++){let v=(grid[y][x]-min)/range;const hue=155-v*90;cx.fillStyle='hsl('+hue+',62%,'+(14+v*55)+'%)';cx.fillRect(x*cell+1,y*cell+1,cell-2,cell-2)}
timeline.value=idx;document.getElementById('position').textContent=s.tick;let m=s.metrics||{};document.getElementById('metrics').innerHTML=Object.entries(m).map(([k,v])=>'<div class="metric"><span>'+k.replaceAll('_',' ')+'</span><strong>'+(typeof v==='number'?Number(v).toFixed(4):String(v))+'</strong></div>').join('');}
function set(i){idx=Math.max(0,Math.min(snapshots.length-1,i));render()}timeline.oninput=()=>set(Number(timeline.value));layer.onchange=render;document.getElementById('back').onclick=()=>set(idx-1);document.getElementById('forward').onclick=()=>set(idx+1);
document.getElementById('play').onclick=()=>{if(timer){clearInterval(timer);timer=null;document.getElementById('play').textContent='▶ Play'}else{timer=setInterval(()=>{if(idx>=snapshots.length-1){clearInterval(timer);timer=null;document.getElementById('play').textContent='▶ Play'}else set(idx+1)},180);document.getElementById('play').textContent='⏸ Pause'}};
render();</script></body></html>'''


def main():
    p = argparse.ArgumentParser()
    p.add_argument("run_dir", type=Path)
    p.add_argument("--output", type=Path, default=Path("garden_replay.html"))
    args = p.parse_args()
    files = sorted((args.run_dir / "snapshots").glob("*.json"))
    if not files and (args.run_dir / "snapshot.json").exists():
        files = [args.run_dir / "snapshot.json"]
    if not files:
        raise SystemExit("No snapshots found: run the Garden with snapshot recording enabled")
    # Operational snapshots wrap the raw world view in a provenance envelope.
    snapshots = [json.loads(f.read_text(encoding="utf-8")) for f in files]
    snapshots = [entry.get("garden", entry) for entry in snapshots]
    text = HTML.replace("__DATA__", json.dumps(snapshots, separators=(",", ":")).replace("</", "<\\/"))
    args.output.write_text(text, encoding="utf-8")
    print(f"Wrote {args.output} with {len(snapshots)} snapshots")


if __name__ == "__main__":
    main()
