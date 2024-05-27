---
authors: [jvanderaa]
comments: true
date: 2023-06-05
slug: nautobot-ip-provisioning
categories:
- automation
- ansible
- nautobot
title: Nautobot IP Provisioning
toc: true
---

One of the great things about building an enterprise system, is being able to get systems to work cohesively amongst themselves to bring a complete solution. One of the workflows that is often required in a static IP address environment is the need to provide static IP addresses to hosts on a network segment. When using an IPAM (IP Address Management) solution such as Nautobot, the APIs and SDKs/modules made available for use in automation workflows is paramount to having the cohesion to make a seamless IT system. 

In this post I will be diving into the use of Nautobot as the IPAM. Using Ansible and the Nautobot modules, I will then show how you can get the next available IP address and assign it for use to the next VM. There will likely need to be some minor tweaks for use in your system.

<!-- more -->

## Nautobot Setup

The first action is to get Nautobot set up with the tags and prefixes that are going to be used. I am using a tag of `VM Addresses` to assign to Prefixes that are to be allowed to assign VM addresses to. This way, you can grab the specific prefix based on the Nautobot data, not being static. You may want to look at having some other tags as well and passing these items into the Ansible execution either from a UI Survey, ExtraVars, or having multiple instances of the playbook.

> This playbook is also using Environment Variables of `NAUTOBOT_URL` and `NAUTOBOT_TOKEN` in order to be able to be ported to other Nautobot systems.

```yaml
---
# create_parent_prefix.yml
- name: "SET UP PARENT PREFIX"
  hosts: localhost
  connection: local
  gather_facts: no
  vars:
    nautobot_url: "{{ lookup('ansible.builtin.env', 'NAUTOBOT_URL')}}"
    nautobot_token: "{{ lookup('ansible.builtin.env', 'NAUTOBOT_TOKEN')}}"
  tasks:
    - name: "100: CREATE A TAG FOR PARENT PREFIX OF VM ADDRESSING"
      networktocode.nautobot.tag:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        name: "VM Addresses"
        description: "Addresses for VMs to live in"

    - name: "200: SET UP PARENT PREFIXES FOR ALL REMOTE SITES"
      networktocode.nautobot.prefix:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        prefix: "{{ item }}"
        status: Active
        description: VM Addresses
        family: 4
        state: present
        tags:
          - VM Addresses
      loop:
        - "198.51.100.0/30"
        - "203.0.113.0/30"
        - "198.51.100.192/26"
```

The `loop` list could also become variables as well, which will allow even further dynamic capability. But this is just an example to do the work rather than having to set this in the UI and demo it. This set up method is much easier.

## Provisioning IP Addresses

Now that the Nautobot environment is set up with tags for the subnet, it is easy to write a playbook to get the prefixes that have the tag. Then from the prefixes that are available, check to see which prefix has available IP addresses. If there is one available, then go ahead and get that IP address and assign it for use.

This playbook is using GraphQL to query the data from Nautobot, this is the fastest way to gather data from Nautobot, using a filter on the prefixes tag `vm-addresses`. The `vm-addresses` is the slug of the Tag that is created in the first playbook execution.

```yaml
---
# get_and_set_next_available.yml
- name: "GET AND USE NEXT AVAILABLE ADDRESS"
  hosts: localhost
  connection: local
  gather_facts: no
  vars:
    nautobot_url: "{{ lookup('ansible.builtin.env', 'NAUTOBOT_URL')}}"
    nautobot_token: "{{ lookup('ansible.builtin.env', 'NAUTOBOT_TOKEN')}}"
    found_available_address: False
    graphql_query: |
      {
        prefixes(tag: "vm-addresses") {
          prefix
          id
        }
      }
  tasks:
    - name: "BLOCK: GET AND USE NEXT AVAILABLE IP, LIMIT TO SINGLE EXECUTION AT A TIME"
      block:
        - name: "100: GET PREFIXES AVAILABLE"
          networktocode.nautobot.query_graphql:
            url: "{{ nautobot_url }}"
            token: "{{ nautobot_token }}"
            query: "{{ graphql_query }}"
          register: query_response

        - debug:
            msg: "{{ query_response }}"

        - name: "200: FIND FIRST AVAILABLE IP ADDRESS"
          include_tasks: "find_available2.yml"
          loop: "{{ query_response['data']['prefixes'] }}"
          loop_control:
            index_var: "my_idx"
          when: not found_available_address


```

Task 100 executes the GraphQL query to get the response. From here the data has just what we need to continue on.

Task 200 executes the following tasks that are defined in the `find_available.yml` file. This is a separate file so that the group of tasks can be executed within a loop.

```yaml
# find_available.yml
---
- name: "debug var"
  debug:
    msg:
      - "{{ my_idx }}: ID={{ item['id'] }}, Prefix={{ item['prefix'] }}"
      - "{{ found_available_address }}"

- name: "300: GET NEXT AVAILABLE IP ADDRESS AND ASSIGN IT"
  networktocode.nautobot.ip_address:
    url: "{{ nautobot_url }}"
    token: "{{ nautobot_token }}"
    prefix: "{{ item['prefix'] }}"
    status: "Active"
    state: new
  register: nautobot_ip_state
  when: "not found_available_address" # A second when check to not keep assigning the IP address

- name: "310: ASSIGN found_available_address TO TRUE"
  ansible.builtin.set_fact:
    found_available_address: True
  when: nautobot_ip_state.changed

```

