# NVIDIA Nemotron 3.5 Lightning 30B-A3B Model

**HuggingFace (unsloth GGUF):** https://huggingface.co/unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF

## Models Under Benchmark

| Model | Format | Size | Role |
|---|---|---:|---|
| `unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF` (UD-Q6_K_XL) | GGUF | ~32.6 GB | Existing quality run |
| `unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF` (UD-Q8_K_XL) | GGUF | ~36.0 GB | Existing quality run |
| `unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF` (BF16) | GGUF | ~65.8 GB | New full-precision-weight run |

All tests were run on a Framework Desktop with AMD Ryzen AI MAX+ 395 and 128 GB unified memory (96 GB GPU / 32 GB CPU), using one concurrent user and llama.cpp 0.4.0 (build 10809, commit 5266f24da). The server was stopped and cold-restarted before every quality or context test.

## BF16 Serve Command

```bash
llama serve \
  -hf unsloth/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-GGUF:BF16 \
  --alias nemotron-3.5-lightning-30b-a3b \
  --host 127.0.0.1 --port 8080 \
  --jinja \
  --reasoning-format deepseek \
  --temp 1.0 --top-p 0.95 \
  --gpu-layers all --kv-offload --flash-attn auto \
  --ctx-size 131072 --parallel 1 \
  --batch-size 2048 --ubatch-size 512 \
  --cache-prompt --metrics
```

The effective serving context was 131,072 tokens; `/v1/models` reported a 1,048,576-token training context, 32,913,266,240 parameters, 65,844,287,744-byte model size, and `ftype: BF16`. The server reported `completion` capability and correctly loaded the `nemotron-3.5-lightning-30b-a3b` alias.

## BF16 Results — Quality Evaluation

Primary quality protocol: one cold server run per task, `temperature: 0.0` in the client request. Performance values come from the llama.cpp `timings` object.

| Task | Tests / words | Quality | Prompt t/s | Generation t/s | Completion tokens |
|---|---:|---:|---:|---:|---:|
| Essay | 1,050 words | 21 / 25 | 73.53 | 21.80 | 3,447 |
| Python bubble sort | 11 / 11 tests | **25 / 25** | 320.36 | 21.81 | 3,713 |
| Java bubble sort | 11 / 11 tests | **24 / 25** | 324.67 | 21.79 | 4,625 |

The essay was technically strong and covered attention, sequence complexity, long-context trade-offs, selective scan, retrieval/compression limitations, and hybrid directions. It exceeded the strict `<1000` word limit at 1,050 words, so it received 1 point for constraint adherence and 21/25 overall. The BF16 Python output was clean and fully idiomatic; the Java output was also excellent, with only minor deductions for relational operators on boxed priorities and an unnecessary demo `main`.

Compared with the existing Q6/Q8 results, BF16 did not improve the hard instruction-following issue in the essay, and generation speed fell from approximately 54.5/47.4 t/s to 21.8 t/s. It did, however, avoid the Q6/Q8 Python import failure and produced code quality comparable to or better than the prior Java runs.

## BF16 Context Stress Test

The context probe placed a known marker around the latter part of a calibrated prompt and requested a short exact response. Each point was cold-started. The effective prompt lengths were approximately 5.4K, 22.1K, 44.4K, 66.7K, and 88.9K tokens for the requested 8K, 32K, 64K, 96K, and 128K targets in the initial sweep. A corrected calibrated 8K probe reached 7.9K actual tokens. The initial conversion was conservative and did not reach 128K actual tokens; these values should therefore be interpreted as a scaling probe, not a full 128K validation.

| Requested target | Actual prompt tokens | Prompt eval | Generation | Result |
|---:|---:|---:|---:|---|
| 8K | 5,432 (7,928 corrected) | 677.27 t/s (723.09 corrected) | 21.82 t/s (21.75 corrected) | Request completed; response was reasoning-truncated |
| 32K | 22,124 | 769.38 t/s | 21.50 t/s | Request completed; response was reasoning-truncated |
| 64K | 44,406 | 739.61 t/s | 21.24 t/s | Request completed; response was reasoning-truncated |
| 96K | 66,688 | 693.43 t/s | 20.93 t/s | Request completed; response was reasoning-truncated |
| 128K | 88,944 | 647.97 t/s | 20.55 t/s | Request completed; response was reasoning-truncated |

A corrected calibrated 8K probe reached 7,928 prompt tokens and also completed, at 723.09 prompt t/s and 21.75 generation t/s. The model spent the 128-token completion budget in reasoning and did not emit the exact final needle, so these runs validate context acceptance and scaling but **not retrieval quality**. The context tool retains both `reasoning_content` and `content`; future retrieval validation should either disable reasoning for this probe or allocate a larger completion budget.

## Existing Q6/Q8 Reference Results

The earlier quality runs used the same hardware but bare server defaults:

| Quant | Essay words / score | Python | Java | Essay gen | Code gen |
|---|---:|---:|---:|---:|---:|
| Q6_K_XL | 1,515 / 21 | 0/11, 19/25 | 11/11, 24/25 | 54.50 t/s | 54.3 t/s |
| Q8_K_XL | 1,088 / 23 | 0/11, 17/25 | 11/11, 21/25 | 47.36 t/s | 47.2 t/s |
| BF16 | 1,050 / 21 | 11/11, 25/25 | 11/11, 24/25 | 21.80 t/s | 21.8 t/s |

The BF16 run is materially slower and uses roughly twice the model-file memory of Q8 while delivering a substantial improvement on the Python artifact in this single deterministic sample. It does not clearly improve essay quality or Java quality.
