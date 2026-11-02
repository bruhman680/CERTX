import pathlib,subprocess,hashlib,json,sys,time
r=pathlib.Path(__file__).resolve().parent
s=r/'sources/FRR/lineage/sources'; out=r/'replays';out.mkdir(exist_ok=True)
results=[]
for folder,script in [('claude-open-world-guard-2026-11-02','open_world_guard'),('claude-open-world-guard-2026-11-02','open_world_power_followup'),('claude-phase3-and-scout-contacts-2026-11-02','phase3_promoted_classes'),('claude-phase3-and-scout-contacts-2026-11-02','metric_cliff_and_distractor')]:
 p=s/folder;t=time.monotonic();run=subprocess.run([sys.executable,script+'.py'],cwd=p,capture_output=True,timeout=180)
 (out/(script+'_stdout.txt')).write_bytes(run.stdout);(out/(script+'_stderr.txt')).write_bytes(run.stderr)
 old=(p/(script+'_output.txt')).read_bytes();row={'script':script,'returncode':run.returncode,'seconds':round(time.monotonic()-t,3),'exact_saved_stdout_match':old==run.stdout,'saved_sha256':hashlib.sha256(old).hexdigest(),'replay_sha256':hashlib.sha256(run.stdout).hexdigest()};results.append(row);print(json.dumps(row),flush=True)
(r/'REPLAY_CHECKS.json').write_text(json.dumps({'python':sys.version,'results':results},indent=2)+'\n')
