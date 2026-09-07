# NVIDIA Nemotron 3.5 Lightning 30B-A3B Model

**HuggingFace (unsloth GGUF):** https://huggingface.co/unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF

## Models Under Benchmark

Benchmarking two quantizations from this family on a Framework Desktop with AMD Ryzen AI MAX+ 395 (96 GB GPU / 32 GB CPU unified memory):

| Model | Format | Size | Role |
|---|---|---|---|
| `unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF` (UD-Q6_K_XL) | GGUF | ~32.6 GB | Quality run (Q6) |
| `unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF` (UD-Q8_K_XL) | GGUF | ~36.0 GB | Quality run (Q8) |

Nemotron-3.5-Lightning is a **mixture-of-experts** model — "A3B" means ~3B parameters are active per
token out of ~32.9B total — so it generates far faster than a dense model of comparable size. It loads
with chain-of-thought reasoning enabled and emits a reasoning trace before its answer.

### Serve Command

Served directly with llama.cpp (`llama serve`, port 8080 by default). The `:quant` tag selects the GGUF
file. These runs used the bare command with llama.cpp defaults:

```bash
# Q6
llama serve -hf unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF:UD-Q6_K_XL
# Q8
llama serve -hf unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF:UD-Q8_K_XL
```

The server was **stopped and restarted cold before each of the three runs** (essay, Python bubble sort,
Java bubble sort) so every task hit a fresh, unwarmed server — matching how the model is used
agentically. The code-eval runs (`manual_code_eval.py`) send `temperature: 0.0` in the request body for
determinism; the essay run uses the server defaults.

## Benchmark Results — Essay (AI MAX+ 395 GPU)

Metrics from the llama.cpp `timings` object (captured by `manual_eval.py`). Prompt: 500–1000 word
technical essay on Transformer vs. State Space Model architectures, single concurrent user. Server
restarted fresh (cold) before each run.

| Metric | Q6_K_XL | Q8_K_XL | Source |
|---|---|---|---|
| Input tokens | 99 | 99 | llama.cpp server |
| Output tokens | 3,109 | 3,107 | llama.cpp server |
| Prompt eval speed | 128.22 t/s | 120.54 t/s | llama.cpp server |
| Prompt eval time | 772 ms | 821 ms | llama.cpp server |
| Generation speed | 54.50 t/s | 47.36 t/s | llama.cpp server |
| Generation time | 57,032 ms (~57 s) | 65,581 ms (~66 s) | llama.cpp server |
| Total time | 57,804 ms (~58 s) | 66,402 ms (~66 s) | llama.cpp server |

Both quants generate at MoE speed — roughly 7× the dense 27–30B models on this hardware (Qwen3.8-27B
~8.5 t/s, Muse-Glimmer-30B ~7.9 t/s) — because only ~3B of the ~32.9B parameters are active per token.
Q8 is ~13% slower than Q6 (47 vs 55 t/s), the expected cost of the heavier quant.

## Code Eval Results — Bubble Sort

`temperature: 0.0`; server restarted cold before each language. Test counts from the automated suites
(`run_tests.py`); quality scores from the rubric (`scorecard-claude.md`). Q6 artifacts live in the
`*-q6` directories, Q8 in the `*-q8` directories.

| Quant | Language | Tests | Quality | Gen speed | Reasoning / answer tokens |
|---|---|:---:|:---:|---:|---|
| Q6 | Python | **0 / 11** | 19 / 25 † | 54.38 t/s | 3,612 / 940 |
| Q6 | Java   | 11 / 11 | 24 / 25 | 54.32 t/s | 3,214 / 1,174 |
| Q8 | Python | **0 / 11** | 17 / 25 † | 47.19 t/s | 3,814 / 1,071 |
| Q8 | Java   | 11 / 11 | 21 / 25 | 47.22 t/s | 3,735 / 997 |

### Q6 vs Q8 tradeoffs

- **Speed:** Q6 is ~15% faster on generation (~54 vs ~47 t/s) across all tasks. Q8 buys no accuracy
  here to offset that cost — see below.
- **Python fails at BOTH quants (0/11).** Both runs emit the invalid line
  `from typing import list, dict, tuple` (those lowercase names aren't in `typing`, and the import is
  redundant under PEP 585), so the module raises `ImportError` before any test runs. † The 17–19/25
  quality scores reflect otherwise-sound code (the algorithms, including the equal-`created_at`
  tiebreak, are correct), but the identical failure at both quants makes this look like a **model trait,
  not a quantization artifact**.
- **Java passes at both quants, but Q6 is cleaner.** Q6 Java (24/25) is the strongest run in the whole
  benchmark set. Q8 Java (21/25) passes all 11 tests too, but carries a **latent correctness bug**: it
  compares nullable priorities with `!=` (reference equality on boxed `Integer`), so two equal
  priorities ≥ 128 (outside the Integer cache) would skip the `createdAt` tiebreaker and mis-order — the
  test suite misses it because it only uses small priorities. Q8 Java also drops the null-input guard
  the Q6 version had.

**Bottom line:** for this model on this hardware, **Q6 is the better pick** — it is faster *and* produced
higher-quality, more correct code than Q8. Q8's extra bits didn't fix the Python import failure and, in
the Java run, coincided with a latent `Integer`-reference bug the Q6 run avoided. See each directory's
`scorecard-claude.md` for the full rubric breakdown.

## Model Architecture

Values below are read from the llama.cpp `/v1/models` metadata for the served GGUFs.

| Property | Q6_K_XL | Q8_K_XL |
|---|---|---|
| Total parameters | ~32.9B (MoE, ~3B active per token) | ~32.9B (MoE, ~3B active per token) |
| Quantization (ftype) | Q6_K (~32.6 GB on disk) | Q8_0 (~36.0 GB on disk) |
| Context window | 1,048,576 tokens (1M) | 1,048,576 tokens (1M) |
| Embedding dim | 2,688 | 2,688 |
| Vocab size | 131,072 | 131,072 |
| Multimodal | No — server reports only `completion` | No — server reports only `completion` |
| Thinking mode | Enabled (emits reasoning before the answer) | Enabled |
| Inference backend | llama.cpp (Vulkan) | llama.cpp (Vulkan) |
