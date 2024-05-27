---
authors: [jvanderaa]
comments: true
date: 2023-07-09
slug: desktop-build-2023
categories: ["automation", "nautobot", "devnet"]
title: Desktop Build 2023
toc: true
coverAlt: Desktop Build 2023
coverCaption: |
  Photo by <a href="https://unsplash.com/@vishnumaiea?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Vishnu Mohanan</a> on <a href="https://unsplash.com/s/photos/computer-chip?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

---

Here I'm going to dive into what I'm planning to build out for my next desktop here in 2023. Prime Day is nearly upon us, and I'm anticipating (but do not know for sure) that prices on some of the gear that I'm looking for will be available at a good price. I'm also looking to build out a bigger system in order to run some intense VMs up coming.

My goals:
- Build a system that will last for 3-4 years at a minimum
- Max out the RAM, that is my most limiting factor in my environments
- Give Linux a try as the desktop OS, still a bit of debate in this, considering options:
  - Debian 12
  - POP OS
  - Linux Mint

<!-- more -->

## The System

What I'm going with are the following:

| Component    | Item                                          | Amazon Link             |
| ------------ | --------------------------------------------- | ----------------------- |
| Processor    | Intel i5-12600K                               | https://amzn.to/3XLsi3H |
| Motherboard  | ~~ASUS Prime B760M-A~~ Gigabyte B765M DS3H AX | https://amzn.to/3OhpdEe |
| Memory       | Qty 2, 2 x 32 GB TEAMGROUP Elite DDR5         | https://amzn.to/3rp0RAR |
| Storage      | Samsung 980 Pro SSD NVMe                      | https://amzn.to/3PS3Fk3 |
| Case         | Cooler Master MasterBox Q300L                 | https://amzn.to/43kHF4j |
| Power Supply | Thermaltake SMART 600W                        | https://amzn.to/3NPuCCt |
| CPU Cooler   | DeepCool AK400                                | https://amzn.to/3rrpM6y |
| GPU          | AISURIX Radeon RX 580                         | https://amzn.to/3Yf4B4a |

!!! note
    These are all affiliate links. I am not a big affiliate person today, but trying it out.


!!! note
    I am making some minor updates based on changes that I had made in troubleshooting. I have swapped out what originally was an ASUS Prime B760M motherboard for a Gigabyte B765M DS3H AX. This provides additional networking capabilities (Wifi/Bluetooth and 2.5 Gbps NIC) and an additional M.2 slot. I have also swapped out the GPU and will stick with the new GPU at this point.
 
### Processor

I was in between the i5 and i7-12700K processor for this. As I look at my systems though, I don't really ever touch the CPU and looking at Passmark on power usage, the i7 (as expected) has a higher TDP, at which point for the amount of idle time that I do expect on the system I stuck with the i5-12600K. It has plenty of speed, and should support what I'm looking to do no issue.

### Motherboard

I was originally looking at the most inexpensive 128 GB DDR5 capable motherboard that I could find. In the end I went with a little bit better one to get a 2.5 Gbps NIC, not that I will need it. But its available for the future.

### Memory

This was what I needed. All of my systems that I have are feeling the pinch when it comes to allocation of RAM. The CPUs are not being touched, but the memory is definitely running pretty hot. So this is where I am maxing out the memory with some DDR5-4800, which is what the CPU recommends. I'm not looking to overclock anything, but this works.

### Storage

Nothing too fancy here. Going with a good amount of memory. I utilize SAN connectivity often and will be the case here as well that I will mount a few folders on my SAN to account for anything that starts to seem excessive.

### Case

This is where I go small and don't need much. I just need the case to be there to house the gear and protect it. The Cooler Master MasterBox is small enough and should be just what I need.

### Power Supply

Similar story as the others, that the system didn't need to be too heavy. So going with something light on the CPU should be just fine for me. I could see a reverse course on this decision at some point.

### CPU Cooler

I have seen good reviews on this and my goal is for quiet. Being a bit more of a budget PC yet, that is what I have decided to go with on an inexpensive front.

### Graphics

Since I'm not doing a ton of gaming, I am likely to either just use the integrated graphics or leverage an existing GPU that I have in the house. With this becoming my primary desktop I will move an NVIDIA card that I already have into the new unit, and take an older card to replace it in my previous desktop that will eventually become another Proxmox node.

## What Will I Do With The System?

So what will I be putting onto this system?

- Cisco CML
  - With the expanded memory I should be able to run at least one IOS-XR device
  - Will run plenty of Arista / Nexus switches to better simulate a DC
- Dev Host
- Possibly some GitHub Actions runners
- Few other VMs that are OK to be rebooted periodically
  - For those that I want to have more generally available I have a few NUCs that are running that do the same thing
- Attempting to integrate Libvirt and Proxmox together

## Happy Prime Day

With Prime Day going on, there are plenty of deals to be had with these items. I in fact had purchased a few of these before thinking that they were already a good price. But then Prime Day deals came in even better. Look for more posts to come in the future!

Josh