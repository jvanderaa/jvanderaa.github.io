---
authors: [jvanderaa]
toc: true
date: 2019-01-12
layout: single
comments: true
slug: ansible-cli-vs-ios-high-level
title: Ansible differences between ios config and cli config
# collections:
#   - Cisco
#   - Ansible
# categories:
#   - Ansible
#   - Cisco Automation
tags:
  - ansible
  - cli_command
  - ios_command
  - cisco
---

This is a post that I'm going to review some of the differences between the ios_config module and
the new cli_config module within Ansible networking. I became interested in the module after a
recent discussion between the two. I have decided to take a look at the differences between the two.

<!-- more -->

This is not an under the hood look at the modules. This has already been covered very well (and
with better graphics than I can produce) here at the
[Ansible Blog](https://www.ansible.com/blog/red-hat-ansible-network-automation-updates) look for
"cli_command and cli_config" with your browser find function.

> I may also try to take a look at some of the other modules as well as time may permit. Next up on
> my interest of is the NXOS commands. I may also be limited a touch on some of the other major
> platforms out there, but hopefully I can find some legitimately and provide some value back.


## Differences

### Parameters

First the differences come in a couple of front and center options. First, in `cli_config` there are
a few more options to do with **committing** configurations. These play a role in having a "uniform"
module for pushing to all sorts of devices like IOS, JUNOS, and the such.

**Lines vs config**

One of the major differences in the paramaters comes on how you put a configuration into the module.
With the original `ios_config` you get to pass _The ordered set of commands_ to the module. This
means that you can apply multiple commands within one statement.

With `cli_config` you are passing a **string** into the module that is
_The config to be pushed to the network device_. 

This difference is a very important one. For instance if you wanted to apply multiple lines to a
configuration you will need to find another way with `cli_config` that previously was very simple to
read:

```yaml

  tasks:
    - name: IOS >> No shut the interfaces
      ios_config:
        lines:
          - description ** Configured by Ansible **
          - no shutdown
        parents: interface GigabitEthernet1/0

```

After doing a few different tests including using the `|` character to send multiple lines, `\n` as
a new line character, and using `with_items` all to no avail. Last step I tried to use the old
carriage return `\r` in the config at which point it was successful.

```yaml
  tasks:
    - name: CLI >> No shut the interfaces
      cli_config:
        config: "interface Gig1/0\rdescription **CLI Config!**\rno shutdown"
```


### Templating

Templating is also a little different. From the
[main module page](https://docs.ansible.com/ansible/latest/modules/cli_config_module.html) you can
see an example that is the following:

#### CLI Config

```yaml

- name: configure device with config (CLI)
  cli_config:
    config: "{{ lookup('template', 'basic/config.j2') }}"

```

**IOS Config**
```yaml
- name: configure device with config (IOS)
  ios_config:
    src: config.j2
```

So the only real difference is the lookup module used in the CLI version. This is pretty straight
forward to see what it is doing. It is using the _lookup filter_, of type _template_. Then the 2nd
argument is the template file that you wish to render.

### Execution Information

This is maybe the **biggest** difference that I have found between the _ios_config_ module and the
_cli_config_ module. When storing results of the configuration module execution, you will only get
back two fields - _changed_ and _failed_. You will not be able to see what was executed that you can
see with the _ios_config_ module.

#### Lab Setup

The lab setup for this is pretty simple. I have added a Cisco IOS L2 switch image to the previous
lab that I had in the [previous post](https://josh-v.com/blog/2019/01/05/ansible-output-work.html).
This is really just for a device to connect to.

I am configuring a port channel, only because that is something that I had lined up quick in the
test, no other particular reason.

The Jinja2 template file that I am calling in this execution is the following:

```bash linenums="1"
interface Port-channel5
 switchport trunk allowed vlan 2,4,5
 switchport trunk encapsulation dot1q
 switchport mode trunk
 spanning-tree portfast edge trunk
```

Here is the playbook run with the CLI module:

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Switch config
  connection: network_cli
  hosts: switches
  gather_facts: no
  become: yes
  become_method: enable
  tags: ['switches']

  tasks:

    - name: CLI >> Configure Port channel
      cli_config:
        config: "{{ lookup('template', 'port_channel.j2') }}"
      register: cli_output

    - name: DEBUG
      debug:
        msg: "{{ item }}"
      with_items:
        - "{{ cli_output }}"

```

Output from this is:

```bash linenums="1"
PLAY [Switch config] *******************************************************************************

TASK [CLI >> Configure Port channel] ***************************************************************
changed: [sw01]

TASK [DEBUG] ***************************************************************************************
ok: [sw01] => (item={'failed': False, u'changed': True}) => {
    "msg": {
        "changed": true,
        "failed": false
    }
}

PLAY RECAP *****************************************************************************************
sw01                       : ok=2    changed=1    unreachable=0    failed=0

```

Moving to virtually the same playbook here:

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Switch config
  connection: network_cli
  hosts: switches
  gather_facts: no
  become: yes
  become_method: enable
  tags: ['switches']

  tasks:

    - name: IOS >> Configure port channel
      ios_config:
        src: port_channel.j2
      register: ios_output

    - name: DEBUG
      debug:
        msg: "{{ item }}"
      with_items:
        - "{{ ios_output }}"


```

The resulting output also includes _banners_, _commands_, and _updates_.

```bash linenums="1"
PLAY [Switch config] ***********************************************************

TASK [IOS >> Configure port channel] *******************************************
changed: [sw01]

TASK [DEBUG] *******************************************************************
ok: [sw01] => (item={'failed': False, u'commands': [u'interface Port-channel5',
u'switchport trunk allowed vlan 2,4,6'], u'changed': True, u'updates': [u'interf
ace Port-channel5', u'switchport trunk allowed vlan 2,4,6'], u'banners': {}}) =>
{
    "msg": {
        "banners": {},
        "changed": true,
        "commands": [
            "interface Port-channel5",
            "switchport trunk allowed vlan 2,4,6"
        ],
        "failed": false,
        "updates": [
            "interface Port-channel5",
            "switchport trunk allowed vlan 2,4,6"
        ]
    }
}

PLAY RECAP *********************************************************************
sw01                       : ok=2    changed=1    unreachable=0    failed=0

```

