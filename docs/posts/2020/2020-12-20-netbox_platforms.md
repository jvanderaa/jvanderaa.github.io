---
authors: [jvanderaa]
date: 2020-12-20
layout: single
comments: true
slug: netbox-ansible-platforms
title: "NetBox Ansible Collection: Platforms"
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

Platforms are an optional item when adding devices into NetBox. The platform is the OS that you are going to be using. Most often this is used to help identify which driver your automation platform is going to be using. Specifically the slug of the platform is what needs to match. So in the terms of Ansible (since we are using Ansible to populate NetBox), you will want to set Cisco IOS devices to **ios**. By having the slug match the automation platform name you have that information in your inventory. For these reasons I strongly recommend setting the Platform for devices.

!!! note
    This post was created when NetBox was an open source project used often in my automation framework. I have moved on to using [Nautobot](https://www.nautobot.com) due to the project vision and providing a methodology that will drive network automation forward further. You may want to take a look at it yourself.


## Module Documentation

* [Read the Docs](https://netbox-ansible-collection.readthedocs.io/en/latest/plugins/netbox_platform_module.html)
* [GitHub](https://github.com/netbox-community/ansible_modules/blob/devel/plugins/modules/netbox_platform.py)

> This module **does** require [pynetbox](https://github.com/digitalocean/pynetbox) to execute properly

## Environment

For this demo, here are the versions shown:

| Component                 | Version                                                                     |
| ------------------------- | --------------------------------------------------------------------------- |
| NetBox                    | v2.9.9 [(NetBox Docker)](https://github.com/netbox-community/netbox-docker) |
| NetBox Ansible Collection | v1.1.0                                                                      |
| pynetbox                  | 5.1.0                                                                       |

## Data File

Now that you may want to have a different slug than what is displayed, the data structure is getting slightly more complex than the manufacturers file. There will be a list of dictionaries, where the dictionary has three keys: name, slug, and manufacturer.

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

### Example - Adding Devices

Getting started I already have a Cisco manufacturer included from a different demo. This will not hurt what is being demonstrated here. The task to add a manufacturer looks like:

```yaml
---
- name: "ADD PLATFORMS TO NETBOX"
  hosts: localhost
  connection: local
  gather_facts: false # No gathering facts about the container execution env
  tasks:
    - name: "05 - ADD PLATFORMS"
      netbox.netbox.netbox_platform:
        netbox_url: "{{ lookup('env', 'NETBOX_URL') }}"
        netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
        data:
          name: "{{ item['name'] }}"
      loop: "{{ platforms }}"
```

### Example - Execution

This execution shows that all of the platforms are added.

```yaml linenums="1"

josh-v@d27199d82bfc:~$ ansible-playbook add_platforms.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [ADD PLATFORMS TO NETBOX] ***********************************************************************************************************************

TASK [05 - ADD PLATFORMS] ****************************************************************************************************************************
changed: [localhost] => (item={'name': 'Arista EOS', 'slug': 'eos', 'manufacturer': 'Arista'})
changed: [localhost] => (item={'name': 'Cisco IOS', 'slug': 'ios', 'manufacturer': 'Cisco'})
changed: [localhost] => (item={'name': 'JUNOS', 'slug': 'junos', 'manufacturer': 'Juniper'})

PLAY RECAP *******************************************************************************************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


```

The second execution of playbook shows that with these three settings the module is idempotent:

```yaml linenums="1"

josh-v@d27199d82bfc:~$ ansible-playbook add_platforms.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [ADD PLATFORMS TO NETBOX] ***********************************************************************************************************************

TASK [05 - ADD PLATFORMS] ****************************************************************************************************************************
ok: [localhost] => (item={'name': 'Arista EOS', 'slug': 'eos', 'manufacturer': 'Arista'})
ok: [localhost] => (item={'name': 'Cisco IOS', 'slug': 'ios', 'manufacturer': 'Cisco'})
ok: [localhost] => (item={'name': 'JUNOS', 'slug': 'junos', 'manufacturer': 'Juniper'})

PLAY RECAP *******************************************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


```

Now you see all of them showing up in NetBox.

![NetBox Platforms After](/images/2020/12/platforms.png)

When editing the Cisco platform you see the result visually.

![NetBox Platform Edit Screen](/images/2020/12/platform_specific.png)

## Summary

Platforms are one of the items that you will strongly want to get updated into NetBox. By associating a device with a platform you can then use it in the inventory plugins to identify things such as the `ansible_network_os` dynamically. Need to have a new platform to test things with, just create a new platform, change a few settings, and the information is dynamically available within your playbooks.  

Hope this has helped. If so, let me know with a comment below or give a thumbs up on the post.
