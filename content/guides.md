---
title: Network Automation Guides
date: 2026-03-09
draft: false
type: "page"
---

Years of writing blog posts on network automation led me to a simple realization: engineers need more than scattered articles. They need a structured, hands-on path from zero to working automation - with real devices, real output, and no fluff.

These guides are lab-driven references built for network engineers who are ready to stop doing things manually. Each guide covers a core automation tool using Arista EOS in Containerlab so you can follow along and run every example yourself.

All guides are available at **[guides.josh-v.com](https://guides.josh-v.com)**.

---

## Ansible for Network Engineers

<img src="https://guides.josh-v.com/images/logo.png" alt="Ansible for Network Engineers" style="float:right;width:80px;height:80px;margin:0 0 1rem 1.5rem;border-radius:0.75rem;box-shadow:0 2px 8px rgba(0,0,0,0.15);">

Ansible is one of the most widely adopted automation tools in network engineering - and for good reason. It is agentless, uses human-readable YAML playbooks, and has deep support for network devices via the `arista.eos`, `cisco.ios`, and `ansible.netcommon` collections.

This guide takes you from your first inventory file to templated configs, roles, facts gathering, and troubleshooting across a six-device Arista cEOS lab.

**What you will learn:**

- Building inventories and running your first playbook
- Configuring devices with `eos_config` and understanding idempotency
- Generating device configs from Jinja2 templates and variable files
- Organizing playbooks into reusable roles
- Gathering and parsing structured facts from devices
- Multi-vendor deployment patterns
- Troubleshooting and debugging Ansible runs

**8 chapters &bull; Validated against live Arista cEOS lab &bull; $19**

<a href="https://joshvguides.lemonsqueezy.com/checkout/buy/8724ae26-ac0e-49bc-bf76-76aa1e7e656f?embed=1" class="lemonsqueezy-button" style="display:inline-block;margin-top:0.5rem;padding:0.5rem 1.25rem;background:#2563eb;color:#fff;border-radius:0.5rem;font-weight:600;font-size:0.9rem;text-decoration:none;">Buy Now - $19</a>

---

## Coming Soon

The following guides are in progress:

- **Netmiko / Scrapli** - SSH automation with Python. Script show commands at scale and push configs without Ansible overhead.
- **NAPALM** - Vendor-neutral network automation. Getters, config replace, config merge across multiple OS types.
- **Nornir** - Pure Python automation framework. Parallelism, inventory plugins, and building your own automation scripts.
- **Go for Network Engineers** - Build fast, compiled network tooling with Go.

---

## Automators Subscription

Get every guide - current and future - for one annual price.

**$49/year** includes all guides across all topics, plus updates as new guides ship.

<a href="https://joshvguides.lemonsqueezy.com/checkout/buy/e16fed0c-338f-40de-8eda-cf805b01e1c1?embed=1" class="lemonsqueezy-button" style="display:inline-block;margin-top:0.5rem;padding:0.5rem 1.25rem;background:#2563eb;color:#fff;border-radius:0.5rem;font-weight:600;font-size:0.9rem;text-decoration:none;">Subscribe - $49/year</a>

<script src="https://assets.lemonsqueezy.com/lemon.js" defer></script>
