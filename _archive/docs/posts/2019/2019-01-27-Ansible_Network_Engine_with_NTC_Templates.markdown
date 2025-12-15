---
authors: [jvanderaa]
toc: true
date: 2019-01-27
layout: single
comments: true
slug: ansible-network-engine-ntc-templates
title: Ansible Network Engine and NTC Templates
# collections:
#   - Cisco
#   - Ansible
# categories:
#   - Ansible
#   - Cisco Automation
tags:
  - ansible
  - ntc
  - parsing
  - cisco
sidebar:
  nav: ansible
---

In this post we will talk about primarily three components that will work together to get structured
data out of the command line of a Cisco device. The three pieces are:

<!-- more -->

- [Ansible Network Engine](https://github.com/ansible-network/network-engine)  
- [Google's TextFSM](https://github.com/google/textfsm)
- [Network to Code Templates](https://github.com/networktocode/ntc-templates)

## Why this Post?

I'm writing this post because I was initially hesitant to start using the Ansible role originally
when I was doing everything pretty well with the generic modules that come available with Ansible. I
was challenged to migrate a Python script that was using TextFSM and Netmiko to be in Ansible. So I
was originally aware of Ansible Network Engine, but had not done anything with it. So what better
time than to put it to practice than when it is needed.

## Ansible Network Engine

The Ansible network engine is an Ansible role that is being developed by the Red Hat Ansible team.
From the Github page:

> This role provides the foundation for building network roles by providing modules and plug-ins that
> are common to all Ansible Network roles.

Within Ansible Network Engine you have the ability to `parse` the output of text. You can write your
own parser, or leverage some work that has been done by others (and willing to put the work out for
the good of the community - not stealing it).

> I'm going to recommend to read more on Ansible Network Engine parser with your own text parsing to
> go to this site - https://termlen0.github.io/2018/06/26/observations/
> This post is more about using already existing TextFSM parsers with the help from NTC than the
> parser itself.
>
> A second link found recently is from the Ansible linklight (learning) team. Take a look here if
> wanting to do more with Parsers. https://github.com/ansible/workshops/tree/master/exercises/ansible_network/supplemental/3-1-parser

### TextFSM

From the Github page: 

> TextFSM is a Python module which implements a template based state machine for parsing
> semi-formatted text. Originally developed to allow programmatic access to information returned
> from the command line interface (CLI) of networking devices.

Basically the gist of things is that TextFSM takes text that is output from a show command and puts
it into structured data. It does this using a regex pattern matching setup under the hood. This can
be helpful for grabbing information out of a text blob issues to networking devices.

You **must** first install the textfsm python module for this to work. To install, I recommend
installing on both Python2 and Python3 in case the Ansible version is still using Python2:

```
pip install textfsm
```

```
pip3 install textfsm
```

### TextFSM Parser

Digging into the code on the Ansible Network Engine Github page you will find the file:
https://github.com/ansible-network/network-engine/blob/devel/library/textfsm_parser.py

This is the TextFSM parser engine that is able to be leveraged. Looking at the Python file and the
`EXAMPLES` section you can find much more information about how to leverage the particular module.
From the Python file it has the following section:

```yaml

- name: store returned facts into a key call output
  textfsm_parser:
    file: files/parser_templates/show_interface.yaml
    content: "{{ lookup('file', 'output/show_interfaces.txt') }}"
    name: output

```

Breaking this down further helps to get to the point. 

Line 1: This is the name of the Ansible task, nothing new here  
Line 2: Calls the plugin `textfsm_parser`  
Line 3: `File`, this is the parsing file that you are leveraging in the task, and where you would
call the file location for the ntc template
Line 4: `Content`, this is what you are going to send through the parser. In the example given it is
a file, but you can also have a variable of say output from a previous command run put in here
Line 5: `name`, this is where you will store the output data, it will be in a structured format

> This will not get into reading the output of the structured data. For more on that please take a
> look back at my [previous post on working without output](https://josh-v.com/blog/2019/01/05/ansible-output-work.html) 

The original tricky part was the part about the `File`. Originally a lot of posts related to having
a parser file all set to go. My original thinking was I don't see those parsers, but they are in the
examples. I decided to try to point the textfsm parser at an NTC template that had been downloaded.
After this, success. 

`Content` is the text that you want to send through the parser. So a variable or a text file

The `name` portion is what you are _registering_ as facts that can be accessed underneath
`ansible_facts`. 

### NTC Templates

NTC (Network to Code) has a community environment with a significant number of parsers available. I
have found these particularly helpful in the Cisco environment. To install - checkout the Github
page.

https://github.com/networktocode/ntc-templates

These are files, so the best methodology I have found is to download these to your machine using the
git process of cloning. There are updates made regularly, so make sure to do `git pull` to get the
most recent version. 

> Pro tip: You may want to install these to your home directory. This is the default directory if
> memory serves me right that Netmiko will look for the textfsm templates as well

## Sample

Here is the playbook that I will run against the lab environment.

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
  roles:
    - ansible-network.network-engine

  tasks:

    - name: CLI >> Get CDP neighbors
      ios_command:
        commands:
          - show cdp neighbors
      register: command_output

    - name: SYS >> Parse CDP Information
      textfsm_parser:
        file: "/opt/ntc-templates/templates/cisco_ios_show_cdp_neighbors.template"
        content: "{{ command_output.stdout[0] }}"
        name: cdp_facts

    - name: DEBUG >> Print output
      debug:
        msg: "{{ ansible_facts.cdp_facts }}"

```

#### Task 1: Get CDP Neighbor information

This task is going to log in and get the CDP neighbor information from the device and register it to
a fact `command_output`

#### Task 2: Send through the parser

This is where the parser comes in, it will take the command output taken in the first task and send
it through the textfsm parser. This then registers the information underneath `ansible_facts`. The
next task is where you will see that output.

#### Task 3: Prints the output

You will see the information underneath the `ansible_facts` to get at the information as it sits
parsed.

### Sample Output

```bash linenums="1"
PLAY [Switch config] *******************************************************************************

TASK [CLI >> Get CDP neighbors] ********************************************************************
ok: [sw01]

TASK [SYS >> Parse CDP Information] ****************************************************************
ok: [sw01]

TASK [DEBUG >> Print output] ***********************************************************************
ok: [sw01] => {
    "msg": [
        {
            "CAPABILITY": "R S",
            "LOCAL_INTERFACE": "Gig 1/0",
            "NEIGHBOR": "Switch",
            "NEIGHBOR_INTERFACE": "Gig 1/0",
            "PLATFORM": "I"
        },
        {
            "CAPABILITY": "R S",
            "LOCAL_INTERFACE": "Gig 1/1",
            "NEIGHBOR": "Switch",
            "NEIGHBOR_INTERFACE": "Gig 1/1",
            "PLATFORM": "I"
        },
        {
            "CAPABILITY": "R",
            "LOCAL_INTERFACE": "Gig 0/0",
            "NEIGHBOR": "router_edge",
            "NEIGHBOR_INTERFACE": "Gig 0/2",
            "PLATFORM": "B"
        }
    ]
}

PLAY RECAP *****************************************************************************************
sw01                       : ok=3    changed=0    unreachable=0    failed=0
```


## Summary

Putting all of these together into a playbook you can more easily get at information presented from
a network device command line. Let's say you wanted to get CDP neighbors. The CDP neighbor command
output is tough to work with, other than seeing if something is in the output. 
