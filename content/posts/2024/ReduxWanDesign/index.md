---
date: 2024-05-31
slug: redux-wan-design
categories:
- networking
- nautobot
- redux
title: 'Redux: WAN Design'
toc: true
tags:
- redux
author: jvanderaa
params:
  showComments: true
---

In this post, we'll dive into WAN design and address a common question that I was provided with in the 2000s: "My home internet costs only $35 per month. Why do we spend $xxx per month per circuit?"

<!--more-->

This question is one that WAN engineers in 2024 and beyond shouldn't have to worry about. As long as we design for the expected availability (which I discussed in a previous [post](https://josh-v.com/designing-wan-availability/)), the types of circuits are no longer a major concern.

## Scenario

The WAN environment we supported hosted many critical applications essential for daily business operations, including revenue processing (online sales were still in their infancy back then). Our design was "cookie cutter," meaning all locations were identical. This approach meant using the same type of circuit for each site, limiting us to a few suppliers and reducing competition.

There were minor differences in hardware at each location, and we used one-time config generation templates to handle these differences, with logic built into the templates for the type of WIC installed on the router.

## What I Would Do Differently

Initially, I thought the only change I'd make was using a more accessible circuit database. However, as I wrote, I realized another improvement: updating the template generator. Let's explore these two changes.

### Solution: Circuit Warehouse/Database

First, I would use a SOT (Source of Truth) like Nautobot as a Circuit Warehouse/Database. Nautobot can track essential details like circuit ID, provider, type of circuit, and the connection point. You can see an example in the [Nautobot demo](https://demo.nautobot.com/circuits/circuits/6b2c4c96-2b3e-4533-b085-9fe31a58dbdc/?tab=main), where a circuit is connected to `sin01-edge-01` on interface `Ethernet16/1`.

![Nautobot Circuit View](image.png)

With this information, I could use Python or Ansible to generate interface configurations. Nautobot's API provides variables for IP addressing, interface type, port speed, shaping configuration, and more. This flexibility allows for different circuit types and service providers across the environment. Plus, with Nautobot's data readily available, operational efficiency improves. Tools like [Nautobot ChatOps](https://docs.nautobot.com/projects/chatops/en/latest/user/app_overview/) can bring this information to your help desk team via MS Teams, WebEx, Slack, or Mattermost.

At the time, our Telecom Expense Management (TEM) system focused on expenses rather than data accessibility. Even if it had API capabilities, I wasn't aware of APIs back then, so I wouldn't have known how to extract the data. Learning how to use REST APIs is well worth the time investment.

### Update the Template Generator to Run On Demand

The generator script I inherited was written in Perl and tied to a spreadsheet that needed updating before execution. While Perl isn't inherently bad, it was challenging for me to understand at the time.

I should have updated this command-line utility to accept CLI inputs for single-device configuration generation. Python 2.6 had just been released, but I didn't encounter Python until 2015.

#### Templating Configurations Today

Today, I'd use [Python Jinja](https://jinja.palletsprojects.com/en/3.1.x/) for configuration templates. Jinja integrates well with [Python](https://www.python.org/), [Ansible](https://www.ansible.com/), [Nautobot Golden Configuration](https://docs.nautobot.com/projects/golden-config/en/latest/), and many other network automation projects, making it the best choice for templated configuration generation.

## Summary

Change is constant, and my approach to WAN design has evolved. Previously, we aimed for native Ethernet service everywhere from a single provider. Now, it's about finding the right provider for each location. Using a Circuit Warehouse/Database like Nautobot to manage site-level details ensures the configuration works seamlessly at each site.
