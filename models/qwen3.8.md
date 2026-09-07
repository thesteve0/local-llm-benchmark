# Qwen3.8 27B Model

**HuggingFace (unsloth GGUF):** https://huggingface.co/unsloth/Qwen3.8-27B-GGUF

## Model Under Benchmark

Benchmarking one quantization from this family on a Framework Desktop with AMD Ryzen AI MAX+ 395 (96 GB GPU / 32 GB CPU unified memory):

| Model | Format | Size | Role |
|---|---|---|---|
| `unsloth/Qwen3.8-27B-GGUF` (UD-Q6_K_XL) | GGUF | ~25.3 GB | Quality run |

The model loads with chain-of-thought reasoning enabled and produces a substantial reasoning trace before its answer.

### Serve Command

Served directly with llama.cpp (`llama serve`, port 8080 by default). The `:quant` tag selects the GGUF file.

```bash
llama serve \
  -hf unsloth/Qwen3.8-27B-GGUF:UD-Q6_K_XL \
  --host 127.0.0.1 --port 8080 \
  --reasoning-format deepseek \
  --reasoning-effort xhigh \
  --reasoning-preserve \
  --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0 \
  --presence-penalty 0.0 --repeat-penalty 1.0 \
  --gpu-layers all --kv-offload --flash-attn on \
  --ctx-size 98304 --parallel 1 \
  --batch-size 2048 --ubatch-size 512 \
  --cache-prompt --metrics
```

Notes on this run's settings:

- `--gpu-layers all` offloads every layer to the GPU (the fix for the prior ~7 t/s run, which was
  under-offloaded), with `--kv-offload` and `--flash-attn on` for the KV cache.
- `--ctx-size 98304` (96K) trims the 256K train context to fit memory alongside full GPU offload.
- The sampling flags (`--temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0`) are Qwen3's recommended
  thinking-mode values. Note the code-eval runs (`manual_code_eval.py`) send `temperature: 0.0` in the
  request body for determinism, which overrides the server `--temp` for those two runs; the essay run
  uses the server defaults.

## Benchmark Results — Qwen3.8 27B UD-Q6_K_XL (AI MAX+ 395 GPU)

Metrics from the llama.cpp `timings` object (captured by `manual_eval.py` into the run trace). Prompt: 500–1000 word technical essay on Transformer vs. State Space Model architectures (see `prompt.txt`), single concurrent user. Server was restarted fresh (cold) before this run.

| Metric | Value | Source |
|---|---|---|
| Input tokens | 133 | llama.cpp server |
| Output tokens | 5,243 | llama.cpp server |
| Prompt eval speed | 56.86 t/s | llama.cpp server |
| Prompt eval time | 2,339 ms | llama.cpp server |
| Generation speed | 8.45 t/s | llama.cpp server |
| Generation time | 620,363 ms (~10.3 min) | llama.cpp server |
| Total time | 622,702 ms (~10.4 min) | llama.cpp server |

Generation speed (~8.5 t/s) is markedly slower than the MoE models previously benchmarked on this
hardware (e.g. Qwen3.6-35B-A3B at ~52 t/s), reflecting that far more parameters are active per token in
this dense 27B model. The 5,243-token output includes a long reasoning trace (~3,810 reasoning tokens
vs ~1,433 answer tokens by character split).

## Model Architecture

Values below are read from the llama.cpp `/v1/models` metadata for the served GGUF.

| Property | Value |
|---|---|
| Total parameters | ~27.3B |
| Quantization | Q6_K (~25.3 GB on disk) |
| Context window | 262,144 tokens (256K) |
| Embedding dim | 5,120 |
| Vocab size | 248,320 |
| Multimodal | Yes — server reports `multimodal` capability |
| Thinking mode | Enabled (emits reasoning before the answer) |
| Inference backend | llama.cpp (Vulkan) |
