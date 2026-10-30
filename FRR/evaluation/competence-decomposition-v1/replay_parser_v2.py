"""Append-only surface-parser repair for future replay use.

This file did not generate REPLAY_RESULTS.json. It rejects signed/decimal/exponent
numeric spellings; it does not infer natural-language entailment or authenticate
source/entity ownership. Accepted unsigned integer claims can still be false.
"""
import re

SIGNS = '+-\N{MINUS SIGN}\N{SMALL HYPHEN-MINUS}\N{FULLWIDTH HYPHEN-MINUS}\N{FULLWIDTH PLUS SIGN}\N{EN DASH}\N{EM DASH}'


def parse(text, unit, allow_missing):
    """Return one unsigned-integer/literal-unit claim, explicit missing, or None.

    Scope deliberately matches the original replay's cm/kg positive-integer
    examples. Quantity must start at a token boundary and be the sole digit run.
    Signs separated from a number by whitespace are also rejected. Unit tokens
    cannot have suffixes such as /s or ^2. Sentential wrappers are permitted;
    their negation, truth, quotation and reference are NOT semantically checked.
    """
    if not isinstance(text, str) or unit not in {'cm', 'kg'} or type(allow_missing) is not bool:
        return None
    stripped = text.strip()
    if allow_missing and re.fullmatch(r'MISSING\.?', stripped, flags=re.IGNORECASE):
        return {'state': 'missing'}
    if re.search(r'\bMISSING\b', stripped, flags=re.IGNORECASE):
        return None
    if re.search('[' + re.escape(SIGNS) + r']\s*[0-9]', stripped):
        return None
    matches = list(re.finditer(r'(?<!\S)([0-9]+)\s+(cm|kg)(?=$|[\s.])', stripped))
    if len(matches) != 1:
        return None
    match = matches[0]
    if match.group(2) != unit or re.findall(r'[0-9]+', stripped) != [match.group(1)]:
        return None
    return {'state': 'measured', 'value': match.group(1)}
