---
toc: true
date: 2019-03-17
layout: single
slug: ansible-cisco-ios-interface
title: Ansible Cisco IOS Interface Module
categories:
- ansible
- cisco
- ios_interface
sidebar:
  nav: ansible
author: jvanderaa
params:
  showComments: true
---

Update: `ios_interface` is to be deprecated as of Ansible 2.13  

In this post I will be taking a deeper look at the **ios_interface** module. This module is used to
configure individual interfaces on a Cisco IOS device. The documentation for the module is located
[here](https://docs.ansible.com/ansible/latest/modules/ios_interface_module.html).
In this module I did have to dig into the actual Python file, and that is located
[here](https://github.com/ansible/ansible/blob/stable-2.9/lib/ansible/modules/network/ios/ios_interfaces.py).  

<!--more-->


> Edit: Had to update the link due to the change in Ansible coming in 2.10. I have hard linked to
> the IOS Interfaces module.

> This module **does not** configure the layer 2 or layer 3 information on an interface. There are
> other modules that are used for configuring these particular pieces.

## A look at the Parameters

### Required Parameters

This module only has a single required module. 

- name: Name of the interface that is being configured, such as _GigabitEthernet0/0/0_  

Using the module with just the one required item of _name_ is pretty uneventful. If you wish to see
the output I'm going to put that at the very bottom as an Appendix type item if you wish to see that
output.

### Optional Parameters

- aggregate: This is what you will need to use if you want to configure multiple interfaces within
the same task execution (or a loop of course)  
- delay: Time to wait before checking the state of an interface, defaults to 10 seconds
- description: Interface description, follows the Cisco command **description** under the
interface configuration  
- duplex: (full/half/auto) duplex settings in the interface configuration  
- enabled: (yes/no) interface link status, should it be enabled/disabled  
- mtu: MTU setting, follows the **mtu** configuration under the interface configuration
- neighbors: Checking for the operational state, using LLDP information, either with the
sub-parameter _host_ or _port_  
- rx_rate: Stated as Receiver rate in bits per second, not sure what this does  
- speed: Interface speed in Mbps, corresponds to the Cisco command **speed** under interface
configuration
- tx_rate: Stated as Transmit rate in bits per second, not sure what it does  

**Note - Operational State**  

As I'm writing (and not having tested yet) the operational state if you are configuring an interface
and looking to validate the neighbors, you may want to up the delay time based on the LLDP neighbor
timers. These timers may be longer than the default 10 seconds.  

#### rx_rate and tx_rate

From the documentation on the module this appears to perhaps to be related to the actual
interface transmit and receive rates that is being reported by the device. The documentation has
some references to **ge** and **le** which would be comparisons. Based on the Python file and the
variables named **want_tx_rate** and **want_rx_rate** within the Python file, this does in fact
appear to be related to the interface traffic amount.

### Parameter Details: Aggregate

This is what I will say is a _group_ of interfaces to configure within a single task. This is where
you will configure multiples of the **ios_interface** task. To leverage this you will need to create
a dictionary (Array) with the required parameters for the module.

## A look at the module in action

First, jumping deep in. Going to take a look at what it looks like to configure interfaces using
the aggregate parameter. This is going to configure specific details about two interfaces on the
switch itself.

#### Pre-Change Config

Before the change there is just the `media-type` and the `negotiation` set to auto. These are
default out of the box.

```yaml {linenos=true}


sw19#show run int gig0/1
Building configuration...

Current configuration : 71 bytes
!
interface GigabitEthernet0/1
 media-type rj45
 negotiation auto
end

sw19#show run int gig0/2
Building configuration...

Current configuration : 71 bytes
!
interface GigabitEthernet0/2
 media-type rj45
 negotiation auto
end


```

#### Playbook

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
      ios_interface:
        aggregate:
          - {name: GigabitEthernet0/1, description: "First Ansible Configured Interface", enabled: no}
          - {name: GigabitEthernet0/2, description: "Second Ansible Configured Interface", enabled: yes}
        speed: 100
        duplex: full
      register: output

    - name: DEBUG >> output
      debug:
        msg: "{{ output }}"

```

#### Ansible Output

Here we see that the commands being sent to the device are to set the speed, duplex to full,
interface description, and then shutting down the interface that was set to disabled.

```yaml {linenos=true}


PLAY [Switch config] ***********************************************************

TASK [IOS >> VLAN Updates] *****************************************************
changed: [sw19]

TASK [DEBUG >> output] *********************************************************
ok: [sw19] => {
    "msg": {
        "changed": true, 
        "commands": [
            "interface GigabitEthernet0/1", 
            "speed 100", 
            "description First Ansible Configured Interface", 
            "duplex full", 
            "shutdown", 
            "interface GigabitEthernet0/2", 
            "speed 100", 
            "description Second Ansible Configured Interface", 
            "duplex full"
        ], 
        "failed": false
    }
}

PLAY RECAP *********************************************************************
sw19                       : ok=2    changed=1    unreachable=0    failed=0   


```

#### Post Execution Configuration

Working through this, it looks like the speed cannot be configured as autonegotation is set on the
interface. I believe that this is something that is primarily set because of using a virtualized
switch platform. I plan to open up a bug report on this soon. We see exactly what we expect in the
configuration after the Ansible output. We see interface description configured on each interface,
the interface shutdown or enabled. 

```yaml {linenos=true}


sw19#show run int gig0/1
Building configuration...

Current configuration : 129 bytes
!
interface GigabitEthernet0/1
 description First Ansible Configured Interface
 shutdown
 media-type rj45
 negotiation auto
end

sw19#show run int gig0/2
Building configuration...

Current configuration : 120 bytes
!
interface GigabitEthernet0/2
 description Second Ansible Configured Interface
 media-type rj45
 negotiation auto
end


```

## Creating a Loopback Interface

In the second example of the playbook we will create additional Loopback addresses. 

### Pre-Change Configuration

Here is the output of the `show ip int breif` of the switch before adding loopbacks.

```yaml {linenos=true}


Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     unassigned      YES unset  up                    up      
GigabitEthernet0/1     unassigned      YES unset  administratively down down    
GigabitEthernet0/2     unassigned      YES unset  up                    up      
GigabitEthernet0/3     unassigned      YES unset  up                    up      
GigabitEthernet1/0     unassigned      YES unset  up                    up      
GigabitEthernet1/1     unassigned      YES unset  up                    up      
GigabitEthernet1/2     unassigned      YES unset  up                    up      
GigabitEthernet1/3     unassigned      YES unset  up                    up      
Loopback0              10.100.100.100  YES manual up                    up      
Port-channel5          unassigned      YES unset  down                  down    
Port-channel6          unassigned      YES unset  down                  down    
Vlan2                  172.16.1.2      YES manual up                    up   


```

Here we only see one loopback address, Loopback0.

### Playbook

The playbook I'm going to add a loopback interface, but there will not be an address configured on
it, you will need to use `ios_l3_interface` in conjunction with this if using `ios_interface` for
loopbacks. 

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
      ios_interface:
        name: Loopback5
      register: output

    - name: DEBUG >> output
      debug:
        msg: "{{ output }}"

```

### Ansible Output

I expect to see the configuration of just creating a loopback address. This is in fact what is seen
upon executing the command.

```yaml {linenos=true}


PLAY [Switch config] ***********************************************************

TASK [IOS >> VLAN Updates] *****************************************************
changed: [sw19]

TASK [DEBUG >> output] *********************************************************
ok: [sw19] => {
    "msg": {
        "changed": true, 
        "commands": [
            "interface Loopback5"
        ], 
        "failed": false
    }
}

PLAY RECAP *********************************************************************
sw19                       : ok=2    changed=1    unreachable=0    failed=0  


```

### Switch Post Run

Now on the switch as expected we see another Loopback address added.

```yaml {linenos=true}


sw19#show ip int brie
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     unassigned      YES unset  up                    up      
GigabitEthernet0/1     unassigned      YES unset  administratively down down    
GigabitEthernet0/2     unassigned      YES unset  up                    up      
GigabitEthernet0/3     unassigned      YES unset  up                    up      
GigabitEthernet1/0     unassigned      YES unset  up                    up      
GigabitEthernet1/1     unassigned      YES unset  up                    up      
GigabitEthernet1/2     unassigned      YES unset  up                    up      
GigabitEthernet1/3     unassigned      YES unset  up                    up      
Loopback0              10.100.100.100  YES manual up                    up      
Loopback5              unassigned      YES unset  up                    up      
Port-channel5          unassigned      YES unset  down                  down    
Port-channel6          unassigned      YES unset  down                  down    
Vlan2                  172.16.1.2      YES manual up                    up   


```

## Summary

Earlier in the week I started using this module in a production environment. I had been using just
**ios_config** and moving down into the interface and issuing the `shutdown` or `no shutdown` of an
interface. After coming across a couple of errors I decided to try the **ios_interface** module for
the playbook. This worked out much better. Digging through this module further with this post I am
finding that **ios_interface** is really good for interface state of up/down and the description of
the interface. So you will want to use this in conjunction with the **ios_l3_interface** and
**ios_l2_interface** to get the complete interface configuration with the modules.

## Appendix

### Task with only the required Parameters (Loopback10)

First taking a look at the play with using a _Loopback10_ interface. There was previously no
_Loopback10_ interface configured. The play looks like the following:

#### Play

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
    - name: IOS Interface >> Configure Loopback10
      ios_interface:
        name: Loopback10
      register: output

    - name: DEBUG >> output
      debug:
        msg: "{{ output }}"

```

#### Play Output

On the output front, nothing surprising. 

The commands sent to the device essentially are:

`config t`
`interface Loopback10`

This creates the interface that was not there previously and does not provide any other
configuration.  

```yaml {linenos=true}


PLAY [Switch config] ***********************************************************

TASK [IOS >> VLAN Updates] *****************************************************
changed: [sw19]

TASK [DEBUG >> output] *********************************************************
ok: [sw19] => {
    "msg": {
        "changed": true, 
        "commands": [
            "interface Loopback10"
        ], 
        "failed": false
    }
}

PLAY RECAP *********************************************************************
sw19                       : ok=2    changed=1    unreachable=0    failed=0   


```

### Task with only the required Parameters (GigabitEthernet0/1)

In this play the interface being configured will be moved from a Loopback interface to one of the
physical interfaces on the device. There will once again be no parameters.

#### Play

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
    - name: IOS Interface >> Configure Gig0/1
      ios_interface:
        name: GigabitEthernet0/1
      register: output

    - name: DEBUG >> output
      debug:
        msg: "{{ output }}"

```

#### Output

The Ansible module appears to check the running configuration as expected before stepping through.
The output shows no commands being applied as the configuration on the interface already has the
desired configuration (blank).

**Pre-Configuration**

```yaml {linenos=true}


#show run int gig0/1
Building configuration...

Current configuration : 71 bytes
!
interface GigabitEthernet0/1
 media-type rj45
 negotiation auto
end


```

There are no pieces that need to be configured, so the output from the playbook execution is below.
With no other parameters defined the module does nothing.

**Play Execution**

```yaml {linenos=true}


PLAY [Switch config] ***********************************************************

TASK [IOS >> VLAN Updates] *****************************************************
ok: [sw19]

TASK [DEBUG >> output] *********************************************************
ok: [sw19] => {
    "msg": {
        "changed": false, 
        "commands": [], 
        "failed": false
    }
}

PLAY RECAP *********************************************************************
sw19                       : ok=2    changed=0    unreachable=0    failed=0   


```
