---
authors: [jvanderaa]
toc: true
date: 2020-06-27
layout: single
comments: true
slug: docker_for_automation_environment_ansible_210
title: Docker for Automation Environment - Ansible 2.10
# categories:
# - Ansible
tags:
- docker
- ansible
- netdevops
---

Docker is a terrific solution for making a consistent working environment. It's been about a year or
so since I built my very first own Docker container. I had always known why you use a container, but
was always intimidated too much so to even get started. I am glad that I did get started and am off
on my journey of using Docker containers. Let me jump into the problem and why? Couple the recent
experiences with Docker, and the upcoming move to slim down Ansible and install Collections for
most Network Automation modules, I thought it would be a good thing to get a write up done.

<!-- more -->


## Problem

From a Network Automation standpoint, there is much change still occurring in the tooling ecosystem.
First that January 1, 2020 marked the end of support for Python 2.7. Yet there are still many setups
that require Python 2.7.  

Upcoming Ansible is changing the behavior from a full batteries included for Network Automation
tooling, moving over to a base package where you install Collections on top of it. This is going to
be, in my opinion, a second driver for really digging into using containers for your enterprise
automation envrionment.

## Why is it a Solution?

### Ansible Experience

This is a solution because it helps that you do your development work within a container. When you
run the command `ansible-playbook` you are getting the `ansible-playbook` executable that is built
into the container image. If outside of a container, there are several things that could happen. You
may install some things with Python 2, could with Python 3, which version of Python 3? Which version
of Python does the executables associated with Ansible reference? There are several methods to get
multiple versions of Python to be executing on your system. Installing Ansible dependencies into the
wrong Python PIP can definitely hamper it.

### I Don't Use Ansible, Why Then?

This is an answer still for both Ansible and Python a like. One, if you mess up an installation you
just rebuild the container image. Yes, it is shorter to just delete a virtual environment as well.
When you go to install the Python application into the customer environment, you get portability, as
you bring your own Python installation with the container. As long as the customer supports
containers it adds portability. No more differing sets of instructions. Just a simple, docker
command or update of a docker-compose file and away you go.  

### Portability

