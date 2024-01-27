---
author: Josh VanDeraa
comments: true
date: 2024-01-11
slug: nautobot-app-cookie
tags:
- programming
- nautobot
title: Nautobot App Baking Cookies
toc: true
coverAlt: Cookies in random shapes
coverCaption: |
    Photo by <a href="https://unsplash.com/@caglararaz?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Caglar Araz</a> on <a href="https://unsplash.com/photos/heart-and-star-cookie-CggwlFAw8Kw?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
  
---

Just recently released at the beginning of 2024 is a project that I am super excited to see in the open source by Network to Code. This is the Nautobot App cookiecutter template. This may already be the biggest thing to become available for Network Automation in 2024. I know, its fresh at this point in the year, but this is something that is going to make getting started with your own Nautobot Application so much quicker.

## CookieCutter

First, a real quick summary and link to more documentation of what is a (CookieCutter)[https://github.com/nautobot/cookiecutter-nautobot-app]? Well, just like in making cookies with fancy designs, this is a template that will generate the entire project layout for you for a Nautobot App. Using Python [CookieCutter]([URL Coming Soon](https://cookiecutter.readthedocs.io/en/stable/)), you tell Python to build a directory structure/layout according to the template defined. 

## Nautobot

The first stop for getting started in your Network Automation journey should be to get Nautobot up and running. Get a Linux Virtual Machine, preferably Ubuntu or RHEL/RHEL derivative. From there you can follow the [Nautobot installation instructions](https://docs.nautobot.com/projects/core/en/stable/user-guide/administration/installation/) for your flavor of Linux. You should look to get a few users set up and then you can work to get your existing environment into Nautobot via the [Onboarding Plugin](https://docs.nautobot.com/projects/device-onboarding/en/latest/) followed by [Network Importer](https://github.com/networktocode/network-importer) to get the existing environment into Nautobot. This is the easiest path for getting your network ready to go. Or if you do not have a supported device type from the Network Importer process, then I have a process that leverages Ansible Facts to get the information from the network into Nautobot.

Next step now that you have data and an inventory? **My recommendation is to build a Nautobot App that you can use to install your custom code and data into Nautobot quickly and efficiently.**

## Why the Nautobot App

So why would I be looking at adding my own Nautobot App? First, it is not to recreate something that already exists. So it is not to write code to audit your network configuration. There is already a proven Nautobot App that does this for you, Nautobot Golden Config. Also, it is not to do something that you could contribute back to an open source project. It is meant to help you build, enhance, and enforce your organization's business logic. 

Nautobot Jobs are a perfect place to centralize your Python scripts that may be on a single developers workstation. To that end, if there is a script that executes business logic, or solves a problem that can then be used by a help desk team member or an application team, this will help to make your organization more productive.

Also, in an earlier post on [Custom Validators](https://josh-v.com/nautobot-remote-validation/) I covered how to apply custom validators from Nautobot on the data. In particular that post showed how you can interact with other 3rd party systems to Nautobot in order to do validation based on other services.

## Summary and Next Posts

Upcoming posts are going to get into the whats next. Where I will look at the following questions and more.

* Exploring the layout of the baked cookie
* How do you install this application into your environment?
* How to get started with Nautobot Jobs
* Nautobot Custom Validators
* Creating Your Own Views

What else would you like to see as you get started with Nautobot and your own app?

-Josh