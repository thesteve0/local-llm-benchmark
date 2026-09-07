# Qwen3.6 35B-A3B Model Series

**HuggingFace (unsloth GGUF):** https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF

## Models Under Benchmark

We are benchmarking two quantizations from this family on a Framework Desktop with AMD Ryzen AI MAX+ 395 (96 GB GPU / 32 GB CPU unified memory):

| Model | Format | Size | Role |
|---|---|---|---|
| `unsloth/Qwen3.6-35B-A3B-GGUF` (Q8_0) | GGUF, MoE | 36.9 GB | Quality baseline |
| `unsloth/Qwen3.6-35B-A3B-GGUF` (UD-Q4_K_M) | GGUF, MoE | 22.1 GB | Efficiency target |

Both models load with `thinking = 1` (chain-of-thought reasoning enabled). The MoE architecture activates only ~3B parameters per forward pass despite 35B total weights in memory.

### Serve Commands

Served directly with llama.cpp (`llama serve`, port 8080 by default). The `:quant` tag selects the GGUF file.

**Q8_0 (quality baseline):**
```bash
llama serve -hf unsloth/Qwen3.6-35B-A3B-GGUF:Q8_0
```

**UD-Q4_K_M (efficiency target):**
```bash
llama serve -hf unsloth/Qwen3.6-35B-A3B-GGUF:UD-Q4_K_M
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

## Full Benchmark Set — llama.cpp Q6 vs Q8 (AI MAX+ 395 GPU)

The results above are the original **Ramalama-era essay-throughput** numbers (Q8_0 and Q4_K_M),
preserved for history. The section below is a fresh, apples-to-apples benchmark under the **current
methodology**: served directly with `llama serve` (one concurrent user), `temperature: 0.0` for the code
evals, and the **server stopped and restarted cold before every task**. Quants compared here:
**UD-Q6_K_XL** and **Q8_0**. All metrics are from the llama.cpp `timings` object.

### Serve commands (this run)

```bash
# Q6
llama serve -hf unsloth/Qwen3.6-35B-A3B-GGUF:UD-Q6_K_XL
# Q8
llama serve -hf unsloth/Qwen3.6-35B-A3B-GGUF:Q8_0
```

### Essay (Transformer vs. Mamba)

| Metric | Q6 (UD-Q6_K_XL) | Q8 (Q8_0) | Source |
|---|---|---|---|
| Input tokens | 91 | 91 | llama.cpp server |
| Output tokens | 3,182 | 4,815 | llama.cpp server |
| Prompt eval speed | 167.53 t/s | 174.85 t/s | llama.cpp server |
| Prompt eval time | 543 ms | 520 ms | llama.cpp server |
| Generation speed | 53.33 t/s | 51.41 t/s | llama.cpp server |
| Generation time | 59,649 ms (~60 s) | 93,631 ms (~94 s) | llama.cpp server |
| Total time | 60,192 ms (~60 s) | 94,151 ms (~94 s) | llama.cpp server |

(The Q8 essay ran longer only because the model chose to emit a longer reasoning trace — 4,815 vs 3,182
tokens — not because it is materially slower per token.)

### Code eval — bubble sort

`temperature: 0.0`; server restarted cold before each language. Test counts from `run_tests.py`; quality
scores from the rubric (`scorecard-claude.md`). Q6 artifacts live in the `*-q6` directories, Q8 in `*-q8`.

| Quant | Language | Tests | Quality | Gen speed | Reasoning / answer tokens |
|---|---|:---:|:---:|---:|---|
| Q6 | Python | 11 / 11 | 24 / 25 | 52.72 t/s | 4,691 / 783 |
| Q6 | Java   | 11 / 11 | 23 / 25 | 52.66 t/s | 5,331 / 765 |
| Q8 | Python | 11 / 11 | 24 / 25 | 51.21 t/s | 4,235 / 727 |
| Q8 | Java   | 11 / 11 | **25 / 25** | 51.13 t/s | 4,798 / 998 |

### Q6 vs Q8 tradeoffs

- **Speed:** Q6 is marginally faster on generation (~53 vs ~51 t/s) — a ~3% edge, much smaller than the
  ~15% Q6→Q8 gap seen on Nemotron. Both are MoE-fast (~7× the dense 27–30B models).
- **Correctness:** unlike Nemotron, **every** Qwen3.6 run passes (4/4 code runs at 11/11). No import
  failures, no boxed-`Integer` `!=` bug.
- **Quality:** essentially a wash on Python (24/25 both). On Java, **Q8 edges Q6**: the Q8 Java run is a
  clean **25/25** (proper 3-way `Integer.compare` comparator, `n-i-1` reducing bound, documented
  null/empty handling — the strongest run in the whole set), while Q6 Java (23/25) used a `do/while`
  that re-scans the full range each pass and left null input unguarded.

**Bottom line:** Qwen3.6 is the most *reliable* model benchmarked here — both quants produce correct,
idiomatic code across Python and Java. Q6 is a hair faster; Q8 produced the single best code artifact.
Either is a safe pick; Q6 for a slight speed/size edge, Q8 if you want the top-quality ceiling.

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
