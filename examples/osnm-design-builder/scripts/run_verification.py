"""Verify the branch designs after seeding the catalog and deploying the fabric."""
from pathlib import Path
import subprocess
import sys

scripts = Path(__file__).resolve().parent
steps = [
    ['lab_api.py', 'fabric', '--dry-run'],
    ['lab_api.py', 'site1', '--dry-run'],
    ['lab_api.py', 'site1'],
    ['lab_api.py', 'site2'],
    ['lab_api.py', 'site1-repeat'],
    ['verify_topology.py'],
    ['verify_address_api.py'],
]
for name, *args in steps:
    subprocess.run([sys.executable, str(scripts/name), *args], check=True)
