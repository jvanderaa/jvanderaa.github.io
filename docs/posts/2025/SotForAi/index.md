---
authors: [jvanderaa]
comments: true
date: 2025-06-03
slug: networking-sot-ai
categories:
- automation
- ai
title: "Network Data for AI"
toc: true
tags:
- ai
---

As the AI movement continues to expand and into the network space and keep going further, now having the appropriate source of truth for the network data is critical as ever. What I have been seeing so far in the industry for networking and AI has been a lot of working on the individual devices one by one. But when looking at leveraging AI for the network, I believe it is best to look at the network as a network as a whole. And that is where the Source of Truth data being stored in Nautobot is going to provide the right information about the network and the **relationships** between pieces of information.

<!-- more -->

## Why a SOT?

The SOT and specifically a [Single Source of Truth](https://networktocode.com/creating-a-single-source-of-truth-for-enterprise-network-automation/) where Nautobot integrates data from many systems together into one system that is able to build the relationships in the data. As an example, connecting a circuit to the device interface allows for AI to know the circuit. 

### Using a SOT for Populating Other Systems

By using the SOT to be the source of information for the network systems then ensures that the appropriate information is connected. Using the SOT to populate an observability platform would then allow the AI to interface with more than just the SOT in a reliable way. By having all of the ancillary tools configuration populated by the SOT allows for the deep connections between systems. Imagine the following workflow:

- Receive a notification from a service provider that circuit A has gone offline
- A workflow is able to execute a check to see if there is a redundant circuit at the location, if so, what interface is that connected to
- The workflow is able to determine if the secondary circuit is active. At which point a secondary workflow can be executed to verify that the site is still available and run secondary checks. Perhaps pausing high bandwidth, low priority data workflows that can sustain some outage time
  - This workflow can then also grab location information to provide location information, such as location of specific onsite equipment such as modems or cabinet information

### Without the SOT Data

In the previous workflow scenario, without having the data inside of a SOT like Nautobot, there are several risks in having a successful workflow:

- The AI would need to analyze configuration data to hypothesize where the secondary circuit or pathway/device is for the location. 
  - Which may lead to hallucinations, when you are conjecturing about data rather than having the specific ask
  - I've seen location information housed in SNMP configuration previously, this data is often stale and forgotten about when moving a device between locations or gets blindly copied as a template, indicating that the device is somewhere it is not.
- When data is not sourced from a single location, data validation and accuracy is easily compromised. Such as location information, if not sourced from somewhere would be typed. It may appear in different formats if not standardized
  - This is where the Data Validation Engine capabilities provides a layer of protection from the risk by enforcing a set of rules

## Why Nautobot

Nautobot is uniquely positioned to really drive forward with both Network Automation and the AI future. The focus has been not only on getting data into the database and the SOT, but also having the capability to validate that the data is valid.

### The Challenge of Data Population

One of the bigger challenges that I have seen over the years is worrying about populating "bad" data into the SoT. This is something that definitely needs to be addressed, but without addressing it at point in the near future this risk of continuing to have bad data (technical debt) about the network is going to continue to expand. My advice here is to just ^^get started^^, getting the data for the use cases that you are looking for. Don't get into a situation where you are prematurely optimizing the environment.

??? note "Premature Optimization"
    As defined by Gemini (2025-06-03)
    > This is a very common phrase in software development. It refers to optimizing a part of the system before it's clear that it's a bottleneck or even necessary. Spending excessive time fetching data you might need later perfectly fits this description. The full quote often cited is "Premature optimization is the root of all evil" (or at least most of it) in programming – Donald Knuth.

### Nautobot Jobs

Nautobot Jobs are going to be a big part in my opinion of providing guardrails to AI within an organization. With using Nautobot Jobs, since they are directly connected with the SOT, you now have a set of predefined jobs that receive input from an AI tool. With the Jobs execution you then get:

- Logging of Job execution, providing the time stamp of who/what system initiated and the job logging of what was executed.
- RBAC control of what can be executed, by which departments.
- If done with Git or via your Nautobot App, you get an approval workflow that has a human involved in which jobs are allowed to be executed.

It is my opinion, at least at the current state in 2025, that there is the need for guardrails in what the AI systems are able to execute on the network. By providing the framework and an API endpoint that can be read by AI, you are able to get the guardrails of what can be done on the network. This should also expand into the data updates to Nautobot, in that the Nautobot Job is used to update data and prevent access to making updates on the Nautobot data directly.

## Summary

In the world of advanced networking that is looking to take advantage of network automation and AI systems, Nautobot as a SOT is what makes the most sense to me. Nautobot is able to natively and quickly provide the data relationships that make AI able to reason better, the Jobs framework to put guardrails in place to understand what can and cannot be done, and finally with the Jobs framework get the appropriate logging in place to understand the what and when. These are all components to me that will enable AI to go further and faster.

At ONUG, Network to Code announced NautobotGPT. NautobotGPT is your GPT that is able to do two things out of the gate with Nautobot:

- Provide proven Nautobot Jobs via the RAG additions curated by Network to Code
- Provide the capability to read data from Nautobot for use within an agent based framework

??? note "AI Editorial Assistance"
    This blog post had editing assistance from Google Gemini Advanced - 204-09-21. The structure of the post was not altered and no significant content was added by the editing.