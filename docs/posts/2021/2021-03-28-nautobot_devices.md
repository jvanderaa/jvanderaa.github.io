---
authors: [jvanderaa]
date: 2021-03-28
layout: single
comments: true
slug: nautobot-ansible-devices
title: "Nautobot Ansible Collection: Devices"
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

All of the work through the modules thus far in the series have brought us to what we all want to see. How to get or update device information inside of Nautobot. Adding of sites, device types, device roles are required to get us to this point. Now you can see how to add a device to Nautobot using the networktocode.nautobot.device module.  

There are many optional parameters for the module specifically. I encourage you to take a look at the module documentation (linked below) in order to get a good sense of all of the options available. The required parameters for a device that is present are:

* device_role
* device_type
* name
* site
* status

An important caveat for me is that this is something that should be done with rarity. Only when truly adding a device to Nautobot, in a programmatic way this should be used. I **do not** advocate for running this module constantly based on your devices. The idea is to get Nautobot to be your source of truth about devices, not to have devices be the source of truth and updating Nautobot.  

So where do I see this being run? I do absolutely see it being a part of a pipeline or a service portal. The idea being that the service portal has a request for a new site to be turned up. That in turn kicks off an Ansible Playbook that will make the necessary updates to Nautobot, and is done in a consistent manor.

<!-- more -->

## Module Documentation

