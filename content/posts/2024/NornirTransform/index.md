---
date: 2024-06-04
slug: nornir-transform-3
categories:
- automation
- nornir
- python
- vault
title: Nornir Transform Function
toc: true
author: jvanderaa
params:
  showComments: true
---

Nornir includes a function that allows for the transformation of inventory data, a feature integrated within the Nornir platform itself. The documentation for Nornir 3.0 is somewhat sparse regarding the usage of Transform functions, so I often refer to the more comprehensive [2.5 documentation](https://nornir.readthedocs.io/en/v2.5.0/howto/transforming_inventory_data.html#Modifying-hosts'-data). According to the Nornir documentation:

> A transform function is a plugin that manipulates the inventory independently from the inventory plugin used. Useful to extend data using the environment, a secret store or similar.

<!--more-->

I'm going to highlight the aspect of extending data, particularly through a `secret store` but using Environment Variables in the example. This approach is essential for using Nornir applications effectively, as it leverages a secret store to gather sensitive information. While applications like Nautobot provide data about the devices themselves, they are not designed to handle cryptographic secrets.

## Getting Started - Environment Variables

One of the first method we will explore is adding data such as a network device username from the environment. This way you do not need anything other than a command line (Linux/Mac is covered here) to the shell, which is exactly where many run their Nornir applications from. If you would like more on setting environment variables, check out the [Twilio blog post](https://www.twilio.com/en-us/blog/how-to-set-environment-variables-html) that dives in more.

{{< alert "neutral" >}}
**Use Existing In Nornir Utils If Looking For Environment Variables**

Added 2024-06-06:  
The use of environment variables in this case is meant to show as an example. The [nornir-utils](https://github.com/nornir-automation/nornir_utils) project has a more production ready version of this same thing. Look to use that if using Environment variables - https://github.com/nornir-automation/nornir_utils/blob/master/nornir_utils/plugins/inventory/transform_functions.py. You should look to use a secrets management system if you have one available.

{{< /alert >}}
{{< alert "neutral" >}}
**Python packaging environment**

For this post I will be using Python Poetry to handle the packaging within the demo. Python Poetry is the environment that I'm most familiar with on using for package management at this time.

{{< /alert >}}
We will first set the environment variables that will be needed for the Nornir script.

```bash {title="Set Nautobot environment variables"}
export NAUTOBOT_URL="https://demo.nautobot.com"  
export NAUTOBOT_TOKEN="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
```

> [!INFO]- Follow Along or Set Your Own
> With the envrionment variables set above, you will be able to follow along at home  as long as the devices haven't been modified on the demo instance. It is a demo instance after all. If you wish to use your own Nautobot instance, just set the `NAUTOBOT_URL` and `NAUTOBOT_TOKEN` above appropriately.
>
Now that all of the environment variables are set for the Nautobot environment, we can look at the slightly modified Nornir Inventory example with the Demo Nautobot instance.

> [!NOTE]- Python Dependencies
> The following Python dependencies will be required to run these examples:
>
> ```bash
> [tool.poetry.dependencies]
> python = "^3.9"
> nornir = "^3.4.1"
> nornir-nautobot = "^3.2.0"
> ```
>
> ```bash title="requirements.txt"
> nornir-nautobot==3.2.0 ; python_version >= "3.9" and python_version < "4.0"
> nornir==3.4.1 ; python_version >= "3.9" and python_version < "4.0"
> ```
>
```python {linenos=true, title="explore-nornir-transform.py"}
"""Testing file."""
import os
import urllib3

from nornir import InitNornir

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    """Nornir testing."""
    location = ["ORD01"]

    my_nornir = InitNornir(
        inventory={
            "plugin": "NautobotInventory",
            "options": {
                "nautobot_url": os.getenv("NAUTOBOT_URL"),
                "nautobot_token": os.getenv("NAUTBOT_TOKEN"),
                "filter_parameters": {"location": location},
                "ssl_verify": False,
            },
        },
    )

    print(f"Hosts found: {len(my_nornir.inventory.hosts)}")
    
    # Print out the keys for the inventory
    print(my_nornir.inventory.hosts.keys())

if __name__ == "__main__":
    main()
```

When you run this script you will get the following output showing the length of the devices and the key list (as defined on line 43).

```bash {title="Set Environment Variables for Network Devices"}
export NET_USERNAME="my_username"
export NET_PASSWORD="my_password"
```

This just set the environment variables of `NET_USERNAME` and `NET_PASSWORD`. You can confirm this by executing:

```bash {title="Verify environment variables are set"}
env | grep NET_
```

Which will provide the output:

```bash {title="Output of env | grep NET_"}
❯ env | grep NET_
NET_USERNAME=my_username
NET_PASSWORD=my_password
```

{{< alert "neutral" >}}
**Environment File Option**

I did previously did a blog post at https://josh-v.com/nautobot-environment-file/ that went into defining environment files and how you would load the data into the environment.

{{< /alert >}}
## Transform Function - Get Username

<div class="annotate" markdown>
Now that there are usernames and passwords in the environment, let's look at how to add those to your Nornir inventory via the transform function. The first part is defining the transform function. Here I will add a function within the same Python file (1) defined outside of the `main()` function.
</div>

1. You may want to look at putting all of the transform functions in a separate file as you get going.

```py
def update_credentials(host: Host):
    """Update the credentials for the host.
    
    Args:
        host (Host): The host object to update.
    """
    host.username = os.getenv("NET_USERNAME")
    host.password = os.getenv("NET_PASSWORD")
```

The function is more lines of documentation than the code itself. Assigning `host.username` to the environment variable for `NET_USERNAME` and `host.password` to the environment variable for `NET_PASSWORD`. You may want to put a little more logic somewhere to make sure that these are defined, since the `os.getenv()` method returns `None` if it is not found.

### Update Pyproject.toml

The second step in this process is to add a section in the `pyproject.toml` file. This will be needed to help register the function to Nornir. Lines 13 & 14 are what are required for the Nornir plugin registration.

```toml {linenos=true, hl_lines=["13-14"], title="pyproject.toml"}
[tool.poetry]
name = "sandbox-python"
version = "0.1.0"
description = ""
authors = ["Josh VanDeraa <>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.9"
nornir = "^3.4.1"
nornir-nautobot = "^3.2.0"

[tool.poetry.plugins."nornir.plugins.transform_function"]
"update_credentials" = "explore-nornir-transformation:update_credentials"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

```

Let's take a look at the two parts on the right side of the assignment on line 14, with the string of `explore-nornir-transformation:update_credentials`. In the middle is the colon `:` that separates the two. The first half is the path to get to the function, with the second half of the string representing the function name that is in the file. So you can nest it using dotted `.` notation.

### Registering The Function

The last step is to register the transform function. That is completed by adding the line below into the script/application. This just needs to be executed before `InitNornir()`. See line 21 in the completed demo application.

```py
TransformFunctionRegister.register("update_credentials", update_credentials)
```

### Completed Python File

Here is the completed demo file:

```py {linenos=true, hl_lines=["21"], title="explore-nornir-transform.py"}
"""Testing file."""
import os
import urllib3

from nornir import InitNornir
from nornir.core.inventory import Host
from nornir.core.plugins.inventory import TransformFunctionRegister

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def update_credentials(host: Host):
    """Update the credentials for the host.
    
    Args:
        host (Host): The host object to update.
    """
    host.username = os.getenv("NET_USERNAME")
    host.password = os.getenv("NET_PASSWORD")

TransformFunctionRegister.register("update_credentials", update_credentials)

def main():
    """Nornir testing."""
    location = ["ORD01"]

    my_nornir = InitNornir(
        inventory={
            "plugin": "NautobotInventory",
            "options": {
                "nautobot_url": os.getenv("NAUTOBOT_URL"),
                "nautobot_token": os.getenv("NAUTBOT_TOKEN"),
                "filter_parameters": {"location": location},
                "ssl_verify": False,
            },
            "transform_function": "update_credentials",
        },
    )

    print(f"Hosts found: {len(my_nornir.inventory.hosts)}")

    # Print out the keys for the inventory
    print(my_nornir.inventory.hosts.keys())
    host1 = my_nornir.inventory.hosts['ord01-dist-01']
    print(host1.username)
    print(host1.password)

if __name__ == "__main__":
    main()

```

When this executes you get the following output:

```bash {linenos=true, title="explore-nornir-transform.py output"}
Hosts found: 27
dict_keys(['ord01-dist-01', 'ord01-edge-01', 'ord01-edge-02', 'ord01-leaf-01', 'ord01-leaf-02', 'ord01-leaf-03', 'ord01-leaf-04', 'ord01-leaf-05', 'ord01-leaf-06', 'ord01-leaf-07', 'ord01-leaf-08', 'ord01-pdu-01', 'ord01-pdu-02', 'ord01-pdu-03', 'ord01-pdu-04', 'ord01-pdu-05', 'ord01-pdu-06', 'ord01-pdu-07', 'ord01-pdu-08', 'ord01-pdu-11', 'ord01-pdu-12', 'ord01-pdu-13', 'ord01-pdu-14', 'ord01-pdu-15', 'ord01-pdu-16', 'ord01-pdu-17', 'ord01-pdu-18'])
my_username
my_password
```

Lines 3 & 4 are the print out of the username and password. This is demonstration of setting these values via transform functions and you probably should not be actually printing passwords 🔒.

## Summary

Using the Transform Function in Nornir is the recommended method for adding credentials to a Nornir script or application. This approach ensures that your secrets are managed separately from your inventory, enhancing security. By incorporating logic to integrate with a secrets vault, such as Hashicorp Vault, within the environment variable loading function, you can securely obtain the necessary credentials to connect to your devices. This method keeps your sensitive information protected while maintaining the flexibility and functionality of your Nornir applications.

> [!INFO]- Don't Have a Secrets Management?
> If you do not have a secrets management system that is programmatically available, I recommend using Hashicorp Vault. You can read more about that in my book [Open Source Network Management](https://josh-v.com/book/) for setting up Vault in Docker environment (amongst other open source tools).