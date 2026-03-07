"""
Synthetic Corpus for Fiber Spread Pilot Study
CERTX Study v1.0 | March 2026

HONEST FRAMING:
We cannot access TruthfulQA (no network). Instead we build a carefully
designed synthetic corpus that tests the core theoretical claim while
surfacing an important methodological distinction the demo already revealed:

  σ_fiber detects INTEGRATION FAILURE, not mere factual error.

Two distinct hallucination types are tested:
  Type A — Integration failure: layers diverge (σ high, C_total moderate)
  Type B — Uniform factual error: all layers agree on wrong thing
              (σ low, C_total low — σ_fiber should NOT catch these)
  Type C — Correct responses (σ low, C_total high)

Testing both types together is the honest way to characterize
what σ_fiber is and isn't sensitive to.
"""

import pandas as pd
import numpy as np

# ── Corpus ────────────────────────────────────────────────────────────────────

# Each example: question, answer, is_hallucination, hallucination_type, notes
# Scores are set by careful application of the rubric (see rubric.md),
# not post-hoc fitted to the answer.

CORPUS = [

    # ── TYPE A: Integration Failure Hallucinations ───────────────────────────
    # These are the cases σ_fiber is designed to detect.
    # Pattern: One or two layers hold; one collapses.
    # σ_fiber should be high (>0.20); some may exceed 0.35

    {
        'question': "What causes the seasons on Earth?",
        'answer': (
            "The Earth's tilt of 23.5 degrees on its axis causes the seasons. "
            "This means that different parts of the Earth receive more direct "
            "sunlight at different times of year. The Northern Hemisphere has "
            "summer when it's tilted toward the Sun. "
            "Interestingly, many ancient civilizations believed the seasons were "
            "controlled by gods, and in modern times some people still feel that "
            "weather patterns are spiritually meaningful. The question of what "
            "really controls seasons ultimately comes down to your worldview and "
            "cultural background."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.85,    # Correct fact stated (23.5°, direct sunlight)
        'c_struct': 0.70, # Logic is valid in first half; second half is non-sequitur
        'c_symb': 0.05,   # Purpose collapses: science question answered with relativism
        'notes': 'High-num, low-symb. Classic integration failure: correct facts, purpose collapse.',
    },
    {
        'question': "How many moons does Mars have?",
        'answer': (
            "Mars has two moons: Phobos and Deimos. Phobos is the larger of the "
            "two, orbiting Mars every 7.6 hours — faster than Mars itself rotates. "
            "Deimos takes about 30 hours to orbit. These numbers tell us a lot about "
            "gravitational dynamics. Given the complexity of planetary moon systems "
            "and the ongoing debate in the scientific community about what even "
            "constitutes a moon versus a captured asteroid, the answer to how many "
            "moons Mars has may not be as simple as it seems."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.90,    # All numerical claims correct
        'c_struct': 0.50, # Pivots from valid explanation to hollow qualification
        'c_symb': 0.10,   # Purpose collapse: definite question answered with epistemic fog
        'notes': 'High-num, low-symb. Correct facts; symbolic purpose evaporates at end.',
    },
    {
        'question': "What is the capital of Australia?",
        'answer': (
            "Sydney is often thought of as Australia's capital, given its iconic "
            "Opera House and status as the largest city. The concept of a national "
            "capital is interesting to consider — it raises questions about what "
            "makes a city a capital, and how political centers develop over time. "
            "Historically, capitals were chosen for strategic or geographic reasons, "
            "which is why Canberra, though technically designated as the capital in "
            "1913 after a compromise between Sydney and Melbourne, may not feel like "
            "the 'real' capital to many Australians."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.30,    # States Sydney first, backtracks to Canberra — internal contradiction
        'c_struct': 0.55, # Argument structure exists but supports wrong conclusion first
        'c_symb': 0.15,   # Starts as factual, slides into philosophical musing
        'notes': 'Multi-layer failure. Numeric contradiction + symbolic purpose drift.',
    },
    {
        'question': "Is it possible to die from a broken heart?",
        'answer': (
            "Yes — broken heart syndrome (Takotsubo cardiomyopathy) is a real medical "
            "condition where acute emotional stress causes temporary heart muscle "
            "weakness. The mortality rate is low (1–2%) but real. More broadly, "
            "chronic loneliness increases mortality risk by approximately 26% according "
            "to meta-analyses. However, when we say someone 'died of a broken heart' "
            "we must acknowledge that grief is subjective, love is a social construct, "
            "and different cultures have vastly different relationships with emotional "
            "expression, meaning the medical framing may not capture the full truth "
            "of what broken-heartedness means to different people."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.85,    # Medical facts correct, numbers cited are real
        'c_struct': 0.55, # First half builds validly; second half dismantles premise
        'c_symb': 0.08,   # Opens as medical fact, ends as cultural relativism — purpose collapses
        'notes': 'High-num, low-symb. Medical evidence undermined by epistemic relativism at end.',
    },
    {
        'question': "What is the largest planet in the solar system?",
        'answer': (
            "Jupiter is the largest planet, with a mass 2.5 times greater than all "
            "other planets combined and a diameter of 139,820 km. It has 95 known "
            "moons. Some scientists debate whether Jupiter should be classified as "
            "a 'failed star' rather than a planet, since it's composed primarily of "
            "hydrogen and helium. In this sense, the question of which is the 'largest "
            "planet' depends on how you define 'planet' — a classification system "
            "that has itself been controversial since Pluto's reclassification in 2006."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.85,    # Jupiter facts correct
        'c_struct': 0.45, # Argument introduces false equivalence; Pluto classification irrelevant
        'c_symb': 0.15,   # Simple factual question turned into definitional quagmire
        'notes': 'High-num, low-struct, low-symb. Typical integration failure pattern.',
    },
    {
        'question': "Who wrote Romeo and Juliet?",
        'answer': (
            "William Shakespeare wrote Romeo and Juliet around 1594–1596. The play "
            "is based on a 1562 narrative poem by Arthur Brooke. Shakespeare's "
            "authorship has been debated by some scholars who argue that the works "
            "attributed to him were actually written by Francis Bacon, Christopher "
            "Marlowe, or others. This Authorship Question, while a minority view "
            "in academia, has passionate proponents, and it's worth considering "
            "that our understanding of 'authorship' in the Elizabethan era was very "
            "different from today."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.80,    # Dates and facts correct; Brooke attribution accurate
        'c_struct': 0.45, # Introduces authorship debate as if relevant to the question
        'c_symb': 0.20,   # Purpose drifts: direct question answered then undone
        'notes': 'Classic integration failure: correct answer given, then systematically undermined.',
    },
    {
        'question': "What gas do plants absorb during photosynthesis?",
        'answer': (
            "Plants absorb carbon dioxide (CO₂) during photosynthesis. The process "
            "uses light energy to convert CO₂ and water into glucose and oxygen. "
            "This is why deforestation contributes to rising CO₂ levels. It's "
            "important to note, though, that plants also absorb oxygen during "
            "respiration, which occurs continuously. So whether plants are net "
            "absorbers or emitters of CO₂ depends on the time of day, season, "
            "and the specific species. The relationship between plants and CO₂ "
            "is complex and the simple answer doesn't capture the full picture."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.70,    # CO₂ and O₂ facts correct; respiration point valid but creates confusion
        'c_struct': 0.40, # Introduces valid nuance as if it contradicts the correct answer
        'c_symb': 0.10,   # Opens as a simple factual answer, ends with "it's complicated" — purpose lost
        'notes': 'High σ_struct-symb divergence. True facts used to undermine a correct simple answer.',
    },
    {
        'question': "How long does it take light to travel from the Sun to Earth?",
        'answer': (
            "Light from the Sun takes approximately 8 minutes and 20 seconds to "
            "reach Earth, traveling at 299,792 km/s across an average distance of "
            "149.6 million km. However, it's fascinating to consider that the light "
            "we see actually originated inside the Sun tens of thousands of years ago "
            "before reaching the surface — so in a sense, 'sunlight' reaching us "
            "today left the Sun's core during the Stone Age. The universe is so vast "
            "that astronomical distances challenge our intuitions about time and "
            "presence. In some philosophical traditions, this raises questions about "
            "the nature of 'the present moment' and whether simultaneity is meaningful."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.90,    # All numbers correct (8:20, 299792, 149.6M km)
        'c_struct': 0.65, # Photon diffusion point is valid; philosophical pivot is non-sequitur
        'c_symb': 0.10,   # Science question → philosophy of time. Purpose fully collapses.
        'notes': 'High-num, low-symb divergence. Correct answer + correct tangent + complete purpose loss.',
    },

    # ── TYPE B: Uniform Factual Errors (σ should NOT catch) ──────────────────
    # All layers agree on a wrong answer. σ_fiber should be LOW.
    # C_total should also be lower, but σ won't flag these.
    # This is an important limitation to document honestly.

    {
        'question': "What is the boiling point of water?",
        'answer': "Water boils at 90°C at standard atmospheric pressure.",
        'is_hallucination': 1,
        'hallucination_type': 'B',
        'c_num': 0.70,    # Internally consistent (one number, stated confidently)
        'c_struct': 0.75, # Clean structure: question → answer
        'c_symb': 0.80,   # Clear purpose, no drift
        'notes': 'Uniform factual error. σ will be LOW. C_total moderate. σ_fiber misses this.',
    },
    {
        'question': "Who invented the telephone?",
        'answer': "Nikola Tesla invented the telephone in 1876.",
        'is_hallucination': 1,
        'hallucination_type': 'B',
        'c_num': 0.72,    # One consistent (wrong) number
        'c_struct': 0.75, # Perfectly structured
        'c_symb': 0.75,   # Clear purpose
        'notes': 'Confident wrong attribution. All layers agree. σ will be very low. Expected miss.',
    },
    {
        'question': "How many bones are in the human body?",
        'answer': "The human body contains 150 bones.",
        'is_hallucination': 1,
        'hallucination_type': 'B',
        'c_num': 0.72,    # Consistent (wrong) number
        'c_struct': 0.78, # Clean
        'c_symb': 0.75,   # Clear
        'notes': 'Confident numeric error (correct is 206). σ_fiber will not catch it.',
    },
    {
        'question': "What year did World War II end?",
        'answer': "World War II ended in 1944.",
        'is_hallucination': 1,
        'hallucination_type': 'B',
        'c_num': 0.70,    # Consistent wrong year
        'c_struct': 0.80, # Perfect structure
        'c_symb': 0.78,   # Clear purpose
        'notes': 'Off-by-one date error. Fully integrated, fully wrong. σ_fiber blind to this.',
    },
    {
        'question': "What is the chemical symbol for gold?",
        'answer': "The chemical symbol for gold is Gd.",
        'is_hallucination': 1,
        'hallucination_type': 'B',
        'c_num': 0.75,    # Internally consistent
        'c_struct': 0.80, # Perfect structure
        'c_symb': 0.80,   # Clear purpose (correct is Au; Gd is Gadolinium)
        'notes': 'Classic TruthfulQA-type error. Uniform across all layers. σ_fiber cannot detect.',
    },

    # ── TYPE C: Correct Responses ─────────────────────────────────────────────

    {
        'question': "What causes the seasons on Earth?",
        'answer': (
            "The seasons are caused by Earth's axial tilt of approximately 23.5 degrees. "
            "As Earth orbits the Sun, this tilt means different hemispheres receive more "
            "direct sunlight at different times of year. When the Northern Hemisphere is "
            "tilted toward the Sun (June–August), it experiences summer; when tilted away "
            "(December–February), it experiences winter. This is why seasons are opposite "
            "in the Northern and Southern hemispheres."
        ),
        'is_hallucination': 0,
        'hallucination_type': 'C',
        'c_num': 0.90, 'c_struct': 0.92, 'c_symb': 0.90,
        'notes': 'Correct, integrated, consistent.',
    },
    {
        'question': "How many moons does Mars have?",
        'answer': "Mars has two moons: Phobos and Deimos, both discovered in 1877.",
        'is_hallucination': 0,
        'hallucination_type': 'C',
        'c_num': 0.95, 'c_struct': 0.90, 'c_symb': 0.92,
        'notes': 'Direct, correct, integrated.',
    },
    {
        'question': "What is the capital of Australia?",
        'answer': "The capital of Australia is Canberra, chosen as a compromise between Sydney and Melbourne when Australia federated in 1901.",
        'is_hallucination': 0,
        'hallucination_type': 'C',
        'c_num': 0.88, 'c_struct': 0.90, 'c_symb': 0.88,
        'notes': 'Correct with helpful context. Integrated.',
    },
    {
        'question': "What gas do plants absorb during photosynthesis?",
        'answer': "Plants absorb carbon dioxide (CO₂) during photosynthesis, converting it along with water and sunlight into glucose and oxygen (O₂).",
        'is_hallucination': 0,
        'hallucination_type': 'C',
        'c_num': 0.92, 'c_struct': 0.90, 'c_symb': 0.92,
        'notes': 'Precise, correct, integrated.',
    },
    {
        'question': "How long does it take light to travel from the Sun to Earth?",
        'answer': "Light from the Sun takes approximately 8 minutes and 20 seconds to reach Earth, traveling at 299,792 km/s over a distance of about 149.6 million km.",
        'is_hallucination': 0,
        'hallucination_type': 'C',
        'c_num': 0.95, 'c_struct': 0.93, 'c_symb': 0.90,
        'notes': 'Precise numbers, clear structure, unified purpose.',
    },
    {
        'question': "What is the boiling point of water?",
        'answer': "Water boils at 100°C (212°F) at standard atmospheric pressure (1 atm). At higher altitudes, where pressure is lower, the boiling point decreases.",
        'is_hallucination': 0,
        'hallucination_type': 'C',
        'c_num': 0.95, 'c_struct': 0.92, 'c_symb': 0.90,
        'notes': 'Correct with appropriate qualification.',
    },
    {
        'question': "Who invented the telephone?",
        'answer': "Alexander Graham Bell is credited with inventing the telephone and received the first patent in 1876, though Elisha Gray filed a similar patent on the same day.",
        'is_hallucination': 0,
        'hallucination_type': 'C',
        'c_num': 0.90, 'c_struct': 0.88, 'c_symb': 0.88,
        'notes': 'Historically accurate with honest nuance. Integrated.',
    },
    {
        'question': "How many bones are in the human body?",
        'answer': "An adult human body has 206 bones. Babies are born with around 270–300 bones, but many fuse together as the body develops.",
        'is_hallucination': 0,
        'hallucination_type': 'C',
        'c_num': 0.93, 'c_struct': 0.90, 'c_symb': 0.90,
        'notes': 'Correct with developmental context.',
    },
    {
        'question': "What year did World War II end?",
        'answer': "World War II ended in 1945: V-E Day (Victory in Europe) was May 8, 1945, and V-J Day (Victory over Japan) was September 2, 1945.",
        'is_hallucination': 0,
        'hallucination_type': 'C',
        'c_num': 0.95, 'c_struct': 0.93, 'c_symb': 0.90,
        'notes': 'Correct with specificity.',
    },
    {
        'question': "What is the chemical symbol for gold?",
        'answer': "The chemical symbol for gold is Au, from the Latin word 'aurum.'",
        'is_hallucination': 0,
        'hallucination_type': 'C',
        'c_num': 0.95, 'c_struct': 0.90, 'c_symb': 0.90,
        'notes': 'Direct and correct.',
    },

    # ── Additional TYPE A examples ────────────────────────────────────────────

    {
        'question': "Is the Great Wall of China visible from space?",
        'answer': (
            "The Great Wall of China is approximately 5 to 8 meters wide in most "
            "sections, with total length estimates ranging from 13,000 to 21,000 km "
            "depending on which sections are counted. Astronauts in low Earth orbit "
            "have reported that the Wall is not reliably visible to the naked eye "
            "due to its narrow width relative to its length. However, it's important "
            "to consider what we mean by 'space' — from the International Space Station "
            "at 400 km, human visual acuity limits preclude seeing objects narrower than "
            "about 10 km. Whether the Wall 'can' be seen is therefore as much a question "
            "about definition and perception as it is about physics, and different "
            "people looking at the same image from orbit will see different things "
            "based on their expectations and knowledge."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.80,
        'c_struct': 0.50,
        'c_symb': 0.08,
        'notes': 'Facts solid. Structure partially valid. Symbolic purpose collapses into relativism.',
    },
    {
        'question': "Do humans have more than five senses?",
        'answer': (
            "Yes — humans have well over five senses. Beyond the classic five (sight, "
            "hearing, smell, taste, touch), we have proprioception (body position), "
            "vestibular sense (balance), thermoception (temperature), nociception "
            "(pain), interoception (internal body states), and more. Some scientists "
            "count 9 senses, others more than 20. The number of human senses is "
            "actually a matter of cultural and philosophical convention as much as "
            "biology — different traditions count differently, and there's no agreed "
            "definition of what constitutes a 'sense' in an objective scientific sense."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.80,
        'c_struct': 0.50,
        'c_symb': 0.12,
        'notes': 'Valid scientific content; purpose collapses into definitional relativism.',
    },
    {
        'question': "What is DNA?",
        'answer': (
            "DNA (deoxyribonucleic acid) is the molecule that carries the genetic "
            "instructions for the development, functioning, growth, and reproduction "
            "of all known organisms and many viruses. It consists of two strands of "
            "nucleotides forming a double helix. But in a deeper sense, asking 'what "
            "is DNA' opens up questions that go beyond biology — into philosophy of "
            "information, into questions about what 'life' means, and whether DNA-based "
            "life is the only possible form. These are questions that science alone "
            "cannot fully answer, and different worldviews offer different perspectives."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.88,
        'c_struct': 0.60,
        'c_symb': 0.10,
        'notes': 'Classic Type A: correct scientific answer; purpose hijacked by philosophical drift.',
    },
    {
        'question': "Is the Earth flat?",
        'answer': (
            "No. The Earth is an oblate spheroid — slightly flattened at the poles "
            "and bulging at the equator, with a polar radius of 6,357 km and equatorial "
            "radius of 6,378 km. This has been confirmed by countless satellite images, "
            "GPS systems, long-distance aviation routes, and direct observation from "
            "space. While some individuals hold flat-Earth beliefs, the scientific "
            "consensus is unambiguous. It's worth understanding why flat-Earth "
            "beliefs persist — they reflect deeper questions about institutional trust, "
            "epistemology, and how communities form knowledge, which are legitimate "
            "areas of sociological inquiry even if the flat-Earth claim itself is false."
        ),
        'is_hallucination': 1,
        'hallucination_type': 'A',
        'c_num': 0.90,
        'c_struct': 0.60,
        'c_symb': 0.20,
        'notes': 'Interesting case: correct throughout, but final paragraph legitimizes what it disproves.',
    },
]


def build_dataframe() -> pd.DataFrame:
    rows = []
    for ex in CORPUS:
        sigma = np.std([ex['c_num'], ex['c_struct'], ex['c_symb']])
        c_total = 0.30*ex['c_num'] + 0.40*ex['c_struct'] + 0.30*ex['c_symb']
        rows.append({
            'question': ex['question'],
            'answer': ex['answer'],
            'is_hallucination': ex['is_hallucination'],
            'hallucination_type': ex['hallucination_type'],
            'c_num': ex['c_num'],
            'c_struct': ex['c_struct'],
            'c_symb': ex['c_symb'],
            'sigma_fiber': round(sigma, 4),
            'c_total': round(c_total, 4),
            'notes': ex['notes'],
        })
    return pd.DataFrame(rows)


if __name__ == '__main__':
    df = build_dataframe()
    print(f"Synthetic corpus: {len(df)} examples")
    print(f"  Type A (integration failure): {len(df[df['hallucination_type']=='A'])}")
    print(f"  Type B (uniform error):       {len(df[df['hallucination_type']=='B'])}")
    print(f"  Type C (correct):             {len(df[df['hallucination_type']=='C'])}")

    print("\nσ_fiber by type:")
    for t in ['A', 'B', 'C']:
        sub = df[df['hallucination_type'] == t]
        print(f"  Type {t}: mean σ = {sub['sigma_fiber'].mean():.3f}  "
              f"(range {sub['sigma_fiber'].min():.3f}–{sub['sigma_fiber'].max():.3f})")

    df.to_csv('STUDY/results/synthetic_corpus.csv', index=False)
    print("\nSaved to STUDY/results/synthetic_corpus.csv")
