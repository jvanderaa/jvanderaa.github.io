---
date: 2024-09-21
slug: linux-port-binding
categories:
- linux
title: Linux Port Binding
toc: true
author: jvanderaa
params:
  showComments: true
---

This post is will provide a brief overview of how port binding works in Linux. This topic that will be required for the small series of using Continue.Dev in your local environment, but before addressing the setup of a machine for remote access in a future post, I thought it would be important to quickly create a post regarding the concept of port binding.

## Showing Listening Ports

In Linux you can view all ports that are being listened on by using the `netstat`  or `ss` commands. This is useful for identifying active ports and their associated services. My preference in 2024 is to use the `ss` command, which, [according to Linux.com](https://www.linux.com/topic/networking/introduction-ss-command/), is a more modern version of the `netstat`.

> [!NOTE]- ss command
> The ss command-line utility can display stats for the likes of PACKET, TCP, UDP, DCCP, RAW, and Unix domain sockets. The replacement for netstat is easier to use (compare the man pages to get an immediate idea of how much easier ss is). With ss, you get very detailed information about how your Linux machine is communicating with other machines, networks, and services; details about network connections, networking protocol statistics, and Linux socket connections. With this information in hand, you can much more easily troubleshoot various networking issues.

Let's take a look at an example output of the `ss` command using the options of `-ltn`:

```linenums="1"
$ ss -ltn
State    Recv-Q    Send-Q    Local Address:Port    Peer Address:Port    Process
LISTEN   0         128       127.0.0.1:5432       0.0.0.0:*            
LISTEN   0         128       0.0.0.0:80           0.0.0.0:*            
LISTEN   0         128       0.0.0.0:22           0.0.0.0:*            
LISTEN   0         128       192.168.100.10:23    0.0.0.0:*            
LISTEN   0         128       [::1]:5432           [::]:*               
LISTEN   0         128       [::]:80              [::]:*               
LISTEN   0         128       [::]:22              [::]:*               
```

> [!NOTE]- Generated with AI
> Instead of leveraging a local system that would show the ports listening on my network, I asked ChatGPT to generate a list of ports that are being listened to on a Linux host showing the output of `ss -ltn`.

The port number, located to the right of the colon, represents the port being listened to. For example, in `0.0.0.0:80`, the `0.0.0.0` denotes the listening address, while `:80` specifies the port number. In the column `Peer Address:Port` shows what peer addresses are allowed to connect to the port that is being listened on. The `Local Address:Port` is the primary area of concern that this post will be diving into.

### IPv4 Port Listening

Lines 4 and 5 feature the address `0.0.0.0`, indicating that the service is listening on all IPv4 addresses on the Linux host. On line 4 we have the port number for a local web server and on line 5 we have the port number for SSH. Because of the listening on all IPv4 addresses, you can connect to these ports from any IPv4 address. If there are multiple IP addresses configured in your Linux host, you'll see multiple entries with the same port numbers.

### IPv6 Port Listening

Mirroring the IPv4 behavior, lines 8 and 9 display`[::]` signifying that the services are listening on all IPv6 addresses. In this example, these services are HTTP (port 80) and SSH (port 22).

### Localhost Listening

Lines 3 and 7 show two entries for port number 5432, associated with the PostgreSQL database application. TThese entries are configured to listen exclusively on localhost addresses. he listening IPv4 address is `127.0.0.1` (line 3), and the IPv6 address is `[::1]` (line 7). This configuration prevents external network connections from accessing the port. Applications utilizing localhost listening IP addresses are accessible solely from that local address.

### Specific IP Listening

While less common, Linux also allows services to listen on specific IP addresses. Line 6 illustrates this with port number 23 and the IPv4 address `192.168.100.10`. This configuration restricts access to this port, allowing connections only from interfaces with the IPv4 address `192.168.100.10`. 

## Summary

In summary I hope you have learned a bit more about how to view and manage ports on Linux hosts. This is just a quick overview of how you should be interpreting the output from `ss` and other configuration commands that will be upcoming.

> [!NOTE]- AI Editorial Assistance
> This blog post had editing assistance from Google Gemini Advanced - 2024-09-21. The structure of the post was not altered and no significant content was added by the editing.

-Josh