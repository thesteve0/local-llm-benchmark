# Muse-Glimmer 30B Model

**HuggingFace (unsloth GGUF):** https://huggingface.co/unsloth/Muse-Glimmer-30B-GGUF

## Model Under Benchmark

Benchmarking one quantization from this family on a Framework Desktop with AMD Ryzen AI MAX+ 395 (96 GB GPU / 32 GB CPU unified memory):

| Model | Format | Size | Role |
|---|---|---|---|
| `unsloth/Muse-Glimmer-30B-GGUF` (UD-Q6_K_XL) | GGUF | ~24.4 GB | Quality run |

Muse-Glimmer is a **dense ~27.9B** model (not a mixture-of-experts), so every parameter is active per
token. It loads with chain-of-thought reasoning enabled and emits a reasoning trace before its answer.

### Serve Command

Served directly with llama.cpp (`llama serve`, port 8080 by default). The `:quant` tag selects the GGUF
file. This run used the bare command with llama.cpp defaults:

```bash
llama serve -hf unsloth/Muse-Glimmer-30B-GGUF:UD-Q6_K_XL
```

The server was **stopped and restarted cold before each of the three runs** (essay, Python bubble sort,
Java bubble sort) so every task hit a fresh, unwarmed server — matching how the model is used
agentically. The code-eval runs (`manual_code_eval.py`) send `temperature: 0.0` in the request body for
determinism; the essay run uses the server defaults.

## Benchmark Results — Muse-Glimmer 30B UD-Q6_K_XL (AI MAX+ 395 GPU)

Metrics from the llama.cpp `timings` object (captured by `manual_eval.py` into the run trace). Prompt:
500–1000 word technical essay on Transformer vs. State Space Model architectures, single concurrent
user. Server was restarted fresh (cold) before this run.

| Metric | Value | Source |
|---|---|---|
| Input tokens | 134 | llama.cpp server |
| Output tokens | 1,516 | llama.cpp server |
| Prompt eval speed | 158.28 t/s | llama.cpp server |
| Prompt eval time | 847 ms | llama.cpp server |
| Generation speed | 7.85 t/s | llama.cpp server |
| Generation time | 192,962 ms (~3.2 min) | llama.cpp server |
| Total time | 193,808 ms (~3.2 min) | llama.cpp server |

Generation speed (~7.9 t/s) is in line with the other dense 27–30B models on this hardware (e.g.
Qwen3.8-27B at ~8.5 t/s) and roughly 7× slower than the A3B MoE models (~52–54 t/s), reflecting that all
~27.9B parameters are active per token. The essay was comparatively terse (411 reasoning / 1,105 answer
tokens).

## Code Eval Results — Bubble Sort

`temperature: 0.0`; server restarted cold before each language. Test counts from the automated suites
(`run_tests.py`); quality scores from the rubric (`scorecard-claude.md`).

| Language | Tests | Quality | Gen speed | Reasoning / answer tokens |
|---|:---:|:---:|---:|---|
| Python | 11 / 11 | 21 / 25 | 7.11 t/s | 1,999 / 416 |
| Java   | 11 / 11 | 22 / 25 | 7.12 t/s | 1,188 / 441 |

Both implementations are correct against the full suite and idiomatic. The **Python** run centralizes
ordering in an `is_better` predicate but has a latent flaw: because that predicate is strict, the swap
condition `not is_better(a, b)` swaps *equal* elements (same priority and same `created_at`), inflating
the swap count and breaking stability — no test exercises exact-duplicate timestamps, so all 11 still
pass. The **Java** run avoids this by using a proper 3-way `compare` (returns `0` on ties) and adds a
clean `List.of()` null-input path, though its external Javadoc is thinner than the Python docstrings.
See each directory's `scorecard-claude.md` for the full rubric breakdown.

## Model Architecture

Values below are read from the llama.cpp `/v1/models` metadata for the served GGUF.

| Property | Value |
|---|---|
| Total parameters | ~27.9B (dense) |
| Quantization | Q6_K (~24.4 GB on disk) |
| Context window | 131,072 tokens (128K) |
| Embedding dim | 6,656 |
| Vocab size | 202,048 |
| Multimodal | Yes — server reports `multimodal` capability |
| Thinking mode | Enabled (emits reasoning before the answer) |
| Inference backend | llama.cpp (Vulkan) |
