# Follow-up before outcomes: recurrent local sharing

The one-time transfer may fail because local donor selection does not track subsequent environmental changes. Test whether repeating the *same* local copy intervention every 300 deployment ticks changes that conclusion.

Frozen-policy controls remain unchanged in their own weights, while social arms are socially modified (policy gradients are disabled); same trained worlds and initial-shift protocol as `SOCIAL2_PLAN.md`. Use 12 fresh seeds 10600–10611 in stable .06 and mild shift .055, 1500 training ticks and 3000 deterministic deployment ticks. Compare none, local best-energy neighbor, random neighbor, shuffled-global and local neighbor mean. Importantly, selecting donor by energy is a hand-coded social rule, not evidence the cells learned when to communicate. Track number of social copy events and endpoint dispersion. Recurrent transfer can erase diversity; no free advantage presumed.
