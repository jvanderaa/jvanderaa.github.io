---
authors: [jvanderaa]
toc: true
date: 2019-03-09
layout: single
comments: true
slug: ansible-ios-vlan
title: Ansible IOS VLAN
# collections:
#   - Cisco
#   - Ansible
# categories:
#   - Ansible
#   - Cisco Automation
tags:
  - ansible
  - ios_vlan
  - cisco
sidebar:
  nav: ansible
---
Back to it finally. Going to take a look at the Ansible module **ios_vlan**. The purpose of this is
to provide a declarative module for managing VLANs on IOS devices. In this I will be using IOSv-L2
images. There are a few interesting quirks (as I will call it) within the parameters for the module.

## Module Documentation

First, the module documentation page is
[here](https://docs.ansible.com/ansible/latest/modules/ios_vlan_module.html).

## Getting Started with the module

### VLANs pre-module work

Starting out the switch is pretty bare as it relates to the number of VLANs. There is VLAN2 defined
on the switch that has an uplink to the edge (of the lab) router. The base VLANs are the only other
ones on the device:

```yaml linenums="1"

#show vlan

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/1, Gi0/3, Gi1/0, Gi1/2
                                                Gi1/3
2    TRANSIT                          active    Gi0/0, Gi1/1
1002 fddi-default                     act/unsup 
1003 token-ring-default               act/unsup 
1004 fddinet-default                  act/unsup 
1005 trnet-default                    act/unsup 

VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
1    enet  100001     1500  -      -      -        -    -        0      0   
2    enet  100002     1500  -      -      -        -    -        0      0   
1002 fddi  101002     1500  -      -      -        -    -        0      0   
1003 tr    101003     1500  -      -      -        -    -        0      0   
1004 fdnet 101004     1500  -      -      -        ieee -        0      0   
1005 trnet 101005     1500  -      -      -        ibm  -        0      0   

Remote SPAN VLANs
------------------------------------------------------------------------------


Primary Secondary Type              Ports
------- --------- ----------------- ------------------------------------------


```

### Building the Play

The module has the following parameters, required ones in bold. This skips over the deprecated
parameters:

- aggregate: List of VLANs definitions
- associated_interfaces: Checks for the operational state of the interface
- delay: default to 10 seconds, how long to wait for the declarative state to be seen
- interfaces: a **list** of interfaces that should have the VLAN assigned to it
- name: Name of the VLAN
- purge: Purge VLANs not defined in the aggregate parameter
- state: present/absent/active/suspend - the state that it should be in
- vlan_id: ID of the VLAN

So what does aggregate mean? It sounds like that if you wanted to have a large list of VLANs, this
is the way to go with a task. First attempt at seeing what it does, the following playbook was setup

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Switch config
  connection: network_cli
  hosts: sw19
  gather_facts: no
  become: yes
  become_method: enable
  tasks:
    - name: IOS >> VLAN Updates
      ios_vlan:
        aggregate:
          - 2
          - 5
        vlan_id: 5
        name: TEST VLAN 5
        state: present
      register: command_output

    - name: DEBUG >> VLAN Update
      debug:
        msg: "{{ command_output }}"

```

When executing it came across an error that gave some more insight that was not portrayed on the
module definition page.

```yaml linenums="1"

ansible-playbook output_test.yml -i ./lab_hosts

PLAY [Switch config] ***********************************************************

TASK [IOS >> VLAN Updates] *****************************************************
fatal: [sw19]: FAILED! => {"changed": false, "msg": "parameters are mutually exclusive: vlan_id, aggregate"}
	to retry, use: --limit @/Users/joshv/Documents/Ansible/output_test.retry

PLAY RECAP *********************************************************************
sw19                       : ok=0    changed=0    unreachable=0    failed=1   

```

Modifying the playbook with the fatal error message out. It now looks like this:

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Switch config
  connection: network_cli
  hosts: sw19
  gather_facts: no
  become: yes
  become_method: enable
  tasks:
    - name: IOS >> VLAN Updates
      ios_vlan:
        aggregate: 
          - { 'vlan_id': 2, 'name': 'TRANSIT' }
          - { 'vlan_id': 5, 'name': 'Test VLAN' }
        state: present
      register: command_output

    - name: DEBUG >> VLAN Update
      debug:
        msg: "{{ command_output }}"

```

This will now deploy in aggregate all of the VLANs that are being defined in the list of
dictionaries. Looking at the output this is what is now on the switch:

```yaml linenums="1"

#show vlan

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/1, Gi0/3, Gi1/0, Gi1/2
                                                Gi1/3
2    TRANSIT                          active    Gi0/0, Gi1/1
5    Test VLAN                        active    Gi0/2
1002 fddi-default                     act/unsup 
1003 token-ring-default               act/unsup 
1004 fddinet-default                  act/unsup 
1005 trnet-default                    act/unsup 

VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
1    enet  100001     1500  -      -      -        -    -        0      0   
2    enet  100002     1500  -      -      -        -    -        0      0   
5    enet  100005     1500  -      -      -        -    -        0      0   
1002 fddi  101002     1500  -      -      -        -    -        0      0   
1003 tr    101003     1500  -      -      -        -    -        0      0   
1004 fdnet 101004     1500  -      -      -        ieee -        0      0   
1005 trnet 101005     1500  -      -      -        ibm  -        0      0   

Remote SPAN VLANs
------------------------------------------------------------------------------


Primary Secondary Type              Ports
------- --------- ----------------- ------------------------------------------


```

## Changing the VLANs on the device

Removing a VLAN that is not supposed to be on the device is incredibly simple with this
**aggregate** feature as well. If we change the play to looking like this

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Switch config
  connection: network_cli
  hosts: sw19
  gather_facts: no
  become: yes
  become_method: enable
  tasks:
    - name: IOS >> VLAN Updates
      ios_vlan:
        aggregate: 
          - { 'vlan_id': 2, 'name': 'TRANSIT', state: present }
          - { 'vlan_id': 5, 'name': 'Test VLAN', state: absent }
      register: command_output

    - name: DEBUG >> VLAN Update
      debug:
        msg: "{{ command_output }}"

```

The resulting play execution shows that the VLAN is removed from the command output.

```yaml linenums="1"


PLAY [Switch config] ***********************************************************

TASK [IOS >> VLAN Updates] *****************************************************
changed: [sw19]

TASK [DEBUG >> VLAN Update] ****************************************************
ok: [sw19] => {
    "msg": {
        "changed": true, 
        "commands": [
            "no vlan 5"
        ], 
        "failed": false
    }
}

PLAY RECAP *********************************************************************
sw19                       : ok=2    changed=1    unreachable=0    failed=0   


```

### Adding a VLAN and assigning to Interface

Want to create an interface and assign it to a VLAN quickly? Here is where the **ios_vlan** module
may be able to help very quickly. In the lab it is very simple as there are only a few interfaces
on the layer 2 switch that we have.

#### Play Definition

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Switch config
  connection: network_cli
  hosts: sw19
  gather_facts: no
  become: yes
  become_method: enable
  tasks:
    - name: IOS >> VLAN Updates
      ios_vlan:
        vlan_id: 12
        name: test-vlan
        interfaces:
          - GigabitEthernet1/2
      register: command_output

    - name: DEBUG >> VLAN Update
      debug:
        msg: "{{ command_output }}"

```

#### Playbook Execution - Adding a VLAN

This play execution will both add a VLAN to the switch, and assign the interfaces to the VLAN as an
access port. With the output from the execution the module registers each of the commands that are
being issued to the switch. This shows the VLAN is first created, then goes into the interface
assigned as a parameter. Lastly it sets that interface to being an access interface in the VLAN.

```yaml linenums="1"


PLAY [Switch config] ***********************************************************

TASK [IOS >> VLAN Updates] *****************************************************
changed: [sw19]

TASK [DEBUG >> VLAN Update] ****************************************************
ok: [sw19] => {
    "msg": {
        "changed": true, 
        "commands": [
            "vlan 12", 
            "name test-vlan", 
            "interface GigabitEthernet1/2", 
            "switchport mode access", 
            "switchport access vlan 12"
        ], 
        "failed": false
    }
}

PLAY RECAP *********************************************************************
sw19                       : ok=2    changed=1    unreachable=0    failed=0   


```

### IOS_VLAN - Purge Parameter

Originally when looking at this module I kind of passed over **purge** parameter. It was mentioned
that this is used with conjunction of the **aggregrate** parameter. My original thinking when I read
_aggregate_ was that this was somehow related to Link Aggregation Control Protocol. Now with looking
at the module much more in depth, I see that was a wrong assumption (in case it was for others).
This adds significant power, to make sure that a switch is configured the way that you define within
a play/task and stays configured that way. If some rogue actor has added a VLAN, how will you ever
know. So for this next test, I went and created three manual VLANs on the switch for VLANs 10, 13,
and 100. 

```yaml linenums="1"


VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/1, Gi0/3, Gi1/0, Gi1/3
2    TRANSIT                          active    Gi0/0, Gi1/1
5    Test VLAN                        active    Gi0/2
10   MANUAL                           active    
12   QB VLAN                          active    Gi1/2
13   MANUAL13                         active    
100  MANUAL100                        active    
1002 fddi-default                     act/unsup 
1003 token-ring-default               act/unsup 
1004 fddinet-default                  act/unsup 
1005 trnet-default                    act/unsup 

VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
1    enet  100001     1500  -      -      -        -    -        0      0   
2    enet  100002     1500  -      -      -        -    -        0      0   
5    enet  100005     1500  -      -      -        -    -        0      0   
10   enet  100010     1500  -      -      -        -    -        0      0   
12   enet  100012     1500  -      -      -        -    -        0      0   
13   enet  100013     1500  -      -      -        -    -        0      0   
          
VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
100  enet  100100     1500  -      -      -        -    -        0      0   
1002 fddi  101002     1500  -      -      -        -    -        0      0   
1003 tr    101003     1500  -      -      -        -    -        0      0   
1004 fdnet 101004     1500  -      -      -        ieee -        0      0   
1005 trnet 101005     1500  -      -      -        ibm  -        0      0   

Remote SPAN VLANs
------------------------------------------------------------------------------


Primary Secondary Type              Ports
------- --------- ----------------- ------------------------------------------


```

#### Play Setup - Purge VLANs

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Switch config
  connection: network_cli
  hosts: sw19
  gather_facts: no
  become: yes
  become_method: enable
  tasks:
    - name: IOS >> VLAN Updates
      ios_vlan:
        aggregate: 
          - { 'vlan_id': 2, 'name': 'TRANSIT', state: present }
          - { 'vlan_id': 5, 'name': 'Test VLAN', state: present }
          - { 'vlan_id': 12, 'name': 'THE TEST VLAN', state: present }
        purge: yes
      register: command_output

    - name: DEBUG >> VLAN Update
      debug:
        msg: "{{ command_output }}"

```

#### PLAY EXECUTION

Below you will find the play execution and the resulting commands sent to the switch. To show this
I did have to run the playbook twice as the bug that I found did not run properly the first time.

> One **important** note that I did find when testing this playbook, at least within Ansible version
> 2.7.5 to use the _purge_ function, you **must** use the keyword **yes** instead of _true_. If you
> use _true_ the purge function will not work.

```yaml linenums="1"


PLAY [Switch config] ***********************************************************

TASK [IOS >> VLAN Updates] *****************************************************
changed: [sw19]

TASK [DEBUG >> VLAN Update] ****************************************************
ok: [sw19] => {
    "msg": {
        "changed": true, 
        "commands": [
            "vlan 5", 
            "name Test VLAN", 
            "vlan 12", 
            "name THE TEST VLAN", 
            "no vlan 10", 
            "no vlan 13", 
            "no vlan 100", 
            "no vlan 1002", 
            "no vlan 1003", 
            "no vlan 1004", 
            "no vlan 1005"
        ], 
        "failed": false
    }
}

PLAY RECAP *********************************************************************
sw19                       : ok=2    changed=1    unreachable=0    failed=0  


```

#### Resulting VLAN Configuration

```yaml linenums="1"


#show vlan

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/1, Gi0/3, Gi1/0, Gi1/3
2    TRANSIT                          active    Gi0/0, Gi1/1
5    Test VLAN                        active    Gi0/2
12   THE TEST VLAN                    active    Gi1/2
1002 fddi-default                     act/unsup 
1003 token-ring-default               act/unsup 
1004 fddinet-default                  act/unsup 
1005 trnet-default                    act/unsup 

VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
1    enet  100001     1500  -      -      -        -    -        0      0   
2    enet  100002     1500  -      -      -        -    -        0      0   
5    enet  100005     1500  -      -      -        -    -        0      0   
12   enet  100012     1500  -      -      -        -    -        0      0   
1002 fddi  101002     1500  -      -      -        -    -        0      0   
1003 tr    101003     1500  -      -      -        -    -        0      0   
1004 fdnet 101004     1500  -      -      -        ieee -        0      0   
1005 trnet 101005     1500  -      -      -        ibm  -        0      0   

Remote SPAN VLANs
------------------------------------------------------------------------------


Primary Secondary Type              Ports
------- --------- ----------------- ------------------------------------------


```

## Summary

In summary there are some pieces that need to get worked out. This was the first time that I had
taken a look at the module. For the work that I've done previously I was just using Jinja2 templates
to assign VLAN configuration to an interface. Looking closer at this module there is a lot of power
to make sure that the proper VLANs are configured everywhere that you need, and be able to eliminate
others. This module is definitely something that you should keep in your pocket.
