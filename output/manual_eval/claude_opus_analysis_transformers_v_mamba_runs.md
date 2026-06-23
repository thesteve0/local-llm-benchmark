# Analysis: Transformer vs Mamba Essay — Four Local Model Runs

**Evaluator:** Claude Opus 4.6  
**Date:** 2026-06-23  
**Prompt:** Write a 500–1000 word technical essay comparing Transformer and SSM (Mamba) architectures, covering attention mechanisms, computational complexity, and long-context implications. Academic introductory style.

---

## Models Tested

| Model | Quant | Reasoning Tokens | Answer Tokens | Word Count | Total Time |
|-------|-------|----------------:|-------------:|----------:|----------:|
| Qwen3.6-35B-A3B | Q8_0 | 3,681 | 931 | 636 | 89.29s |
| Qwen3.6-35B-A3B-UD | Q4_K_M | 2,480 | 830 | 570 | 55.52s |
| mellum2:12b-a2.5b | Q8_0 | 210 | 1,645 | 950 | 22.85s |
| mellum2:12b-a2.5b | Q6_K | 139 | 1,727 | 950 | 20.37s |

---

## 1. Quality Scores

Each response is scored on four dimensions (1–10 scale), then combined into a weighted overall score.

### Qwen3.6-35B-A3B Q8_0 — Overall: 8.5/10

| Dimension | Score | Notes |
|-----------|------:|-------|
| Technical Accuracy | 9 | All claims are correct. Proper SSM equations (ḣ = Ah + Bx, y = Ch + Dx). Correctly identifies selective scan, ZOH discretization, and the role of input-dependent B, C, Δ. |
| Completeness | 9 | Covers all three required topics with good depth. Mentions KV cache explosion, needle-in-a-haystack tradeoff, and hybrid architectures. |
| Constraint Adherence | 9 | 636 words — solidly within range. Appropriate academic tone throughout. |
| Writing Quality | 8 | Clean paragraph-based flow. No headers or tables, but reads well as a continuous essay. Good transitions between topics. |

**Standout strength:** The response correctly identifies the information-theoretic tradeoff — that SSMs compress history into a fixed-size state, creating a theoretical ceiling on information capacity that attention does not have. This is a nuanced point that shows genuine understanding.

### Qwen3.6-35B-A3B-UD Q4_K_M — Overall: 8.5/10

| Dimension | Score | Notes |
|-----------|------:|-------|
| Technical Accuracy | 8 | One imprecision: states KV cache causes "memory usage to grow quadratically with sequence length." The KV cache actually grows linearly (O(n·d)); it is the attention *computation* that is quadratic. Minor but worth noting. |
| Completeness | 9 | Covers all topics and adds useful references to FlashAttention, RoPE, sparse attention, and associative scan algorithms that the Q8 version omitted. |
| Constraint Adherence | 9 | 570 words — within range. Academic tone. |
| Writing Quality | 9 | Slightly more polished prose than the Q8 version. Better paragraph transitions and a more confident authorial voice. |

**Standout strength:** Mentions the vanishing gradient advantage of SSMs over traditional RNNs, and draws a wider picture of the optimization landscape (FlashAttention, RoPE, sparse attention). Broader survey perspective than the Q8 run.

### mellum2:12b-a2.5b Q8_0 — Overall: 8.0/10

| Dimension | Score | Notes |
|-----------|------:|-------|
| Technical Accuracy | 7.5 | Mostly accurate. Correct SSM equations (h_t = A_t h_{t-1} + B_t x_t). However, claims "even with kernel-based approximations (e.g., Performer)... the asymptotic cost remains O(n²)" — this is incorrect; Performer achieves O(n) by design. Also cites "Liu et al., 2023" which appears fabricated. |
| Completeness | 9 | Excellent coverage. Five numbered practical implications. Includes a complexity comparison table covering full attention, sparse/linearized attention, and Mamba. |
| Constraint Adherence | 8 | 950 words — within range but pressing against the 1000-word ceiling. The model did not self-monitor its word count. |
| Writing Quality | 9 | Best-structured response of the four. Numbered sections, LaTeX equations, horizontal rules, comparison table. Reads like a proper course handout. |

**Standout strength:** The complexity comparison table including sparse/linearized attention variants is a genuinely useful addition that none of the other models provided. The five-point practical implications section (scalability, training efficiency, representational fidelity, flexibility, trade-offs) is well-organized and informative.

### mellum2:12b-a2.5b Q6_K — Overall: 6.5/10

| Dimension | Score | Notes |
|-----------|------:|-------|
| Technical Accuracy | 5 | Significant error: the SSM equations presented (b_t = z_t ⊙ x_t, c_t = r_t ⊙ x_t, x_{t+1} = f_t(x_t) + b_t) do not represent the Mamba/SSM formulation. This looks like a gated recurrent network (GRU-like) rather than a state space model. The Q8_0 version of the same model got these equations correct. Also, the per-token attention cost is listed as O(h·d²), which omits the sequence-length dependence. |
| Completeness | 8 | Covers all required topics. Five practical implications listed. Mentions hybrid approaches and temporal credit assignment. |
| Constraint Adherence | 8 | 950 words — within range. Academic tone. |
| Writing Quality | 8 | Well-structured with sections, table, and LaTeX. But the incorrect equations undermine the credibility of an otherwise polished presentation. |

**Critical weakness:** The core SSM equations are wrong. In an academic essay whose central task is to explain the Mamba architecture, presenting incorrect equations for that architecture is a fundamental failure. The confident formatting and academic style make this worse — a reader unfamiliar with SSMs would absorb wrong information presented with authority.

