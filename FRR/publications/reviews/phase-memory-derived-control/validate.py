"""Validate the copy-ready publication; do not overwrite historical RM-C1 results."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
POST = HERE.parents[1] / 'REDDIT_PHASE_MEMORY_DERIVED_CONTROL.md'
text = POST.read_text()
blocks = re.findall(r'^```python\n(.*?)^```', text, flags=re.M | re.S)
assert len(blocks) == 1
with tempfile.TemporaryDirectory() as tmp:
    script = Path(tmp) / 'example.py'
    script.write_text(blocks[0])
    run = subprocess.run([sys.executable, '-I', str(script)], capture_output=True, text=True)

def scalar_score(b):
    # Query=1, rational real candidate b. Independent exact arithmetic.
    return F(1, 2) * (1 + b)**2 / (1 + b*b) * (2*abs(b)/(1 + b*b))

checks = {
    'under_40000_codepoints': len(text) < 40000,
    'under_40000_utf16_units': len(text.encode('utf-16-le')) // 2 < 40000,
    'under_40000_utf8_bytes': len(text.encode()) < 40000,
    'near_limit_without_padding': 39500 <= len(text) < 39900,
    'ascii_only': text.isascii(),
    '33_numbered_sections': len(re.findall(r'^## \d+\.', text, flags=re.M)) == 33,
    'all_fences_paired': len(re.findall(r'^```', text, flags=re.M)) % 2 == 0,
    'snippet_executes': run.returncode == 0,
    'aligned_scalar': scalar_score(F(2)) == F(18, 25),
    'opposite_scalar': scalar_score(F(-2)) == F(2, 25),
    'ranking_reversal_exact': scalar_score(F(10)) == F(1210, 10201) < F(1, 2),
}
receipt = {
    'scope': 'publication length, included Python illustration and new exact worked examples; not a rerun or replacement of historical experiment',
    'body_file': POST.name,
    'sha256': hashlib.sha256(POST.read_bytes()).hexdigest(),
    'characters_including_markdown_urls_and_newlines': len(text),
    'utf16_units': len(text.encode('utf-16-le')) // 2,
    'utf8_bytes': len(text.encode()),
    'words_whitespace': len(text.split()),
    'headroom_to_40000': 40000 - len(text),
    'title': text.splitlines()[0].removeprefix('# '),
    'snippet_stdout': run.stdout,
    'snippet_stderr': run.stderr,
    'checks': checks,
}
(HERE / 'CHECKS.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
assert all(checks.values())
