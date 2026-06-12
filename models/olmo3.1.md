# OLMo 3.1 32B Think

**HuggingFace (bartowski GGUF):** https://huggingface.co/bartowski/allenai_Olmo-3.1-32B-Think-GGUF
**HuggingFace (original):** https://huggingface.co/allenai/Olmo-3.1-32B-Think
**Developer:** Allen Institute for AI (Ai2)
**License:** Apache 2.0
**Training data:** Publicly released (Dolma 3, ~9.3T tokens)

## Why This Model

OLMo 3.1 releases both weights AND training data. It is benchmarked as the representative of
the truly open model class — open meaning both weights and training data are publicly available,
not just weights.

## Models Under Benchmark

We are benchmarking two quantizations from this family on a Framework Desktop with AMD Ryzen AI MAX+ 395 (96 GB GPU / 32 GB CPU unified memory):

| Model | Format | Size | Role |
|---|---|---|---|
| `unsloth/Olmo-3.1-32B-Think-GGUF` (Q8_0) | GGUF, Dense | ~34.3 GB | Quality baseline |
| `unsloth/Olmo-3.1-32B-Think-GGUF` (Q4_K_M) | GGUF, Dense | ~19.5 GB | Efficiency target |

### Ramalama Serve Commands

**Q8_0 (quality baseline):**
```bash
ramalama serve \
  --name llm-server \
  --port 8081 \
  --network llm-bench \
  hf.co/unsloth/Olmo-3.1-32B-Think-GGUF/Olmo-3.1-32B-Think-Q8_0.gguf
```

**Q4_K_M (efficiency target):**
```bash
ramalama serve \
  --name llm-server \
  --port 8081 \
  --network llm-bench \
  hf.co/unsloth/Olmo-3.1-32B-Think-GGUF/Olmo-3.1-32B-Think-Q4_K_M.gguf
```

## Thinking Token Verbosity — A Key Future Evaluation Dimension

OLMo 3.1 generates significantly more tokens than the other benchmarked models for the same prompt:

| Model | Output tokens | Architecture |
|---|---|---|
| Qwen3.6 35B-A3B Q8_0 | 3,200 | MoE, thinking |
| Qwen3.6 35B-A3B UD-Q4_K_M | 3,750 | MoE, thinking |
| OLMo 3.1 32B Q8_0 | 8,135 | Dense, thinking |
| OLMo 3.1 32B Q4_K_M | 6,741 | Dense, thinking |

OLMo produces roughly 2–2.5x more tokens than Qwen3.6 for the same prompt. On a slow dense model,
extra thinking tokens compound the latency problem significantly.

**For future agentic benchmarking:** token efficiency matters as much as raw speed. A model that
reaches the same accuracy with fewer thinking tokens is more valuable in practice than one that
reasons verbosely. Tracking thinking token count vs. answer quality (not just total throughput)
should be part of the next evaluation stage.

## Important: Thinking Is ON By Default Despite Ramalama Reporting Otherwise

Ramalama (via llama.cpp) reports `thinking = 0` in the server startup logs for OLMo 3.1 Think.
**This is misleading — the model IS reasoning on every request.**

### Why This Happens

OLMo's chat template **unconditionally injects `<think>` as a prompt prefix** on every assistant
turn. There is no `enable_thinking` conditional variable in the template. llama.cpp detects
thinking mode by looking for that specific conditional pattern (which Qwen3 and DeepSeek use).
Since OLMo's template doesn't have it, llama.cpp reports `thinking = 0` even though reasoning
is always active.

The practical effects:
- The model generates a full reasoning chain on every request (confirmed via `</think>` in output)
- Because `thinking = 0`, llama.cpp routes all tokens — including the reasoning chain — into the
  `content` field of the API response rather than a separate `reasoning_content` field
- For throughput/latency benchmarking this makes no difference; output token counts include
  all reasoning tokens either way
- For agentic harnesses that read `reasoning_content` to separate chain-of-thought from the
  final answer (e.g. some Goose / Hermes agent integrations), the merged output may require
  parsing `</think>` from `content` manually

### References

