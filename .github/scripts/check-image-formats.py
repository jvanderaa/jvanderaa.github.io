"""Check published image extensions against their file signatures before Hugo runs."""
from pathlib import Path
import sys


def matches(path):
    with path.open('rb') as image:
        header = image.read(12)
    suffix = path.suffix.lower()
    if suffix == '.png':
        return header.startswith(b'\x89PNG\r\n\x1a\n')
    if suffix in ('.jpg', '.jpeg'):
        return header.startswith(b'\xff\xd8\xff')
    if suffix == '.gif':
        return header.startswith((b'GIF87a', b'GIF89a'))
    if suffix == '.webp':
        return header[:4] == b'RIFF' and header[8:12] == b'WEBP'
    return True


paths = [path for root in ('content', 'static', 'assets') for path in Path(root).rglob('*')
         if path.is_file() and path.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.webp')]
invalid = [str(path) for path in paths if not matches(path)]
if invalid:
    print('Image extensions do not match their contents:\n' + '\n'.join(invalid), file=sys.stderr)
    raise SystemExit(1)
print(f'Image signatures match filenames for {len(paths)} published assets.')
