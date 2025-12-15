---
authors: [jvanderaa]
toc: true
date: 2018-12-08
layout: single
comments: true
slug: discontiguous_masks
title: Discontiguous Masks
# collections:
#   - Cisco
# categories:
#   - Cisco
tags: ["network design", "segmentation"]
---

Discontiguous masks are something that is going to be somewhat historic within the network design toolbox. It is basically a methodology of looking at particular bits of a network/host definition. The big thing to recall is that as a packet crosses a network device it does so within a packet. The packet is nothing more than a stream of bits. Within the packet header there are bits that define the source network address and the destination network address. This is where discontiguous masks come into play. With a system that can leverage discontiguous masks, you can access information about any part of the network bits, not just starting reading and then stopping (or vice versa) when you look at a bit boundry masking only.

<!-- more -->

This is a originally posted from my previous blog here  [Previous Post](https://connectforall.blogspot.com/2011/06/discontiguous-masks.html). I plan to give this a complete re-write when I have the opportunity.

## Original post

Simply put, discontiguous masks are those that are represented by a potentially alternating sets of 1s and 0s within a mask (subnet/standard mask or wild card). This does not really apply to a subnet mask as you have a network portion of the address, and then the host portion, so everything is contiguous. The primary place that you will see this is in Access Control Lists or ACLs (for more info on ACLs, here is a quick link to a Wikipedia article. This may be a topic later on within this blog http://en.wikipedia.org/wiki/Standard_Access_Control_List).  

The first two use cases that these come in handy for are for Quality of Service ACLs and Security/Firewall ACLs. There are many more uses out there, but these are the two primary ones that I have come across. Feel free to leave comments, and I will dive into it, modifying this post for this.

My first tip for understanding this concept is that you need to think the way that a router (or other network device) thinks. Everything that passes through a router or switch is passing through the device in a logical method. The router and switch are looking at binary 1s and 0s as they cross the wire.  

Everything for this discussion revolves around binary addressing. Remember that currently in the IPv4 space that there are 32 bits to a network address. That is the IP address 192.168.0.1 can be translated into binary bits of `1100 0000 . 1010 1000 . 0000 0000 . 0000 0001`.

Discontiguous masks are as they state, a mask that can be discontiguous. Many devices in the industry have support for what is a contiguous mask. This does not have do with wild card or subnet masking yet. It just matters how the devices check to see if something matches. In a standard mask or subnet mask, the mask that you define may look something like 255.255.255.0 (11111111.11111111.11111111.00000000). In this case you will be doing a logical "AND" operation where the bits that you care about are represented by a "1".  The bits that are represented by a "0" are those that you do not care about. In the Cisco world of wild card masking, it is the inverse. Most of my examples will be in wild card notation, since this is where it is most prevalent in my world.

A discontiguous mask does not follow this. First, let's take the previous example of the mask 255.255.255.0 and turn it into a wild card mask, so that we can follow along in the same fashion moving forward. This then turns into a 0.0.0.255 mask. Simply changing the important bits, or the bits that you care about from a "1" to a "0" and vice versa. Binary representation is `00000000.00000000.00000000.11111111`. So now, the discontiguous part. Let's say you run a network where you have 10 sites. They are all the same IP address wise, except that you change the third octet to represent your site. Let's use addressing 192.168.0.0 - 192.168.255.255 to represent this. Site A has the IP addresses 192.168.1.0/24 (contiguous masking) and site B has the IP addresses  192.168.2.0/24. You assign a server the address of X.X.X.2 at each site. Now you want to write an ACL that will match that at each site.

The process that I would follow, is we need to figure out what is important. As we look at the 10 site  addresses (we will just use two, but we will see the commonality) that we care about.

|  IP address  |                     Binary                      |
| :----------: | :---------------------------------------------: |
| 192.168.1.2  | `1100 0000 . 1010 1000 . 0000 0001 . 0000 0010` |
| 192.168.2.2  | `1100 0000 . 1010 1000 . 0000 0010 . 0000 0010` |
| 192.168.3.2  | `1100 0000 . 1010 1000 . 0000 0011 . 0000 0010` |
| 192.168.4.2  | `1100 0000 . 1010 1000 . 0000 0100 . 0000 0010` |
| 192.168.5.2  | `1100 0000 . 1010 1000 . 0000 0101 . 0000 0010` |
| 192.168.6.2  | `1100 0000 . 1010 1000 . 0000 0110 . 0000 0010` |
| 192.168.7.2  | `1100 0000 . 1010 1000 . 0000 0111 . 0000 0010` |
| 192.168.8.2  | `1100 0000 . 1010 1000 . 0000 1000 . 0000 0010` |
| 192.168.9.2  | `1100 0000 . 1010 1000 . 0000 1001 . 0000 0010` |
| 192.168.10.2 | `1100 0000 . 1010 1000 . 0000 1010 . 0000 0010` |

You notice a little bit of a pattern develop. So if I were to look at a wild card mask here, let's look at each individual octet one at a time. I encourage you to do so when trying to create your own. We know that in this world that all of the addresses will start with 192.168. on all of the sites. This makes the first two octets very easy to write the wild card mask. You care about all of the bits in the first two octets. So they are simply "0". So far we have 0.0.?.? for a mask.  

The third octet is where it becomes more difficult. As we take a look at the binary information above, you will notice that there isn't a complete pattern in that octet (with only 10 sites, there is a little bit of a pattern, but if this were to get expanded out to say 100 or 200 sites with each the same addressing, then it becomes more difficult. We will say for our discussion, that we don't care what the third octet is. It can be 2, it could be 254 or 140. For simplicity sake of discontiguous explanation, this is the case, we don't care about any of the bits. So now we would have the mask 0.0.255.?

The last octet is once again easy in this case. We care about every bit. So it is "0" again. Our complete wild card mask would be 0.0.255.0 in this case. This is where discontiguous masks are very powerful. Now, let's say that we add a second server at each site. The easiest thing to do from a network perspective is set the IP address to .3 at the site. These two servers do the same functionality in a high availability design, so you want all traffic to be treated as equal. You simply change the very last bit in the octet to be a 1 (in that you don't care if it is a 0 or a 1), and you have your new wild card mask of 0.0.255.1 that will match traffic on two IP addresses at a site instead of just one.

In a contiguous state, there would need to be a clear "border" between the 0s and 1s, that you can't go back and forth on. So `0000000000000001111111111111111` is a contiguous mask. The `000000000000000011111111000000000` mask would not play well with hardware that does not support it.

Remember, think about how a router thinks in order to understand clearly what is happening.

Happy masking! 