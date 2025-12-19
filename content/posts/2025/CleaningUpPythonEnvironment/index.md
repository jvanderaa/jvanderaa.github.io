---
author: Josh VanDeraa
title: "Cleaning Up Python Environment"
date: 2025-12-18
tags:
  - python
  - uv
draft: false
summary: >
    Recently I updated my Python development environments to use Python UV for managing Python versions and tools on the system. In this post I take you on the journey that I went on to replace pyenv and Pipx.
coverAlt: Alternative Cover Art Words
coverCaption: |
    Photo by <a href="https://unsplash.com/@makabera?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Markus Kammermann</a> on <a href="https://unsplash.com/photos/a-stiff-bristled-brush-on-a-concrete-floor-p5NKub2JdgM?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
---

The one challenge that I have had for many years is working with Python and the local system. So much so that I have had good discussions with many of the pure Python developers at [NTC](https://www.linkedin.com/company/network-to-code/). It often involved my statements along the lines of putting everything inside of a [Docker](https://www.docker.com/) container or something to that effect. I still distinctly remember my first attempt at installing pyenv completely borked my Ansible environment. A very technical term I know.

Now today I was suggested to take a look at using [Python UV](https://docs.astral.sh/uv/guides/install-python/) for managing the Python tools and environments. After taking a few steps on the journey I am convinced that this is the method that I am going to be going on.

## Making the Switch

So the previously used environment consisted of pyenv for managing the versions of Python and Pipx for managing the tools that were installed via Python. Poetry is still the NTC tool of choice for managing Python packages and libraries. So this was a must have to integrate fine with Poetry for the NTC projects. To make the switch happen there is first the uninstall of the current tools and then the instalation of the new system.

### Uninstalling Pyenv

The first step is to remove pyenv from being loaded by any shells that may be using, such as by bash (`.bashrc`) or ZSH (`.zshrc`). I found this to be a critical step the hard way. So the first thing on my machines since I'm using ZSH is to start by commenting out the references to pyenv in that file.

```bash {title="Remove all pyenv settings from loading"}
vi ~/.zshrc
```

After commenting out the lines with `#` I reloaded the shell.

```bash {title="Reload ZSH"}
source ~/.zshrc
```

In my particular configuration I had two sections to comment out. A PATH statement near the top and near the bottom of the file a pyenv specific section.

Once the environment is set to no longer load pyenv, next up is to remove the directory that maintains the pyenv data and removing pyenv that was previously installed via Homebrew.

```bash {title="Remove pyenv directory"}
rm -rf ~/.pyenv
```

```bash {title="Uninstall pyenv"}
brew uninstall pyenv
```

> [!EXAMPLE]+ Example Output Uninstalling pyenv
>
> ```bash
> ❯ brew uninstall pyenv
> Uninstalling /opt/homebrew/Cellar/pyenv/2.6.16... (1,407 files, 4.6MB)
> ==> Autoremoving 3 unneeded formulae:
> autoconf
> m4
> pkgconf
> Uninstalling /opt/homebrew/Cellar/pkgconf/2.5.1... (28 files, 532.2KB)
> Uninstalling /opt/homebrew/Cellar/autoconf/2.72... (72 files, 3.8MB)
> Uninstalling /opt/homebrew/Cellar/m4/1.4.20... (14 files, 802.1KB)
> ```

Once the 


### Removing Pipx

Next up is to remove Pipx. This was primarily installed for me to install Python Poetry. This will still be installed, just done via Python UV instead. I had done the installation of pipx via HomeBrew:

```bash
brew uninstall pipx
```

### Brew Cleanup

At the end of removing these applications that were installed for me on Homebrew, I'm now running a `brew cleanup` command to remove the old pieces.

```bash {title="brew cleanup"}
brew cleanup
```

## UV For Tools

I'm going to skip right past the [UV installation steps](https://docs.astral.sh/uv/getting-started/installation/) since the UV documentation handles this nicely. First tool that I'm going to need to install is [Python Poetry](https://python-poetry.org/docs/). The docs suggest to use Pipx, but we just removed that in the line before. The installation is actually quite simple. Just a single command of `uv tool install poetry`.

```bash {title="Install Python Poetry with UV"}
uv tool install poetry
```

> [!EXAMPLE]+ Example output of installing poetry with UV
>
> ```bash {title="Installation of Poetry"}
> ❯ uv tool install poetry
> Resolved 43 packages in 216ms
> Prepared 29 packages in 261ms
> Installed 43 packages in 29ms
>  + anyio==4.12.0
>  + build==1.3.0
>  + cachecontrol==0.14.4
>  + certifi==2025.11.12
>  + cffi==2.0.0
>  + charset-normalizer==3.4.4
>  + cleo==2.1.0
>  + crashtest==0.4.1
>  + distlib==0.4.0
>  + dulwich==0.24.10
>  + fastjsonschema==2.21.2
>  + filelock==3.20.1
>  + findpython==0.7.1
>  + h11==0.16.0
>  + httpcore==1.0.9
>  + httpx==0.28.1
>  + idna==3.11
>  + installer==0.7.0
>  + jaraco-classes==3.4.0
>  + jaraco-context==6.0.1
>  + jaraco-functools==4.3.0
>  + keyring==25.7.0
>  + more-itertools==10.8.0
>  + msgpack==1.1.2
>  + packaging==25.0
>  + pbs-installer==2025.12.17
>  + pkginfo==1.12.1.2
>  + platformdirs==4.5.1
>  + poetry==2.2.1
>  + poetry-core==2.2.1
>  + pycparser==2.23
>  + pyproject-hooks==1.2.0
>  + rapidfuzz==3.14.3
>  + requests==2.32.5
>  + requests-toolbelt==1.0.0
>  + shellingham==1.5.4
>  + tomlkit==0.13.3
>  + trove-classifiers==2025.12.1.14
>  + typing-extensions==4.15.0
>  + urllib3==2.6.2
>  + virtualenv==20.35.4
>  + xattr==1.3.0
>  + zstandard==0.25.0
> Installed 1 executable: poetry
> ```

With that Poetry is now installed.

### Cookiecutter Installation

Also as part of the installation in order to get started easily with creating Nautobot Apps is the use of Python [CookieCutter](). The tool installs in a snap with UV, taking less than half a second to install everything:

```bash {title="Install Cookiecutter"}
uv tool install cookiecutter
```

> [!EXAMPLE]+ Output during the install of Cookiecutter
>
> ❯ uv tool install cookiecutter
> Resolved 22 packages in 230ms
> Prepared 12 packages in 116ms
> Installed 22 packages in 27ms
> + arrow==1.4.0
> + binaryornot==0.4.4
> + certifi==2025.11.12
> + chardet==5.2.0
> + charset-normalizer==3.4.4
> + click==8.3.1
> + cookiecutter==2.6.0
> + idna==3.11
> + jinja2==3.1.6
> + markdown-it-py==4.0.0
> + markupsafe==3.0.3
> + mdurl==0.1.2
> + pygments==2.19.2
> + python-dateutil==2.9.0.post0
> + python-slugify==8.0.4
> + pyyaml==6.0.3
> + requests==2.32.5
> + rich==14.2.0
> + six==1.17.0
> + text-unidecode==1.3
> + tzdata==2025.3
> + urllib3==2.6.2
> Installed 1 executable: cookiecutter
> ```

### Python Versions

The installation of different Python versions is just as easy. It's a `uv python install x.y` where `x`, `y`, and `z` are the version numbers. Such as 3.13. You can also specify the patch version as well.

```bash {title="Installing Python version 3.13"}
uv python install 3.13
```

This took only a few seconds to download and install!

> [!EXAMPLE]+ Installation of Python 3.13 with UV
> ```bash {title="Installation example for uv python install 3.13"}
> ❯ uv python install 3.13
> Installed Python 3.13.11 in 578ms
>  + cpython-3.13.11-macos-aarch64-none (python3.13)
> ```

## Summary

At this point I'm not going back. I hold myself the right to change or if there are other issues that arise. But the use of Python UV to handle the tools and Python software versions is here to state for a bit for me. What do you think? Let me know in the comments.

-Josh
