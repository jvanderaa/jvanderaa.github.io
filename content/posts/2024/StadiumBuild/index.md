---
date: 2024-06-19
slug: stadium-automation
categories:
- automation
- network
title: 'Redux: Stadium Automation'
toc: true
tags:
- network
- netdevops
author: jvanderaa
params:
  showComments: true
---

At a previous position to joining Network to Code I was asked to help to build automation to help with the configuration of switches going into a MLS stadium. The stadium was under construction and the network build out would take place at the same time as the stadium was being built out. It was definitely a first and maybe only opportunity that I would have to build out a new stadium.

## Scenario

The task at hand is that each of the ports would need to be configured leveraging a good L2/L3 separation with each of the service providers that provide a service to the stadium their own network segment to work through. A large number of ports were going to need to be configured.

<!--more-->

## What was Automated

There were two primary components that were automated at the onset of the project. The first part was building automation to handle the provisioning of several hundred (400+) access points. Since this was in the late 2010s, WiFi 📶 would be a key part of the system.

### Wireless Access Point Provisioning

I developed a provisioning script for the wireless LAN controller to handle over 400 access points. The script read data from a spreadsheet designed by the wireless architect and provisioned the access points into the correct WLAN groups, setting their radios according to the plan. The automation impressed the wireless architect with its flawless execution.

### Switchport Configuration

Diving into the bigger day to day component of the stadium build would be the configuration of the access ports for all of the vendors. At this point in time, there was not a good plan of exactly which vendor would be plugging into which port, which would feed back to each of the IDFs for the stadium. This is something that was planned for to be dynamic in nature and would need to be tweaked as each vendor provisioned their environment.

Each of the switch interfaces would get a configuration template for the particular VLAN, and the variables were controlled in an Infrastructure as Code (IaC) methodology. Ansible Ansible would be the automation engine and orchestrator in the environment, using [Ansible AWX](https://github.com/ansible/awx) to handle the Ansible items. Every morning at 9am (or somewhere around there), Ansible AWX would kick off the automation and re-provision every access port to match that of the configuration in the IaC definition.

This was great for having consistency and having the definition of the interfaces.

## What I Should Have Done Differently

Reflecting on the project, there are two areas I would approach differently:

1. CI/CD Deployment
2. Source of Truth
3. Automated Testing

### CI/CD Deployment

The first thing that I should have built out better at the time, if I were given the right time to do so, a proper CI/CD pipeline like Jenkins Jenkins. The only complaint about adopting the Infrastructure as Code deployment from the team of network engineers was that they couldn't get it done when they needed it to get done. So there would be ports that would get provisioned on say a Tuesday afternoon while working with the vendor. The engineer would miss getting the update into the system and the next morning their configuration would be wiped out. If I had built out a proper CI/CD system, since the deployment part of the CI/CD was already happening, then I believe that the adoption of the port update via IaC would have been significantly improved.

### Source of Truth

The second is that I would look to bring in Source of Truth as that inventory source for the interfaces. There are much more controls that can be brought forward to define the intended state of the interfaces. This would allow for the visualization of the relationships between the interfaces, the VLANs, and the L3 information. I would then incorporate webhooks on changes to the interfaces to automatically deploy the updated configuration as needed.

### Automated Testing of the Environment

I would have loved for the opportunity to have driven the technology assurance of the environment a lot further back then. It was an idea that I had back in 2018/2019 when it was being built. I had started to tinker with the idea of position a few Raspberry Pi devices around the stadium and writing a script that would join the various WiFi networks, including the fan WiFi network. Then report back on the ability to join or not. There ended up being a few other things that occupied the time of troubleshooting that in the end really should have been spent on the automated testing. But that was not a priority at the time to get completed.

## Summary

To wrap this up, I think that I had an overall positive experience automating the MLS stadium that I was involved in. There are definitely some things that I would have pushed for sooner. The experience of building the stadium network is not something that I will forget any time soon. But at the same time, it isn't something that I would say I must do again. It turns out that the priority isn't the build of the network with a stadium being built. It is the construction of the stadium itself. Rightfully so. Building a stadium network brings some unique challenges and some unique opportunities as well. Thankfully the Network Automation community has some great tools to work with that are vastly different from the past several decades, and exploration of the use of those tools together are what bring together a great story. 
