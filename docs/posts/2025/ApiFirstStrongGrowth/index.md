---
authors: [jvanderaa]
comments: true
date: 2025-12-13
slug: services-first-strong-growth
categories:
- automation
title: "Services First - A Reminder of Strong Growth"
toc: true
tags:
- api
- services
- strategy
---

Recently we had a post happen on the internal Slack at [Network to Code](https://networktocode.com) that highlighted the Amazon API Mandate from 2002 that was seen as trasnformative for Amazon. In the post (which can be found [here](https://nordicapis.com/the-bezos-api-mandate-amazons-manifesto-for-externalization/)) it is highlighted that **All teams will henceforth expose their data and functionality through service interfaces.** As I took my first read of this mandate, I am immediately a strong believer in the strategy. Let's take a deeper dive into this. First the mandate had the following requirements:

1. All teams will henceforth expose their data and functionality through service interfaces.

2. Teams must communicate with each other through these interfaces.

3. There will be no other form of interprocess communication allowed: no direct linking, no direct reads of another team’s data store, no shared-memory model, no back-doors whatsoever. The only communication allowed is via service interface calls over the network.

4. It doesn’t matter what technology they use. HTTP, Corba, Pubsub, custom protocols — doesn’t matter.

5. All service interfaces, without exception, must be designed from the ground up to be externalizable. That is to say, the team must plan and design to be able to expose the interface to developers in the outside world. No exceptions.

6. Anyone who doesn’t do this will be fired.

7. Thank you; have a nice day!

<!-- more -->

## Introduction

When I first started to take a look at writing this post I was centered around the idea of supporting the Services First strategy to be all through API services. And this is the most likely component as far as getting started. But as I was reading the mandata again I read the part about **Pubsub** being one of the options. This is something that I do happen to completely agree with. There are many solid **Pubsub** systems available such as Kafka, NATS, and MQTT.

At Network to Code Professional Services we are typicallyed centered around automation workflows to enable our customers to get the most out of their networks. And the best part about using [Nautobot](https://nautobot.com) is that everything about the system is API driven. [Nautobot Jobs](https://docs.nautobot.com/projects/core/en/stable/development/jobs/) are a great example of how you can take a CLI based workflow and put it into a system that can be scaled and consumed by other teams. I wrote about this both in a previous post about [Nautobot Jobs Execution](https://josh-v.com/nautobot-jobs-execution/) and in the [Nautobot Book](https://josh-v.com/nautobot-book/).

With Nautobot Jobs it is incredibly easy to get started with creating your own API service. With minor adaptation from your Python CLI based workflow you can create a Nautobot Job that can be launched via API assuming that the system requesting the job has the proper permissions.

### Why Nautobot Jobs?

The first reason is around the mandate that is described above and is a tried and true method for enabling services to be consumed by other teams.

On top of that, Nautobot provides all of the mechanisms that are needed to secure and provide authentication for the API services. Instead of writing an API service from scratch where you need to then handle authentication, permissions, logging, and other mechanisms, **you can get started right away with your business logic**. 

## Pubsub and Nautobot

Pubsub and Nautobot are a natural combination. By being able to integrate with Enterprise level [Pubsub](https://en.wikipedia.org/wiki/Publish-subscribe_pattern) systems such as [Apache Kafka](https://kafka.apache.org) or [NATS](https://nats.io) you can enable your Enterprise teams to be able to react to events about Nautobot data in real-time. Out of the box Nautobot provides the capability to publish events to Redis and Syslog.

By using a Pubsub system you can enable your teams to react to events about Nautobot data in real-time. So if someone makes an update to an IP address in Nautobot, you can react to that event and update your systems in near real-time. The scenario that we have seen most often is incorporating devices into monitoring or authentication systems once a device moves from a `Planned` status to an `Active` status. That once the device status makes the change to a production state, then it is added into the RADIUS system for authentication.

## Analysis

What Network Automation teams should have a strong focus on is making services available for the network. This may be a self-service portal for a port change, such as a VLAN change form on Service Now, or to a port update within the data center when new services are ordered.

Interestingly enough I have seen too often then days where interprocess communication is happening with direct access to the database. I very much agree within the mandate that accessing the database directly is not a good idea. While you can certainly have read-only access to the database, there are other caveats that may come as a result of providing that first direct access. The data should be presented via an API when querying and then either having Pubsub or API access for kicking off workflows.

## Summary

When taking the next step in the automation journey beyond the initial automation of read-only workflows with network devices I believe that you should be looking into delivering services via APIs and Pubsub systems. This is a natural progression from the initial automation of read-only workflows with network devices and is a strong foundation for building a modern network automation strategy.

I'm going to dive into a few examples in the future to show how you can take advantage of these strategies.

-Josh