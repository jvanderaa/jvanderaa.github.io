---
author: Josh VanDeraa
title: "Creating Your Own Validation"
date: 2025-12-20
tags:
  - python
  - nautobot
  - ssot
draft: false
summary: >
    I recently was presented with a request to look at where there was a request to validate that a Rack would be unique at a Location in Nautobot. I took a look at the data validation engine and wasn't able to determine a method to make this work there. So here is the solution.
coverAlt: Alternative Cover Art Words
coverCaption: |
    Photo by <a href="https://unsplash.com/@makabera?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Markus Kammermann</a> on <a href="https://unsplash.com/photos/a-stiff-bristled-brush-on-a-concrete-floor-p5NKub2JdgM?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
---

I recently was presented with a request to look at where there was a request to validate that a Rack would be unique at a Location in Nautobot. I took a look at the data validation engine and wasn't able to determine a method to make this work there. So here is the solution.

## Solution

The solution to this is to create a [Custom Validator](https://docs.nautobot.com/projects/core/en/stable/development/apps/api/platform-features/custom-validators/). The whole point of the Custom Validators is to allow you to enforce your own business rules while allowing the Open Source project to remain open and general. In the case of keeping Nautobot generic, Racks are allowed to have the same name anywhere. Sometimes within the same location. Which some organizations may have. The project shouldn't enforce something when there is the possibility of the scenario being true.

## Implementation of the Solution

Now let's dive through the steps taken to get the solution built and tested. This is where the inspiration for my previous post on [using Python UV for tools and Python version management]({{< relref "../CleaningUpPythonEnvironment/index.md" >}}) came to be. Here is the process where I started from scratch:

1. Used the [Nautobot App Cookiecutter](https://github.com/nautobot/cookiecutter-nautobot-app/) to create a Sandbox application for me to test the environment
2. Added some test data including a Site and some racks
3. Validated that I could make a rack with the same name as an existing rack
4. Wrote and debug the Custom Validator
5. Tested that the Rack name would now need to be unique

### Creating an app from the Cookiecutter repo

First step is to get yourself a sandbox Nautobot App for you to be able to work from. To do this 

```bash {title="Cookiecutter Bake a Cookie"}
cookiecutter https://github.com/nautobot/cookiecutter-nautobot-app --checkout main --directory="nautobot-app"
```

The folks (and myself) and NTC have given a bunch of prompts that will fill in various components of the repository as it gets built. This is just the start. Here are what I set for my sandbox repository:

```bash {title="Cookiecutter Input."}
❯ cookiecutter https://github.com/nautobot/cookiecutter-nautobot-app --checkout main --directory="nautobot-app"
  [1/16] codeowner_github_usernames (): jvanderaa
  [2/16] full_name (Network to Code, LLC): Josh-V
  [3/16] email (info@networktocode.com): joshv@example.com
  [4/16] github_org (nautobot): jvanderaa
  [5/16] app_name (my_app): sandbox_app
  [6/16] verbose_name (Sandbox App):
  [7/16] app_slug (sandbox-app):
  [8/16] project_slug (nautobot-app-sandbox-app):
  [9/16] repo_url (https://github.com/jvanderaa/nautobot-app-sandbox-app):
  [10/16] base_url (sandbox-app):
  [11/16] camel_name (SandboxApp):
  [12/16] project_short_description (Sandbox App):
  [13/16] Camel case name of the model class to be created, enter None if no model is needed (SandboxAppExampleModel):
  [14/16] Select open_source_license
    1 - Apache-2.0
    2 - Not open source
    Choose from [1/2] (1):
  [15/16] docs_base_url (https://docs.nautobot.com):
  [16/16] docs_app_url (https://docs.nautobot.com/projects/sandbox-app/en/latest):

Congratulations! Your cookie has now been baked. It is located at /Users/joshv/projects/nautobot-app-sandbox-app

⚠️⚠️ Before you start using your cookie you must run the following commands inside your cookie:

* poetry lock
* poetry install
* poetry self add poetry-plugin-shell
* poetry shell
* invoke makemigrations
* invoke ruff --fix # this will ensure all python files are formatted correctly, may require `sudo chown -R $USER ./` as migrations may be owned by root

Note: The file `development/creds.env` may be automatically created and ignored by git. It can be used to override default environment variables within the docker containers.
```

For each of these steps, I'll make them expandable. Each of the steps after "baking the cookie" are laid out to include:

- Changing the directory to where the cookie was baked to
- Running the command `poetry lock` to make a Poetry lock file
> [!EXAMPLE]- Poetry lock output
> ```bash {title="poetry lock command output"}
> ❯ poetry lock
> Creating virtualenv sandbox-app in /Users/joshv/projects/nautobot-app-sandbox-app/.venv
> Updating dependencies
> Resolving dependencies... (16.2s)
> 
> Writing lock file
> ```
- Running `poetry install` to install all of the packages
- Running `poetry self add poetry-plugin-shell` to get a Poetry shell, this was a recent change in Poetry 2.0 that separated the creating the shell from other utilities
- Running `poetry shell` to activate the virtual environment is recommended. I'm going to recommend otherwise to use the command `source .venv/bin/activate`. I have not had success installing the shell without it being installed in the system Python.
> [!EXAMPLE]- source .venv/bin/activate output
>
> ```bash {title="source .venv/bin/activate command output"}
> ❯ source .venv/bin/activate
> source /Users/joshv/projects/nautobot-app-sandbox-app/.venv/bin/activate
> ```
- Running the migrations
- And then fixing the formatting of the files that the migrations made

