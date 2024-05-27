---
authors: [jvanderaa]
toc: true
date: 2019-01-05
layout: single
comments: true
slug: ansible-output-work
title: Ansible - Working with command output
# collections:
#   - Cisco
#   - Ansible
# categories:
#   - Ansible
#   - Cisco Automation
tags: ["ansible", "cisco"]
---

You have decided to move forward with using/trying Ansible. You can now connect to a device and get
a green success that you get a _hello world_ like command such as `show hostname` or
`show inventory` and get the GREEN success on Ansible. Now what. You may want to see the output of
the command that you sent and got information back. This is your post on _getting started_.

This is the process that I typically go through when developing a playbook for use. Let's say this
is a playbook that you wish to just get show information out of the device, say investigating if
there are any configurations that are applied that would be part of a CVE bug, or just operational
status.

During this post I will relate the Ansible data structures/formats to that of Python. So the terms
will be dictionary (hashes) and lists (lists).

**Playbook Design Process**

1. Make sure that I can connect to the devices with a simple show command
2. Get necessary show output
3. Debug the outputs of the show commands
4. Set facts or take more action based on other outputs

This can get extremely elaborate. I am going to attempt to keep this about the debug commands along
the way.

## Lab Setup

First I will just give a quick diagram of the lab environment. This is simulated with
[EVE-NG](https://www.eve-ng.net). I will be accessing the devices via a management network to show
various things.

![LabDesign](/images/2019/01/lab_design.png)

I am going to connect to just Cisco IOS and Cisco ASA virtual images for this. That can extend as
well to any other platform using the standard
[Ansible 2.9 network modules](https://docs.ansible.com/ansible/2.9/modules/list_of_network_modules.html).

## Playbook Play and Task

First, the initial connection and a simple show command.

### Playbook A

#### Task 1 (A1)

The play in the playbook is going to log in and execute the following two tasks:

1. Task 1: Issue command `show run interface loopback 0` -> Save to a variable named
**show_commands**
2. Task 2: **Debug** the output of the variable **show_commands**, which is stored for each device
that is connected to.

```yaml
---
# yamllint disable rule:truthy
- name: Test command outputs
  connection: network_cli
  hosts: cisco_routers
  gather_facts: no
  become: yes
  become_method: enable

  tasks:
    - name: IOS >> Show commands
      ios_command:
        commands:
          - show run interface loopback 0
      register: show_commands

    - name: SYS >> DEBUG OUTPUT
      debug:
        msg: "{{ show_commands }}"
```

Here is the output from connecting to a single device:

```bash linenums="1"
PLAY [Test command outputs] ****************************************************

TASK [IOS >> Show commands] ****************************************************
ok: [rtr01]

TASK [SYS >> DEBUG OUTPUT] *****************************************************
ok: [rtr01] => {
    "msg": {
        "changed": false,
        "failed": false,
        "stdout": [
            "Building configuration...\n\nCurrent configuration : 68 bytes\n!\ni
nterface Loopback0\n ip address 10.100.100.1 255.255.255.255\nend"
        ],
        "stdout_lines": [
            [
                "Building configuration...",
                "",
                "Current configuration : 68 bytes",
                "!",
                "interface Loopback0",
                " ip address 10.100.100.1 255.255.255.255",
                "end"
            ]
        ]
    }
}

PLAY RECAP *********************************************************************
rtr01                      : ok=2    changed=0    unreachable=0    failed=0
```

As we look at the output, the task itself creates the part `"msg":` This itself shows the output
dictionary. This has several `keys:` and `values`. Breaking down each of the keys and values in the
output:

1. `changed`: This is a boolean field where you will see if the variable stored (output of a task)
had made a change. Most `*_command` outputs will not make changes to the devices.
2. `failed`: Did the task have a failed return code or not
3. `stdout`: The standard output, including escape characters, of the output, this output is a list
4. `stdout_lines`: This is a more human readable output format, that puts the line breaks in. This
output is in the format of a list

These outputs are in the forms of lists, so if we want to get access to the actual string of the
command `show run interface loopback 0`? We need to access the `show_commands['stdout'][0]`.
This will be shown with the updated playbook (a second debug has been added):

```yaml
---
# yamllint disable rule:truthy
- name: Test command outputs
  connection: network_cli
  hosts: cisco_routers
  gather_facts: no
  become: yes
  become_method: enable
  tasks:
    - name: IOS >> Show commands
      ios_command:
        commands:
          - show run interface loopback 0
      register: show_commands

    - name: SYS >> DEBUG OUTPUT
      debug:
        msg: "{{ show_commands }}"

    - name: SYS >> DEBUG to get to the actual output
      debug:
        msg: "{{ show_commands['stdout'][0] }}"
```

This now yields this output:

```bash linenums="1"
PLAY [Test of connectivity] ****************************************************

TASK [IOS >> Show commands] ****************************************************
ok: [rtr01]

TASK [SYS >> DEBUG OUTPUT] *****************************************************
ok: [rtr01] => {
    "msg": {
        "changed": false,
        "failed": false,
        "stdout": [
            "Building configuration...\n\nCurrent configuration : 68 bytes\n!\ni
nterface Loopback0\n ip address 10.100.100.1 255.255.255.255\nend"
        ],
        "stdout_lines": [
            [
                "Building configuration...",
                "",
                "Current configuration : 68 bytes",
                "!",
                "interface Loopback0",
                " ip address 10.100.100.1 255.255.255.255",
                "end"
            ]
        ]
    }
}

TASK [SYS >> DEBUG to get to the actual output] ********************************
ok: [rtr01] => {
    "msg": "Building configuration...\n\nCurrent configuration : 68 bytes\n!\nin
terface Loopback0\n ip address 10.100.100.1 255.255.255.255\nend"
}

PLAY RECAP *********************************************************************
rtr01                      : ok=3    changed=0    unreachable=0    failed=0
```

### Why Lists?

So why are `stdout` and `stdout_lines` are in the type of lists? This goes back to the section of
the Ansible module `ios_commands` where `commands` is fed a list. This means that you can send
multiple commands in a single task. Updating the playbook to be this:

```yaml
---
# yamllint disable rule:truthy
- name: Test command outputs
  connection: network_cli
  hosts: cisco_routers
  gather_facts: no
  become: yes
  become_method: enable

  tasks:
    - name: IOS >> Show commands
      ios_command:
        commands:
          - show run interface loopback 0
          - ping 8.8.8.8 source loopback 0 repeat 20 size 1500
      register: show_commands

    - name: SYS >> DEBUG OUTPUT
      debug:
        msg: "{{ show_commands }}"

    - name: SYS >> DEBUG to get to the actual output for 1st command run
      debug:
        msg: "{{ show_commands['stdout'][0] }}"

    - name: SYS >> DEBUG to get the ping results
      debug:
        msg: "{{ show_commands['stdout'][1] }}"
```

Which now yields:

```bash linenums="1"
PLAY [Test command outputs] ****************************************************

TASK [IOS >> Show commands] ****************************************************
ok: [rtr01]

TASK [SYS >> DEBUG OUTPUT] *****************************************************

ok: [rtr01] => {
    "msg": {
        "changed": false,
        "failed": false,
        "stdout": [
            "Building configuration...\n\nCurrent configuration : 68 bytes\n!\ninterface Loopback0\n ip address 10.100.100.1 255.255.255.255\nend",
            "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:\nPacket sent with a source address of 10.100.100.1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min/avg/max = 86/108/213 ms",
            "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:\nPacket sent with a source address of 10.100.100.1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min/avg/max = 82/108/217 ms"
        ],
        "stdout_lines": [
            [
                "Building configuration...",
                "",
                "Current configuration : 68 bytes",
                "!",
                "interface Loopback0",
                " ip address 10.100.100.1 255.255.255.255",
                "end"
            ],
            [
                "Type escape sequence to abort.",
                "Sending 20, 1500-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:",
                "Packet sent with a source address of 10.100.100.1 ",
                "!!!!!!!!!!!!!!!!!!!!",
                "Success rate is 100 percent (20/20), round-trip min/avg/max = 86/108/213 ms"
            ]
        ]
    }
}

TASK [SYS >> DEBUG to get to the actual output for 1st command run] ***
ok: [rtr01] => {
    "msg": "Building configuration...\n\nCurrent configuration : 68 bytes\n!\nin
terface Loopback0\n ip address 10.100.100.1 255.255.255.255\nend"
}

TASK [SYS >> DEBUG to get the ping results] ************************************
ok: [rtr01] => {
    "msg": "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to
8.8.8.8, timeout is 2 seconds:\nPacket sent with a source address of 10.100.100.
1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min/av
g/max = 41/108/260 ms"
}

PLAY RECAP *********************************************************************
rtr01                      : ok=4    changed=0    unreachable=0    failed=0
```

We can now see how you may get at particular command outputs, while running multiple commands during
one task on the device. From what I can tell, these commands are run sequentially, and not with
separate SSH sessions, as during my testing I only ever saw a single SSH session on the device.

#### Accessing variables from other tasks

This is something that I stumbled upon at some point that was helpful in multiple play playbooks.
You have multiple plays in a playbook right? So how do you get at information from a previous task?
You access it via the keyword variable `hostvars`. I've added a second play to the previous
playbook. I also added another DNS provider to test my pings to in order to show this.


```yaml
---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Test command outputs
  connection: network_cli
  hosts: cisco_routers
  gather_facts: no
  become: yes
  become_method: enable

  tasks:
    - name: IOS >> Show commands
      ios_command:
        commands:
          - show run interface loopback 0
          - ping 8.8.8.8 source loopback 0 repeat 20 size 1500
          - ping 1.1.1.1 source loopback 0 repeat 20 size 1500
      register: show_commands

    - name: SYS >> DEBUG OUTPUT
      debug:
        msg: "{{ show_commands }}"

    - name: SYS >> DEBUG to get to the actual output for 1st command run
      debug:
        msg: "{{ show_commands['stdout'][0] }}"

    - name: SYS >> DEBUG to get the ping results
      debug:
        msg: "{{ show_commands['stdout'][1] }}"

- name: See output from previous play
  connection: local
  hosts: local
  gather_facts: no

  tasks:
    - name: SYS >> Debug variable from previous task
      debug:
        msg: "{{ hostvars['rtr01']['show_commands']['stdout'][2] }}"
```

This now has the output of the ping test to 1.1.1.1 in the output.

```bash linenums="1"
PLAY [Test command outputs] ****************************************************

~~~~ PLAY OUTPUT TRUNCATED FOR BREVITY ~~~~~

PLAY [See output from previous play] *******************************************

TASK [SYS >> Debug variable from previous task] ********************************
ok: [localhost] => {
    "msg": "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to
1.1.1.1, timeout is 2 seconds:\nPacket sent with a source address of 10.100.100.
1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min/av
g/max = 63/108/236 ms"
}

PLAY RECAP *********************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0
rtr01                      : ok=4    changed=0    unreachable=0    failed=0
```

## Looping over the output

You can also loop over the output of the commands as well. I added in some more lines to the debug
that will show how you can loop over all of the commands you issued. In a future post we will
discuss on how to debug through using `with_items`.

```yaml linenums="1"
    - name: SYS >> DEBUG to see loop
      debug:
        msg: "{{ item }}"
      with_items: "{{ show_commands['stdout'] }}"
```

We want to get to each of the `stdout` outputs. I've added `with_items` and we have a new variable
of `item` that we reference in the message. We now get the following output related to that task:

```bash linenums="1"
TASK [SYS >> DEBUG to see loop] ************************************************
ok: [rtr01] => (item=Building configuration...

Current configuration : 68 bytes
!
interface Loopback0
 ip address 10.100.100.1 255.255.255.255
end) => {
    "msg": "Building configuration...\n\nCurrent configuration : 68 bytes\n!\nin
terface Loopback0\n ip address 10.100.100.1 255.255.255.255\nend"
}
ok: [rtr01] => (item=Type escape sequence to abort.
Sending 20, 1500-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
Packet sent with a source address of 10.100.100.1
!!!!!!!!!!!!!!!!!!!!
Success rate is 100 percent (20/20), round-trip min/avg/max = 86/108/213 ms) =>
{
    "msg": "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to
 8.8.8.8, timeout is 2 seconds:\nPacket sent with a source address of 10.100.10
0.1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min
/avg/max = 86/108/213 ms"
}
ok: [rtr01] => (item=Type escape sequence to abort.
Sending 20, 1500-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
Packet sent with a source address of 10.100.100.1
!!!!!!!!!!!!!!!!!!!!
Success rate is 100 percent (20/20), round-trip min/avg/max = 82/108/217 ms) =>
{
    "msg": "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to
 1.1.1.1, timeout is 2 seconds:\nPacket sent with a source address of 10.100.10
0.1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min
/avg/max = 82/108/217 ms"
}
```

## Final Run

Here is the final playbook

```yaml
---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Test command outputs
  connection: network_cli
  hosts: cisco_routers
  gather_facts: no
  become: yes
  become_method: enable

  tasks:
    - name: IOS >> Show commands
      ios_command:
        commands:
          - show run interface loopback 0
          - ping 8.8.8.8 source loopback 0 repeat 20 size 1500
          - ping 1.1.1.1 source loopback 0 repeat 20 size 1500
      register: show_commands

    - name: SYS >> DEBUG OUTPUT
      debug:
        msg: "{{ show_commands }}"

    - name: SYS >> DEBUG to get to the actual output for 1st command run
      debug:
        msg: "{{ show_commands['stdout'][0] }}"

    - name: SYS >> DEBUG to get the ping results
      debug:
        msg: "{{ show_commands['stdout'][1] }}"

    - name: SYS >> DEBUG to see loop
      debug:
        msg: "{{ item }}"
      with_items: "{{ show_commands['stdout'] }}"

- name: See output from previous play
  connection: local
  hosts: local
  gather_facts: no

  tasks:
    - name: SYS >> Debug variable from previous task
      debug:
        msg: "{{ hostvars['rtr01']['show_commands']['stdout'][2] }}"

```

Final Run Output

```bash linenums="1"
PLAY [Test command outputs] ****************************************************

TASK [IOS >> Show commands] ****************************************************
ok: [rtr01]

TASK [SYS >> DEBUG OUTPUT] *****************************************************
ok: [rtr01] => {
    "msg": {
        "changed": false,
        "failed": false,
        "stdout": [
            "Building configuration...\n\nCurrent configuration : 68 bytes\n!\ni
nterface Loopback0\n ip address 10.100.100.1 255.255.255.255\nend",
            "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to
 8.8.8.8, timeout is 2 seconds:\nPacket sent with a source address of 10.100.100
.1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min/a
vg/max = 86/108/213 ms",
            "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to
 1.1.1.1, timeout is 2 seconds:\nPacket sent with a source address of 10.100.100
.1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min/a
vg/max = 82/108/217 ms"
        ],
        "stdout_lines": [
            [
                "Building configuration...",
                "",
                "Current configuration : 68 bytes",
                "!",
                "interface Loopback0",
                " ip address 10.100.100.1 255.255.255.255",
                "end"
            ],
            [
                "Type escape sequence to abort.",
                "Sending 20, 1500-byte ICMP Echos to 8.8.8.8, timeout is 2 secon
ds:",
                "Packet sent with a source address of 10.100.100.1 ",
                "!!!!!!!!!!!!!!!!!!!!",
                "Success rate is 100 percent (20/20), round-trip min/avg/max = 8
6/108/213 ms"
            ],
            [
                "Type escape sequence to abort.",
                "Sending 20, 1500-byte ICMP Echos to 1.1.1.1, timeout is 2 secon
ds:",
                "Packet sent with a source address of 10.100.100.1 ",
                "!!!!!!!!!!!!!!!!!!!!",
                "Success rate is 100 percent (20/20), round-trip min/avg/max = 8
2/108/217 ms"
            ]
        ]
    }
}

TASK [SYS >> DEBUG to get to the actual output for first command of show run] ***
ok: [rtr01] => {
    "msg": "Building configuration...\n\nCurrent configuration : 68 bytes\n!\nint
erface Loopback0\n ip address 10.100.100.1 255.255.255.255\nend"
}

TASK [SYS >> DEBUG to get the ping results] ************************************
ok: [rtr01] => {
    "msg": "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to
8.8.8.8, timeout is 2 seconds:\nPacket sent with a source address of 10.100.100
.1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min/
avg/max = 86/108/213 ms"
}

TASK [SYS >> DEBUG to see loop] ************************************************
ok: [rtr01] => (item=Building configuration...

Current configuration : 68 bytes
!
interface Loopback0
 ip address 10.100.100.1 255.255.255.255
end) => {
    "msg": "Building configuration...\n\nCurrent configuration : 68 bytes\n!\nin
terface Loopback0\n ip address 10.100.100.1 255.255.255.255\nend"
}
ok: [rtr01] => (item=Type escape sequence to abort.
Sending 20, 1500-byte ICMP Echos to 8.8.8.8, timeout is 2 seconds:
Packet sent with a source address of 10.100.100.1
!!!!!!!!!!!!!!!!!!!!
Success rate is 100 percent (20/20), round-trip min/avg/max = 86/108/213 ms) =>
{
    "msg": "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to
 8.8.8.8, timeout is 2 seconds:\nPacket sent with a source address of 10.100.10
0.1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min
/avg/max = 86/108/213 ms"
}
ok: [rtr01] => (item=Type escape sequence to abort.
Sending 20, 1500-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
Packet sent with a source address of 10.100.100.1
!!!!!!!!!!!!!!!!!!!!
Success rate is 100 percent (20/20), round-trip min/avg/max = 82/108/217 ms) =>
{
    "msg": "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to
1.1.1.1, timeout is 2 seconds:\nPacket sent with a source address of 10.100.100
.1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min/
avg/max = 82/108/217 ms"
}

PLAY [See output from previous play] *******************************************

TASK [SYS >> Debug variable from previous task] ********************************
ok: [localhost] => {
    "msg": "Type escape sequence to abort.\nSending 20, 1500-byte ICMP Echos to
1.1.1.1, timeout is 2 seconds:\nPacket sent with a source address of 10.100.100.
1 \n!!!!!!!!!!!!!!!!!!!!\nSuccess rate is 100 percent (20/20), round-trip min/av
g/max = 82/108/217 ms"
}

PLAY RECAP *********************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0
rtr01                      : ok=5    changed=0    unreachable=0    failed=0
```

Hope that this has been helpful!
