---
date: 2020-11-29
layout: single
slug: netbox-ansible-inventory_plugin
title: 'NetBox Ansible Collection: Inventory - Starting Out'
collections:
- netbox_ansible_collection
categories:
- netbox
- ansible
toc: true
author: jvanderaa
params:
  showComments: true
---

The documentation can be found on [ReadTheDocs](https://netbox-ansible-collection.readthedocs.io/en/latest/plugins/inventory/nb_inventory/netbox.netbox.nb_inventory_inventory.html). This is going to be starting out with the basics of the plugin and getting some sample output and to show how to form groups to be used.

<!--more-->

{{< alert "neutral" >}}
This post was created when NetBox was an open source project used often in my automation framework. I have moved on to using [Nautobot](https://www.nautobot.com) due to the project vision and providing a methodology that will drive network automation forward further. You may want to take a look at it yourself.


{{< /alert >}}
> This particular plugin **DOES NOT** require pynetbox to be used. 

Late addition: You can see a corresponding video on YouTube:

<div style="position: relative; padding-bottom: 56.25%; height: 0;">
  <iframe src="https://www.youtube.com/embed/3NRbIpH5G5Q" 
          style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" 
          frameborder="0" 
          allowfullscreen>
  </iframe>
</div>

## Purpose

The purpose of the NetBox Inventory plugin is to provide an inventory to use within your Ansible automations. The plugin will gather information from NetBox and from the data create groups and an inventory for use by Ansible.

## Install

Please checkout the first post in the series for the [getting started / installation](https://www.josh-v.com/netbox_ansible_collection/collection_install/) process. 

## Environment

For this demo, as there are many pieces of information brought back by the inventory I have reduced the inventory to two hosts. 

Here are the rest of the installation versions:

| Component                 | Version                                                                     |
| ------------------------- | --------------------------------------------------------------------------- |
| NetBox                    | v2.9.9 [(NetBox Docker)](https://github.com/netbox-community/netbox-docker) |
| NetBox Ansible Collection | v1.1.0                                                                      |
| pynetbox                  | Not required - Not installed                                                |

## Basic Setup - No Groups

First a good practice for working on systems is to use environment variables to define the server and secret information within the environment. The environment has been configured with for this demo are:

| Environment Variable Name | What is in the variable                                 |
| ------------------------- | ------------------------------------------------------- |
| NETBOX_API                | API URL for NetBox such as `http://netbox.example.com`  |
| NETBOX_TOKEN              | API Token set inside of NetBox Admin -> Admin -> Tokens |

From the documentation these variables if not defined in the inventory YAML file that the plugin will search for the values to be in the environment with *NETBOX_API* and *NETBOX_TOKEN*. This allows you to share the inventory file to be shared across multiple NetBox environments, all based on the environment.

You configure the inventory with a YAML file that references the plugin. Here is the starting point to verify that we can get data from NetBox into an inventory before we add some of the filtering and groupings. 

```yaml
# netbox_inventory.yml
---
plugin: netbox.netbox.nb_inventory
validate_certs: false
config_context: false
```

What is being done here:

| Line Number | Key            | Value                                                                                                                                                                               |
| ----------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2           | plugin         | Which inventory plugin to be used, the FQCN of `netbox.netbox.nb_inventory`                                                                                                         |
| 3           | validate_certs | If TLS is configured, then the certificates will not be validated.                                                                                                                  |
| 4           | config_context | This is important on large NetBox environments. Setting `config_context` to false tells the API to not return the config_context field, reducing the amount of data being returned. |

Alternatively if you do not define the items in the environment, then you would add the keys into the file, such that it looks like below. The rest of the post will assume that the items are configured in the environment.

```yaml
# netbox_inventory.yml
---
plugin: netbox.netbox.nb_inventory
api_endpoint: http://netbox.example.com
token: <API_TOKEN here>
validate_certs: false
config_context: false
```

### Basic Setup Result

When executing the inventory `ansible-inventory -i netbox_inventory.yml`. This example the file name is netbox_inventory.yml. This is completely arbitrary. You can name the inventory any file you wish. Most likely you should name it something that relates to the inventory you are creating. The result of the inventory gives the following:

```json {linenos=true}
{
    "_meta": {
        "hostvars": {
            "dcrtr001": {
                "ansible_host": "192.0.2.10",
                "custom_fields": {
                    "os_version": null
                "device_roles": [
                    "network"
                ],
                "device_types": [
                    "iosv"
                ],
                "is_virtual": false,
                "local_context_data": [
                    null
                ],
                "manufacturers": [
                    "cisco"
                ],
                "platforms": [
                    "cisco_ios"
                ],
                "primary_ip4": "192.0.2.10",
                "regions": [],
                "services": [],
                "sites": [
                    "site01"
                ],
                "tags": []
            },
            "wanrtr002": {
                "ansible_host": "10.10.0.2",
                "custom_fields": {
                    "os_version": null
                },
                "device_roles": [
                    "network"
                ],
                "device_types": [
                    "csr1000v"
                ],
                "is_virtual": false,
                "local_context_data": [
                    null
                ],
                "manufacturers": [
                    "cisco"
                ],
                "platforms": [
                    "cisco_ios"
                ],
                "primary_ip4": "10.10.0.2",
                "regions": [],
                "services": [],
                "sites": [
                    "site01"
                ],
                "tags": []
            }
        }
    },
    "all": {
        "children": [
            "ungrouped"
        ]
    },
    "ungrouped": {
        "hosts": [
            "dcrtr001",
            "wanrtr002"
        ]
    }
}
```

In this output, you get several components made available. First take notice on lines 62-74 at the bottom. This gives the groupings that will be made available. Since this is the basic query with no groupings defined, there is a single group of _ungrouped_. This is a child of the _all_ group. Which allows only hosts defined as all or the specific hostname.  

Taking a look at the hostvars that get assigned (lines 1-62), you get several host variables defined from the API call. Including the primary_ip4 address, device_role, an Ansible Host from the primary_ip4 address, and also the custom fields that are part of the NetBox environment.

## Groupings

Next up is adding some more context and adding groupings. This is done within your inventory YAML file with the key of *group_by*. There are several choices of what you can group objects by, including sites, tenants, tags, platforms, and many more. Take a look at the [documentation reference](https://netbox-ansible-collection.readthedocs.io/en/latest/plugins/inventory/nb_inventory/netbox.netbox.nb_inventory_inventory.html) for all of the options. Taking a look at having a grouping of by device_role, tags, sites, and platform gives the following additional groups: 

```yaml
# netbox_inventory_group_by.yml
---
plugin: netbox.netbox.nb_inventory
validate_certs: false
config_context: false
group_by:
  - device_roles
  - platforms
  - tags
  - sites
```

This now yields the following:

```json {linenos=true}
{
    "all": {
        "children": [
            "device_roles_network",
            "platforms_cisco_ios",
            "sites_datacenter01",
            "sites_site01",
            "tags_virtual",
            "ungrouped"
        ]
    },
    "device_roles_network": {
        "hosts": [
            "dcrtr001",
            "wanrtr002"
        ]
    },
    "platforms_cisco_ios": {
        "hosts": [
            "dcrtr001",
            "wanrtr002"
        ]
    },
    "sites_datacenter01": {
        "hosts": [
            "dcrtr001"
        ]
    },
    "sites_site01": {
        "hosts": [
            "wanrtr002"
        ]
    },
    "tags_virtual": {
        "hosts": [
            "dcrtr001"
        ]
    }
}
```

> This filtered out the hostvars as these are not changing.

There are now 5 additional groups showing up in the *all* group. And each of these have different hosts available for you to use in your playbooks. Now these are making sense and you can now have groupings for each of the items.

## Filtering Devices from NetBox

Next up is how do you filter hosts from the NetBox environment? That is done with *query_filters* key. From the documentation page: 

> List of parameters passed to the query string for both devices and VMs (Multiple values may be separated by commas)

In the testing I was not able to get multiple values on a status. This may need some clarification from the project.  

First search that was changed is that I moved `wanrtr002` to an offline state. Now when running the following inventory with a query filter status of active, the host is no longer in the grouping:

```yaml
# netbox_inventory_filtered.yml
---
plugin: netbox.netbox.nb_inventory
validate_certs: false
config_context: false
group_by:
  - device_roles
  - platforms
  - tags
  - sites
query_filters:
  - status: "active"
```

Looking at just the platforms_cisco_ios grouping, there is now a single device.

```json {linenos=true}
    "platforms_cisco_ios": {
        "hosts": [
            "dcrtr001"
        ]
    },
```

You can add additional queries to the query_filters key, such that status is listed twice. Once we add the second status then both devices show up again:

```yaml
query_filters:
  - status: "active"
  - status: "offline"
```

```json {linenos=true}
    "platforms_cisco_ios": {
        "hosts": [
            "dcrtr001",
            "wanrtr002"
        ]
    },
```

## Adding Variables

The method to add custom hostvars to your inventory from NetBox, is done with the *compose* parameter. From the documentation site:

> List of custom ansible host vars to create from the device object fetched from NetBox

THe first item that I use often with the compose parameter of the plugin is to set the `ansible_network_os` for a device. This is very helpful with a multi-vendor environment that allows you to run tasks against different network OS's. The final demonstration inventory YAML file is this:

```yaml
# netbox_inventory_all.yml
---
plugin: netbox.netbox.nb_inventory
validate_certs: false
config_context: false
group_by:
  - device_roles
  - platforms
  - tags
  - sites
query_filters:
  - status: "active"
  - status: "offline"
compose:
  ansible_network_os: platform.slug

```

With this modification the output shows the following hostvars with the groups unchanged. Notice specifically line 3 that there is now the *ansible_network_os* is set to *ios*, which will match the Ansible Network OS that Ansible will use. I just make sure that the slug for the Platform name matches that of the primary automation system.

```json {linenos=true}
"dcrtr001": {
    "ansible_host": "192.0.2.10",
    "ansible_network_os": "ios",
    "custom_fields": {
        "os_version": null
    },
    "device_roles": [
        "network"
    ],
    "device_types": [
        "iosv"
    ],
    "is_virtual": false,
    "local_context_data": [
        null
    ],
    "manufacturers": [
        "cisco"
    ],
    "platforms": [
        "cisco_ios"
    ],
    "primary_ip4": "192.0.2.10",
    "regions": [],
    "services": [],
    "sites": [
        "datacenter01"
    ],
    "tags": [
        "virtual"
    ]
},
```

## Summary

The NetBox Inventory Plugin for Ansible is quite powerful. It provides for methods to group your devices, filter on data points maintained within NetBox, and to create additional hostvars. The parameters for the plugin are quite extensive and you should take a look at what makes sense for your environment or needs within the Ansible playbooks. There are a few defaults that are set to no, such as *interfaces*, that helps keep the data provided at a proper level. You can add more information to the hostvars that you may use in the playbooks.  

I think the plugin is awesome and has a lot of work that has gone into it. There is likely even more to come as you go.