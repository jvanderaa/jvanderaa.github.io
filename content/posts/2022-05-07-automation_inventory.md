---
author: Josh VanDeraa
comments: true
date: "2022-05-07T07:00:00Z"
slug: automation-inventory
tags:
- automation
- ansible
- nornir
title: Automation Inventory
toc: true
---
This is a topic that I'm fairly opinionated on as of late is looking at what should be maintained within an inventory and the strategy of how to set up the inventory. 

> For the case of this blog post, I am going to use the term playbook to represent the automation being run. This is yes an Ansible term, but also apply this as your automation run that is using Nornir or any other automation framework.

## What Should Be In an Inventory

When taking a look at inventories there are usually a lot of options of what to include in your inventory for network devices. This can include the interfaces, VLANs on the device, BGP ASN, and connection information. For me, the _only_ thing that should be in the inventory is **connection information**. All of the other items such as BGP ASN, Interface Names, and anything else should be on a playbook by playbook basis. 

**An inventory is meant to represent what could be automated**. Because of this, extra information such as interface information should _not_ be included. Your environment may have a lot of playbooks that the interface information is relevant, but it is not always the case. And because of this, that information should be gathered at runtime as the playbook executes, not as part of the inventory.

The only thing that should be in an inventory and is the basic needs of the inventory is connection information. This includes at a minimum the IP address/hostname of the device. It may also include SSH key/API key information or username and password to connect. This is also something that may be gathered as part of the process if you maintain this information inside of a password management system (such as Hashicorp Vault).

## Inventory Strategy

When looking to set up your inventory, I would expect a minimal number of inventories. One that maintains production devices. One for development/test hosts. This may be broken up more into the teams that are responsible for particular devices, but if you can, I also argue that the devices across teams should be available within the same production inventory. This will allow for more automation collaboration to deliver results for the organization, which is the goal. There may be individual inventories for each of the scope of business, which may make sense as well, especially if there are some boundaries that may not want to be crossed.

What about different sites? Well, these should all be within groups within the organization. If you have a large number of sites or buildings with a lot of gear, this is exactly where groups fit in. Both in Ansible and Nornir there is the concept of groups, which allows for the setup of the environment. There **should not** be an inventory per building/location, as this leads to difficulty as the automation scales.

## A Look At Inventories

![Inventory Actions](/images//2022/inventory_actions.png)

Looking at the graphic above where there are 4 playbooks that you currently have. With an automation framework, your inventory should be the same inventory for each of the playbook activities. Whether it is for an OS version check, checking or configuring BGP neighbors, or configuring access interfaces. Of those examples, only the changing of the access interface playbook would need to know what the interfaces are. So to have the interfaces live in the inventory, especially if the inventory is gathered at run time, is causing unnecessary data gathering that may get in the way of automation.

## Possible Exception

One possible exception to this may be when using a system like AWX that maintains a database of inventory. In this setup, the inventory plugin execution may be run independently and at an off hours of automation usage. This would then allow for effective caching of these inventory data items. Since the inventory will then be used often without checking the source of truth for network devices, you would not be making unnecessary calls. This would still lead to ineffective loading of data though during development of playbooks. In development the inventory should be much lighter, which will allow for quick development regardless.

Hopefully this information will help to keep your automation environment up and running smoothly! Or if you are just getting started, a good place to start from!

Josh
