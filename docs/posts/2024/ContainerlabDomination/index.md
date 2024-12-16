---
authors: [jvanderaa]
comments: true
date: 2024-12-15
slug: containerlab-explodes
categories:
- linux
- containerlab
- lab
title: "Containerlab - Popularity Exploding"
toc: true
---

Coming out of the 2024 AutoCon2 conference held in Denver the week of November 18th, 2024 - there is one thing that is standing out more so than anything else. Containerlab is a **HUGE** blowout success. In observing through several of the workshops at the conference on Monday and Tuesday, many were using Containerlab in some fashion. Now, Containerlab has been around for a while, so this isn't a press release of it. But it is re-affirming what many already know, that this is a great tool to be in the network engineer and network automator toolset.

<!-- more -->

## What is Containerlab

Summed up best by the site:

> Containerlab provides a CLI for orchestrating and managing container-based networking labs. It starts the containers, builds a virtual wiring between them to create lab topologies of users choice and manages labs lifecycle.

So Containerlab itself does not run containers. It provides a command line method for using Docker native constructs, including containers and networks. This orchestration provides for powerful lab capabilities to make things more easily consumable by engineers. This has really evolved the usage of container images for networking labs.

### Benefits of Network Container Images

There are several benefits to using containers within computing. These include:

- Container images are typically smaller and more system resource efficient
  - Use fewer resources
  - Which brings capability to run more complex labs on smaller hardware footprints
- Faster boot times
- Able to be defined in code/YAML
- More portable, providing entire OSes that are able to be run on multiple systems and systems types

Of all of these capabilities that are being developed, the idea of a digital twin for a network of size starts to become a possibility. The idea of Integration testing your network is the ideal state to have the example of the network built in another environment. What I have found is that this has not historically been something that has been easy to accomplish. From devices on GNS3/EVE-NG requiring different interface names when building out configurations to when doing anything of size, it requires a large lab environment.

## Network Device State as a Container

For me the availability of having container immages is still something that is a challenge towards this environment. Containerlab does have the capability to run non-container native if you only have virtual machine images. The [VRNetLab Project](https://github.com/vrnetlab/vrnetlab) is used in conjunction with the Containerlab environment. Take a look at the [Containerlab documentation on using VRNetlab](https://containerlab.dev/manual/vrnetlab/) for more details on the capability to do so.

## Summary

This is real short, if you are just getting started on your lab environment? Use Containerlab as your base. I plan on working to incorporate Containerlab into all of my labs for my ongoing Network Automation development and all of my writing moving forward. Containerlab was heavily used at a majority of the AutoCon2 workshops and also used heavily was GitHub Codespaces to provide the environment to have for the environment. This allows for easier up and running for those that are looking to learn more. There are a lot of great capabilities that are being developed to provide resources. If anything else besides use Containerlab - it would be great ready to learn some new things! That is a very exciting time.

-Josh
