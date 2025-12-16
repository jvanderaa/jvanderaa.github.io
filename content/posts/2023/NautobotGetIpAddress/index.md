---
date: 2023-07-07
slug: nautobot-get-ip-address-info
categories:
- automation
- nautobot
- golang
- python
- ansible
title: 'Nautobot: Get IP Addresses From Nautobot'
toc: true
author: jvanderaa
params:
  showComments: true
---

One of Nautobot's primary functions is to serve as an IPAM solution. Within that realm, the application needs to provide a method to get at IP address data for a device, quickly and easily. In this post I will review three prominent methods to get an IP address from Nautobot. It will demonstrate getting the address via:

- Nautobot REST API
  - curl
  - Python Requests
  - GoLang HTTP
  - pynautobot
  - Ansible Lookup
- Nautobot GraphQL API
  - curl
  - Python Requests
  - GoLang HTTP
  - pynautobot
  - Ansible Lookup

<!--more-->

Each method I will demonstrate how to get the IP address for Loopback0 on the [device](https://demo.nautobot.com/dcim/devices/5e7c0bdd-254b-44cb-bf7c-2f2560082f6d/?tab=main) `bre01-edge-01` within the demo instance of Nautobot. This device has 62 interfaces, so being able to filter down to which interface IP address we are looking for makes sense.

## Getting an IP Address From The API

For this set up, the environment variables of `NAUTOBOT_URL` and `NAUTOBOT_TOKEN` will be used. Set those with

```plaintext
export NAUTOBOT_URL=https://demo.nautobot.com
export NAUTOBOT_TOKEN=secretTokenHere
```

### curl

The first straight forward method is going to be using the curl application to accomplish the goal.

```bash {linenos=true}
curl -X "GET" \
  "$NAUTOBOT_URL/api/ipam/ip-addresses/?device=bre01-edge-01&interface=Loopback0" \
  -H "accept: application/json" \
  -H "Authorization: Token $NAUTOBOT_TOKEN"

```

> This requires the quotes to be double quotes. Bash and shell prompts will not expand it if it is single quotes.

This is the full API response that is provided then:

```json {linenos=true}
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "77371932-3b7f-4e94-9179-d1d4290695d9",
      "display": "10.30.128.1/32",
      "url": "https://demo.nautobot.com/api/ipam/ip-addresses/77371932-3b7f-4e94-9179-d1d4290695d9/",
      "family": {
        "value": 4,
        "label": "IPv4"
      },
      "address": "10.30.128.1/32",
      "vrf": null,
      "tenant": {
        "display": "Nautobot Baseball Stadiums",
        "id": "a39f2dd8-84c8-4816-9e6f-4a7c46e91a77",
        "url": "https://demo.nautobot.com/api/tenancy/tenants/a39f2dd8-84c8-4816-9e6f-4a7c46e91a77/",
        "name": "Nautobot Baseball Stadiums",
        "slug": "nautobot-baseball-stadiums"
      },
      "status": {
        "value": "active",
        "label": "Active"
      },
      "role": null,
      "assigned_object_type": "dcim.interface",
      "assigned_object_id": "6ecee964-e4e0-4a0a-83b7-b7485633fc78",
      "assigned_object": {
        "display": "Loopback0",
        "id": "6ecee964-e4e0-4a0a-83b7-b7485633fc78",
        "url": "https://demo.nautobot.com/api/dcim/interfaces/6ecee964-e4e0-4a0a-83b7-b7485633fc78/",
        "device": {
          "display": "bre01-edge-01",
          "id": "5e7c0bdd-254b-44cb-bf7c-2f2560082f6d",
          "url": "https://demo.nautobot.com/api/dcim/devices/5e7c0bdd-254b-44cb-bf7c-2f2560082f6d/",
          "name": "bre01-edge-01"
        },
        "name": "Loopback0",
        "cable": null
      },
      "nat_inside": null,
      "nat_outside": null,
      "dns_name": "edge-01.bre01.mlb.nautobot.com",
      "description": "",
      "created": "2022-11-09",
      "last_updated": "2022-11-09T15:11:51.606550Z",
      "tags": [],
      "notes_url": "https://demo.nautobot.com/api/ipam/ip-addresses/77371932-3b7f-4e94-9179-d1d4290695d9/notes/",
      "custom_fields": {}
    }
  ]
}
```

### Python Requests

```python {linenos=true}
from requests import Session
import json
import os

url = f"{os.getenv('NAUTOBOT_URL')}/api/ipam/ip-addresses/?device=bre01-edge-01&interface=Loopback0"

session = Session()
session.headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {os.getenv('NAUTOBOT_TOKEN')}",
}

response = session.get(url)
ip_address = response.json()["results"][0]["address"]

print(ip_address)

```

In this example I've used the requests Session method to store the headers instead of passing it in with requests.get(). They both work, but it is good habit to utilize a session when applicable and especially when making multiple API calls. The output is:

```bash
❯ python get_ip_address.py
10.30.128.1/32
```

### GoLang HTTP

```go {linenos=true}
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

type IPAddress struct {
	Address string `json:"address"`
}

type Response struct {
	Results []IPAddress `json:"results"`
}

func main() {
	nautobotBase := os.Getenv("NAUTOBOT_URL")
	nautobotToken := os.Getenv("NAUTOBOT_TOKEN")
	url := fmt.Sprintf("%s/api/ipam/ip-addresses/?device=bre01-edge-01&interface=Loopback0", nautobotBase)
	method := "GET"

	payload := strings.NewReader(``)

	client := &http.Client{}
	req, err := http.NewRequest(method, url, payload)

	if err != nil {
		fmt.Println(err)
		return
	}
	tokenString := fmt.Sprintf("Token %s", nautobotToken)
	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("Authorization", tokenString)

	res, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer res.Body.Close()

	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		fmt.Println(err)
		return
	}

	// Parse the JSON response
	var response Response
	err = json.Unmarshal(body, &response)
	if err != nil {
		fmt.Println(err)
		return
	}

	// Print the desired value
	if len(response.Results) > 0 {
		fmt.Println("IP Address:", response.Results[0].Address)
	} else {
		fmt.Println("No IP addresses found.")
	}
}

```

This provides the same output as seen in the Python version:

```bash
❯ go run get_ip.go
IP Address: 10.30.128.1/32
```

### pynautobot

The Python SDK that works to turn the Nautobot API into a Python object you can get the IP address data with the code below. Pynautobot examples are falling under the REST API section at the moment as that is where it fits the best.

```python {linenos=true}
import os
import pynautobot

nautobot = pynautobot.api(url=os.getenv("NAUTOBOT_URL"), token=os.getenv("NAUTOBOT_TOKEN"))
ip_address = nautobot.ipam.ip_addresses.get(interface="Loopback0", device="bre01-edge-01")
print(ip_address)

```

The execution:

```bash {linenos=true}
❯ python get_ip_address_sdk.py
10.30.128.1/32
```

### REST API - Ansible

With Ansible, there are two methods available to use. You can use the native URI module that will gather data from the API endpoint. This example is with the Nautobot Ansible collection lookup plugin, which uses pynautobot under the hood. This allows for a little easier methodology of gathering data.

```yaml {linenos=true}
---
- name: "GET IP ADDRESS FROM NAUTOBOT"
  hosts: localhost
  connection: local
  gather_facts: no
  vars:
    nautobot_url: "{{ lookup('ansible.builtin.env', 'NAUTOBOT_URL') }}"
    nautobot_token: "{{ lookup('ansible.builtin.env', 'NAUTOBOT_TOKEN') }}"
  tasks:
    - name: "10: GET IP ADDRESS FROM NAUTOBOT"
      set_fact:
        ip_address: "{{ lookup('networktocode.nautobot.lookup',
          'ip-addresses',
          api_endpoint=nautobot_url,
          token=nautobot_token,
          api_filter='device=bre01-edge-01 interface=Loopback0') }}"

    - debug:
        msg: "{{ ip_address['value']['address'] }}"
```

Which gives the following output.

```json
PLAYBOOK: get_ip.yml ***********************************************************************************************************************
1 plays in get_ip.yml

PLAY [GET IP ADDRESS FROM NAUTOBOT] ********************************************************************************************************
META: ran handlers

TASK [10: GET IP ADDRESS FROM NAUTOBOT] ****************************************************************************************************
task path: /home/joshv/projects/sandbox-ansible/get_ip.yml:10
ok: [localhost] => {
    "ansible_facts": {
        "ip_address": {
            "key": "77371932-3b7f-4e94-9179-d1d4290695d9",
            "value": {
                "address": "10.30.128.1/32",
                "assigned_object": {
                    "cable": null,
                    "device": {
                        "display": "bre01-edge-01",
                        "id": "5e7c0bdd-254b-44cb-bf7c-2f2560082f6d",
                        "name": "bre01-edge-01",
                        "url": "https://demo.nautobot.com/api/dcim/devices/5e7c0bdd-254b-44cb-bf7c-2f2560082f6d/"
                    },
                    "display": "Loopback0",
                    "id": "6ecee964-e4e0-4a0a-83b7-b7485633fc78",
                    "name": "Loopback0",
                    "url": "https://demo.nautobot.com/api/dcim/interfaces/6ecee964-e4e0-4a0a-83b7-b7485633fc78/"
                },
                "assigned_object_id": "6ecee964-e4e0-4a0a-83b7-b7485633fc78",
                "assigned_object_type": "dcim.interface",
                "created": "2022-11-09",
                "custom_fields": {},
                "description": "",
                "display": "10.30.128.1/32",
                "dns_name": "edge-01.bre01.mlb.nautobot.com",
                "family": {
                    "label": "IPv4",
                    "value": 4
                },
                "id": "77371932-3b7f-4e94-9179-d1d4290695d9",
                "last_updated": "2022-11-09T15:11:51.606550Z",
                "nat_inside": null,
                "nat_outside": null,
                "notes_url": "https://demo.nautobot.com/api/ipam/ip-addresses/77371932-3b7f-4e94-9179-d1d4290695d9/notes/",
                "role": null,
                "status": {
                    "label": "Active",
                    "value": "active"
                },
                "tags": [],
                "tenant": {
                    "display": "Nautobot Baseball Stadiums",
                    "id": "a39f2dd8-84c8-4816-9e6f-4a7c46e91a77",
                    "name": "Nautobot Baseball Stadiums",
                    "slug": "nautobot-baseball-stadiums",
                    "url": "https://demo.nautobot.com/api/tenancy/tenants/a39f2dd8-84c8-4816-9e6f-4a7c46e91a77/"
                },
                "url": "https://demo.nautobot.com/api/ipam/ip-addresses/77371932-3b7f-4e94-9179-d1d4290695d9/",
                "vrf": null
            }
        }
    },
    "changed": false
}

TASK [debug] *******************************************************************************************************************************
task path: /home/joshv/projects/sandbox-ansible/get_ip.yml:18
ok: [localhost] => {
    "msg": "10.30.128.1/32"
}
META: ran handlers
META: ran handlers

PLAY RECAP *********************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

## GraphQL

The second methodology, which is the preferred method to get data from Nautobot, as it provides the data you are looking for only, it doesn't get all of the additional data that comes with the REST API calls. The best methodology for discovering the GraphQL query is by using the iQL interface. This is by selecting `GraphQL` icon on the bottom right of the Nautobot instance.

The query that is going to be used here:

```plaintext {linenos=true}
query {
  ip_addresses(device:"bre01-edge-01", interface: "Loopback0") {
    address
  }
}
```

On line 2 the query is indicating to search ip_addresses from Nautobot. Then to filter on the device by name and the interface by interface name. You can turn these into variables as well within the GraphQL standards. The returned response is:

```json
{
    "data": {
        "ip_addresses": [
            {
                "address": "10.30.128.1/32"
            }
        ]
    }
}
```

Let's take a look at how this is then accomplished with the various methods.

### GraphQL - Curl

```bash
curl --location "$NAUTOBOT_URL/api/graphql/" \
--header "Content-Type: application/json" \
--header "Authorization: Token $NAUTOBOT_TOKEN" \
--data '{"query":"query {\n  ip_addresses(device:\"bre01-edge-01\", interface: \"Loopback0\") {\n    address\n  }\n}\n","variables":{}}'
```

The response is back as expected, just in the printed format.

### Python Requests

```python {linenos=true}
from requests import Session
import json
import os

url = "https://demo.nautobot.com/api/graphql/"

session = Session()
session.headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {os.getenv('NAUTOBOT_TOKEN')}",
}
payload = {
    "query": """
query {
  ip_addresses(device:"bre01-edge-01", interface: "Loopback0") {
    address
  }
}
"""
}

