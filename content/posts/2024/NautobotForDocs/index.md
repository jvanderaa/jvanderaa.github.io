---
author: Josh VanDeraa
comments: true
date: 2024-03-01
slug: nautobot-for-docs
tags:
- networking
- nautobot
- documentation
title: Nautobot for Docs
toc: true
coverAlt: Cookies in random shapes
coverCaption: |
    Photo by <a href="https://unsplash.com/@caglararaz?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Caglar Araz</a> on <a href="https://unsplash.com/photos/heart-and-star-cookie-CggwlFAw8Kw?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>
  
---

Recently the age old question of network architecture came up on a Discord thread, how can I build diagrams of the network dynamically? This is a question that is pretty frequent within the network automation community. I'm almost certain that it is something that many in the network automation field has been asked at some point in time. I'm here to suggest that there is another way. To get the outcome that is being looked for, just in another format/display.

## The Goals of Diagrams

I've been there. I have been the person that spent many of days working on the network diagram, getting things just right. My Microsoft Visio skills at the time were getting quite decent. The goal for each of the diagrams was:

- To document the physical layout and cabling
- Layer 2 domain
- Layer 3 domain

In these diagrams we had to get standards of what was copper, multimode, and singlemode cabling looked like so that there would be consistency. Would the diagrams have images of the devices or be generic? Where would device names, interface names, and cabling intermediate information be displayed? Should there be layers involved? 

That all took time and effort.

## A Different Approach

In the field of network automation for many years now there have been multiple tools, open-source and paid, that provide for the capability to provide the details you are looking for. The data may be presented a bit differently than a topology diagram, it presents the answers to many of the questions that you would build a diagram for.