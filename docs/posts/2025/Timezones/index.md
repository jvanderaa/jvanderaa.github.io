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

It’s been a while since my last post — life and work have both been full. Today, I’m diving into one of the most quietly critical aspects of network design: **time synchronization**. Specifically, how to design NTP within an enterprise network and how to think about time zones when correlating logs.

We'll look at two main topics in this post: designing NTP (Network Time Protocol) and managing time zone display in logs. 

<!-- more -->

## Network Time Protocol (NTP)

Network Time Protocol (NTP) keeps device clocks synchronized — a small detail that can have big operational consequences. Accurate time is essential for correlating logs, troubleshooting issues, and maintaining consistency across systems. In enterprise environments, having a common time source is vital. Whether investigating a cyber incident or reviewing footage from security cameras, synchronized time keeps all data sources in lockstep.

??? note "Precision Time Protocol"
    For most organizations, second-level precision is sufficient. However, environments requiring microsecond accuracy may use [Precision Time Protocol (PTP)](https://en.wikipedia.org/wiki/Precision_Time_Protocol). I haven’t personally needed that level of precision yet, but it’s worth exploring if your use case demands it.

### Time Sources

The first design decision is whether your organization should maintain its own time source. Common dedicated sources include:

- **Satellite clocks** — synchronized via GPS signals  
- **Radio signals** — received from regional broadcast time services  
- **Atomic clocks** — the reference source behind most public and private time systems  

???+ note "Hosted Time Sources"
    If you’re hosting your own time source, **monitor it regularly** with your observability platform to ensure it’s receiving valid signals rather than relying on its internal oscillator. These devices periodically sync with their upstream references while serving NTP requests to downstream systems.

    Want to learn more about building modern telemetry and observability systems? Check out the book I co-authored with [David Flores](https://www.linkedin.com/in/david-flores-80282917/) and [Christian Adell](https://www.linkedin.com/in/christianadell/): [*Modern Network Observability*](https://www.packtpub.com/en-us/product/modern-network-observability-9781835083178). It’s also available on [Amazon](https://www.amazon.com/Modern-Network-Observability-hands-open-source/dp/1835081061/).

#### Internet Clocks

If you don’t want to maintain hardware, you can synchronize with public Internet NTP servers. These servers, often tied directly to atomic clocks, provide highly reliable time.  
A good starting point is the [NTP Pool Project](https://www.ntppool.org/en/), which distributes requests across a global pool of community-run time servers.

### Design Considerations

Once your primary time source is established, ensure all systems retrieve time from reliable, redundant servers. In most environments, I recommend **a primary and secondary NTP source** — both enterprise-wide and within each site (data center, campus, or branch). Typically, a **Layer 3 device** such as a router or core switch provides local NTP services.

???+ note "Windows Time Service (W32Time)"
    Microsoft Windows systems don’t use NTP directly. They rely on the **Windows Time Service (W32Time)**, which synchronizes through Active Directory. Ensure your AD servers synchronize from the same authoritative NTP source as the rest of the environment.

#### Data Center Time

In larger data centers, consider deploying dedicated NTP servers that synchronize with your enterprise’s primary and secondary sources. These servers then provide time to all other equipment — not just network gear, but also hosts, VMs, and monitoring systems.  
Virtual machines should derive time from their hypervisors, which in turn should sync with the NTP servers.

#### Campus Designs

In campus networks, edge or core routers can act as NTP sources for local systems. These include Linux-based hosts, networking gear, security cameras, and other business systems. This approach ensures consistency across devices without requiring every host to reach the Internet or the enterprise core.

#### Branch Design

At branch sites, especially those with limited infrastructure, a single router can serve as the **primary local time source**, synchronizing upstream to a central NTP server. Configure a **secondary remote source** in case the local router or WAN connection fails. This design maintains local accuracy even when external links are unavailable.

## UTC Versus Local Time Zone

When it comes to log timestamps, this decision is often cultural as much as technical. Ideally, all systems should record logs in **UTC**. However, for organizations operating entirely within one region, using **local time** can improve usability — as long as everyone understands the offset.  
For distributed teams across multiple time zones, UTC is almost always the better choice for correlation and analysis.

## EST vs. EDT — They’re the Same, Right?

Not quite. **EST (Eastern Standard Time)** is UTC−05:00, while **EDT (Eastern Daylight Time)** is UTC−04:00. The offset changes with daylight saving time. If you want a neutral reference, use **Eastern Time (ET)** or **Eastern Prevailing Time (EPT)** to represent whichever offset is currently in effect.

## Summary

Time synchronization may not be glamorous, but it’s foundational. A few seconds of drift can complicate troubleshooting, incident response, or forensic analysis.  
Design your NTP hierarchy deliberately, monitor it continuously (ideally through your observability platform), and define clearly how your organization handles time zones.

What are your thoughts on these design approaches? Anything you’d add or handle differently?

— Josh

???+ ai "Assisted by AI"
    Some editorial support for this article was provided by AI to improve clarity and concision.