response = session.post(url, json=payload)
ip_address = response.json()["data"]["ip_addresses"][0]["address"]

print(ip_address)

```

The structure returned by GraphQL is a little bit different than the REST API, but nothing that we can't work through as seen on line 23.

### GoLang

```go {linenos=true}
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

type IPAddressResponse struct {
	Data struct {
		IPAddresses []struct {
			Address string `json:"address"`
		} `json:"ip_addresses"`
	} `json:"data"`
}

// Define a struct to represent the GraphQL query and its variables
type GraphQLRequest struct {
	Query     string   `json:"query"`
	Variables struct{} `json:"variables"`
}

func main() {
	nautobotUrl := os.Getenv("NAUTOBOT_URL")
	nautobotToken := os.Getenv("NAUTOBOT_TOKEN")
	url := fmt.Sprintf("%s/api/graphql/", nautobotUrl)
	method := "POST"

	// Create a GraphQLRequest object with the query and an empty variables object
	graphQLRequest := GraphQLRequest{
		Query: `query {
			ip_addresses(device:"bre01-edge-01", interface: "Loopback0") {
				address
			}
		}`,
		Variables: struct{}{},
	}

	// Serialize the GraphQLRequest object to JSON
	jsonData, err := json.Marshal(graphQLRequest)
	if err != nil {
		fmt.Println("Error marshaling JSON:", err)
		return
	}
	payload := strings.NewReader(string(jsonData))

	client := &http.Client{}
	req, err := http.NewRequest(method, url, payload)

	if err != nil {
		fmt.Println(err)
		return
	}
	req.Header.Add("Content-Type", "application/json")
	req.Header.Add("Authorization", fmt.Sprintf("Token %s", nautobotToken))

	res, err := client.Do(req)
	if err != nil {
		fmt.Println(err)
		return
	}
	defer res.Body.Close()

	body, err := ioutil.ReadAll(res.Body)
	if err != nil {
		fmt.Println(err)
		return
	}
	// Parse the response JSON
	var ipResponse IPAddressResponse
	err = json.Unmarshal(body, &ipResponse)
	if err != nil {
		fmt.Println("Error parsing response JSON:", err)
		return
	}

	// Access the IP address from the response
	ipAddresses := ipResponse.Data.IPAddresses
	if len(ipAddresses) > 0 {
		ipAddress := ipAddresses[0].Address
		fmt.Println("IP Address:", ipAddress)
	} else {
		fmt.Println("No IP address found.")
	}
}

