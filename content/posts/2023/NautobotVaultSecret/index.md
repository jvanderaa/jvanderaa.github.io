---
date: 2023-06-27
slug: nautobot-secrets-hashicorp-vault
categories:
- automation
- nautobot
- security
- hashicorp
- vault
title: Nautobot Secrets - Hashicorp Vault
toc: true
author: jvanderaa
params:
  showComments: true
---

With Nautobot, one of the things that came up was how to work with secrets. Nautobot itself is not the place to maintain secrets, as it is not a vault. There may be some good cryptographic libraries out to handle this, but by its nature, that is not the intent. So Nautobot has written methods to be able to retrieve secrets from proper vault sources and be able to leverage them. These can be tricky to get set up however. I had struggled for a while myself. So now that I have it working, I thought it would be a good time to have a quick personal blog about it.

<!--more-->

## Secrets Set Up

In my writing within the [Open Source Network Management](https://josh-v.com/book/) book I showed how to get started with Hashicorp Vault for secrets within Ansible. This is a natural progression to house my secrets for my Nautobot recommendation as well. This will not cover the set up of Nautobot for secrets. That is best to be done by the provider [documentation](https://github.com/nautobot/nautobot-plugin-secrets-providers#hashicorp-vault-1). This will however dive into how the vault is set up in my environment, and how that translates into Nautobot.

## Nautobot Parameters

When setting up a Hashicorp Vault secret in Nautobot, you will need the following parameters:

- Path
- Key
- Mount point
- Kv version

![Nautobot Hashicorp Secret Parameters](..//images/2023/nautobot_vault_parameters.png)

### Nautobot Parameters: Vault Mount Point

So the vault that I have set up inside of Vault, is a KV store. In the image there is the `cubbyhole` which is used for local passwords, so I wouldn't use that for my vaults. The name of `kv` below will be the first item into the Nautobot secret and will map to the `Mount point` with Nautobot. The default is `secret`, and this needs to change to `kv` if that is what you have.

![Vault Overview](..//images/2023/vault_overview.png)

### Nautobot Parameters: Vault Path

Next down the folder path on Hashicorp Vault is the folder/path. When you navigate into the kv link you then get the next item of the path, in this case `net_device`. This is the `Path` within the parameters form.

![Vault Path](..//images/2023/vault_net_device.png)

### Nautobot Parameters: Key

The last part you need within your Nautobot secret is the Key itself. So in the secret within Vault, you have various keys. These line up with the `key` within the parameters of the Nautobot secret.

![Vault Keys](..//images/2023/vault_net_device_overview.png)

{{< alert "neutral" >}}
It's worth noting that each key in the vault secret is its own entity. That being that you will need to set up a Nautobot Secrets Group to pair the username and password together. **You need to set up a secret for both a username and password** if you are having a username/password combination that is often the case.


{{< /alert >}}
### Testing the Secret

One of my favorite features of the Nautobot Secrets Provider is that there is the opportunity to "test" the secrets gathering. Once the secret is created you can find the `Check Secret` button in the upper right.

![Test Button](..//images/2023/nautobot_secrets_check.png)

When you click that button and all is well you get the successful message back.

![Test Success](..//images/2023/nautobot_secrets_check_successful.png)

## Alignment Table

Here is what the Nautobot terminology lined up:

| Nautobot Parameter | Hashicorp Vault                                                  |
| ------------------ | ---------------------------------------------------------------- |
| Path               | Folders inside of the KV store, including the secret name itself |
| Key                | Key within the secret                                            |
| Mount point        | Name of the KV store                                             |
| Kv version         | Version of the Key/Value store                                   |

## Summary

Nautobot is handling secrets right in my opinion. That secrets are not to be stored within Nautobot. These are things that there are great solutions already available for. Use those tools. Nautobot provides a good mechanism to be able to integrate with various secrets providers. This hopefully helps out someone get started with using Hashicorp Vault secrets and Nautobot. I know I will be using this post again in the future some day!

Let me know on social media (until I get a comment system built in) what your thoughts are. 

Josh