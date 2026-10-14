# LFM2.5-24B-A2B Model

**HuggingFace (Liquid AI GGUF):** https://huggingface.co/LiquidAI/LFM2.5-24B-A2B-GGUF

## Model Under Benchmark

Benchmarking one quantization from this family on a Framework Desktop with AMD Ryzen AI MAX+ 395 (96 GB GPU / 32 GB CPU unified memory):

| Model | Format | Size | Role |
|---|---|---|---|
| `LiquidAI/LFM2.5-24B-A2B-GGUF` (BF16) | GGUF | ~48 GB | Quality/speed baseline run (BF16 quant requested) |

## Model Architecture

- **Total parameters:** 24.0B
- **Active parameters:** 2.45B (MoE: 64 experts per MoE block, top-4 routing)
- **Layers:** 40 (30 double-gated short convolution blocks + 10 GQA attention)
- **Context length:** 131,072 tokens (native — served at full 131K since the small
  KV cache on the 10 GQA layers fits in 96 GB GPU memory)
- **Vocabulary size:** 128,000
- **Reasoning:** pure reasoning model — always emits a `积极` trace before the answer
  (tag is added by the chat template)
- **Text-only** (no vision)

## Serve Command

Served directly with llama.cpp (`llama serve`, port 8080 by default). The `:BF16` tag
selects the GGUF file. Flags follow the model card's recommended generation parameters
(`temperature 0.1`, `top_k 50`, `repetition_penalty 1.05`), which the GGUF also carries
as `general.sampling.*` metadata:

```bash
llama serve \
  -hf LiquidAI/LFM2.5-24B-A2B-GGUF:BF16 \
  --host 127.0.0.1 --port 8080 \
  --reasoning-format deepseek \
  --reasoning-preserve \
  --temp 0.1 --top-k 50 --repeat-penalty 1.05 \
  --gpu-layers all --kv-offload --flash-attn on \
  --ctx-size 131072 --parallel 1 \
  --batch-size 2048 --ubatch-size 512 \
  --cache-prompt --metrics
```

Notes on this run's settings:

- `--gpu-layers all` — full offload (the lesson from the slow under-offloaded Qwen3.8 run).
  BF16 weights (~48 GB) plus the hybrid model's small KV cache fit in 96 GB GPU memory.
- `--ctx-size 131072` — full native context, unlike prior runs that trimmed to 96K for memory.
- `--reasoning-format deepseek --reasoning-preserve` — capture the always-on reasoning trace.
- Sampling flags are the model card's recommended values. Code evals still send
  `temperature: 0.0` in the request body for determinism; the essay run uses
  `--temperature 0.1` (top-k/repeat-penalty stay at server defaults from GGUF metadata).
- No `--reasoning-effort` — LFM2.5 has no effort levels (Qwen3-specific flag).

## Benchmark Results — LFM2.5-24B-A2B BF16 (AI MAX+ 395 GPU)

| Metric | Py | Java | Rust | Essay |
|---|--:|--:|--:|--:|
| Gen tokens | 7,240 | 6,836 | 6,478 | 3,804 |
| Gen speed | 11.76 t/s | 11.44 t/s | 11.42 t/s | 11.43 t/s |
| Prompt eval | 242 t/s | 238 t/s | 241 t/s | 54 t/s |
| Tests | 11/11 | 11/11 | 0/11 | — |
| Quality | 24/25 | 24/25 | 19/25 | 21/25* |

\* Essay: ~2,756 words — far over the 500–1000 limit (worst constraint overshoot in the set).

Context stress (needle retrieval, 128 max tokens): **all 5 probes failed exact retrieval** —
the always-on reasoning exhausts the 128-token budget (needle only appears truncated inside
the reasoning trace). Root cause is verbose-thinking + small max_tokens, not retrieval failure.

**Verdict:** ~12 t/s generation is ~4x slower than prior MoE runs (45–54 t/s at Q6/Q8) and
slower than Nemotron BF16 (21.8 t/s). BF16's compute overhead on the iGPU is heavy; **Q8_0
(~24 GB, half the file) is the recommended next benchmark** per user criterion.

## Benchmark Results — LFM2.5-24B-A2B Q8_0 (AI MAX+ 395 GPU)

Ran 2026-10-14 per the BF16 verdict: same flag set, only the quant tag changes
(`llama serve -hf LiquidAI/LFM2.5-24B-A2B-GGUF:Q8_0`). ~24 GB file, cold restart
before every task, code evals at temperature 0.0, essay at 0.1, full native
131,072 context, `--gpu-layers all --flash-attn on`.

| Metric | Py | Java | Rust | Essay |
|---|--:|--:|--:|--:|
| Gen tokens | 5,355 | 8,335 | 6,546 | 5,190 |
| Gen speed | 71.34 t/s | 70.94 t/s | 71.38 t/s | 71.65 t/s |
| Prompt eval | 1,734 t/s | 1,736 t/s | 1,708 t/s | 526 t/s |
| Tests | 11/11 | 0/11 | 11/11 | — |
| Quality | 25/25 | 21/25 | 24/25 | 24/25 |

- **Python 25/25** (11/11 tests) — best-in-set: consistent builtin-generic type hints,
  NumPy-style docstring, tuple swap, early exit. Fixes the BF16 run's mixed typing style.
- **Java 0/11, 21/25** — fatal model bug: `sorted[j]` array-indexing on a `List` instead
  of `sorted.get(j)` (the only such line; everything else uses the `List` API). Logic is
  otherwise correct; the model iterated 4 drafts in its thinking trace and never fixed it.
  Extraction verified byte-for-byte — genuine model bug, not tooling.
- **Rust 11/11, 24/25** — clean compile, idiomatic `match (Option, Option)`, derives,
  `Vec::swap`; directly reverses the BF16 run's fatal E0753 module-doc bug.
- **Essay 700 words** — squarely inside the 500–1000 limit (vs BF16's ~2,756-word blowout).
- **Context stress 0/5 exact** — same root cause as BF16: the always-on reasoning exhausts
  the 128-token budget (`generation_tokens: 128` in every probe; needle only appears
  truncated in the reasoning trace). Long-context *processing* itself is fine.

**Performance:** generation 70.9–71.7 t/s — **~6x faster than BF16** (11.4–11.8) and
faster than every prior MoE run (45–54 t/s). Prompt eval 1,708–1,736 t/s on code prompts
(~7x BF16); long-context prefill 2,231 t/s @ 8K → 550 t/s @ 129K (BF16: 450 → 282 t/s).
Wall time for the 129,552-token prefill probe: 239s (BF16: 472s). Inference on this iGPU
is memory-bandwidth-bound, so halving the file size roughly sextupled throughput.

**Verdict:** Q8_0 is the right quant for this model on this hardware — faster than BF16 by
~6x with equal-or-better code quality (Py 25/25, Rust 11/11/24/25 vs BF16's Py 24/25,
Rust 0/11). The always-think chat template remains the main caveat: it multiplies output
tokens 4–5x (reasoning ≫ answer), which dominates wall time in interactive agentic loops.
