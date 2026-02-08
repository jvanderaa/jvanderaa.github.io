---
date: 2026-02-07
slug: welcome-ai-01
categories:
- automation
- ai
title: "AI: My Welcome"
summary: >
  Here we are diving into just one of the time savings samples of what the AI world is able to accomplish these days. This post is going to dig into a simple one that I have been trying to solve for a while and just couldn't get right - Cloud Init virtual machines. I now am spinning up virtual machines in a few seconds, all with the help of Claude.
toc: true
tags:
  - ai
  - codex
  - claude
  - openclaw
author: jvanderaa
coverAlt: Alternative Cover Art Words
coverCaption: |
    Photo by <a href="https://unsplash.com/@jakubzerdzicki?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Jakub Żerdzicki</a> on <a href="https://unsplash.com/photos/a-laptop-computer-sitting-on-top-of-a-desk-ynllMMWBdi0?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>

params:
  showComments: true
---

First and foremost is what is my promise to anyone that may read my blog posts, that I will write all of the bulk of the content of the blog posts. I may have some help from AI in some code snippet section type thing. I will definitely use AI to help edit and review the blog post, but the content that is coming to this blog is my own content.

My problem here was that I have some compute in my home that I would like to leverage to the best of my ability to do so. But far too often things have remained idle. Couple that thought with the fact that I am diving in on [OpenClaw](https://openclaw.ai/) coupled with [Claude](https://claude.ai) and I am exploring lots of possible use cases. For this today, I wanted to spin up some VMs that I would then be able to sync into **OpenClaw** that I have running. This time I decided to take a small bit of time to send the challenge at hand to Claude and see what it would come up with.

## Solution

First, I'm following the best practices that are being put out there by the folks at Anthropic of using a Planing session to build out what the plans are and then go build after. I started with the simple prompt that was able to get me a good amount of the way to what we would be looking for.

### First Prompt

Just straight forward:

> [!EXAMPLE] **Prompt**
> I want to use this to build local VMs here. I have some SSH keys that I wish to incorporate and cloud-init through an Ubuntu image.

From this one prompt Claude got to work. It came back and asked me a few clarifying questions, basically asking if it should use Makefile or another system. I said, yeah, let's go forward with Make, which gives me a whole bunch of options on what to build. It went through and was able to get us to about 90% complete. However there was still one thing missing, the documentation.

### Documentation Prompt

So here comes the follow up prompt:

> [!EXAMPLE] Prompt for README
> Create a README as well. I think it is self explanatory but with it being a git repo, this makes sense

At which point the readme was created.

### Missing Items

So now I had the bulk of the idea but there were still just a few outstanding items. Such things over the next few prompts:

- Where should I import an SSH key for authentication
- Please update the readme whenever making updates that impact the process

At that point I went forward with the process that was created. There were a few quirks that had to be ironed out for my specific host. Such as the bridge interface that we were going to bridge the VMs to. And finally the last materially piece to the process that is now able to manage my entire fleet of VMs on the host:

> [!EXAMPLE] Console Connection
> Can we build a `make console NAME=??` to connect to the console?

## Summary

Previously I had spent hours attempting to get the whole cloud-init capability set up on my virtual environment. **Without success**. So by leveraging the tools that I have available to me, Claude (and likely other agents) I said, let's tackle this. I went to the Claude Code in a remote VS Code window and tackled the problem. Probably in about 15-30 minutes. Which also includes the downloading of the images. This is quite the world we are living in. This is showing the power and savings to the individuals that are out there creating and looking to get things done.
