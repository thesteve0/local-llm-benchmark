---
name: llama-cpp-serving
description: Models are served directly with llama.cpp (`llama serve -hf`); Ramalama was dropped
metadata:
  type: project
---

We serve benchmark models directly with llama.cpp using `llama serve -hf <hf-org>/<hf-repo>:<quant-tag>` (e.g. `llama serve -hf unsloth/Qwen3.8-27B-GGUF:UD-Q8_K_XL`). It listens on port 8080 by default, which matches the `HOST` in `manual_eval.py` and `manual_code_eval.py`. No Podman network or container is involved.

**Why:** We originally used Ramalama, but it only wrapped llama.cpp while adding container/network overhead and lagged behind upstream llama.cpp releases (blocking newer models). Running `llama serve` directly is simpler and keeps us on current llama.cpp.

**How to apply:** When giving serve commands or writing model docs, use `llama serve -hf …` (not `ramalama serve …`, no `--network llm-bench`). Pull benchmark metrics from the llama.cpp `timings` object (see [[feedback-metrics-source]]). Historical `models/*.md` result tables keep their `Source: Ramalama server` labels because those numbers were genuinely measured under Ramalama at the time.
