---
author: Josh VanDeraa
comments: true
date: "2022-09-25T07:00:00Z"
slug: python-pseudo-code
tags:
- automation
- python
- nornir
title: Python Pseudo Code
toc: true
---
One of my favorite things to do as I get started with writing a piece of automation or code, is to lay out the design with pseudo code in the form of comments. I will do this with both Python and Ansible automations, and is a great way to get started on writing your automation or code. What pseudo code does for you is to layout the process at which you wish to accomplish a particular goal. And from there, you write the code that corresponds to the plain English wording of what is being done. By starting with pseudo code, you are starting with the process first. Then working on getting to the details of the code as you go.

In this post, I will take you through the writing of a Nautobot Job that is going to be used with the Nautobot Circuit Maintenance plugin, that will review the upcoming maintenance notifications that have been ingested into Nautobot and determining if there are any overlapping maintenances.

## The Pseudo Code

My initial pseudo code for the Job looks like this:

```
        # Query for all of the circuits maintenances that are on going in the future
        # Query for all of the circuits within Nautobot
        # Loop over each of the circuit maintenance records
            # Check to see if there are any circuit maintenances that are duplicated time
            # Query to see how many circuits are available at the site
            # Determine how many other maintenances there may be at the same time
            # Report failures for any time where a circuit will take an outage
            # Evaluate adding a tag of an impeding site outage due to WAN outages (This is a design note, will probably be implemented)
            # Log success for each time there is a known circuit still available at the site at the same time
```

Here I'm outlining with the general indentation of the planned code. Note that there is nothing about the actual code here. As I progress, I will be able to handle each of these independently. I will also try to keep the logic as minimal as I can. If I have to break out to a function because the logic is getting deep, this allows for the code to get tested quite well. This is the logic that I will put into an issue on GitHub to allow for the maintainers of the library to provide feedback on.

> The testing subject will be a follow up post up after finishing up this post. I wish to keep things as short as possible on the topic.

The indented space starting on line 4 of the example are what will be executed under the for loop. So there is still some programming layout that is being done here, but does not have code.

Now that there is a framework that is going to be worked from, the next steps are to start building the code.

## Building Out the Code

Now that the pseudo code is developed, it is putting code to the program (I so wanted to say something like pen to paper). 