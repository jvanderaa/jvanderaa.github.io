---
authors: [jvanderaa]
toc: true
date: 2019-06-20
layout: single
slug: ansible-asa-command
title: Ansible ASA Command Module
comments: true
# collections:
#   - Cisco
#   - Ansible
# categories:
#   - Ansible
#   - Cisco Automation
categories:
  - ansible
  - cisco
  - asa
sidebar:
  nav: ansible
---

Today will be a touch shorter post, but it is good to be back at it. In this
post I will be taking a quick look around at the asa_command module, as we start
down the path with looking at the ASA modules in Ansible. This is spurned on a
little bit by Ansible 2.8 coming out with an Object Group specific module. I
will be looking into that further in a future post.

<!-- more -->

For the set of posts regarding the ASA, we will be starting with a pretty bare
configuration on the device. We will have just a management IP address and the
ability to SSH to the device.

## Module Documentation

Module documentation page can be found
[here](https://docs.ansible.com/ansible/latest/modules/asa_command_module.html).

## Lab Configuration

The device has bare basic configuration on it. Here we see that it has just a
management IP address on it.

``` cisco
fw01# show int ip brie
Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0         unassigned      YES unset  administratively down up  
GigabitEthernet0/1         unassigned      YES unset  administratively down up  
GigabitEthernet0/2         unassigned      YES unset  administratively down up  
Management0/0              172.16.0.254    YES CONFIG up                    up 
```

## Using the playbook

### Parameters

There are a couple of key parameters on this module for getting started are:

* commands: A list of commands to send to the device; this can be one, or 
several commands within a list
* context: used for firewalls in multi-context mode, which context do you want
to run the command(s) in

### Simple first Playbook

This is a simple playbook that will issue two commands. We will access both of
them in different tasks within the play. Taking a look at the play we are
executing the task with two commands, a `show int ip brie` and a ping to Google
DNS. 

#### Playbook

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: ASA Command Output
  connection: network_cli
  hosts: asa_firewalls
  gather_facts: no
  become: yes
  become_method: enable
  tasks:
    - name: "TASK 1: Read output from ASA"
      asa_command:
        commands:
          - show int ip brief
          - ping 8.8.8.8
      register: output

    - name: "TASK 2: Print output of show interfaces"
      debug:
        msg: "{{ output.stdout_lines.0 }}"

    - name: "TASK 3: Print output of pinging Google DNS"
      debug:
        msg: "{{ output.stdout_lines.1 }}"


```

#### Tasks High Level

TASK 1 is when Ansible logs into the device and issues the two commands.  
TASK 2 we get the expected output of the `show int ip brie` and the commands
TASK 3 we see that the device is able to successfully ping Google DNS

These are the tasks that are to be run via the playbook broken out:

```bash
cat asa_command_demo.yml | grep TASK
    - name: "TASK 1: Read output from ASA"
    - name: "TASK 2: Print output of show interfaces"
    - name: "TASK 3: Print output of pinging Google DNS"
```

#### Playbook Run

Execution of the playbook:

To see a video of this on Youtube - [https://youtu.be/Wk-3Zg08oSw](https://youtu.be/Wk-3Zg08oSw)

```bash
PLAY [ASA Command Output] *********************************************************************

TASK [TASK 1: Read output from ASA] ***********************************************************
ok: [asa1]

TASK [TASK 2: Print output of show interfaces] ************************************************
ok: [asa1] => {
    "msg": [
        "Interface                  IP-Address      OK? Method Status                Protocol",
        "GigabitEthernet0/0         unassigned      YES unset  administratively down up  ",
        "GigabitEthernet0/1         unassigned      YES unset  administratively down up  ",
        "GigabitEthernet0/2         unassigned      YES unset  administratively down up  ",
        "Management0/0              172.16.0.254    YES CONFIG up                    up"
    ]
}

TASK [TASK 3: Print output of pinging Google DNS] *********************************************
ok: [asa1] => {
    "msg": [
        "Type escape sequence to abort.",
        "Sending 5, 100-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:",
        "!!!!!",
        "Success rate is 100 percent (5/5), round-trip min/avg/max = 20/104/190 ms"
    ]
}

PLAY RECAP ************************************************************************************
asa1                       : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

#### Access Multiple Commands

This is another example of how to issue multiple commands against a device
within a single task. For a deeper dive on that you can see an earlier post
[here](https://josh-v.com/blog/2019/01/05/ansible-output-work.html).

## Summary

This is a solid starting out module for working with ASA firewalls. It does
come in very handy with dealing and gathering information from the ASA
firewall platform. I have used this for several things within a production
environment, primarily for data gathering. Hopefully coming up I will be able
to expand on this further in building out an ASA firewall.

Hope this was helpful! 

