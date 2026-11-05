# Explicit runtime-interruption recovery

The managed workspace session changed while the50-entryblock was running. The old execution session was unavailable, and both lock-holder processes were defunct zombies. The last completed logical check was490. Entries490and491had committed; zero-based492had a frozen plan and a before_generate resource sample but no surviving output/committed event.

The first liveness preflight stopped because the PIDs still existed. Inspection established that both were defunct; that evidence, the lock bytes, original plan, resource stream and projections were archived before stale markers were removed. No model inference was retried during that preflight.

Session0090was finalized from durable evidence with two committed outputs, an explicit interrupted step and `weights_unchanged:null`: the terminated process's post-session in-memory digest is unavailable. Training updates remain0under the frozen inference-only code. Complete old-history replay then passed at492, verifier0094.

The recovery runner was pinned before inference. It reloaded the same model/adapter and checked the parameter digests. It reconstructed492's prompt and tokenIDs, required exact equality with the original plan/hash/seed, preserved that plan unchanged, and recorded a separate recovery attempt before generation. The prior attempt's output remains unknown, not a failed or successful response selected away. Steps493and494then used newly saved plans and the unchanged policy. No prior committed entry or world state was rolled back.

The recovery session0091checked weights before/after and preserved the old plan/resource hashes. Full replay passed at495, verifier0095. The original block observer saved its495checkpoint; the normal driver continued the finalfiveentries in a new log. The original BLOCK_LOG and WINDOW_495_RUN.log remain unchanged evidence of where the first process stopped.

The final block therefore has50committed outputs,51known generation starts,11session records, ten logicalfive-entrychecks plus an extra check at492. One in-memory post-session digest is unavailable; persisted model pins and all completed-session digests were checked. Recorded generation time excludes the unknown lost attempt. This is a host interruption and explicit recovery, not an inferred model behavior, phase change or rule-learning result.
