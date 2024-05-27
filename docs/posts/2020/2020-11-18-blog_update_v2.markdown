---
authors: [jvanderaa]
date: 2020-11-18
layout: single
comments: true
slug: blog_update_v2
title: 2020 Blog Update
tags:
- blog
- hashnode
- jekyll
- hugo
toc: true
---


I've changed a few things on the site. Sorry about that! URLs have changed. Over the past week or so I have been working through making some what originally were small updates to the blog, that turned into a little too much effort. I was hoping to add a little bit of polish to the site while keeping the content in place. Earlier in 2020, maybe even back in 2019 I had become aware of Hashnode from the posts of [David Flores - aka NetPanda](https://twitter.com/davidban77) who is on the Hashnode side at [https://davidban77.hashnode.dev/](https://davidban77.hashnode.dev/). I liked many things that the blogging site has to offer. From a very quick up and running, to having a strong start of a
community.

## Hashnode Trial

I decided to move the blog to Hashnode as a let's get started. I found it is easy to move the site as they already supported Markdown, which is what I write my blogs in already. The only downside that I originally saw as that there were no line numberings on the code blocks. I can live without that, but I still did desire it. I added my domain name and made the necessary DNS updates and it started to work out.

### Downsides of Moving to Hashnode

In the process I found that my first downside was that I lost some of my search engine rankings. One of the more popular over time posts was now gone from the search list. This is better as now my posts with Network to Code and some more recent post updates are showing up at the top of the list. Just wanted to make sure that was known.  

An unexpected downside of the move was that Hashnode appeared to enable HSTS on the domain josh-v.com. The implications of this is that on my development hosts that get the domain extension josh-v.com are then also expecting to be HTTPS. And the browsers automatically forwarded to the HTTPS domain. So I just went ahead and moved them to a new domain. Nothing that I couldn't overcome, but it took a short bit to figure that out.

## Move Away from Hashnode

In the end I found that when my domain was moved over there was not a way to customize the RSS feed. I chose to move back for that reason. I also want to be able to have a little more control on my domain about which URLs are HTTPS and which ones are not. And there are some other implications for the future as well. I moved back to the GitLab Pages that was still in place. This migration was an easy undo action.

## Hugo Evaluation

[Hugo](https://gohugo.io/) has a tremendous upside to it as the static site generator platform. It is written in Go, which helps with its speed, and can help you work with GoLang learning. There is an awesome centralized theme gallery for you to view possible themes to apply, and their features/code. It is extremely flexible.  

The one thing that I could not get to work out right was the image sizes on the site. When I tested locally and on GitHub pages (note that my main site is hosted on GitLab pages) the images would not resize to match the article. I found several posts that indicated to make a shortcode and then call the image that way, however that didn't seem to resolve my issues. So after a couple of evenings of attempting to figure this out that is when I turned back to check into the Jekyll themes arena.

## Jekyll Themes

The one downside is there is not a great system for themes like Hugo has, but there were some theme galleries around. I decided first to take a look at [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) to see if there was something that I could do. And there was. There had been many updates to the theme, and it has had an extreme amount of flexibility and capabilities added on. I got the theme up and running and then tested out what my existing blog posts would look like. They looked terrific, and just what I was looking for. I had a few small tweaks to make. I also needed to update the GitLab CI process for the new theme version. This has been a pleasant experience thus far. The couple of downsides that I see are that I need to research how to add a copy button to the code snippets where I would like them. I can handle that. And then the deployment length has some added pieces due ot the Ruby install process. I can live with this for now and have some paths forward to take.  

I love the new layouts in it. I like the table of contents options that will be on most if not all of my posts. I have a few tweaks on some presentations which shouldn't be too hard.  

The only downside thus far to the move to the newer version (and maybe this was my fault from 2+ years ago) was that my posts now have new URLs. So if I was counting on someone bookmarking a post, these have now changed. I hope that these URLs will now remain in the future as they seem consistent on platforms from Hashnode, Hugo, and Jekyll now.  

So for now, I am staying on Jekyll. 

## Python - Pelican

I'd love to look at moving this blog to being a Pelican theme. However, when I researched some of the features I was looking for they just didn't seem to have it yet. I know Python the best and can contribute at times, but now is not the time for me to be contributing to this. I have other priorities that I know I won't be able to tackle this type of adventure at this time. Maybe some point in the future.

## Hashnode - Good Platform

I did a small amount of negative points around Hashnode. There is a **TON** of good things about the platform. I do intend to keep an eye on how the platform moves on. I have opened several feature requests to hopefully get the last pieces that I would need to move over to them. There are several awesome things that are going on within the platform:

* Using modern techniques, writing within Markdown and providing a modern browser interface is good
* Easy, no research needed features
* Image resizing! This is why I didn't move to Hugo
* Nice layouts pre-built

I absolutely would look at Hashnode if I were starting out on my blog. There is a great amount of features available. I had the opportunity to stick with something else.

## TLDR

1. Moved to Hashnode, had some quirks that I didn't like
2. Moved back to GitLab Pages!
3. Tried hugo, but couldn't get images to work right
4. Moved back to Jekyll with an updated theme and here we are!
