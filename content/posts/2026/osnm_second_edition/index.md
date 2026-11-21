---
date: 2026-07-11
slug: osnm2
categories:
- automation
- book
title: "Open Source Network Management Second Edition"
summary: >
  The second edition of my book Open Source Network Management is out. Digital, paperback, and digital + print bundles are all available now at https://osnm.josh-v.com, and print copies have been shipping since August 28.
toc: true
tags:
  - open-source
  - network
  - book
author: jvanderaa
coverAlt: >
  The Open Source Network Management stack drawn as a left-to-right data
  pipeline — your network into Telegraf (collect), Nautobot as the source of
  truth, Prometheus (store) and Grafana (visualize), with Vault and NGINX as
  the platform layer.
params:
  showComments: true
---

> [!NOTE]
> **Update (November 2026):** The paperback is here. Print copies started shipping on August 28, and digital, print, and bundle orders all ship now from [osnm.josh-v.com](https://osnm.josh-v.com/).

{{< osnm-cta >}}

Today (July 11, 2026) I'm announcing the availability of the second edition of my book - Open Source Network Management. This is an updated version on the writing that I put together several years ago about how to manage networks using Open Source tooling. I wanted to take the time to get an update out and make a few general updates as well to the guide. On top of the initial writing, I'm also working on alternative chapters or a take on a "Choose Your Own Adventure" books that I used to love as a kid. I'm working on putting together additional chapters with tooling that I think Enterprises may want to adopt in order to continue managing networks in a new, modern way.

<!-- more -->

## Updates Made

First, it is updated to 2026 versions of all of the software. That was the first thing that was definitely a requirement. The tooling has come a long ways and continued to be adopted. Nautobot has been updated from version 1.x to 3.x now. Which has many awesome improvements along the way over the years. And it is even better now.

The one glaring hole from the first edition was configuration management. At that time I didn't think Golden Config from Nautobot was the right tool to make changes to network devices. That has now changed and I have added Nautobot Golden Config to the book.

### Metrics & Logs

I've gone ahead and brought in [Victoria Metrics](https://victoriametrics.com/) and [Victoria Logs](https://docs.victoriametrics.com/victorialogs/) to the chapters on Metrics and Logs. These are drop in replacements and there are additional options that will be brought in with the additional chapters that will be made available.

### Remaining Consistent

A lot of the rest is remaining consistent, but there are new capabilities within the tools. Including improved Alerting and Dashboarding with Grafana and updates to the rest of the stack involved.

## Summary

You can get your copy now at [osnm.josh-v.com](https://osnm.josh-v.com/). Digital, paperback, and the digital + print bundle are all available, and you can read the full first chapter before you buy. Let me know your thoughts on the book below.

{{< osnm-cta >}}

-Josh