```

### pynautobot

Pynautobot also provides a helper method to be able to make GraphQL queries as well. It returns a JSON object at `.json` and can be accessed as a dictionary:

```python {linenos=true}
import os
import pynautobot

query_str = """
query {
  ip_addresses(device:"bre01-edge-01", interface: "Loopback0") {
    address
  }
}"""

nautobot = pynautobot.api(url=os.getenv("NAUTOBOT_URL"), token=os.getenv("NAUTOBOT_TOKEN"))
print(nautobot.graphql.query(query=query_str).json["data"]["ip_addresses"][0]["address"])

```

### GraphQL: Ansible

A slight modification to the Ansible playbook, adding a variable at the top for the query string, and using the action module to query instead of a lookup plugin.

```yaml {linenos=true}
---
- name: "GET IP ADDRESS FROM NAUTOBOT"
  hosts: localhost
  connection: local
  gather_facts: no
  vars:
    nautobot_url: "{{ lookup('ansible.builtin.env', 'NAUTOBOT_URL') }}"
    nautobot_token: "{{ lookup('ansible.builtin.env', 'NAUTOBOT_TOKEN') }}"
    query_str: |
      query {
        ip_addresses(device:"bre01-edge-01", interface: "Loopback0") {
          address
        }
      }

  tasks:
    - name: "10: GET IP ADDRESS FROM NAUTOBOT"
      networktocode.nautobot.query_graphql:
        url: "{{ nautobot_url }}"
        token: "{{ nautobot_token }}"
        query: "{{ query_str }}"
      register: "query_response"

    - debug:
        msg: "{{ query_response['data']['ip_addresses'][0]['address'] }}"

```

With the expected result as seen:

```
PLAY [GET IP ADDRESS FROM NAUTOBOT] ********************************************************************************************************

TASK [10: GET IP ADDRESS FROM NAUTOBOT] ****************************************************************************************************
ok: [localhost]

TASK [debug] *******************************************************************************************************************************
ok: [localhost] => {
    "msg": "10.30.128.1/32"
}

PLAY RECAP *********************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

## Summary

There are several ways that you can get IP addresses out of Nautobot. With having the robust API capabilities that Nautobot has, including the GraphQL endpoints, you are able to work quite quickly to get at the data that you need to automate your network, automate your enterprise. Whether it is working with some programming languages, or working with an automation engine such as Ansible, Nautobot is available to help out!