"""Verify source bytes against the checksum from the same repository checkout."""
import hashlib
from pathlib import Path
import sys


def main():
    root = Path(__file__).resolve().parent.parent
    checksum = root / 'SOURCE.sha256'
    source = root / 'OBOS.pine'
    fields = checksum.read_text(encoding='ascii').split()
    if len(fields) != 2 or fields[1] != 'OBOS.pine':
        print('FAIL: SOURCE.sha256 must contain one hash for OBOS.pine.', file=sys.stderr)
        return 1
    expected = fields[0].lower()
    if len(expected) != 64 or any(char not in '0123456789abcdef' for char in expected):
        print('FAIL: invalid SHA-256 value.', file=sys.stderr)
        return 1
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    if actual != expected:
        print(f'FAIL: expected {expected}, found {actual}', file=sys.stderr)
        return 1
    print(f'OK: OBOS.pine SHA-256 {actual}')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, UnicodeError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        sys.exit(1)
