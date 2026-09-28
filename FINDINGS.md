# Local LLM Benchmark — Findings

**Hardware:** Framework Desktop, AMD Ryzen AI MAX+ 395, 128 GB unified (96 GB GPU / 32 GB CPU).
**Serving:** llama.cpp directly (`llama serve`), port 8080, one concurrent user, bare defaults.
**Methodology:** server **stopped and cold-restarted before every task**; code evals sent at
`temperature: 0.0`; essay used server defaults. All performance numbers are from the llama.cpp
`timings` object (authoritative), not a client-side tool.

> **Provenance / caveat:** The code and essay **rubrics, and every quality score in this report,
> were written by Claude (Opus 4.8) autonomously — no human authored, edited, reviewed, or
> approved them.** Test pass/fail counts and performance metrics are machine-measured and
> objective; the 1–5 quality scores are one model's judgment of other models' output. Treat the
> fine-grained ordering as soft. Rubrics: `evals/bubble-sort/rubric.md` (code),
> `evals/essay/rubric.md` (essay). Per-run detail: `evals/**/scorecard-claude.md`,
> `evals/essay/scorecard-claude.md`, `output/manual_eval/transformer_v_mamba_*.md`.

---

## 1. Models under test

| Model | Arch | Total / active params | Quants benchmarked | Notes |
|---|---|---|---|---|
| Qwen3.6-35B-A3B | MoE | 35B / ~3B | UD-Q6_K_XL, Q8_0 | multimodal; ctx 256K |
| Qwen3.8-27B | Dense | 27B | UD-Q6_K_XL | thinking; slow on this HW |
| NVIDIA Nemotron-3.5-Lightning-30B-A3B | MoE | ~33B / ~3B | UD-Q6_K_XL, Q8_K_XL, BF16 | ctx 128K served / 1M train; completion-only |
| Muse-Glimmer-30B | Dense | ~27.9B | UD-Q6_K_XL | ctx 128K |
| Ornith-1.5-35B-A3B | MoE | ~34.7B / ~3B | UD-Q8_K_XL | Qwen35MoE; thinking; ctx 256K native; MTP stripped from all quant tiers (untrained) |

Two architecture classes dominate the results: **MoE (~3B active)** models run ~7× faster than the
**dense 27–30B** models on this hardware.

---

## 2. Performance (llama.cpp `timings`)

Generation speed is the number that matters for agentic use. It splits cleanly by architecture.

| Model (quant) | Class | Essay gen | Code gen (Py / Java) | Prompt eval |
|---|---|--:|--:|--:|
| Nemotron Q6 | MoE | 54.50 t/s | 54.38 / 54.32 | 128 t/s |
| Qwen3.6 Q6 | MoE | 53.33 t/s | 52.72 / 52.66 | 168 t/s |
| Qwen3.6 Q8 | MoE | 51.41 t/s | 51.21 / 51.13 | 175 t/s |
| Nemotron Q8 | MoE | 47.36 t/s | 47.19 / 47.22 | 121 t/s |
| Ornith Q8 | MoE | 45.77 t/s | 45.12 / 45.09 | 139–599 t/s |
| Nemotron BF16 | MoE | 21.80 t/s | 21.81 / 21.79 | 73–325 t/s |
| Muse-Glimmer Q6 | Dense | 7.85 t/s | 7.11 / 7.12 | 158 t/s |
| Qwen3.8 Q6 | Dense | 8.45 t/s | 8.44 / 8.43 | 57 t/s |

