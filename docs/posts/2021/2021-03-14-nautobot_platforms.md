---
authors: [jvanderaa]
date: 2021-03-14
layout: single
comments: true
slug: nautobot-ansible-platforms
title: "Nautobot Ansible Collection: Platforms"
collections:
  - nautobot_ansible_collection
categories:
- nautobot
- ansible
- cisco
- arista
- juniper
toc: true
---
Platforms are an optional item when adding devices into Nautobot. The platform is the OS that you are going to be using. Most often this is used to help identify which driver your automation platform is going to be using. Specifically the slug of the platform is what needs to match. So in the terms of Ansible (since we are using Ansible to populate Nautobot), you will want to set Cisco IOS devices to **ios**. By having the slug match the automation platform name you have that information in your inventory. For these reasons I strongly recommend setting the Platform for devices.

## Module Documentation

* [Read the Docs](https://nautobot-ansible.readthedocs.io/en/latest/plugins/platform_module.html)
* [GitHub](https://github.com/nautobot/nautobot-ansible/blob/develop/plugins/modules/platform.py)

> This module **does** require [pynautobot](https://pynautobot.readthedocs.io/en/latest/) to execute properly

## Environment

For this demo, here are the versions shown:

| Component                   | Version  |
| --------------------------- | -------- |
| Nautobot                    | v1.0.0b2 |
| Nautobot Ansible Collection | v1.0.3   |
| pynautobot                  | 1.0.0    |

## Data File

Now that you may want to have a different slug than what is displayed, the data structure is getting slightly more complex than the manufacturers file. There will be a list of dictionaries, where the dictionary has three keys: name, slug, and manufacturer. Because in this series the platform is going to be tied to the manufacturer, the manufacturer is the next item in the list to get added after the site.

```yaml
---
platforms:
  - name: Arista EOS
    slug: eos
    manufacturer: Arista
  - name: Cisco IOS
    slug: ios
    manufacturer: Cisco
  - name: JUNOS
    slug: junos
    manufacturer: Juniper
```


## Example

### Example - Adding Platform

Getting started I already have a Cisco manufacturer included from a different demo. This will not hurt what is being demonstrated here. The task to add a manufacturer looks like:

```yaml
---
- name: "ADD PLATFORMS"
  hosts: localhost
  connection: local
  gather_facts: false # No gathering facts about the container execution env
  tasks:
    - name: "05 - ADD PLATFORMS"
      networktocode.nautobot.platform:
        url: "{{ lookup('env', 'NAUTOBOT_URL') }}"
        token: "{{ lookup('env', 'NAUTOBOT_TOKEN') }}"
        data:
          name: "{{ item['name'] }}"
          slug: "{{ item['slug'] }}"
          manufacturer: "{{ item['manufacturer'] }}"
      loop: "{{ platforms }}"


```

Before the execution there are no platforms showing in Nautobot.

![Nautobot No Platforms](/images/2021/nautobot_no_platforms.png)

### Example - Execution

This execution shows that all of the platforms are added.

```yaml
josh-v@a6339c74e30d:~$ ansible-playbook add_platforms.yml -vv
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

PLAYBOOK: add_platforms.yml ************************************************************************************************
1 plays in add_platforms.yml

PLAY [ADD PLATFORMS] *******************************************************************************************************
META: ran handlers

TASK [05 - ADD PLATFORMS] **************************************************************************************************
task path: /local/add_platforms.yml:7
changed: [localhost] => (item={'name': 'Arista EOS', 'slug': 'eos', 'manufacturer': 'Arista'}) => changed=true 
  ansible_loop_var: item
  item:
    manufacturer: Arista
    name: Arista EOS
    slug: eos
  msg: platform Arista EOS created
  platform:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: 1d6b8698-c709-49f7-921e-d4a4c85f3317
    last_updated: '2021-03-14T18:33:18.255025Z'
    manufacturer: fdead7a3-58a6-4a62-bb52-e21bbe2c6bf7
    name: Arista EOS
    napalm_args: null
    napalm_driver: ''
    slug: eos
    url: http://nautobot-demo.josh-v.com/api/dcim/platforms/1d6b8698-c709-49f7-921e-d4a4c85f3317/
changed: [localhost] => (item={'name': 'Cisco IOS', 'slug': 'ios', 'manufacturer': 'Cisco'}) => changed=true 
  ansible_loop_var: item
  item:
    manufacturer: Cisco
    name: Cisco IOS
    slug: ios
  msg: platform Cisco IOS created
  platform:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: 96d58cc1-ad7e-43c7-a79f-db748e6eb894
    last_updated: '2021-03-14T18:33:19.081567Z'
    manufacturer: 58c56ff8-f507-4356-9b6f-915be289831b
    name: Cisco IOS
    napalm_args: null
    napalm_driver: ''
    slug: ios
    url: http://nautobot-demo.josh-v.com/api/dcim/platforms/96d58cc1-ad7e-43c7-a79f-db748e6eb894/
changed: [localhost] => (item={'name': 'JUNOS', 'slug': 'junos', 'manufacturer': 'Juniper'}) => changed=true 
  ansible_loop_var: item
  item:
    manufacturer: Juniper
    name: JUNOS
    slug: junos
  msg: platform JUNOS created
  platform:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    id: a6abfcb8-3ec9-4067-9aca-e88f9fa8eb87
    last_updated: '2021-03-14T18:33:19.884201Z'
    manufacturer: 3aa03612-10d9-41e6-81ad-90a0d52fe03a
    name: JUNOS
    napalm_args: null
    napalm_driver: ''
    slug: junos
    url: http://nautobot-demo.josh-v.com/api/dcim/platforms/a6abfcb8-3ec9-4067-9aca-e88f9fa8eb87/
META: ran handlers
META: ran handlers

PLAY RECAP *****************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

Now you see all of the defined platforms showing up in Nautobot.

![NetBox Platforms After](/images/2021/nautobot_platforms.png)

### Example - Idempotency

Showing the idempotency of the module, on the second run there are no changes made.

```yaml
josh-v@a6339c74e30d:~$ ansible-playbook add_platforms.yml -vv
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

PLAYBOOK: add_platforms.yml ************************************************************************************************
1 plays in add_platforms.yml

PLAY [ADD PLATFORMS] *******************************************************************************************************
META: ran handlers

TASK [05 - ADD PLATFORMS] **************************************************************************************************
task path: /local/add_platforms.yml:7
ok: [localhost] => (item={'name': 'Arista EOS', 'slug': 'eos', 'manufacturer': 'Arista'}) => changed=false 
  ansible_loop_var: item
  item:
    manufacturer: Arista
    name: Arista EOS
    slug: eos
  msg: platform Arista EOS already exists
  platform:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    device_count: 0
    id: 1d6b8698-c709-49f7-921e-d4a4c85f3317
    last_updated: '2021-03-14T18:33:18.255025Z'
    manufacturer: fdead7a3-58a6-4a62-bb52-e21bbe2c6bf7
    name: Arista EOS
    napalm_args: null
    napalm_driver: ''
    slug: eos
    url: http://nautobot-demo.josh-v.com/api/dcim/platforms/1d6b8698-c709-49f7-921e-d4a4c85f3317/
    virtualmachine_count: 0
ok: [localhost] => (item={'name': 'Cisco IOS', 'slug': 'ios', 'manufacturer': 'Cisco'}) => changed=false 
  ansible_loop_var: item
  item:
    manufacturer: Cisco
    name: Cisco IOS
    slug: ios
  msg: platform Cisco IOS already exists
  platform:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    device_count: 0
    id: 96d58cc1-ad7e-43c7-a79f-db748e6eb894
    last_updated: '2021-03-14T18:33:19.081567Z'
    manufacturer: 58c56ff8-f507-4356-9b6f-915be289831b
    name: Cisco IOS
    napalm_args: null
    napalm_driver: ''
    slug: ios
    url: http://nautobot-demo.josh-v.com/api/dcim/platforms/96d58cc1-ad7e-43c7-a79f-db748e6eb894/
    virtualmachine_count: 0
ok: [localhost] => (item={'name': 'JUNOS', 'slug': 'junos', 'manufacturer': 'Juniper'}) => changed=false 
  ansible_loop_var: item
  item:
    manufacturer: Juniper
    name: JUNOS
    slug: junos
  msg: platform JUNOS already exists
  platform:
    created: '2021-03-14'
    custom_fields: {}
    description: ''
    device_count: 0
    id: a6abfcb8-3ec9-4067-9aca-e88f9fa8eb87
    last_updated: '2021-03-14T18:33:19.884201Z'
    manufacturer: 3aa03612-10d9-41e6-81ad-90a0d52fe03a
    name: JUNOS
    napalm_args: null
    napalm_driver: ''
    slug: junos
    url: http://nautobot-demo.josh-v.com/api/dcim/platforms/a6abfcb8-3ec9-4067-9aca-e88f9fa8eb87/
    virtualmachine_count: 0
META: ran handlers
META: ran handlers

PLAY RECAP *****************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

## Summary

Platforms are one of the items that you will strongly want to get updated into Nautobot. By associating a device with a platform you can then use it in the inventory plugins to identify things such as the `ansible_network_os` dynamically. Need to have a new platform to test things with, just create a new platform, change a few settings, and the information is dynamically available within your playbooks.  

Hope this has helped. If so, let me know with a comment below or give a thumbs up on the post. You can leave a comment or connect with me on Twitter as well, at [@vanderaaj](https://twitter.com/vanderaaj/).  

Thanks,

Josh
