---
authors: [jvanderaa]
toc: true
date: 2019-10-20
layout: single
comments: true
slug: ansible-cli-vs-ios-command
title: Ansible differences between ios command and cli command
# collections:
#   - Cisco
#   - Ansible
# categories:
#   - Ansible
#   - Cisco Automation
tags:
  - ansible
  - cisco
  - ios_command
  - cli_command
sidebar:
  nav: ansible
---

In an earlier [post](https://josh-v.com/blog/2019/01/12/ansible-cli-vs-ios-high-level.html) I
covered the differences between `ios_config` and  `cli_config`. However I did not cover what the
difference was between `ios_command` and `cli_command`. Most of the items covered there remain the
same. So this will be a post that mostly gets straight to it and sees what the difference is.  

> A reminder that I am also putting playbooks used here out on Github. You can find this at:
> https://github.com/jvanderaa/ansible-using_ios

## Differences

First, for the `cli_commands` module, you must be using a connection method of `network_cli`. You
should not use `connection: local` for this module. Note that the `cli_command` can also be used
with multiple device types, including multiple vendors. Take a look at the `cli_command`
documentation page that there is a link at the bottom of the post.

### Parameters

As in the config modules, the first difference is how you pass what you wish to have executed. With
`cli_command` you are sending a single string, just one command. This is under the **command**
parameter. With `ios_command` you get to send a **list of commands** send with the **commands**
parameter. This _can_ be handy in some times to execute a whole bunch of commands in one task to a
device.

### Output

The second major difference according to the documentation between `cli_command` and `ios_command`
is the return format. Assuming a single command on the `ios_command` side of things is sent, here
are the returns from the module:

#### ios_command returns

- failed_conditions
- stdout
- stdout_lines

#### cli_command returns

- json
- stdout

#### Analysis of returns

The first thing about the **stdout_lines** output is that it makes it very human readable what the
output of the command is. If you are working on something programmatically speaking, you will likely
only want to use **stdout**.  

Next we see that cli_command has a json return, which is going to provide more structured feedback
from the command.  

Both have in common the **stdout** return, however, the data type is **very** different. Since
`cli_command` sent only a single string, the return is a single string. On `ios_command` this is a
list of responses. Even if you sent a single command, it comes back as a list that is only one item.
So you will need to access `variable_name.stdout.0` (or `variable_name.stdout[0]`) to get at the
command output.  

Let's get to taking a look at the output.

## Demo of commands

Let's take a look at how the responses look with just a single command first. I have a preference of
taking a look at NTP associations lately.

### ios_command - single command

Here is what the task portion of the playbook looks like with a single command.  

```yaml linenums="1"


tasks:
  - name: "TASK 1: Get NTP Associations"
    ios_command:
      commands:
        - show ntp associations
    register: command_output

  - name: "TASK 2: Debug output"
    debug:
      msg: "{{ command_output }}"


```}

The output from this is as follows assuming an NTP association to the cloudflare NTP servers:  

```yaml linenums="1"


PLAY [PLAY 1: Using ios_command for a single command] **********************************************

TASK [TASK 1: Get NTP Associations] ****************************************************************
ok: [r1]

TASK [TASK 2: Debug output] ************************************************************************
ok: [r1] => {
    "msg": {
        "changed": false,
        "failed": false,
        "stdout": [
            "address         ref clock       st   when   poll reach  delay  offset   disp\n*~162.159.200.123 10.72.8.95       3     14     64     7 21.111  72.531  0.746\n * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured"
        ],
        "stdout_lines": [
            [
                "address         ref clock       st   when   poll reach  delay  offset   disp",
                "*~162.159.200.123 10.72.8.95       3     14     64     7 21.111  72.531  0.746",
                " * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured"
            ]
        ]
    }
}

PLAY RECAP ************************************************************************************************************
r1                         : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```

![IOS Command Single](/images/2019/10/blog-ios_single.gif)

