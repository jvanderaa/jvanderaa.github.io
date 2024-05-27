---
authors: [jvanderaa]
toc: true
date: 2018-06-07
layout: single
slug: ansible-blocks
comments: true
title: Ansible Blocks
tags: ["ansible"]
---
One of the more interesting features that I have just come across within the Ansible automation
world is that of the `block`. I find this very helpful for both error handling, and also grouping
tasks into logical separation.

## Ansible Official Link

[Ansible Docs: Block](https://docs.ansible.com/ansible/latest/user_guide/playbooks_blocks.html)
> Blocks allow for logical grouping of tasks and in play error handling. Most of what you can apply
> to a single task can be applied at the block level, which also makes it much easier to set data
> or directives common to the tasks. This does not mean the directive affects the block itself, but
> is inherited by the tasks enclosed by a block. i.e. a when will be applied to the tasks, not the
> block itself.

## So what is this about?

The primary reason to use blocks within Ansible is for error handling. I liken this a lot to the Python `try:` and `except:` exception handling. You are able to group tasks into one error "group" and then provides for rescue blocks and always executes blocks. This can be extremely helpful.

## Using with when

I've found that a second place to put in blocks within Ansible is to also pair it with a `when:` statement to help separate out tasks. Some may put this into a different play, but the down side of this is when you are leveraging variables. With separate plays you will be defining variables within each play. With using blocks to define what to do when, can be very helpful.
