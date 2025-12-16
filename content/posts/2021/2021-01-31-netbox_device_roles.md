---
author: Josh VanDeraa
date: 2021-01-31 06:00:00+00:00
layout: single
comments: true
slug: netbox-ansible-device-roles
title: "NetBox Ansible Collection: Device Roles"
collections:
  - netbox_ansible_collection
tags:
- netbox
- ansible
- cisco
- arista
- juniper
toc: true
---

A device role is aptly named, the role of the device. This is likely to be something that is meaningful to your organization and could change. For example you may have the 3 tier system of Core, Distribution, and Access layer environments. These are just fine. So you would want to have the roles there to reflect this reality. You may have leaf-spine environments, there are two more roles. And in my past I have also had roles that would indicate that there are dedicated DMZ, WAN edge, Internet edge devices. So this is the place to set this.

{{< alert >}}
This post was created when NetBox was an open source project used often in my automation framework. I have moved on to using [Nautobot](https://www.nautobot.com) due to the project vision and providing a methodology that will drive network automation forward further. You may want to take a look at it yourself.
{{< /alert >}}

## Module Documentation

* [Read the Docs](https://netbox-ansible-collection.readthedocs.io/en/latest/plugins/netbox_device_role_module.html)
* [GitHub](https://github.com/netbox-community/ansible_modules/blob/devel/plugins/modules/netbox_device_role.py)

> This module **does** require [pynetbox](https://github.com/digitalocean/pynetbox) to execute properly

Outside of the NetBox URL and Token, the data parameter has a single required parameter of **name**. There are only a few additional options, so those are worth mentioning here of color, slug (will be auto-generated if not), and a yes/no parameter of vm_role.

## Environment

For this demo, here are the versions shown:

| Component                 | Version                                                                      |
| ------------------------- | ---------------------------------------------------------------------------- |
| NetBox                    | v2.9.10 [(NetBox Docker)](https://github.com/netbox-community/netbox-docker) |
| NetBox Ansible Collection | v2.0.0                                                                       |
| pynetbox                  | 5.3.1                                                                        |

## Data File

The roles are going to be a little more straight forward. We will only set the name, color, and if the role can be a VM or not, from the vm_role key.

```yaml
---
device_roles:
  - name: Firewall
    color: "FF0000"
    vm_role: true
  - name: Leaf
    color: "008000"
    vm_role: false
  - name: Router
    color: "000080"
    vm_role: true
  - name: Server
    color: "000000"
    vm_role: false
  - name: Spine
    color: "0000FF"
    vm_role: false
  - name: Switch
    color: "008000"
    vm_role: true
  - name: VM
    color: "00FFFF"
    vm_role: true
```

## Example

### Example - Adding Device Roles

Running the playbook on the roles are going to be straight to the point.

```yaml

---
- name: "ADD DEVICE ROLES TO NETBOX"
  hosts: localhost
  connection: local
  gather_facts: false # No gathering facts about the container execution env
  tasks:
    - name: "05 - ADD DEVICE ROLES" # Already present, showing idempotency
      netbox.netbox.netbox_device_role:
        netbox_url: "{{ lookup('env', 'NETBOX_URL') }}"
        netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
        data:
          name: "{{ item['name'] }}"
          color: "{{ item['color'] }}"
          vm_role: "{{ item['vm_role'] }}"
      loop: "{{ device_roles }}"

```

### Example - Execution

This execution shows that all of the device types are added.

{{< highlight yaml "linenos=table" >}}

josh-v@588715249c44:~$ ansible-playbook add_device_role.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [ADD DEVICE ROLES TO NETBOX] *********************************************************************************************************************

TASK [05 - ADD DEVICE ROLES] **************************************************************************************************************************
changed: [localhost] => (item={'name': 'Firewall', 'color': 'FF0000', 'vm_role': True})
changed: [localhost] => (item={'name': 'Leaf', 'color': '008000', 'vm_role': False})
changed: [localhost] => (item={'name': 'Router', 'color': '000080', 'vm_role': True})
changed: [localhost] => (item={'name': 'Server', 'color': '000000', 'vm_role': False})
changed: [localhost] => (item={'name': 'Spine', 'color': '0000FF', 'vm_role': False})
changed: [localhost] => (item={'name': 'Switch', 'color': '008000', 'vm_role': True})
changed: [localhost] => (item={'name': 'VM', 'color': '00FFFF', 'vm_role': True})

PLAY RECAP ********************************************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


{{< /highlight>}}

The second execution of playbook shows that with these three settings the module is idempotent:

{{< highlight yaml "linenos=table" >}}

josh-v@588715249c44:~$ ansible-playbook add_device_role.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [ADD DEVICE ROLES TO NETBOX] *********************************************************************************************************************

TASK [05 - ADD DEVICE ROLES] **************************************************************************************************************************
ok: [localhost] => (item={'name': 'Firewall', 'color': 'FF0000', 'vm_role': True})
ok: [localhost] => (item={'name': 'Leaf', 'color': '008000', 'vm_role': False})
ok: [localhost] => (item={'name': 'Router', 'color': '000080', 'vm_role': True})
ok: [localhost] => (item={'name': 'Server', 'color': '000000', 'vm_role': False})
ok: [localhost] => (item={'name': 'Spine', 'color': '0000FF', 'vm_role': False})
ok: [localhost] => (item={'name': 'Switch', 'color': '008000', 'vm_role': True})
ok: [localhost] => (item={'name': 'VM', 'color': '00FFFF', 'vm_role': True})

PLAY RECAP ********************************************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


{{< /highlight>}}

After completion of this you will have the device roles are now available to be assigned out.

## Summary

Device roles are a required item to add devices to NetBox. This can be as generic as "Device" or "Network Device". However, I **strongly** encourage you to look at putting some thought into the roles that you will assign to devices. This will become very helpful in the future as you look at building out the automation platform. You can see in the inventory build, you can assign devices based on roles to an inventory group. This becomes particularly helpful when you want to run a playbook against a single group, such as all Leaf switches, or all Spine switches that must have a particular configuration set.  

Hope this has helped. If so, let me know with a comment below or give a thumbs up on the post.
