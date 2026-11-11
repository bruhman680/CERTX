"""Independent mild-regime transfer and online-adaptation stress test.

Original Garden v0.1 world except that resource regeneration is .055 instead
of .06 during test internal ticks 1000..1999. There is NO exogenous shock and
no harvesting cost change. This file does not mutate other simulator sources.
"""
import hashlib,json,platform
from pathlib import Path
import numpy as np
from ADAPTIVE_threshold import AdaptiveThresholdGarden


class MildRegimeGarden(AdaptiveThresholdGarden):
    def step(self):
        resource=self.resource.copy();energy=self.energy.copy()
        regrowth=.055 if 1000<=self.tick<2000 else .06
        p=self._sigmoid(self.slope*(resource-self.thresholds))
        action=((resource>self.thresholds) if self.deterministic
                else (self.rng_action.random(self.count)<p)).astype(float)
        diffusion=.08*(self._neighbors(resource)-resource)
        next_resource=np.clip(resource+diffusion+regrowth*(1.-resource)-.18*resource*action,0.,1.)
        raw=.25*resource*action-.03-.055*action+.008*(1.-action)
        next_energy=np.clip(energy+raw,0.,1.)
        realized=next_energy-energy
        if self.learning:
            score=-self.slope*(action-p)
            self.traces=self.trace_decay*self.traces+score
            advantage=realized-self.value_baseline
            update=np.clip(self.lr*advantage*self.traces,-.01,.01)
            self.thresholds=np.clip(self.thresholds+update,.05,.95)
            self.value_baseline=.99*self.value_baseline+.01*realized
        self.resource=next_resource;self.energy=next_energy
        self.prev_action=action;self.last_action=action.copy()
        self.prev_reward=realized;self.last_raw_delta=raw
        self.tick+=1
        self._last={"tick":self.tick,"mean_energy":float(next_energy.mean()),
                    "mean_resource":float(next_resource.mean()),
                    "harvest_rate":float(action.mean()),
                    "raw_energy_drift":float(raw.mean()),
                    "mean_threshold":float(self.thresholds.mean()),
                    "prediction_mse":None,"mean_reward":float(realized.mean()),
                    "weight_update_rms":float(np.sqrt(np.mean(update**2))) if self.learning else 0.,
                    "regrowth":regrowth}
        return self.metrics()


ARMS=('online','frozen_stochastic','frozen_deterministic','untrained_stochastic','fixed50','fixed51')
CHECKPOINTS=(999,1200,1600,1999,2200,2600,3000)

def run():
    rows=[]
    for training_seed in range(3200,3220):
        trained=AdaptiveThresholdGarden(seed=training_seed,size=16,learning=True)
        init_thresholds=trained.thresholds.copy()
        for _ in range(1200):trained.step()
        test_seed=training_seed+10000
        worlds={
            'online':MildRegimeGarden(seed=test_seed,size=16,learning=True,deterministic=False),
            'frozen_stochastic':MildRegimeGarden(seed=test_seed,size=16,learning=False,deterministic=False),
            'frozen_deterministic':MildRegimeGarden(seed=test_seed,size=16,learning=False,deterministic=True),
            'untrained_stochastic':MildRegimeGarden(seed=test_seed,size=16,learning=False,deterministic=False),
            'fixed50':MildRegimeGarden(seed=test_seed,size=16,learning=False,deterministic=True),
            'fixed51':MildRegimeGarden(seed=test_seed,size=16,learning=False,deterministic=True)}
        for arm in ('online','frozen_stochastic','frozen_deterministic'):
            worlds[arm].thresholds=trained.thresholds.copy()
        worlds['untrained_stochastic'].thresholds=init_thresholds.copy()
        worlds['fixed50'].thresholds[:]=.50
        worlds['fixed51'].thresholds[:]=.51
        assert all(np.array_equal(w.energy,worlds['online'].energy) and
                   np.array_equal(w.resource,worlds['online'].resource) for w in worlds.values())
        tail={arm:[] for arm in ARMS}
        for tick in range(1,3001):
            for arm,world in worlds.items():
                before=world.resource.copy()
                world.step()
                raw=float(world.last_raw_delta.mean())
                tail[arm].append(raw)
                if tick in CHECKPOINTS:
                    a=world.last_action;r=before
                    rows.append({"train_seed":training_seed,"test_seed":test_seed,
                        "arm":arm,"tick":tick,"regrowth_rate":world.metrics()['regrowth'],
                        "energy":float(world.energy.mean()),
                        "resource":float(world.resource.mean()),
                        "floor_fraction":float(np.mean(world.energy<=.01)),
                        "ceiling_fraction":float(np.mean(world.energy>=.99)),
                        "energetic_fraction":float(np.mean(world.energy>.1)),
                        "raw_drift":raw,
                        "tail100_raw_drift":float(np.mean(tail[arm][-100:])),
                        "resource_action_cov":float(np.mean((r-r.mean())*(a-a.mean()))),
                        "threshold_mean":float(world.thresholds.mean())})
    summary={}
    for tick in CHECKPOINTS:
        summary[str(tick)]={}
        for arm in ARMS:
            rr=[r for r in rows if r['arm']==arm and r['tick']==tick]
            summary[str(tick)][arm]={k:float(np.mean([r[k] for r in rr]))
                                      for k in ('energy','resource','floor_fraction',
                                                'energetic_fraction','tail100_raw_drift','resource_action_cov')}
    p=Path(__file__).resolve().parent
    sources={f:hashlib.sha256((p/f).read_bytes()).hexdigest()
             for f in ('garden.py','ADAPTIVE_threshold.py','MILD_REGIME_probe.py')}
    result={"design":"posthoc exploratory mild single-variable regrowth change",
            "size":16,"training_seeds":list(range(3200,3220)),
            "test_seeds":list(range(13200,13220)),"training_ticks":1200,
            "test_ticks":3000,"world_regimes":[[0,999,.06],[1000,1999,.055],[2000,2999,.06]],
            "arms":list(ARMS),"python":platform.python_version(),"numpy":np.__version__,
            "sources":sources,"summary":summary,"rows":rows}
    (p/'MILD_REGIME_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({t:{a:round(v['energy'],4) for a,v in d.items()} for t,d in summary.items()},indent=2))

if __name__=='__main__':run()
