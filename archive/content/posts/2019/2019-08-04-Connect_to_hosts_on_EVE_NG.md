---
author: Josh VanDeraa
toc: true
date: 2019-08-04 07:00:00+00:00
layout: single
slug: eveng-for-autoamtion-practice-and-testing
title: EVE-NG for Automation Practice and Testing
comments: true
# collections:
#   - Cisco
#   - Ansible
# categories:
#     - Ansible
tags:
  - eveng
  - ansible
  - network simulation
  - netdevops
sidebar:
  nav: ansible
---

As I restarted looking at how I'm continuing my education on the Network
Automation and certification realm I asked the question "How are you simulating
your network environment?" At the same time there has been thought on the idea
of leveraging cloud resources to gain experience there.  

First requirement for me is that whatever tool/simulation set that I use it has
to work. That being said, I need to be able to generate configurations, connect
devices to each other, and have packets flow through the simulated network, just
like any other network.

Second requirement is that I desire the solution to be economical. As a
**budget** for this there wasn't a lot of money left to be throwing around.  

Asking around, the third softer requirement is the solution should have a GUI of
some sorts to make things work quickly so you aren't fussing around with
creating your own middleware solution.  

My answer then to this at this point in time (2019-08-04) is EVE-NG. There is a
strong possibility of this changing in the near future based on what I saw at
2019 Cisco Live to Cisco's VIRL, but at the moment, EVE-NG and GNS3 both meet
the requirements.

If you are looking for the part about how I get at devices in the EVE-NG network
jump down to "EVE-NG for Automation Practice".  

This is not going to be a post on getting started on using the solutions.
This post assumes that you are up and running with EVE locally on your network
already. There are links further down that do help though for getting
connectivity.

## Requirements for automation

- Must be able to simulate larger networks
- Must be able to SSH to the devices directly for automation (Not just click on
and get a console window)

## Evaluation (In my mind, no formal written down)

First when looking at the cloud side of things for running EVE-NG, I had built
out an instance of EVE-NG in Google Cloud with the help of
[@showipintbri](https://twitter.com/showipintbri)'s article on
[EVE-NG in the Cloud](https://showipintbri.blogspot.com/2018/08/eve-ng-in-cloud.html).
As I looked at what I had already done with a bare metal host it appeared that
I would need to create a VPN to be able to get at the network behind the cloud
of an EVE-NG. Looking at the pricing on a VPN tunnel per minute/hour with Google
Cloud, I made the evaluation that doing this in the cloud would not be
economical.  

GNS3 has been a solid main stay for some time in the Network simulation world.
There is nothing wrong with it. I have been successful in reaching into the
GNS3 simulated world from a real network. There are some instructions on the web
about how to do so. I had basically followed this instruction set (that has been removed, using the
way back machine to get the old post) - 
[Connect GNS3 to the Internet](https://web.archive.org/web/20190521002219/https://docs.gns3.com/1vFs-KENh2uUFfb47Q2oeSersmEK4WahzWX-HrMIMd00/index.html).  

For me to get started quickly, I had recently installed an EVE-NG bare metal
installation. That is the route that I have chosen at the moment to get started
quickly. For instructions on doing a bare metal installation of EVE-NG I
followed the online docs located on the EVE-NG main page - 
[EVE-NG Bare Metal Install](https://www.eve-ng.net/documentation/installation/bare-install).

## EVE-NG for Automation Practice and Testing

So now how do we get access to the network? First within EVE-NG I **Add a New
Network** to the project. I make sure that it is set to:

* Number of Networks to build: 1
* Name/Prefix: Internet (Be creative if you wish)
* Type: **bridge**

![EVE-NG Bridge Net](/images/2019/07/eveng_add_bridge_net.png)  
The type of **bridge** is what we are looking for to enable the connectivity.  

### Connecting your router

First thing you need to do within EVE-NG is to add a router and connect it to
your _Outside_ network. I've done so as shown here:

![EVE-NG Router Host](/images/2019/07/eveng_add_bridge_host.png)  

Then the configuration on this Cisco edge device I have configured the following
on the interface that has been connected to the outside.

{{< highlight bash "linenos=table" >}}


interface GigabitEthernet0/0
 ip address dhcp
 duplex full
 speed 1000
 media-type rj45
end


{{< /highlight>}}

This allows the device to come online and get a network address. If you wanted
to prescribe what address it is in a static fashion, that is something you can
do too. I like to use DHCP to verify that the device is in fact connected to the
home network.  

### Routing

For connectivity this is where I like to start with OSPF to peer with my home
firewall. Why? First, because the firewall at home supports OSPF and why not use
routing! Secondly it is more practice with OSPF. Much of the time in my career
has been spent at places where EIGRP is the predominant IGP. It always helps to
continue to gain experience. This is where you could use a static route for your
device to send the routes back into your EVE-NG environment. You'll want to make
sure that you have routes for the networks that are in the network and that they
do not overlap with your existing home network.  

### Test Connections

Once connected, I make sure that I make sure that I'm able to connect
successfully with SSH before starting the Ansible work. You could create and get
started with a playbook and test, but I found it is easier to verify that you
have SSH connectivity natively to your devices just like you would with a
non-virtualized network.  

## Automation Testing

Now that there is connectivity to the devices on the box that you can SSH to
each device from your home network, you are able to do testing of various
playbooks. Start with some simple show commands using the **ios_command** or the
newer **cli_command** module. And then debug it. Head on over to the post my
earlier post
[Ansible - working with command output](https://josh-v.com/blog/2019/01/05/ansible-output-work.html)
for some samples on getting started with Cisco devices.  

Hope this is something that is helpful for you at home already running EVE
locally!