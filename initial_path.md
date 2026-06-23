# Benchmark Path — Phase 2: Quality Evaluation

## Where We Are

Phase 1 (speed benchmarking) is complete. We benchmarked five model families for throughput and latency on a Framework Desktop with AMD Ryzen AI MAX+ 395 (96 GB GPU unified memory). OLMo 3.1 32B was eliminated due to unacceptably slow generation speed (~6–11 t/s, 10–21 minutes per request). Gemma 4 had a system crash during the 26B run and weak numbers for the 31B dense variant.

Two model families advanced based on speed:

| Model | Quant | Generation Speed |
|---|---|---|
| Qwen3.6 35B-A3B | Q8_0 | 51.76 t/s |
| Qwen3.6 35B-A3B | UD-Q4_K_M | 59.49 t/s |
| Mellum2 12B-A2.5B | Q8_0 | 81.19 t/s |
| Mellum2 12B-A2.5B | Q6_K | 92.89 t/s |

All four models use thinking/reasoning (`<think>` blocks enabled) and fit comfortably within the 96 GB GPU memory pool.

## Phase 2: Quality Evaluation

The next step is to evaluate output quality across these four models for agentic use cases. Specific tasks and evaluation dimensions are to be determined.

### Key Questions to Answer

- Does Mellum2's speed advantage come at a meaningful quality cost for agentic tasks?
- Is the quality difference between Q8_0 and the smaller quant (Q4_K_M / Q6_K) within each family noticeable in practice?
- Which model produces the best quality-per-second for a single agentic user?

### Models Under Evaluation

| Model | Quant | Size | Notes |
|---|---|---|---|
| Qwen3.6 35B-A3B | Q8_0 | 36.9 GB | Effectively lossless quality baseline |
| Qwen3.6 35B-A3B | UD-Q4_K_M | 22.1 GB | 15% faster generation than Q8_0 |
| Mellum2 12B-A2.5B | Q8_0 | 12.9 GB | Purpose-built for agentic workflows |
| Mellum2 12B-A2.5B | Q6_K | 10.9 GB | Fastest model tested (92.89 t/s) |
