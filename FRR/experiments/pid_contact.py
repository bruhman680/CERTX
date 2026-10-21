"""Fixed illustrative control comparisons, not a reasoning-agent experiment."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evaluation/pid-contact-v1'


def settings():
    return dict(dt=.1,steps=400,
        plant='y_next=y+dt*(-y+u+disturbance); sensor=y+bias+noise; y0=0',
        gains=dict(kp=.8,ki=.4,kd=.2),derivative_filter_memory=.85,
        controllers=['P','PI','PI_clamped','PID','PID_filtered','PID_clamped','PID_filtered_clamped'],
        scenarios=['constant_load','saturation_release','noisy_sensor','biased_sensor'],noise_seeds=list(range(30)),
        ordinary_target=1.,load_disturbance=-.4,ordinary_actuator=[0.,2.],
        saturation_target_before=3.,saturation_target_after=.2,saturation_change_step=200,saturation_actuator=[0.,1.],
        noise_alternating_amplitude=.06,noise_gaussian_sd=.02,sensor_bias=.4,
        settling_tolerance=.05,summary_tail_steps=50,
        scope='One fixed constructed first-order plant; hand-chosen gains, no tuning or independent confirmation')


def prepare():
    if (OUT/'SETTINGS.json').exists():raise SystemExit('Refusing to overwrite settings')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'SETTINGS.json').write_text(json.dumps(settings(),indent=2)+'\n')
    paths=['experiments/pid_contact.py','evaluation/pid-contact-v1/SETTINGS.json','evaluation/pid-contact-v1/PROTOCOL.md']
    (OUT/'LAUNCH_MANIFEST.json').write_text(json.dumps(dict(status='Before simulation execution',
        hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}),indent=2)+'\n')
    print(json.dumps(dict(prepared=True,controller_count=7,scenario_seed_instances=33,total_runs=231)))


def simulate(s,scenario,controller,seed=0):
    dt=s['dt'];n=s['steps'];rng=np.random.default_rng(seed)
    noise=np.zeros(n)
    if scenario=='noisy_sensor':
        noise=s['noise_alternating_amplitude']*((-1.)**np.arange(n))+rng.normal(0,s['noise_gaussian_sd'],n)
    kp=s['gains']['kp'];ki=0 if controller=='P' else s['gains']['ki']
    kd=s['gains']['kd'] if controller.startswith('PID') else 0
    rho=s['derivative_filter_memory'] if 'filtered' in controller else 0
    clamp='clamped' in controller
    limits=s['saturation_actuator'] if scenario=='saturation_release' else s['ordinary_actuator']
    disturbance=s['load_disturbance'] if scenario=='constant_load' else 0
    bias=s['sensor_bias'] if scenario=='biased_sensor' else 0
    y=0.;integral=0.;derivative=0.;previous=None;rows=[]
    for t in range(n):
        target=(s['saturation_target_before'] if t<s['saturation_change_step'] else s['saturation_target_after']) if scenario=='saturation_release' else s['ordinary_target']
        measured=y+bias+noise[t];error=target-measured
        raw_derivative=0. if previous is None else -(measured-previous)/dt
        derivative=rho*derivative+(1-rho)*raw_derivative
        candidate_integral=integral+ki*error*dt
        raw=kp*error+candidate_integral+kd*derivative
        prevent=clamp and ((raw>limits[1] and error>0) or (raw<limits[0] and error<0))
        if prevent:
            raw=kp*error+integral+kd*derivative
        else:
            integral=candidate_integral
        applied=float(np.clip(raw,*limits))
        rows.append([float(t*dt),float(target),float(y),float(measured),applied,float(raw),float(integral)])
        y+=dt*(-y+applied+disturbance);previous=measured
    a=np.asarray(rows);target=a[:,1];truth=a[:,2];measured=a[:,3];u=a[:,4];tail=slice(-s['summary_tail_steps'],None)
    recovery=None
    if scenario=='saturation_release':
        err=np.abs(truth-target);switch=s['saturation_change_step']
        # First point after switch remaining within tolerance until the end.
        for t in range(switch,n):
            if np.all(err[t:]<=s['settling_tolerance']):recovery=float((t-switch)*dt);break
    metrics=dict(tracking_mse=float(np.mean((target-truth)**2)),tail_true_mae=float(np.mean(np.abs(target[tail]-truth[tail]))),
        tail_sensor_mae=float(np.mean(np.abs(target[tail]-measured[tail]))),
        actuator_total_variation=float(np.abs(np.diff(u)).sum()),actuator_effort=float(dt*np.abs(u).sum()),
        maximum_abs_integral=float(np.abs(a[:,6]).max()),saturation_fraction=float(np.mean((a[:,5]<limits[0])|(a[:,5]>limits[1]))),
        recovery_seconds=recovery)
    return dict(scenario=scenario,controller=controller,seed=seed,metrics=metrics,trajectory=rows)


def run():
    manifest=json.loads((OUT/'LAUNCH_MANIFEST.json').read_text())
    checks={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in manifest['hashes'].items()}
    if not all(checks.values()):raise ValueError('Frozen source changed')
    s=json.loads((OUT/'SETTINGS.json').read_text());start=time.perf_counter();runs=[]
    for scenario in s['scenarios']:
        seeds=s['noise_seeds'] if scenario=='noisy_sensor' else [0]
        for seed in seeds:
            for controller in s['controllers']:runs.append(simulate(s,scenario,controller,seed))
    elapsed=time.perf_counter()-start
    if any(not np.isfinite(np.asarray(r['trajectory'])).all() for r in runs):raise ValueError('Nonfinite trajectory')
    for r in runs:
        limits=s['saturation_actuator'] if r['scenario']=='saturation_release' else s['ordinary_actuator']
        if not all(limits[0]<=v[4]<=limits[1] for v in r['trajectory']):raise ValueError('Applied actuator outside bounds')
    summaries=[]
    for scenario in s['scenarios']:
        for controller in s['controllers']:
            group=[r for r in runs if r['scenario']==scenario and r['controller']==controller]
            metrics={}
            for key in group[0]['metrics']:
                vals=[r['metrics'][key] for r in group]
                metrics[key]=None if any(v is None for v in vals) else float(np.mean(vals))
            summaries.append(dict(scenario=scenario,controller=controller,runs=len(group),mean_metrics=metrics))
    get=lambda scenario,controller:next(r for r in summaries if r['scenario']==scenario and r['controller']==controller)['mean_metrics']
    p_expected=(s['gains']['kp']*s['ordinary_target']+s['load_disturbance'])/(1+s['gains']['kp'])
    p_actual=next(r for r in runs if r['scenario']=='constant_load' and r['controller']=='P')['trajectory'][-1][2]
    validation=dict(finite_and_bounded=True,P_steady_state_expected=p_expected,P_last_recorded_y=p_actual,
        P_steady_state_absolute_error=abs(p_actual-p_expected),launch_hashes_unchanged=all(checks.values()))
    if abs(p_actual-p_expected)>1e-10:raise ValueError('P fixed-point mismatch')
    predictions=dict(PI_reduces_tail_error_vs_P_in_constant_load=get('constant_load','PI')['tail_true_mae']<get('constant_load','P')['tail_true_mae'],
        clamping_reduces_release_recovery_time=get('saturation_release','PID_clamped')['recovery_seconds'] is not None and
            (get('saturation_release','PID')['recovery_seconds'] is None or get('saturation_release','PID_clamped')['recovery_seconds']<get('saturation_release','PID')['recovery_seconds']),
        derivative_filter_reduces_actuator_variation=get('noisy_sensor','PID_filtered')['actuator_total_variation']<get('noisy_sensor','PID')['actuator_total_variation'],
        biased_sensor_can_track_with_wrong_true_state=get('biased_sensor','PI')['tail_sensor_mae']<.01 and get('biased_sensor','PI')['tail_true_mae']>.35)
    result=dict(study='PID-C1',settings=s,runs=runs,summary=summaries,validation=validation,prediction_checks=predictions,
                run_count=len(runs),internal_compute_seconds=elapsed,model_calls=0,
                scope='Constructed control behavior, not agent reasoning efficacy or a tuned controller ranking')
    (OUT/'RESULTS.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    compact={k:v for k,v in result.items() if k!='runs'}
    (OUT/'SUMMARY.json').write_text(json.dumps(compact,indent=2)+'\n')
    print(json.dumps(dict(run_count=len(runs),seconds=elapsed,validation=validation,prediction_checks=predictions,summary=summaries),indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['prepare','run']);a=p.parse_args();prepare() if a.mode=='prepare' else run()
