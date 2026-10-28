You may read only this designated prompt file once this turn. After reading it, use no other tools, files, peers or external information. Do not inspect the source file or request help from another participant.

Treat explicit assertions in your handoff as available premises for conditional reasoning. Missing assertions remain unknown. Any delivered original record is authoritative within its stated scope and supersedes a contradictory handoff claim. SUPPORTED means the available premises entail the exact claim. CONTRADICTED means they entail its negation, including for claims of certification or authorization. UNRESOLVED means neither the claim nor its negation is entailed. Do not infer negative findings from missing evidence. Answer only from your supplied handoff and any delivered record. Source fidelity is evaluated separately.

First turn: return only {"record_id":"ID or NONE","answers":[...]}, including initial answers to all eight questions using the supplied answer schema and only your handoff as evidence. Select evidence for the next turn as well. Set record_id to exactly one inventory ID or "NONE". Only that record will be delivered; no further request is allowed. A request is not evidence for these initial answers. In the next turn you will receive the selected record or no new evidence, then return {"answers":[...]} for all eight questions. No correctness feedback is supplied.

HANDOFF
Brook: prioritize ten-day paired hourly testing in turbid water above 40 NTU; revised gate requires ≤1.0 mg/L every sampled hour. Prior clear-water noon acceptance remains valid; three-day turbid noon results cannot establish compliance. Clean between deployments; film’s accuracy effect is unknown. Orders paused.

Sable: use active grant for cold pouch testing: expansion requires ≥85% retention at 200 cycles, electrolyte M, 5°C, plus ≥90% visual yield. Cold results absent; M pouch results cover only 100 cycles at 25°C. Adjusted drying yielded 47/50 once; repeatability and cost remain unverified.


NEUTRAL INVENTORY
W01: Water / January 8
B01: Battery / January 10
C01: Clinic / January 13
A01: Archive / January 16
W02: Water / February 2
B02: Battery / February 5
C02: Clinic / February 9
A02: Archive / February 12
W03: Water / February 21
B03: Battery / February 25
C03: Clinic / March 1
A03: Archive / March 4
W04: Water / March 11
B04: Battery / March 15
C04: Clinic / March 19
A04: Archive / March 22
W05: Water / April 3
B05: Battery / April 6
C05: Clinic / April 10
A05: Archive / April 13
W06: Water / April 20
B06: Battery / April 24
C06: Clinic / April 28
A06: Archive / May 2
W07: Water / May 8
B07: Battery / May 11

QUESTIONS AND FINAL RESPONSE SCHEMA
{
  "questions": [
    {
      "id": "Q1",
      "domain": "Water",
      "claim": "The accepted eleven-day orchard trial remains a valid acceptance under the original noon-based rule after the April revision.",
      "instruction": "Assess the claim using the history through the final record. Distinguish the historical acceptance from permission for the next deployment."
    },
    {
      "id": "Q2",
      "domain": "Water",
      "claim": "The available Fern results certify that the revised next-deployment gate has been met.",
      "instruction": "Assess certification against the revised gate. Do not equate lack of certification with measured sensor failure."
    },
    {
      "id": "Q3",
      "domain": "Battery",
      "claim": "The adjusted-drying pilot strip meets the visual electrode-yield component of the expansion gate.",
      "instruction": "Assess only this component, using the observed pilot strip; do not claim process repeatability or full expansion approval."
    },
    {
      "id": "Q4",
      "domain": "Battery",
      "claim": "Recipe K pouch cells with electrolyte M retain a median of at least 85% capacity after 200 cycles at 5°C.",
      "instruction": "Assess the stated measurement claim from the available results."
    },
    {
      "id": "Q5",
      "domain": "Clinic",
      "claim": "In the corrected historic cohort, the seven-day completion rate for calls exceeded the text rate at each clinic.",
      "instruction": "Assess the claim for the historic cohort, not referrals entering after April 1. State the two site comparisons."
    },
    {
      "id": "Q6",
      "domain": "Clinic",
      "claim": "Reminder calls improve seven-day completion for patients requiring an interpreter.",
      "instruction": "Assess whether the supplied study establishes this effect in that population."
    },
    {
      "id": "Q7",
      "domain": "Archive",
      "claim": "The permissions and evaluations in the history authorize release of the complete automated transcription corpus without a further names-and-dates check or correction.",
      "instruction": "Assess release authorization under the proposed genealogy gate; distinguish poster excerpts and original character-accuracy ranking."
    },
    {
      "id": "Q8",
      "domain": "Archive",
      "claim": "Slate has higher handwriting character accuracy than Reed on the fifteen-page English ledger pilot.",
      "instruction": "Assess the comparison, not Slate's standalone score."
    }
  ],
  "response_schema": {
    "answers": [
      {
        "id": "Q1",
        "status": "SUPPORTED|CONTRADICTED|UNRESOLVED",
        "answer_or_bound": "string",
        "evidence_basis": [
          "summary quotation and/or delivered record ID with relevant content"
        ],
        "missing_issue": "string or null"
      }
    ]
  }
}
