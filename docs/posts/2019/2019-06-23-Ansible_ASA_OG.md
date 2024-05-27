---
authors: [jvanderaa]
toc: true
date: 2019-06-23
layout: single
slug: ansible-asa-og
title: Ansible ASA OG Module
comments: true
# collections:
#   - Cisco
#   - Ansible
# categories:
#   - Ansible
#   - Cisco Automation
categories:
  - cisco
  - ansible
  - asa
  - asa_og
sidebar:
  nav: ansible
---

Today we are taking a look at the newest module out for Cisco ASA Ansible
module - [asa_og](https://docs.ansible.com/ansible/latest/modules/asa_og_module.html).
This one is particularly exciting for the configurations that are being managed
heavily with Object Groups on firewalls. I'm particularly excited to review the
**asa_og** module, time to dig in.  

**New** in this post is the finished playbooks being added to Github. I'm hoping
that this may be helpful and I am uploading the contents to Github for more to
be able to see and get access to if necessary. This will improve as I continue.  

[https://github.com/jvanderaa/ansible-asa_work](https://github.com/jvanderaa/ansible-asa_work)

**Note**
> When working with this module there is not an option to save the configuration
> available with it. Please remember this in your playbook logic. If needing
> to save the configuration there are options. Take a look for samples on my
> previous post [Saving Configurations](https://josh-v.com/blog/2019/03/30/ansible-saving-cisco-configs-ios.html)
> which does not include an example with ASAs yet. I will have to write a follow
> up post on this at which point I will update hte link and content.

## Parameters

First we are going to take a look at the particular parameters to get started,
and what our options are for them. The items in bold are the ones that are
required by the module.

* description: Description for the object group, good for documenting the
purpose
* group_object: This is a list for items within the group
* **group_type**: network-object, service-object, or port-object
* host_ip: List of host addresses within the object group
* ip_mask: List of IPs and masks for use in object groups
* **name**: Name of the object group
* port_eq: Single port for port-object
* port_range: Range for a port-object
* protocol: UDP/TCP/TCP-UDP
* service_cfg: Service object configuration protocol, direction, range or port
* state: **present**/absent/replace to manage the state of the object

For the straight forward parameters this seems like it is something that will be
very handy to use.  

## Starting Lab Setup

For this module we are starting with an effectively blank configuration on the
firewalls. In future posts I will come back to this and show complete firewall
policy management using Ansible.

So the lab looks very much the same at the moment as some of the other posts,
which is below:  

![LabDesign](/images/2019/01/lab_design.png)  

Sample goals:  
- Create an object group for internal addresses (RFC1918)
- Create an object group for external DNS services (Google DNS, Cloudflare,
Quad9)
- Create a service group for DNS and NTP services
- Verify than a service group for just NTP_ONLY does not exist

## Leveraging Ansible OG for creating the modules

### Creating RFC1918 Group

Let's tackle the first item. First to show the configuration on the ASA
firewall for the object group:

```yaml linenums="1"


fw01# show object-group 
fw01# show run | i RFC 1918


```

We see that there is not the object group that is desired to be there.  

We are going to modify the _Playbook_ created in the last blog post for
[asa_command](https://josh-v.com/blog/2019/06/20/ansible-asa-command.html) and
change it to managing our object groups. Starting out it will look like this:

```yaml


---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: ASA OG Working
  connection: network_cli
  hosts: asa_firewalls
  gather_facts: no
  become: yes
  become_method: enable

  tasks:

    - name: "TASK 1: Set RFC1918 Object Group"
      asa_og:
        name: RFC1918_Networks
        group_type: network-object
        state: present
        description: RFC1918 Local Networks
        ip_mask:
          - 10.0.0.0 255.0.0.0
          - 172.16.0.0 255.240.0.0
          - 192.168.0.0 255.255.0.0
      register: output

    - name: "TASK 2: Print output of show interfaces"
      debug:
        msg: "{{ output }}"


```

Now to run the playbook, the expect that the object group will be on the
firewall.  

#### Playbook Execution

The output from the playbook execution gives us exactly what we were looking
for. 

- Task 1: Connects to the ASA and runs the commands, there is a change as the
ASA did not have the object group previously
- Task 2: Output from the previous task shows the commands that were run and the
fact that the device was changed.

##### First Run

<iframe width="853" height="480" src="https://www.youtube.com/embed/PKTEWZG85G0?rel=0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>  

```bash
PLAY [ASA OG Working] **********************************************************

TASK [TASK 1: Set RFC1918 Object Group] ****************************************
changed: [asa1]

TASK [TASK 2: Print output of RFC1918 Object Group] ****************************
ok: [asa1] => {
    "msg": {
        "changed": true,
        "commands": [
            "object-group network RFC1918_Networks",
            "description RFC1918 Local Networks",
            "network-object 10.0.0.0 255.0.0.0",
            "network-object 172.16.0.0 255.240.0.0",
            "network-object 192.168.0.0 255.255.0.0"
        ],
        "failed": false
    }
}

PLAY RECAP *********************************************************************
asa1                       : ok=2    changed=1    unreachable=0    failed=0    s
kipped=0    rescued=0    ignored=0
```

Re-running the playbook again, we see that the module is idempotent. Being that
we can safely run this continuously and not have any changes unless they are
necessary.

##### Second Run

```yaml linenums="1"


PLAY [ASA OG Working] **********************************************************

TASK [TASK 1: Set RFC1918 Object Group] ****************************************
ok: [asa1]

TASK [TASK 2: Print output of RFC1918 Object Group] ****************************
ok: [asa1] => {
    "msg": {
        "changed": false,
        "commands": [],
        "failed": false
    }
}

PLAY RECAP *********************************************************************
asa1                       : ok=2    changed=0    unreachable=0    failed=0    s
kipped=0    rescued=0    ignored=0


```

### Adding onto the previous playbook to add the second group

Continuing within this playbook we will create the second object group that will
be used, the external DNS providers will be added as host objects to a new group
for `EXTERNAL_DNS_NTP`. 

Let's get straight to the play update. We will create a new task for this
second operation and then output the debug summary.

#### Playbook Setup - Adding Host IP group

We have added the second task to the playbook here, with another debug so we can
see when the changes are being made.

```yaml


---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: ASA OG Working
  connection: network_cli
  hosts: asa_firewalls
  gather_facts: no
  become: yes
  become_method: enable

  tasks:

    - name: "TASK 1: Set RFC1918 Object Group"
      asa_og:
        name: RFC1918_Networks
        group_type: network-object
        state: present
        description: RFC1918 Local Networks
        ip_mask:
          - 10.0.0.0 255.0.0.0
          - 172.16.0.0 255.240.0.0
          - 192.168.0.0 255.255.0.0
      register: output

    - name: "TASK 2: Set External DNS/NTP Providers Object Group"
      asa_og:
        name: EXTERNAL_DNS_NTP
        group_type: network-object
        state: present
        description: External DNS Providers (CloudFlare, Google, Quad9, Umbrella)
        host_ip:
          - 1.1.1.1
          - 8.8.8.8
          - 9.9.9.9
          - 208.67.222.222
          - 208.67.220.220
      register: output2     

    - name: "DEBUG 1: Print output of RFC1918 Object Group"
      debug:
        msg: "{{ output }}"

    - name: "DEBUG 2: Print output of External DNS Group"
      debug:
        msg: "{{ output2 }}"


```

##### Playbook Execution 

- Task 1: Comes back OK, the object group is as defined and does not need to get
updated
- Task 2: Adds the second object group that we were anticipating adding to the
firewall
- Debug 1: Shows that there was no change by the `changed` output being set to
false
- Debug 2: Once again shows the `changed` flag is set to `True` and the commands
executed on the device

<iframe width="853" height="480" src="https://www.youtube.com/embed/mOiixwviHFk?rel=0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>  

```bash
PLAY [ASA OG Working] **********************************************************

TASK [TASK 1: Set RFC1918 Object Group] ****************************************
ok: [asa1]

TASK [TASK 2: Set External DNS/NTP Providers Object Group] *********************
changed: [asa1]

TASK [DEBUG 1: Print output of RFC1918 Object Group] ***************************
ok: [asa1] => {
    "msg": {
        "changed": false,
        "commands": [],
        "failed": false
    }
}

TASK [DEBUG 2: Print output of External DNS Group] *****************************
ok: [asa1] => {
    "msg": {
        "changed": true,
        "commands": [
            "object-group network EXTERNAL_DNS_NTP",
            "network-object host 1.1.1.1",
            "network-object host 8.8.8.8",
            "network-object host 9.9.9.9",
            "network-object host 208.67.222.222",
            "network-object host 208.67.220.220",
            "description External DNS Providers (CloudFlare, Google, Quad9, Umbr
            ella)"
        ],
        "failed": false
    }
}

PLAY RECAP **************************************************************************
asa1                       : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

##### Playbook Results on ASA

As expected, we get the new items added to the configuration. When we look at
the before and after on the configuration of the ASA we now see that we have
the second object group, exactly as we expected.

```yaml linenums="1"


fw01# show object-group
object-group network RFC1918_Networks
 description: RFC1918 Local Networks
 network-object 10.0.0.0 255.0.0.0
 network-object 172.16.0.0 255.240.0.0
 network-object 192.168.0.0 255.255.0.0
fw01#
fw01#
fw01# 
fw01# show object-group
object-group network RFC1918_Networks
 description: RFC1918 Local Networks
 network-object 10.0.0.0 255.0.0.0
 network-object 172.16.0.0 255.240.0.0
 network-object 192.168.0.0 255.255.0.0
object-group network EXTERNAL_DNS_NTP
 description: External DNS Providers (CloudFlare, Google, Quad9, Umbrella)
 network-object host 1.1.1.1
 network-object host 8.8.8.8
 network-object host 9.9.9.9
 network-object host 208.67.222.222
 network-object host 208.67.220.220


```

### Adding on the Port Group

Now we need to complete the setup by adding a port group to the playbook so
when a policy is built that the hosts can communicate on the specific ports. To
start off the policy will use only UDP ports 53 (DNS) and 123 (NTP).

> Yes DNS is also on TCP/53, but for this we will stick to only the UDP side for
> non large requests.

> Issue: When working on this I came across an issue with the asa_og module and
> my particular setup (Python3.7.2) with respects to Ansible 2.8. The
> concatenation engine would error out combining strings (the actual commands)
> and integers. The work around on this that you see in the playbook is that
> the ports are surrounded by quotes. This makes them strings instead of
> integers and the module works. I have opened an issue on github for this.
> [https://github.com/ansible/ansible/issues/58258](https://github.com/ansible/ansible/issues/58258)
> if you wish to check on the status.

#### Playbook - Adding in port-object group creation

As expected there is a third task now that will be for creating the port object.
From the module parameters we are now using parameters of `protocol` and
`port_eq`. These are expected parameters for creating a port group.

##### Playbook Task Design - Port Group

Here is the task that is added with the group-type set to `port-object`:  

```yaml

    - name: "TASK 3: Add Port Group"
      asa_og:
        name: SVC_OBJ_DNS_NTP
        group_type: port-object
        state: present
        description: DNS and NTP ports
        protocol: udp
        port_eq:
          - 53
          - 123
      register: output3


```

This brings the full playbook to looking like this:  

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: ASA OG Working
  connection: network_cli
  hosts: asa_firewalls
  gather_facts: no
  become: yes
  become_method: enable

  tasks:

    - name: "TASK 1: Set RFC1918 Object Group"
      asa_og:
        name: RFC1918_Networks
        group_type: network-object
        state: present
        description: RFC1918 Local Networks
        ip_mask:
          - 10.0.0.0 255.0.0.0
          - 172.16.0.0 255.240.0.0
          - 192.168.0.0 255.255.0.0
      register: output

    - name: "TASK 2: Set External DNS/NTP Providers Object Group"
      asa_og:
        name: EXTERNAL_DNS_NTP
        group_type: network-object
        state: present
        description: External DNS Providers (CloudFlare, Google, Quad9, Umbrella)
        host_ip:
          - 1.1.1.1
          - 8.8.8.8
          - 9.9.9.9
          - 208.67.222.222
          - 208.67.220.220
      register: output2

    - name: "TASK 3: Add Port Group"
      asa_og:
        name: SVC_OBJ_DNS_NTP
        group_type: port-object
        state: present
        description: DNS and NTP ports
        protocol: udp
        port_eq:
          - 53
          - 123
      register: output3

    - name: "DEBUG 1: Print output of RFC1918 Object Group"
      debug:
        msg: "{{ output }}"

    - name: "DEBUG 2: Print output of External DNS Group"
      debug:
        msg: "{{ output2 }}"

    - name: "DEBUG 3: Print output of adding Port Group"
      debug:
        msg: "{{ output3 }}"

...


```

##### Playbook Execution

Task 1: Reports OK, as there are no changes here - as expected
Task 2: Also reports OK, as there should be no changes - as expected
Task 3: Creates the port-object to be used
Debug 1: Shows no changes
Debug 2: Shows no changes
Debug 3: Shows that the changed flag is set to `True` and that the changes sent
to the device creates the port object

<iframe width="853" height="480" src="https://www.youtube.com/embed/X7mH-x9ui28?rel=0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

```yaml linenums="1"


PLAY [ASA OG Working] **********************************************************

TASK [TASK 1: Set RFC1918 Object Group] ****************************************
ok: [asa1]

TASK [TASK 2: Set External DNS/NTP Providers Object Group] *********************
ok: [asa1]

TASK [TASK 3: Add Port Group] **************************************************
changed: [asa1]

TASK [DEBUG 1: Print output of RFC1918 Object Group] ***************************
ok: [asa1] => {
    "msg": {
        "changed": false,
        "commands": [],
        "failed": false
    }
}

TASK [DEBUG 2: Print output of External DNS Group] *****************************
ok: [asa1] => {
    "msg": {
        "changed": false,
        "commands": [],
        "failed": false
    }
}

TASK [DEBUG 3: Print output of adding Port Group] ******************************
ok: [asa1] => {
    "msg": {
        "changed": true,
        "commands": [
            "object-group service SVC_OBJ_DNS_NTP udp",
            "port-object eq 53",
            "port-object eq 123",
            "description DNS and NTP ports"
        ],
        "failed": false
    }
}

PLAY RECAP *********************************************************************
asa1                       : ok=6    changed=1    unreachable=0    failed=0    s
kipped=0    rescued=0    ignored=0


```

##### Changes on the ASA

And as we are use to seeing, we see the update on the ASA itself:

```yaml linenums="1"


fw01# show object-group
object-group network RFC1918_Networks
 description: RFC1918 Local Networks
 network-object 10.0.0.0 255.0.0.0
 network-object 172.16.0.0 255.240.0.0
 network-object 192.168.0.0 255.255.0.0
object-group network EXTERNAL_DNS_NTP
 description: External DNS Providers (CloudFlare, Google, Quad9, Umbrella)
 network-object host 1.1.1.1
 network-object host 8.8.8.8
 network-object host 9.9.9.9
 network-object host 208.67.222.222
 network-object host 208.67.220.220
fw01#
fw01#
fw01# show object-group
object-group network RFC1918_Networks
 description: RFC1918 Local Networks
 network-object 10.0.0.0 255.0.0.0
 network-object 172.16.0.0 255.240.0.0
 network-object 192.168.0.0 255.255.0.0
object-group network EXTERNAL_DNS_NTP
 description: External DNS Providers (CloudFlare, Google, Quad9, Umbrella)
 network-object host 1.1.1.1
 network-object host 8.8.8.8
 network-object host 9.9.9.9
 network-object host 208.67.222.222
 network-object host 208.67.220.220
object-group service SVC_OBJ_DNS_NTP udp
 description: DNS and NTP ports
 port-object eq domain
 port-object eq ntp


```

### Removing groups

The last thing to demo is the `state: absent` of the module. What I have seen in
testing at the moment is that the module does not delete the group all together,
but removes the object members. Let's take a look at this in action.

#### Setup - Deletion

First I went ahead and created a new group (using Ansible of course). This is
the old group for DNS that is no longer being used. So we should clean that up
of course. **This module only deletes items from within the object-group, it
will NOT remove an entire object-group**.  

The firewall configuration has the following for object groups:  

```yaml linenums="1"


object-group network RFC1918_Networks
 description: RFC1918 Local Networks
 network-object 10.0.0.0 255.0.0.0
 network-object 172.16.0.0 255.240.0.0
 network-object 192.168.0.0 255.255.0.0
object-group network EXTERNAL_DNS_NTP
 description: External DNS Providers (CloudFlare, Google, Quad9, Umbrella)
 network-object host 1.1.1.1
 network-object host 8.8.8.8
 network-object host 9.9.9.9
 network-object host 208.67.222.222
 network-object host 208.67.220.220
object-group service SVC_OBJ_DNS_NTP udp
 description: DNS and NTP ports
 port-object eq domain
 port-object eq ntp
object-group service DNS_ONLY udp
 description: DNS ports
 port-object eq domain


```

#### Task Created - Absent state

Here is the task with the state changed from `present` to `absent`:  

```yaml

    - name: "TASK 4: Remove Extra Group"
      asa_og:
        name: DNS_ONLY
        group_type: port-object
        state: absent
        protocol: udp
        port_eq:
          - domain
      register: output4


```

#### Playbook Execution - Absent state for an object group

Task 1 - 3: These are the idempotent adds. There is not any changes being made,
so these remain OK.
Task 4: Removes the particular item from within a group. So you will need to
call out all of the objects that you want to have missing from here. The next
task will take a look at another helpful state of **replace**.  

<iframe width="853" height="480" src="https://www.youtube.com/embed/ucKFWlirHjE?rel=0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>  


```yaml linenums="1"


PLAY [ASA OG Working] **********************************************************

TASK [TASK 1: Set RFC1918 Object Group] ****************************************
ok: [asa1]

TASK [TASK 2: Set External DNS/NTP Providers Object Group] *********************
ok: [asa1]

TASK [TASK 3: Add Port Group] **************************************************
ok: [asa1]

TASK [TASK 4: Remove Extra Group] **********************************************
changed: [asa1]

TASK [DEBUG 1: Print output of RFC1918 Object Group] ***************************
ok: [asa1] => {
    "msg": {
        "changed": false,
        "commands": [],
        "failed": false
    }
}

TASK [DEBUG 2: Print output of External DNS Group] *****************************
ok: [asa1] => {
    "msg": {
        "changed": false,
        "commands": [],
        "failed": false
    }
}

TASK [DEBUG 3: Print output of adding Port Group] ******************************
ok: [asa1] => {
    "msg": {
        "changed": false,
        "commands": [],
        "failed": false
    }
}

TASK [DEBUG 4: Print output of removing extra Port Group] **********************
ok: [asa1] => {
    "msg": {
        "changed": true,
        "commands": [
            "object-group service DNS_ONLY udp",
            "no port-object eq domain"
        ],
        "failed": false
    }
}

PLAY RECAP *********************************************************************
asa1                       : ok=8    changed=1    unreachable=0    failed=0    s
kipped=0    rescued=0    ignored=0


```

##### Firewall After

Here we see that the port object that we asked to remove is gone. If there were
other object items in the object-group they would still remain.

```yaml linenums="1"


fw01# show object-group
object-group network RFC1918_Networks
 description: RFC1918 Local Networks
 network-object 10.0.0.0 255.0.0.0
 network-object 172.16.0.0 255.240.0.0
 network-object 192.168.0.0 255.255.0.0
object-group network EXTERNAL_DNS_NTP
 description: External DNS Providers (CloudFlare, Google, Quad9, Umbrella)
 network-object host 1.1.1.1
 network-object host 8.8.8.8
 network-object host 9.9.9.9
 network-object host 208.67.222.222
 network-object host 208.67.220.220
object-group service SVC_OBJ_DNS_NTP udp
 description: DNS and NTP ports
 port-object eq domain
 port-object eq ntp
object-group service DNS_ONLY udp
 description: DNS ports
 port-object eq domain
fw01#
fw01# ! AFTER THE CHANGE
fw01# show object-group
object-group network RFC1918_Networks
 description: RFC1918 Local Networks
 network-object 10.0.0.0 255.0.0.0
 network-object 172.16.0.0 255.240.0.0
 network-object 192.168.0.0 255.255.0.0
object-group network EXTERNAL_DNS_NTP
 description: External DNS Providers (CloudFlare, Google, Quad9, Umbrella)
 network-object host 1.1.1.1
 network-object host 8.8.8.8
 network-object host 9.9.9.9
 network-object host 208.67.222.222
 network-object host 208.67.220.220
object-group service SVC_OBJ_DNS_NTP udp
 description: DNS and NTP ports
 port-object eq domain
 port-object eq ntp
object-group service DNS_ONLY udp
 description: DNS ports


```

### State: Replace

Originally this was not on the radar to include in this post, but I have found
it very helpful. What `replace` will do for you is allow you to set this as the
"standard". So if there are extraneous items in the object group `replace` will
remove anything extra. If there are any items missing from the object group it
will add them in.  

#### Tasks - Replace

I'm going to modify _Task 3_ from earlier to add some extra ports to the
port-group and change _domain_ to _dns_ even though _domain_ is the proper ASA
shorthand for port 53.  The two tasks are now this:

```yaml

    - name: "TASK 3: Add Port Group"
      asa_og:
        name: SVC_OBJ_DNS_NTP
        group_type: port-object
        state: present
        description: DNS and NTP ports
        protocol: udp
        port_eq:
          - "ntp"
          - "dns"
          - "5353"
          - "553"
          - "353"
      register: output3

    - name: "TASK 5: Fix the DNS Port Group"
      asa_og:
        name: SVC_OBJ_DNS_NTP
        group_type: port-object
        state: replace
        description: DNS and NTP ports
        protocol: udp
        port_eq:
          - "domain"
          - "ntp"
      register: output5


```

#### Replace Task Execution

Let's get right to looking at the execution based on the summary above.  

##### Firewall Before

Here we see that the object group **SVC_OBJ_DNS_NTP** has a lot more entries
than one should expect.  

```bash
fw01# show object-group
object-group network RFC1918_Networks
 description: RFC1918 Local Networks
 network-object 10.0.0.0 255.0.0.0
 network-object 172.16.0.0 255.240.0.0
 network-object 192.168.0.0 255.255.0.0
object-group network EXTERNAL_DNS_NTP
 description: External DNS Providers (CloudFlare, Google, Quad9, Umbrella)
 network-object host 1.1.1.1
 network-object host 8.8.8.8
 network-object host 9.9.9.9
 network-object host 208.67.222.222
 network-object host 208.67.220.220
object-group service SVC_OBJ_DNS_NTP udp
 description: DNS and NTP ports
 port-object eq domain
 port-object eq ntp
 port-object eq dnsix
 port-object eq 5353
 port-object eq 553
 port-object eq 353
```

##### Replace - Full Playbook

The full playbook with all of the debugs and the tasks.  

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: ASA OG Working
  connection: network_cli
  hosts: asa_firewalls
  gather_facts: no
  become: yes
  become_method: enable

  tasks:

    - name: "TASK 1: Set RFC1918 Object Group"
      asa_og:
        name: RFC1918_Networks
        group_type: network-object
        state: present
        description: RFC1918 Local Networks
        ip_mask:
          - 10.0.0.0 255.0.0.0
          - 172.16.0.0 255.240.0.0
          - 192.168.0.0 255.255.0.0
      register: output

    - name: "TASK 2: Set External DNS/NTP Providers Object Group"
      asa_og:
        name: EXTERNAL_DNS_NTP
        group_type: network-object
        state: present
        description: External DNS Providers (CloudFlare, Google, Quad9, Umbrella)
        host_ip:
          - 1.1.1.1
          - 8.8.8.8
          - 9.9.9.9
          - 208.67.222.222
          - 208.67.220.220
      register: output2

    - name: "TASK 3: Add Port Group"
      asa_og:
        name: SVC_OBJ_DNS_NTP
        group_type: port-object
        state: present
        description: DNS and NTP ports
        protocol: udp
        port_eq:
          - "ntp"
          - "dnsix"
          - "5353"
          - "553"
          - "353"
      register: output3

    - name: "TASK 4: Remove Extra Group"
      asa_og:
        name: DNS_ONLY
        group_type: port-object
        state: absent
        protocol: udp
        port_eq:
          - domain
      register: output4

    - name: "TASK 5: Fix the DNS Port Group"
      asa_og:
        name: SVC_OBJ_DNS_NTP
        group_type: port-object
        state: replace
        description: DNS and NTP ports
        protocol: udp
        port_eq:
          - "domain"
          - "ntp"
      register: output5

    - name: "DEBUG 1: Print output of RFC1918 Object Group"
      debug:
        msg: "{{ output }}"

    - name: "DEBUG 2: Print output of External DNS Group"
      debug:
        msg: "{{ output2 }}"

    - name: "DEBUG 3: Print output of adding Port Group"
      debug:
        msg: "{{ output3 }}"

    - name: "DEBUG 4: Print output of removing extra Port Group"
      debug:
        msg: "{{ output4 }}"

    - name: "DEBUG 5: Print output of Port Group Replace"
      debug:
        msg: "{{ output5 }}"
...

```

##### Execution

Task 1-4: All check out OK, there are no changes being made  
Task 5: This is that additional task to fix the item properly  
Debug 1-4: All show no changes  
Debug 5: Shows that the changes were made, including add `domain` and removing a
bunch of extra items  

<iframe width="853" height="480" src="https://www.youtube.com/embed/HARqtDKc0MM?rel=0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>  

```bash
PLAY [ASA OG Working] **********************************************************

TASK [TASK 1: Set RFC1918 Object Group] ****************************************
ok: [asa1]

TASK [TASK 2: Set External DNS/NTP Providers Object Group] *********************
ok: [asa1]

TASK [TASK 3: Add Port Group] **************************************************
ok: [asa1]

TASK [TASK 4: Remove Extra Group] **********************************************
ok: [asa1]

TASK [TASK 5: Fix the DNS Port Group] ******************************************
changed: [asa1]

TASK [DEBUG 1: Print output of RFC1918 Object Group] ***************************
ok: [asa1] => {
    "msg": {
        "changed": false,
        "commands": [],
        "failed": false
    }
}

TASK [DEBUG 2: Print output of External DNS Group] *****************************
ok: [asa1] => {
    "msg": {
        "changed": false,
        "commands": [],
        "failed": false
    }
}

TASK [DEBUG 3: Print output of adding Port Group] ******************************
ok: [asa1] => {
    "msg": {
        "changed": false,
        "commands": [],
        "failed": false
    }
}

TASK [DEBUG 4: Print output of removing extra Port Group] **********************
ok: [asa1] => {
    "msg": {
        "changed": false,
        "commands": [],
        "failed": false
    }
}

TASK [DEBUG 5: Print output of Port Group Replace] *****************************
ok: [asa1] => {
    "msg": {
        "changed": true,
        "commands": [
            "object-group service SVC_OBJ_DNS_NTP udp",
            "port-object eq domain",
            "no port-object eq 553",
            "no port-object eq 353",
            "no port-object eq 5353",
            "no port-object eq dnsix"
        ],
        "failed": false
    }
}

PLAY RECAP *********************************************************************
asa1                       : ok=10   changed=1    unreachable=0    failed=0    s
kipped=0    rescued=0    ignored=0
```

## Summary

This module is a terrific module if you are asked to manage ASA policy. This is
very complete and should be part of your toolset for managing ASA devices. I do
foresee a significant amount of use out of the `state: replace` setup in getting
object groups to a declared state.  

Again, very important as well, **do not forget** to save your configurations at
the end if making changes.  

I hope that this has been informative!  