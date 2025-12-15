---
date: 2021-03-14
layout: single
slug: nautobot-ansible-device-roles
title: 'Nautobot Ansible Collection: Device Roles'
collections:
- nautobot_ansible_collection
categories:
- nautobot
- ansible
- cisco
- arista
- juniper
toc: true
author: jvanderaa
params:
  showComments: true
---

A device role is aptly named, the role of the device. This is likely to be something that is meaningful to your organization and could change. For example you may have the 3 tier system of Core, Distribution, and Access layer environments. These are just fine. So you would want to have the roles there to reflect this reality. You may have leaf-spine environments, there are two more roles. And in my past I have also had roles that would indicate that there are dedicated DMZ, WAN edge, Internet edge devices. So this is the place to set this.

<!--more-->


## Module Documentation

* [Read the Docs](https://nautobot-ansible.readthedocs.io/en/latest/plugins/device_role_module.html)
* [GitHub](https://github.com/nautobot/nautobot-ansible/blob/develop/plugins/modules/device_role.py)

> This module **does** require [pynautobot](https://pynautobot.readthedocs.io/en/latest/) to execute properly

## Environment

For this demo, here are the versions shown:

| Component                   | Version  |
| --------------------------- | -------- |
| Nautobot                    | v1.0.0b2 |
| Nautobot Ansible Collection | v1.0.3   |
| pynautobot                  | 1.0.0    |

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

Running the playbook on the roles are going to be straight to the point. Before the execution Nautobot's UI shows no device roles:

![Nautobot no device role](/images/2021/nautobot_no_device_roles.png)

```yaml

---
- name: "ADD DEVICE ROLES"
  hosts: localhost
  connection: local
  gather_facts: false # No gathering facts about the container execution env
  tasks:
    - name: "05 - ADD DEVICE ROLES" # Already present, showing idempotency
      networktocode.nautobot.device_role:
        url: "{{ lookup('env', 'NAUTOBOT_URL') }}"
        token: "{{ lookup('env', 'NAUTOBOT_TOKEN') }}"
        data:
          name: "{{ item['name'] }}"
          color: "{{ item['color'] }}"
          vm_role: "{{ item['vm_role'] }}"
      loop: "{{ device_roles }}"


```

### Example - Execution

This execution shows that all of the device types are added.

```yaml linenums="1"

josh-v@a6339c74e30d:~$ ansible-playbook add_device_role.yml -vv
ansible-playbook 2.10.6
  config file = /local/ansible.cfg
  configured module search path = ['/local/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.7/site-packages/ansible
  executable location = /usr/local/bin/ansible-playbook
  python version = 3.7.10 (default, Feb 16 2021, 19:28:34) [GCC 8.3.0]
Using /local/ansible.cfg as config file
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'
redirecting (type: callback) ansible.builtin.yaml to community.general.yaml
redirecting (type: callback) ansible.builtin.yaml to community.general.yaml
Skipping callback 'default', as we already have a stdout callback.
Skipping callback 'minimal', as we already have a stdout callback.
Skipping callback 'oneline', as we already have a stdout callback.

PLAYBOOK: add_device_role.yml **********************************************************************************************
1 plays in add_device_role.yml

PLAY [ADD DEVICE ROLES] ****************************************************************************************************
META: ran handlers

TASK [05 - ADD DEVICE ROLES] ***********************************************************************************************
task path: /local/add_device_role.yml:7
changed: [localhost] => (item={'name': 'Firewall', 'color': 'FF0000', 'vm_role': True}) => changed=true 
  ansible_loop_var: item
  device_role:
    color: ff0000
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: 252bd7ba-3b15-4651-a7e3-e43cdd85227c
    last_updated: '2021-03-14T18:50:53.994175Z'
    name: Firewall
    slug: firewall
    url: http://nautobot-demo.josh-v.com/api/dcim/device-roles/252bd7ba-3b15-4651-a7e3-e43cdd85227c/
    vm_role: true
  item:
    color: FF0000
    name: Firewall
    vm_role: true
  msg: device_role Firewall created
changed: [localhost] => (item={'name': 'Leaf', 'color': '008000', 'vm_role': False}) => changed=true 
  ansible_loop_var: item
  device_role:
    color: 008000
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: 35f176c4-9b20-4e3c-b961-47c624afaa56
    last_updated: '2021-03-14T18:50:54.942372Z'
    name: Leaf
    slug: leaf
    url: http://nautobot-demo.josh-v.com/api/dcim/device-roles/35f176c4-9b20-4e3c-b961-47c624afaa56/
    vm_role: false
  item:
    color: 008000
    name: Leaf
    vm_role: false
  msg: device_role Leaf created
changed: [localhost] => (item={'name': 'Router', 'color': '000080', 'vm_role': True}) => changed=true 
  ansible_loop_var: item
  device_role:
    color: 000080
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: c6909cfd-0fd9-4ab1-b0e7-58493fff84b7
    last_updated: '2021-03-14T18:50:55.901588Z'
    name: Router
    slug: router
    url: http://nautobot-demo.josh-v.com/api/dcim/device-roles/c6909cfd-0fd9-4ab1-b0e7-58493fff84b7/
    vm_role: true
  item:
    color: 000080
    name: Router
    vm_role: true
  msg: device_role Router created
changed: [localhost] => (item={'name': 'Server', 'color': '000000', 'vm_role': False}) => changed=true 
  ansible_loop_var: item
  device_role:
    color: '000000'
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: f9acf678-7b71-4cf9-88f8-4e3ad3f499cb
    last_updated: '2021-03-14T18:50:57.004599Z'
    name: Server
    slug: server
    url: http://nautobot-demo.josh-v.com/api/dcim/device-roles/f9acf678-7b71-4cf9-88f8-4e3ad3f499cb/
    vm_role: false
  item:
    color: '000000'
    name: Server
    vm_role: false
  msg: device_role Server created
changed: [localhost] => (item={'name': 'Spine', 'color': '0000FF', 'vm_role': False}) => changed=true 
  ansible_loop_var: item
  device_role:
    color: 0000ff
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: 4121b0bf-8085-424e-bf0d-b11855cd9c04
    last_updated: '2021-03-14T18:50:57.912158Z'
    name: Spine
    slug: spine
    url: http://nautobot-demo.josh-v.com/api/dcim/device-roles/4121b0bf-8085-424e-bf0d-b11855cd9c04/
    vm_role: false
  item:
    color: 0000FF
    name: Spine
    vm_role: false
  msg: device_role Spine created
changed: [localhost] => (item={'name': 'Switch', 'color': '008000', 'vm_role': True}) => changed=true 
  ansible_loop_var: item
  device_role:
    color: 008000
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: c99fe14b-5172-446f-8bd5-78c1e84aaa1c
    last_updated: '2021-03-14T18:50:58.743836Z'
    name: Switch
    slug: switch
    url: http://nautobot-demo.josh-v.com/api/dcim/device-roles/c99fe14b-5172-446f-8bd5-78c1e84aaa1c/
    vm_role: true
  item:
    color: 008000
    name: Switch
    vm_role: true
  msg: device_role Switch created
changed: [localhost] => (item={'name': 'VM', 'color': '00FFFF', 'vm_role': True}) => changed=true 
  ansible_loop_var: item
  device_role:
    color: 00ffff
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: 00a2da7f-fe44-4332-bc58-391b429c97eb
    last_updated: '2021-03-14T18:50:59.548621Z'
    name: VM
    slug: vm
    url: http://nautobot-demo.josh-v.com/api/dcim/device-roles/00a2da7f-fe44-4332-bc58-391b429c97eb/
    vm_role: true
  item:
    color: 00FFFF
    name: VM
    vm_role: true
  msg: device_role VM created
META: ran handlers
META: ran handlers

PLAY RECAP *****************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


```

After completion of this you will have the device roles are now available to be assigned to devices. Taking a look the UI now has the data:

![Nautobot Device Roles](/images/2021/nautobot_device_roles.png)

## Summary

Device roles are a required item to add devices to Nautobot. This can be as generic as "Device" or "Network Device". However, I **strongly** encourage you to look at putting some thought into the roles that you will assign to devices. This will become very helpful in the future as you look at building out the automation platform. You can see in the inventory build, you can assign devices based on roles to an inventory group. This becomes particularly helpful when you want to run a playbook against a single group, such as all Leaf switches, or all Spine switches that must have a particular configuration set.  

Hope this has helped. If so, let me know with a comment below or give a thumbs up on the post. Connect with me on Twitter [@vanderaaj](https://twitter.com/vanderaaj).
