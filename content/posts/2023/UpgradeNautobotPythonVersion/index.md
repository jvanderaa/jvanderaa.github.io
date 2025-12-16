---
author: Josh VanDeraa
title: "Upgrade Nautobot Python Version in Virtual Machine"
slug: upgrade-nautobot-python-virtual-machine
date: 2023-08-14
tags:
  - nautobot
  - automation
draft: false
coverAlt: Heavy machinery for road work
coverCaption: |
  Photo by <a href="https://unsplash.com/@luandmario?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Maria Lupan</a> on <a href="https://unsplash.com/photos/XeRqsvi9qBc?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  
---

One observation lately is that Python is moving along quickly with new versions and new EOLs. Along with needing to make these updates, the applications that Python uses will also need to be moving along. Nautobot is my favorite, and in my opinion the best SOT platform available in the open source ecosystem today. So let's dive into the updating of the Python version.

For this post, I've created a new Rocky 8 Virtual Machine to be the host. See the note below for the reasoning. This will start off with a Nautobot [install](https://docs.nautobot.com/projects/core/en/stable/installation/) from the Nautobot docs. I won't dive into all of that, assume that is the starting point with a fresh Nautobot application.

> I originally thought just doing a DNF update on the host that I would be able to use Python 3.8 or something of that nature. I was wrong. Running the DNF update put Python3.11 on the host. So now it is on to removing Python3.11 and move to 3.8 for this post. I completed this step with a `sudo dnf install python3.8`

{{< alert "circle-info" >}}
It is a strong recommendation to not have to follow this process. In that you should be looking to be using infrastructure that can be destroyed and recreated. Such as with Docker containers or having the build process to be able to replace virtual machines as needed.
{{< /alert >}}

## My Original Challenges With Upgrading Python

Going back a few years I had the experience that was terribly painful to update Python versions on RHEL 7 and its derivatives. All of the documentation that I had found required to install Python from source, that you were not able to use DNF/YUM to just get the latest version of Python. Thankfully since RHEL8 and its derivatives, it is much simpler. Now DNF just is able to install and off we go.

## Explaining the Upgrade Path

If you followed the instructions on the Nautobot installation docs for your virtual machine build, this will become pretty quick. The installation method has a virtual environment created. So in order to update the version of Python, with the help of the Python VENV capabilities, it is a short process.

1. Install the desired version of Python on your system (`sudo dnf install python3.11` or `sudo apt install python3.11`)
2. Verify the Python command to run the latest version (`python3 -V`)
3. Make a backup of the requirements and the directory
4. Remove the existing virtual environment files
5. Recreate the virtual environment with the new version of Python
6. Re-install the Python packages
7. Restart the Nautobot services

## The Upgrade

The process will begin with saving the current pip freeze requirements to a tmp file. THis is going to provide a quick method to re-install the Python packages required for your Nautobot instance.

```
pip freeze > /tmp/nautobot_requirements.txt
```

### Remove Bad Requirement

The `backports.zoneinfo` requirement that gets generated is deprecated and within Python3.9 should not be used. To accommodate for this remove any reference to backports.zoneinfo from the `tmp/nautobot_requirements.txt` file.

### Create a Backup of Directory

With the file in place, now let's move the copy the nautobot user directory to another directory. Most likely this will not be required, but if you need to do a restore of the directory having a backup is good practice.

```
[user@rocky-nautobot ~]$ sudo cp -a /opt/nautobot /opt/nautobot-old
```

### Remove Existing Virtual Environment

Now to remove the existing Nautobot virtual environment by removing the bin directory (`/opt/nautobot/bin`).

```
sudo -u nautobot rm -rf /opt/nautobot/bin
```

### Create New Virtual Environment

Create a new virtual environment into `/opt/nautobot` by using the same command from the install instructions.

```
sudo -u nautobot python3 -m venv /opt/nautobot
```

Now log in as the Nautobot user to update the `pip` and `wheel` packages. And from there install the rest of the requirements.txt items that were saved off earlier.

```
sudo -iu nautobot
pip install --upgrade pip wheel
pip install -r /tmp/nautobot_requirements.txt
```

### Restart Services

The last step is to restart the services for Nautobot, which will then pick up the new Python version.

```bash
# Exit out of the Nautobot user
exit

sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```

## Summary

While the recommended method for upgrading the Nautobot application is to create a new virtual machine, migrate the database over, and reclaim the previous host, that may not always be a viable option. This process is just tested out on my lab environment and has not been done in a production environment yet, but this should work.