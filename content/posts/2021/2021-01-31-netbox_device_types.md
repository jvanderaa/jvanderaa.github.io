---
date: 2021-01-31
layout: single
slug: netbox-ansible-device-types
title: 'NetBox Ansible Collection: Device Types'
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

A device type is the next piece in the NetBox Device onboarding requirements. The device type corresponds to the model number of the hardware (or virtual machine). This is where you are able to template out devices during their creation. So if you have a console port on a device type, that console port will be created when you create the device. However, **there is NOT** a relationship built between the device type and the device. If the device type gets updated after the device is created, the device itself is **not** updated. 

{{< alert "neutral" >}}
This post was created when NetBox was an open source project used often in my automation framework. I have moved on to using [Nautobot](https://www.nautobot.com) due to the project vision and providing a methodology that will drive network automation forward further. You may want to take a look at it yourself.

{{< /alert >}}
<!--more-->

## Module Documentation

* [Read the Docs](https://netbox-ansible-collection.readthedocs.io/en/latest/plugins/netbox_device_type_module.html)
* [GitHub](https://github.com/netbox-community/ansible_modules/blob/devel/plugins/modules/netbox_device_type.py)

> This module **does** require [pynetbox](https://github.com/digitalocean/pynetbox) to execute properly

## Environment

For this demo, here are the versions shown:

| Component                 | Version                                                                     |
| ------------------------- | --------------------------------------------------------------------------- |
| NetBox                    | v2.9.9 [(NetBox Docker)](https://github.com/netbox-community/netbox-docker) |
| NetBox Ansible Collection | v1.1.0                                                                      |
| pynetbox                  | 5.1.0                                                                       |

## Data File

This gets to be a little more of the complex data source types. There are many data parameters that are good to include. The minimum data parameter has just the model. But there are going to be many more options as you build out your NetBox environment that feeds into the data correlation that makes NetBox a pleasure to use. Such as the manufacturer that it is tied to, the part number, and the u_height as you build rack diagrams from NetBox.  

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
- name: "ADD DEVICE TYPES TO NETBOX"
  hosts: localhost
  connection: local
  gather_facts: false # No gathering facts about the container execution env
  tasks:
    - name: "05 - ADD DEVICE TYPES"
      netbox.netbox.netbox_device_type:
        netbox_url: "{{ lookup('env', 'NETBOX_URL') }}"
        netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
        data:
          model: "{{ item['model'] }}"
          manufacturer: "{{ item['manufacturer'] }}"
          slug: "{{ item['slug'] }}"
          part_number: "{{ item['part_number'] }}"
      loop: "{{ device_types }}"

```

### Example - Execution

This execution shows that all of the device types are added.

```yaml {linenos=true}
josh-v@d27199d82bfc:~$ ansible-playbook add_devices.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [ADD DEVICE TYPES TO NETBOX] ********************************************************************************************************************

TASK [05 - ADD DEVICE TYPES] *************************************************************************************************************************
changed: [localhost] => (item={'model': 'ASAv', 'manufacturer': 'Cisco', 'slug': 'asav', 'part_number': 'asav'})
changed: [localhost] => (item={'model': 'CSR1000v', 'manufacturer': 'Cisco', 'slug': 'csr1000v', 'part_number': 'csr1000v'})
changed: [localhost] => (item={'model': 'IOSv', 'manufacturer': 'Cisco', 'slug': 'iosv', 'part_number': 'iosv'})
changed: [localhost] => (item={'model': 'nxosv', 'manufacturer': 'Cisco', 'slug': 'nxosv', 'part_number': 'nxosv'})
changed: [localhost] => (item={'model': 'vEOS', 'manufacturer': 'Arista', 'slug': 'veos', 'part_number': 'veos'})

PLAY RECAP *******************************************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  

```

The second execution of playbook shows that with these three settings the module is idempotent:

```yaml {linenos=true}
josh-v@d27199d82bfc:~$ ansible-playbook add_devices.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [ADD DEVICE TYPES TO NETBOX] ********************************************************************************************************************

TASK [05 - ADD DEVICE TYPES] *************************************************************************************************************************
ok: [localhost] => (item={'model': 'ASAv', 'manufacturer': 'Cisco', 'slug': 'asav', 'part_number': 'asav'})
ok: [localhost] => (item={'model': 'CSR1000v', 'manufacturer': 'Cisco', 'slug': 'csr1000v', 'part_number': 'csr1000v'})
ok: [localhost] => (item={'model': 'IOSv', 'manufacturer': 'Cisco', 'slug': 'iosv', 'part_number': 'iosv'})
ok: [localhost] => (item={'model': 'nxosv', 'manufacturer': 'Cisco', 'slug': 'nxosv', 'part_number': 'nxosv'})
ok: [localhost] => (item={'model': 'vEOS', 'manufacturer': 'Arista', 'slug': 'veos', 'part_number': 'veos'})

PLAY RECAP *******************************************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

After completion of this you will have the device types (hardware models) available for you to assign to devices (coming up next).

## Summary

Device types are important so you know what model of devices you have to work with. This will come in handy as well in your automations that if you have a particular device type that you need to do something against. Such as having a separate type for Cisco Catalyst 3750G vs Catalyst 3750X. They are all 3750 switches, however you may need to apply a unique configuration set against a particular device type. By having this predefined in your source of truth, you are all set to be able to run automations against each.  

Hope this has helped. If so, let me know with a comment below or give a thumbs up on the post.
