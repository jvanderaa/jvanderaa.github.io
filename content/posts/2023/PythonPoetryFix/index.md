---
author: Josh VanDeraa
comments: true
date: 2023-06-29
slug: nornir-brief
tags:
- programming
- poetry
title: Poetry Fix
toc: true
---

The Python [Poetry](https://python-poetry.org/) is our go to package management system thus far, you can see that in all of the Python projects that Network to Code open sources, such as [Nautobot](https://docs.nautobot.com/projects/core/en/stable/), [pyntc](https://pyntc.readthedocs.io/en/latest/user/lib_overview/), [network-importer](https://github.com/networktocode/network-importer), and [NTC-Templates](https://github.com/networktocode/ntc-templates). Lately though, I've been having some challenges when my HomeBrew updates happen and my system Python gets updated. I've been able to recover with the help of the same few pages I land on from my Google searches. But since I've done this twice now, I'm using this post to document the fix as much as for myself, but for anyone else that may come across Poetry issues.

## The Issue

The issue occurs when I'm updating the system Python through HomeBrew. I start to see errors where Poetry is unable to be detected, with some nasty looking MacOS shell issues. Such as:

```
poetry Library not loaded: /opt/homebrew/Cellar/python@3.10/3.10.12/Frameworks/Python.framework/Versions/3.10/Python
```

With this error, I made the mistake (maybe) of just removing `poetry` by finding the location with `which poetry` and then removing that file. Not recommended.

## The Fix

The proper way that I'm finding to fix this is to run the Poetry uninstall scripts, which are found on the Poetry [docs](https://python-poetry.org/docs/).

```
curl -sSL https://install.python-poetry.org | python3 - --uninstall
curl -sSL https://install.python-poetry.org | POETRY_UNINSTALL=1 python3 -
```

Once it is removed, you try to re-install Poetry, but then you get the following symlinks issue:

```
raise Exception("This build of python cannot create venvs without using symlinks")
Exception: This build of python cannot create venvs without using symlinks
```

This is coming from a pyenv set up that I've also been convinced to run (however, I'm not convinced). So the next step is instead of installing to `python3`, you install to the current minor version of Python:

```
curl -sSL https://install.python-poetry.org | python3.10 -
```

## My Preferred Set Up For Various Versions of Python

My preferred method of running different versions of Python is the use of containers. Then you have a fully isolated system rather than running different versions within your shell. Allow the system Python to be that, the system. Then use containers to handle the different versions.

## Summary

This is my fix thus far that I have found. If there is a better way of getting Poetry to work with pyenv (until I uninstall it), I'd love to hear what the solutions are. Until next time, happy automating!

Josh