# Current FRR orientation

30 October2026 America/Chicago. [Handoff](../CURRENT_HANDOFF.md), [latest report](../evaluation/narrow-training-pilot-v1/REPORT.md), [checkpoint](checkpoints/AFTER_NARROW_TRAINING_2026-10-30.md).

Firstactualfullweighttraining:1AdamWstep beforememoryheadroomguard, notplanned48steps. Partialcheckpoint+optimizerseparate;originalweights unchanged.120evalcalls; structuraltest4/48original vs16/48adapted, adaptedallNO/tiesconstantbaseline. No intendedsemanticdiscrimination shown; actualbatchcontainedzero+positive,no missingclass.272tensors numericallychanged.120newcache/tokenchecks;370oldmodel/cachefilesunchanged. Data/inputguardpreparationfailures preserved,12baseline-devcalls reusedonce,no testbeforetrainingcomplete. No paidservices/install/defaultpromotion/independentexperimentreview.

Strongnext: separatelyfrozen lower-memory training-feasibilityprobe, measureactualoptimizer/activationfootprint andexactstopreadings, balanceearlyeffectiveupdates. Current48testcases nowregressions; newprimarytest needed. [Primary-paper scout](../evaluation/narrow-training-pilot-v1/RESEARCH_SCOUT.md), [LoRAmemorynote](../evaluation/narrow-training-pilot-v1/MEMORY_SCOUT.md). No secondtrainingattempt/backgroundtask.

Optionalexactcalculation/audittoolsremain unchanged. Registryofscopedstations/ancestry remainsproposed. Failedreadinggate/broadqueue/core/schema preserved. Included/freeonly; localcheckpoint/cachepersistence notindependentarchival guarantee.
