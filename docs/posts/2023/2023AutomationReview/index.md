---
authors: [jvanderaa]
title: "2023 Automation Review: Top 3"
date: 2023-12-15
categories:
  - nautobot
  - automation
  - ansible
draft: false
coverAlt: Alternative Cover Art Words
coverCaption: |
  Photo by <a href="https://unsplash.com/@enginakyurt?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">engin akyurt</a> on <a href="https://unsplash.com/photos/a-beach-with-a-heart-drawn-in-the-sand-3fGYGza-43g?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
---

The year of 2023 I think may have had some of the biggest leaps in the Network Automation capabilities that are being delivered by some of the best in the business. With Nautobot's Golden Config App adding the ability to complete configuration remediation and Ansible release Event Driven Ansible, there are a couple of powerful tools to help you with your Network Automation. And all with a great new conference addition specific to Network Automation.

<!-- more -->

## Nautobot Golden Config - Configuration Remediation

On the surface [configuration remediation](https://docs.nautobot.com/projects/golden-config/en/latest/user/app_feature_remediation/) may not sound like a big deal. But I was astonished when the team that worked on the feature within Nautobot Golden Config demo'd the features and capabilities internally before the webinar releasing it. Initially, ok this is going to be pushing configuration. To me that is generally a solved problem, and wouldn't be a big deal.

What the tool brings to the automation capabilities the ability to add an approval workflow to the configuration remediation effort. This is a big time process improvement in its own. On top of this, you are able to correlate which devices are associated to the configuration plan. And this all comes with the templating capabilities of the data that is in your SOT. Check out the [YouTube Video](https://www.youtube.com/watch?v=F0HtRBSEjqY) for a deeper introduction.

!!! info
    This is coming from a project that I am employed at. I still believe in the statements of this being game changing for configuration management. I would like to think that I am able to still be impartial, but I was truly impressed seeing this.


## Event Driven Ansible

Next up we really started to see a lot more [Event Driven Ansible (EDA)](https://www.redhat.com/en/technologies/management/ansible/event-driven-ansible). Technically announced in 2022, but it really started to gain conversation a lot more in 2023. EDA brings the ease of getting started with Ansible to Events, which are things that happen in the environment. What does this mean? Well, out of the box one of the event driven capabilities with EDA is to be a webhook receiver. This means that you can set up EDA to listen for an incoming webhook, and then launch an Ansible playbook based on conditions received in the webhook. This is all configured via rule books.

Other capabilities natively as part of the system include the capability to listen to Kafka topics. Kafka is one of the leading pub/sub messaging systems that allow for providing messages to various systems. So you can have EDA subscribe to a particular topic on Kafka, and then kick off an Ansible Playbook from the message, again based on the conditions that are in the rule book.

## Network Automation Forum - autocon0

This is not going to be a review, but a kudos and **thank you** to those at [Network Automation Forum](https://networkautomation.forum/) that brought autocon0 to being. This was a very well attended conference in the fall of 2023, and with a good number of attendees, it shows that the topic of Network Automation is still hot. 

## Summary

2023 was an awesome year for Network Automation, and I foresee even more coming in 2024. There will be even more built on top of what currently exists in open source, and I foresee even more new capabilities being brought and talked about all together.

-Josh

