---
author: Josh VanDeraa
title: "Nautobot Environment File"
date: 2023-08-17
tags:
  - nautobot
  - automation
draft: false
coverAlt: The Environment
coverCaption: |
  Photo by <a href="https://unsplash.com/@tibrewalpratik?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Pratik Tibrewal</a> on <a href="https://unsplash.com/photos/P5keEjqg6zM?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
---

Within Nautobot there are many ways to be able to get the Nautobot environment running. Environment variables are used quite a bit in the Docker environment following best practice principles set forth in the [12 Factor App](https://12factor.net/). The use of environment variables is helpful for working through the various stages of an application to production. The installation instructions leverage a single environment variable `NAUTOBOT_ROOT` and that is set in the SystemD files shown below:

```systemd {linenos=table,hl_lines=[10]}
/etc/systemd/system/nautobot.service
[Unit]
Description=Nautobot WSGI Service
Documentation=https://docs.nautobot.com/projects/core/en/stable/
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
Environment="NAUTOBOT_ROOT=/opt/nautobot"

User=nautobot
Group=nautobot
PIDFile=/var/tmp/nautobot.pid
WorkingDirectory=/opt/nautobot

ExecStart=/opt/nautobot/bin/nautobot-server start --pidfile /var/tmp/nautobot.pid --ini /opt/nautobot/uwsgi.ini
ExecStop=/opt/nautobot/bin/nautobot-server start --stop /var/tmp/nautobot.pid
ExecReload=/opt/nautobot/bin/nautobot-server start --reload /var/tmp/nautobot.pid

Restart=on-failure
RestartSec=30
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

This is great if there are only a few environment variables, and since SystemD files are only available via the root user, there is some protection.

## Environment File

There is also a method that is supported of using an environment file. The environment file allows for putting several variables into a single file that can then be loaded by the application. Let's start with the file format itself.

The file itself is recommended to live at the Nautobot root and be named `.env`, `/opt/nautobot/.env`. It really could be named anything, as long as it is known to you and your organization.

### Environment File Format

The format is an environment variable per line matching the syntax. So if you want to add to the environment NAPALM credentials for example, then you would have the following in the file, where the `#` is a comment when loading. You should be creating this file as the Nautobot user:

```bash
# Change to the Nautobot User
sudo -iu nautobot

# Create the file, you can use Nano or other text editors if you choose.
vim .env
```

```env
# /opt/nautobot/.env

# NAPALM Credentials
NAPALM_USERNAME=my_user
NAPALM_PASSWORD=what_is_that_password_again
```

Note on the environment variables show there are no quotes. You could also put quotes into the environment variable. Use the comment character to help to organize your credentials. So now there is a file with environment items, which may include credentials, now what?

### File Permissions

It is a good practice to restrict the permissions on the file to that of the Nautobot user. So that only those that can get to the Nautobot user on the system are able to read the file. To update this to being only readable (and editable) to the Nautobot user. So this is executed as the Nautobot user again.

```bash
chmod 0600 .env
```

### Using the Environment File

The last step in using the `.env` file that was created is to now reference that in the SystemD files. Note that you will need to make this change for each of the SystemD files including if using the core docs of `nautobot`, `nautobot-worker`, `nautobot-scheduler`. If there are any other files that you have added as well, you will need to update these. These files should be updated as the root user:

```bash
sudo vi /etc/systemd/system/nautobot.service
```

```systemd {linenos=table,hl_lines=[11]}
# /etc/systemd/system/nautobot.service
[Unit]
Description=Nautobot WSGI Service
Documentation=https://docs.nautobot.com/projects/core/en/stable/
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
Environment="NAUTOBOT_ROOT=/opt/nautobot"
EnvironmentFile=/opt/nautobot/.env

User=nautobot
Group=nautobot
PIDFile=/var/tmp/nautobot.pid
WorkingDirectory=/opt/nautobot

ExecStart=/opt/nautobot/bin/nautobot-server start --pidfile /var/tmp/nautobot.pid --ini /opt/nautobot/uwsgi.ini
ExecStop=/opt/nautobot/bin/nautobot-server start --stop /var/tmp/nautobot.pid
ExecReload=/opt/nautobot/bin/nautobot-server start --reload /var/tmp/nautobot.pid

Restart=on-failure
RestartSec=30
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

{{< alert >}}
It is important to note that there are no quotes/double quotes around the file path. If you put these in, there will be issues. I had invested a fair bit of time the first time troubleshooting why my environment variables are not loading.
{{< /alert >}}

Once all of the files have been updated, you should complete a daemon reload:

```bash
sudo systemctl daemon-reload
```

## Loading the Environment Variables on Login of Nautobot

Now there are variables in the file that by default do not get loaded. If you try to run `source /opt/nautobot/.env` then you will not have the proper format to load these. As the Nautobot user, modify the `/opt/nautobot/.bashrc` file, adding the following to the end of the file (from this [gist](https://gist.github.com/mihow/9c7f559807069a03e302605691f85572)). The highlighted line the `.env` file should match what you name the file.

```bash {linenos=table,hl_lines=[2]}
set -o allexport
source /opt/nautobot/.env
set +o allexport
```

Now whenever you enter the bash prompt for the Nautobot user, then the environment is loaded. This is especially helpful if the database credentials are being controlled via the environment.

## Summary

I hope this helps out some folks over time on getting rolling with Nautobot and some of the capabilities. I myself have had to research this several times and wanted to get something out to be able to be a reference in order to get additional capabilities going. Let me know in the comments or on a social media link if you found this helpful!

Josh