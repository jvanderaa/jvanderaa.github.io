---
author: Josh VanDeraa
date: 2020-12-12 08:00:00+00:00
layout: single
comments: true
slug: netbox-ansible-lookup-plugin
title: "NetBox Ansible Collection: Lookup Plugin"
collections:
  - netbox_ansible_collection
tags:
- netbox
- ansible
toc: true
---
The NetBox lookup plugin is to **get information** out of NetBox for use within Ansible. This uses [pynetbox](https://github.com/digitalocean/pynetbox) to query the NetBox API for the information requested. On top of being helpful in gathering data from NetBox (when it is not your inventory source), but it is extremely helpful in larger NetBox deployments when compared to using the URI module as well. If you wish to use NetBox as your inventory source, you should definitely read my previous post on getting started with the [NetBox Inventory Plugin](https://josh-v.com/netbox_ansible_collection/netbox-ansible-inventory_plugin/).


- [Read the Docs](https://netbox-ansible-collection.readthedocs.io/en/latest/plugins/lookup/nb_lookup/netbox.netbox.nb_lookup_lookup.html)
- [GitHub Source File](https://github.com/netbox-community/ansible_modules/blob/devel/plugins/lookup/nb_lookup.py)
- [Installing the Colleciton](https://josh-v.com/netbox_ansible_collection/collection_install/)

> The recommended Jinja function to use with this lookup plugin is the `query` function. This tells Ansible that the result of the lookup should be a type list. The same behavior is also available by using the `lookup` function, in conjunction with the parameter `wantlist=true`. For this post we will use the `query` method.

{{< alert "circle-info" >}}
This post was created when NetBox was an open source project used often in my automation framework. I have moved on to using [Nautobot](https://www.nautobot.com) due to the project vision and providing a methodology that will drive network automation forward further. You may want to take a look at it yourself.
{{< /alert >}}

## Methodology

My methodology for gathering this information is that the plugin is looking to get the Django application (Sites, Devices, IPAM)

## Environment

For this demo, here are the versions shown:

| Component                 | Version                                                                     |
| ------------------------- | --------------------------------------------------------------------------- |
| NetBox                    | v2.9.9 [(NetBox Docker)](https://github.com/netbox-community/netbox-docker) |
| NetBox Ansible Collection | v1.1.0                                                                      |
| pynetbox                  | 5.1.0                                                                       |

## Query Plugin Note

So I was originally trying to use the Jinja variable template when I was working with the plugin. The query function does not need the templating language (wrapped in `{{ }}`). The variable name _should_ be used without the wrapping and just work.

## Parameter: Terms

The parameter `_terms` as I can understand relates to which end point within the pynetbox endpoint is being referenced. Digging into the code itself, I have found that the following is the available endpoints:

| Lookup Endpoint                | Corresponding pynetbox endpoint           |
| ------------------------------ | ----------------------------------------- |
| aggregates                     | netbox.ipam.aggregates                    |
| circuit-terminations           | netbox.circuits.circuit_terminations      |
| circuit-types                  | netbox.circuits.circuit_types             |
| circuits                       | netbox.circuits.circuits                  |
| circuit-providers              | netbox.circuits.providers                 |
| cables                         | netbox.dcim.cables                        |
| cluster-groups                 | netbox.virtualization.cluster_groups      |
| cluster-types                  | netbox.virtualization.cluster_types       |
| clusters                       | netbox.virtualization.clusters            |
| config-contexts                | netbox.extras.config_contexts             |
| console-connections            | netbox.dcim.console_connections           |
| console-ports                  | netbox.dcim.console_ports                 |
| console-server-port-templates" | netbox.dcim.console_server_port_templates |
| console-server-ports           | netbox.dcim.console_server_ports          |
| device-bay-templates           | netbox.dcim.device_bay_templates          |
| device-bays                    | netbox.dcim.device_bays                   |
| device-roles                   | netbox.dcim.device_roles                  |
| device-types                   | netbox.dcim.device_types                  |
| devices                        | netbox.dcim.devices                       |
| export-templates               | netbox.dcim.export_templates              |
| front-port-templates           | netbox.dcim.front_port_templates          |
| front-ports                    | netbox.dcim.front_ports                   |
| graphs                         | netbox.extras.graphs                      |
| image-attachments              | netbox.extras.image_attachments           |
| interface-connections          | netbox.dcim.interface_connections         |
| interface-templates            | netbox.dcim.interface_templates           |
| interfaces                     | netbox.dcim.interfaces                    |
| inventory-items                | netbox.dcim.inventory_items               |
| ip-addresses                   | netbox.ipam.ip_addresses                  |
| manufacturers                  | netbox.dcim.manufacturers                 |
| object-changes                 | netbox.extras.object_changes              |
| platforms                      | netbox.dcim.platforms                     |
| power-connections              | netbox.dcim.power_connections             |
| power-outlet-templates         | netbox.dcim.power_outlet_templates        |
| power-outlets                  | netbox.dcim.power_outlets                 |
| power-port-templates           | netbox.dcim.power_port_templates          |
| power-ports                    | netbox.dcim.power_ports                   |
| prefixes                       | netbox.ipam.prefixes                      |
| rack-groups                    | netbox.dcim.rack_groups                   |
| rack-reservations              | netbox.dcim.rack_reservations             |
| rack-roles                     | netbox.dcim.rack_roles                    |
| racks                          | netbox.dcim.racks                         |
| rear-port-templates            | netbox.dcim.rear_port_templates           |
| rear-ports                     | netbox.dcim.rear_ports                    |
| regions                        | netbox.dcim.regions                       |
| reports                        | netbox.extras.reports                     |
| rirs                           | netbox.ipam.rirs                          |
| roles                          | netbox.ipam.roles                         |
| secret-roles                   | netbox.secrets.secret_roles               |
| secrets                        | netbox.secrets.secrets                    |
| services                       | netbox.ipam.services                      |
| sites                          | netbox.dcim.sites                         |
| tags                           | netbox.extras.tags                        |
| tenant-groups                  | netbox.tenancy.tenant_groups              |
| tenants                        | netbox.tenancy.tenants                    |
| topology-maps                  | netbox.extras.topology_maps               |
| virtual-chassis                | netbox.dcim.virtual_chassis               |
| virtual-machines               | netbox.virtualization.virtual_machines    |
| virtualization-interfaces      | netbox.virtualization.interfaces          |
| vlan-groups                    | netbox.ipam.vlan_groups                   |
| vlans                          | netbox.ipam.vlans                         |
| vrfs                           | netbox.ipam.vrfs                          |

## Examples

The goal is to really dig into the examples to see how it is used. Let's get right to it. For these demos I am using the following definitions for the Play:

```yaml
---
- name: "GATHER DATA FROM NETBOX"
  hosts: localhost
  connection: local
  gather_facts: no
  vars:
    netbox_url: "{{ lookup('env', 'NETBOX_API') }}"
    netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"

```

Of note, the URL and token are embedded into the environment. To maintain consistency with the NetBox Inventory plugin I am mapping `NETBOX_API` to be the netbox_url. At this moment of writing the lookup plugin does not natively lookup the environment like the other modules do. I do intended to submit a [PR](https://github.com/netbox-community/ansible_modules/pull/391) to update this.

### Gathering Sites

When taking a look at gathering sites the following task is used:

```yaml
- name: "TASK 1: GET SITES WITH NB_QUERY"
  set_fact:
    sites: "{{ query('netbox.netbox.nb_lookup', 'sites', api_endpoint=netbox_url, token=netbox_token) }}"

- name: "TASK 2: PRINT JUST THE SITE NAMES"
  debug:
    msg: "{{ sites | json_query('[*].value.name') }}"

```

#### Gathering Sites: TASK 1 Output

Lines 1-3 are the collecting of data from NetBox itself. In my NetBox demo environment I currently have 4 sites. Instead of giving you the entire output that is quite long, below is that output. Note that there is a bunch of information available to you about each site here.

{{< highlight yaml "linenos=table" >}}

   - key: 6
      value:
        asn: null
        circuit_count: null
        comments: ''
        contact_email: ''
        contact_name: ''
        contact_phone: ''
        created: '2020-12-06'
        custom_fields: {}
        description: Portland
        device_count: 3
        facility: ''
        id: 6
        last_updated: '2020-12-06T15:29:45.112426Z'
        latitude: null
        longitude: null
        name: PDX
        physical_address: ''
        prefix_count: null
        rack_count: null
        region: null
        shipping_address: ''
        slug: pdx
        status:
          label: Active
          value: active
        tags: []
        tenant: null
        time_zone: America/Los_Angeles
        url: http://netbox-demo/api/dcim/sites/6/
        virtualmachine_count: null
        vlan_count: null

{{< /highlight>}}

#### Gathering Sites: TASK 2 Output - Getting Just the Site Names

I used json_query (which uses JMESPATH) to get just the site names. I see a future post on this coming in the future. The result of this gives me the output of just the four sites and not the rest of the data:

{{< highlight yaml "linenos=table" >}}

ok: [localhost] => 
  msg:
  - DEN
  - MSP
  - NYC
  - PDX


{{< /highlight>}}

### Get Devices - Filtered to a single site

You can then filter with the lookup plugin as well. In these two tasks I'm going to filter and get the devices that are located at the DEN site. Task 3 you add the `api_filter` to the plugin definition on the set_fact. The API filters are key/value and are separated with a space inside of the string to have multiple searches. If you wish to search multiple sites or multiple roles (or multiple anything) then you add a second instance of it. The value of the key/value pair is the corresponding **slug** associated with the search.  

```yaml
- name: "TASK 3: GET DEVICES WITH ROLE ROUTER AT DEN SITE"
  set_fact:
    den_devices: "{{ query('netbox.netbox.nb_lookup', 'devices', api_filter='site=den role=router', api_endpoint=netbox_url, token=netbox_token) }}"

- name: "TASK 4: PRINT THE DEVICES"
  debug:
    msg: "{{ den_devices | json_query('[*].value.name') }}"

```

#### Getting Denver Routers Output

The output from these two tasks where there is a single router device at the site Denver is then the following output with the single device on line 77.

{{< highlight yaml "linenos=table" >}}

TASK [TASK 3: GET ROLE ROUTERS AT DEN SITE] **************************************************************************************************************************
  ansible_facts:
    den_devices:
    - key: 4
      value:
        asset_tag: null
        cluster: null
        comments: ''
        config_context: {}
        created: '2020-12-06'
        custom_fields: {}
        device_role:
          id: 3
          name: Router
          slug: router
          url: http://netbox-demo/api/dcim/device-roles/3/
        device_type:
          display_name: Cisco IOSV
          id: 3
          manufacturer:
            id: 1
            name: Cisco
            slug: cisco
            url: http://netbox-demo/api/dcim/manufacturers/1/
          model: IOSV
          slug: iosv
          url: http://netbox-demo/api/dcim/device-types/3/
        display_name: den-wan01
        face: null
        id: 4
        last_updated: '2020-12-12T19:55:16.432666Z'
        local_context_data: null
        name: den-wan01
        parent_device: null
        platform:
          id: 2
          name: cisco_ios
          slug: ios
          url: http://netbox-demo/api/dcim/platforms/2/
        position: null
        primary_ip:
          address: 10.16.0.2/24
          family: 4
          id: 4
          url: http://netbox-demo/api/ipam/ip-addresses/4/
        primary_ip4:
          address: 10.16.0.2/24
          family: 4
          id: 4
          url: http://netbox-demo/api/ipam/ip-addresses/4/
        primary_ip6: null
        rack: null
        serial: 90Q1VEN47MPBMU2718KJ1
        site:
          id: 4
          name: DEN
          slug: den
          url: http://netbox-demo/api/dcim/sites/4/
        status:
          label: Active
          value: active
        tags:
        - color: 3f51b5
          id: 2
          name: snmp_monitoring
          slug: snmp_monitoring
          url: http://netbox-demo/api/extras/tags/2/
        tenant: null
        url: http://netbox-demo/api/dcim/devices/4/
        vc_position: null
        vc_priority: null
        virtual_chassis: null

TASK [TASK 4: PRINT THE DEVICES OF TYPE ROUTER AT DENVER LOCATION] ***************************************************************************************************
ok: [localhost] => 
  msg:
  - den-wan01


{{< /highlight>}}

#### Searching Multiple Locations

With this you are able to filter many things. To filter multiple sites, say you wanted to get the devices at both of the sites DEN and MSP. To do this you change the filter to be `site=den site=-msp`. Seeing this you get the following:

> I am only showing a single device corresponding to MSP & DEN site.

{{< highlight yaml "linenos=table" >}}

  ansible_facts:
    msp_den_devices:
    - key: 5
      value:
        asset_tag: null
        cluster: null
        comments: ''
        config_context: {}
        created: '2020-12-06'
        custom_fields: {}
        device_role:
          id: 2
          name: Network
          slug: network
          url: http://netbox-demo/api/dcim/device-roles/2/
        device_type:
          display_name: Cisco IOSV
          id: 3
          manufacturer:
            id: 1
            name: Cisco
            slug: cisco
            url: http://netbox-demo/api/dcim/manufacturers/1/
          model: IOSV
          slug: iosv
          url: http://netbox-demo/api/dcim/device-types/3/
        display_name: den-dist01
        face: null
        id: 5
        last_updated: '2020-12-06T17:16:02.266041Z'
        local_context_data: null
        name: den-dist01
        parent_device: null
        platform:
          id: 2
          name: cisco_ios
          slug: ios
          url: http://netbox-demo/api/dcim/platforms/2/
        position: null
        primary_ip:
          address: 10.17.1.2/30
          family: 4
          id: 5
          url: http://netbox-demo/api/ipam/ip-addresses/5/
        primary_ip4:
          address: 10.17.1.2/30
          family: 4
          id: 5
          url: http://netbox-demo/api/ipam/ip-addresses/5/
        primary_ip6: null
        rack: null
        serial: 9ZYX8XZUMP0AF69YGO5Z5
        site:
          id: 4
          name: DEN
          slug: den
          url: http://netbox-demo/api/dcim/sites/4/
        status:
          label: Active
          value: active
        tags:
        - color: 3f51b5
          id: 2
          name: snmp_monitoring
          slug: snmp_monitoring
          url: http://netbox-demo/api/extras/tags/2/
        tenant: null
        url: http://netbox-demo/api/dcim/devices/5/
        vc_position: null
        vc_priority: null
        virtual_chassis: null


{{< /highlight>}}

Here is the result of Task 6, which is the list of the devices:

{{< highlight yaml "linenos=table" >}}

TASK [TASK 6: PRINT THE DEVICES AT DEN & MSP LOCATIONS] **************************************************************************************************************
ok: [localhost] => 
  msg:
  - den-dist01
  - den-dist02
  - den-wan01
  - msp-dist01
  - msp-dist02
  - msp-wan01


{{< /highlight>}}

## Working With Large Data Sets

One may say that I can just get the data from using the URI module from Ansible. I've been there as well on this. One of the larger draws of using the lookup plugin is the ability to handle pagination of the results natively. Consider the following task, where I have changed the `MAX_PAGE_SIZE` environment variable to 2 in order to demonstrate the paging setup.

```yaml
- name: "TASK 7: GET DATA FROM NETBOX VIA THE REST API"
  uri:
    url: "{{ lookup('env', 'NETBOX_URL') }}/api/dcim/devices/?site=den&limit=2"
    method: "GET"
    headers:
      Content-Type: "application/json"
      Authorization: "token {{ lookup('env', 'NETBOX_TOKEN') }}"
    status_code: 200
  register: search_result

- name: "TASK 8: PRINT LENGTH OF PAGED SETUP"
  debug:
    msg:
      - "Length of result on paginated response: {{ search_result['json']['results'] | length }}"
      - "Total results (if no paging): {{ search_result['json']['count'] }}"

```

Task 7 gets the data, and looking at the response data coming back we can see that there is a second page by the **next** field:

{{< highlight yaml "linenos=table" >}}

  json:
    count: 3
    next: http://netbox-demo/api/dcim/devices/?limit=2&offset=2&site=den
    previous: null
    results:


{{< /highlight>}}

Task 8 then confirms this for us:

{{< highlight yaml "linenos=table" >}}

  msg:
  - 'Length of result on paginated response: 2'
  - 'Total results (if no paging): 3'


{{< /highlight>}}

This is where leveraging pynetbox under the hood and it handling the pagination will be helpful. Some day there may be an Ansible module that handles API calls and combines the results on multiple responses. But today one would need to add a fair amount of logic handling into a Playbook execution to handle pagination.  

The result is handling the paging in the task and makes the life very easy to get data from NetBox with it!

{{< highlight yaml "linenos=table" >}}

TASK [TASK 10: PRINT THE DEVICES AT DEN LOCATION] ********************************************************************************************************************
ok: [localhost] => 
  msg:
  - den-dist01
  - den-dist02


{{< /highlight>}}

## Summary

The lookup plugin from the NetBox Ansible Content Collection is a great tool to help get your NetBox search data into your Ansible Playbooks. You can filter as needed, and you get the data into a format that you can then use!

## Final Playbook

Since there were a lot of demos in here, below is the final playbook. In the environment are the NETBOX variables that you set the environment variables and you can use this same playbook to get started. Just make the updates as needed!

```yaml
---
- name: "GATHER DATA FROM NETBOX"
  hosts: localhost
  connection: local
  gather_facts: no
  vars:
    netbox_url: "{{ lookup('env', 'NETBOX_API') }}"
    netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
  tasks:
    - name: "GET SITES WITH NB_QUERY"
      set_fact:
        sites: "{{ query('netbox.netbox.nb_lookup', 'sites', api_endpoint=netbox_url, token=netbox_token) }}"

    - debug:
        msg: "{{ sites | json_query('[*].value.name') }}"

    - name: "TASK 3: GET ROLE ROUTERS AT DEN SITE"
      set_fact:
        den_devices: "{{ query('netbox.netbox.nb_lookup', 'devices', api_filter='site=den role=router', api_endpoint=netbox_url, token=netbox_token) }}"

    - name: "TASK 4: PRINT THE DEVICES OF TYPE ROUTER AT DENVER LOCATION"
      debug:
        msg: "{{ den_devices | json_query('[*].value.name') }}"

    - name: "TASK 5: GET DEVICES AT DEN & MSP SITES"
      set_fact:
        msp_den_devices: "{{ query('netbox.netbox.nb_lookup', 'devices', api_filter='site=den site=msp', api_endpoint=netbox_url, token=netbox_token) }}"

    - name: "TASK 6: PRINT THE DEVICES AT DEN & MSP LOCATIONS"
      debug:
        msg: "{{ msp_den_devices | json_query('[*].value.name') }}"

    - name: "TASK 7: GET DATA FROM NETBOX VIA THE REST API"
      uri:
        url: "{{ lookup('env', 'NETBOX_URL') }}/api/dcim/devices/?site=den"
        method: "GET"
        headers:
          Content-Type: "application/json"
          Authorization: "token {{ lookup('env', 'NETBOX_TOKEN') }}"
        status_code: 200
      register: search_result

    - name: "TASK 8: PRINT LENGTH OF PAGED SETUP"
      debug:
        msg:
          - "Length of result on paginated response: {{ search_result['json']['results'] | length }}"
          - "Total results (if no paging): {{ search_result['json']['count'] }}"

    - name: "TASK 9: GET DEVICES AT DEN SITE"
      set_fact:
        den_devices: "{{ query('netbox.netbox.nb_lookup', 'devices', api_filter='site=den', api_endpoint=netbox_url, token=netbox_token) }}"

    - name: "TASK 10: PRINT THE DEVICES AT DEN LOCATION"
      debug:
        msg: "{{ den_devices | json_query('[*].value.name') }}"

```

Let me know your thoughts below! Like it if you have found it valuable.

Josh