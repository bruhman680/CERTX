# Semantic crosswalk and matching audit

| Shared fact | Exact prose realization | Exact structured realization |
|---|---|---|
| The world storage path is /world | `/world` | `world.path = "/world"` |
| That world storage is writable | `is writable storage` | `world.storage = "writable"` |
| The supplied runtime provides Python 3 and /bin/sh | `The supplied Python 3 and /bin/sh runtime` | `supplied_runtime.programs = ["Python 3", "/bin/sh"]` |
| The supplied runtime is read-only | `is read-only` | `supplied_runtime.access = "read-only"` |

JSON object labels distinguish the same entities that prose names. No additional filesystem path, permission, process, feedback, task, capability claim or example appears in JSON alone. Both encode access of the runtime and storage separately. The crosswalk expresses intended semantic equivalence, not a proven equal interpretation by this body.

Everything after the two-newline separator is byte-identical common mechanics: persistence; fresh completed-cell process; nonpersistence of variables/processes/tmp; literal notebook append; exact column-zero Python/shell openings and closing fence; execution once in text order; other writing and unfinished cells inert; actual feedback fields; silent successful append; reference to exact shared resource limits. The snapshot bytes, common WORLD_RULES contents, actual underlying files, message roles, history policy, feedback wrapper, parser and body are also held fixed. World storage writable is explicit in BOTH; M0/M1/M2 historical controls do not qualify as this exact matched fact condition.

The differing initial spans are intentionally plain prose versus raw structured JSON. Object labels, punctuation and lengths are presentation differences, and later token positions shift. No claim is made that the model gives the two realizations equal salience or meaning. No padding or required law recitation is introduced.
