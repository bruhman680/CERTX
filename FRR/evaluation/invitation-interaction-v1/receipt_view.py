"""Prospective controlled receipt view; NOT wired into the frozen experiment.

Keep complete raw receipts externally. Omit only wrapper-measured elapsed seconds
from model-facing metadata; never rewrite stdout, stderr or world facts.
"""
import math

def model_receipt(raw):
    if set(raw)!={'stdout','stderr','exit_code','boundary','seconds'}:
        raise ValueError('unknown receipt schema; inspect rather than silently filter')
    if not isinstance(raw['stdout'],str) or not isinstance(raw['stderr'],str) or type(raw['exit_code']) is not int or not (raw['boundary'] is None or isinstance(raw['boundary'],str)):
        raise ValueError('invalid receipt fields')
    if type(raw['seconds']) not in (int,float) or not math.isfinite(raw['seconds']) or raw['seconds']<0:
        raise ValueError('invalid elapsed-time evidence')
    return {k:raw[k] for k in ('stdout','stderr','exit_code','boundary')}