One of the tenants of the [12-factor app](https://www.12factor.net) for developing modern apps is to
ask the question if you could open source your project tomorrow. If developing in virtual
environments you will still need to have a setup instruction set that could miss something that you
just have in your environment. With a container you bring a blank OS to the table inside of the
container. You install explicitly everything you need to get the app up and running.

### RHEL vs Ubuntu vs MacOS vs Any Other Linux OS

The next thing about containers if you are going to interact with a file system in any way is that
you get consistency for your app. No longer do you need to understand how to interact with MacOS
with this command, and CentOS is this command, and Ubuntu is this other command. You choose the base
OS image, and interact with it as such.

## Getting Started

My methodology for getting started with Docker was to read some getting started guides, and adapt
them for my Network Automation flavor. I'm going to try to walk you along so you can learn from some
of the things I learned along the way, and improve upon them.  

I started off with installing Docker Desktop on my Mac. The best way to get started is to install
Docker onto your OS of choice. The installation guide is https://docs.docker.com/get-docker/. There
is also a HomeBrew package available for installing Docker as well.  

### Docker Labs on the Internet

There are several resources available on the Internet for you to get experience with Docker.

- [Cisco DevNet Learning Labs](https://developer.cisco.com/learning/lab/docker-101/step/1)
- [Play with Docker Labs](https://labs.play-with-docker.com/) 

I encourage you to take a look at these if you do not want to get started on your own in your own
machine. The following examples will be done on your local machine.

### Writing A Dockerfile

A Dockerfile is the set of instructions of how to build your container. So if you want to follow
along, create a directory anywhere that is accessible via command line called `docker_test`. Take
the following and paste it into a file called `Dockerfile`.  

```bash
FROM python:3.8.3-slim-buster

RUN apt-get update && apt-get install sshpass vim -y

COPY . /local
WORKDIR /local

RUN pip install -r requirements.txt
RUN ansible-galaxy collection install -r requirements.yml
```

What this is doing:

| Line Number | Outline                                                                                                                |
| ----------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1           | Selecting the base image, this can be found on https://hub.docker.com, searching Python                                |
| 3           | Installing `sshpass` and `vim` via apt. Updating the apt repo list first. Being a slim image, VIM is not pre-installed |
| 5           | Copies everything in the local directory into a directory /local                                                       |
| 6           | Changes the working directory, similar to `cd` in many OSes                                                            |
| 8           | Installs Python packages from the local `requirements.txt` file that was copied on line 5                              |
| 9           | Uses `ansible-galaxy` to install Galaxy collections from the local `requirements.yml` file                             |

To have this work right, lets use this as an opportunity to test out installing the new version of
Ansible into a container, by pip installing `ansible-base`.  

In order to build this container, you will need to have a requirements file ready to go for both
Python and Ansible Galaxy. So to this effort, here are those two files with a few packages:

#### requirements.txt

```toml {linenos=true}
ansible-base
```

The only Python package going to install this for is `ansible-base` which will install the current
beta versions of Ansible Base 2.10.

#### requirements.yml

```yaml

---
# Collection Installations
collections:
  - name: cisco.asa
    version: 1.0.0

```

This has a few more keys to the requirements.yml file that Ansible Galaxy will install with. The YML
file first has a key of `collections`. This is because you can use the file to install both roles
and collections, not just collections. Here this will install the 1.0.0 release of the Ansible
modules for the Cisco ASA platform. You will likely need to add additional roles to here. To get the
name you leverage https://galaxy.ansible.com to search and find the modules that you would install.

## Helper

The last piece I'd like to provide some info on as well is a helper file. Many of the *nix systems
have Make available to them. If unable to use Make on your filesystem, I will suggest to take a look
at the Python package [invoke](http://www.pyinvoke.org/). Invoke does have more flexibility than
make as it is written in Python, but for this demo I want to use Make so you can see the command
line commands that are used.  

The arguments for Make are made available by defining information in a `Makefile`. Here is the
Makefile that I will be using for this:

```bash

IMG_NAME=jvanderaa/network_automation
IMG_VERSION=2.0-rc2
.DEFAULT_GOAL := cli

.PHONY: build
build:
	docker build -t $(IMG_NAME):$(IMG_VERSION) . 

.PHONY: cli
cli:
	docker run -it \
		-v $(shell pwd):/local \
		-w /local \
		$(IMG_NAME):$(IMG_VERSION) bash

```

| Line Number | Action                                                                                                                                                                                    |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1           | Defining a variable for image name, here `jvanderaa/network_automation`                                                                                                                   |
| 2           | Defining a variable for IMG_VERSION so you can version your Docker containers                                                                                                             |
| 3           | Setting a default goal so you can just type make and that is what will be done                                                                                                            |
| 5           | .PHONY is saying that this is a phony file that is upcoming. It is best practice to include but not required                                                                              |
| 6           | The key build: is what will be executed with the `make build` command                                                                                                                     |
| 7           | The actual command, it is **tabbed** in. You **MUST NOT** use spaces and **MUST** use tabs with Make                                                                                      |
| 9           | Definition of .PHONY for CLI                                                                                                                                                              |
| 10          | Defining a key of cli for `make cli` or just `make` due to the default goal defined                                                                                                       |
| 11          | Start of the Docker run command, which includes mapping the local directory into the container directory so you can make live updates, changing the working directory, and launching bash |

## Building The Container

First in my container image list I have no containers (I just pruned them all, and they are now all
deleted with the command `docker system prune -a`):

```bash {linenos=true}

$ docker image ls       
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE

```

With no containers, I execute the command from the `Makefile` of `make build`. This will download
all of the layers, run the apt installations, pip install, and galaxy install. The output is below
with many of the lines removed.

```bash {linenos=true}

docker build -t jvanderaa/network_automation:2.0-rc2 . 
Sending build context to Docker daemon   5.12kB
Step 1/6 : FROM python:3.8.3-slim-buster
3.8.3-slim-buster: Pulling from library/python
8559a31e96f4: Pull complete 
62e60f3ef11e: Pull complete 
93c8ae153782: Pull complete 
ea222f757df7: Pull complete 
e97d3933bbbe: Pull complete 
Digest: sha256:938fd520a888e9dbac3de374b8ba495cc50fe96440030264a40f733052001895
Status: Downloaded newer image for python:3.8.3-slim-buster
 ---> 9d84edf35a0a
Step 2/6 : RUN apt-get update && apt-get install sshpass vim -y
 ---> Running in 66e37abb454a


[ I REMOVED A BUNCH OF LINES HERE]

Step 6/6 : RUN ansible-galaxy collection install -r requirements.yml
 ---> Running in 94ca0bb3f3c9
Starting galaxy collection install process
Process install dependency map
Starting collection install process
Installing 'cisco.asa:1.0.0' to '/root/.ansible/collections/ansible_collections/cisco/asa'
Installing 'ansible.netcommon:1.0.0' to '/root/.ansible/collections/ansible_collections/ansible/netcommon'
Removing intermediate container 94ca0bb3f3c9
 ---> 0805ddb1719f
Successfully built 0805ddb1719f
Successfully tagged jvanderaa/network_automation:2.0-rc2

```

If you have followed along, congratulations, you have created your first Docker Image. This is what
will be used to create additional containers, which are a copy of the image, but a whole separate
container.  

Because of the tags, I prefer to use the `Makefile` to execute my containers as well. Now I just go
to the command line within the container by issuing `make cli` command. This will then take me to
the root user prompt of my conatiner.

```yaml {linenos=true}

$ make cli  
docker run -it \
                -v /Users/joshv/projects/docker_test:/local \
                -w /local \
                jvanderaa/network_automation:2.0-rc2 bash
root@58a4ea071203:/local# ansible-galaxy collection list

# /root/.ansible/collections/ansible_collections
Collection        Version
----------------- -------
ansible.netcommon 1.0.0  
cisco.asa         1.0.0  

```

Inside of the container I execute the command `ansible-galaxy collection list`. This now shows me
that there are two collections installed:

- ansible.netcommon
- cisco.asa

## Summary

With the container built, and a Dockerfile in place. I can now upload the Dockerfile along with the
rest of the project file to Git. This coupled with the Makefile will help to build any system
quickly. No more trying to find a place to host the Docker image (like Docker Hub), how to install
into the proper Python executable any modules that may be needed (like pandevice for PANOS modules)
or other SDKs that are helpers to the Ansible Collections being created.  

Hopefully this has been helpful. Take a look at the links!

Thanks,

-Josh