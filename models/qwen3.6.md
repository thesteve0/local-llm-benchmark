# Qwen3.6 35B-A3B Model Series

**HuggingFace (unsloth GGUF):** https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF

## Models Under Benchmark

We are benchmarking two quantizations from this family on a Framework Desktop with AMD Ryzen AI MAX+ 395 (96 GB GPU / 32 GB CPU unified memory):

| Model | Format | Size | Role |
|---|---|---|---|
| `unsloth/Qwen3.6-35B-A3B-GGUF` (Q8_0) | GGUF, MoE | 36.9 GB | Quality baseline |
| `unsloth/Qwen3.6-35B-A3B-GGUF` (UD-Q4_K_M) | GGUF, MoE | 22.1 GB | Efficiency target |

Both models load with `thinking = 1` (chain-of-thought reasoning enabled). The MoE architecture activates only ~3B parameters per forward pass despite 35B total weights in memory.

### Ramalama Serve Commands

**Q8_0 (quality baseline):**
```bash
ramalama serve \
  --name llm-server \
  --port 8081 \
  --network llm-bench \
  hf.co/unsloth/Qwen3.6-35B-A3B-GGUF/Qwen3.6-35B-A3B-Q8_0.gguf
```

**UD-Q4_K_M (efficiency target):**
```bash
ramalama serve \
  --name llm-server \
  --port 8081 \
  --network llm-bench \
  hf.co/unsloth/Qwen3.6-35B-A3B-GGUF/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf
```

## Benchmark Results — Qwen3.6 35B-A3B Q8_0 (AI MAX+ 395 GPU)

| Metric | Value | Source |
|---|---|---|
| Input tokens | 91 | Ramalama server |
| Output tokens | 3,200 | Ramalama server |
| Prompt eval speed | 189.58 t/s | Ramalama server |
| Prompt eval time | 480 ms | Ramalama server |
| Generation speed | 51.76 t/s | Ramalama server |
| Generation time | 61,819 ms | Ramalama server |
| Total time | 62,299 ms | Ramalama server |
| Graphs reused | 3,186 / 3,200 (99.6%) | Ramalama server |

Generation speed was remarkably stable across the entire 3,200-token output — variance of less than 0.3 t/s from first token to last. The high graph-reuse ratio (99.6%) reflects efficient MoE expert routing with minimal expert switching across tokens.

Prompt: 500–1000 word technical essay on Transformer vs. State Space Model architectures (see `prompt.txt`). Benchmark run with `--rate-type synchronous`, 1 concurrent user.

## Benchmark Results — Qwen3.6 35B-A3B UD-Q4_K_M (AI MAX+ 395 GPU)

| Metric | Value | Source |
|---|---|---|
| Input tokens | 91 | Ramalama server |
| Output tokens | 3,750 | Ramalama server |
| Prompt eval speed | 183.70 t/s | Ramalama server |
| Prompt eval time | 495 ms | Ramalama server |
| Generation speed | 59.49 t/s | Ramalama server |
| Generation time | 63,037 ms | Ramalama server |
| Total time | 63,532 ms | Ramalama server |
| Graphs reused | 3,734 / 3,750 (99.6%) | Ramalama server |

Generation speed was stable across the entire 3,750-token output — variance of less than 0.7 t/s from start to finish.

Prompt: same as Q8_0 run (see `prompt.txt`). Benchmark run with `--rate-type synchronous`, 1 concurrent user.

## Head-to-Head Comparison (AI MAX+ 395 GPU)

| Metric | Q8_0 | UD-Q4_K_M | Ratio |
|---|---|---|---|
| Prompt eval speed | 189.58 t/s | 183.70 t/s | Q8_0 ~3% faster |
| Generation speed | 51.76 t/s | 59.49 t/s | UD-Q4_K_M 15% faster |
| Total time per request | 62,299 ms | 63,532 ms | essentially equal (different output lengths) |
| Output tokens | 3,200 | 3,750 | — |

---

## Model Architecture

Qwen3.6 is part of the Qwen3 model family from Alibaba's Qwen team. The 35B-A3B variant is a Mixture of Experts (MoE) architecture — only ~3B parameters are active during each forward pass despite 35B total parameters resident in memory. This gives MoE-class inference speed while retaining the quality of a much larger dense model.

| Property | Value |
|---|---|
| Architecture | MoE (Mixture of Experts) |
| Total parameters | 35B |
| Active parameters per token | ~3B |
| Context window | 262,144 tokens |
| Thinking mode | Enabled (`thinking = 1`) |
| Vision capability | Yes — mmproj files included in GGUF repo |
| Inference backend | llama.cpp (via Ramalama / Vulkan) |

### Vision Support

The unsloth GGUF repository includes `mmproj-BF16.gguf`, `mmproj-F16.gguf`, and `mmproj-F32.gguf` projector files, indicating multimodal (image+text) capability. Vision inference requires downloading the appropriate mmproj file alongside the main GGUF and passing it at serve time.

## Available GGUF Quantizations

| Quantization | Filename | Size | Notes |
|---|---|---|---|
| UD-Q4_K_M | `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` | 22.1 GB | Unsloth Dynamic — recommended default |
| Q8_0 | `Qwen3.6-35B-A3B-Q8_0.gguf` | 36.9 GB | Effectively lossless vs BF16 |
| UD-Q5_K_M | `Qwen3.6-35B-A3B-UD-Q5_K_M.gguf` | 26.5 GB | Mid-point quality/size |
| UD-Q6_K | `Qwen3.6-35B-A3B-UD-Q6_K.gguf` | 29.3 GB | Near-lossless |
| BF16 | `BF16/Qwen3.6-35B-A3B-BF16-*.gguf` | 69.4 GB | Full precision (2-file split) |

All quantizations fit within the 96 GB GPU allocation on the AMD Ryzen AI MAX+ 395.