* [Read the Docs](https://nautobot-ansible.readthedocs.io/en/latest/plugins/device_module.html)
* [GitHub](https://github.com/nautobot/nautobot-ansible/blob/develop/plugins/modules/device.py)

> This module **does** require [pynautobot](https://pynautobot.readthedocs.io/en/latest/) to execute properly

## Environment

For this demo, here are the versions shown:

| Component                   | Version  |
| --------------------------- | -------- |
| Nautobot                    | v1.0.0b2 |
| Nautobot Ansible Collection | v1.0.3   |
| pynautobot                  | 1.0.1    |

## Data File

The Nautobot devices file is going to be a little bit more involved. In this particular demo case there are no existing inventories to use. If you want to see a demo of a similar how to add devices to NetBox using an existing Ansible inventory, I encourage you to take a look at my [GitHub repository](https://github.com/jvanderaa/ansible_netbox_demo) where I did a Meetup video on working with [Ansible + NetBox](https://www.youtube.com/watch?v=GyQf5F0gr3w). The same/similar concept can be used with Nautobot.  

To simulate the idea that we are going to be running a playbook execution as part of a service request, here is the data file that will be fed to the Ansible playbook:

```yaml
# group_vars/all/devices.yml
---
devices:
  - name: "grb-rtr01"
    site: "GRB"
    device_role: "Router"
    device_type: "IOSv"
  - name: "msp-rtr01"
    site: "MSP"
    device_role: "Router"
    device_type: "IOSv"
```

## Example

### Example - Adding Device Types

First if you are following along with the examples thus far, I made a new site here. So in order to accommodate the new site, I added GRB and re-ran the playbook to create sites. That was done successfully and idempotently with only the GRB site being added.

```yaml

---
- name: "ADD DEVICES"
  hosts: localhost
  connection: local
  gather_facts: false # No gathering facts about the container execution env
  tasks:
    - name: "05 - ADD DEVICES"
      networktocode.nautobot.device:
        url: "{{ lookup('env', 'NAUTOBOT_URL') }}"
        token: "{{ lookup('env', 'NAUTOBOT_TOKEN') }}"
        data:
          name: "{{ item['name'] }}"
          site: "{{ item['site'] }}"
          device_role: "{{ item['device_role'] }}"
          device_type: "{{ item['device_type'] }}"
          platform: "IOS"
          status: "Active" # Newly required for Nautobot, a status of some kind
      loop: "{{ devices }}"


```

### Example - Execution

Before the execution there are no devices within Nautobot:

![Nautobot Without Devices](/images/2021/nautobot_no_devices.png)

This execution shows that all of the device types are added.

```yaml linenums="1"

josh-v@1297da6292df:~$ ansible-playbook add_devices.yml -vv
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

PLAYBOOK: add_devices.yml *******************************************************************************************************
1 plays in add_devices.yml

PLAY [ADD DEVICES] **************************************************************************************************************
META: ran handlers

TASK [05 - ADD DEVICES] *********************************************************************************************************
task path: /local/add_devices.yml:7
changed: [localhost] => (item={'name': 'grb-rtr01', 'site': 'GRB', 'device_role': 'Router', 'device_type': 'IOSv'}) => changed=true 
  ansible_loop_var: item
  device:
    asset_tag: null
    cluster: null
    comments: ''
    config_context: {}
    created: '2021-03-28'
    custom_fields: {}
    device_role: c6909cfd-0fd9-4ab1-b0e7-58493fff84b7
    device_type: 70504d2c-1641-4e6d-be40-192eb1d6e0c0
    display_name: grb-rtr01
    face: null
    id: 7757ffbd-cca8-49ee-978f-66fbdb3f6b14
    last_updated: '2021-03-28T15:48:29.324146Z'
    local_context_data: null
    name: grb-rtr01
    parent_device: null
    platform: 96d58cc1-ad7e-43c7-a79f-db748e6eb894
    position: null
    primary_ip: null
    primary_ip4: null
    primary_ip6: null
    rack: null
    serial: ''
    site: c92f368a-93a0-472b-a391-b9e9665b42a4
    status: active
    tags: []
    tenant: null
    url: http://nautobot-demo.josh-v.com/api/dcim/devices/7757ffbd-cca8-49ee-978f-66fbdb3f6b14/
    vc_position: null
    vc_priority: null
    virtual_chassis: null
  item:
    device_role: Router
    device_type: IOSv
    name: grb-rtr01
    site: GRB
  msg: device grb-rtr01 created
changed: [localhost] => (item={'name': 'msp-rtr01', 'site': 'MSP', 'device_role': 'Router', 'device_type': 'IOSv'}) => changed=true 
  ansible_loop_var: item
  device:
    asset_tag: null
    cluster: null
    comments: ''
    config_context: {}
    created: '2021-03-28'
    custom_fields: {}
    device_role: c6909cfd-0fd9-4ab1-b0e7-58493fff84b7
    device_type: 70504d2c-1641-4e6d-be40-192eb1d6e0c0
    display_name: msp-rtr01
    face: null
    id: 72f14290-865d-43a6-af7b-4e29c6400460
    last_updated: '2021-03-28T15:48:30.966452Z'
    local_context_data: null
    name: msp-rtr01
    parent_device: null
    platform: 96d58cc1-ad7e-43c7-a79f-db748e6eb894
    position: null
    primary_ip: null
    primary_ip4: null
    primary_ip6: null
    rack: null
    serial: ''
    site: c72cce62-1dd6-483e-90a3-3331ea3155a8
    status: active
    tags: []
    tenant: null
    url: http://nautobot-demo.josh-v.com/api/dcim/devices/72f14290-865d-43a6-af7b-4e29c6400460/
    vc_position: null
    vc_priority: null
    virtual_chassis: null
  item:
    device_role: Router
    device_type: IOSv
    name: msp-rtr01
    site: MSP
  msg: device msp-rtr01 created
META: ran handlers
META: ran handlers

PLAY RECAP **********************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


```

The second execution of playbook shows that with these three settings the module is idempotent:

```yaml linenums="1"

josh-v@1297da6292df:~$ ansible-playbook add_devices.yml -vv
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

PLAYBOOK: add_devices.yml *******************************************************************************************************
1 plays in add_devices.yml

PLAY [ADD DEVICES] **************************************************************************************************************
META: ran handlers

TASK [05 - ADD DEVICES] *********************************************************************************************************
task path: /local/add_devices.yml:7
ok: [localhost] => (item={'name': 'grb-rtr01', 'site': 'GRB', 'device_role': 'Router', 'device_type': 'IOSv'}) => changed=false 
  ansible_loop_var: item
  device:
    asset_tag: null
    cluster: null
    comments: ''
    config_context: {}
    created: '2021-03-28'
    custom_fields: {}
    device_role: c6909cfd-0fd9-4ab1-b0e7-58493fff84b7
    device_type: 70504d2c-1641-4e6d-be40-192eb1d6e0c0
    display_name: grb-rtr01
    face: null
    id: 7757ffbd-cca8-49ee-978f-66fbdb3f6b14
    last_updated: '2021-03-28T15:48:29.324146Z'
    local_context_data: null
    name: grb-rtr01
    parent_device: null
    platform: 96d58cc1-ad7e-43c7-a79f-db748e6eb894
    position: null
    primary_ip: null
    primary_ip4: null
    primary_ip6: null
    rack: null
    serial: ''
    site: c92f368a-93a0-472b-a391-b9e9665b42a4
    status: active
    tags: []
    tenant: null
    url: http://nautobot-demo.josh-v.com/api/dcim/devices/7757ffbd-cca8-49ee-978f-66fbdb3f6b14/
    vc_position: null
    vc_priority: null
    virtual_chassis: null
  item:
    device_role: Router
    device_type: IOSv
    name: grb-rtr01
    site: GRB
  msg: device grb-rtr01 already exists
ok: [localhost] => (item={'name': 'msp-rtr01', 'site': 'MSP', 'device_role': 'Router', 'device_type': 'IOSv'}) => changed=false 
  ansible_loop_var: item
  device:
    asset_tag: null
    cluster: null
    comments: ''
    config_context: {}
    created: '2021-03-28'
    custom_fields: {}
    device_role: c6909cfd-0fd9-4ab1-b0e7-58493fff84b7
    device_type: 70504d2c-1641-4e6d-be40-192eb1d6e0c0
    display_name: msp-rtr01
    face: null
    id: 72f14290-865d-43a6-af7b-4e29c6400460
    last_updated: '2021-03-28T15:48:30.966452Z'
    local_context_data: null
    name: msp-rtr01
    parent_device: null
    platform: 96d58cc1-ad7e-43c7-a79f-db748e6eb894
    position: null
    primary_ip: null
    primary_ip4: null
    primary_ip6: null
    rack: null
    serial: ''
    site: c72cce62-1dd6-483e-90a3-3331ea3155a8
    status: active
    tags: []
    tenant: null
    url: http://nautobot-demo.josh-v.com/api/dcim/devices/72f14290-865d-43a6-af7b-4e29c6400460/
    vc_position: null
    vc_priority: null
    virtual_chassis: null
  item:
    device_role: Router
    device_type: IOSv
    name: msp-rtr01
    site: MSP
  msg: device msp-rtr01 already exists
META: ran handlers
META: ran handlers

PLAY RECAP **********************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


```

### Post Execution

After the execution and notice that the module is idempotent, the two devices shown are all set to be added.

![Nautobot Devices](/images/2021/nautobot_devices.png)

## Summary

Now that you have some devices, you can start to do a little bit more with your Nautobot environment. This playbook purposely did not add more information about the device yet, such as the serial number, interfaces, or IP addressing. This is all information that you can add more about the device as well using Ansible Facts and Resource Modules to continue to develop your source of truth. More likely to come in the future, or you can check out the content on GitHub and YouTube referenced above for immediate reference.


Getting devices into Nautobot provides a powerful place to put your source of truth for automation. It does take a small bit to get to a good place, but with a little bit of effort up front you can get things done in a **consistent** and **repeatable** fashion. No more having to do things by hand with the data points.  

Hope this has helped. If so, let me know with a comment below or give a thumbs up on the post.
