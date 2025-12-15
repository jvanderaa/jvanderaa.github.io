---
date: 2025-06-03
slug: critical-role-of-sot
categories:
- automation
- ai
title: 'Fueling Network AI: The Critical Role of Source of Truth Data'
toc: true
tags:
- ai
author: jvanderaa
params:
  showComments: true
---

As the AI movement continues to expand its reach into the networking space, the need for an appropriate source of truth for network data becomes more critical than ever. What I have been seeing so far in the industry for networking and AI has been a lot of working on the individual devices one by one. But when looking at leveraging AI for the network, I believe it is best to look at the network as a whole. And that is where the Source of Truth data being stored in Nautobot is going to provide the right information about the network and the **relationships** between pieces of information -  AI thrives on context, and relationships provide that context for more accurate insights and actions.

<!--more-->

## Why a SOT?

The SOT and specifically a [Single Source of Truth](https://networktocode.com/creating-a-single-source-of-truth-for-enterprise-network-automation/) where Nautobot integrates data from many systems together into one system that is able to build the relationships in the data. As an example, connecting a circuit to a device interface allows AI to understand the circuit's context and relationships.

### Using a SOT for Populating Other Systems

Using the SoT as the source of information for network systems ensures that the appropriate information is connected. Using the SOT to populate an observability platform would then allow the AI to interface with more than just the SOT in a reliable way. Populating all ancillary tool configurations from the SoT enables deep, reliable connections between systems. Imagine the following workflow:

- Receive a notification from a service provider that circuit A has gone offline.
- A workflow is able to execute a check to see if there is a redundant circuit at the location, if so, what interface is that connected to.
- The workflow is able to determine if the secondary circuit is active. Then a secondary workflow can be executed to verify that the site is still available and run secondary checks. Perhaps pausing high bandwidth, low priority data workflows that can sustain some outage time.
  - This workflow can then also grab location information details, such as location of specific onsite equipment such as modems or cabinet information.

### Without the SOT Data

In the previous workflow scenario, without having the data inside of a SOT like Nautobot, there are several risks in having a successful workflow:

- The AI would need to analyze configuration data to hypothesize where the secondary circuit, pathway, or device is for the location. 
  - This reliance on conjecture rather than structured data significantly increases the risk of AI hallucinations.
  - I've seen location information housed in SNMP configuration previously, this data is often stale and forgotten about when moving a device between locations or gets blindly copied as a template, indicating that the device is somewhere it is not.
- When data is not sourced from a single location, data validation and accuracy is easily compromised. Such as location information, if not sourced from somewhere would be typed. It may appear in different formats if not standardized
  - This is where the Data Validation Engine capabilities provide a layer of protection from the risk by enforcing a set of rules

## Why Nautobot

Nautobot is uniquely positioned to really drive forward with both Network Automation and the AI future. The focus has been not only on getting data into the database and the SOT, but also having the capability to validate that the data is valid.

### The Challenge of Data Population

One of the biggest challenges that I have seen over the years is worrying about populating "bad" data into the SoT. This is something that definitely needs to be addressed, but without addressing it at some point in the near future this risk of continuing to have bad data (technical debt) about the network is going to continue to expand. My advice here is to just ^^get started^^, getting the data for the use cases that you are looking for. Don't get into a situation where you are prematurely optimizing the environment.

> [!NOTE]- Premature Optimization
> As defined by Gemini (2025-06-03)
> > This is a very common phrase in software development. It refers to optimizing a part of the system before it's clear that it's a bottleneck or even necessary. Spending excessive time fetching data you might need later perfectly fits this description. The full quote often cited is "Premature optimization is the root of all evil" (or at least most of it) in programming – Donald Knuth.
>
### Nautobot Jobs

Nautobot Jobs are going to be a big part in my opinion of providing guardrails to AI within an organization. With Nautobot Jobs, since they are directly connected with the SOT, you now have a set of predefined jobs that receive input from an AI tool. With the Jobs execution you then get:

- Logging of Job execution, providing the time stamp of who/what system initiated and the job logging of what was executed.
- RBAC control of what can be executed, by which departments.
- If done with Git or via your Nautobot App, you can implement an approval workflow involving human oversight for job execution.

It is my opinion, at least at the current state in 2025, that there is a need for guardrails in what the AI systems are able to execute on the network. By providing the framework and an API endpoint that can be read by AI, you are able to get the guardrails of what can be done on the network. This principle should also extend to data updates within Nautobot, where Nautobot Jobs are used to update data, thereby preventing direct, uncontrolled modifications to Nautobot data. These guardrails help to provide a Data Governance for AI framework.

## Summary

In the world of advanced networking that is looking to take advantage of network automation and AI systems, Nautobot as an SOT is what makes the most sense to me. Nautobot is able to natively and quickly provide the data relationships that make AI able to reason better, the Jobs framework to establish guardrails, defining what can and cannot be done, and finally, the Jobs framework provides the appropriate logging to understand the what and when. These are all components that, in my view, will enable AI to advance further and faster

At ONUG, Network to Code announced NautobotGPT. NautobotGPT is a GPT that offers two key capabilities out of the gate with Nautobot:

- Provide access to proven Nautobot Jobs via Retrieval Augmented Generation (RAG), with content curated by Network to Code.
- Enable reading data from Nautobot for use within an agent-based framework.

> [!NOTE]- AI Editorial Assistance
> This blog post had editing assistance from Google Gemini.