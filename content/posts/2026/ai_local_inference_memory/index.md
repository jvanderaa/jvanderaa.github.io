---
date: 2026-03-28
slug: local-inference-memory
categories:
- automation
- ai
title: "AI: Local Models Memory"
summary: >
  TODO: Update
toc: true
tags:
  - ai
  - local_ai
  - openclaw
author: jvanderaa
coverAlt: AI Memory Bursting
coverCaption:
params:
  showComments: true
---

For a long while I was getting it all wrong with my set up of AI local inference. I thought that for each sub-agent that I would spin up on my OpenClaw that the system would use that amount of VRAM. I've been running [Qwen3.5-122B-A10B](https://huggingface.co/unsloth/Qwen3.5-122B-A10B-GGUF) at 6bit. This model uses 101GB in the loading of the model. So I thought if I had two sub-agents using this model that I would need 202GB of RAM. **I was wrong**.

So what I was doing was loading multiple models into my system and pointing different sub-agents at different models. Where my heavy coding agent would use a much lighter than the model that I would be using for reasoning and research.

![Wrong memory footprint](image.png)

## Introduction to Weights

I finally went ahead and asked an AI system (I forget if I talked to Harry or Gemini or ChatGPT or Claude about this). I asked the simple question, am I doing this right in that I need to have multiple models running for each sub-agent to be able to have each of the sub-agents working simultaneously, and the quick answer was that I was wrong. I was then learned that the bulk of the memory numbers that are quote are [AI Model Weights](https://www.ntia.gov/programs-and-initiatives/artificial-intelligence/open-model-weights-report/background). This is the information that is loaded and used to respond to prompts that are provided.

That being, that the weights are loaded in, and then there is a KV-Cache, which is the calculation of the context that is processed. So the system will use this KV-Cache as part of the processing. And this is dynamic in nature that grows with each prompt that is processed.

Here is what is actually happening on the system:

![AI Memory Allocations](image-1.png)

## Summary

The technology road is a road that is quite the journey. I'm learning new things all of the time. This one may have been a moment of "Yeah, you didn't know that?". Well, I did not know this and I have learned. I have migrated all of my sub-agents on to using the same local model now. And the performance out of both the original sub-agents that were using the model and the other agents that were using a bit smaller of a model is greatly improved. The system is more stable. And the best part is that I have learned something new. I just thought I would share with others. If I had the mis-understanding, then there is a non-zero chance that this may be new for someone else as well.

-Josh