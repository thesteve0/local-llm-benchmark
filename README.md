# Local LLM Benchmark

A tool for benchmarking local AI models for agentic coding use (single concurrent user). Models are served directly with llama.cpp; code quality is measured with prompt-based evals plus automated test suites and rubric scoring (see `evals/`).

## Setup

### Serve the model

```bash
llama serve -hf unsloth/gemma-4-26B-A4B-it-GGUF:Q8_0
```

`llama serve` listens on port 8080 by default, which matches the `HOST` configured in the eval scripts. Replace the `-hf` reference with whichever model you want to benchmark. The exact serve command for each model under evaluation is documented in its corresponding file under `models/`.

> **Note:** We previously served models with Ramalama over a shared Podman network. We dropped it — it only wrapped llama.cpp while adding container/network overhead and lagging behind upstream llama.cpp releases. Running `llama serve` directly is simpler and lets us run newer models.

## Running the evals

The benchmark is a manual code-eval workflow: prompt the model, run the generated code against a test suite, and score code quality against a rubric. See [`evals/README.md`](evals/README.md) for the full workflow.

Performance metrics (prompt eval speed, generation speed, token counts) come from the llama.cpp server — the `timings` object in the API response, which the eval scripts capture into each run's trace.

> **Deprecated:** An earlier approach used GuideLLM (in a container) for throughput/latency benchmarking. It was dropped because its client-side numbers were unreliable and because throughput is the wrong signal for agentic coding use (see `CLAUDE.md`). The legacy GuideLLM outputs remain under `results/`.
