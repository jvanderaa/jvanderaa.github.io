---
author: Josh VanDeraa
date: 2021-03-14 06:00:00+00:00
layout: single
comments: true
slug: nautobot-ansible-manufacturers
title: "Nautobot Ansible Collection: Manufacturers"
collections:
  - nautobot_ansible_collection
tags:
- nautobot
- ansible
- cisco
- arista
- juniper
toc: true
---
Adding your manufacturers via code is the easy way to get started with your Nautobot devices. Immediately after adding Sites, the next thing to get going when using Nautobot as your Source of Truth is to add in Manufacturers. These are just that, who makes the gear that you use. For this demonstration you will see adding just a few manufacturers. I'm not necessarily picking on any vendors and who should or shouldn't be here. It is just what my background brings.

## Module Documentation

* [Read the Docs](https://nautobot-ansible.readthedocs.io/en/latest/plugins/manufacturer_module.html)
* [GitHub](https://github.com/nautobot/nautobot-ansible/blob/develop/plugins/modules/manufacturer.py)

> This module **does** require [pynautobot](https://pynautobot.readthedocs.io/en/latest/) to execute properly

## Environment

For this demo, here are the versions shown:

| Component                   | Version  |
| --------------------------- | -------- |
| Nautobot                    | v1.0.0b2 |
| Nautobot Ansible Collection | v1.0.3   |
| pynautobot                  | 1.0.0    |

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
- name: "SETUP MANUFACTURERS"
  hosts: localhost
  connection: local
  gather_facts: false # No gathering facts about the container execution env
  tasks:
    - name: "05 - ADD MANUFACTURERS"
      networktocode.nautobot.manufacturer:
        url: "{{ lookup('env', 'NAUTOBOT_URL') }}"
        token: "{{ lookup('env', 'NAUTOBOT_TOKEN') }}"
        data:
          name: "{{ item }}"
      loop: "{{ manufacturers }}"


```

Here is the before:

![Nautobot Manufacturers Before](../../images/2021/nautobot_no_manufacturers.png)

### Example - Execution

Pretty short and sweet on this playbook. With having `Cisco` already present, you can see that the module is idempotent:

```yaml
josh-v@a6339c74e30d:~$ ansible-playbook add_manufacturers.yml -vv
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

PLAYBOOK: add_manufacturers.yml ********************************************************************************************
1 plays in add_manufacturers.yml

PLAY [SETUP MANUFACTURERS] *************************************************************************************************
META: ran handlers

TASK [05 - ADD MANUFACTURERS] **********************************************************************************************
task path: /local/add_manufacturers.yml:7
changed: [localhost] => (item=Arista) => changed=true 
  ansible_loop_var: item
  item: Arista
  manufacturer:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: fdead7a3-58a6-4a62-bb52-e21bbe2c6bf7
    last_updated: '2021-03-14T17:43:35.202049Z'
    name: Arista
    slug: arista
    url: http://nautobot-demo.josh-v.com/api/dcim/manufacturers/fdead7a3-58a6-4a62-bb52-e21bbe2c6bf7/
  msg: manufacturer Arista created
changed: [localhost] => (item=Cisco) => changed=true 
  ansible_loop_var: item
  item: Cisco
  manufacturer:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: 58c56ff8-f507-4356-9b6f-915be289831b
    last_updated: '2021-03-14T17:43:36.293444Z'
    name: Cisco
    slug: cisco
    url: http://nautobot-demo.josh-v.com/api/dcim/manufacturers/58c56ff8-f507-4356-9b6f-915be289831b/
  msg: manufacturer Cisco created
changed: [localhost] => (item=Juniper) => changed=true 
  ansible_loop_var: item
  item: Juniper
  manufacturer:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: 3aa03612-10d9-41e6-81ad-90a0d52fe03a
    last_updated: '2021-03-14T17:43:37.481073Z'
    name: Juniper
    slug: juniper
    url: http://nautobot-demo.josh-v.com/api/dcim/manufacturers/3aa03612-10d9-41e6-81ad-90a0d52fe03a/
  msg: manufacturer Juniper created
META: ran handlers
META: ran handlers

PLAY RECAP *****************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


```

### Example - Idempotency

Give this a second run and the playbook shows everything coming back as OK, without any changes.

```yaml
josh-v@a6339c74e30d:~$ ansible-playbook add_manufacturers.yml -vv
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

PLAYBOOK: add_manufacturers.yml ********************************************************************************************
1 plays in add_manufacturers.yml

PLAY [SETUP MANUFACTURERS] *************************************************************************************************
META: ran handlers

TASK [05 - ADD MANUFACTURERS] **********************************************************************************************
task path: /local/add_manufacturers.yml:7
ok: [localhost] => (item=Arista) => changed=false 
  ansible_loop_var: item
  item: Arista
  manufacturer:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    devicetype_count: 0
    id: fdead7a3-58a6-4a62-bb52-e21bbe2c6bf7
    inventoryitem_count: 0
    last_updated: '2021-03-14T17:43:35.202049Z'
    name: Arista
    platform_count: 0
    slug: arista
    url: http://nautobot-demo.josh-v.com/api/dcim/manufacturers/fdead7a3-58a6-4a62-bb52-e21bbe2c6bf7/
  msg: manufacturer Arista already exists
ok: [localhost] => (item=Cisco) => changed=false 
  ansible_loop_var: item
  item: Cisco
  manufacturer:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    devicetype_count: 0
    id: 58c56ff8-f507-4356-9b6f-915be289831b
    inventoryitem_count: 0
    last_updated: '2021-03-14T17:43:36.293444Z'
    name: Cisco
    platform_count: 0
    slug: cisco
    url: http://nautobot-demo.josh-v.com/api/dcim/manufacturers/58c56ff8-f507-4356-9b6f-915be289831b/
  msg: manufacturer Cisco already exists
ok: [localhost] => (item=Juniper) => changed=false 
  ansible_loop_var: item
  item: Juniper
  manufacturer:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    devicetype_count: 0
    id: 3aa03612-10d9-41e6-81ad-90a0d52fe03a
    inventoryitem_count: 0
    last_updated: '2021-03-14T17:43:37.481073Z'
    name: Juniper
    platform_count: 0
    slug: juniper
    url: http://nautobot-demo.josh-v.com/api/dcim/manufacturers/3aa03612-10d9-41e6-81ad-90a0d52fe03a/
  msg: manufacturer Juniper already exists
META: ran handlers
META: ran handlers

PLAY RECAP *****************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

Now you see all of them showing up in Nautobot.

![Nautobot Manufacturers After](../../images/2021/nautobot_manufacturers.png)

## Summary

The manufacturers are a base to adding devices. To add/sync manufacturers you can leverage the Nautobot Ansible Collection for manufacturers to get this data synced. To have your entire environment completely automated with using Ansible, this is a great solution.
