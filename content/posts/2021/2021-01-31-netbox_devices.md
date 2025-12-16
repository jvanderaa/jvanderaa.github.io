---
date: 2021-01-31
layout: single
slug: netbox-ansible-devices
title: 'NetBox Ansible Collection: Devices'
collections:
- netbox_ansible_collection
categories:
- netbox
- ansible
- cisco
- arista
- juniper
toc: true
author: jvanderaa
params:
  showComments: true
---

All of the work through the modules thus far in the series have brought us to what we all want to see. How to get or update device information inside of NetBox. Adding of sites, device types, device roles are required to get us to this point. Now you can see how to add a device to NetBox using the netbox.netbox.netbox_device module.  

{{< alert "neutral" >}}
This post was created when NetBox was an open source project used often in my automation framework. I have moved on to using [Nautobot](https://www.nautobot.com) due to the project vision and providing a methodology that will drive network automation forward further. You may want to take a look at it yourself.

{{< /alert >}}
<!--more-->

There are many optional parameters for the module specifically. I encourage you to take a look at the module documentaation (linked below) in order to get a good sense of all of the options available. The required parameters for a device that is present are:

* device_role
* device_type
* name
* site

An important caveat for me is that this is something that should be done with rarity. Only when truly adding a device to NetBox, in a programmatic way this should be used. I **do not** advocate for running this module constantly based on your devices. The idea is to get NetBox to be your source of truth about devices, not to have devices be the source of truth and updating NetBox.  

So where do I see this being run? I do absolutely see it being a part of a pipeline or a service portal. The idea being that the service portal has a request for a new site to be turned up. That in turn kicks off an Ansible Playbook that will make the necessary updates to NetBox, and is done in a consistent manor.

## Module Documentation

* [Read the Docs](https://netbox-ansible-collection.readthedocs.io/en/latest/plugins/netbox_device_module.html)
* [GitHub](https://github.com/netbox-community/ansible_modules/blob/devel/plugins/modules/netbox_device.py)

> This module **does** require [pynetbox](https://github.com/digitalocean/pynetbox) to execute properly

## Environment

For this demo, here are the versions shown:

| Component                 | Version                                                                      |
| ------------------------- | ---------------------------------------------------------------------------- |
| NetBox                    | v2.9.10 [(NetBox Docker)](https://github.com/netbox-community/netbox-docker) |
| NetBox Ansible Collection | v1.1.0                                                                       |
| pynetbox                  | 5.1.0                                                                        |

## Data File

The NetBox devices file is going to be a little bit more involved. In this particular demo case there are no existing inventories to use. If you want to see a demo of how to add devices to NetBox using an existing Ansible inventory, I encourage you to take a look at my [GitHub repository](https://github.com/jvanderaa/ansible_netbox_demo) where I did a Meetup video on working with [Ansible + NetBox](https://www.youtube.com/watch?v=GyQf5F0gr3w).  

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
- name: "ADD DEVICES TO NETBOX"
  hosts: localhost
  connection: local
  gather_facts: false # No gathering facts about the container execution env
  tasks:
    - name: "05 - ADD DEVICES"
      netbox.netbox.netbox_device:
        netbox_url: "{{ lookup('env', 'NETBOX_URL') }}"
        netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
        data:
          name: "{{ item['name'] }}"
          site: "{{ item['site'] }}"
          device_role: "{{ item['device_role'] }}"
          device_type: "{{ item['device_type'] }}"
      loop: "{{ devices }}"


```

### Example - Execution

This execution shows that all of the device types are added.

```yaml {linenos=true}

josh-v@588715249c44:~$ ansible-playbook add_devices.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [ADD DEVICES TO NETBOX] **************************************************************************************************************************

TASK [05 - ADD DEVICES] *******************************************************************************************************************************
changed: [localhost] => (item={'name': 'grb-rtr01', 'site': 'GRB', 'device_role': 'Router', 'device_type': 'IOSv'})
changed: [localhost] => (item={'name': 'msp-rtr01', 'site': 'MSP', 'device_role': 'Router', 'device_type': 'IOSv'})

PLAY RECAP ********************************************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 


```

The second execution of playbook shows that with these three settings the module is idempotent:

```yaml {linenos=true}

josh-v@588715249c44:~$ ansible-playbook add_devices.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [ADD DEVICES TO NETBOX] **************************************************************************************************************************

TASK [05 - ADD DEVICES] *******************************************************************************************************************************
ok: [localhost] => (item={'name': 'grb-rtr01', 'site': 'GRB', 'device_role': 'Router', 'device_type': 'IOSv'})
ok: [localhost] => (item={'name': 'msp-rtr01', 'site': 'MSP', 'device_role': 'Router', 'device_type': 'IOSv'})

PLAY RECAP ********************************************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


```

Now that you have some devices, you can start to do a little bit more with your NetBox environment. This playbook purposely did not add more information about the device yet, such as the serial number, interfaces, or IP addressing. This is all information that you can add more about the device as well using Ansible Facts and Resource Modules to continue to develop your source of truth. More likely to come in the future, or you can check out the content on GitHub and YouTube referenced above for immediate reference.

## Summary

Getting devices into NetBox provides a powerful place to put your source of truth for automation. It does take a small bit to get to a good place, but with a little bit of effort up front you can get things done in a **consistent** and **repeatable** fashion. No more having to do things by hand with the data points.  

Hope this has helped. If so, let me know with a comment below or give a thumbs up on the post.
