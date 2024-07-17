---
authors: [jvanderaa]
comments: true
date: 2024-07-17
slug: redux-wireless-conversion
categories:
- redux
- wireless
- cisco
title: "Redux: Wireless Conversion"
toc: true
draft: false
tags:
- redux
---

This may be my favorite post within the realm of what is possible as I write this series. There are many more things that could be done, but we did pretty well considering. Going back over a decade now, I had the fortunate opportunity to work to deploy Guest WiFi :material-wifi: for a large number of retail sites, with the heavy lifting of the work being done within a five month period of time. This post is about the conversion of access points from one management system to another.

<!-- more -->

## The Task At Hand: Converting Management System

As part of the process to better manage the wireless infrastructure, it was determined that we needed to migrate management systems as a first step to the process before adding any additional infrastructure to account for the expected capacity needs. The deployment of additional capacity would be required to help provide consistent wireless experience for guests throughout the store. The wireless profile of where guest mobile devices would be used was a little different than the every day store operations wireless needs.

What was needed was to get access points to join a new wireless management system, effectively a code upgrade would be needed. At which point it would go through the discovery process to join a wireless controller. We decided to convert one store at a time and would convert the wireless system in small batches to migrate seamlessly over to the new system. To accomplish this we partnered with a team that built out a database system that would track the migration to completion, verifying that all the steps that were needed were completed. As part of this database, the system provided all of the necessary commands to complete the activity in a copy and paste fashion. So the process looked like:

1. Migration technician would log into the database
2. Initialize the migration based on the schedule
3. Start the process on say 3 access points, none of which were in the same area of the retail environment. I don't remember how many access points at a time were done. Just that we would separate it out so that no one area of the site would be completely offline.
4. Have the remote AP join a staging controller that received all of the new access points join it
5. Apply the configuration to the wireless AP, including the final controller destination
6. Have the AP move to the new controller, and verify functionality

This process worked out well and completed the activity required to move into the next stages of providing Guest WiFi throughout the entire environment.

## How I Would Accomplish This in 2024

The overall process worked great, I don't think that I would change too much to the process for those requirements. It was a cost effective way to provide wireless out to a large retail environment. But, I would absolutely automate the process a bit further. The concept of using the database for the inventory is wise. It is the foundation of building good network automation. Let's break this apart into more sections of what I would do differently. The phases that I would look at are now:

* Data Gathering
* Migration
* Continuing Operations

### Data Gathering

I would look for a way to get the data from original management system if it was available and put it into Nautobot as my vendor agnostic source of truth. Why? Well, this will set up for future success if needing to make other migrations without having to rely on a system that may have its own path. I would attempt to build out the following data points and the why I would need it:

| Data Point | Why Needed? |
| ---------- | ----------- |
| Ethernet MAC Address | Needed for identification of the device |
| Neighbor Interface | Needed for recovery of services if necessary |
| Current Clients | Needed for **verification** of services at the end |

There are two data points of what is needed. The MAC address is a pretty self evident item as it is what identifies the physical unit to the network.

For the neighbor interface I would build out the switches inside of Nautobot with the corresponding interface names. I would then build the cable connection to the device. From there, that is all that I would build out. Nautobot provides for the capability to also put data points such as cable length, color of cable and so on into the database. I would **not** do this. Why? I don't need it for anything. I know that I can come back and gather that data later if it was ever needed. But from the task at hand for the automation did I need this? No. So I'm not going to worry about that data point.

As a starting point, additional diagnostic data about the environment would be gathered and recorded for verification. Things such as the number of wireless clients on the network and what their MAC addresses are. This would provide the proper verification that the services were working.

With the data available inside of Nautobot, I can now start a process to make the migration.

### Migration

Now the bigger dream that I would have for this migration would to get it fully automated, with logging additions. I would use a long running Job to start the migration. This is something that I would first look towards Nautobot to control the process of initiating the configuration update. I would [add a new status into Nautobot](https://docs.nautobot.com/projects/core/en/stable/user-guide/platform-functionality/status/#customizing-statuses) of `Upgrading`. This will allow me to query the Nautobot database to know exactly what access points are in the process of upgrade, and give a quick search while in a loop to determine if the next access point is ready for the upgrade. 

??? note "Nautobot Task Timeout"
    Of note that the Nautobot Task timeout would need to be increased for this task. Take a look at the Nautobot Docs for further explanation - https://docs.nautobot.com/projects/core/en/stable/user-guide/administration/configuration/optional-settings/#celery_task_soft_time_limit.

Once the access point has started the migration, there would need to be a separate task that would be run to complete the controller side of the upgrade. That once an access point was ready for completing the configuration, that the automation to complete the configuration would be completed. Here I would first look to determine if there was a logging mechanism that I could hook into with the wireless LAN controller (WLC). That when the WLC had a new access point join the controller, send a log to a logging destination. Then from the logging destination would fire a webhook to a service that would provision the access point. This I would look to house on a separate Nautobot Job as the easiest getting started perspective. Then this provisioning Nautobot Job would:

1. Gather the MAC addresses of the access points that are on the staging controller
2. Look up the MAC address inside of Nautobot to determine what the access point configuration should be
3. Provision the access point as prescribed by the source of truth - Nautobot
4. Send the AP to its final controller
5. Log into the final controller, and verify that the AP is providing the services it suggests that it is
6. Change the status of the access point in Nautobot from Upgrading to Active

I would then build out a reporting view to show the status of the ongoing sites, the past day of site migrations, and the past week of migrations. I would likely build out a data model to handle the migration data to be able to see the status of the site as it progressed as well.

### Continuing Operations

Now that these processes have been built out, I would look to arm the operations teams with these tools to be able to complete the daily activities, such as break/fix replacement of APs, the re-provisioning of access points, and provide a verification/audit capability to compare the configuration of the APs to the intended design housed with Nautobot (are changes being made locally without updating the source of truth).

## Summary

Overall the process to migrate from one architecture to another architecture over a decade ago went well. There was the start of a source of truth strategy that I look back and that I missed that opportunity on. There may have been a few times that the data gathered during that migration effort was used, but not in what it should look like to make that data available as needed like there is today with something like Nautobot. The human side of the conversion would need to be looked at a little bit further as well. How errors would be handled and escalated as necessary. But by putting the automation in the hands of the system, consistency of the migration would ensure quality and full completion. Thoughts?

-Josh