There are four items returned, with the first two primarily being "standard" Ansible returns for
`changed` and `failed`. There is then:

- `stdout`: **List** of outputs, so when there are multiple commands.
- `stdout_lines`: **List** of **lists**, the inner list is the commands printed line by line, which
makes it more human readable. The outer list is like that of stdout, that is for each command run,
including if there is only a single command. **Look at the end of line 11, and line 13**. This shows
that there is in fact a list [] of responses to parse through.  

### cli_command - single command

The tasks on the `cli_command` looks pretty similar. However there a few differences. First the
value of `command:` is a string, this you will see by not having a `-` in the line. I'm also going
to use quotes around to demonstrate this.

```yaml


tasks:
  - name: "TASK 1: Get NTP Associations"
    cli_command:
      command: "show ntp associations"
    register: command_output

  - name: "TASK 2: Debug output"
    debug:
      msg: "{{ command_output }}"


```

The command output looks awfully similar now in recent versions of Ansible.

```yaml linenums="1"


PLAY [PLAY 1: Using cli_command for a single command] ****************************************************************************

TASK [TASK 1: Get NTP Associations] **********************************************************************************************
ok: [r1]

TASK [TASK 2: Debug output] ******************************************************************************************************
ok: [r1] => {
    "msg": {
        "changed": false,
        "failed": false,
        "stdout": "address         ref clock       st   when   poll reach  delay  offset   disp\n*~162.159.200.123 10.72.8.95       3     50     64   377 16.772  28.507  5.117\n * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured",
        "stdout_lines": [
            "address         ref clock       st   when   poll reach  delay  offset   disp",
            "*~162.159.200.123 10.72.8.95       3     50     64   377 16.772  28.507  5.117",
            " * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured"
        ]
    }
}

PLAY RECAP ***********************************************************************************************************************
r1                         : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```

![CLI Command Single](/images/2019/10/blog-cli_single.gif)

The big difference here is that the **stdout** part of the response is of type string, and not of a
type list like `ios_command`. Take a look at line number 11 where **stdout** is. Immediately
following the colon is a double quote, indicating that this is a string. So if you are doing work on
this variable, you will need to take string actions.

### ios_comamnd - multiple commands

The "bonus" of the ios_command module is that you can run multiple commands within a single task. As
I type that out, it seems against the idea of individual task execution, to do 2 or more things in a
single task. But that is what the module allows us in this instance. Let's take a look at this
playbook to verify NTP information and then get the time from the device.

> This could be a part of the `ios_command` history as well. When `ios_command` was written each
> individual task would start a new connection to IOS devices. So to preserve the number of logins
> required it would be good to be able to execute multiple lines.

There is now a single task, but there are two commands in the commands section. These will be run
and saved to a variable named `command_output`.

```yaml

- name: "TASK 1: Get NTP Associations"
  ios_command:
    commands:
      - show ntp associations
      - show clock
  register: command_output

- name: "TASK 2: Debug output"
  debug:
    msg: "{{ command_output }}"


```

Let's take a look at how this looks now:

```yaml linenums="1"


PLAY [PLAY 1: Using ios_command for a single command] ****************************************************************************

TASK [TASK 1: Get NTP Associations] **********************************************************************************************
ok: [r1]

TASK [TASK 2: Debug output] ******************************************************************************************************
ok: [r1] => {
    "msg": {
        "changed": false,
        "failed": false,
        "stdout": [
            "address         ref clock       st   when   poll reach  delay  offset   disp\n*~162.159.200.123 10.72.8.95       3    262    512   377 16.551  65.112  0.097\n * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured",
            "21:57:28.776 UTC Sun Oct 20 2019"
        ],
        "stdout_lines": [
            [
                "address         ref clock       st   when   poll reach  delay  offset   disp",
                "*~162.159.200.123 10.72.8.95       3    262    512   377 16.551  65.112  0.097",
                " * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured"
            ],
            [
                "21:57:28.776 UTC Sun Oct 20 2019"
            ]
        ]
    }
}

PLAY RECAP ***********************************************************************************************************************
r1                         : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```

