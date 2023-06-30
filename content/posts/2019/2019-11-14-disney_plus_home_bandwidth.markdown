---
author: Josh VanDeraa
toc: true
date: 2019-11-14 07:00:00+00:00
layout: single
slug: disney_plus_streaming
title: Disney Plus Streaming Bandwidth
comments: true
# categories:
# - home_net
tags:
- homenet
- disney
- streaming
---

This will be a brief departure from the automation focused attention that I have been giving to this
blog over the past year or so. This week in the United States was the launch of Disney+ streaming
service. I have subscribed to it at this point and have found some interesting data based on SNMP
polling my network.  

This post is about the bandwidth that I am seeing used, not about anything about the service, or if
another service is better. I don't have the time for that at this time. This is just about what was
an unexpected jump in the bandwidth usage with the new application. But I am very much OK with that
as my subscription level is taking care of that.

## Streaming Setup

So what this is going to show is numbers with just a single device. So this isn't a full across the
board deep test. But it is something to get some numbers out there. My household streaming consists
of primarily an Apple TV Full HD (not the 4k one) or an iPad mini streaming.  

My broadband provider is a cable service provider that speed tests have shown consistent speeds at
around 200 Mbps down, 11 Mbps up.

## Streaming Bandwidth Number - Historically

Historically I've always maintained that based on a Netflix stream, or use of PlayStation Vue that
an HD stream would use somewhere between 3-5 Mbps of bandwidth on a broadband network. I'll show
where that still remains true on the bandwidth graph. That has held true so far.

### Disney+ Streaming

So what have I seen at this point from just 2 days of use of Disney+? It uses much more bandwidth
than I originally expected, in fact, it has been over double that of Netflix streams. So much more
so that the 95th percentile on the home network with just a single stream running has consistently
run up to 11 Mbps for my download.

### Quality?

From the picture that I have seen, it does look very crisp and clear. Makes sense that there are
more bits coming across the wire. I would say that at least in my experience there is a correlation
of quality to the amount of bits coming across.  

The Netflix subscription is the basic HD level. I have not done that study of what that actually
means if that is 720p or 1080p that is coming across. I also do not know what compression there is
within the applications.  

## Graph To Show

Here is the bandwidth graphs. I will try to pretty up the graphics a little more in a future post.

![Graph from LibreNMS](/images/2019/12/disney_plus_bandwidth.png)  

The two spikes up to the red line (95th percentile) on the top side of 0 Mbps are the two times that
Disney+ was in use. Definitely some good amount of usage there. If you see the other couple of early
morning spikes, that is Netflix to an iPad in use. There are some other general streams of data that
happen throughout the day as the family jumps in and out of some other streaming services. But
nothing close to the Disney+ numbers.  

## Summary

There has been some negative press around the large launch, although I have not had the experiences.
Thus far things have been good, we see that there is more bandwidth utilized from Disney+ launch. At
this point a kudos to Disney's CDN providers as well that have been able to push out this kind of
data rates. I assume that others are likely having the same bandwidth utilization with the
service.  

I hope this helps!

> I have it on my radar to move to a more modern network graphing setup as well, I'm just not to
> that point in the home environment yet.
