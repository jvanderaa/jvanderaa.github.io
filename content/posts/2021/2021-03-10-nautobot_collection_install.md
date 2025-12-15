---
date: 2021-03-10
layout: single
slug: collection_install
title: 'Nautobot Ansible Collection: Installation'
collections:
- nautobot_ansible_collection
categories:
- nautobot
- ansible
toc: true
author: jvanderaa
params:
  showComments: true
---

This is the first post as I shift into taking a closer look at the Nautobot Ansible Collection. The collection includes many of the needed modules to effectively manage your Nautobot environment. If  This will take a deeper dive into several of the components of the **inventory plugin**, but not all of the options. The documentation for all of the collection can be found at:

- ReadTheDocs: [https://nautobot-ansible.readthedocs.io](https://nautobot-ansible.readthedocs.io)
- Galaxy Page: [https://galaxy.ansible.com/networktocode/nautobot](https://galaxy.ansible.com/networktocode/nautobot)  

This post is going to give information on how to install the collection as it may be applicable to every post in the series (as they get posted).  

If you were a user of the NetBox Ansible Collection previously, you will notice a few differences. The first big difference in the modules is that there is no preface of nautobot_ before each module. Since this Collection is developed after Ansible 2.10 they are using the FQCN (Fully Qualified Collection Name), there is no longer the need to prefix the name to the module name. So where there was a netbox_device before it will now be just device, underneath the FQCN of `networktocode.nautobot.device` as an example.  

<!--more-->

## Installation

Installation is done via Ansible Galaxy. It is recommended to have the latest version of the collection when working on it as there are updates happening routinely. There is a **Python requirement** with many the modules of the [pynautobot](https://pynautobot.readthedocs.io) Python package.  

It does not matter which order you install these in, you just need to install both before you start using the module.

### Installation - pynautobot

To install you execute the following to get the latest version of pynautobot:

```shell
pip install pynautobot --upgrade
```

### Installation - Nautobot Collection

The collection is installed via Ansible Galaxy as a primary method to install. You can also install the collection manually from GitHub, but the galaxy method is the preferred method.

```shell
ansible-galaxy collection install networktocode.nautobot
```

If you add on `--force` at the end, Ansible Galaxy will install the latest version on top of what you may already have. If you already have a version of the collection installed, Galaxy will not overwrite what you already have.

## Verification of Installation

Once you have run the steps there are many ways to verify that the installation is completed successfully for the Python package. The one that I like to use is to execute a `pip freeze | grep <package_name>`. The execution looks like this on the current date:

```shell
pip3 freeze | grep pynautobot    
pynautobot==1.0.1
```

To verify that you have installed the Nautobot Ansible Collection, you can execute the Ansible Doc command to get the current documentation. This is done as followed with the device module to verify that the docs load:

```shell
ansible-doc networktocode.nautobot.device
```

If the module is not installed properly you will see, with a key in on the first line

```shell linenums="1"
$ ansible-doc networktocode.nautobot.device
[WARNING]: module networktocode.nautobot.device not found in:
/root/.ansible/plugins/modules:/usr/share/ansible/plugins/modules:/usr/local/lib/python3.7/site-packages/ansible/modules
```

When the collection is installed properly you will see the following output with the command:

```
> NETWORKTOCODE.NAUTOBOT.DEVICE    (/root/.ansible/collections/ansible_collections/networktocode/nautobot/plugins/modules/device.py)

        Creates, updates or removes devices from Nautobot

OPTIONS (= is mandatory):

= data
        Defines the device configuration

        type: dict

        SUBOPTIONS:

        - asset_tag
            Asset tag that is associated to the device
            [Default: (null)]
            type: str

        - cluster
            Cluster that the device will be assigned to
            [Default: (null)]
            type: raw

        - comments
            Comments that may include additional information in regards to the device
            [Default: (null)]
            type: str

        - custom_fields
            must exist in Nautobot
            [Default: (null)]
            type: dict

        - device_role
            Required if `state=present' and the device does not exist yet
            [Default: (null)]
            type: raw

        - device_type
            Required if `state=present' and the device does not exist yet
            [Default: (null)]
            type: raw

        - face
            Required if `rack' is defined
            (Choices: Front, front, Rear, rear)[Default: (null)]
            type: str

        - local_context_data
            Arbitrary JSON data to define the devices configuration variables.
            [Default: (null)]
            type: dict

        = name
            The name of the device

            type: str

        - platform
            The platform of the device
            [Default: (null)]
            type: raw

        - position
            The position of the device in the rack defined above
            [Default: (null)]
            type: int

        - primary_ip4
            Primary IPv4 address assigned to the device
            [Default: (null)]
            type: raw

        - primary_ip6
            Primary IPv6 address assigned to the device
            [Default: (null)]
            type: raw

        - rack
            The name of the rack to assign the device to
            [Default: (null)]
            type: raw

        - serial
            Serial number of the device
            [Default: (null)]
            type: str

        - site
            Required if `state=present' and the device does not exist yet
            [Default: (null)]
            type: raw

        - status
            The status of the device
            [Default: (null)]
            type: raw

        - tags
            Any tags that the device may need to be associated with
            [Default: (null)]
            type: list

        - tenant
            The tenant that the device will be assigned to
            [Default: (null)]
            type: raw

        - vc_position
            Position in the assigned virtual chassis
            [Default: (null)]
            type: int

        - vc_priority
            Priority in the assigned virtual chassis
            [Default: (null)]
            type: int

        - virtual_chassis
            Virtual chassis the device will be assigned to
            [Default: (null)]
            type: raw

- query_params
        This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
        in plugins/module_utils/utils.py and provides control to users on what may make
        an object unique in their environment.
        [Default: (null)]
        elements: str
        type: list

- state
        Use `present' or `absent' for adding or removing.
        (Choices: absent, present)[Default: present]
        type: str

= token
        The token created within Nautobot to authorize API access

        type: str

= url
        URL of the Nautobot instance resolvable by Ansible control host

        type: str

- validate_certs
        If `no', SSL certificates will not be validated. This should only be used on personally
        controlled sites using self-signed certificates.
        [Default: True]
        type: raw


NOTES:
      * Tags should be defined as a YAML list
      * This should be ran with connection `local' and hosts `localhost'


REQUIREMENTS:  pynautobot

AUTHOR: Network to Code (@networktocode), David Gomez (@amb1s1)

METADATA:
  metadata_version: '1.1'
  status:
  - preview
  supported_by: community


VERSION_ADDED_COLLECTION: networktocode.nautobot

EXAMPLES:

- name: "Test Nautobot modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create device within Nautobot with only required information
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Device
          device_type: C9410R
          device_role: Core Switch
          site: Main
          status: active
        state: present

    - name: Create device within Nautobot with empty string name to generate UUID
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: ""
          device_type: C9410R
          device_role: Core Switch
          site: Main
          status: active
        state: present

    - name: Delete device within nautobot
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Device
        state: absent

    - name: Create device with tags
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Another Test Device
          device_type: C9410R
          device_role: Core Switch
          site: Main
          status: active
          local_context_data:
            bgp: "65000"
          tags:
            - Schnozzberry
        state: present

    - name: Update the rack and position of an existing device
      networktocode.nautobot.device:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          name: Test Device
          rack: Test Rack
          position: 10
          face: Front
        state: present


RETURN VALUES:
- device
        Serialized object as created or already existent within Nautobot

        returned: success (when `state=present')
        type: dict

- msg
        Message indicating failure or info about what has been achieved

        returned: always
        type: str
```

## Summary

Overall the process for getting going with this collection is two steps, of installing the Python dependency and installing the collection via Ansible Galaxy. With these done, you are on your way to using the Nautobot Ansible Collection in your environment.

## Up Next

- Ansible Inventory with Nautobot collection

