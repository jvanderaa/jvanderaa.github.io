"""Private local API utility: submit real Jobs and retain credential-free evidence."""
import argparse
import json
from pathlib import Path
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
ENV = dict(line.split('=',1) for line in (ROOT/'.lab.env').read_text().splitlines() if '=' in line)
BASE = 'http://127.0.0.1:8089'

def api(path, data=None, method=None):
    req=urllib.request.Request(BASE+path, data=json.dumps(data).encode() if data is not None else None,
        headers={'Authorization':'Token '+ENV['NAUTOBOT_SUPERUSER_API_TOKEN'],'Content-Type':'application/json'},method=method)
    try:
        with urllib.request.urlopen(req,timeout=25) as response:
            return json.load(response)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'HTTP {e.code}: '+e.read().decode()[:6000]) from None

def inventory():
    result={}
    for model in ('locations','racks','devices','interfaces','cables'):
        result[model]=api('/api/dcim/'+model+'/?limit=1')['count']
    result['deployments']=api('/api/plugins/design-builder/deployments/?limit=1')['count']
    return result

def get_jobs():
    return [j for j in api('/api/extras/jobs/?limit=100')['results'] if j['name'].startswith('OSNM')]

def submit(job_name, data, output):
    job=next(j for j in get_jobs() if j['name']==job_name)
    if not job['enabled']:
        api('/api/extras/jobs/'+job['id']+'/',{'enabled':True},'PATCH')
    before=inventory()
    response=api('/api/extras/jobs/'+job['id']+'/run/',{'data':data},'POST')
    result=response.get('job_result',response)
    path=ROOT/'evidence'/output
    record={'job_name':job_name,'job_id':job['id'],'input':data,'before':before,'submission':result}
    path.write_text(json.dumps(record,indent=2))
    result_id=result['id']
    for _ in range(45):
        result=api('/api/extras/job-results/'+result_id+'/')
        state=result.get('status'); state=state.get('value') if isinstance(state,dict) else state
        if state in ('SUCCESS','FAILURE','ERRORED','ABORTED','REVOKED'):
            record.update(result=result,after=inventory())
            path.write_text(json.dumps(record,indent=2))
            print(json.dumps({'job_result_id':result_id,'status':state,'before':before,'after':record['after'],'evidence':str(path)},indent=2))
            if state!='SUCCESS':
                print(json.dumps(result.get('result'),indent=2))
                raise SystemExit(1)
            return record
        time.sleep(1)
    print(json.dumps({'job_result_id':result_id,'status':'pending; inspect existing result before retry','evidence':str(path)}))
    raise SystemExit(2)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=['jobs','inventory','fabric','site1','site2','site1-repeat'])
    parser.add_argument('--dry-run',action='store_true')
    args=parser.parse_args()
    if args.action=='jobs':
        print(json.dumps([{k:j.get(k) for k in ('id','name','enabled','module_name','job_class_name')} for j in get_jobs()],indent=2))
    elif args.action=='inventory': print(json.dumps(inventory(),indent=2))
    else:
        site='site1' if args.action=='site1-repeat' else args.action
        data={'deployment_name':'osnm-'+('dc1' if site=='fabric' else site), 'dryrun':args.dry_run,'import_mode':False}
        if site!='fabric':data.update(site_name=site,physical_address=f"{100 if site=='site1' else 200} Example Avenue, Chicago, IL 60601",wan_port='Ethernet2' if site=='site1' else 'Ethernet3',access_ports=2,rack_units=6,include_endpoint=True)
        submit('OSNM Data Center Fabric' if args.action=='fabric' else 'OSNM Branch Site',data,args.action+('-dryrun' if args.dry_run else '-apply')+'.json')
