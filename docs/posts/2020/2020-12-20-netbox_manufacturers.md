---
authors: [jvanderaa]
date: 2020-12-20
layout: single
comments: true
slug: netbox-ansible-manufacturers
title: "NetBox Ansible Collection: Manufacturers"
collections:
  - netbox_ansible_collection
categories:
- netbox
- ansible
- cisco
- arista
- juniper
toc: true
---

Adding your manufacturers via code is the easy way to get started with your NetBox devices. Immediately after adding Sites, the next thing to get going when using NetBox as your Source of Truth is to add in Manufacturers. These are just that, who makes the gear that you use. For this demonstration you will see adding just a few manufacturers. I'm not necessarily picking on any vendors and who should or shouldn't be here. It is just what my background brings.

!!! note
    This post was created when NetBox was an open source project used often in my automation framework. I have moved on to using [Nautobot](https://www.nautobot.com) due to the project vision and providing a methodology that will drive network automation forward further. You may want to take a look at it yourself.


## Module Documentation

* [Read the Docs](https://netbox-ansible-collection.readthedocs.io/en/latest/plugins/netbox_manufacturer_module.html)
* [GitHub](https://github.com/netbox-community/ansible_modules/blob/devel/plugins/modules/netbox_manufacturer.py)

> This module **does** require [pynetbox](https://github.com/digitalocean/pynetbox) to execute properly

## Environment

For this demo, here are the versions shown:

| Component                 | Version                                                                     |
| ------------------------- | --------------------------------------------------------------------------- |
| NetBox                    | v2.9.9 [(NetBox Docker)](https://github.com/netbox-community/netbox-docker) |
| NetBox Ansible Collection | v1.1.0                                                                      |
| pynetbox                  | 5.1.0                                                                       |

## Data File

The documentation indicates that there are two parameters, name and slug. I'm not going to modify the slug in any way for these as the auto-generated slug is just fine. Because of this, the demo will not have a more complex variable, just a list of manufacturers.

```yaml
---
manufacturers:
  - Arista
  - Cisco
  - Juniper
```

## Example

### Example - Adding Devices

Getting started I already have a Cisco manufacturer included from a different demo. This will not hurt what is being demonstrated here. The task to add a manufacturer looks like:

```yaml
---
- name: "ADD MANUFACTURERS TO NETBOX"
  hosts: localhost
  connection: local
  gather_facts: false # No gathering facts about the container execution env
  tasks:
    - name: "05 - ADD MANUFACTURERS" # Already present, showing idempotency
      netbox.netbox.netbox_manufacturer:
        netbox_url: "{{ lookup('env', 'NETBOX_URL') }}"
        netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
        data:
          name: "{{ item }}"
      loop: "{{ manufacturers }}"

```

Here is the before:

![NetBox Manufacturers Before](/images/2020/12/manufacturers_before.png)

### Example - Execution

Pretty short and sweet on this playbook. With having `Cisco` already present, you can see that the module is idempotent:

```yaml linenums="1"

josh-v@d27199d82bfc:~$ ansible-playbook add_manufacturers.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [ADD MANUFACTURERS TO NETBOX] *******************************************************************************************************

TASK [05 - ADD MANUFACTURERS] ************************************************************************************************************
changed: [localhost] => (item=Arista)
ok: [localhost] => (item=Cisco)
changed: [localhost] => (item=Juniper)

PLAY RECAP *******************************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


```

Now you see all of them showing up in NetBox.

![NetBox Manufacturers After](/images/2020/12/manufacturers_after.png)

## Summary

The manufacturers are a base to adding devices. To add/sync manufacturers you can leverage the NetBox Ansible Collection for manufacturers to get this data synced. To have your entire environment completely automated with using Ansible, this is a great solution.
