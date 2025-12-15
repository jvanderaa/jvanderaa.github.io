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

Recently, a discussion on the internal Slack at [Network to Code](https://networktocode.com) highlighted the "Amazon API Mandate" from 2002—a directive widely seen as transformative for Amazon. In the post (which can be found [here](https://nordicapis.com/the-bezos-api-mandate-amazons-manifesto-for-externalization/)), the core tenet is clear: **All teams will henceforth expose their data and functionality through service interfaces.** Upon rereading this mandate, I was immediately reminded of why I am such a strong believer in this strategy. Let's take a deeper dive. First, the mandate included the following requirements:

1. All teams will henceforth expose their data and functionality through service interfaces.
2. Teams must communicate with each other through these interfaces.
3. There will be no other form of interprocess communication allowed: no direct linking, no direct reads of another team’s data store, no shared-memory model, no back-doors whatsoever. The only communication allowed is via service interface calls over the network.
4. It doesn’t matter what technology they use. HTTP, Corba, Pubsub, custom protocols — doesn’t matter.
5. All service interfaces, without exception, must be designed from the ground up to be externalizable. That is to say, the team must plan and design to be able to expose the interface to developers in the outside world. No exceptions.
6. Anyone who doesn’t do this will be fired.
7. Thank you; have a nice day!

<!-- more -->

## Introduction

When I first started drafting this post, I centered on the idea of supporting a "Services First" strategy strictly through API services. While that is the most common starting point, as I reviewed the mandate, I noticed the explicit inclusion of **Pub/Sub** (Publish-Subscribe) as a valid communication option. This is something I completely agree with; there are many solid Pub/Sub systems available today, such as Kafka, NATS, and MQTT.

At Network to Code Professional Services, we are typically centered around automation workflows that enable our customers to get the most out of their networks. The best part about using [Nautobot](https://nautobot.com) is that the entire system is API-driven. [Nautobot Jobs](https://docs.nautobot.com/projects/core/en/stable/development/jobs/) are a great example of how you can take a CLI-based workflow and migrate it into a system that scales and can be consumed by other teams. I wrote about this in a previous post about [Nautobot Jobs Execution](https://josh-v.com/nautobot-jobs-execution/) and in the [Nautobot Book](https://josh-v.com/nautobot-book/).

With Nautobot Jobs, it is incredibly easy to start creating your own API service. With minor adaptations to your Python CLI-based workflow, you can create a Nautobot Job that can be launched via API (assuming the requesting system has the proper permissions).

### Why Nautobot Jobs?

The primary reason aligns with the mandate described above: it is a tried-and-true method for enabling services to be consumed by other teams.

On top of that, Nautobot provides all the mechanisms needed to secure and authenticate these API services. Instead of writing an API service from scratch—where you must handle authentication, permissions, logging, and infrastructure—**you can get started right away with your business logic**.

## Pub/Sub and Nautobot

Pub/Sub and Nautobot are a natural combination.  By integrating with enterprise-level [Pub/Sub](https://en.wikipedia.org/wiki/Publish-subscribe_pattern) systems such as [Apache Kafka](https://kafka.apache.org) or [NATS](https://nats.io), you enable your enterprise teams to react to events regarding Nautobot data in real-time. Out of the box, Nautobot provides the capability to publish events to Redis and Syslog.

Using a Pub/Sub system allows downstream teams to react immediately. For example, if someone updates an IP address in Nautobot, you can catch that event and update your systems in near real-time. The scenario we see most often is incorporating devices into monitoring or authentication systems once a device moves from a `Planned` status to an `Active` status. Once the device status changes to a production state, an event triggers the addition of that device into the RADIUS system for authentication.

## Analysis

Network Automation teams should focus heavily on making services available for the network. This might take the form of a self-service portal for a port change (such as a VLAN change form on ServiceNow) or a port update within the data center when new services are ordered.

Interestingly, I still see direct database access used for interprocess communication far too often. I agree entirely with the mandate: accessing the database directly is rarely a good idea. While read-only access to a database seems harmless, it introduces tight coupling and bypasses the abstraction layer that an API provides. Data should be presented via an API when querying, and workflows should be triggered via API or Pub/Sub.

## Summary

When taking the next step in your automation journey—beyond the initial automation of read-only workflows with network devices—I believe you should look into delivering services via APIs and Pub/Sub systems. This is a natural progression and provides a strong foundation for building a modern network automation strategy.

I'm going to dive into a few specific examples in future posts to show how you can take advantage of these strategies.

-Josh