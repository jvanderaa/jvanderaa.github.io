---
authors: [jvanderaa]
toc: true
date: 2020-08-11
layout: single
comments: true
slug: ansible_for_enterprise
title: Ansible for Enterprise
# categories:
# - Ansible
tags:
- ansible
- enterprise design
---

One of the appealing features that I have towards working with Ansible is that it is able to
automate components across the entire Enterprise IT stacks. Rather than having to stitch together
your network, server, and desktop automation tools, there is at least one automation tool that will
work with just about your entire IT stack. In this I will take a high level overview of some of the
features that are there for you to explore.

## Ansible for Network Automation

The first area that I will be brief on is from the network side of things. I am a long time network
engineer and that is close to my heart.  

Ansible is agentless and uses SSH as it's communication path. That leads well to interacting with
some of the more legacy network devices. Ansible also supports using the newer tooling of APIs from
devices, so until all of your entire Enterprise IT infrastructure supports API calls for automation,
Ansible can definitely fit the bill.  

The other interesting shift in the modules for networking is the move towards helping with intent
based configuration. The newer modules being written by the Ansible team have an absolute intent
configuration to them. This being that you need to send through your entire defined state to the
modules, or else they will be seen as intended to have a blank configuration. The modules will then
configure the devices as such. To see more on that look at my
[post on the interfaces module](https://josh-v.com/blog/2020/01/26/ansible-cisco-ios-interfaces-module.html).

If you are running an OS in your network that is Linux based, then you are in luck as well! Continue
to the next section about Linux automation.

## Ansible for Linux Server Automation

This is the original purpose of Ansible. It was built to automate Linux systems. Many of the core
modules that will be part of the Ansible base moving forward are modules that you use to manage
Linux systems. This is an absolute fit for the market. The times that I have written Ansible
Playbooks for Linux OS it has been a joy to work with and works very smoothly.

## Ansible for Docker

Ansible is able to automate your Docker environment as well. With support for both Docker containers
and docker-compose functionality. This will help you through your life cycle of Docker containers.
Although it does not get to the level of what Kubernetes will do from an orchestration level without
some level of effort.

## Ansible for Windows

Ansible for Windows is a thing! Although I do think it takes a little more effort to get off the
ground than even the network side. You need to enable WinRM on the Windows host for the
functionality to work. After that under the hood instead of using Python Ansible is leveraging
PowerShell code to interact with Windows OS. So yes, you can automate Windows devices.

## Ansible for MacOS

Being a *nix operating system, you can manage your Mac deployment with Ansible. Now you just need
to make sure the hosts are online when executing. So there isn't an out of the box check in agent
within Ansible. That's what makes Ansible awesome for networking is that it is agentless. Take a
look at Ansible for your Macs.

## Ansible for Cloud

I will need to find the link again, but Ansible is one of the largest percentage increase in tools
to manage your cloud environments. There are quite the number of modules available for the leading
public cloud (and private) providers. If there isn't a specific module, one characteristic of a
good cloud environment these days is the ability to have a REST API. With Ansible you can leverage
the URI module for this.  

On the cloud module front, take a look at the table below. This is the number of modules that there
are within Ansible for managing their cloud environment. In my opinion, that is quite a bit and can
get you what you need.

| Cloud         | Module Count  |
| ------------- | ------------- |
| AWS           | 45+           |
| Azure         | 169           |
| Oracle Cloud  | 30 “services” |
| Google        | 153           |
| Digital Ocean | 22            |
| Rackspace     | 26            |
| Avi Networks  | 65            |
| VMWare        | 140+          |

## Downside of Ansible

The biggest downside to leveraging Ansible would be the timeliness of execution. If you are looking
for speed on execution, then Ansible would either need some tweaks (such as installing mitogen).  

When it comes to automation, in my book the first gain is not speed. Speed is a by product of not
having to do rework and to move verification into an automated state. The real gain is by having a
consistent environment. Then moving your operations into Playbooks, which many may have heard of a
"runbook" which defines the process. Now your process is defined into a system that actually does
something.

## Summary

In my opinion Ansible is still a right tool for the job when it comes to automating both your
network environments, and your entire enterprise IT stack. I encourage you to take a look, evaluate
other options as well. I hope this summary may be helpful. Let me know your thoughts in the comments
or on Twitter/LinkedIn.

Josh