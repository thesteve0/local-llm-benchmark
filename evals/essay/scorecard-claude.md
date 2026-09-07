# Essay Scorecard — Transformer vs. State Space Model

Graded against `evals/essay/rubric.md`. Source essays are the `## Response` sections of
`output/manual_eval/transformer_v_mamba_*.md`. Word counts are of the essay body only
(between `## Response` and `## Timings`), measured with `wc -w`.

> **Provenance:** Both the rubric (`rubric.md`) and every score below were produced by Claude
> (Opus 4.8), autonomously, in a single session, **without human oversight, review, or
> approval**. Steve did not grade any essay, adjust any score, or validate the rubric. These
> are one model's judgments of other models' prose and should be read as such. Evaluator:
> Claude. Date: 2026-09-07.

## Summary table

| # | Model (quant) | Words | Accuracy | Coverage | Depth | Structure/Tone | Constraint | **Total** |
|--:|---|--:|:--:|:--:|:--:|:--:|:--:|:--:|
| 1 | Qwen3.8-27B (Q6) | 803 | 5 | 5 | 5 | 5 | 5 | **25 / 25** |
| 2 | Qwen3.6-35B-A3B (Q8) | 603 | 5 | 5 | 4 | 5 | 5 | **24 / 25** |
| 2 | Qwen3.6-35B-A3B (Q6) | 574 | 5 | 5 | 4 | 5 | 5 | **24 / 25** |
| 2 | Muse-Glimmer-30B (Q6) | 808 | 5 | 5 | 5 | 4 | 5 | **24 / 25** |
| 5 | Nemotron-3.5-Lightning-30B-A3B (Q8) | 1088 | 5 | 5 | 5 | 5 | 3 | **23 / 25** |
| 6 | Nemotron-3.5-Lightning-30B-A3B (Q6) | 1515 | 5 | 5 | 5 | 5 | 1 | **21 / 25** |

**Essay-quality ranking:** Qwen3.8 Q6 > (Qwen3.6 Q8 ≈ Qwen3.6 Q6 ≈ Muse-Glimmer Q6) >
Nemotron Q8 > Nemotron Q6.

The spread is narrow: on raw substance five of the six are excellent and nearly
interchangeable. The ranking is decided almost entirely by **instruction-following on the
length limit**, not by prose quality — both Nemotron runs write the most substantive essays
in the set but are the only two that break the "< 1000 words" constraint.

---

## 1. Qwen3.8-27B-UD-Q6_K_XL — 25 / 25 (803 words)

| Dimension | Score | Notes |
|---|:--:|---|
| Technical Accuracy | 5 | Correct throughout: attention as `softmax(QK^T/√d)V`, O(n²) time+memory, the SSM recurrence with A/B/C/D, input-dependent Mamba parameters, parallel scan for training. No errors. |
| Topic Coverage | 5 | All three aspects for both architectures, plus a dedicated paragraph on KV-cache memory behavior. |
| Depth & Insight | 5 | Best-balanced trade-off treatment of the mid-tier: names the SSM **compression weakness** ("older information may be partially overwritten or blended into the state") *and* the Transformer's precise-retrieval strength, plus streaming and hybrids. |
| Structure & Tone | 5 | Clean flowing essay, eight well-linked paragraphs, no headings — the closest match to "essay" in "academic introductory-course style." |
| Constraint Adherence | 5 | 803 words, comfortably in range. |

**Note:** the top essay came from the model ranked *third* on code. Its prose reasoning is
excellent even though its generation speed on this hardware is by far the worst (dense 27B,
~8.5 t/s; the essay took ~10 min of wall clock).

## 2 (tie). Qwen3.6-35B-A3B-Q8_0 — 24 / 25 (603 words)

| Dimension | Score | Notes |
|---|:--:|---|
| Technical Accuracy | 5 | Accurate; correctly describes the selective mechanism as modulating the discretization step size and projection matrices. |
| Topic Coverage | 5 | All three aspects, clean intro/conclusion. |
| Depth & Insight | 4 | Solid, but presents SSMs fairly one-sidedly as the long-context winner; doesn't flag the fixed-state retrieval weakness. |
| Structure & Tone | 5 | Textbook five-paragraph academic essay; ideal register. |
| Constraint Adherence | 5 | 603 words. |

