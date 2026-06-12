# Gemma 4 Model Series

## Models Under Benchmark

We are benchmarking two models from this family on a Framework Desktop with AMD Ryzen AI MAX+ 395 (96 GB GPU / 32 GB CPU unified memory):

| Model | Format | Role |
|---|---|---|
| `unsloth/gemma-4-26B-A4B-it-GGUF` (UD-Q4_K_M) | GGUF, MoE | Efficiency baseline |
| `unsloth/gemma-4-31B-it-qat-GGUF` (UD-Q4_K_XL) | GGUF, Dense, QAT | Quality target |

Both models load with `thinking = 1` (chain-of-thought reasoning enabled), making results directly comparable. At runtime, the 31B model + KV cache consumes ~43 GB of GPU memory.

### Ramalama Serve Commands

**26B MoE:**
```bash
ramalama serve \
  --name llm-server \
  --port 8081 \
  --network llm-bench \
  hf.co/unsloth/gemma-4-26B-A4B-it-GGUF/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf
```

**31B Dense (UD-Q4_K_XL):**
```bash
ramalama serve \
  --name llm-server \
  --port 8081 \
  --network llm-bench \
  hf.co/unsloth/gemma-4-31B-it-qat-GGUF/gemma-4-31B-it-qat-UD-Q4_K_XL.gguf
```

> The 31B requires the explicit filename — without it, Ramalama defaults to the MTP drafter file and fails to load.

## Benchmark Results — Gemma 4 26B-A4B (AI MAX+ 395 GPU)

> **Note:** Run was cut short at 1 of 10 requests due to a hard system crash. Results reflect a single completed request.

| Metric | Value | Source |
|---|---|---|
| Requests completed | 1 of 10 (run incomplete — system crash) | GuideLLM |
| Input tokens | 92 | Ramalama server |
| Output tokens | 2,203 | Ramalama server |
| Prompt eval speed | 428 t/s | Ramalama server |
| Prompt eval time | 214.81 ms | Ramalama server |
| Generation speed | 43.31 t/s | Ramalama server |
| Generation time | 50,869 ms | Ramalama server |
| Total time | 51,084 ms | Ramalama server |

Prompt: 500–1000 word technical essay on Transformer vs. State Space Model architectures (see `prompt.txt`). Benchmark run with `--rate-type synchronous`, 1 concurrent user, 10 samples.

## Benchmark Results — Gemma 4 31B Dense (AI MAX+ 395 GPU)

> **Note:** Results confirmed stable across requests — no warmup effect. Generation speed is consistent from the first request onward.

| Metric | Value | Source |
|---|---|---|
| Requests completed | 2 confirmed stable | Ramalama server |
| Input tokens | 99 | Ramalama server |
| Output tokens | ~1,742 | Ramalama server |
| Prompt eval speed | ~128 t/s | Ramalama server |
| Prompt eval time | ~751 ms | Ramalama server |
| Generation speed | 11.47 t/s | Ramalama server |
| Generation time | ~151,845 ms | Ramalama server |
| Total time | ~152,597 ms | Ramalama server |

Prompt: same as 26B run (see `prompt.txt`). Benchmark run with `--rate-type synchronous`, 1 concurrent user.

## Head-to-Head Comparison (AI MAX+ 395 GPU)

| Metric | 26B MoE | 31B Dense | Ratio |
|---|---|---|---|
| Prompt eval speed | 428 t/s | ~128 t/s | 26B is 3.3x faster |
| Generation speed | 43.31 t/s | 11.47 t/s | 26B is 3.8x faster |
| Total time per request | 51,084 ms | ~152,597 ms | 26B is 3.0x faster |
| Output tokens | 2,203 | ~1,742 | — |

The speed difference reflects architecture: the MoE activates only ~4B parameters per forward pass while the dense 31B activates all 30.7B on every token.

---

Gemma 4 is Google DeepMind's open multimodal model family, released under the Apache 2.0 license. Models accept text and image input and produce text output. The family spans a wide range of sizes, from edge-optimized models to a dense 31B.

## Model Variants

| Model | Architecture | Active Params | Context | Notes |
|---|---|---|---|---|
| Gemma 4 E2B | Dense | 2B | — | Mobile/edge optimized |
| Gemma 4 E4B | Dense | 4B | — | Mobile/edge optimized |
| Gemma 4 4B | Dense | 4B | — | |
| Gemma 4 12B | Dense | 12B | — | |
| Gemma 4 26B-A4B | MoE | 4B active / 26B total | 256K | Efficient inference, lower compute per token |
| Gemma 4 31B | Dense | 30.7B | 256K | Highest quality in the family |

