# CLAUDE.md

We are running local AI models on our machines and want to have a way to benchmark them. We are specifically benchmarking for agentic use of the models so there will only be 1 concurrent user. 

We will only use Ramalama for model serving. Its documentation is here: https://ramalama.ai/docs/introduction. When you are going to give a Ramalama command you should ALWAYS read the documentation from the website first.

### Why we dropped GuideLLM

We originally planned to use GuideLLM (https://vllm-project.github.io/guidellm/stable/) as our benchmark tool, running it inside a container with `--rate-type synchronous` for single-user testing. We dropped it for two reasons:

1. **Unreliable client-side metrics.** GuideLLM's reported numbers were inflated and distorted by network overhead, streaming chunk counting, and cold-start queuing time. For example, client TTFT of 20s vs actual server prompt eval of 215ms, and client throughput of 77 t/s vs server's actual 43 t/s. The Ramalama (llama.cpp) server logs turned out to be far more accurate.

2. **Wrong kind of benchmark.** GuideLLM measures throughput and latency — useful for production serving, but our goal is benchmarking models for *agentic coding use*. What matters is whether the model produces correct, well-structured code, not how fast it streams tokens. We shifted to a manual code eval approach: give the model a coding prompt, run the output against a test suite, then score code quality against a rubric.

### Current approach

- **Model serving:** Ramalama
- **Performance metrics:** Ramalama server logs (prompt eval speed, generation speed, token counts)
- **Code quality evaluation:** Prompt-based evals with automated test suites + manual rubric scoring (see `evals/`)

## Memory

Project memory files are stored in `.claude/memory/`. Read `.claude/memory/MEMORY.md` at the start of each session to load portable context (user preferences, feedback, project decisions). When saving new memories, write to this in-repo directory instead of the default auto-memory location, except for machine-specific facts (hardware specs, local paths) which should stay in the per-machine auto-memory at `~/.claude/projects/`.

## Project Status

We are just getting started