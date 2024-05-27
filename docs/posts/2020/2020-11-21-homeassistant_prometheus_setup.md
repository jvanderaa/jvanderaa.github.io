---
authors: [jvanderaa]
date: 2020-11-21
layout: single
comments: true
slug: homeassistant-prometheus
title: Home Assistant Prometheus Exporting Setup
collections:
  - homeassistant
categories:
- homeassistant
- prometheus
toc: true
---

There does not appear to be a complete set of documentation pieces available for setting up Prometheus on the Home Assistant platform. This post will take you along on my journey of setting up the Home Assistant to get metrics from it. The link for the documentation is a good start at getting Prometheus installed. [https://www.home-assistant.io/integrations/prometheus/](https://www.home-assistant.io/integrations/prometheus/)

## Starting Prometheus

1. Edit your `configuration.yaml` file
2. Add in a key of `prometheus:` 
3. Add in any parameters you may need, but just they key alone is enough to start the exporter

Once you have started the exporter, I was still getting a 404 not found. So I did restart the Home Assistant.

## Installation of Prometheus Endpoint

The first thing that is different from most of the times that I have used Prometheus is that this implementation puts the information behind an authorization page. This is not so bad, but it definitely threw me for a loop for a short bit. There are a few options that I looked at for getting past the authentication issue

### Legacy Tokens

The first thing I looked at was the legacy tokens. But quickly moved beyond this as Legacy wording is key. It is going away in the future and since this is a new setup, I didn't want to use anything legacy.

### Trusted Networks & Authentication Providers

I started to take a look at [auth_providers](https://www.home-assistant.io/docs/authentication/providers/) and specifically the Trusted Networks aspect. I would love to be able to see what the Prometheus HTTP page looks like. However, making changes to the authentication mechanisms seemed like overkill for what I was looking to do.

Continuing to look at the Prometheus example:

```yaml
# Example Prometheus scrape_configs entry
  - job_name: 'hass'
    scrape_interval: 60s
    metrics_path: /api/prometheus

    # Legacy api password
    params:
      api_password: ['PASSWORD']

    # Long-Lived Access Token
    bearer_token: 'your.longlived.token'

    scheme: https
    static_configs:
      - targets: ['HOSTNAME:8123']
```

I kept finding the comment of "Long-Lived Access Token". This seems ideal for what we would want in an API based application. 

### Long Lived Access Token

This seems like the ideal state to get into. Setting this token is outlined [https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token). To get at the profile page for your user:

1. Select your username on the lower left
2. Scroll to the **very** bottom
3. Select Create Token
4. Save this token to your password manager → It will go away from sight

## Setup Prometheus

The final configuration that I used for the Prometheus scraping was set:

```yaml
  - job_name: 'homeassistant'
    scrape_interval: 60s
    metrics_path: /api/prometheus
    bearer_token: <token>
    static_configs:
      - targets:
        - "192.0.2.10:8123"
```

Substitute "192.0.2.10" with the IP address/name of your home assistant host.

## Verify Metrics

Once the scraping has been setup, go to your Prometheus end point, then search. My devices started showing up immediately with the measurement prefix of `hass` when there was nothing more specifically setup.

## Summary

Gathering metrics about your Home Automation platform is a fun thing to do, and to continue to gather experience on how to work with the modern metrics tooling. Whether the database is Prometheus or InfluxDB or other option, this can be helpful. This walked through looking at a couple of options for setting up Prometheus. Then once Prometheus was setup on the Home Assistant side, went and setup the Prometheus scraping configuration. Finally how to verify that you are getting appropriate metrics ingested.  

Note that I look to have a post in the future on why Home Assistant, where I have installed Home Assistant (there is some thought on this), and perhaps some of my graphs that I have being stored in Grafana at this time. I also hope to go through and setup the same for an InfluxDB instance as well.  

Hope this has helped. Leave a comment or give a thumbs up or down!  

Josh