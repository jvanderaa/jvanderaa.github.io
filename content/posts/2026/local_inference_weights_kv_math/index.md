---
title: "The Math Behind Running LLMs Locally: Weights and KV Cache"
date: 2026-03-26
draft: true
description: "Why does a 70B model need 40GB of RAM? What is a KV cache and why does context length eat your memory? Here's the math behind running large language models on your own hardware."
summary: "A practical breakdown of the two things that determine whether your local LLM fits in memory: model weights and the KV cache. No PhD required."
tags:
  - ai
  - llm
  - local-ai
  - inference
categories:
  - ai
  - learning
featureimage: "feature.png"
---

When I started running LLMs locally on my Mac Studio, I ran into the same confusion most people hit: why does a "70B" model need ~40GB of RAM? What actually happens when you run out of context? And what is everyone talking about when they say "KV cache"?

This post is my attempt to explain the math clearly - the kind of explanation I wish I'd had when I started.

---

## Part 1: Model Weights - Why 70B Means ~40GB

<!-- TODO: Explain parameters vs bytes vs GB -->
<!-- Key formula: params × bytes_per_param = VRAM for weights -->
<!-- Walk through each quantization level: FP32, FP16, INT8, Q4 -->

### Parameters vs Bytes

A "70 billion parameter" model has 70,000,000,000 individual numbers stored in it. Each number takes up space depending on its precision:

| Format | Bits per weight | Bytes per weight | 70B model size |
|--------|----------------|------------------|----------------|
| FP32   | 32             | 4                | ~280 GB        |
| FP16   | 16             | 2                | ~140 GB        |
| INT8   | 8              | 1                | ~70 GB         |
| Q4_K_M | ~4.5          | ~0.56            | ~40 GB         |

<!-- TODO: Add your own real example - what does your Mac Studio run at what quant? -->

### What Quantization Actually Does

<!-- TODO: Explain the tradeoff - smaller numbers = less precision = slight quality loss -->
<!-- Real example: running Qwen3.5 122B at Q6_K_XL on the Mac Studio -->

---

## Part 2: The KV Cache - Why Context Length is Expensive

<!-- TODO: This is the "why did adding a longer prompt suddenly crash my inference?" section -->

### What the K and V Actually Are

When a transformer processes text, at each attention layer it computes three things for every token: a **Query (Q)**, a **Key (K)**, and a **Value (V)**.

- The Query is "what am I looking for?"
- The Key is "what do I contain?"
- The Value is "what should I pass forward?"

During generation, every new token needs to attend to every previous token. Without a cache, you'd recompute K and V for all previous tokens on every single step. The KV cache stores those results so you only compute them once.

### The KV Cache Memory Formula

<!-- TODO: Fill in the formula and walk through it -->

The memory required for the KV cache scales with:

```
KV cache size = 2 × num_layers × num_kv_heads × head_dim × seq_len × bytes_per_element
```

- `2` = one K tensor + one V tensor
- `num_layers` = depth of the model (e.g., 80 for Llama 3 70B)
- `num_kv_heads` = number of key-value heads (GQA reduces this vs MHA)
- `head_dim` = dimension of each head (usually 128)
- `seq_len` = total context length (prompt + output so far)
- `bytes_per_element` = 2 for FP16, 1 for INT8

<!-- TODO: Work a real example - Qwen3.5 122B at 65K context = how many GB? -->

### MHA vs GQA vs MQA

<!-- TODO: Explain why modern models use Grouped Query Attention to shrink the KV cache -->
<!-- This is why Llama 3 70B has 8 KV heads instead of 64 -->

---

## Part 3: Total VRAM Budget

<!-- TODO: Bring it together -->

The total VRAM you need to run a model is roughly:

```
Total VRAM ≈ weights + KV cache + activations overhead (~10-20%)
```

<!-- TODO: Real numbers from your Mac Studio setup -->
<!-- Qwen3.5 122B Q6_K_XL + 65K context × 4 slots = ? -->

---

## What This Means in Practice

<!-- TODO: Practical takeaways for someone running LLMs at home -->

- Why 4-bit quants matter more than you think
- How to estimate if a model fits before downloading it
- The context window vs throughput tradeoff

---

## Further Reading

**On KV caches:**
- [KV Caching Explained - Hugging Face Blog](https://huggingface.co/blog/not-lain/kv-caching) - clear intro to why KV caching exists
- [LLM Inference Series: KV Caching, a Deeper Look - Pierre Lienhart](https://medium.com/@plienhar/llm-inference-series-4-kv-caching-a-deeper-look-4ba9a77746c8) - goes into the math properly
- [KV Cache Memory Calculation for LLMs - Lyceum Technology](https://lyceum.technology/magazine/kv-cache-memory-calculation-llm/) - formulas for MHA, GQA, and MQA architectures

**On weights and quantization:**
- [Quantization Explained: Q4_K_M vs AWQ vs FP16 - SitePoint](https://www.sitepoint.com/quantization-q4km-vs-awq-fp16-local-llms/) - practical comparison of quant formats
- [LLM Quantization - BentoML Inference Handbook](https://bentoml.com/llm/getting-started/llm-quantization) - approachable explanation of FP32 → INT4 tradeoffs
- [Understanding and Coding the KV Cache from Scratch - Sebastian Raschka](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms) - if you want to go deeper with code

---

-Josh