**Takeaways**
- The two dense models are **~6–7× slower** at generation than the MoE models. On this hardware,
  dense 27–30B is painful for interactive/agentic loops (Qwen3.8's essay took ~10 min wall clock).
- **Q6 → Q8 costs ~8–13% generation speed** with no correctness benefit here (see §5); Q6 is the
  better default for the MoE models unless you specifically want the Q8 quality ceiling.
- Nemotron is the fastest generator in the quantized runs, but BF16 drops to 21.8 t/s; Qwen3.6 has the best prompt-eval among the earlier comparison runs.
- BF16 prompt evaluation varies substantially with workload (73.53 t/s for the essay and 320–325 t/s for the short code prompts), so prompt-eval speed should not be summarized by one model-independent number.
- **Ornith Q8 is the slowest of the Q8-class MoE models** (~45 t/s vs. ~47–51 t/s for Nemotron/Qwen3.6
  Q8) but still firmly in the MoE performance class, not the dense one — generation speed is stable
  across all four of its tasks (44.3–45.8 t/s). Its prompt eval is very fast on the short code prompts
  (~595–599 t/s) but much slower on the essay (139 t/s), echoing the same workload-dependent
  prompt-eval variance seen with Nemotron BF16.

---

## 3. Code quality — bubble sort (Python + Java)

All test counts from `run_tests.py` (Python via `unittest`, Java via Docker `eclipse-temurin:21`).
Quality is scored /25 against `evals/bubble-sort/rubric.md`.

| Model (quant) | Python tests | Python /25 | Java tests | Java /25 |
|---|:--:|:--:|:--:|:--:|
| Qwen3.6 Q8 | 11/11 | 24 | 11/11 | **25** |
| Qwen3.6 Q6 | 11/11 | 24 | 11/11 | 23 |
| Qwen3.8 Q6 | 11/11 | 24 | 11/11 | 22 |
| Ornith Q8 | 11/11 | **25** | 11/11 | 24 |
| Muse-Glimmer Q6 | 11/11 | 21 | 11/11 | 22 |
| Nemotron Q6 | **0/11** | 19 | 11/11 | 24 |
| Nemotron Q8 | **0/11** | 17 | 11/11 | 21 |
| Nemotron BF16 | **11/11** | **25** | 11/11 | 24 |

**Takeaways**
- **Qwen3.6 is the most reliable coder** — every run passes at both quants, and its Q8 Java run is
  the single best artifact in the whole benchmark (clean 25/25: proper 3-way `Integer.compare`
  comparator, `n-i-1` reducing bound, documented null/empty handling).
- **Nemotron fails Python at both quantized settings** with an identical fatal bug:
  `from typing import list, dict, tuple` (lowercase names aren't exported → `ImportError`, 0/11).
  The BF16 run avoids that failure and produces the strongest Python artifact in this benchmark
  (25/25). Its Java remains strong at 24/25.
- **Q6 → Q8 did not help, and for Nemotron made things worse** (Java 24→21, Python 19→17). BF16
  improved Nemotron's Python result to 25/25 in this one deterministic sample, but cost ~54–59% of
  quantized generation speed. Treat the single-run quality difference as suggestive, not definitive.
- **Ornith is the second model (after Nemotron BF16) to land a clean 25/25 Python run**, and its only
  Java deduction is an unrequested demo `main` method — its comparator logic is a correct 3-way
  `Integer.compare`/`Long.compare`, avoiding the boxed-`Integer` pitfall in the Nemotron Java runs.
- **Latent bugs that still pass tests** (documented, not fixed): Muse-Glimmer's Python swaps
  exact-duplicate timestamps every pass (strict-predicate/`not` mismatch); Nemotron Q8 Java compares
  boxed `Integer` with `!=`, so equal priorities ≥128 skip the tiebreaker. The test suites don't
  exercise those inputs, so they score as passing.

**Rust (new for this benchmark set):** Ornith Q8 is the **first model to receive a scored Rust
run** — prior Rust runs (Mellum2, early Qwen3.6) were only ever test-checked, never rubric-graded.
It passed all 11 hidden tests and scored **25/25**, with fully idiomatic `Option` pattern matching
centralizing every ordering rule and a working doc-test example. No other current model has a
scored Rust run to compare against. This run also surfaced (and led to fixing) a tooling bug:
`manual_code_eval.py`'s code-extraction step naively concatenated *every* fenced code block in a
response — including nested ``` fences inside Rust doc-comment examples — which corrupted the
saved `lib.rs` when the model's answer included an illustrative `Cargo.toml` snippet and a closing
usage note as separate top-level fences. The file was manually corrected from the trace before
testing/scoring (see `evals/bubble-sort/rust/ornith-1.5-35b-a3b-q8/scorecard-claude.md`), and
`extract_code()` was subsequently fixed to (1) only match fence markers at the start of a line, so
nested doc-comment fences can't prematurely close a block, and (2) prefer blocks tagged with the
target language, falling back to "all blocks" only when none are tagged. Verified against all
three of this run's responses (Python/Java/Rust) — output now matches byte-for-byte.

---

## 4. Essay quality — Transformer vs. State Space Model

Scored /25 against `evals/essay/rubric.md`. The prompt required **500–1000 words**, academic
introductory-course tone, covering attention, complexity vs. sequence length, and long-context
implications. Word counts are of the essay body (`wc -w`).

| Model (quant) | Words | /25 | Point(s) lost |
|---|--:|:--:|---|
| Qwen3.8 Q6 | 803 | **25** | — |
| Qwen3.6 Q8 | 603 | 24 | Depth (one-sided pro-SSM) |
| Qwen3.6 Q6 | 574 | 24 | Depth |
| Muse-Glimmer Q6 | 808 | 24 | Structure (lecture-notes, not essay prose) |
| Nemotron Q8 | 1088 | 23 | Constraint (over 1000 words) |
| Ornith Q8 | 808 | 23 | Depth (one-sided) + Structure (headings, not prose) |
| Nemotron Q6 | 1515 | 21 | Constraint (**51% over** the limit) |
| Nemotron BF16 | 1050 | 21 | Constraint (5% over 1000 words) |

**Takeaways**
- On raw substance, **six of seven essays are near-interchangeable** and excellent. The ranking is
  decided almost entirely by **instruction-following on the length limit** and, secondarily, by
  whether the essay reads as flowing prose vs. markdown-headed sections.
- **Nemotron writes the most substantive essays** (full derivations, best treatment of SSM's
  fixed-state retrieval weakness, names Performer/Linformer and hybrids) but is the **only model
  that broke the "< 1000 words" constraint — at both quants.** For an agentic/instruction-following
  benchmark, ignoring a hard, checkable instruction is a real failure. Like the Python bug, it
  shows at both quants → a model trait.
- **Muse-Glimmer** — near the bottom on code — writes a **top-tier essay**, including the sharpest
  technical point in the set (correctly distinguishing S4's O(n log n) FFT from Mamba's O(n)
  selective scan).
- **Ornith** stays safely in range (808 words) but loses a point apiece on Depth (presents Mamba's
  selectivity as resolving older SSMs' weaknesses without flagging the fixed-state retrieval
  limitation — the same one-sidedness as both Qwen3.6 quants) and Structure (seven markdown-headed
  sections rather than flowing essay prose — the same deduction applied to Muse-Glimmer). It ties
  Nemotron Q8 at 23/25, arriving there by a different path: constraint-following instead of depth
  and register.

---

## 5. Cross-cutting conclusions

1. **Prose quality and code quality are different axes.** The code ranking and the essay ranking are
   nearly inverted at the extremes:
   - **Code:** Qwen3.6 Q8 ≈ Ornith Q8 > Nemotron Q6 > Qwen3.8 Q6 > Muse-Glimmer Q6
   - **Essay:** Qwen3.8 Q6 > (Qwen3.6 Q8 ≈ Qwen3.6 Q6 ≈ Muse-Glimmer Q6) > (Nemotron Q8 ≈ Ornith Q8)
     > Nemotron Q6

   Qwen3.8 is mid-pack on code but #1 on essays; Nemotron is near the top on code but last on
   essays; Muse-Glimmer is last on code but tied-2nd on essays; Ornith is tied-top on code (25+24
   across Python/Java, plus a clean 25/25 on the first-ever scored Rust run) but only mid-pack on
   essay depth and structure. Do not infer a model's coding ability from its writing, or vice versa.

2. **Quantization (Q6 vs Q8) is not a quality lever here.** Across both tasks, Q8 never improved
   correctness or scores, cost ~8–13% speed, and for Nemotron made code *worse*. **Q6 is the
   default choice** for the MoE models; reserve Q8 only for the top quality ceiling on a specific
   artifact (e.g., Qwen3.6 Q8 Java).

3. **Architecture dominates the speed/usability tradeoff.** MoE (~3B active) is ~7× faster than
   dense 27–30B on this hardware. The two dense models (Qwen3.8, Muse-Glimmer) write well but are
   too slow (~7–8.5 t/s) for comfortable agentic use here regardless of quality.

4. **BF16 removes the observed Nemotron Python import failure, but not the length-limit issue.**
   BF16 passed all Python tests and scored 25/25, while all three Nemotron settings overshot the essay
   limit. The BF16 speed cost is substantial: 21.8 t/s versus 47–54 t/s for Q8/Q6.

### Overall recommendation for this hardware (agentic coding)

**Qwen3.6-35B-A3B at Q6** remains the best all-rounder: MoE-fast (~53 t/s), 100% test pass rate
across Python and Java, strong code quality (24/23), and a solid in-range essay (24/25). Step up to
**Q8** only for the top code-quality ceiling. Nemotron BF16 produces excellent code in this single
sample (25/25 Python, 24/25 Java), but is much slower (~21.8 t/s), uses a ~65.8 GB model file, and
still overshoots the essay constraint. Q6/Q8 remain the better default for interactive agentic use;
BF16 is a quality-oriented option when memory and latency are acceptable.

**Ornith-1.5-35B-A3B at Q8** is the strongest new contender in this round: 100% test pass rate
across Python, Java, **and** Rust — the first model in this benchmark set to have a Rust run
rubric-scored, and it landed a clean 25/25 there alongside a 25/25 Python and a 24/25 Java. It's
essentially tied with Qwen3.6 Q8 on code quality (49 vs. 49 combined Python+Java points) but trails
it on essay quality (23 vs. 24, on depth and header-heavy structure) and generation speed (~45 t/s
vs. ~51 t/s). Only a Q8 quant has been tested so far — no Q6 data point yet to compare the usual
quant/speed tradeoff. Worth a second look once a lighter quant is benchmarked, but for now Qwen3.6
remains the default pick on this hardware.
