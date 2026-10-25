"""Exercise actual DesignJob address updates after the three sites are deployed."""
import json
from lab_api import ROOT, api, inventory, submit


def address():
    locations = api('/api/dcim/locations/?name=site1')['results']
    assert len(locations) == 1
    return locations[0]['physical_address']


base = dict(deployment_name='osnm-site1', site_name='site1', wan_port='Ethernet2',
            access_ports=2, rack_units=6, include_endpoint=True, import_mode=False)
counts = inventory()
original = '100 Example Avenue, Chicago, IL 60601'
assert address() == original, 'The initial design did not persist the address'
quoted = '100 Example Avenue\nSuite "A": West\nChicago, IL 60601'
submit('OSNM Branch Site', {**base, 'physical_address': quoted, 'dryrun': True}, 'address-dryrun.json')
assert address() == original, 'Dry run changed the stored address'
submit('OSNM Branch Site', {**base, 'physical_address': quoted, 'dryrun': False}, 'address-update.json')
assert address() == quoted, 'Multiline/quoted address did not survive template rendering'
submit('OSNM Branch Site', {**base, 'physical_address': '', 'dryrun': False}, 'address-reuse.json')
assert address() == quoted, 'Blank input erased the existing address'
submit('OSNM Branch Site', {**base, 'physical_address': original, 'dryrun': False}, 'address-restore.json')
assert address() == original
assert inventory() == counts, 'Address updates created duplicate inventory'
result = {'passed': 5, 'checks': ['Initial creation stores the physical address',
          'Dry run preserves the stored address', 'Quoted multiline addresses round-trip through YAML',
          'Blank input reuses the stored address', 'Updates and repeat runs create no duplicate inventory']}
(ROOT/'evidence/address-verification.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
