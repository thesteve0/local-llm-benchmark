# Essay Quality Rubric — Transformer vs. State Space Model Essay

Companion to the code-eval rubric (`evals/bubble-sort/rubric.md`). This one scores the
**technical essay** prompt (`output/manual_eval/transformer_v_mamba_*.md`):

> Write a comprehensive, detailed technical essay of **at least 500 words and less than
> 1000 words**, explaining the architectural differences between Transformer-based Large
> Language Models and State Space Models (like Mamba). Discuss their respective approaches
> to the **attention mechanism**, **computational complexity regarding sequence length**,
> and their **practical implications for long-context window processing**. Use an
> **academic, introductory course** style of writing and tone.

Score each of the five dimensions 1–5. Total: 25 points. Grade the **`## Response`**
(the final essay) only — not the `## Reasoning` scratchpad.

> **Provenance:** This rubric was written by Claude (Opus 4.8), autonomously, without human
> oversight or review, as part of grading the essay benchmark set. It is a first draft of a
> criterion set, not a human-validated standard. Steve did not author, edit, or approve it.

## 1. Technical Accuracy (1–5)

Are the technical claims correct? (self-attention as pairwise QK^T softmax; O(N²) attention;
KV-cache growth; the SSM recurrence h_t = A·h_{t-1} + B·x_t / y_t = C·h_t; Mamba's
input-dependent "selective" parameters; parallel scan; S4-vs-Mamba distinctions.)

| Score | Criteria |
|------:|----------|
| 5 | All substantive claims correct. Any equations shown are right. No misconceptions. |
| 4 | Correct throughout with one minor imprecision or loose statement that doesn't mislead. |
| 3 | Mostly correct but one clear technical error or a persistent oversimplification. |
| 2 | Several errors or a fundamental misconception about how one architecture works. |
| 1 | Pervasively wrong; would teach the reader incorrect mental models. |

## 2. Topic Coverage (1–5)

Does it address all **three** required aspects — (a) attention mechanism, (b) computational
complexity vs. sequence length, (c) practical implications for long-context — for **both**
architectures?

| Score | Criteria |
|------:|----------|
| 5 | All three aspects covered substantively for both architectures, plus a clear intro/conclusion. |
| 4 | All three covered, but one is treated more thinly than the others. |
| 3 | One of the three required aspects is only glancingly addressed. |
| 2 | One required aspect is essentially missing, or one architecture is underdeveloped. |
| 1 | Multiple required aspects missing. |

## 3. Depth & Insight (1–5)

Beyond reciting definitions: does it engage the real trade-offs? (SSM's fixed-state
**compression weakness** for precise long-range retrieval; "lost in the middle"; training
parallelism vs. sequential recurrence; hybrid architectures; S4 FFT O(N log N) vs. Mamba's
selective scan.)

| Score | Criteria |
|------:|----------|
| 5 | Engages the core trade-off (efficiency vs. retrieval/expressivity) in **both** directions, with at least one non-obvious insight (e.g., SSM retrieval limits, hybrids, S4/Mamba nuance). |
| 4 | Good depth and at least one trade-off, but presents one architecture somewhat one-sidedly. |
| 3 | Correct but largely definitional; trade-offs asserted, not explored. |
| 2 | Surface-level; reads like a glossary. |
| 1 | Little beyond restating the prompt. |

## 4. Structure & Academic Tone (1–5)

Is it a well-organized **essay** in an **academic, introductory-course** register — coherent
intro/body/conclusion, logical flow, precise-but-accessible prose?

| Score | Criteria |
|------:|----------|
| 5 | Clean essay arc, strong topic sentences, flows as prose, pitched exactly at an intro-course academic level. |
| 4 | Well-organized and appropriately toned, with a minor lapse (e.g., leans on headings/notes more than flowing essay prose, or one register wobble). |
| 3 | Followable but mechanical (e.g., bullet-like sections) or tone drifts (too casual or too dense for "introductory"). |
| 2 | Disorganized or a poor register match (e.g., marketing tone, or graduate-level density inaccessible to a beginner). |
| 1 | Incoherent or not essay-form. |

## 5. Constraint Adherence (1–5)

The prompt sets a hard, explicit range: **≥ 500 and < 1000 words** (essay body). For an
agentic-use benchmark, obeying an explicit, checkable instruction is itself a graded skill.

| Score | Criteria |
|------:|----------|
| 5 | Within 500–999 words. |
| 4 | Within ~10% of a bound (450–499, or 1000–1099). |
| 3 | Overshoots/undershoots a bound by 10–25% (1100–1249, or 375–449). |
| 2 | Off by 25–50% (1250–1499, or 250–374). |
| 1 | Off by > 50% (≥ 1500 words, or < 250), i.e., the length instruction was effectively ignored. |
