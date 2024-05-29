---
authors: [jvanderaa]
comments: true
date: 2024-05-29
slug: bindkey-search
categories:
- linux
- chatgpt
title: "Bindkey For Autocompletion"
toc: true
---

I have been looking at migrating over to the [Starship shell](https://starship.rs) for a little while. The allure of running a rust shell prompt that gives me a ton of information is what I look for in a shell prompt. Such as the prompt below:

```
joshv in 🌐 my_device in nautobot on  u/jvanderaa-update_install_home_doc is 📦 v2.2.5b1 via 🐍 v3.11.9 (nautobot-py3.11)
```

The default installation however did not get the same behavior as my previous Oh My Zsh set up with the zsh-autocompletions and zsh-syntaxhighlighting. Whenever I would hit the up arrow key, the system would cycle through the commands as comes default with zsh/bash. But I was looking for subcommand scrolling. Such as the following command sequence.

<!-- more -->

```bash linenums="1"
poetry init
ls
systemctl status nautobot
```

When I type **`poetry`** on the 4th command, I wanted the search to find **`poetry init`** immediately as my last used **`poetry`** command. To be honest, I'm not sure where the feature came from within my previous set up of Zsh, Oh my zsh, and the powerlevel10k setup that I was using. But it is part of my zen experience on a shell. 

## ChatGPT to the Rescue

I was about to abandon my Starship prompt and just get back to installing Oh my zsh and powerlevel10k when I decided to ask ChatGPT:

> Ok, the Starship prompt is not getting me what I would like. I may just go back to oh my zsh to get the proper suggestions. Tell me if I could do this with starship.
> 
> Command 1: poetry env use 3.11.4  
> Command 2: ls  
> Command 3: systemctl status  
> 
> Now for command 4, when I start typing `poetry ` I want the up arrow key to suggest command 1. Right now it moves up to Command 4.

From there I got the response that inspired this post and to dive more into bindkeys. The suggestion came back to add the following to my `~/.zshrc` file:

```bash
# Custom history search bindings
bindkey '^[[A' history-search-backward
bindkey '^[[B' history-search-forward
```

With the bindkeys in place and testing, it gave me exactly what I was looking for out of my history searching on the command line. A quick reload of the shell environment and bam it took care of exactly what I was looking for.

## Summary

This post has been more for my own documentation for when I inevitably rebuild a system somewhere and need to find what I have done in the past. I'm hopeful that this post may help out others as well, as this is the reason that I put things out in a blog format instead of just keeping an internal wiki. Thanks for the read!

-Josh