---
authors: [jvanderaa]
toc: true
date: 2020-06-21
layout: single
comments: true
slug: apple_automator
title: Using Apple Automator to Open Projects
# categories:
# - Productivity
tags:
- vscode
- mac
- productivity
---

Today I'm going to walk through the newest part of my personal workflow for working with projects.
Straight to the point, this is going to be using Apple Automator to quickly open your project that
you wish to work on within VS Code, and presumably PyCharm as well.  

<!-- more -->


## Problem

So what is the problem that I'm trying to solve? I am one that generally likes the workspace concept
within VS Code, but I don't like having to maintain workspace files. I have found them a little
difficult to maintain and keep organized. To that end I have found that there is an option to
install VS Code shortcut into your OS path from the command pallet (cmd-P), and `path`.

![VS Code Path](/images/2020/vscode-path.png)

Once this is installed, you can issue at a terminal (or iTerm2) prompt the command `code .` and this
will bring up VS Code from the folder that you are currently working on.  

This sounds great, what is the problem? Well, I tend to open a lot of iTerm2 tabs just to open up
and go into VS Code. While working in VS Code, I then use the terminal that is baked into VS Code as
my terminal. So I have a window that is open unnecessarily.

## My Solution - Apple Script and Automator

So I was reminded about Apple Automator for some particular reason and I thought this would be a
great solution to opening VS Code directly to my folder that I want to work on and be able to close
VS Code windows whenever I was done working in a folder. So for me I use a specific directory on my
Mac to have all of my projects in them. This is a typical directory structure:

```bash
projects
├── project1
├── project2
```

### Automator Flow

The flow is going to have a prompt come to the top when a command shortcut is executed. So ->:

```bash
command-shortcut -> Select project -> Open VS Code
```

### Start a New Quick Action

When creating a new document in your Automator, make sure to select the type as **Quick Action**.
This type is needed in order to use the Keyboard shortcut later.

### First Step: Run AppleScript

I looked at a couple of options here to get the prompt to display. From what I could tell there was
options in both AppleScript and JavaScript. I choose to stick with AppleScript in the current
iteration for ease of access to the file system. I will have to do additional research, but that
would be for a learning thing, not necessarily for productivity gains. I worked through a few links
and eventually came up with the following AppleScript:

```applescript
on run {input, parameters}
    # Define the folder that is being used as project directory. This is the only thing that needs to be set
    set projectFolder to "/Users/joshv/projects/"
    # Use the finder application to get the list of all the folders inside of the folder
    tell application "Finder"
        set fileList to get name of folders of folder (projectFolder as POSIX file)
    end tell
    # Create a prompt
    choose from list fileList with prompt "Which project?"
    # Create a string of projectFolder with result of response
    set resultString to projectFolder & result as string
    # Return the path
    return the resultString as string
end run
```

The only parameter that needs to be changed is the path to the directory on the third line, to match
what is your own project directory.

### Second Step: Run Shell Script

I then took the easy way out at the moment to execute an application. I will have to work to add
this all into one AppleScript or JavaScript execution in the future, but for now I know this works.
It is a short command, first I needed to find out where the `code` application that was mentioned
above is stored. So I did the command `which code` to get my path to the code shortcut. The final
result for me is:

```bash
/usr/local/bin/code $1
```

This takes an argument that is passed in from the AppleScript and passes it into the shell script.
The next change I needed to do on the Run Shell Script module of Automator was to set
**Pass input** to _as arguments_ to pass it in as an argument.  

This now looks like the following from an Automator application:  

![Automator](/images/2020/automator-complete.png)

### Keyboard Shortcuts

Last thing to do is to assign a keyboard shortcut to your automation.

1. Open Keyboard preferences
2. Select **Shortcuts**
3. Select _Services_ on the left
4. Scroll to the section _General_
5. Find the name of your document that you created in Automator
6. Assign a keyboard shortcut, I'm using `CMD-Shift-'` for mine

![Shortcut](/images/2020/shortcuts.png)  

Now when I select the keyboard shortcut, I get a visual prompt of the folders in the project folder
specified. And when I select the project and **OK** I am then taken to either a new VS Code window
based in that directory or the already opened VS Code window for that project folder.  

## Summary

Not all automation tools have to be Python, Ansible, or other modern language. You can use tools
that are provided that may feel old to help you in your every day work. Hopefully this comes in
handy for you as well! Let me know. In the end, if this helps great, otherwise this is good
documentation for myself if needed in the future!  

Thanks,

-Josh
