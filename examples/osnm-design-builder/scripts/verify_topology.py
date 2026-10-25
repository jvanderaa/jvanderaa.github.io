"""Verify the real lab inventory against OSNM's expected nodes and all 13 cables."""
import json
from pathlib import Path
from lab_api import ROOT, api, inventory

fixture=json.loads((ROOT/'evidence/osnm-topology.json').read_text())
devices=api('/api/dcim/devices/?limit=100')['results']
interfaces=api('/api/dcim/interfaces/?limit=100')['results']
cables=api('/api/dcim/cables/?limit=100')['results']
device_names={r['id']:r['name'] for r in devices}
ports={r['id']:device_names[r['device']['id']]+':'+r['name'] for r in interfaces}
actual={frozenset((ports[r['termination_a_id']],ports[r['termination_b_id']])) for r in cables}
expected={frozenset(r) for r in fixture['links']}
assert set(device_names.values())==set(fixture['nodes']), 'Device names differ from the OSNM fixture.'
assert actual==expected, f'Cable topology mismatch. Missing={expected-actual}; extra={actual-expected}'
counts=inventory()
assert counts==dict(locations=3,racks=3,devices=13,interfaces=26,cables=13,deployments=3),counts
checks=['All 13 OSNM device names match','All 13 OSNM cable endpoint pairs match','Three locations, three racks and three deployments exist']
for name in ('fabric-dryrun','site1-dryrun','site1-repeat-apply'):
    record=json.loads((ROOT/'evidence'/f'{name}.json').read_text())
    assert record['before']==record['after'],f'{name} changed inventory counts.'
    assert record['result']['status']['value']=='SUCCESS',record['result']['status']
    checks.append(name+': SUCCESS with unchanged inventory counts')

# Form/context validation must reject invalid requests before creating model objects.
branch=next(j for j in api('/api/extras/jobs/?limit=100')['results'] if j['name']=='OSNM Branch Site')
base=dict(deployment_name='osnm-site1',site_name='site1',physical_address='100 Example Avenue, Chicago, IL 60601',wan_port='Ethernet2',access_ports=2,rack_units=6,include_endpoint=True,dryrun=True,import_mode=False)
for label,overrides,expected_text in [('insufficient rack',{'rack_units':1},'2U'),('conflicting WAN port',{'site_name':'site3','deployment_name':'osnm-site3'},'already connected')]:
    before=inventory()
    try:
        api('/api/extras/jobs/'+branch['id']+'/run/',{'data':{**base,**overrides}},'POST')
    except RuntimeError as error:
        assert 'HTTP 400' in str(error) and expected_text in str(error),str(error)
        assert inventory()==before
        checks.append(label+': rejected with HTTP 400 and no inventory change')
    else:
        raise AssertionError(label+' was not rejected.')

result={'counts':counts,'checks':checks,'passed':len(checks),'topology_pairs':[sorted(r) for r in sorted(actual,key=lambda r:sorted(r))], 'notes':'Real API/Design Builder execution; synthetic inventory only; no device configuration rollout.'}
(ROOT/'evidence/verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
