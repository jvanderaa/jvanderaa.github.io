---
authors: [jvanderaa]
toc: true
date: 2018-12-08
layout: single
slug: microsegmentation
comments: true
title: Micro Segmentation vs Segmentation
# collections:
#   - Cisco
#   - Ansible
# categories:
#   - Ansible
#   - Cisco Automation
tags: ["network design"]
---

In a recent podcast there was some discussion that it sounded like the term **Micro Segmentation**
was being used where it was really traditional **segmentation**. So I thought I would put out a few
thoughts on this front.

<!-- more -->

## What is Segmnentation in Networking

Segmentation is a methodology to create separatet _zones_ of sorts of various traffic types. Various
places you may want to do this is within a campus environment to separate students from faculty, or
engineering from finance. The list of examples goes on and on. Go to a basic reading of VLANs and
you will get the idea of what segmentation is. Once you have VLANs, really segmentation then builds
upon this and allows policy to be applied. This policy can be whether or not hosts should be able to
talk to each other, or various traffic treatments (QoS). This is something that is well covered
already and I do not wish to cover more.

## What is Micro Segmentation? 

So the newer term is **Micro Segmentation**. This is exactly as what was covered before but doing it
at an even more detailed level. This is getting into being able to apply policy to individual hosts
within a segment, creating a micro-segmentation effort. 

## In Practice

![SegmentDrawing](../../images/2018/12/segments.png)

| Source Host | Destination Host | Able to apply policy - Segmentation | Able to apply policy - Micro Segmentation |
| ----------- | ---------------- | :---------------------------------: | :---------------------------------------: |
| Host A      | Host B           |               **No**                |                  **Yes**                  |
| Host A      | Host C           |               **No**                |                  **Yes**                  |
| Host A      | Host D           |   Yes, at that L3 device/firewall   |                    Yes                    |
| Host B      | Host C           |               **No**                |                  **Yes**                  |
| Host B      | Host D           |   Yes, at that L3 device/firewall   |                    Yes                    |
| Host C      | Host D           |   Yes, at that L3 device/firewall   |                    Yes                    |

Given the diagram above of two network segments with a firewall in between, we will cover what you
can enforce policy with and what you can't. In this drawing this is a firewall that separates the
network segments. However, you could also have this be a L3 device, such as a L3 switch, or a router
where there are ACLs in place.

With traditional segmentation, you can apply policy only between the two segments. Host D will have
policy applied to try to talk with Host A, B, or C. Host A, B, and C will be able to communicate
between each other without any policy being applied.

### Micro Segmentation

In that same diagram with Micro Segmentation practices applied, not only can you have policy applied
between Host D and the trio of hosts (A, B, C), but you can also apply policy between hosts A, B, C
on the same network segment. So if you wanted to lock down so that Host A can only talk out of the
segment, but not to any other hosts within the same segment, this **is** possible. This is the major
difference between standard **Segmentation** and **Micro Segmentation**, the ability to prevent
east-west traffic between hosts in the same network segments.

## How to?

So how is this done you may ask? There may be more ways about this, but the ones that I'm aware of
are:

- Controller Based Wireless (Preventing host to host communication)
- [Cisco ISE](https://www.cisco.com/c/en/us/products/security/identity-services-engine/index.html)
- [Cisco ACI](https://www.cisco.com/c/en/us/solutions/data-center-virtualization/application-centric-infrastructure/index.html)
- [Private VLANs](https://en.wikipedia.org/wiki/Private_VLAN) (**Administratively burdensome**)
- [NSX](https://www.vmware.com/try-vmware/nsx-micro-hol-labs.html)
- Host based firewalls (**More burden**) (Maybe Illumio can help here? - [Packet Pushers BIB Illumio](https://packetpushers.net/podcast/bib-062-globally-scalable-microsegmentation-with-illumio/))

### Does this work?

Absolutely. I have done host to host policy enforcement within a VLAN using Cisco ISE in a campus
LAN environment. There was a requirement to prevent one host to talk to any other host within the
same network segment. Cisco ISE definitely delivered on this, within the policy matrix by defining
policy that a tag (say 6) could not talk to that same tag (6). If you have some unmanaged switches
in the wire that don't have the hosts wired up directly to a switchport, this is no longer feasible.

## Summary

So in summary, hopefully this helps clear up some ideas about what Segmentation and Micro
Segmentation are in the industry. This is my take on what the difference between **Segmentation**
and **Micro Segmentation** and that there is a difference. Not just segmenting at a L3 boundry.

#### Discussion

I have not figured out yet how to add disqus to the blog at this point. Hopefully I can get that
added soon.

#### Notes

Drawing completed at [draw.io](https://draw.io).
