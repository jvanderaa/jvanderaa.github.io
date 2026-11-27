---
# TODO(Josh): set the real publish date before flipping draft to false.
date: 2026-11-27
slug: mcp-server-skills
draft: true
title: "Skills Can Now Ship Inside Your MCP Server"
summary: >
  The MCP Skills extension lets a server hand an agent its how-to instructions
  along with its tools. I walk through what changed, build a small Nautobot
  example with FastMCP, and look at where I would be careful.
categories:
  - automation
  - ai
tags:
  - ai
  - mcp
  - agent-skills
  - nautobot
toc: true
author: jvanderaa
# TODO(Josh): add feature.png to this folder (or let Grok Bot generate one) and
# fill in coverAlt / coverCaption to match.
coverAlt: >
  TODO
coverCaption: "TODO"
params:
  showComments: true
---

<!-- TODO(Josh): Replace or tweak this opening with your own moment. What made
you notice this? A specific MCP server you use, a skill you keep copying
between machines, a conversation at AutoCon? -->

I've been using MCP (Model Context Protocol) servers and Agent Skills together for a while now. The MCP server is how my agent gets to Nautobot or GitHub, and the skill is where I write down how I actually want that work done. What has bugged me is that they live in two different places. The server is something I connect to, and the skills are files I copy around and try to remember to update.

That is changing. MCP now has a Skills extension, so a server can hand the agent its skills right along with its tools. I wanted to see how it works, so I built a small Nautobot example with FastMCP. Here is what I found.

<!-- more -->

## Tools vs Skills

If you haven't spent time with both yet, here is the quick version. An MCP server gives an AI agent tools: look up a device, query an IP prefix, run a Job. That covers what the agent is able to do.

