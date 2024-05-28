---
authors: [jvanderaa]
toc: true
date: 2020-03-14
layout: single
comments: true
slug: ansible-cisco-ios-user
title: Ansible Cisco IOS User Module
# collections:
#   - Cisco
#   - Ansible
# categories:
#   - Ansible
#   - Cisco Automation
tags:
- ansible
- cisco
- ios_user
- netdevops
- network automation
sidebar:
  nav: ansible
---

In this post I will be taking a look at some of the usability setup of managing Cisco IOS devices
with the [Ansible Cisco IOS User Module](https://docs.ansible.com/ansible/latest/modules/ios_config_module.html).
This can be very helpful for setting up managed user accounts on systems, or the backup user
accounts when you have TACACS or RADIUS setup.

The module documentation overall looks complete from what I have done for user account management on
devices in the past. There are a couple of interesting parameters available, that I may not get to
completely on this post. There is support for aggregate, meaning that you can generate the
configuration for multiple user accounts and pass it in as one. You can set a password in clear text
that gets encrypted when on the device, or you can set a hashed_password with the type of hash and
its corresponding value. And as expected with a module for setting user accounts you can also set
the privilege level for which the user account uses.

<!-- more -->


## SSH Before Setting Up SSH Keys

You have probably seen this before, but for completeness sake I did get the output of the SSH login
banner. This has the default lab setup on the device. So we do get a banner, but I'm getting
prompted for a Password as well.

```shell linenums="1"


ssh rtr-1
The authenticity of host 'rtr-1 (10.250.0.167)' can't be established.
RSA key fingerprint is SHA256:iyEgRBFlLhkW+Z2OOYWPvrjuzhTVY9wULmoHkWYgbrw.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'rtr-1' (RSA) to the list of known hosts.
Warning: the RSA host key for 'rtr-1' differs from the key for the IP address '10.250.0.167'
Offending key for IP in /Users/joshv/.ssh/known_hosts:170
Are you sure you want to continue connecting (yes/no)? yes

**************************************************************************
* IOSv is strictly limited to use for evaluation, demonstration and IOS  *
* education. IOSv is provided as-is and is not supported by Cisco's      *
* Technical Advisory Center. Any use or disclosure, in whole or in part, *
* of the IOSv Software or Documentation to any third party for any       *
* purposes is expressly prohibited except as otherwise authorized by     *
* Cisco in writing.                                                      *
**************************************************************************Password:



```

## Adding SSH Key Users

Copying from the example on the module definition, I went ahead and created a playbook that will
create an account on the same device but with my local computer account. Here is the playbook:

```yaml

---
- name: "PLAY 1: WORKING WITH IOS USER MODULE"
  hosts: cisco_routers
  connection: network_cli
  tasks:
    - name: "TASK 1: Add local username with SSH Key"
      ios_user:
        name: joshv
        nopassword: True
        sshkey: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
        state: absent
        
    - name: "FINAL TASK: Save Config"
      ios_config:
        save_when: always

```

It is a single play playbook, with 2 tasks. Task 1 will add the local id_rsa public key to the IOS
device. The final task is a play to save the configuration.

```shell linenums="1"


ansible-playbook working_with_ios_user-1.yml

PLAY [PLAY 1: WORKING WITH IOS USER MODULE] ****************************************************

TASK [TASK 1: Add local username with SSH Key] *************************************************
[WARNING]: Module did not set no_log for update_password
[WARNING]: Module did not set no_log for password_type
changed: [r1]

TASK [debug] ***********************************************************************************
ok: [r1] => {
    "msg": {
        "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python"
        },
        "changed": true,
        "commands": [
            "ip ssh pubkey-chain",
            "username joshv",
            "key-hash ssh-rsa <hash_masked> joshv@<adevice>",
            "exit",
            "exit",
            "username joshv nopassword"
        ],
        "failed": false,
        "warnings": [
            "Module did not set no_log for update_password",
            "Module did not set no_log for password_type"
        ]
    }
}

TASK [FINAL TASK: Save Config] *****************************************************************
changed: [r1]

PLAY RECAP *************************************************************************************
r1                         : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```

![Playbook1 Execution](/images/2020/03/add_user_with_key_mask.gif)

On execution one can see that the commands pushed in the debug task including setting up an IP SSH
keypair, setting a username of joshv, and setting the key hash. Then Ansible exits to what is
expected to be the first level of config mode and sets username `joshv` without a password.  

Execution is pretty much what we would expect of adding a username to the device. Taking a look at
if we get prompted when connecting to the device is a no, I do not.

```yaml linenums="1"


$ ssh rtr-1

**************************************************************************
* IOSv is strictly limited to use for evaluation, demonstration and IOS  *
* education. IOSv is provided as-is and is not supported by Cisco's      *
* Technical Advisory Center. Any use or disclosure, in whole or in part, *
* of the IOSv Software or Documentation to any third party for any       *
* purposes is expressly prohibited except as otherwise authorized by     *
* Cisco in writing.                                                      *
**************************************************************************
**************************************************************************
* IOSv is strictly limited to use for evaluation, demonstration and IOS  *
* education. IOSv is provided as-is and is not supported by Cisco's      *
* Technical Advisory Center. Any use or disclosure, in whole or in part, *
* of the IOSv Software or Documentation to any third party for any       *
* purposes is expressly prohibited except as otherwise authorized by     *
* Cisco in writing.                                                      *
**************************************************************************
rtr-1#


```

Taking a look at the configuration in the router, it looks exactly as we would expect. There are
only two users configured. The first being the one that Ansible uses to connect to this device. The
second being the one we just reconfigured.

```yaml linenums="1"


rtr-1#show run | i username
username cisco secret 5 $1$GNTQ$RpNy.E9LZMzgrOz/g2pYJ.
username joshv nopassword
  username joshv


```

On the output you see that there is the username `joshv` multiple times. One is in the generic
username section that was created with the command `username joshv nopassword` and then another time
that is within the public key section of the SSH configuration.  

### Removing SSH Key User

To go along with creating an user on the device, I have created the playbook to remove the same user
from the device. This is as simple as changing the state from `present` to `absent`. This will
remove all of what was created on the device.

```yaml

---
- name: "PLAY 1: WORKING WITH IOS USER MODULE"
  hosts: cisco_routers
  connection: network_cli
  tasks:
    - name: "TASK 1: Remove local username with SSH Key"
      ios_user:
        name: joshv
        nopassword: True
        sshkey: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
        state: absent
      register: config_output

    - debug:
        msg: "{{ config_output }}"

    - name: "FINAL TASK: Save Config"
      ios_config:
        save_when: always


```

Execution looks extremely similar. Here it is:

```yaml linenums="1"


PLAY [PLAY 1: WORKING WITH IOS USER MODULE] ****************************************************

TASK [TASK 1: Remove local username with SSH Key] **********************************************
[WARNING]: Module did not set no_log for update_password
[WARNING]: Module did not set no_log for password_type
changed: [r1]

TASK [debug] ***********************************************************************************
ok: [r1] => {
    "msg": {
        "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python"
        },
        "changed": true,
        "commands": [
            "ip ssh pubkey-chain",
            "no username joshv",
            "exit"
        ],
        "failed": false,
        "warnings": [
            "Module did not set no_log for update_password",
            "Module did not set no_log for password_type"
        ]
    }
}

TASK [FINAL TASK: Save Config] *****************************************************************
changed: [r1]

PLAY RECAP *************************************************************************************
r1                         : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```

> In writing of this I did find what I would consider a bug within Ansilbe's ios_user. If you use an
> SSH Key with the credential, you will need to remove the user account with running the same taskk
> 2 times. This is filed under issue https://github.com/ansible/ansible/issues/68238

![Playbook2 Execution](/images/2020/03/removing_user_with_key.gif)

Executing the module a second time you get the full removal of the user account.

```yaml linenums="1"


PLAY [PLAY 1: WORKING WITH IOS USER MODULE] ****************************************************

TASK [TASK 1: Remove local username with SSH Key] **********************************************
[WARNING]: Module did not set no_log for update_password
[WARNING]: Module did not set no_log for password_type
changed: [r1]

TASK [debug] ***********************************************************************************
ok: [r1] => {
    "msg": {
        "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python"
        },
        "changed": true,
        "commands": [
            {
                "answer": "y",
                "command": "no username joshv",
                "newline": false,
                "prompt": "This operation will remove all username related configurations with same name"
            }
        ],
        "failed": false,
        "warnings": [
            "Module did not set no_log for update_password",
            "Module did not set no_log for password_type"
        ]
    }
}

TASK [FINAL TASK: Save Config] *****************************************************************
changed: [r1]

PLAY RECAP *************************************************************************************
r1                         : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```

## Setting Username and Password - No Key

Now that I have gone through the use of creating a SSH Key user, let's take a look at setting an
user account on the device with a credential. I've created a local environmental variable named
`NEW_PASSWORD` that has the credential that I wish to set the username to. This could be any
lookup that gets a password, such as a lookup to a password manager.

```yaml

---
- name: "PLAY 1: WORKING WITH IOS USER MODULE"
  hosts: cisco_routers
  connection: network_cli
  tasks:
    - name: "TASK 1: Add local username with SSH Key"
      ios_user:
        name: josh2
        configured_password: "{{ lookup('env', 'NEW_PASSWORD') }}"
        state: present
        privilege: 15
      register: config_output

    - debug:
        msg: "{{ config_output }}"

    - name: "FINAL TASK: Save Config"
      ios_config:
        save_when: always


```

The output on this particular setup is **not** idempotent. Each time the play will be run it will
set a new username and password on the device due to the checking of the running configuration. You
will need to add some additional logic to your playbook to have the task only executed when a
condition is met.  

Here is the execution. Note that Ansible masks the password being set.

```yaml linenums="1"


PLAY [PLAY 1: WORKING WITH IOS USER MODULE] ****************************************************

TASK [TASK 1: Add local username with SSH Key] *************************************************
[WARNING]: Module did not set no_log for update_password
[WARNING]: Module did not set no_log for password_type
changed: [r1]

TASK [debug] ***********************************************************************************
ok: [r1] => {
    "msg": {
        "ansible_facts": {
            "discovered_interpreter_python": "/usr/bin/python"
        },
        "changed": true,
        "commands": [
            "username josh2 secret ********"
        ],
        "failed": false,
        "warnings": [
            "Module did not set no_log for update_password",
            "Module did not set no_log for password_type"
        ]
    }
}

TASK [FINAL TASK: Save Config] *****************************************************************
changed: [r1]

PLAY RECAP *************************************************************************************
r1                         : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```

![Playbook2 Execution](/images/2020/03/add_user_with_pass.gif)

## Summary

From the examples that I have given, hopefully this will help to see what you _could_ do in your own
environment. Need to regularly rotate an offline access password? A playbook may be a way that is
low impact to get you on your way for automating the management of your Cisco IOS devices.  

I also started with the use of SSH keys as well as this may be an under utilized method to log into
devices. This sets up and uses a known cryptographic key set for authentication. Please check with
the team/individuals responsible for security before implementing.  

As always, I hope this has helped!

I've added the Playbooks executed within this post to my collection of examples on Github at
https://github.com/jvanderaa/ansible-using_ios.
