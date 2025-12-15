---
toc: true
date: 2019-03-30
layout: single
slug: ansible-saving-cisco-configs-ios
title: Ansible Saving Cisco Configs to NVRAM with Cisco Specific Modules
categories:
- ansible
- cisco
- cisco_ios
- cisco_wlc
- cisco_nxos
- saving_config
sidebar:
  nav: ansible
author: jvanderaa
params:
  showComments: true
---

Today I'm going to take a look at a method to be able to save the configuration of a Cisco device to
NVRAM (copy run start). I will be taking a look at multiple Cisco platforms to save changes done
during an Ansible Playbook to NVRAM. There are options to save the configuration on every change
within the modules such as **ios_config** or **cli_config**, however, this can slow down the
execution of your playbook.

<!--more-->

First I will take a look at saving the configuration within its own task just for saving
configuration. This is how I have many of my playbooks as I'm executing several tasks, breaking them
out. I then have a dedicated task that will save the configuration. I do this for speed of the
playbook execution. If there are multiple changes on tasks and each one of the tasks is saving the
configuration, then there will be some significant time spent saving the configuration multiple
times. In this I will take a look at the copy command execution, but also, the trick I like to use
of the config module and just **save_when** parameter.

<!--more-->

The second methodology I will take a look at is the saving the configuration within the task itself,
using the **save_when** parameter. This is something that I use when I have simple playbooks, with
only a couple of tasks that will modify the configuration.

We will be taking a look at how to do this with the following Cisco platforms:

- Cisco IOS
- Cisco NXOS
- Cisco WLC

## Saving Configuration in one task

### IOS / NXOS

The method I like to use to save the configuration is to use the **ios_config** module with the
parameter of **save_when** set to _always_. No other parameter set, just the **save_when**. The
**nxos_config** and **ios_config** modules both work in the same way. I'll show both of the outputs,
but no separate write up on the NXOS side.

To save the configuration then here is the task:

#### Playbook Definition

**IOS**

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Switch config
  connection: network_cli
  hosts: rtr02
  gather_facts: no
  become: yes
  become_method: enable
  tasks:
    - name: IOS >> Save Configuration to NVRAM
      ios_config:
        save_when: always
      register: output

    - name: DEBUG >> output
      debug:
        msg: "{{ output }}"


```

**NXOS** 

```yaml


---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Switch config
  connection: network_cli
  hosts: nxos_switches
  gather_facts: no
  tasks:
    - name: NXOS >> Save Configuration to NVRAM
      nxos_config:
        save_when: always
      register: output

    - name: DEBUG >> output
      debug:
        msg: "{{ output }}"


```

#### Playbook Execution

On the output from the playbook, you don't get a lot of feedback that the config is copied other
than the task being successful. However, since I'm using a vIOS image in my lab environment the
console does show GRUB messages. The second output shows the successful saving of the configuration
that was done as the Ansible Playbook was being executed.

**Playbook Execution - IOS**

```yaml linenums="1"


PLAY [Switch config] ***********************************************************

TASK [IOS >> Save Configuration to NVRAM] **************************************
changed: [rtr02]

TASK [DEBUG >> output] *********************************************************
ok: [rtr02] => {
    "msg": {
        "changed": true, 
        "failed": false
    }
}

PLAY RECAP *********************************************************************
rtr02                      : ok=2    changed=1    unreachable=0    failed=0  


```


**GRUB Output - IOS**

```yaml linenums="1"


*Mar 30 16:51:15.832: %GRUB-5-CONFIG_WRITING: GRUB configuration is being updated on disk. Please wait...
*Mar 30 16:51:16.446: %GRUB-5-CONFIG_WRITTEN: GRUB configuration was written to disk successfully


```

**NXOS Execution**

Here the output is minimal, with the output reporting success as our only method to know that the
configuration was in fact saved.

```yaml linenums="1"


PLAY [Switch config] ***********************************************************

TASK [NXOS >> Save Configuration to NVRAM] *************************************
changed: [nxos01]

TASK [DEBUG >> output] *********************************************************
ok: [nxos01] => {
    "msg": {
        "changed": true, 
        "failed": false
    }
}

PLAY RECAP *********************************************************************
nxos01                     : ok=2    changed=1    unreachable=0    failed=0 


```


#### Method with IOS_Command

Not recommended, but if you must.  

Here there are two options for using a dedicated task for saving the configuration. The second method
requires specific configuration to be added, which is something that I don't really like to have to
do. You would use the configuration `file prompt quiet` within the configuratoin of the IOS device,
then you can use the **ios_command** module to issue `copy run start`.

### Cisco WLC - Save Configuration aireos_command

I have not been able to test the methodology of using **save_when** on the Cisco Wireless
Controllers yet, but the methodology that I have used is using the command module. The difficulty on
the aireos_command module is that there really isn't a methodology to handle prompts yet. This is 
actually very easy to overcome however on the module using escape characters.

Here you see a `\r` in the middle of the output before the response of `y` for do you wish to save.
You do not need one on the end as there is an implicit carriage return at the end of any line within
the modules.

Using the **aireos_command** module task looks like this:

```yaml

- name: WLC >> Save Configuration
  aireos_command:
    commands:
      - "save config\ry"


