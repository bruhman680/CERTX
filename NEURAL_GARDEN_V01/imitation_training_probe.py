"""Second exploratory probe: teach, freeze, deploy deterministic neural action.

The teacher is explicit. This tests representational capacity, not discovery.
"""
import json
from pathlib import Path
from imitation_garden import ImitationGarden

def main():
    data={"seed_range": [760,764], "pretrain_ticks": 250,
          "test_ticks": 600, "arms": {}, "note": "teacher labels supplied"}
    for lr in (.22, .5, 1.):
        rows=[]
        for seed in range(760,765):
            obj=ImitationGarden(seed=seed, size=16, imitation_rate=lr)
            for _ in range(250): obj.step()
            trained_accuracy=obj.metrics()['teacher_imitation_accuracy']
            obj.learning=False
            obj.deterministic_action=True
            for _ in range(600): obj.step()
            rows.append({"seed":seed,"train_accuracy":trained_accuracy,
                         "test_energy":obj.metrics()['mean_energy'],
                         "test_resource":obj.metrics()['mean_resource'],
                         "test_accuracy":obj.metrics()['teacher_imitation_accuracy']})
        data["arms"][str(lr)]=rows
        print(lr, "mean_deployed_energy",sum(r['test_energy'] for r in rows)/len(rows),
              "accuracy",sum(r['test_accuracy'] for r in rows)/len(rows),flush=True)
    Path(__file__).with_name('imitation_training_probe.json').write_text(json.dumps(data,indent=2)+'\n')

if __name__=='__main__': main()