A [skill](https://agentskills.io/specification) is a folder with a `SKILL.md` file in it. The top of the file has YAML front matter with a `name` and a `description`, and below that are the instructions in Markdown. You can drop reference docs, templates, or scripts into the folder too. The agent only looks at the name and description to start. It reads the full instructions when a task needs them, and it only opens the extra files if the instructions tell it to. The spec calls this progressive disclosure. For me it just means I'm not burning context on instructions that have nothing to do with what I asked.

So the tools are the what, and the skill is the how: which tools, what order, and what "good" looks like for my environment.

## Two Things to Keep in Sync

Until now these have shipped separately. A good example of this is the community [nautobot-mcp-cli](https://github.com/latuannetnam/nautobot-mcp-cli) project. It has an MCP server for Nautobot, and it also has a set of skills in the repo. To get the skills you run an install script that copies them into your home directory, and the README says to run it again after each `git pull`.

That's fine when it is just me on my laptop. Once a team is sharing a server, it gets messy. Someone upgrades the server, a tool's arguments change, and the skill sitting on my laptop still describes the old behavior. And if the agent is running in a browser or on a phone, there's no home directory to copy anything into in the first place.

## SEP-2640: The Skills Extension

The change came in through [SEP-2640](https://modelcontextprotocol.io/seps/2640-skills-extension) from the [Skills Over MCP Working Group](https://github.com/modelcontextprotocol/ext-skills). It was opened on April 23, 2026, and the [pull request merged on September 13, 2026](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2640). The SEP is Final. The extension is still at Beta in the MCP extension lifecycle though, so I expect a few revisions as more clients pick it up.

The extension is called `io.modelcontextprotocol/skills`, and the spec targets MCP protocol revision `2026-07-28`. I like that the working group didn't add a brand new primitive for this. Skills are files, and MCP already has Resources for serving files, so they built on that.

Each file in a skill folder becomes a resource with a URI like `skill://<skill-path>/<file-path>`, and the main file is always `skill://<skill-path>/SKILL.md`. A server that supports the extension says so in its capabilities and implements two methods. `skills/list` returns the skills it has, and `skills/get` returns a single skill by URI. Every entry includes the front matter as written, plus a list of every file in the skill with its SHA-256 digest and size. There's also an optional `resources/directory/read` method for browsing a skill folder, which the server turns on with `directoryRead: true`. The file contents come back through the normal `resources/read` call when the agent actually needs them.

This is the capability block from the [extension overview](https://modelcontextprotocol.io/extensions/skills/overview):

```json
{
  "capabilities": {
    "resources": {},
    "extensions": {
      "io.modelcontextprotocol/skills": {
        "directoryRead": true
      }
    }
  }
}
```

The skill format is left to the Agent Skills spec. MCP only covers how the skills get from the server to the agent, which means a skill folder you already have can be served as it is.

## Building One With FastMCP

The easiest way I found to try this was [FastMCP](https://gofastmcp.com/servers/skills), which added skills in version 4.2.0. I used 4.2.6. The official MCP Python SDK has the extension merged, but it wasn't in a release yet when I checked the working group's [implementations list](https://github.com/modelcontextprotocol/ext-skills/blob/main/docs/implementations.md).

I kept the example small: one tool and one skill. The tool pulls a device out of Nautobot, and the skill tells the agent how to audit that device against our data standards. Here is how the folder is laid out:

```text
nautobot-lab/
├── server.py
└── skills/
    └── nautobot-device-audit/
        ├── SKILL.md
        └── references/
            └── data-standards.md
```

The `SKILL.md` is below. The front matter is what the agent sees when it is deciding whether to use the skill, and the numbered steps are what it follows once it does.

```markdown
---
name: nautobot-device-audit
description: Check that a device in Nautobot meets our data standards before it is used for config generation. Use when asked to audit, validate, or review a device record.
---

# Nautobot device audit

1. Use the `get_device` tool to pull the device by name.
2. Compare the record against `references/data-standards.md`.
3. Report each standard as PASS or FAIL with the field value you found.
4. Do not change any data in Nautobot. This skill is read-only.
```

The actual rules are in `references/data-standards.md`. The agent doesn't read this file until it is doing an audit.

```markdown
# Device data standards

- Name is lowercase and follows `<site>-<role>-<number>`, for example `msp01-leaf-01`.
- Status is `Active` before the device is used for config generation.
- Location, Role, and Platform are all set.
- A primary IPv4 address is assigned.
```

<!-- TODO(Josh): Swap these for your real standards or the naming convention
from the OSNM book lab, if you want readers to be able to follow along. -->

Next up is the server. `SkillsDirectoryProvider` picks up every skill folder under `skills/`, and the folder path turns into the skill URI. The tool itself is just a call to the Nautobot REST API.

```python
import os

import httpx
from fastmcp import FastMCP
from fastmcp.skills.provider import SkillsDirectoryProvider

mcp = FastMCP("nautobot-lab", providers=[SkillsDirectoryProvider("skills")])


@mcp.tool
def get_device(name: str) -> dict:
    """Get a device record from Nautobot by name."""
    response = httpx.get(
        f"{os.environ['NAUTOBOT_URL']}/api/dcim/devices/",
        params={"name": name, "depth": 1},
        headers={"Authorization": f"Token {os.environ['NAUTOBOT_TOKEN']}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    mcp.run()
```

The `providers=` argument is the only line in there that has anything to do with skills. FastMCP takes care of registering the extension and the new methods. With that in place, `fastmcp list` shows the tool and the skill side by side:

```text
$ fastmcp list server.py --skills
Tools (1)

  get_device(name: str) -> dict
    Get a device record from Nautobot by name.

Skills (1)

  skill://nautobot-device-audit/SKILL.md
    Check that a device in Nautobot meets our data standards before it is used
    for config generation. Use when asked to audit, validate, or review a device
    record.
    skill://nautobot-device-audit/SKILL.md (490 bytes)
    skill://nautobot-device-audit/references/data-standards.md (264 bytes)
```

This is the `skills/list` entry a client gets back. Each file has a digest, so the client can check that what it reads later is the same thing it was shown.

```json
{
  "uri": "skill://nautobot-device-audit/SKILL.md",
  "frontmatter": {
    "name": "nautobot-device-audit",
    "description": "Check that a device in Nautobot meets our data standards before it is used for config generation. Use when asked to audit, validate, or review a device record."
  },
  "resources": [
    {
      "uri": "skill://nautobot-device-audit/SKILL.md",
      "digest": "sha256:e6cb7bd1de7c3236c27ed5f88f60bac93fbd29d4b5f56f137dbc99fbab081e89",
      "size": 490
    },
    {
      "uri": "skill://nautobot-device-audit/references/data-standards.md",
      "digest": "sha256:3569aa246198d2dd65980ae9e311a5c3d9d20f5a1e377a6214f237e5e777f5f4",
      "size": 264
    }
  ]
}
```

<!-- TODO(Josh): The output above came from a test run of this exact code with
FastMCP 4.2.6 (no live Nautobot behind it). Re-run it in your lab, ideally
against the OSNM book Nautobot, and add a screenshot of an agent actually
running the audit. -->

When I want to change the skill, I edit the folder and redeploy the server. Anyone who connects after that gets the new version. The digests change too, so the client can tell it's looking at something different.

## Client Support

The server is only half of this. The agent you're using has to support the extension as well, and that is still rolling out.

VS Code is one of the first ones there. Microsoft [posted on November 18, 2026](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/skills-over-mcp-are-now-available-in-vs-code/4574580) that VS Code 1.147 and newer can load skills from an MCP server in GitHub Copilot. The skills show up as slash commands, and VS Code asks you before it loads skills from a server. You can allow it once or always.

<!-- TODO(Josh): If you try this in VS Code (or another client you use), add a
screenshot of the slash command and the consent prompt here. -->

When I looked at the [implementations list](https://github.com/modelcontextprotocol/ext-skills/blob/main/docs/implementations.md) and the [extension client matrix](https://modelcontextprotocol.io/extensions/client-matrix), the SDK side had it in TypeScript v2.4.0, C# v2.4.0, Rust (rmcp) v3.9.0, Ruby v1.9.0, and FastMCP v4.2.0. Python was merged but not released, and Go and Java were still in progress. For hosts, VS Code and Claude Code were listed with beta support, ChatGPT and Codex were listed as planned, and a bunch of others had pull requests open. On the server side, the GitHub MCP Server has it as an opt-in since v2.2.0, and Cloudflare and Hugging Face are already serving skills. That list is changing week to week, so check it before you count on a particular client.

## What About Network Automation?

The one that got my attention is the [Ansible Automation Platform (AAP) MCP server](https://github.com/ansible/aap-mcp-server). They [merged support for serving AAP platform skills](https://github.com/ansible/aap-mcp-server/pull/209) on October 28, 2026, turned off by default, and then on November 3 a follow-up [put skill serving under admin control](https://github.com/ansible/aap-mcp-server/pull/213).

There's a test written up in that first pull request that I thought was worth calling out. They asked a client "is my AAP platform healthy?" against a server with a skill written for pretty much that exact question. When the server didn't point the client to the skill, the client never found it. It answered that everything reported healthy, and the platform actually had a failing inventory source. When the server pointed to the skill in its `instructions` field, the client read the skill first. The `instructions` field is part of base MCP, so this works even on clients that don't support the extension yet. If I were building one of these, I would add that pointer.

This is the part I'm excited about for our space. Whoever runs Nautobot or AAP in an organization already decides which tools the agent gets to use. Now that same team can ship the how-to along with it. I can picture a device audit like the one above, a Golden Config compliance review that knows which features matter to you and what an acceptable exception is, or a new-site onboarding skill that runs the right Jobs in the right order.

<!-- TODO(Josh): Do you want to name a specific server here? For example, your
own lab server, or a public project. Keep anything from Network to Code
internal work out unless it is already public. -->

## Be Careful What You Load

A skill is a set of instructions that goes straight to the model. That makes it a prompt injection risk, and the spec doesn't shy away from that in its [security considerations](https://github.com/modelcontextprotocol/ext-skills/blob/main/specification/beta/skills.mdx). The host is supposed to treat skills from an MCP server as untrusted, and as riskier than a remote tool call. It has to label a skill with the server it came from rather than mixing it in with your local skills. A served skill can't get code running on your machine without you approving that skill, and its `allowed-tools` front matter is ignored unless you approve that too. Approvals are tied to the file digests, so if the server changes the content, you get asked again.

The digests only tell you that what you read matches the list the server gave you. They say nothing about whether the server itself is trustworthy, and the spec calls that out. I'm going to treat these the same way I treat an Ansible playbook from someone else's repo. Read it before you run it, and only connect to servers you'd already trust on your network.

The working group was also honest about when you don't need any of this. In the [September 22 meeting notes](https://github.com/modelcontextprotocol/modelcontextprotocol/discussions/3388), the guidance was that if everything already runs through a local CLI that has its own access controls, you may not need to bring MCP into it at all. It pays off more when the agent is running somewhere without a file system, or when a team is sharing a server.

## Summary

With the Skills extension, an MCP server can publish skills next to its tools through `skills/list`, `skills/get`, and `skill://` resources, with a digest on each file. The SEP is final, the extension is in Beta, and clients are still catching up. If you already run an MCP server and have a folder of skills you keep copying around, I think it's worth trying now. In FastMCP it was one line for me.

<!-- TODO(Josh): Your take goes here. Do you think skills over MCP replaces
plugin bundles and copied skill folders, or do they live side by side for a
while? Is this how you want vendors shipping "best practice" for their
platforms? -->

-Josh
