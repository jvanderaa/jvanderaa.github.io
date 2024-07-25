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

To better manage the wireless infrastructure, we needed to migrate management systems as a first step before adding any additional infrastructure to meet the expected capacity needs. The deployment aimed to ensure a consistent wireless experience for guests throughout the store. The wireless profile for guest mobile devices differed from everyday store operations.

The goal was to get access points to join a new wireless management system, effectively requiring a code upgrade. The process involved converting one store at a time and migrating the wireless system in small batches to ensure seamless transition. We partnered with a team that built a database system to track the migration, verifying all necessary steps were completed. The process was as follows:

1. Migration technician logs into the database.
2. Initializes the migration based on the schedule.
3. Starts the process on a few access points, ensuring no area of the retail environment is completely offline.
4. The remote AP joins a staging controller that receives all new access points.
5. Applies the configuration to the wireless AP, including the final controller destination.
6. The AP moves to the new controller, and functionality is verified.

This process worked well and paved the way for the next stages of providing Guest WiFi throughout the entire environment.

## How I Would Accomplish This in 2024

The overall process was effective, but I would automate it further. Using a database for inventory is foundational for good network automation. The phases I would focus on are now:

* Data Gathering
* Migration
* Continuing Operations

### Data Gathering

I would gather data from the original management system and put it into Nautobot as a vendor-agnostic source of truth. This sets up future success for other migrations without relying on a specific system. If these data points were not available from the original management system, I would write some automation to gather the data points. Key data points include:

| Data Point | Why Needed? |
| ---------- | ----------- |
| Ethernet MAC Address | Needed for identification of the device |
| Neighbor Interface | Needed for recovery of services if necessary |
| Current Clients | Needed for **verification** of services at the end |

The MAC address is essential for device identification. For the neighbor interface, I would build out the switches in Nautobot with corresponding interface names and cable connections. I would avoid unnecessary details like cable length or color unless needed for the automation task.

Gathering additional diagnostic data, such as the number of wireless clients and their MAC addresses, would help verify the services.

With data available in Nautobot, I can start the migration process.

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

Overall the process to migrate from one architecture to another architecture over a decade ago went well. There was the start of a source of truth strategy that I look back and that I missed that opportunity on. There may have been a few times that the data gathered during that migration effort was used, but not in what it should look like to make that data available as needed like there is today with something like Nautobot. The human side of the conversion would need to be looked at a little bit further as well. How errors would be handled and escalated as necessary. But by putting the automation in the hands of the system, consistency of the migration would ensure quality and full completion.

### The Best Part

The Best Part for me? I got to design and implement something very similar. I'm very proud of this execution and where that application has gone. Read more about the [case study on the Network to Code website](https://networktocode.com/study/major-chain-of-convenience-stores-streamlines-hardware-refresh-for-over-900-locations-quickly-and-consistently-with-network-automation/) 
-Josh