- [llama.cpp issue #20196](https://github.com/ggml-org/llama.cpp/issues/20196) — thinking = 0
  logged but model still emits think tokens (known detection fragility)
- [llama.cpp issue #20809](https://github.com/ggml-org/llama.cpp/issues/20809) — false positive
  thinking detection breaking tool calls on other models (same underlying auto-detect mechanism)

## Benchmark Results — OLMo 3.1 32B Think Q8_0 (AI MAX+ 395 GPU)

> **Note:** 6.32 t/s is near the theoretical maximum for a dense 32B Q8_0 model on this hardware.
> The AMD Ryzen AI MAX+ 395 has ~273 GB/s unified memory bandwidth; reading ~32 GB of weights
> per token gives a ceiling of ~8.5 t/s. This is not misconfiguration — see architecture note below.

| Metric | Value | Source |
|---|---|---|
| Input tokens | 89 | Ramalama server |
| Output tokens | 8,135 | Ramalama server |
| Prompt eval speed | 104.44 t/s | Ramalama server |
| Prompt eval time | 852 ms | Ramalama server |
| Generation speed | 6.32 t/s | Ramalama server |
| Generation time | 1,287,163 ms (~21.5 min) | Ramalama server |
| Total time | 1,288,015 ms | Ramalama server |
| Graphs reused | 10,137 / 8,135 tokens | Ramalama server |

## Benchmark Results — OLMo 3.1 32B Think Q4_K_M (AI MAX+ 395 GPU)

| Metric | Value | Source |
|---|---|---|
| Input tokens | 133 | Ramalama server |
| Output tokens | 6,741 | Ramalama server |
| Prompt eval speed | 140.51 t/s | Ramalama server |
| Prompt eval time | 947 ms | Ramalama server |
| Generation speed | 10.85 t/s | Ramalama server |
| Generation time | 621,190 ms (~10.4 min) | Ramalama server |
| Total time | 622,137 ms | Ramalama server |
| Graphs reused | 6,713 / 6,741 tokens | Ramalama server |

Model loaded in ~4 seconds (vs ~26 seconds for Q8_0).

Prompt: 500–1000 word technical essay on Transformer vs. State Space Model architectures (see `prompt.txt`). Benchmark run with `--rate-type synchronous`, 1 concurrent user.

## Head-to-Head Comparison (AI MAX+ 395 GPU)

| Metric | Q8_0 | Q4_K_M | Ratio |
|---|---|---|---|
| Prompt eval speed | 104.44 t/s | 140.51 t/s | Q4_K_M 35% faster |
| Generation speed | 6.32 t/s | 10.85 t/s | Q4_K_M 1.7x faster |
| Total time per request | 1,288,015 ms (~21.5 min) | 622,137 ms (~10.4 min) | Q4_K_M 2.1x faster |
| Output tokens | 8,135 | 6,741 | — |

### Architecture Speed Ceiling

Generation speed is bounded by memory bandwidth, not compute. At ~273 GB/s unified bandwidth:

| Quant | Weight data/token | Theoretical max | Actual | Efficiency |
|---|---|---|---|---|
| Q8_0 | ~32 GB | ~8.5 t/s | 6.32 t/s | 74% |
| Q4_K_M | ~16 GB | ~17.1 t/s | 10.85 t/s | 63% |

Q4_K_M's lower efficiency reflects the extra dequantization overhead of K-quants vs the simpler Q8 format.

## Model Architecture

| Property | Value |
|---|---|
| Architecture | Dense (all parameters active per token) |
| Parameters | 32B |
| Context window | 65,536 tokens |
| Thinking mode | Always on (see note above) |
| Multimodal | No (text only) |
| Inference backend | llama.cpp (via Ramalama / Vulkan) |

## Benchmark Scores (from model card)

| Benchmark | OLMo 3.1 32B Think | OLMo 3.1 32B Instruct |
|---|---|---|
| MATH | 96.2 | 93.4 |
| AIME 2025 | 78.1 | — |
| HumanEvalPlus | 91.5 | — |
| MMLU | 86.4 | 80.9 |
| GPQA Diamond | 57.5 | 48.6 |
| IFEval | 93.8 | 88.8 |

## What Makes This Model Truly Open

Unlike the other models in this benchmark (Gemma 4, Qwen3.6), OLMo 3.1 releases:

- **Weights** — Apache 2.0, no use restrictions
- **Training data** — Dolma 3 pretraining corpus (~9.3T tokens), publicly available
- **Post-training data** — Dolci suite including ~228K tool-use SFT examples
- **Training code, recipes, logs, and intermediate checkpoints** — all public
