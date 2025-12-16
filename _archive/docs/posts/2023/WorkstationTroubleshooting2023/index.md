---
authors: [jvanderaa]
comments: true
date: 2023-07-29
slug: workstation-troubleshooting-2023
categories: ["automation"]
title: Workstation Troubleshooting 2023
toc: true
coverAlt: Workstation Troubleshooting 2023
coverCaption: |
  Photo by <a href="https://unsplash.com/@vishnumaiea?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Vishnu Mohanan</a> on <a href="https://unsplash.com/s/photos/computer-chip?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

---

In my [previous post](https://josh-v.com/desktop-build-2023/) I wrote about a workstation that I was working on building. It took an incredibly long time to get up and into a stable environment. But I have finally accomplished stability (hoping to not jinx it here with the post). I went through a fair bit of troubleshooting to get to this point.

<!-- more -->

## Symptom

The symptom that was having instability was that the system would freeze randomly. There was not a particular application or otherwise that would be point me to an application that was causing the failures. The system would just freeze overnight or at the start of getting into the desktop UI.

I first tried multiple versions of Linux to see if there was a flavor of Linux that was causing the issue. To no avail. I tried:

- Ubuntu 23
- Fedora 38
- PopOS 22.04
- Debian 12

All of these had some sort of failure that was occurring within the system. Debian 12 wouldn't even complete it's full installation.

Of these, PopOS did seem to work the longest. This was encouraging, but I was really interested in getting to Gnome 44, which has some excellent polish in the UI.

## Hardware Testing

First up in the testing was to do some tests of the hardware. I went with doing a memory stress test using [MemTest86+](https://www.memtest.org/). With all 4 sticks of RAM in the system I received some errors on test #6 pretty quickly. So I was thinking that the next test would be to run tests on each individual stick of RAM. This test showed everything as clear. So I loaded all 4 sticks back into the system, and re-ran test #6 that gave errors pretty quickly. That was clear this time. Back to the OS! But then the freezing continued.

Next up I had happened to pick up a second nVME SSD during Amazon's Prime Days deals. This just happened to arrive after being placed on backorder instantly (that is another interesting quirk). So I go to install the nVME and get started installing. But the freezing kept happening.

Next up was since I was going down the path of Fedora and the possible challenges (unfounded claim) that Nvidia drivers could be causing issues, I ordered a new GPU. Put this into the system and still no change.

> What I was really impressed on the swapping of the GPU was how quickly that Fedora was able to just pick this up and get moving. I just booted up and bam I had my UI going. Nothing to have to work through.

At this point, I am suspecting that maybe the motherboard would be my next stop on the troubleshooting chain. I decided to go to [PC Parts Picker](https://www.pcpartspicker.com) to look at what else would be compatible with the processor and RAM choices. I found the [Gigabyte B765M DS3H AX](https://amzn.to/3OhpdEe) would work, and it comes with some added benefits of having wireless (bluetooth) and a 2.5 Gbps NIC. I ordered up this motherboard and got to it the same night with completing the motherboard swap. Interestingly enough, it also includes a second M.2 interface that I was able to install both nVME drives that I have.

Instantly things just felt better in the OS. Fedora was able to be installed smoothly and without any hesitation. The system BIOS already had XMP disabled, which was a recommendation that I had seen in some other posts. And the hardware was all detected.

Fedora ran through the night at this point. Once waking up to get started with the day it felt good to just have the Dev Workstation up and running.

## Fedora Choice

I'm going with Fedora at the moment for a couple of reasons. First, on top of being a solid, trusted OS, it is running the latest kernels and latest UI. I'm impressed with where Linux is at. Secondly, I just need to get better. In the world of Network Automation, as much as it is easy to just get moving with Ubuntu, I need to be able to work within the world of Fedora. So this will hopefully work out well.

## Dual Boot

One of the interesting things that I didn't think about with the second drive, is that I have an easy method to set up a dual booting system. Every time my workstation reboots at this point I am presented with a choice of a previous PopOS install or the Fedora install. I am continuing to run Fedora, but it is nice to know that I have the option.

## Summary

So far it was an experience that I wasn't looking to have, but I did get to experience desktop hardware troubleshooting. It's interesting space that I hadn't had the opportunity to do for a while. Just the timing of this could have been better. Well, time to return that old motherboard.

Josh