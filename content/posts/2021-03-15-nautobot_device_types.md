---
author: Josh VanDeraa
date: 2021-03-15 06:00:00+00:00
layout: single
comments: true
slug: nautobot-ansible-device-types
title: "Nautobot Ansible Collection: Device Types"
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

A device type is the next piece in the Nautobot Device onboarding requirements. The device type corresponds to the model number of the hardware (or virtual machine). This is where you are able to template out devices during their creation. So if you have a console port on a device type, that console port will be created when you create the device. However, **there is NOT** a relationship built between the device type and the device. If the device type gets updated after the device is created, the device itself is **not** updated. 

## Module Documentation

* [Read the Docs](https://nautobot-ansible.readthedocs.io/en/latest/plugins/device_type_module.html)
* [GitHub](https://github.com/nautobot/nautobot-ansible/blob/develop/plugins/modules/device_type.py)

> This module **does** require [pynautobot](https://pynautobot.readthedocs.io/en/latest/) to execute properly

## Environment

For this demo, here are the versions shown:

| Component                   | Version  |
| --------------------------- | -------- |
| Nautobot                    | v1.0.0b2 |
| Nautobot Ansible Collection | v1.0.3   |
| pynautobot                  | 1.0.1    |

## Data File

This gets to be a little more of the complex data source types. There are many data parameters that are good to include. The minimum data parameter has just the model. But there are going to be many more options as you build out your Nautobot environment that feeds into the data correlation that makes Nautobot a pleasure to use. Such as the manufacturer that it is tied to, the part number, and the u_height as you build rack diagrams from Nautobot.  

In the demo the model, manufacturer, part number, and slug will get defined. The slug will be the lower case of the model name. The primary key is the model name in this case.

```yaml
---
device_types:
  - model: "ASAv"
    manufacturer: "Cisco"
    slug: "asav"
    part_number: "asav"
  - model: "CSR1000v"
    manufacturer: "Cisco"
    slug: "csr1000v"
    part_number: "csr1000v"
  - model: "IOSv"
    manufacturer: "Cisco"
    slug: "iosv"
    part_number: "iosv"
  - model: "nxosv"
    manufacturer: "Cisco"
    slug: "nxosv"
    part_number: "nxosv"
  - model: "vEOS"
    manufacturer: "Arista"
    slug: "veos"
    part_number: "veos"
```

## Example

### Example - Adding Device Types

Getting started I already have a Cisco manufacturer included from a different demo. This will not hurt what is being demonstrated here. The task to add a manufacturer looks like:

```yaml

---
- name: "ADD DEVICE TYPES"
  hosts: localhost
  connection: local
  gather_facts: false # No gathering facts about the container execution env
  tasks:
    - name: "05 - ADD DEVICE TYPES"
      networktocode.nautobot.device_type:
        url: "{{ lookup('env', 'NAUTOBOT_URL') }}"
        token: "{{ lookup('env', 'NAUTOBOT_TOKEN') }}"
        data:
          model: "{{ item['model'] }}"
          manufacturer: "{{ item['manufacturer'] }}"
          slug: "{{ item['slug'] }}"
          part_number: "{{ item['part_number'] }}"
      loop: "{{ device_types }}"


```

### Example - Execution

This execution shows that all of the device types are added. Before the execution Nautobot does not have any device types.

![Nautobot no device types](/images/2021/nautobot_no_device_types.png)

```yaml
josh-v@60a6498959f8:~$ ansible-playbook add_device_types.yml -vv
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

PLAYBOOK: add_device_types.yml **************************************************************************************************************************
1 plays in add_device_types.yml

PLAY [ADD DEVICE TYPES] *********************************************************************************************************************************
META: ran handlers

TASK [05 - ADD DEVICE TYPES] ****************************************************************************************************************************
task path: /local/add_device_types.yml:7
changed: [localhost] => (item={'model': 'ASAv', 'manufacturer': 'Cisco', 'slug': 'asav', 'part_number': 'asav'}) => changed=true 
  ansible_loop_var: item
  device_type:
    comments: ''
    created: '2021-03-16'
    custom_fields: {}
    display_name: Cisco ASAv
    front_image: null
    id: 0bdb5944-a2c2-4093-a83c-c8c69485d5ac
    is_full_depth: true
    last_updated: '2021-03-16T00:15:49.347705Z'
    manufacturer: 58c56ff8-f507-4356-9b6f-915be289831b
    model: ASAv
    part_number: asav
    rear_image: null
    slug: asav
    subdevice_role: null
    tags: []
    u_height: 1
    url: http://nautobot-demo.josh-v.com/api/dcim/device-types/0bdb5944-a2c2-4093-a83c-c8c69485d5ac/
  item:
    manufacturer: Cisco
    model: ASAv
    part_number: asav
    slug: asav
  msg: device_type asav created
changed: [localhost] => (item={'model': 'CSR1000v', 'manufacturer': 'Cisco', 'slug': 'csr1000v', 'part_number': 'csr1000v'}) => changed=true 
  ansible_loop_var: item
  device_type:
    comments: ''
    created: '2021-03-16'
    custom_fields: {}
    display_name: Cisco CSR1000v
    front_image: null
    id: a804d796-194a-46e2-af72-bdfbc179af92
    is_full_depth: true
    last_updated: '2021-03-16T00:15:50.335484Z'
    manufacturer: 58c56ff8-f507-4356-9b6f-915be289831b
    model: CSR1000v
    part_number: csr1000v
    rear_image: null
    slug: csr1000v
    subdevice_role: null
    tags: []
    u_height: 1
    url: http://nautobot-demo.josh-v.com/api/dcim/device-types/a804d796-194a-46e2-af72-bdfbc179af92/
  item:
    manufacturer: Cisco
    model: CSR1000v
    part_number: csr1000v
    slug: csr1000v
  msg: device_type csr1000v created
changed: [localhost] => (item={'model': 'IOSv', 'manufacturer': 'Cisco', 'slug': 'iosv', 'part_number': 'iosv'}) => changed=true 
  ansible_loop_var: item
  device_type:
    comments: ''
    created: '2021-03-16'
    custom_fields: {}
    display_name: Cisco IOSv
    front_image: null
    id: 70504d2c-1641-4e6d-be40-192eb1d6e0c0
    is_full_depth: true
    last_updated: '2021-03-16T00:15:51.095938Z'
    manufacturer: 58c56ff8-f507-4356-9b6f-915be289831b
    model: IOSv
    part_number: iosv
    rear_image: null
    slug: iosv
    subdevice_role: null
    tags: []
    u_height: 1
    url: http://nautobot-demo.josh-v.com/api/dcim/device-types/70504d2c-1641-4e6d-be40-192eb1d6e0c0/
  item:
    manufacturer: Cisco
    model: IOSv
    part_number: iosv
    slug: iosv
  msg: device_type iosv created
changed: [localhost] => (item={'model': 'nxosv', 'manufacturer': 'Cisco', 'slug': 'nxosv', 'part_number': 'nxosv'}) => changed=true 
  ansible_loop_var: item
  device_type:
    comments: ''
    created: '2021-03-16'
    custom_fields: {}
    display_name: Cisco nxosv
    front_image: null
    id: 177ec0e0-6455-4d0c-9074-ee3f519cdcd8
    is_full_depth: true
    last_updated: '2021-03-16T00:15:51.913297Z'
    manufacturer: 58c56ff8-f507-4356-9b6f-915be289831b
    model: nxosv
    part_number: nxosv
    rear_image: null
    slug: nxosv
    subdevice_role: null
    tags: []
    u_height: 1
    url: http://nautobot-demo.josh-v.com/api/dcim/device-types/177ec0e0-6455-4d0c-9074-ee3f519cdcd8/
  item:
    manufacturer: Cisco
    model: nxosv
    part_number: nxosv
    slug: nxosv
  msg: device_type nxosv created
changed: [localhost] => (item={'model': 'vEOS', 'manufacturer': 'Arista', 'slug': 'veos', 'part_number': 'veos'}) => changed=true 
  ansible_loop_var: item
  device_type:
    comments: ''
    created: '2021-03-16'
    custom_fields: {}
    display_name: Arista vEOS
    front_image: null
    id: f93a4194-a71d-4532-b6f7-0af6e67f8155
    is_full_depth: true
    last_updated: '2021-03-16T00:15:52.673428Z'
    manufacturer: fdead7a3-58a6-4a62-bb52-e21bbe2c6bf7
    model: vEOS
    part_number: veos
    rear_image: null
    slug: veos
    subdevice_role: null
    tags: []
    u_height: 1
    url: http://nautobot-demo.josh-v.com/api/dcim/device-types/f93a4194-a71d-4532-b6f7-0af6e67f8155/
  item:
    manufacturer: Arista
    model: vEOS
    part_number: veos
    slug: veos
  msg: device_type veos created
META: ran handlers
META: ran handlers

PLAY RECAP **********************************************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

At this point the device types are now available inside of the UI.

![Nautobot Device Types](/images/2021/nautobot_device_types.png)  

The second execution of playbook shows that with these three settings the module is idempotent:

{{< highlight yaml "linenos=table" >}}

josh-v@60a6498959f8:~$ ansible-playbook add_device_types.yml -vv
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

PLAYBOOK: add_device_types.yml **************************************************************************************************************************
1 plays in add_device_types.yml

PLAY [ADD DEVICE TYPES] *********************************************************************************************************************************
META: ran handlers

TASK [05 - ADD DEVICE TYPES] ****************************************************************************************************************************
task path: /local/add_device_types.yml:7
ok: [localhost] => (item={'model': 'ASAv', 'manufacturer': 'Cisco', 'slug': 'asav', 'part_number': 'asav'}) => changed=false 
  ansible_loop_var: item
  device_type:
    comments: ''
    created: '2021-03-16'
    custom_fields: {}
    device_count: 0
    display_name: Cisco ASAv
    front_image: null
    id: 0bdb5944-a2c2-4093-a83c-c8c69485d5ac
    is_full_depth: true
    last_updated: '2021-03-16T00:15:49.347705Z'
    manufacturer: 58c56ff8-f507-4356-9b6f-915be289831b
    model: ASAv
    part_number: asav
    rear_image: null
    slug: asav
    subdevice_role: null
    tags: []
    u_height: 1
    url: http://nautobot-demo.josh-v.com/api/dcim/device-types/0bdb5944-a2c2-4093-a83c-c8c69485d5ac/
  item:
    manufacturer: Cisco
    model: ASAv
    part_number: asav
    slug: asav
  msg: device_type asav already exists
ok: [localhost] => (item={'model': 'CSR1000v', 'manufacturer': 'Cisco', 'slug': 'csr1000v', 'part_number': 'csr1000v'}) => changed=false 
  ansible_loop_var: item
  device_type:
    comments: ''
    created: '2021-03-16'
    custom_fields: {}
    device_count: 0
    display_name: Cisco CSR1000v
    front_image: null
    id: a804d796-194a-46e2-af72-bdfbc179af92
    is_full_depth: true
    last_updated: '2021-03-16T00:15:50.335484Z'
    manufacturer: 58c56ff8-f507-4356-9b6f-915be289831b
    model: CSR1000v
    part_number: csr1000v
    rear_image: null
    slug: csr1000v
    subdevice_role: null
    tags: []
    u_height: 1
    url: http://nautobot-demo.josh-v.com/api/dcim/device-types/a804d796-194a-46e2-af72-bdfbc179af92/
  item:
    manufacturer: Cisco
    model: CSR1000v
    part_number: csr1000v
    slug: csr1000v
  msg: device_type csr1000v already exists
ok: [localhost] => (item={'model': 'IOSv', 'manufacturer': 'Cisco', 'slug': 'iosv', 'part_number': 'iosv'}) => changed=false 
  ansible_loop_var: item
  device_type:
    comments: ''
    created: '2021-03-16'
    custom_fields: {}
    device_count: 0
    display_name: Cisco IOSv
    front_image: null
    id: 70504d2c-1641-4e6d-be40-192eb1d6e0c0
    is_full_depth: true
    last_updated: '2021-03-16T00:15:51.095938Z'
    manufacturer: 58c56ff8-f507-4356-9b6f-915be289831b
    model: IOSv
    part_number: iosv
    rear_image: null
    slug: iosv
    subdevice_role: null
    tags: []
    u_height: 1
    url: http://nautobot-demo.josh-v.com/api/dcim/device-types/70504d2c-1641-4e6d-be40-192eb1d6e0c0/
  item:
    manufacturer: Cisco
    model: IOSv
    part_number: iosv
    slug: iosv
  msg: device_type iosv already exists
ok: [localhost] => (item={'model': 'nxosv', 'manufacturer': 'Cisco', 'slug': 'nxosv', 'part_number': 'nxosv'}) => changed=false 
  ansible_loop_var: item
  device_type:
    comments: ''
    created: '2021-03-16'
    custom_fields: {}
    device_count: 0
    display_name: Cisco nxosv
    front_image: null
    id: 177ec0e0-6455-4d0c-9074-ee3f519cdcd8
    is_full_depth: true
    last_updated: '2021-03-16T00:15:51.913297Z'
    manufacturer: 58c56ff8-f507-4356-9b6f-915be289831b
    model: nxosv
    part_number: nxosv
    rear_image: null
    slug: nxosv
    subdevice_role: null
    tags: []
    u_height: 1
    url: http://nautobot-demo.josh-v.com/api/dcim/device-types/177ec0e0-6455-4d0c-9074-ee3f519cdcd8/
  item:
    manufacturer: Cisco
    model: nxosv
    part_number: nxosv
    slug: nxosv
  msg: device_type nxosv already exists
ok: [localhost] => (item={'model': 'vEOS', 'manufacturer': 'Arista', 'slug': 'veos', 'part_number': 'veos'}) => changed=false 
  ansible_loop_var: item
  device_type:
    comments: ''
    created: '2021-03-16'
    custom_fields: {}
    device_count: 0
    display_name: Arista vEOS
    front_image: null
    id: f93a4194-a71d-4532-b6f7-0af6e67f8155
    is_full_depth: true
    last_updated: '2021-03-16T00:15:52.673428Z'
    manufacturer: fdead7a3-58a6-4a62-bb52-e21bbe2c6bf7
    model: vEOS
    part_number: veos
    rear_image: null
    slug: veos
    subdevice_role: null
    tags: []
    u_height: 1
    url: http://nautobot-demo.josh-v.com/api/dcim/device-types/f93a4194-a71d-4532-b6f7-0af6e67f8155/
  item:
    manufacturer: Arista
    model: vEOS
    part_number: veos
    slug: veos
  msg: device_type veos already exists
META: ran handlers
META: ran handlers

PLAY RECAP **********************************************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


{{< /highlight>}}

After completion of this you will have the device types (hardware models) available for you to assign to devices (coming up next).

## Summary

Device types are important so you know what model of devices you have to work with. This will come in handy as well in your automations that if you have a particular device type that you need to do something against. Such as having a separate type for Cisco Catalyst 3750G vs Catalyst 3750X. They are all 3750 switches, however you may need to apply a unique configuration set against a particular device type. By having this predefined in your source of truth, you are all set to be able to run automations against each.  

Hope this has helped. If so, let me know with a comment below or give a thumbs up on the post. Feel free to connect with me on Twitter [@vanderaaj](https://twitter.com/vanderaaj)
