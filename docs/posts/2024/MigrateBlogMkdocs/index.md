---
authors: [jvanderaa]
comments: true
date: 2024-05-28
slug: to-mkdocs
categories:
- blog
title: "Migration to MkDocs Material Blog Theme!"
toc: true
---

So, if you are a returning user you notice something that is a little bit different. I have migrated my blog site to a new site generator and format. I am now using [mkdocs-material] blog them that was introduced in late 2022 to the platform. The migration was not too painful to make, but I'm feeling in a good place about it at this point. The blog has been on a journey so far. It started off with a Jekyll themed site which I liked. Then I decided to move onto something that has a little more development. So I moved into the land of Hugo.

<!-- more -->

## Why the Change

The idea of changing first crept into my mind because I was having a mild panic attack after attempting to publish my latest post and GitHub Actions was failing the build process. It turned out that the processing time to build the Hugo blog was just taking longer than the timeout that was default at 30 seconds. In fairness to me, this didn't even cross my mind that it would be an issue since on my home system that same build process would take under a second. So in the troubleshooting I thought, what if I moved my blog to mkdocs?

Recently I have been writing a fair bit of documentation updates to the [Nautobot](https://docs.nautobot.com) documentation and have found the additional features and capabilities to the format quite enticing. That, along with a general easier method to implement admonitions over having to use Hugo shortcodes for everything. With those in mind, I decided to move forward with it.

??? note "Sorry RSS Feed"
    In making the migration, I didn't properly exclude sections of the blog that shouldn't go into the RSS feed. That has been cleared up going forward. Hopefully that will settle down as we go. I still need to investigate if the RSS system has a method to migrate a site to a new feed URL without it just being a fresh take. Research later.

## Interesting Challenges?

There were a few challenges along the way. Making a change in technology almost certainly has some challenges.

### GitHub Actions Failures

I worked a little bit with ChatGPT along the way to help. So of course there were a few things that I had to work through. The first challenge working through was that I set up two CI files, one for testing to make sure the build would work. The second was to do the actual deployment. These mostly should be the same. The deployment CI action was failing. I ended up working my way and with the help from another mkdocs blog - [Copdips.com](https://copdips.com/) I was able to get the deployment CI system working. Using their deployment tests, it deploys flawless. 

### RSS Feed

The RSS feed tool has a different URL for the feed. While not a huge subscriber base (especially when I look at the numbers on Feedly), I want to be able to allow those that have set it up to not have a disruption. I have a copy of the feed file made from the existing file. This is a hack that I had used on the Hugo blog as well. 

### Easiest Getting Started

I attempted a couple of times to follow a site that had the start of the blogging set up, but I kept getting some roadblocks. Whether it was that my post URLs were not formatting the way that I wanted them or something was showing up where they shouldn't. I eventually followed the [setting up a blog](https://squidfunk.github.io/mkdocs-material/setup/setting-up-a-blog/) setup page. Once I did that from scratch there, I was off to the races. If you want to start your own blog, and I encourage you to do so, then I would recommend starting with that page. It gets things moving quite quickly.

## Outstanding ToDos

### Figure out the commenting System

I need to figure out the commenting system and how to migrate over to a new site. This may require a re-do of the config option yet. I've done minimal research thus far. So this may be next.

### Check through some of the old posts

Working through updating my old posts is on the list. I think I got most of the pieces that I need. So this may be done. Just not sure yet. Working on a few things for work that are taking priority on that.

### Look into building a command 

The last reason why I moved was that mkdocs is Python :fontawesome-brands-python:. At this point in my career with automation tools and such, I'm on the Python fan page. More to come on this. So I'm looking forward to seeing what I can do to extend the capabilities as I need them here.

Also a contributing factor is that @squidfunk has what looks like a pretty successful business in supporting mkdocs-material. 

Let me know your thoughts.

-Josh