## Gemma 4 31B

- **HuggingFace:** https://huggingface.co/google/gemma-4-31B-it-qat-q4_0-unquantized
- **Architecture:** Dense (all parameters active per forward pass), 60 layers
- **Context window:** 256K tokens
- **Attention:** Hybrid — interleaved local sliding window (1,024 tokens) + full global attention
- **Global attention:** Unified K/V with Proportional RoPE (p-RoPE) for long-context efficiency
- **Vision encoder:** ~550M parameters (text + image input)
- **Vocabulary:** 262K tokens
- **License:** Apache 2.0

### QAT Quantization

The 31B uses Quantization-Aware Training (QAT), meaning the model is trained with quantization in the loop rather than quantized after the fact. This preserves quality close to bfloat16 while significantly reducing memory requirements — better quality at the same bit-width compared to standard post-training quantization (PTQ).

### Benchmark Performance

| Benchmark | Score |
|---|---|
| MMLU Pro | 85.2% |
| GPQA Diamond | 84.3% |
| AIME 2026 | 89.2% |
| LiveCodeBench v6 | 80.0% |

## Gemma 4 26B-A4B (MoE)

The 26B-A4B is a Mixture of Experts model — only 4B parameters are active during each forward pass despite 26B total parameters. This makes inference significantly cheaper per token at the cost of higher memory to hold all weights.

- **unsloth GGUF:** `unsloth/gemma-4-26B-A4B-it-GGUF`
- **Context window:** 256K tokens

## 31B Quantized Releases: Comparison

There are four official/semi-official quantized releases of the 31B — two from Google, two from unsloth. They split into two fundamentally different formats.

### GGUF (compatible with llama.cpp / Ramalama)

| Model | Size | Quant Method | Files |
|---|---|---|---|
| [`google/gemma-4-31B-it-qat-q4_0-gguf`](https://huggingface.co/google/gemma-4-31B-it-qat-q4_0-gguf) | 17.7 GB | Q4_0 | Single file + mmproj |
| [`unsloth/gemma-4-31B-it-qat-GGUF`](https://huggingface.co/unsloth/gemma-4-31B-it-qat-GGUF) | 17.3 GB (UD-Q4_K_XL) | Multiple levels | UD-Q4_K_XL, Q4_0, Q8_0, F16, BF16 + MTP drafter |

**Google Q4_0 GGUF:** A single, simple Q4_0 file positioned for "broad ecosystem compatibility." Straightforward to deploy but offers no choice of quantization level. Q4_0 is the older baseline GGUF quantization format.

**unsloth GGUF:** A full collection with multiple quantization levels. The recommended default is **UD-Q4_K_XL** — K-quantization assigns more bits to the most sensitive weight layers, producing better quality than Q4_0 at a similar file size. Also includes an MTP (Multi-Token Prediction) drafter file for speculative decoding, which can improve throughput. This is the better choice for Ramalama/llama.cpp use.

### W4A16 Compressed Tensors (vLLM / SGLang only — not compatible with Ramalama)

| Model | Size | Runtime |
|---|---|---|
| [`google/gemma-4-31B-it-qat-w4a16-ct`](https://huggingface.co/google/gemma-4-31B-it-qat-w4a16-ct) | ~34B tensors | vLLM, SGLang |
| [`unsloth/gemma-4-31B-it-qat-w4a16`](https://huggingface.co/unsloth/gemma-4-31B-it-qat-w4a16) | ~34B tensors | vLLM, SGLang |

**W4A16** = 4-bit weights, 16-bit activations. The **CT** (compressed-tensors) serialization format is native to vLLM and SGLang and is not loadable by llama.cpp or Ramalama. Both variants are functionally equivalent — unsloth's is a repackage of Google's. These are suited for multi-GPU server deployments, not the single-APU local inference setup used here.

### Summary for This Benchmark Setup

Since we use Ramalama (llama.cpp backend), only the GGUF variants apply. Between the two GGUF options, **`unsloth/gemma-4-31B-it-qat-GGUF` with UD-Q4_K_XL** is the better choice — higher quality quantization than Google's Q4_0 and includes the MTP drafter for potential speculative decoding gains.

## Other unsloth GGUF Variants

| Model ID | Description |
|---|---|
| `unsloth/gemma-4-26B-A4B-it-GGUF` | 26B MoE, standard GGUF |
| `unsloth/gemma-4-26B-A4B-it-qat-GGUF` | 26B MoE, QAT quantized |
| `unsloth/gemma-4-12b-it-GGUF` | 12B dense |
| `unsloth/gemma-4-12B-it-qat-GGUF` | 12B dense, QAT quantized |