![IOS Command Multiple](/images/2019/10/blog-ios_multiple.gif)

This is where you start to see that there are multiple list items in the response. Taking a look at
line number 11 we still have the `[` of the list showing at the end, then line 12 ends in a comma,
indicating the next list item. Line 13 ends the list. This repeats on the stdout_lines as well.  

If you wanted to get at just the time of the device in this instance, this is how you would do a
debug task for it:

```yaml


- name: "Debug time"
  debug:
    msg: "{{ command_output.stdout[1] }}"


```

You see that you need to call the variable name, then the return value that you are looking for - 
stdout. Then you need the list position on the response that corresponds to where it was called on
the `ios_command` module.  

### cli_command - multiple commands

To do the same multiple commands on the `cli_command` front, you will want to use a loop. Here I
prefer to use the `with_items` loop. You will see several more key/value pairs on the variable when
using a loop, so let's take a look below:

```yaml

- name: "TASK 1: Get NTP Associations"
  cli_command:
    command: "{{ item }}"
  register: command_output
  with_items:
    - "show ntp associations"
    - "show clock"

- name: "TASK 2: Debug command output"
  debug:
    msg: "{{ command_output }}"


```

The output:

```yaml linenums="1"


PLAY [PLAY 1: Using cli_command for a single command] ****************************************************************************

TASK [TASK 1: Get NTP Associations] **********************************************************************************************
ok: [r1] => (item=show ntp associations)
ok: [r1] => (item=show clock)

TASK [TASK 2: Debug command output] **********************************************************************************************
ok: [r1] => {
    "msg": {
        "changed": false,
        "msg": "All items completed",
        "results": [
            {
                "ansible_loop_var": "item",
                "changed": false,
                "failed": false,
                "invocation": {
                    "module_args": {
                        "answer": null,
                        "check_all": false,
                        "command": "show ntp associations",
                        "prompt": null,
                        "sendonly": false
                    }
                },
                "item": "show ntp associations",
                "stdout": "address         ref clock       st   when   poll reach  delay  offset   disp\n*~162.159.200.123 10.72.8.95       3     64    128   377 16.354 -25.131  2.283\n * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured",
                "stdout_lines": [
                    "address         ref clock       st   when   poll reach  delay  offset   disp",
                    "*~162.159.200.123 10.72.8.95       3     64    128   377 16.354 -25.131  2.283",
                    " * sys.peer, # selected, + candidate, - outlyer, x falseticker, ~ configured"
                ]
            },
            {
                "ansible_loop_var": "item",
                "changed": false,
                "failed": false,
                "invocation": {
                    "module_args": {
                        "answer": null,
                        "check_all": false,
                        "command": "show clock",
                        "prompt": null,
                        "sendonly": false
                    }
                },
                "item": "show clock",
                "stdout": "02:19:22.598 UTC Mon Oct 21 2019",
                "stdout_lines": [
                    "02:19:22.598 UTC Mon Oct 21 2019"
                ]
            }
        ]
    }
}

PLAY RECAP ***********************************************************************************************************************
r1                         : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


```

![CLI Command Multiple](/images/2019/10/blog-cli_multiple-looping.gif)

In this execution we now have to get at the information within the results section. You do however
also get the command in the output, as well as some other module arguments, which can be handy! To
get at the results from `show ntp associations` you will need to use
`command_output.results[0].stdout` and `command_output.results[1].stdout` to get at the results of
`show clock`. 

## Summary

I hope this has been valuable to you as a reader. With `cli_command` still relatively new, having
been released in Ansible 2.7, I expect that it will continue to evolve. Take a look at the docs
pages for these here:

[cli_command](https://docs.ansible.com/ansible/latest/modules/cli_command_module.html)  
[ios_command](https://docs.ansible.com/ansible/latest/modules/ios_command_module.html)  