```

## Saving Configurations on Each Task

When looking at the four modules of **ios_config**, **nxos_config**, **cli_config**, and
**aireos_config** you will find that there is an parameter for either **save** or **save_when**. The
parameter **save** is something that is being deprecated and I would not recommend using this. All
of these modules will flag deprecation warnings on Ansible version 2.7.

| Module        | Deprecated Parameter <br /> Move Away | Current Save <br />Parameter                 |
| ------------- | ------------------------------------- | -------------------------------------------- |
| ios_config    | save (yes, no)                        | save_when (always, never, modified, changed) |
| nxos_config   | save (yes, no)                        | save_when (always, never, modified, changed) |
| aireos_config | save (yes, no)                        | save_when (always, never, modified, changed) |

> Note: I do not actively have a Cisco Wireless Controller available in my lab at the time of the 
> writing. From working in my production environment, the configuration being save follows closely
> to that of the **ios_config** or **nxos_config** modules.

### Module Details Links

[aireos_config](https://docs.ansible.com/ansible/latest/modules/aireos_config_module.html)  
[ios_config](https://docs.ansible.com/ansible/latest/modules/ios_config_module.html)  
[nxos_config](https://docs.ansible.com/ansible/latest/modules/nxos_config_module.html)  

### Parameter Choices

- always  
- never  
- modified  
- changed  

### Choices Detail

> When changes are made to the device running-configuration, the changes are not copied to
> non-volatile storage by default. Using this argument will change that before. If the argument is
> set to always, then the running-config will always be copied to the startup-config and the
> modified flag will always be set to True. If the argument is set to modified, then the
> running-config will only be copied to the startup-config if it has changed since the last save to
> startup-config. If the argument is set to never, the running-config will never be copied to the
> startup-config. If the argument is set to changed, then the running-config will only be copied to
> the startup-config if the task has made a change. changed was added in Ansible 2.6.

### ios_config save_when Parameter

This is straight forward, when you want to save the configuration after a change within each task
then you would set the parameter **save_when** to **changed**. This is advantages on simple
playbooks. Next we will take a look at a playbook with the task set to **changed**.

#### Playbook Definition

At the start, I have modified the hostname of the router that I'm going to be working on. I have set
the hostname to `router02` which you can see with the prompt being `router02#` once entering enable
mode. This playbook we will be changing the hostname of hte device to match that which is in the
Ansible inventory file.

Here is the playbook

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Switch config
  connection: network_cli
  hosts: rtr02
  gather_facts: no
  become: yes
  become_method: enable
  tasks:
    - name: IOS >> Set hostname
      ios_config:
        lines:
          - hostname {{ inventory_hostname }}
        save_when: changed
      register: output

    - name: DEBUG >> output
      debug:
        msg: "{{ output }}"

```

When looking at the startup configuration on the router this is what we have:

```yaml linenums="1"


router02#show start | i hostname
hostname router02


```


#### Playbook Execution

We see that the configuration was updated with the command:

```
hostname rtr02
```

```yaml linenums="1"


PLAY [Switch config] ***********************************************************

TASK [IOS >> Set hostname] *****************************************************
changed: [rtr02]

TASK [DEBUG >> output] *********************************************************
ok: [rtr02] => {
    "msg": {
        "banners": {}, 
        "changed": true, 
        "commands": [
            "hostname rtr02"
        ], 
        "failed": false, 
        "updates": [
            "hostname rtr02"
        ]
    }
}

PLAY RECAP *********************************************************************
rtr02                      : ok=2    changed=1    unreachable=0    failed=0   



```

After the execution we have the startup configuration with the new name, just as we expected

```yaml linenums="1"


rtr02#show start | i hostname
hostname rtr02


```

#### Second Execution of the ios_config module

I'm going to run the same playbook once again, to show that the module has the smarts to not change
the configuration since it is set. Note the **changed** output is set to _false_.

```yaml linenums="1"


PLAY [Switch config] ***********************************************************

TASK [IOS >> Set hostname] *****************************************************
ok: [rtr02]

TASK [DEBUG >> output] *********************************************************
ok: [rtr02] => {
    "msg": {
        "changed": false, 
        "failed": false
    }
}

PLAY RECAP *********************************************************************
rtr02                      : ok=2    changed=0    unreachable=0    failed=0  


```


### nxos_config save_when Parameter

Similar to the **ios_config** here is a run through of the same set of plays this time with a NXOS
device.

#### Playbook Definition

Once again, I have the NXOS device hostname set to something different than we would like.

The startup configuration has the hostname of `nxos_switch1` but the Ansible inventory has the name
`nxos01` for the inventory_name. 

```yaml linenums="1"


nxos_switch1# show start | i hostname
hostname nxos_switch1


```

THe playbook now looks like this:

```yaml

---
# yamllint disable rule:truthy
# yamllint disable rule:line-length
- name: Switch config
  connection: network_cli
  hosts: nxos_switches
  gather_facts: no
  tasks:
    - name: NXOS >> Set hostname
      nxos_config:
        lines:
          - hostname {{ inventory_hostname }}
        save_when: changed
      register: output

    - name: DEBUG >> output
      debug:
        msg: "{{ output }}"

```

#### Playbook Execution

Just as before we have the hostname change to match that of the Ansible inventory. 

```yaml linenums="1"


PLAY [Switch config] ***********************************************************

TASK [NXOS >> Set hostname] ****************************************************
changed: [nxos01]

TASK [DEBUG >> output] *********************************************************
ok: [nxos01] => {
    "msg": {
        "changed": true, 
        "commands": [
            "hostname nxos01"
        ], 
        "failed": false, 
        "updates": [
            "hostname nxos01"
        ]
    }
}

PLAY RECAP *********************************************************************
nxos01                     : ok=2    changed=1    unreachable=0    failed=0   


```

The show start shows that the startup configuration was changed.

```yaml linenums="1"


nxos01# show start | i hostname
hostname nxos_switch1


```

## Summary

There are multiple methods available for saving the configuration to NVRAM in the Cisco world. The
first method works very well when you have a large number of tasks and always wish to have the
startup configuration match that of the running configuration from playbook execution. If there are
small/simple playbooks with only one or two configurations being applied, it may be worth it to
have the task save the configuration. 

Hope this was helpful! 

