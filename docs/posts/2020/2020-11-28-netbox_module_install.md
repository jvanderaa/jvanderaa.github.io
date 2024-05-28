---
authors: [jvanderaa]
date: 2020-11-28
layout: single
comments: true
slug: collection_install
title: "NetBox Ansible Collection: Installation"
collections:
  - netbox_ansible_collection
categories:
- netbox
- ansible
toc: true
---
This is the first post as I start to look at the NetBox Ansible Collection. This is an impressive collection with modules for several of the NetBox applications, a query plugin, and an inventory plugin. This will take a deeper dive into several of the components of the **inventory plugin**, but not all of the options. The documentation for all of the collection can be found at:

- ReadTheDocs: [https://netbox-ansible-collection.readthedocs.io/en/latest/](https://netbox-ansible-collection.readthedocs.io/en/latest/)
- Galaxy Page: [https://galaxy.ansible.com/netbox/netbox](https://galaxy.ansible.com/netbox/netbox)  

<!-- more -->

!!! note
    This post was created when NetBox was an open source project used often in my automation framework. I have moved on to using [Nautobot](https://www.nautobot.com) due to the project vision and providing a methodology that will drive network automation forward further. You may want to take a look at it yourself.


This post is going to give information on how to install the collection as it may be applicable to every post in the series (as they get posted).

(Update 2020-12-05)
The corresponding YouTube video is here:

<div style="position: relative; padding-bottom: 56.25%; height: 0;">
  <iframe src="https://www.youtube.com/embed/KjGwNRoBYU0" 
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
          frameborder="0" 
          allowfullscreen>
  </iframe>
</div>

## Installation

Installation is done via Ansible Galaxy. It is recommended to have the latest version of the collection when working on it as there are updates happening routinely. There is a **Python requirement** with the modules of the [pynetbox](https://github.com/digitalocean/pynetbox) package.  

It does not matter which order you install these in, you just need to install both before you start using the module.

### Installation - pynetbox

To install you execute the following to get the latest version of pynetbox:

```shell
pip install pynetbox --upgrade
```

### Installation - NetBox Collection

The collection is installed via Ansible Galaxy as a primary method to install. You can also install the collection manually from GitHub, but the galaxy method is the preferred method.

```shell
ansible-galaxy collection install netbox.netbox --force
```

The addition of `--force` will have Ansible Galaxy install the latest version on top of what you may already have. If you already have a version of the collection installed, Galaxy will not overwrite what you already have.

## Verification of Installation

Once you have run the steps there are many ways to verify that the installation is completed successfully for the Python package. The one that I like to use is to execute a `pip freeze | grep <package_name>`. The execution looks like this on the current date:

```shell
pip3 freeze | grep pynetbox    
pynetbox==5.1.0
```

To verify that you have installed the NetBox Ansible Collection, you can execute the Ansible Doc command to get the current documentation. This is done as followed with the netbox_device module to verify that the docs load:

```shell
ansible-doc netbox.netbox.netbox_device
```

If the module is not installed properly you will see, with a key in on the first line

```shell linenums="1"
[WARNING]: module netbox.netbox.netbox_inventory not found in:
~/.local/lib/python3.7/site-packages/ansible/modules
```
The output when I sent the stdout to a file is:

```
> NETBOX.NETBOX.NETBOX_DEVICE    (/Users/joshvanderaa/.ansible/collections/ansible_collections/netbox/netbox/plugins/modules/netbox_device.py)

        Creates, updates or removes devices from Netbox

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
            Comments that may include additional information in
            regards to the device
            [Default: (null)]
            type: str

        - custom_fields
            must exist in Netbox
            [Default: (null)]
            type: dict

        - device_role
            Required if `state=present' and the device does not exist
            yet
            [Default: (null)]
            type: raw

        - device_type
            Required if `state=present' and the device does not exist
            yet
            [Default: (null)]
            type: raw

        - face
            Required if `rack' is defined
            (Choices: Front, front, Rear, rear)[Default: (null)]
            type: str

        - local_context_data
            Arbitrary JSON data to define the devices configuration
            variables.
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
            Required if `state=present' and the device does not exist
            yet
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

= netbox_token
        The token created within Netbox to authorize API access

        type: str

= netbox_url
        URL of the Netbox instance resolvable by Ansible control host

        type: str

- query_params
        This can be used to override the specified values in
        ALLOWED_QUERY_PARAMS that is defined
        in plugins/module_utils/netbox_utils.py and provides control
        to users on what may make
        an object unique in their environment.
        [Default: (null)]
        elements: str
        type: list

- state
        Use `present' or `absent' for adding or removing.
        (Choices: absent, present)[Default: present]
        type: str

- validate_certs
        If `no', SSL certificates will not be validated. This should
        only be used on personally controlled sites using self-signed
        certificates.
        [Default: True]
        type: raw


NOTES:
      * Tags should be defined as a YAML list
      * This should be ran with connection `local' and hosts
        `localhost'


REQUIREMENTS:  pynetbox

AUTHOR: Mikhail Yohman (@FragmentedPacket), David Gomez (@amb1s1)

METADATA:
  metadata_version: '1.1'
  status:
  - preview
  supported_by: community


VERSION_ADDED_COLLECTION: netbox.netbox

EXAMPLES:

- name: "Test Netbox modules"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create device within Netbox with only required information
      netbox_device:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test Device
          device_type: C9410R
          device_role: Core Switch
          site: Main
        state: present

    - name: Create device within Netbox with empty string name to generate UUID
      netbox_device:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: ""
          device_type: C9410R
          device_role: Core Switch
          site: Main
        state: present

    - name: Delete device within netbox
      netbox_device:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test Device
        state: absent

    - name: Create device with tags
      netbox_device:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Another Test Device
          device_type: C9410R
          device_role: Core Switch
          site: Main
          local_context_data:
            bgp: "65000"
          tags:
            - Schnozzberry
        state: present

    - name: Update the rack and position of an existing device
      netbox_device:
        netbox_url: http://netbox.local
        netbox_token: thisIsMyToken
        data:
          name: Test Device
          rack: Test Rack
          position: 10
          face: Front
        state: present


RETURN VALUES:
- device
        Serialized object as created or already existent within Netbox

        returned: success (when `state=present')
        type: dict

- msg
        Message indicating failure or info about what has been
        achieved

        returned: always
        type: str
```

## Summary

Overall the process for getting going with this collection is two steps, of installing the Python dependency and installing the collection via Ansible Galaxy. With these done, you are on your way to using the NetBox Ansible Collection in your environment.

## Up Next

- [Ansible Inventory](https://www.josh-v.com/netbox_ansible_collection/netbox-ansible-inventory_plugin/)

