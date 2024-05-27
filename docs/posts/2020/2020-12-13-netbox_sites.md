---
authors: [jvanderaa]
date: 2020-12-13
layout: single
comments: true
slug: netbox-ansible-sites
title: "NetBox Ansible Collection: Site Module"
collections:
  - netbox_ansible_collection
categories:
- netbox
- ansible
toc: true
---
This post dives into the [NetBox Ansible Content Collection](https://netbox-ansible-collection.readthedocs.io/en/latest/) module to create/update a [Site](https://netbox-ansible-collection.readthedocs.io/en/latest/plugins/modules/netbox_site/netbox.netbox.netbox_site_module.html). As I start into this series on looking at the modules that create/update/delete data from NetBox, the question that I keep asking myself is should I be looking at the modules that are creating/updating/deleting items? The reason that I ask this to myself is because I am a firm believer that automation should be coming from NetBox as its Source of Truth (SoT). You can hear/read plenty more about these thoughts on posts and videos here:

- [Minneapolis Ansible Meetup April 2020 Talk](https://www.youtube.com/watch?v=GyQf5F0gr3w&t)
- [Ansible Guest Blog Post](https://www.ansible.com/blog/using-netbox-for-ansible-source-of-truth)

!!! note
    This post was created when NetBox was an open source project used often in my automation framework. I have moved on to using [Nautobot](https://www.nautobot.com) due to the project vision and providing a methodology that will drive network automation forward further. You may want to take a look at it yourself.


When it comes to creating and deleting sites in NetBox, this one is an easy one. In my opinion this is a **yes it should be**. Most likely an IT tool is not the tool that will be the Source of Truth as it comes to physical sites. So this module in particualr that should be looked at and put into production use with Ansible.

## Environment

For this demo, here are the versions shown:

| Component                 | Version                                                                     |
| ------------------------- | --------------------------------------------------------------------------- |
| NetBox                    | v2.9.9 [(NetBox Docker)](https://github.com/netbox-community/netbox-docker) |
| NetBox Ansible Collection | v1.1.0                                                                      |
| pynetbox                  | 5.1.0                                                                       |

## Site Module

Within NetBox, the site is the most basic unit, and is required for devices to be added. This is the first thing that you should do when creating a NetBox instance is to start to build out sites. There are a many set of parameters that you can add to your sites, but the minimum required are:

- name: The name of the site

Take a look at the [documentation](https://netbox-ansible-collection.readthedocs.io/en/latest/plugins/modules/netbox_site/netbox.netbox.netbox_site_module.html) for all of the additional parameters. The ones that stick out to me (and there are many more) include:

- asn: The BGP AS Number
- contact name & email: Site contact information
- physical and shipping addresses
- tags
- time_zone

## Examples

The point of these posts are to show examples and get you started. So let's get started. At the beginning of this there are going to be four sites that we can check out with the query function:

```yaml linenums="1"

TASK [05 - QUERY SITES] **********************************************************************************************************************************************
  ansible_facts:
    site_list_before:
    - DEN
    - MSP
    - NYC
    - PDX


```

The data here instead of coming from a system of record that has sites will come from a YAML file. So the first step would be to look at getting data from a data source that has sites. This could be a CRM tool if you were a MSP, or any other tooling that has your sites. Here is what the data would look like:

```yaml
---
sites:
  - name: MSP
    time_zone: America/Chicago
    status: active
    description: Minneapolis
  - name: DEN
    time_zone: America/Denver
    status: active
    description: Denver
  - name: NYC
    time_zone: America/New_York
    status: active
    description: New York
  - name: PDX
    time_zone: America/Los_Angeles
    status: active
    description: Portland

```

Running the following playbook multiple times will show that the module itself is idempotent in that it will not keep creating sites.

```yaml
---
- name: "SETUP SITES"
  hosts: localhost
  connection: local
  gather_facts: no
  tasks:
    - name: "05 - QUERY SITES"
      set_fact:
        site_list_before: "{{ query('netbox.netbox.nb_lookup', 'sites') | json_query('[*].value.name') }}"

    - name: "10 - SETUP SITES"
      netbox.netbox.netbox_site:
        netbox_url: "{{ lookup('env', 'NETBOX_URL') }}"
        netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
        data: "{{ site }}"
        state: present
        validate_certs: False
      loop: "{{ sites }}"
      loop_control:
        loop_var: site
        label: "{{ site['name'] }}"

```

The output below is from a second run. The sites for the current NetBox demo was originally deployed with this.

```yaml linenums="1"

TASK [05 - QUERY SITES] **********************************************************************************************
ok: [localhost] => changed=false 
  ansible_facts:
    site_list_before:
    - DEN
    - MSP
    - NYC
    - PDX

TASK [10 - SETUP SITES] **********************************************************************************************
ok: [localhost] => (item=MSP) => changed=false 
  ansible_loop_var: site
  msg: site MSP already exists
  site:
    description: Minneapolis
    name: MSP
    status: active
    time_zone: America/Chicago
ok: [localhost] => (item=DEN) => changed=false 
  ansible_loop_var: site
  msg: site DEN already exists
  site:
    description: Denver
    name: DEN
    status: active
    time_zone: America/Denver
ok: [localhost] => (item=NYC) => changed=false 
  ansible_loop_var: site
  msg: site NYC already exists
  site:
    description: New York
    name: NYC
    status: active
    time_zone: America/New_York
ok: [localhost] => (item=PDX) => changed=false 
  ansible_loop_var: site
  msg: site PDX already exists
  site:
    description: Portland
    name: PDX
    status: active
    time_zone: America/Los_Angeles

PLAY RECAP ***********************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


```

In here we see that there were two tasks that showed **ok** and no tasks in the other sections of the play recap.

## Adding an additional site

The source for the sites just had a new site added. This is adding the Orlando location. As such the data now looks like this:

```yaml
---
sites:
  - name: MSP
    time_zone: America/Chicago
    status: active
    description: Minneapolis
  - name: DEN
    time_zone: America/Denver
    status: active
    description: Denver
  - name: NYC
    time_zone: America/New_York
    status: active
    description: New York
  - name: PDX
    time_zone: America/Los_Angeles
    status: active
    description: Portland
  - name: MCO
    time_zone: America/New_York
    status: active
    description: Orlando

```

With the new location, the Ansible Playbook is executed and we see a new site is added:

```yaml linenums="1"

TASK [05 - QUERY SITES] **********************************************************************************************
ok: [localhost] => changed=false 
  ansible_facts:
    site_list_before:
    - DEN
    - MSP
    - NYC
    - PDX

TASK [10 - SETUP SITES] **********************************************************************************************
ok: [localhost] => (item=MSP) => changed=false 
  ansible_loop_var: site
  msg: site MSP already exists
  site:
    description: Minneapolis
    name: MSP
    status: active
    time_zone: America/Chicago
ok: [localhost] => (item=DEN) => changed=false 
  ansible_loop_var: site
  msg: site DEN already exists
  site:
    description: Denver
    name: DEN
    status: active
    time_zone: America/Denver
ok: [localhost] => (item=NYC) => changed=false 
  ansible_loop_var: site
  msg: site NYC already exists
  site:
    description: New York
    name: NYC
    status: active
    time_zone: America/New_York
ok: [localhost] => (item=PDX) => changed=false 
  ansible_loop_var: site
  msg: site PDX already exists
  site:
    description: Portland
    name: PDX
    status: active
    time_zone: America/Los_Angeles
changed: [localhost] => (item=MCO) => changed=true 
  ansible_loop_var: site
  msg: site MCO created
  site:
    description: Orlando
    name: MCO
    status: active
    time_zone: America/New_York

PLAY RECAP ***********************************************************************************************************
localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


```

Taking a look at line 45 in this last execution you see the message **site MCO created**. This shows that it as created and there was a task that showed chagned in the play recap.

## Removing Sites

In this example for the removing of sites I am going to keep it a little bit more manual. I'm going to create a new variable in the `group_vars/all/sites.yml` file called `closed_sites`. So in this scenario the Orlando site was opened, but very quickly it was decided to close it down. So now we need to remove the site from NetBox. The `group_vars/all/sites.yml` now looks like below:

```yaml
---
sites:
  - name: MSP
    time_zone: America/Chicago
    status: active
    description: Minneapolis
  - name: DEN
    time_zone: America/Denver
    status: active
    description: Denver
  - name: NYC
    time_zone: America/New_York
    status: active
    description: New York
  - name: PDX
    time_zone: America/Los_Angeles
    status: active
    description: Portland
closed_sites:
  - name: MCO
    time_zone: America/New_York
    status: active
    description: Orlando

```

The updated Ansible Playbook now needs to remove any sites that are showing up in the closed sites:

```yaml
---
- name: "SETUP SITES"
  hosts: localhost
  connection: local
  gather_facts: no
  tasks:
    - name: "05 - QUERY SITES"
      set_fact:
        site_list_before: "{{ query('netbox.netbox.nb_lookup', 'sites') | json_query('[*].value.name') }}"

    - name: "10 - SETUP SITES"
      netbox.netbox.netbox_site:
        netbox_url: "{{ lookup('env', 'NETBOX_URL') }}"
        netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
        data: "{{ site }}"
        state: present
        validate_certs: False
      loop: "{{ sites }}"
      loop_control:
        loop_var: site
        label: "{{ site['name'] }}"

    - name: "20 - REMOVE CLOSED SITES"
      netbox.netbox.netbox_site:
        netbox_url: "{{ lookup('env', 'NETBOX_URL') }}"
        netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
        data: "{{ site }}"
        state: absent
        validate_certs: False
      loop: "{{ sites }}"
      loop_control:
        loop_var: site
        label: "{{ site['name'] }}"

    - name: "25 - QUERY SITES AT END"
      set_fact:
        site_list_end: "{{ query('netbox.netbox.nb_lookup', 'sites') | json_query('[*].value.name') }}"

    - name: "30 - SHOW RESULTS"
      debug:
        msg:
          - "{{ site_list_before }}"
          - "{{ site_list_end }}"

```

The result of the playbook shows that we had the site at the beginning, then we were able to successfully remove it in Task 20 to remove the closed sites.

> When removing a site, you do need to make sure that all of the corresponding devices and other relationships are gone from the site. NetBox will not allow you to remove a site without it being empty first.

```yaml linenums="1"

TASK [05 - QUERY SITES] **********************************************************************************************
task path: /local/add_sites.yml:7
ok: [localhost] => changed=false 
  ansible_facts:
    site_list_before:
    - DEN
    - MCO
    - MSP
    - NYC
    - PDX

TASK [10 - SETUP SITES] **********************************************************************************************
task path: /local/add_sites.yml:11
ok: [localhost] => (item=MSP) => changed=false 
  ansible_loop_var: site
  msg: site MSP already exists
  site:
    description: Minneapolis
    name: MSP
    status: active
    time_zone: America/Chicago
ok: [localhost] => (item=DEN) => changed=false 
  ansible_loop_var: site
  msg: site DEN already exists
  site:
    description: Denver
    name: DEN
    status: active
    time_zone: America/Denver
ok: [localhost] => (item=NYC) => changed=false 
  ansible_loop_var: site
  msg: site NYC already exists
  site:
    description: New York
    name: NYC
    status: active
    time_zone: America/New_York
ok: [localhost] => (item=PDX) => changed=false 
  ansible_loop_var: site
  msg: site PDX already exists
  site:
    description: Portland
    name: PDX
    status: active
    time_zone: America/Los_Angeles

TASK [20 - REMOVE CLOSED SITES] **************************************************************************************
task path: /local/add_sites.yml:23
changed: [localhost] => (item=MCO) => changed=true 
  ansible_loop_var: site
  msg: site MCO deleted
  site:
    description: Orlando
    name: MCO
    status: active
    time_zone: America/New_York

TASK [25 - QUERY SITES AT END] ***************************************************************************************
task path: /local/add_sites.yml:35
ok: [localhost] => changed=false 
  ansible_facts:
    site_list_end:
    - DEN
    - MSP
    - NYC
    - PDX

TASK [30 - SHOW RESULTS] *********************************************************************************************
task path: /local/add_sites.yml:39
ok: [localhost] => 
  msg:
  - - DEN
    - MCO
    - MSP
    - NYC
    - PDX
  - - DEN
    - MSP
    - NYC
    - PDX
META: ran handlers
META: ran handlers

PLAY RECAP ***********************************************************************************************************
localhost                  : ok=5    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  


```

## Summary

This module is a very good module with a lot of options to get you started. This is absolutely a module that I would become familiar with as your organization is changing over time. This will allow you to keep your NetBox environment up to date with the site changes as you get new and closed sites alike. Hopefully this has been helpful to demonstrate it's capabities. Let me know your comments below, or give it a thumbs up if you have found this helpful.  

Thanks,

Josh