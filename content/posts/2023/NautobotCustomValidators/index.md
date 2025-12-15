---
date: 2023-07-05
slug: nautobot-remote-validation
categories:
- automation
- nautobot
- security
- devnet
- flask
title: Nautobot Remote Validation
toc: true
author: jvanderaa
params:
  showComments: true
---

In this post I'm going to dive into a bit more on the Nautobot custom validators. This is a powerful validation tool that will allow for you to write your own validation capability, including in this demonstration on how to complete a validation against a remote API endpoint. The custom validators are a part of the Nautobot App extension capability. This allows for custom code to be written to validate data upon the `clean()` method being called, which is used in the majority of API calls and form inputs of Nautobot.

<!--more-->

I will look to accomplish four different objectives in this post from my point of view. This will help to get some targeted experiences with what I believe the DevNet Expert exam has in mind for Web Services, working with Flask. In my day to day I deal more so within the Django Web Framework to build web applications that are part of the Nautobot ecosystem. So the need to write some Flask applications is a good way to branch out some.

The goals that I have for this post:

- Creating a Web Services endpoint using Flask
  - Creating multiple endpoints for validation
  - Process the HTTP Request
  - Provide a response
- Provide additional details around the Nautobot custom validation engine

## Nautobot Custom Validators

The Nautobot extensibility features are quite awesome. It is what makes Nautobot a platform worth investing in. The [Nautobot Custom Validators](https://docs.nautobot.com/projects/core/en/stable/plugins/development/#implementing-custom-validators) is no exception here. The example from the link previous is that a validator may set the requirement that every site must have a region:

```python linenums="1"
# custom_validators.py
from nautobot.apps.models import CustomValidator


class SiteValidator(CustomValidator):
    """Custom validator for Sites to enforce that they must have a Region."""

    model = 'dcim.site'

    def clean(self):
        if self.context['object'].region is None:
            # Enforce that all sites must be assigned to a region
            self.validation_error({
                "region": "All sites must be assigned to a region"
            })


custom_validators = [SiteValidator]
```

More information about the details of this can be found on the link provided, including the most up to date information on writing custom validators.

## Flask App

First the Flask application. In this instance, I am using the Flask extension Flask-RESTX to help in handling a REST API endpoint that I plan on extending in future iterations. After installing Flask and Flask-RESTX into a new Poetry virtual environment I built the following API endpoint that will check that the hostname is all lower case:

```python linenums="1"
from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)


@api.route("/validate_name/")
class HelloWorld(Resource):
    def post(self):
        """Handles POST request.

        Data comes in via api.payload object that can be interacted upon. This is a type dictionary.
        """
        # Get the data that is coming in, expecting the key of proposed_device_name
        proposed_device_name = api.payload.get("proposed_name")
        print(proposed_device_name)
        print(api.payload)

        if proposed_device_name is None:
            return {
                "valid": False,
                "details": "Proposed Name was not sent appropriately",
            }, 422

        # Verify the case
        if proposed_device_name != proposed_device_name.lower():
            return {
                "valid": False,
                "details": f"{proposed_device_name} is not all lower case.",
            }, 201

        return {
            "valid": True,
            "details": f"{proposed_device_name} passes validation",
        }, 201


if __name__ == "__main__":
    app.run(debug=True)

```

{{< alert "neutral" >}}
Lines 17 & 18 are just the debugging code that will print out to the console the details to help understand what is coming in.


{{< /alert >}}
### Testing Flask Endpoints (Manual)

Some manual tests of the Flask endpoint to verify that the data is working as expected get the following results.

#### Good Test

```bash linenums="1"
curl localhost:5000/validate_name/ -d '{"proposed_name":"goodname"}' -X POST -H "Content-Type: application/json"
```

The response:

    {
        "valid": true,
        "details": "goodname passes validation"
    }

#### Bad Test

```bash
curl localhost:5000/validate_name/ -d '{"proposed_name":"Badname01"}' -X POST -H "Content-Type: application/json"
```

    {
        "valid": false,
        "details": "Badname01 is not all lower case."
    }

## Returns

In working with an endpoint, it is imperative from a backwards compatibility perspective that you maintain the keys that you start with. If you are adopting a micro services approach like this with an endpoint that is going to provide data back, then you must maintain some consistency with the keys that you are using. If you all of a sudden change "valid" to "status", then you are going to have extra work to do. Maintain the keys, and maybe expand the data structure to maintain "valid" as a key. You can add more keys into the base of the structure response.

## Nautobot Custom Validator

{{< alert "info" >}}
I have a "sandbox" Nautobot App that I use to do tests like this. It is its own standalone plugin that I have built from the structure that built many of the Network to Code sponsored Nautobot Apps. You may want to build a Sandbox app for yourself to work from as well.


{{< /alert >}}
The Nautobot Custom Validator is quite boring actually compared to the code that is put into the remote API. The code is the following and then I'll explain a few of the core parts:

```python linenums="1"
"""Custom validators."""
import requests

from nautobot.apps.models import CustomValidator


class DeviceValidator(CustomValidator):
    """Custom validator for Device names to be validated remotely."""

    model = "dcim.device"

    def clean(self):
        response = requests.post(
            url="http://validator_svc/validate_name/",
            json={"proposed_name": self.context["object"].name},
            headers={"Content-Type": "application/json"},
        )

        if not response.json().get("valid"):
            self.validation_error({"name": response.json().get("details", "Error in testing.")})


custom_validators = [DeviceValidator]

```

The validator is going to make an API request out and Python Requests is the best library for single threaded requests, so that is imported. If you do not have the Requests module in your Nautobot environment, you need to make sure to add the Python Requests library to the pip install in the Nautobot environment.

Line 10 shows the model that is having the validation applied to. This is required for the application to know what to validate.

Within the clean method the first action is to make a POST request to the validator service. This provides a response back as part of the API definition that was set up.

Lines 19 and 20 are the components that are required by Nautobot and the custom validator to provide a negative response if there is an error in the validation and to provide a message back. The dictionary key is the field on the form that is having an error. The value in the dictionary is the details to present back to the form.

The last line on line 23 assigns a list of the single class to do validation against. This then gets loaded into the validation engine for Nautobot.

## How Would I Do This Differently?

If all I was doing was using case or another field that could be done with Regex, I would look at using the Nautobot Data Validation app. That was built with this in mind and to provide a methodology. The second part I would do would be to not put the validation into a separate application, at least not immediately. With the minimal amount of code, that is something that could have just been done in the validator itself. I completed it this way for demonstration purposes and a start for some personal learning of Flask for my own studies.

## Summary

All together, I'm looking at having the Nautobot custom validator as part of my practices as it is needed, but is something that should probably be added sooner than later. 

To get started with a custom validator for your business logic, create your own Nautobot App, then install it into your environment. You don't need to have new models in order to make a Nautobot App. The best way to do this at the moment is to copy another plugin, such as the Nautobot BGP Plugin. Remove all of the information in the models and then put the code pieces together. That is not a great answer, and there will be more coming soon on this!

Josh