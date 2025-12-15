---
date: 2022-12-17
slug: graphql-aliasing
categories:
- automation
- python
- graphql
- nautobot
- meraki
title: GraphQL - Aliasing
toc: true
author: jvanderaa
params:
  showComments: true
---

One of the features that I find myself using periodically that I think is underrated as far as using GraphQL is its ability to alias return keys in the response. This can be extremely helpful for developers writing applications, as it allows them to have the API response with the keys they are looking for. I have found this feature particularly useful when working on applications like Meraki and Nautobot together. In Nautobot a place is typically defined as the key `site`. In the Meraki world this is commonly set up as a `network`. Without GraphQL's alias feature, the developer would need to translate this data over.

Let's explore two scenarios where a developer might choose to alias the response from GraphQL:

- Quick translation between systems
- Response from multiple queries

I will demonstrate the capabilities of these scenarios using the Nautobot demo instance at https://demo.nautobot.com. For each of these, make sure that you have logged in already before going to the GraphiQL page.

<!--more-->

## Base GraphQL Query

The base GraphQL query will be:

```graphql
query {
  devices(name__ic: "den") {
    name
    site {
      name
    }
  }
}
```

> Note that I am filtering down to a smaller subset of the devices within Nautobot for brevity.

With the filter in place looking for devices that include `bre` in the name you get the response of:

```json
{
  "data": {
    "devices": [
      {
        "name": "den01-dist-01",
        "site": {
          "name": "DEN01"
        }
      },
      {
        "name": "den01-edge-01",
        "site": {
          "name": "DEN01"
        }
      },
      {
        "name": "den01-edge-02",
        "site": {
          "name": "DEN01"
        }
      },
      {
        "name": "den01-leaf-01",
        "site": {
          "name": "DEN01"
        }
      },
      {
        "name": "den01-leaf-02",
        "site": {
          "name": "DEN01"
        }
      },
      {
        "name": "den01-leaf-03",
        "site": {
          "name": "DEN01"
        }
      },
      {
        "name": "den01-leaf-04",
        "site": {
          "name": "DEN01"
        }
      },
      {
        "name": "den01-leaf-05",
        "site": {
          "name": "DEN01"
        }
      },
      {
        "name": "den01-leaf-06",
        "site": {
          "name": "DEN01"
        }
      },
      {
        "name": "den01-leaf-07",
        "site": {
          "name": "DEN01"
        }
      },
      {
        "name": "den01-leaf-08",
        "site": {
          "name": "DEN01"
        }
      }
    ]
  }
}
```

First of all, it's pretty awesome to get just the data that you're looking for. This is by far one of the best features of GraphQL. Use it whenever you are getting data from a system that offers GraphQL.

## GraphQL - Alias

Now with the request in place, let's go down the path of changing the response where ever the key of `site` is found that GraphQL will instead send the key `network`. This will align more with the data format that Meraki is looking for within their API.

The alias is done by having instead of just `site` on line 4 of the query, but to add the new key name in front of a colon. Such as line 4 of the query will now be `network: site {`.

```graphql
query {
  devices(name__ic: "bre") {
    name
    network: site {
      name
    }
  }
}
```

And the response you notice you no longer see `site:` any where in the response.

```json
{
  "data": {
    "devices": [
      {
        "name": "bre01-dist-01",
        "network": {
          "name": "BRE01"
        }
      },
      {
        "name": "bre01-edge-01",
        "network": {
          "name": "BRE01"
        }
      },
      {
        "name": "bre01-edge-02",
        "network": {
          "name": "BRE01"
        }
      },
      {
        "name": "bre01-leaf-01",
        "network": {
          "name": "BRE01"
        }
      },
      {
        "name": "bre01-leaf-02",
        "network": {
          "name": "BRE01"
        }
      },
      {
        "name": "bre01-leaf-03",
        "network": {
          "name": "BRE01"
        }
      },
      {
        "name": "bre01-leaf-04",
        "network": {
          "name": "BRE01"
        }
      }
    ]
  }
}
```

## GraphQL - Multiple Queries

A second case, which is from the [GraphQL learning page](https://graphql.org/learn/queries/#aliases) is where you have multiple queries to the same part of the API. This is where you would then need to alias the response in order to make the GraphQL query to be valid.

### Multiple Search Query - Error

First let's look at what a bad query looks like from GraphQL that will generate an error. Let's say you want to get data about two sites from Nautobot. A query that would get you the data looks like:

```graphql
query {
  sites(name: "ORD01") {
    facility
  }
  sites(name: "DEN01") {
    facility
  }
}
```

Running that query generates the following error message:

```no-highlight
"message": "Fields \"sites\" conflict because they have differing arguments. Use different aliases on the fields to fetch both if this was intentional.",
```

### Multiple Search Query - Successful

The workaround is to alias the response. Such that instead of sites being sent back, we can use the site name with an incrementing counter number on the end. This may be something where you build a query offline in Python where you keep appending to a string, and in the end send over a large query with aliased keys.

The new query looks like this:

```graphql
query {
  site1: sites(name: "ORD01") {
    facility
  }
  site2: sites(name: "DEN01") {
    facility
  }
}
```

There are now new site keys at the beginning. The response now gives you the data that you would expect:

```json
{
  "data": {
    "site1": [
      {
        "facility": "O'Hare International Airport"
      }
    ],
    "site2": [
      {
        "facility": "Denver International Airport"
      }
    ]
  }
}
```

## Using in Python

Taking the first example to Python, let's take a look at how you can then access the aliased response. The pynautobot package takes the response and has a convenience attribute of `.json` that will get the data into a Python dictionary for use. This will loop over each of the devices in the response and print the corresponding network (which will all be the same):

```python
import json

import click
import pynautobot


@click.command
@click.option("--nautobot_url", envvar="NAUTOBOT_URL")
@click.option("--nautobot_token", envvar="NAUTOBOT_TOKEN")
def main(nautobot_url, nautobot_token):
    nautobot = pynautobot.api(url=nautobot_url, token=nautobot_token)

    query = """
query {
  devices(name__ic: "den") {
    name
    network: site {
      name
    }
  }
}
    """

    graphql_response = nautobot.graphql.query(query=query)
    response = graphql_response.json
    for device in response["data"]["devices"]:
        print(device["network"])


if __name__ == "__main__":
    main()

```

Running that code with setting the appropriate environment variables of `NAUTOBOT_URL` and `NAUTOBOT_TOKEN` gets you this response:

```
❯ python graphql_aliasing.py
{'name': 'DEN01'}
{'name': 'DEN01'}
{'name': 'DEN01'}
{'name': 'DEN01'}
{'name': 'DEN01'}
{'name': 'DEN01'}
{'name': 'DEN01'}
{'name': 'DEN01'}
{'name': 'DEN01'}
{'name': 'DEN01'}
{'name': 'DEN01'}
```

## Summary

In summary, when you are able to use GraphQL to get data and the response may not be exactly the format you are looking for, take a look at using a GraphQL alias to get your response. This will come in super helpful over time. I'd love to hear what your thoughts are on this and where you are using it!

Happy Automating!
