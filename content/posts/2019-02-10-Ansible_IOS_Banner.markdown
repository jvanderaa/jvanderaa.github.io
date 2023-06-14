---
author: Josh VanDeraa
toc: true
date: 2019-02-10 07:00:00+00:00
layout: single
slug: ansible-ios-banner
title: Ansible IOS Banner
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
  - ios_banner
sidebar:
  nav: ansible
---

Today's post is going to be a short and sweet one (unless I get to writing two). I'm going to take a
look at `ios_banner` module. This one is pretty much straight to the point, what it states,
modifying the banner on an IOS device. There are multiple reasons to want to manipulate the banner
on a Cisco device. We will leave those reasons to you and the organization that you are a part of
for that. For now, we will take a real quick look at the module.

## Module Documentation

First, the module documentation page is
[here](https://docs.ansible.com/ansible/latest/collections/cisco/ios/ios_banner_module.html).

## Getting Started with the Lab

I'm starting out with no banner on the page of my system as evident from this login:

**Cisco Router Login**

{{< highlight bash "linenos=table">}}
Escape character is '^]'.

Username: 

{{< /highlight>}}

### IOS Banner Play / tasks

Let's go ahead and apply a banner to the login with the following tasks:

```yaml

    - name: IOS >> Set banner to single login
      ios_banner:
        banner: login
        state: present
        text: "Quick banner, this device is being managed by Ansible."
      register: output

    - name: DEBUG >> Output
      debug:
        msg: "{{ output }}"

```

I now have the following banner showing up on the login to the Cisco device over SSH.

**Banner on Router**

{{< highlight bash "linenos=table">}}
Quick banner, this device is being managed by Ansible.
{{< /highlight>}}

### Output of ios_banner

Let's take a look at the output of the `ios_banner` module when saved to a variable. We get the
following output to the screen:

{{< highlight bash "linenos=table" >}}
TASK [DEBUG >> Output] *********************************************************
ok: [rtr01] => {
    "msg": {
        "changed": true,
        "commands": [
            "banner login @\nQuick banner, this device is being managed by Ansible.\n@"
        ],
        "failed": false
    }
}
{{< /highlight>}}

There are three "outputs" to the variable. Changed, commands, and failed. 

**Changed** looks to be the true/false of was the device changed as part of the play execution.  
**comamnds** are what actually was run on the Cisco device from config mode.  
**failed** is the state of the task, true/false

## Multiline banner

To set a multi-line banner on something, it is as simple as using the `|` or `>` keys that are part
of YAML. These again are functions known within YAML and not something specific to Ansible, so this
is something that would carry over between languages/tools that are using YAML as the formatting.

```yaml

  tasks:
    - name: IOS >> Set banner to single login
      ios_banner:
        banner: login
        state: present
        text: |
          ===This device is being managed by Ansible===
          Making changes at your own risk!
      register: output

    - name: DEBUG >> Output
      debug:
        msg: "{{ output }}"

```

This has successfully added a multiple line banner to the configuration:

{{< highlight bash "linenos=table" >}}
TASK [IOS >> Set banner to single login] ***************************************
changed: [rtr01]

TASK [DEBUG >> Output] *********************************************************
ok: [rtr01] => {
    "msg": {
        "changed": true,
        "commands": [
            "banner login @\n===This device is being managed by Ansible===\nMaki
ng changes at your own risk!\n@"
        ],
        "failed": false
    }
}
{{< /highlight>}}

A quick look at the configuration itself in IOS:

{{< highlight bash "linenos=table">}}
!
banner login ^C
===This device is being managed by Ansible===
Making changes at your own risk!
^C
!
{{< /highlight>}}

This automatically puts the `^C` as the character delineation for you, as that was not something
that was specified within the module itself.

## Setting Multiple Banners

If you want to set multiple banners, say `exec`, `login`, and `motd`, you will want to change this
to leveraging `with_items`. This way Ansible will iterate and set all of these. Here is the Play.

Notice the changes on line 3 below has been changed from the banner `login` to the variable
`{{ item }}`. `with_items` has been added on line 8. And we have set this to change the banner for
`motd` (Message of the Day), `login`, and `exec`. 

```yaml

    - name: IOS >> Set banner to single login
      ios_banner:
        banner: "{{ item }}"
        state: present
        text: |
          ===This device is being managed by Ansible===
          Making changes at your own risk!
      with_items:
        - motd
        - login
        - exec
      register: output

    - name: DEBUG >> Output
      debug:
        msg: "{{ output }}"

```

**Output**
{{< highlight bash "linenos=table" >}}
TASK [IOS >> Set banner to single login] ***************************************
changed: [rtr01] => (item=motd)
ok: [rtr01] => (item=login)
changed: [rtr01] => (item=exec)

TASK [DEBUG >> Output] *********************************************************
ok: [rtr01] => {
    "msg": {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "_ansible_ignore_errors": null,
                "_ansible_item_label": "motd",
                "_ansible_item_result": true,
                "_ansible_no_log": false,
                "_ansible_parsed": true,
                "changed": true,
                "commands": [
                    "banner motd @\n===This device is being managed by Ansible===\nMaking changes at your own risk!\n@"
                ],
                "failed": false,
                "invocation": {
                    "module_args": {
                        "auth_pass": null,
                        "authorize": null,
                        "banner": "motd",
                        "host": null,
                        "password": null,
                        "port": null,
                        "provider": null,
                        "ssh_keyfile": null,
                        "state": "present",
                        "text": "===This device is being managed by Ansible===\nMaking changes at your own risk!\n",
                        "timeout": null,
                        "username": null
                    }
                },
                "item": "motd"
            },
            {
                "_ansible_ignore_errors": null,
                "_ansible_item_label": "login",
                "_ansible_item_result": true,
                "_ansible_no_log": false,
                "_ansible_parsed": true,
                "changed": false,
                "commands": [],
                "failed": false,
                "invocation": {
                    "module_args": {
                        "auth_pass": null,
                        "authorize": null,
                        "banner": "login",
                        "host": null,
                        "password": null,
                        "port": null,
                        "provider": null,
                        "ssh_keyfile": null,
                        "state": "present",
                        "text": "===This device is being managed by Ansible===\nMaking changes at your own risk!\n",
                        "timeout": null,
                        "username": null
                    }
                },
                "item": "login"
            },
            {
                "_ansible_ignore_errors": null,
                "_ansible_item_label": "exec",
                "_ansible_item_result": true,
                "_ansible_no_log": false,
                "_ansible_parsed": true,
                "changed": true,
                "commands": [
                    "banner exec @\n===This device is being managed by Ansible===\nMaking changes at your own risk!\n@"
                ],
                "failed": false,
                "invocation": {
                    "module_args": {
                        "auth_pass": null,
                        "authorize": null,
                        "banner": "exec",
                        "host": null,
                        "password": null,
                        "port": null,
                        "provider": null,
                        "ssh_keyfile": null,
                        "state": "present",
                        "text": "===This device is being managed by Ansible===\nMaking changes at your own risk!\n",
                        "timeout": null,
                        "username": null
                    }
                },
                "item": "exec"
            }
        ]
    }
}

{{< /highlight>}}

## Summary

The `ios_banner` module is a quick and handy module for those that need to have banners as part of
the operating entity. There are many reasons for banners that this is not going to explore further,
there are plenty of other resources (including possible Legal ones) available for this discussion.
Hopefully this has been a good primer of what things look like for the `ios_banner` and what output
looks like.