Task 300 uses the Ansible module `networktocode.nautobot.ip_address` to get the next available address in the prefix and registers it to the variable `nautobot_ip_state`. In Task 310 the `nautobot_ip_state` is checked to determined if the IP address has changed. If it has, it will set the variable `found_available_address` to `True`, so that the system knows that it no longer needs to check for an address because an address has been found and set.

The looping condition from Task 200 to keep going through the playbook allows for more tasks to be added on after Task 200 and then the 300 series tasks. If this playbook were to be done at this point and nothing further is to be executed you could change task 310 to be an `ansible.builtin.meta` task with the directive of `end_play` to stop the looping and the Play itself. That is how you would look to chain multiple plays together in a Playbook, that the first play of finding the address is completed and the next play of adding the business logic would take place.

Before the first execution, here is what Nautobot looks like without an address assigned:

![Nautobot no addresses](/images/2023/nautobot_no_ipaddresses.png)

The first execution of the playbook you get the following result:

```yaml
❯ ansible-playbook get_and_set_next_available.yml
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [GET AND USE NEXT AVAILABLE ADDRESS] ******************************************************************************************************

TASK [100: GET PREFIXES AVAILABLE] *************************************************************************************************************
ok: [localhost]

TASK [debug] ***********************************************************************************************************************************
ok: [localhost] => {
    "msg": {
        "changed": false,
        "data": {
            "prefixes": [
                {
                    "id": "819f71d5-d761-4011-a3d3-d61f9ea15fec",
                    "prefix": "198.51.100.0/30"
                },
                {
                    "id": "f23de4a0-7a5d-4921-9cbb-5f2da6eb419f",
                    "prefix": "198.51.100.192/26"
                },
                {
                    "id": "7c464ee3-1ce2-47c1-b1aa-5628ab421e83",
                    "prefix": "203.0.113.0/30"
                }
            ]
        },
        "failed": false,
        "graph_variables": null,
        "query": "{\n  prefixes(tag: \"vm-addresses\") {\n    prefix\n    id\n  }\n}\n",
        "url": "https://demo.nautobot.com"
    }
}

TASK [200: FIND FIRST AVAILABLE IP ADDRESS] ****************************************************************************************************
included: ./automationday_demos/find_available.yml for localhost => (item={'prefix': '198.51.100.0/30', 'id': '819f71d5-d761-4011-a3d3-d61f9ea15fec'})
included: ./automationday_demos/find_available.yml for localhost => (item={'prefix': '198.51.100.192/26', 'id': 'f23de4a0-7a5d-4921-9cbb-5f2da6eb419f'})
included: ./automationday_demos/find_available.yml for localhost => (item={'prefix': '203.0.113.0/30', 'id': '7c464ee3-1ce2-47c1-b1aa-5628ab421e83'})

TASK [debug var] *******************************************************************************************************************************
ok: [localhost] => {
    "msg": [
        "0: ID=819f71d5-d761-4011-a3d3-d61f9ea15fec, Prefix=198.51.100.0/30",
        false
    ]
}

TASK [300: GET NEXT AVAILABLE IP ADDRESS AND ASSIGN IT] ****************************************************************************************
ok: [localhost]

TASK [310: ASSIGN found_available_address TO TRUE] *********************************************************************************************
skipping: [localhost]

TASK [debug var] *******************************************************************************************************************************
ok: [localhost] => {
    "msg": [
        "1: ID=f23de4a0-7a5d-4921-9cbb-5f2da6eb419f, Prefix=198.51.100.192/26",
        false
    ]
}

TASK [300: GET NEXT AVAILABLE IP ADDRESS AND ASSIGN IT] ****************************************************************************************
changed: [localhost]

TASK [310: ASSIGN found_available_address TO TRUE] *********************************************************************************************
ok: [localhost]

TASK [debug var] *******************************************************************************************************************************
ok: [localhost] => {
    "msg": [
        "2: ID=7c464ee3-1ce2-47c1-b1aa-5628ab421e83, Prefix=203.0.113.0/30",
        true
    ]
}

TASK [300: GET NEXT AVAILABLE IP ADDRESS AND ASSIGN IT] ****************************************************************************************
skipping: [localhost]

TASK [310: ASSIGN found_available_address TO TRUE] *********************************************************************************************
skipping: [localhost]

PLAY RECAP *************************************************************************************************************************************
localhost                  : ok=11   changed=1    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0   
```

You can see on the first run of TASK 310 that the task has been skipped because there was not an available address (I purposely assigned addresses to fill up the first IP prefix space). The second loop through there was an IP address assigned and created. Then the last iteration skipped since the IP address was already assigned. Looking in the Nautobot UI, you now see an IP address assigned by the automation.

![Nautobot 1 IP address](/images/2023/nautobot_one_ip_address.png)

## Summary

Combining the power of Nautobot as your source of truth about network data with the tools that the systems teams are using such as Ansible provides for a powerful combination. The Nautobot ecosystem is continuing to grow and the amount of capabilities enabled by Nautobot is tremendous. In an upcoming post, I will put together a Nautobot Job that will be able to complete the same activity and allow for an API call to be made by systems if you are not leveraging Ansible in your environment today.

Let me know what you think on the social media at [LinkedIn](https://www.linkedin.com/in/josh-vanderaa/) or [Twitter](https://twitter.com/vanderaaj/).
