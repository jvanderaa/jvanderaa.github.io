---
authors: [jvanderaa]
toc: true
date: 2020-01-26
layout: single
comments: true
slug: ansible-cisco-ios-interfaces-module
title: Ansible Cisco ios_interfaces module
# collections:
#   - Cisco
#   - Ansible
# categories:
# - Ansible
# - Cisco Automation
tags:
- blog
- ansible
- cisco
- deprecation
sidebar:
  nav: ansible
---

This has become a post about the **ios_interfaces** module with documentation that can be found
[Ansible ios_interfaces doc](https://docs.ansible.com/ansible/latest/modules/ios_interfaces_module.html).
Originally I was going to write about the deprecations for just the Cisco IOS modules. Then as I
investigated further, I had found that there are many more modules that are being deprecated. In
this post I will take a closer look at the differences between the `ios_interface` and `ios_vlan`
modules that I had written posts on last year and what their new counter parts look like. And in the
end the post had quite a bit of good detail about the module. I think you will like what is here.  

> Previous Posts
>
> - [ios_interface](https://josh-v.com/blog/2019/03/17/ansible-cisco-ios-interface.html)
> - [ios_vlan](https://josh-v.com/blog/2019/03/09/ansible-ios-vlan.html)

## Module Deprecations

In addition to the Cisco "legacy" interface and vlan modules that are being deprecated, the Ansible
generic modules are being deprecated as well. These include `net_interface`, `net_linkagg`,
`net_l2/l3_interface`, and `net_l2/l3_vlan`.  

Not to be outdone, not only are the Cisco and Ansible generic modules being deprecated, so are each
of the same set of modules for Juniper, EOS, VYOS, NXOS, IOSXR, and Netvisor.  

In all by doing a browser search for `(D)` on the Ansible 2.9 Network Modules
[page](https://docs.ansible.com/ansible/2.9/modules/list_of_network_modules.html) I come across a
total of 77 different modules that are in the process of being deprecated. That is quite a bit, so
make sure that you are taking a look at your playbooks to look for this.  

One of the downsides I see coming out of this module change is the change from `ios_interface` to
`ios_interfaces`. This is such a subtle difference between the two. You are going to need to pay
extra attention to it. In fact I was taken back when I first saw the parameters of the module being
posted on the Network To Code Public Slack that I had to take a second look. I thought that someone
was way off on the parameters they were using. Then I saw the deprecations and new modules.

### PANOS Module Deprecation

I did also observe an interesting (in my mind) planned deprecation. All of the PANOS modules are
planned to be deprecated in favor of using community drivers from Ansible Galaxy. Why is this
interesting? Well, this is the start of the move to move modules out of Ansible Core and start using
Ansible Galaxy to distribute the modules that you need. More on that to come in another post.

## Differences

There are quite a bit of differences in the modules. The first level parameters for *_interfaces
across vendors has been reduced to just two, **config** and **state**.  

A second difference that I'm observing is the lack of the ability to save the config when change.
This means that you as the playbook creator will need to take action such as notifying a handler or
running a save config when there is a change. You can do this, or have a task executed when there is
a change.

### Config

All of the bulk of the configuration has moved into the config parameter. Within Cisco
`ios_interfaces` you now have the options to configure the _description_, _duplex_, _enabled_,
_mtu_, _name_*, and _speed_. These were previously first level parameters within the module
definition. You can find the module definition at
[Ansible Docs ios_interfaces](https://docs.ansible.com/ansible/latest/modules/ios_interfaces_module.html).

### State

The state is now referencing the configuration of the interface. It does not state whether or not
the interface is enabled or disabled. That is controlled by the _enabled_ sub-parameter of
**config**. The options for **state** include _merged_ (default setting), _replaced_, _overridden_,
and _deleted_.

#### State: Merged

This looks to take whatever is already in the interface configuration and adding/replacing based on
what the module parameters that are configured. So if you have an interface that has just the speed
configured and you just have a task that configures the duplex, you will have speed and duplex
configured.  

With the merged module, you will run the commands that are defined, not worrying about the defaults.
For this demo, I have set the MTU to 1450, which is different than the default of 1500 for this
device type. You will see that in other states, that Ansible will change the configuration. Where as
with the **merged** type, you will run the commands seen in the module parameters, not worrying
about the other parameters not provided.

```yaml

  tasks:
    - name: "TASK 1: IOS >> Set some interfaces with merge"
        ios_interfaces:
        state: replaced
        config:
            - name: GigabitEthernet0/3
            enabled: yes
            description: "Configured by Ansible"
        register: ios_interface_output

    - name: "TASK 2: SYS >> DEBUG OUTPUT"
        debug:
        msg: "{{ ios_interface_output }}"


```

```yaml linenums="1"


"commands": [
    "interface GigabitEthernet0/3",
    "description Configured by Ansible"


```

#### State: Replaced

When using replaced, the entire interface will be configured with what is set in the module. If you
set duplex only, you will only get the duplex of the interface set.  

In this example I will only be looking to enable the interface and change the description. There
will be no changes to the other interfaces defined.  

```yaml

  tasks:
    - name: "TASK 1: IOS >> Set some interfaces with merge"
      ios_interfaces:
        state: replaced
        config:
          - name: GigabitEthernet0/3
            enabled: yes
            description: "Configured by Ansible"
      register: ios_interface_output

    - name: "TASK 2: SYS >> DEBUG OUTPUT"
      debug:
        msg: "{{ ios_interface_output }}"


```

The output (shown in full here only, will skip the "after" and "before" keys in subsequent examples)
shows that the only changes being made are to `GigabitEthernet0/3`. This is similar to what we will
see in the overridden section. Overridden will configure every interface on the device vs replaced
looks to only be handling the interface defined within the config parameter.

```bash linenums="1"


    "msg": {
        "after": [
            {
                "enabled": true,
                "name": "loopback0"
            },
            {
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/0",
                "speed": "auto"
            },
            {
                "description": "MANAGEMENT",
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/1",
                "speed": "auto"
            },
            {
                "description": "PRODUCTION",
                "duplex": "auto",
                "enabled": true,
                "mtu": 1400,
                "name": "GigabitEthernet0/2",
                "speed": "auto"
            },
            {
                "description": "Configured by Ansible",
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/3",
                "speed": "auto"
            }
        ],
        "before": [
            {
                "enabled": true,
                "name": "loopback0"
            },
            {
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/0",
                "speed": "auto"
            },
            {
                "description": "MANAGEMENT",
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/1",
                "speed": "auto"
            },
            {
                "description": "PRODUCTION",
                "duplex": "auto",
                "enabled": true,
                "mtu": 1400,
                "name": "GigabitEthernet0/2",
                "speed": "auto"
            },
            {
                "description": "BEFORE ANSIBLE",
                "duplex": "auto",
                "enabled": true,
                "mtu": 1450,
                "name": "GigabitEthernet0/3",
                "speed": "auto"
            }
        ],
        "changed": true,
        "commands": [
            "interface GigabitEthernet0/3",
            "no mtu",
            "description Configured by Ansible"


```

#### State: Overridden

This one was not completely obvious to me when originally looking at. But as I tested, I have now
come to find that this state is something to be **VERY** cautious with. In the testing, I had the
following configuration on the devices:

```bash linenums="1"


interface GigabitEthernet0/1
 description MANAGEMENT
 OUTPUT OMITTED
!
interface GigabitEthernet0/2
 description PRODUCTION


```

You can see that there are configurations applied to the description. I then created these playbook
tasks to test the `Overridden` setting.

```yaml


  tasks:
    - name: "TASK 1: IOS >> Set some interfaces with merge"
      ios_interfaces:
        state: overridden
        config:
          - name: GigabitEthernet0/3
            enabled: yes
            description: "Configured by Ansible"
      register: ios_interface_output

    - name: "TASK 2: SYS >> DEBUG OUTPUT"
      debug:
        msg: "{{ ios_interface_output }}"


```

The output shows that Ansible is going to erase the description lines:

```bash linenums="1"


"commands": [
    "interface GigabitEthernet0/1",
    "no description",
    "interface GigabitEthernet0/2",
    "no description"


```

This indicates that Ansible will default settings that are not specifically defined within the
module.

The next test I changed the MTU on `GigabitEthernet0/1` and `GigabitEthernet0/2` to some random
14xx MTUs. I've left everything else the same as the play above with no changing fo the MTU, just
setting the description on a single interface. The results from running that playbook now show that
the interface MTU is reset to default since it was not statically defined in the task.

```bash linenums="1"


    "commands": [
    "interface GigabitEthernet0/1",
    "no mtu",
    "interface GigabitEthernet0/2",
    "no mtu",
    "interface GigabitEthernet0/3",
    "no mtu"
],


```

##### State: Overridden - Loop

So what does this look like if we wanted to loop over a set of interfaces? Would there be special
considerations made for the module? The answer is no. If you attempted to loop over a module that is
using the state of **overridden**, then you are going to default the other interfaces. Given the
following task:

```yaml

  tasks:
    - name: "TASK 1: IOS >> Set some interfaces with merge"
      ios_interfaces:
        state: overridden
        config:
          - name: "{{ item }}"
            enabled: yes
            description: "Configured by Ansible"
      register: ios_interface_output
      loop:
        - "GigabitEthernet0/2"
        - "GigabitEthernet0/3"
      loop_control:
        loop_var: item

    - name: "TASK 2: SYS >> DEBUG OUTPUT"
      debug:
        msg: "{{ ios_interface_output }}"


```

You will have two loops. The first time through the loop when the loop_var is `GigabitEthernet0/2`
you will have the other interfaces all defaulted, except `GigabitEthernet0/2` will have the state
enabled and the description set to `Configured by Ansible`. The rest of the interface descriptions
will be removed. MTU all set to default, and so on.  

The second time through the loop the module will configure `GigabitEthernet0/3` with each of the
interface configurations. Defaulting the rest of the interfaces on teh device. So the description
at the end of this execution for `GigabitEthernet0/2` will be blank. Even though it was configured
on the first loop through.

To handle this you will need to define the interfaces within the context of the config. Here is the
new configuration of the tasks:

```yaml

  tasks:
    - name: "TASK 1: IOS >> Set some interfaces with merge"
      ios_interfaces:
        state: overridden
        config:
          - name: "GigabitEthernet0/2"
            enabled: yes
            description: "Configured by Ansible"
          - name: "GigabitEthernet0/3"
            enabled: yes
            description: "Configured by Ansible"
      register: ios_interface_output

    - name: "TASK 2: SYS >> DEBUG OUTPUT"
      debug:
        msg: "{{ ios_interface_output }}"


```

With having multiple interfaces defined under the config as another list item you are able to get
both of the interfaces configured with what you are looking to do.

```yaml linenums="1"


        "after": [
            {
                "enabled": true,
                "name": "loopback0"
            },
            {
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/0",
                "speed": "auto"
            },
            {
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/1",
                "speed": "auto"
            },
            {
                "description": "Configured by Ansible",
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/2",
                "speed": "auto"
            },
            {
                "description": "Configured by Ansible",
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/3",
                "speed": "auto"
            }
        ],
        "before": [
            {
                "enabled": true,
                "name": "loopback0"
            },
            {
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/0",
                "speed": "auto"
            },
            {
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/1",
                "speed": "auto"
            },
            {
                "description": "BEFORE ANSIBLE",
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/2",
                "speed": "auto"
            },
            {
                "description": "BEFORE ANSIBLE",
                "duplex": "auto",
                "enabled": true,
                "name": "GigabitEthernet0/3",
                "speed": "auto"
            }
        ],
        "changed": true,
        "commands": [
            "interface GigabitEthernet0/2",
            "description Configured by Ansible",
            "interface GigabitEthernet0/3",
            "description Configured by Ansible"


```

You now see within the _commands_ key that both of hte interfaces are configured by Ansible. At this
point with both interfaces being defined in the config parameter, you get both of the interfaces
configured. To do this more programmatically  you would need to create the list ahead of time and
feed the list of interfaces with their state into the module. This may be a future blog post.

#### State: Deleted

The task looks straight to the point for the deleted status. As expected. In this you define which
interface name is to have the configuration removed, and then the module will default all of the
sub-parameters of _description_, _duplex_, _enabled_, _mtu_, and _speed_. Note that the _enabled_
default in the module is currently (2020-01-26) set to enabled.

```yaml


  tasks:
    - name: "TASK 1: IOS >> Set some interfaces with merge"
      ios_interfaces:
        state: deleted
        config:
            - name: GigabitEthernet0/3
        register: ios_interface_output

    - name: "TASK 2: SYS >> DEBUG OUTPUT"
      debug:
        msg: "{{ ios_interface_output }}"


```

When the configuration previously had an interface description and an MTU set, the following is
the commands that are executed on just the single interface that is defined in the task:

```yaml linenums="1"


"commands": [
    "interface GigabitEthernet0/3",
    "no description",
    "no mtu"


```