---

## 2. Reasoning Length vs. Quality

| Model | Reasoning Tokens | Overall Score | Constraint Violations |
|-------|----------------:|:------------:|:---------------------:|
| Qwen Q8_0 | 3,681 | 8.5 | None |
| Qwen Q4_K_M | 2,480 | 8.5 | Minor accuracy slip |
| mellum2 Q8_0 | 210 | 8.0 | Performer claim wrong, fabricated citation |
| mellum2 Q6_K | 139 | 6.5 | Wrong SSM equations, complexity errors |

**Clear correlation exists, with diminishing returns.** The most striking pattern is not the raw correlation but *what reasoning is used for*:

**Self-correction through reasoning.** Both Qwen models used their reasoning chains to catch and fix word-count problems. The Q8 Qwen initially drafted ~462 words, identified the shortfall, and expanded to ~662 with targeted additions. The Q4 Qwen did the same, expanding from ~580 to ~630. Neither mellum2 model monitored word count at all — they happened to land within range (950 words) by coincidence rather than design, pressing dangerously close to the 1000-word ceiling.

**Diminishing returns within a model family.** Within the Qwen pair, 48% more reasoning tokens (3,681 vs 2,480) produced no measurable quality improvement — both scored 8.5. The Q4_K_M model was arguably more efficient: it produced a comparably good response with less reasoning, included broader references (FlashAttention, RoPE), and ran in 62% of the time. The extra reasoning in Q8 was spent on more granular word counting, not on improving content.

**Minimum threshold matters.** The mellum2 models, with only 139–210 reasoning tokens, both had factual errors. There appears to be a minimum reasoning investment below which accuracy degrades — the model jumps straight to generation without verifying its technical claims.

---

## 3. Additional Observations

### Quantization Degrades Factual Accuracy Before It Degrades Style

This is the most striking finding across all four runs. Both lower-quant models produced responses that *read* just as well as their higher-quant siblings — the prose is fluent, the structure is clean, the tone is appropriate. But the factual content degraded:

- **Qwen Q4_K_M vs Q8_0:** The Q4 version introduced a subtle error (KV cache scaling described as quadratic when it's linear). The Q8 version made no such error.
- **mellum2 Q6_K vs Q8_0:** The Q6 version got the fundamental SSM equations wrong — it substituted a GRU-like gated recurrence for the actual state space formulation. The Q8 version presented the correct equations.

This suggests that **quantization erodes the model's stored knowledge before it erodes its language fluency.** A model can lose the ability to correctly recall a mathematical formulation while retaining the ability to write a well-structured academic paragraph around an incorrect formulation. This is a dangerous failure mode — the output looks authoritative but is wrong.

### Model Architecture Affects Response Strategy

The two model families took fundamentally different approaches:

| Aspect | Qwen (both quants) | mellum2 (both quants) |
|--------|--------------------|-----------------------|
| Reasoning strategy | Outline → Draft → Word count → Expand → Polish | Brief plan → Generate |
| Response format | Continuous prose paragraphs | Numbered sections, tables, LaTeX blocks |
| Token allocation | ~75% reasoning, ~25% answer | ~12% reasoning, ~88% answer |
| Self-monitoring | Active (caught and fixed word count issues) | None |

The mellum2 models produced visually richer output (tables, equations, section numbers) but spent almost no tokens verifying correctness. The Qwen models produced plainer prose but invested heavily in self-review.

### Speed vs. Quality Tradeoff

| Model | Total Time | Tokens/sec (total) | Quality |
|-------|----------:|-------------------:|:-------:|
| mellum2 Q6_K | 20.37s | 91.6 | 6.5 |
| mellum2 Q8_0 | 22.85s | 81.2 | 8.0 |
| Qwen Q4_K_M | 55.52s | 59.6 | 8.5 |
| Qwen Q8_0 | 89.29s | 51.7 | 8.5 |

The mellum2 models are 2–4× faster than the Qwen models. Most of this speed difference comes from generating far fewer reasoning tokens. If your use case tolerates the accuracy tradeoffs, mellum2 Q8_0 offers the best speed-to-quality ratio at 22.85 seconds and a score of 8.0.

### TTFT Suggests Different Model Loading Characteristics

| Model | TTFT |
|-------|-----:|
| mellum2 Q8_0 | 0.09s |
| mellum2 Q6_K | 0.31s |
| Qwen Q4_K_M | 0.51s |
| Qwen Q8_0 | 0.54s |

The mellum2 Q8_0 model had a remarkably fast 0.09s time-to-first-token despite being the larger quantization. This may reflect differences in model loading or the amount of prompt processing required. The Qwen models were consistently slower to start, possibly due to their larger effective parameter count or MoE routing overhead.

---

## Summary

**Best overall quality:** Qwen Q8_0 and Q4_K_M tied at 8.5/10. Both produced accurate, well-reasoned, constraint-compliant essays.

**Best value (speed × quality):** mellum2 Q8_0 — 8.0/10 quality in 22.85 seconds. A strong performer despite minimal reasoning.

**Most concerning result:** mellum2 Q6_K — presented incorrect equations for the core architecture being discussed, while maintaining confident academic prose. Demonstrates that quantization can silently degrade factual accuracy while preserving surface quality.

**Key insight:** Reasoning tokens serve as a self-correction mechanism. Models that invest in reasoning catch their own constraint violations and factual gaps. Models that skip reasoning produce faster but less reliable output. For tasks requiring factual accuracy (like technical writing), reasoning investment pays off.
