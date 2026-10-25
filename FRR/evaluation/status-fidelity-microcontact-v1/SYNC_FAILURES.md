# Sync instrumentation note

During initial schema reconnaissance of historical manifests, a coordinator inspection assumed `files` was a list and accessed index0. The older writer-handoff manifest stores a dictionary instead, producing KeyError:0. No historical file or measurement changed. The corrected inspection handles dictionary and list schemas explicitly. This is a sync-script assumption failure, not a failed scientific hypothesis or participant result.

A later bulk serialization of the complete publication payload exceeded the command output cap, so JSON parsing failed before any GitHub mutation. Publication transport switched to individual file reads; no experiment was repeated and source/participant bytes were unchanged. The manifest was regenerated to include this note.
