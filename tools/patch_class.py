# -*- coding: utf-8 -*-
"""Patch UTF8 string constants inside JVM class files (constant-pool rewrite)."""
import struct

def parse_pool(data):
    assert data[:4] == b'\xca\xfe\xba\xbe', 'not a class file'
    minor, major = struct.unpack('>HH', data[4:8])
    n = struct.unpack('>H', data[8:10])[0]
    i = 10
    entries = []  # (slot, tag, offset, length) for UTF8
    idx = 1
    while idx < n:
        tag = data[i]
        i += 1
        if tag == 1:
            ln = struct.unpack('>H', data[i:i+2])[0]
            entries.append((idx, tag, i + 2, ln))
            i += 2 + ln
            idx += 1
        elif tag in (7, 8, 16, 19, 20):
            i += 2; idx += 1
        elif tag == 15:
            i += 3; idx += 1
        elif tag in (3, 4, 9, 10, 11, 12, 17, 18):
            i += 4; idx += 1
        elif tag in (5, 6):
            i += 8; idx += 2
        else:
            raise ValueError('bad tag %d at offset %d' % (tag, i - 1))
    return entries, i, n

def patch_class(data, mapping):
    """mapping: dict old_str -> new_str (exact full-string match on constant)."""
    entries, body_off, n = parse_pool(data)
    changes = []
    for slot, tag, off, ln in entries:
        raw = data[off:off + ln]
        try:
            s = raw.decode('utf-8')
        except UnicodeDecodeError:
            continue
        if s in mapping:
            new = mapping[s].encode('utf-8')
            if new == raw:
                continue
            changes.append((off, ln, new, s))
    if not changes:
        return data, []
    out = bytearray(data)
    # apply from the end to keep offsets valid
    for off, ln, new, s in sorted(changes, reverse=True):
        out[off:off + ln] = new
        changes_len = len(new) - ln
        if changes_len:
            # patch recorded length field (2 bytes at off-2)
            struct.pack_into('>H', out, off - 2, len(new))
    return bytes(out), [(c[3], c[2].decode('utf-8')) for c in changes]

if __name__ == '__main__':
    import sys, os
    src = sys.argv[1]
    dst = sys.argv[2]
    pairs = sys.argv[3:]
    assert len(pairs) % 2 == 0
    mapping = dict(zip(pairs[0::2], pairs[1::2]))
    data = open(src, 'rb').read()
    out, log = patch_class(data, mapping)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'wb').write(out)
    for a, b in log:
        print('patched:', repr(a), '->', repr(b))
    print('written', dst, len(out), 'bytes')
