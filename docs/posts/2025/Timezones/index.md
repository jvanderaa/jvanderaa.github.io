---
authors: [jvanderaa]
comments: true
date: 2025-11-01
slug: time_design
categories:
- automation
- network_design
title: "Network Design with NTP"
toc: true
tags:
- network_design
---

I know, it has been a really long time between posts for me. It has been a busy time overall from the personal life and the career front. But that is not why you would be here. In this post I'm going to dig into time design and networking. One of the things that I have done for all 6 years that I have worked at Network to Code is to remind our teams about [Daylight Saving Time](https://en.wikipedia.org/wiki/Daylight_saving_time). This time shift is something that could cause someone to look bad because the clock changed and I didn't get my clocks updated. Adding to this mix though is the fact that Network to Code serves clients all over the entire world. In Europe, many of the countries there observe Daylight Saving Time on a different day than the US. Creating a time period where calendars change for some but not for others. Now in 2025/2026, many of the clocks on our systems are all internet connected. However, there are still many systems in households that are not connected. So the messaging in the Professional Services world is to make sure you are aware, and that times do change. So the first tip is to definitely use your calendar apps to manage your time and be aware of changes, especially when working worldwide. 

Now, getting into the network design elements of time. I'll dive into two things in this post, the NTP (Network Time Protocol) design and time zone displaying of logs. 

<!-- more -->

## NTP

Network Time Protocol (NTP) is a commonly used protocol to keep device time in sync. It can be critical to business operations to not overlook the importance of setting up time. It is critical in correlating and understanding logs. And in an Enterprise environment, it is also critical to have a common time source for the entire enterprise. Whether investing a cyber break in or doing physical world investigations with cameras, it is important to have all of these sources in lock step.

??? note "Precision Time Protocol"
    For many organizations time may not be super critical, in some organizations it may be. I know that there is another option out and available of [Precision Time Protocol](https://en.wikipedia.org/wiki/Precision_Time_Protocol), but I have not yet been required to need to have deep precision of time. Please take a look at that

### Primary Hosted Clocks

The first decision that needs to be made for an organization is whether or not you need to have your own source of time. Several options for a dedicated time source include:

- Satellite Clocks - synchronized from GPS signals
- Radio Signals
- Atomic Clocks - the source for most of the other signal types listed above

???+ note "Hosted Time Sources"
    If you are looking at hosting your own time source within the environment, do not forget to monitor the clock to make sure that the clock signal is in fact being received. So that the clock is not relying on its own internal time keeping, periodically these clocks sync up their time on top of serving to NTP requests from computer equipment.

    Want to dive in more on a Modern Telemetry system? Check out the book that I co-authored with [David Flores](https://www.linkedin.com/in/david-flores-80282917/) and [Christian Adell](https://www.linkedin.com/in/christianadell/) of [Modern Network Observability](https://www.packtpub.com/en-us/product/modern-network-observability-9781835083178?srsltid=AfmBOoogOny6GIwH2w_1K1so8CMavYbw-k95pgNZ2HnvtFrMjczP2LLs). It is also available on [Amazon](https://www.amazon.com/Modern-Network-Observability-hands-open-source/dp/1835081061/)

### Internet Clocks

If not looking to maintain your own hardware there are also opportunities to get time from the Internet using NTP as well. You can point your time server right at these Internet Clocks and get time from. These are a great place to start to keep time synchronized from a trusted source. These are often synchronized directly with the Atomic clocks. Take a look at the NTP Pool site of https://www.ntppool.org/en/ for more information.

## NTP Design

Now that there is a primary source of time within the environment, the next step is to make sure that your systems are getting the appropriate time from these. In my design philosophy I look to have a primary and secondary NTP source within both the entire enterprise but then also the same set up for a site. This site may be a data center, campus location, or branch. It doesn't really matter. Whatever the logical separation of the network, I recommend a primary and secondary source there.

With each of those environments typically looking a little bit different network wise, here is where I would go for each. In most of my designs of time, I'm looking at a Layer 3 device provide the NTP services.

???+ note "Microsoft Windows Time"
    In this consideration as well is the environments that have Microsoft Windows hosts. Windows itself does not use time from NTP directly, it leverages W32Time. The Windows servers are connected then to Active Directory and Active Directory provides time. Make sure that these Windows hosts are syncing their time from the same source.

### Data Center Time

This is where I would look first on the size of the network. If the data center is of size (not likely a colo facility) you may want to have dedicated NTP servers that all they do is sync up time with the primary and secondary time sources for your environment and then serve time to all of the rest of the equipment in the data center. Be thinking more than just the network gear in this instance. Be thinking about all of the servers and virtual machines within the environment here as well. The VMs may want to get time from their host. The host should be getting the time from the NTP Server.

### Campus Designs

In many campus designs there is enough hardware on the edge of the site that can be considered the Core connection. This is where I would look to have the hosts providing as a time source for the equipment at the campus that is not Microsoft Windows. So all of the local server hosts that are Linux based and networking gear that provides the services. This also includes security cameras and other ancillary systems that provide business services via technology.

### Branch Design

For me when I'm designing a branch site, depending on the equipment in the environment, if there is only one router for example, I'm likely designing where my primary time source is that router, this is the edge of the branch site. Then a secondary of something upstream. This way there are still two sources of time. One locally in the site and the other should the NTP service stop working properly.

## UTC versus Local Time Zone

Now when it comes to logs this is perhaps one of the most challenging, non-technical influenced decision. The purest in me says that you should be using UTC time for all of the clock displays. However, having previously been at organizations that were only Central Time Zone based, it was awfully convenient to see the time in the current time zone. This is going to be an organization by organization based decision. For those that have operations in multiple time zones that provide all about equal support to the organization, then UTC time for displaying logs on systems probably makes sense. If the organization is primarily based in one time zone, it then may make sense to display the logs in the time zone that you are in.

## EST vs EDT - They are the same right?

This is one of my biggest challenges. EST (Eastern Standard Time) and EDT (Eastern Daylight Time) are **not the same**. These are very specific times and have an offset from UTC that are different. EST has an offset of UTC−05:00, and EDT has an offset of UTC−04:00. UTC is the only constant here that remains the same. So these are different times. I in the past have suggested just saying ET for "Eastern Time" which indicates to be the time that is current for the east coast US. I also have come across a new term earlier this year used by my electric company of Prevailing Time. So Eastern Prevailing Time (EPT) is the time that is generally observed on the east coast.

## Summary

Overall, I have seen some not so exciting things come from having time be off on equipment. Whether doing an investigation into an outage or just trying to correlate events that happened, if the clock is off on one piece of gear and there is correlation happening from these logs, it can make yours and others lives difficult to work through.

What are your thoughts on the designs mentioned here? Anything else happening that should be discussed more?

-Josh