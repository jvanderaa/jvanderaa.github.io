---
authors: [jvanderaa]
toc: true
date: 2018-11-22
layout: single
title: Getting Started with the Blog
comments: true
# collections:
#   - Blog
# categories:
#   - Blog
tags: ["blog"]
---

Why this post? Because I decided to change the style of how I was hosting my blog. Before I had decided to just host the blog on something that was easy to get to and update. I could have kept on blogging there, but I found making blog posts a little bit more difficult than what I wanted to. I also wanted to learn some of the `new` ways of doing things within networking technologies.

With this, I decided to bring my blog over to a static site generator. I'm not doing anything significantly crazy with a blog site, other than hopefully creating some useful content. So static site generation brought me over to Github.

<!-- more -->

## What I wanted to accomplish

What I wanted to accomplish with my blog:
- Create some useful content that others may find helpful
- Leverage [Markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) for quick document creation (Previous site was time consuming in my mind to create content, but it did get a start)
- If possible, figure out how to appropriately handle CI/CD
- Maybe, maybe, look to moving to a Python static site generator, since I am doing most of my own work in Python. Perhaps GoLang if there is such a thing in that sphere. We will see.

> The first four posts on this page are pieces that I was able to quickly move over from the
> previous blogging platform over to the markdown flavor. This explains the timing of this post with
> having older posts on the blog.

## Evaluation

I originally started with Gitlab, knowing that they had a good exposure of the CI/CD process and had it all integrated. I didn't want to try to integrate a different solution into the Github arena if possible. I tried originally forking the `jekyll` format over, but this didn't get going well. The CSS never quite made it into the page, so I was frustrated and decided to try Github.

Over at Github, I could start to get the content, and as soon as I would push a new commit to master I would get an email a few minutes later saying that the build had failed. No other helpful information in the email, just that the Jekyll build had failed. After about four of these messages I decided to try just doing Jekyll on a new VM host of my own and see if I could get it working there.

### Decision Making

I started with a fresh Jekyll page, and immediately things came right up. Finally some progress! Eventually, I found my way to the [Jekyll Quickstart/Docs](https://jekyllrb.com/docs/), following that tutorial and looking at other blogging pages on various Github/Gitlab pages I figured out the structure a little bit more.

I then cloned the repository from Gitlab pages to my local instance and gave it a run. The default page showed immediately. From there I went ahead and copied my posts into the `_posts` directory and the content was right there. I decided to push the content to my Gitlab pages and low and behold it worked there as well! I was in business.

### SSL and Custom Domain

There are lots of articles all over the web on how to do a [custom domain](https://docs.gitlab.com/ee/user/project/pages/getting_started_part_three.html) on Gitlab pages. So I'm not going to provide details, but high level:

- Make sure your repository name is `<userid>.gitlab.io`
- Point your DNS records at Gitlab and away you go

SSL was a little more tricky. I had found an "official" link from Gitlab, but that was not helpful to me. I couldn't get the certificate information to show up with [Let's Encrypt](https://letsencrypt.org/). I eventually came across this [blog](https://autonomic.guru/using-letsencrypt-on-gitlabs/) on how to do certificates with Let's Encrypt via Gitlab pages. Once I completed the work done described there, I was able to get my certificates from Let's Encrypt, and I now have a SSL blog.

#### Final Decision: Gitlab Pages

At that point, I finally had a page out on the web and am at the point that I am now. I'm going to continue to evolve what the pages will look like. I've still got some more to learn about how to get Jekyll in the right setup. Maybe a trip to using Python Pelican to build a flavor. But for now, I have a place where I can post material, and so far with writing this post, things are much quicker.
