---
date: 2025-11-30
slug: siri-shortcuts-microphone
categories:
- productivity
- apple
title: Using Siri Shortcuts to Set Microphone
toc: true
tags:
- siri
- shortcuts
- apple
- mac
- productivity
- automation
author: jvanderaa
params:
  showComments: true
---

Managing audio settings on Mac devices can be repetitive, especially when switching between different microphones for calls, recordings, or meetings. Siri Shortcuts provides a powerful way to automate this process.

<!--more-->

## The Problem

I found myself constantly having to go to the audio settings and use the <kbd>Option</kbd> click to get to the sub menu that would set the microphone to my external microphone. After doing this manually for several years, I knew there had to be a better way.

## The Solution

Recently I have been doing a few things with Siri Shortcuts on my Mac, learning a few more capabilities that the tool has. So I took a multiple step approach to getting the microphone to be set, with some help from ChatGPT and Claude.

First I built a Shortcut that would handle just setting the microphone to my Yeti mic. With a little bit of help and the use of the Homebrew SwitchAudioSource command line script I was able to have Siri Shortcuts set the microphone.

This is great, but I wanted to automate this further. Next, I verified that I could automate this Shortcut whenever the Bluetooth device connected. I found this capability within the Automation section.

The last piece: I didn't want the automation to fail if the device was not connected, whether because I was traveling away from home or using the laptop without the dock attached. Originally I went down the location path, but that didn't help when I was moving around within the house. So I went with a quick script check to determine if the Yeti microphone was attached to the device.

## Setting Up the Shortcut

Let's dive through setting up the automation pieces. 

1. With Homebrew you will need to install [switchaudio-osx](https://formulae.brew.sh/formula/switchaudio-osx#default).
```
brew install switchaudio-osx
```

   1. Once installed, validate what devices are available and find your device name.
   ```
   SwitchAudioSource -a
   ```
   2. Run the command outside of Siri Shortcuts to validate that the script works before integrating it

   ```
   /opt/homebrew/bin/SwitchAudioSource -t input -s "Yeti Stereo Microphone"
   ```

2. Once the script works, set up your Shortcuts

![Shortcuts image with these settings](image.png)

    1. This will use multiple `Run Shell Script` types, the first of which verifies the microphone is attached to the system.
    2. If the first script's output contains the word `Yeti`, the second script executes to change the **input** device to the Yeti microphone. Note that this does not change the audio output; I let the system handle that automatically.
    3. In the `Otherwise` section I set some output to help debug if that condition is hit.
    4. Name the Shortcut at the top of the interface

3. Set the automation

   1. To get the automation to run whenever a particular Bluetooth device connects, use the automation section on the left sidebar to create a new automation. Select "Bluetooth" as an option.

   ![Bluetooth option](image-1.png)
   2. Select your device from the list. Set the option to "Is Connected" and "Run Immediately". If you want to receive confirmation before making the switch, you can use the "Run After Confirmation" option instead. I am _not_ using this.

   ![Bluetooth Options](image-2.png)

   3. Finally, select the Shortcut that you just created.

## Using the Shortcut

Now this Shortcut will run immediately when the Bluetooth device connects to your Mac.

## Summary

Siri Shortcuts definitely has some power. There are some interesting quirks to how it works, but it is a tool you can use to help automate your Mac environment. I'm likely to dive into a few more areas as well that will help automate my workflows.

— Josh
