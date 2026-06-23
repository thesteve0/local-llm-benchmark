# Local LLM Benchmark

A tool for benchmarking local AI models for agentic use cases, using Ramalama for model serving and GuideLLM for benchmarking (single concurrent user).

## Setup

### Step 1: Create a shared Podman network

```bash
podman network create llm-bench
```

### Step 2: Serve the model

```bash
ramalama serve \
  --name llm-server \
  --port 8081 \
  --network llm-bench \
  hf.co/unsloth/gemma-4-26B-A4B-it-GGUF:Q8_0
```

The container runs detached by default. Replace the model path with whichever model you want to benchmark. The exact Ramalama serve command for each model under evaluation is documented in its corresponding file under `models/`.

### Step 3: Run the benchmark

Results are written to a local `results/` directory. Mount `prompt.txt` into the container and reference it with `--data` so GuideLLM uses your single prompt for every request.

```bash
mkdir -p results

podman run \
  --rm -it \
  --network llm-bench \
  -v "./results:/results:rw,Z" \
  -v "./prompt.txt:/prompt.txt:ro,Z" \
  ghcr.io/vllm-project/guidellm:latest \
  benchmark run \
  --target http://llm-server:8081 \
  --data /prompt.txt \
  --max-requests 10 \
  --rate-type synchronous \
  --output-dir /results/ \
  --outputs result.html,result.json,result.csv
```
