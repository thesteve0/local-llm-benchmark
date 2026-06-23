# Mellum2 12B-A2.5B Thinking

**HuggingFace (Q8_0 GGUF):** https://huggingface.co/JetBrains/Mellum2-12B-A2.5B-Thinking-GGUF-Q8_0
**HuggingFace (Q6_K GGUF):** https://huggingface.co/JetBrains/Mellum2-12B-A2.5B-Thinking-GGUF-Q6_K
**HuggingFace (base model):** https://huggingface.co/JetBrains/Mellum2-12B-A2.5B-Thinking
**Developer:** JetBrains
**License:** Apache 2.0

## Why This Model

JetBrains-developed MoE reasoning model explicitly designed for agentic workflows, multi-step planning, and complex debugging. At only 2.5B active parameters per token it is the most computationally lightweight model in this benchmark set — interesting as a speed/quality tradeoff candidate for agentic use where latency per token matters.

## Models Under Benchmark

| Model | Format | Size | Role |
|---|---|---|---|
| `JetBrains/Mellum2-12B-A2.5B-Thinking-GGUF-Q8_0` | GGUF, MoE | 12.9 GB | Quality baseline (effectively lossless) |
| `JetBrains/Mellum2-12B-A2.5B-Thinking-GGUF-Q6_K` | GGUF, MoE | 10.9 GB | Efficiency target |

Both models emit chain-of-thought inside `<think>...</think>` blocks. The MoE architecture activates only 2.5B parameters per forward pass (8 of 64 experts), despite holding 12B total weights in memory.

### Ramalama Serve Commands

**Q8_0 (quality baseline):**
```bash
ramalama serve \
  --name llm-server \
  --port 8081 \
  --network llm-bench \
  hf.co/JetBrains/Mellum2-12B-A2.5B-Thinking-GGUF-Q8_0/Mellum2-12B-A2.5B-Thinking-Q8_0.gguf
```

**Q6_K (efficiency target):**
```bash
ramalama serve \
  --name llm-server \
  --port 8081 \
  --network llm-bench \
  hf.co/JetBrains/Mellum2-12B-A2.5B-Thinking-GGUF-Q6_K/Mellum2-12B-A2.5B-Thinking-Q6_K.gguf
```

## Benchmark Results — Mellum2 12B-A2.5B Q8_0 (AI MAX+ 395 GPU)

| Metric | Value | Source |
|---|---|---|
| Input tokens | 93 | Ramalama server |
| Output tokens | 1,718 | Ramalama server |
| Prompt eval speed | 387.28 t/s | Ramalama server |
| Prompt eval time | 240.14 ms | Ramalama server |
| Generation speed | 81.19 t/s | Ramalama server |
| Generation time | 21,160 ms | Ramalama server |
| Total time | 21,400 ms | Ramalama server |
| Graphs reused | 1,709 / 1,718 tokens (99.5%) | Ramalama server |

## Benchmark Results — Mellum2 12B-A2.5B Q6_K (AI MAX+ 395 GPU)

> **Note:** Cold-start run (empty prompt cache, task 0). Prompt eval numbers are fully representative.

| Metric | Value | Source |
|---|---|---|
| Input tokens | 93 | Ramalama server |
| Output tokens | 2,157 | Ramalama server |
| Prompt eval speed | 345.55 t/s | Ramalama server |
| Prompt eval time | 269.14 ms | Ramalama server |
| Generation speed | 92.89 t/s | Ramalama server |
| Generation time | 23,220 ms | Ramalama server |
| Total time | 23,489 ms | Ramalama server |
| Graphs reused | 2,147 / 2,157 tokens (99.5%) | Ramalama server |

## Head-to-Head Comparison (AI MAX+ 395 GPU)

| Metric | Q8_0 | Q6_K | Ratio |
|---|---|---|---|
| Prompt eval speed | 387.28 t/s | 345.55 t/s | Q8_0 12% faster |
| Generation speed | 81.19 t/s | 92.89 t/s | Q6_K 14% faster |
| Total time per request | 21,400 ms | 23,489 ms | Q8_0 10% faster (fewer output tokens) |
| Output tokens | 1,718 | 2,157 | — |

## Model Architecture

| Property | Value |
|---|---|
| Architecture | MoE (Mixture of Experts) |
| Total parameters | 12B |
| Active parameters per token | ~2.5B (8 of 64 experts) |
| Layers | 28 |
| Hidden size | 2,304 |
| Attention | Hybrid — sliding window (1,024) + full global |
| Q/KV heads | 32 Q / 4 KV (GQA) |
| Context window | 131,072 tokens |
| Vocabulary | 98,304 tokens |
| Thinking mode | Always on (emits `<think>` blocks) |
| Multimodal | No (text only) |
| Inference backend | llama.cpp (via Ramalama) |

### Training

Built from `Mellum2-12B-A2.5B-Base` via:
1. Supervised fine-tuning (loss on final assistant turn only)
2. Reinforcement learning with verifiable rewards (RLVR) on a harder mix including long-form math

## Quantization Quality (vs BF16)

| Quant | Size | KL Divergence | Top-token Match |
|---|---|---|---|
| BF16 | 24.3 GB | — | — |
| Q8_0 | 12.9 GB | 0.004 | 97.4% |
| Q6_K | 10.9 GB | 0.014 | 95.1% |
| Q4_K_M | 8.1 GB | 0.052 | 89.8% |

Q8_0 is described as effectively lossless — perplexity is marginally lower than BF16 on Wikitext-2. Q6_K is near-lossless at ~2 GB smaller.

## Benchmark Scores (from model card, self-reported)

| Benchmark | Score |
|---|---|
| LiveCodeBench v6 | 69.9% |
| BFCL v3 | 69.4% |
| BFCL v4 | 45.6% |
| AIME 2025+2026 | 58.4% |
| GSM-Plus | 87.0% |
| MMLU-Redux | 86.2% |
| GPQA Diamond | 57.6% |
| IFEval | 76.5% |
