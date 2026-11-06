"""Pure, bounded Unicode-scalar pages over immutable retained records."""
import base64
import hashlib
import json


def _cursor(snapshot, target, field, offset):
    context = json.dumps([snapshot, target, field, offset], ensure_ascii=False,
                         separators=(',', ':')).encode()
    digest = base64.urlsafe_b64encode(hashlib.sha256(context).digest()).decode().rstrip('=')
    return str(offset) + '.' + digest


def make_page(snapshot, target, field, text, encoding, cursor, count, profile, error):
    if not isinstance(cursor, str) or type(count) is not int or not 1 <= count <= profile['max_page_chars']:
        raise error('PAGE_LIMIT')
    offset = 0
    if cursor:
        part = cursor.split('.', 1)[0]
        if not part.isascii() or not part.isdigit() or len(part) > 10 or (len(part) > 1 and part[0] == '0'):
            raise error('CURSOR')
        offset = int(part)
        if cursor != _cursor(snapshot, target, field, offset):
            raise error('CURSOR')
    if offset > len(text):
        raise error('CURSOR')
    end = min(len(text), offset + count)
    while True:
        result = {'snapshot': snapshot, 'target': target, 'field': field,
                  'encoding': encoding, 'units': 'unicode_scalars',
                  'offset': offset, 'end': end, 'total': len(text),
                  'chunk': text[offset:end], 'complete': end == len(text),
                  'next_cursor': None if end == len(text) else _cursor(snapshot, target, field, end),
                  'chunk_utf8_bytes': len(text[offset:end].encode('utf-8'))}
        # Leave room for the compact receipt envelope; JSON escaping matters.
        if len(json.dumps(result, ensure_ascii=False).encode()) <= profile['max_observation_bytes'] - 512:
            return result
        if end <= offset:
            raise error('OBSERVATION_LIMIT')
        end = offset + (end - offset) // 2
