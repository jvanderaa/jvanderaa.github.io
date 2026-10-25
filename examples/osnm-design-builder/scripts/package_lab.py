"""Rebuild the blog downloads from an explicit list of credential-free sources."""
from pathlib import Path
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
BUNDLE = REPO / 'content/posts/2026/RepeatableNetworkDesignWithNautobot'


def package():
    files = [Path(name) for name in (
        'README.md', 'Dockerfile', 'compose.yaml', '.gitignore', '.dockerignore',
        'evidence/osnm-topology.json', 'evidence/verification.json',
        'evidence/address-verification.json',
    )]
    for folder, pattern in [('config', '*.py'), ('jobs', '*.py'), ('jobs', '*.j2'), ('scripts', '*.py')]:
        files.extend(path.relative_to(ROOT) for path in (ROOT / folder).rglob(pattern))
    archive = BUNDLE / 'osnm-design-builder-lab.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
        for relative in sorted(set(files)):
            info = zipfile.ZipInfo(str(Path('osnm-design-builder') / relative), (2026, 10, 25, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            output.writestr(info, (ROOT / relative).read_bytes())
    shutil.copyfile(ROOT / 'jobs/osnm_site_designs/templates/site.yaml.j2', BUNDLE / 'site.yaml.j2')
    print(f'Packaged {len(set(files))} source files into {archive.name}; refreshed site.yaml.j2.')


if __name__ == '__main__':
    package()
