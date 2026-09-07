---
name: feedback-metrics-source
description: Prefer llama.cpp server-side metrics over GuideLLM client-side metrics for benchmark results
metadata:
  type: feedback
---

Use llama.cpp server metrics as the primary source of benchmark data, not GuideLLM client-side numbers.

**Why:** Prior analysis showed the server metrics are more accurate and informative. GuideLLM client numbers are inflated/distorted by network overhead, streaming chunk counting, and cold-start queuing time (e.g., client TTFT of 20s vs server prompt eval of 215ms; client throughput of 77 t/s vs server's actual 43 t/s).

**How to apply:** When recording or reporting benchmark results, pull prompt eval speed, generation speed, token counts, and timing from the llama.cpp server. The `timings` object returned in the llama.cpp API response (also present in the final streamed chunk) carries `prompt_per_second`, `predicted_per_second`, `prompt_n`, `predicted_n`, etc. — the same figures the server logs print. The eval scripts (`manual_eval.py`, `manual_code_eval.py`) now capture this into each trace's "Server Timings (llama.cpp)" section. GuideLLM output can be noted as supplementary but not used as the primary figures. See [[llama-cpp-serving]].