## 2 (tie). Qwen3.6-35B-A3B-UD-Q6_K_XL — 24 / 25 (574 words)

| Dimension | Score | Notes |
|---|:--:|---|
| Technical Accuracy | 5 | Accurate; shows the recurrence `h_t = A h_{t-1} + B x_t`, LSTM-gating analogy, parallel scan. |
| Topic Coverage | 5 | All three aspects covered. |
| Depth & Insight | 4 | A touch deeper than its own Q8 run — cites the "lost in the middle" phenomenon — but still light on the SSM retrieval trade-off. |
| Structure & Tone | 5 | Clean five-paragraph essay, correct register. |
| Constraint Adherence | 5 | 574 words. |

*Q6 vs Q8 for Qwen3.6: effectively a wash (both 24). Q6 adds the state equation and
"lost in the middle"; Q8 adds the selective-parameter detail and a training-parallelism
note. Neither dominates.*

## 2 (tie). Muse-Glimmer-30B-UD-Q6_K_XL — 24 / 25 (808 words)

| Dimension | Score | Notes |
|---|:--:|---|
| Technical Accuracy | 5 | The most precise on SSM lineage — correctly distinguishes **S4's O(n log n) FFT** convolution from **Mamba's O(n) selective scan**, and shows input-dependent `B_k, C_k, Δ_k`. A subtle point the others glossed. |
| Topic Coverage | 5 | All three aspects, with explicit complexity figures (e.g., "~1B attention entries" for 32k). |
| Depth & Insight | 5 | Engages the compressed-state retrieval limit ("information must be routed through the latent state, which can limit fine-grained recall"). |
| Structure & Tone | 4 | Strong, but leans on markdown section headings + display equations — reads more like polished lecture notes than a flowing *essay*. Minor register deduction. |
| Constraint Adherence | 5 | 808 words. |

**Note:** the biggest surprise of the set. Muse-Glimmer was near the bottom on **code**
(Python 21/25 with a latent equality-swap bug, Java 22/25) yet writes a top-tier **essay**.
Prose quality and code quality are not the same axis.

## 5. Nemotron-3.5-Lightning-30B-A3B-UD-Q8_K_XL — 23 / 25 (1088 words)

| Dimension | Score | Notes |
|---|:--:|---|
| Technical Accuracy | 5 | Excellent — full equations for both paradigms, selective SSM, dependency-modeling comparison. |
| Topic Coverage | 5 | All three aspects, extensively. |
| Depth & Insight | 5 | Deep: explicit dependency-structure comparison, hardware-aware parallelism, hybrid convergence. |
| Structure & Tone | 5 | Well-organized, academic, coherent arc. |
| Constraint Adherence | 3 | **1088 words — over the 1000-word ceiling by ~9%.** Substantive but overshoots the explicit limit. |

## 6. Nemotron-3.5-Lightning-30B-A3B-UD-Q6_K_XL — 21 / 25 (1515 words)

| Dimension | Score | Notes |
|---|:--:|---|
| Technical Accuracy | 5 | The richest and most correct essay in the set — full derivations, and the best treatment of SSM's retrieval weakness ("implicit compression may struggle with tasks requiring precise, arbitrary retrieval"); even names Performer/Linformer and SSM-in-Transformer hybrids. |
| Topic Coverage | 5 | Exhaustive on all three aspects plus future directions. |
| Depth & Insight | 5 | The deepest of all six — this is the essay you'd want on content alone. |
| Structure & Tone | 5 | Clean section structure, academic. (Arguably beyond "introductory," but well-built.) |
| Constraint Adherence | 1 | **1515 words — 51% over the "< 1000 words" limit.** The explicit, checkable length instruction was effectively ignored. In an agentic setting this is a real failure, not a stylistic quibble. |

**Note:** best content, worst instruction-following. Nemotron's essay would win on substance
and lose on obedience — and both quants overshoot the ceiling, so this is a model trait, not a
quant artifact (mirroring how its Python `from typing import list, dict, tuple` failure showed
up identically at Q6 and Q8).
