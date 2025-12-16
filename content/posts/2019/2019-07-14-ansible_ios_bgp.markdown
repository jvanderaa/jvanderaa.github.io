---
authors: [jvanderaa]
toc: true
date: 2019-07-13
layout: single
slug: ansible-ios-bgp-module
title: Ansible IOS BGP Module
comments: true
# collections:
#   - Cisco
#   - Ansible
# categories:
#   - Ansible
#   - Cisco Automation
tags:
  - ansible
  - cisco
  - ios_bgp
sidebar:
  nav: ansible
---

In this post I'm going to be taking a deeper dive into the new in Ansible 2.8
[IOS BGP](https://docs.ansible.com/ansible/2.8/modules/ios_bgp_module.html)
module. This may be one of the more complex modules to date and I'll try to
make it as simple as possible.  

<!-- more -->

For a reminder about the BGP protocol is that this is the predominate protocol
that runs the Internet. It is used to peer up with other companies and is what
helps to make the Internet great. This is a very powerful protocol, and has been
expanded to support many things. This is also a protocol that is heavily used in
modern data centers.  

On this module there are a TON of parameters (OK - 47 parameters). That is going
to be too many to list out. If you want to take a look at each and every one of
the parameters (which I do recommend doing at times, or at least going to the 
examples) check out the link above that takes you to the Ansible documentation.  

Let's dive on in.

> Note: In this I will be working with a "fixed version" of the `ios_bgp`
> module. In working on the post it was found that `next-hop-self` was not
> getting applied when used in the module. This is fixed in a coming release of
> Ansible. As of 2.8.1 this is still broken. See
> [https://github.com/ansible/ansible/pull/58789](https://github.com/ansible/ansible/pull/58789)
> for more information.  

## Observations

A couple of general observations and my take on the module before getting into
the lab and demo portions. This module is a great start on simplifying what can
be a very complex configuration with BGP. By its nature BGP has a deep and
complex configuration because of how flexible and how much has been stuffed into
the BGP protocol. It's being used within Data Centers of single tenants! This is
not going to be a post about BGP however - you can find plenty of those
elsewhere that are more in depth at this point.  

This module gets the basics spot on. I'm going to look to leverage this wherever
I can. That said however, there are still a few pieces that I haven't been able
to figure out how to do with this, and first comes the ISP world. Where there
are multiple VRFs configured within BGP. I'm hopeful that this can be expanded
in the future to support VRF configuration as well.  

All that said, this is a complex module, and has a lot of great standardization
to it. Take a look at the module definition in the
[Ansible docs](https://docs.ansible.com/ansible/2.8/modules/ios_bgp_module.html).

A very impressive part to this as well is that the redistribution from multiple
protocols is covered within the module. Route maps can be applied on
redistributions as well as the network advertisements. It's going to continue to
improve!  

## Lab Setup

### Lab Devices

For this module in particular I went ahead and designed a new lab so we can dig
deep into the setup of various methods of BGP. First we are having R2 as the
edge of the lab, heading out Gig0/1 towards the Internet. R2 is acting as a
single router within an ISP in this instance. R1 is the edge of the virtualized
environment which allows me to leverage Ansible from my machine as the control
machine. R3 and R4 will be on the edge of the enterprise network, with R5
originating some routes via EIGRP to the routers on R3 and R4.  

![BGPLabDesign](/images/2019/07/lab_for_bgp.png)  

### Networks

Routes being advertised by R5 are two /25 networks out of the 203.0.113.0/24
network. All of the addressing in the "production" area of this enterprise are
using [RFC5737](https://tools.ietf.org/html/rfc5737) address space. These are:

* 198.51.100.0/24
* 203.0.113.0/24
* 192.0.2.0/24

### Scenario

For demonstration purposes the configuration will be getting done on only R3
from a text perspective. There will however be the modules on the
[Github](https://github.com/jvanderaa/ansible-using_ios) page, and in a follow
on subsequent video demonstration of the playbook.

```bash {linenos=true}


- name: "PLAY 1: Get Configuration Backup to verify connectivity"
    - name: "TASK 1: Verify Config Backup"
- name: "PLAY 2: Setup R2"
    - name: "TASK 1: Setup eBGP Peers"
- name: "PLAY 3: Setup R4"
    - name: "TASK 1: Setup BGP Peers"


```

This is going to walk through getting R3 to eBGP peer with R2 as a 3rd party
connection, and to R4 as an iBGP peer for internal BGP. This will not work with
the internal routing protocols. We assume that these are already all set to
go.  

#### Initial Routing Configuration

This is more just to show where we are and that there is nothing configured for
BGP on R3.

```bash {linenos=true}


R3#show run | sec bgp
R3#


```

#### First BGP Neighbor

The first BGP neighbor we should bring up is within the same AS. Let's make sure
that we are able to get BGP going to that within your same autonomous system
and control before bringing up an exterior peer. In this example we will be
building a BGP peer to 198.51.100.2 with the AS65500.  

##### Playbook Start - Add iBGP peer

Getting started with building the internal BGP connection the task does get a
touch lengthy, so leveraging copy and paste and finding the fields with the
help of the module documentation this is the play to build that iBGP neighbor:

```yaml

- name: "PLAY 1: Setup iBGP Peer to R4"
  connection: network_cli
  hosts: r3
  become: yes
  become_method: enable
  tasks:
    - name: "TASK 1: Setup iBGP Peer"
      ios_bgp:
        config:
          bgp_as: 65500
          router_id: 10.0.0.3
          log_neighbor_changes: true
          neighbors:
            - neighbor: 198.51.100.2
              remote_as: 65500
              activate: true
              timers:
                keepalive: 15
                holdtime: 45
                min_neighbor_holdtime: 5
              description: R4
          networks:
            - prefix: 198.51.100.0
              masklen: 24
            - prefix: 203.0.113.0
              masklen: 24
          address_family:
            - afi: ipv4
              safi: unicast
              neighbors:
                - neighbor: 198.51.100.2
                  activate: yes
                  next_hop_self: yes
        operation: merge
      register: ibgp_peer1

    - name: "TASK 2: Debug output"
      debug:
        msg: "{{ ibgp_peer1 }}"


```

Lines 10, 11, 12 are very common on the BGP configuration. Let's walk through
some of these.

Line 10: Sets the locally running BGP AS on the router  
Line 11: Sets the router-id to be used for the BGP process  
Line 12: Sets logging of neighbor changes to true  
Lines 13-21: Sets configuration of neighbor detail, outside of the address
family  
Lines 22-26: Are used for what networks we want to advertise from BGP  
Lines 27-33: Used for BGP address family configuration updates  
Lines 34-36: Identify our neighbor within the address family  
Line 37: The operation style from Merge, Replace, Override or Delete  

##### Playbook iBGP - Execution

```bash {linenos=true}
- name: "PLAY 1: Setup iBGP Peer to R4"
    - name: "TASK 1: Setup iBGP Peer"
    - name: "TASK 2: Debug output"
```

<iframe width="853" height="480" src="https://www.youtube.com/embed/pqIDnPkiyiE?rel=0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

There are 2 tasks so we can see the output. The first task is to setup an iBGP
peer. We get to see the output on the second task.  

Task 2 output has all of the router configurations that are going to be applied.
Before the change there are no neighbors established. On the console there is
an immediate neighbor established on the iBGP side of things with this
configuration.

```yaml {linenos=true}


PLAY [PLAY 1: Setup iBGP Peer to R4] *******************************************

TASK [TASK 1: Setup iBGP Peer] *************************************************
changed: [r3]

TASK [TASK 2: Debug output] ****************************************************
ok: [r3] => {
    "msg": {
        "changed": true,
        "commands": [
            "router bgp 65500",
            "bgp router-id 10.0.0.3",
            "bgp log-neighbor-changes",
            "neighbor 198.51.100.2 remote-as 65500",
            "neighbor 198.51.100.2 timers 15 45 5",
            "neighbor 198.51.100.2 description R4",
            "network 198.51.100.0 mask 255.255.255.0",
            "network 203.0.113.0 mask 255.255.255.128",
            "address-family ipv4",
            "no auto-summary",
            "neighbor 198.51.100.2 activate",
            "neighbor 198.51.100.2 next-hop-self",
            "exit-address-family",
            "exit"
        ],
        "failed": false
    }
}

PLAY RECAP *********************************************************************
r3                         : ok=2    changed=1    unreachable=0    failed=0    s
kipped=0    rescued=0    ignored=0


```

Pretty straight to the point, that we have a complete BGP configuration getting
deployed. A second run of the playbook _should_ be idempotent, however, when
executing the `show run` to get the configuration of the device and the network
is subnetted on its proper class boundary the Ansible playbook will re-execute
the command. 

> In working on this I have opened up a bug report on the module to see if this
> can be made idempotent. See
> [Github Ansible Issue #59083](https://github.com/ansible/ansible/issues/59083)

#### Second neighbor - the ISP connection

Let's get to adding the second BGP connection. We will add a few more pieces of
information onto the single task of creating a full BGP configuration.  

First let's take a look at the BGP table on the router at this time, there is
only one neighbor:  

```bash {linenos=true}


BGP router identifier 10.0.0.3, local AS number 65500
BGP table version is 37404, main routing table version 37404
11 network entries using 1584 bytes of memory
12 path entries using 960 bytes of memory
6/6 BGP path/bestpath attribute entries using 912 bytes of memory
1 BGP AS-PATH entries using 24 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 3480 total bytes of memory
BGP activity 18/6 prefixes, 18708/18696 paths, scan interval 60 secs

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
198.51.100.2    4        65500   37400      63    37404    0    0 00:13:39       11


```

THe playbook is now:

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: "PLAY 1: Setup iBGP Peer to R4"
  connection: network_cli
  hosts: r3
  become: yes
  become_method: enable
  tasks:
    - name: "TASK 1: Setup iBGP Peer"
      ios_bgp:
        config:
          bgp_as: 65500
          router_id: 10.0.0.3
          log_neighbor_changes: true
          neighbors:
            - neighbor: 198.51.100.2
              remote_as: 65500
              timers:
                keepalive: 15
                holdtime: 45
                min_neighbor_holdtime: 5
              description: R4
            - neighbor: 192.0.2.1
              remote_as: 65510
              timers:
                keepalive: 15
                holdtime: 45
                min_neighbor_holdtime: 5
              description: ISP Neighbor 1
          networks:
            - prefix: 198.51.100.0
              masklen: 24
            - prefix: 203.0.113.0
              masklen: 25
            - prefix: 203.0.113.128
              masklen: 25
          address_family:
            - afi: ipv4
              safi: unicast
              auto_summary: no
              neighbors:
                - neighbor: 198.51.100.2
                  activate: yes
                  next_hop_self: yes
                - neighbor: 192.0.2.1
                  activate: yes
        operation: merge
      register: bgp_setup

    - name: "SUMMARY TASK: Debug output"
      debug:
        msg:
          - "{{ bgp_setup }}"
...



```

#### Adding Second Neighbor - Execution

The execution of the playbook is straight forward again. As expected a second
neighbor statement is created with the `remote-as`, `timers`, and `description`.
The module also activates the neighbor.  

<iframe width="853" height="480" src="https://www.youtube.com/embed/haevkbppxmI?rel=0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>  
  

```yaml {linenos=true}


PLAY [PLAY 1: Setup iBGP Peer to R4] *******************************************

TASK [TASK 1: Setup iBGP Peer] *************************************************
changed: [r3]

TASK [SUMMARY TASK: Debug output] **********************************************
ok: [r3] => {
    "msg": [
        {
            "changed": true,
            "commands": [
                "router bgp 65500",
                "neighbor 192.0.2.1 remote-as 65510",
                "neighbor 192.0.2.1 timers 15 45 5",
                "neighbor 192.0.2.1 description ISP Neighbor 1",
                "network 198.51.100.0 mask 255.255.255.0",
                "network 203.0.113.128 mask 255.255.255.128",
                "address-family ipv4",
                "no auto-summary",
                "neighbor 192.0.2.1 activate",
                "exit-address-family",
                "exit"
            ],
            "failed": false
        }
    ]
}

PLAY RECAP *********************************************************************
r3                         : ok=2    changed=1    unreachable=0    failed=0    s
kipped=0    rescued=0    ignored=0


```

Taking a look at the BGP table, we now have 2 neighbors formed instead of just
the one.  

```yaml {linenos=true}


BGP router identifier 10.0.0.3, local AS number 65500
BGP table version is 58006, main routing table version 58006
11 network entries using 1584 bytes of memory
19 path entries using 1520 bytes of memory
9/6 BGP path/bestpath attribute entries using 1368 bytes of memory
1 BGP AS-PATH entries using 24 bytes of memory
0 BGP route-map cache entries using 0 bytes of memory
0 BGP filter-list cache entries using 0 bytes of memory
BGP using 4496 total bytes of memory
BGP activity 21/9 prefixes, 29013/28994 paths, scan interval 60 secs

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
192.0.2.1       4        65510      31      30    56929    0    0 00:03:26        6
198.51.100.2    4        65500   57996      99    58006    0    0 00:21:06       11


```

## Summary

The module library keeps expanding. Originally I was taken back on the number of
different modules being created that had a specialty to it. Take a look at the
number of modules available for Ansible 2.9 and
[NXOS](https://docs.ansible.com/ansible/2.9/modules/list_of_network_modules.html#nxos)!
I now see the benefit, and this module is a great addition the IOS module
family. There are still areas that aren't covered that may be better suited to
be done with a Jinja template, but this is a great start on the BGP world for
IOS.  

Hope that this has helped someone along the way!