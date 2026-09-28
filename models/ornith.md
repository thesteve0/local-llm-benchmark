# Ornith-1.5-35B-A3B Model

**HuggingFace (base model):** https://huggingface.co/ornith-ai/Ornith-1.5-35B-A3B
**HuggingFace (unsloth-style GGUF quant):** https://huggingface.co/peculiar-ragdoll/Unsloth-Ornith-1.5-35B-A3B

## Model Under Benchmark

Benchmarking one quantization from this family on a Framework Desktop with AMD Ryzen AI MAX+ 395
(96 GB GPU / 32 GB CPU unified memory):

| Model | Format | Size | Role |
|---|---|---:|---|
| `peculiar-ragdoll/Unsloth-Ornith-1.5-35B-A3B` (UD-Q8_K_XL) | GGUF | ~38.5 GB (38,440,192,512 bytes) | Quality run |

Ornith-1.5-35B-A3B is a **Qwen35MoE** architecture — 35B total parameters with only ~3B active per
token — making it architecturally the closest peer to Qwen3.6-35B-A3B in this benchmark set. It
loads with chain-of-thought reasoning enabled (`<think>` block, served as `reasoning_content`) and
emits a reasoning trace before every answer.

### MTP note

The user asked whether MTP (multi-token prediction / speculative self-decoding) should be enabled
for this run on the AMD hardware. The `peculiar-ragdoll/Unsloth-Ornith-1.5-35B-A3B` model card
states the MTP (`nextn`) block was **stripped from every quantization tier, including UD-Q8_K_XL**,
because Ornith-1.5 ships it untrained ("could only add size" — uninitialized weights, no functional
benefit, ~0.3–0.9 GB saved per tier). There are no MTP weights present in this GGUF to enable, and
no MTP/speculative-decoding flag is documented for it, so this run used the bare serve command with
no MTP-related flags.

### Serve Command

Served directly with llama.cpp (`llama serve`, port 8080 by default), bare command with llama.cpp
defaults — no extra flags:

```bash
llama serve -hf peculiar-ragdoll/Unsloth-Ornith-1.5-35B-A3B:UD-Q8_K_XL
```

The server was **stopped and restarted cold before each of the four runs** (essay, Python, Java,
Rust bubble sort) so every task hit a fresh, unwarmed server — matching how the model is used
agentically. The code-eval runs (`manual_code_eval.py`) send `temperature: 0.0` in the request body
for determinism; the essay run uses the server defaults.

`/v1/models` reported: 34,660,610,688 parameters, 262,144-token context (native, no YaRN needed for
these prompt lengths), embedding dim 2,048, vocab size 248,320, `ftype: Q8_0`.

## Benchmark Results — Ornith-1.5-35B-A3B UD-Q8_K_XL (AI MAX+ 395 GPU)

Metrics from the llama.cpp `timings` object. Test counts from `run_tests.py` (Python/Java) and a
manual `cargo test` run in Docker (Rust — `run_tests.py` doesn't support Rust, a documented
limitation). Quality scores from the rubric (`evals/bubble-sort/rubric.md`,
`evals/essay/rubric.md`); see each directory's `scorecard-claude.md` for the full breakdown.

| Task | Tests / words | Quality | Prompt t/s | Generation t/s | Completion tokens |
|---|---:|---:|---:|---:|---:|
| Essay | 808 words | 23 / 25 | 139.25 | 45.77 | 1,731 |
| Python bubble sort | 11 / 11 tests | **25 / 25** | 599.01 | 45.12 | 5,720 |
| Java bubble sort | 11 / 11 tests | 24 / 25 | 597.39 | 45.09 | 5,825 |
| Rust bubble sort | 11 / 11 tests | **25 / 25** | 594.76 | 44.27 | 13,336 |

Generation speed is remarkably stable across all four tasks (44.3–45.8 t/s) — consistent with the
MoE architecture's ~3B active parameters per token, in the same performance class as Qwen3.6-35B-A3B
(~51–53 t/s) and Nemotron-3.5-Lightning-30B-A3B (~47–54 t/s) rather than the dense 27–30B models
(~7–8.5 t/s).

- **Essay (23/25):** technically accurate and fully in range (808 words), but presents Mamba's
  selectivity as resolving older SSMs' long-range weakness without flagging the fixed-state
  retrieval/compression limitation the top essays raise (Depth 4/5), and is written as seven
  markdown-headed sections rather than flowing essay prose (Structure/Tone 4/5).
- **Python (25/25):** a clean, fully idiomatic run — the `_should_swap` predicate uses strict
  inequalities throughout, so exact ties (same priority **and** `created_at`) are correctly left
  unswapped, avoiding the stability bug found in the Muse-Glimmer Python run.
- **Java (24/25):** proper `record`-based `Task`/`SortResult` types with a correct 3-way
  `Integer.compare`/`Long.compare` comparator (avoiding the boxed-`Integer` pitfall seen in the
  Nemotron Java runs). The only deduction is an unrequested demo `main` method — the same
  deduction applied to the Nemotron BF16 Java run for the same reason.
- **Rust (25/25):** the first Rust run in this benchmark set to receive a quality score (prior Rust
  runs were only ever test-checked). Fully idiomatic `Option` pattern matching centralizes every
  ordering rule, and the crate ships a working doc-test example. One tooling caveat: the
  `manual_code_eval.py` extraction script concatenates every fenced code block in a response, and
  this response included an illustrative `Cargo.toml` snippet and a closing usage note as separate
  blocks alongside the real `lib.rs`, corrupting the saved file. The `lib.rs` was manually corrected
  from the trace before testing/scoring — see `evals/bubble-sort/rust/ornith-1.5-35b-a3b-q8/scorecard-claude.md`
  for detail. This is a bug in the eval tooling, not a defect in the model's output.

## Model Architecture

| Property | Value |
|---|---|
| Architecture | Qwen35MoE (Mixture of Experts) |
| Total parameters | ~34.66B |
| Active parameters per token | ~3B |
| Context window | 262,144 tokens native (YaRN-extendable to ~1M) |
| Embedding dim | 2,048 |
| Vocab size | 248,320 |
| Thinking mode | Enabled (`<think>` block, served as `reasoning_content`) |
| MTP (multi-token prediction) | Not present in any GGUF quant tier — stripped as untrained |
| Inference backend | llama.cpp |
