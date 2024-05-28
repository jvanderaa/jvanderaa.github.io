---
authors: [jvanderaa]
date: 2020-11-28
layout: single
comments: true
slug: jekyll-url-redirection
title: "Jekyll - Adding a URL Redirection"
tags:
  - blog
  - jekyll
toc: true
---
Recently I had some discussions with [Nick Russo](https://twitter.com/nickrusso42518) on some URL redirection changes he was making for his content. I'm not going to take any of his thunder of what he is doing, and that is quite awesome. I decided that I wanted to take a look at that as well within my domain/blog using the Jekyll approach. This is going to be my short post regarding the steps I took to add the URL redirection setup to my personal blog page - josh-v.com.  

<!-- more -->

## First Step - Research

Not being a native Ruby/gem person myself (Python + Ansible), the first thing I did was what anyone should do, see if there is prior art. So I did a search on your favorite search tool and there are a few references. Terrific this should be able to be done.  

The first page that came up was [https://github.com/hlaueriksson/jekyll-url-shortener](https://github.com/hlaueriksson/jekyll-url-shortener). It itself was a little bit tougher for me to decipher but enough to get started. What really helped was the blog post that accompanied the page, which was the third result in the search - [https://conductofcode.io/post/introducing-jekyll-url-shortener/](https://conductofcode.io/post/introducing-jekyll-url-shortener/).  

## Second Step - Testing

Next up was to generate some test code on my local Docker container that I could test the Jekyll blog out. This has been a terrific help. I had some issues getting Jekyll installed on my Mac, so I built a container to handle the testing and that has been working great. I sense a future post here.  

### Redirect Page

First thing was to create a redirect page with front matter. I decided the best thing to start with was a redirect to my employer's page. So I put this in:

```yaml
---
permalink: /ntc/
redirect_to: https://www.networktocode.com/
---
```

Once in I attempted to load the page to see if it would redirect. No go. That is where the second URL, the one referenced in the references section comes into play. I found that there were an additional two configuration items needed to help the Jekyll pages handle the redirection.

### Additional Packages

The first thing was to add the package to the gemspec file. I went and found where the Jekyll plugins were referenced and found them inside the `minimal-mistakes-jekyll.gemspec` file. The blog theme I am using is [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/). So I added the following configuration line to the gemspec:

```ruby
spec.add_runtime_dependency "jekyll-redirect-from", "~> 0.1"
```

I then added the line to the plugins section of the `_config.yml` file (there are more plugins than just what's listed here):

```yaml
plugins:
  - jekyll-redirect-from
```

Once these two updates were made I was successfully getting redirects from my http://localhost:4000/ntc/ URL to [https://www.networktocode.com](https://www.networktocode.com).

## Production

Next up was to put into production the changes. So I took the files over from the test instance into the GitLab project that I host this on. The same changes were made to the system and all is set to go.

## Next Up

There are several improvements that I'm looking to improve upon now that I'm all set in this current blog environment. First is to merge the development environment with my regular blog site. This should not be too bad, but as I was writing this post I realized the importance of this. The reasoning behind why I got in this state is because I was testing different blog platforms (Hugo vs Hashnode vs Jekyll vs Pelican).  

I also plan to re-evaluate if Disqus is the proper platform for my commenting. There are some other options out there, and I need to take a look for how low volume the blog is.  

The last feature that I am looking that would have come in handy on this post is the copy of code snippets feature. That looks a bit more involved however. There are posts on how to do it, but I just need to take a little bit of time to test it out.  

## Summary

In the end it was not too difficult to add a redirect URL page to my Jekyll blog. I plan to have a few links made available, and it is really to just help maintain a list of redirects to helpful content elsewhere and shorten URLs that become lengthy in social posting. Let me know your thoughts below, or if there is another method that I am missing. I may also start to look at some shorter domains, although two characters is probably the best I would be able to squeak out.

## Resources

[https://conductofcode.io/post/introducing-jekyll-url-shortener/](https://conductofcode.io/post/introducing-jekyll-url-shortener/)
