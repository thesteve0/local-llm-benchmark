# TODO — Open Research Items

> Added 2026-10-14 (after LFM2.5-24B-A2B BF16+Q8_0 rounds, commit 2f611aa).
> Each item has initial analysis so future sessions can pick up without re-deriving context.

## 1. Benchmark models at different reasoning levels (llama.cpp)

### The question
How do we start llama.cpp with different reasoning levels for models that support it, and how should reasoning level factor into benchmark comparisons?

### What our llama-server build exposes
(verified via `llama-server --help` on this machine, llama.cpp <version>):
| Control | Flag / request field | Scope | Notes |
|---|---|---|---|
| Thinking on/off | `-rea on|off|auto` / `--reasoning` | server-wide | default `auto` (detect from template) |
| Effort level | `--reasoning-effort LEVEL` | server-wide | `default` keeps template default; levels seen: minimal, low, medium, high, xhigh (+ ...) — given to the chat template, so only effective if the model's Jinja template consumes it |
| Token budget | `--reasoning-budget N` | server-wide | -1 unrestricted (default), 0 = end thinking immediately (off), N>0 = cap thinking tokens; `--reasoning-budget-message` injects a nudge when exhausted |
| Trace capture | `--reasoning-format deepseek|deepseek-legacy|...` | server-wide | we already use deepseek (thoughts → `reasoning_content`) |
| Template kwargs | `--chat-template-kwargs '{"key":"val"}'` | server-wide | e.g. Qwen `enable_thinking` |
| Per-request | JSON fields in /v1/chat/completions | per request | check which our build accepts: `chat_template_kwargs`, `reasoning_effort`, `reasoning_budget` (verify via strings on binary / a live probe) |

### Per-model support (from models/*.md — verify by probe)
| Model | Thinking behavior | Effort levels? |
|---|---|---|
| Qwen3.6-35B-A3B | thinking=1 | likely (Qwen3 family template) — verify |
| Qwen3.8-27B | thinking (Qwen recommended thinking sampling) | likely — verify |
| Ornith-1.5-35B-A3B | Qwen35MoE arch, `imd`/think block → reasoning_content | likely — verify |
| OLMo-3.1-32B-Think | dedicated think variant; template injects think prefix | verify |
| LFM2.5-24B-A2B | always-on, no effort levels (per model doc) | no |
| Nemotron-3.5-Lightning | completion-only | n/a |
| Muse-Glimmer-30B | CoT enabled | verify |
| gemma4 / mellum2 | non-thinking | n/a |

### Proposed experiments
1. **Fix context-stress 0/5 (quick win):** re-run the needle probes with `-rea off` (or `--reasoning-budget 0`) — current failures are budget exhaustion by always-on reasoning, not retrieval failure (FINDINGS §6–7). Compare against `--reasoning-budget N` sweeps.
2. **Effort sweep on hybrid models** (Qwen3.6 as first candidate): effort ∈ {off, low, medium, high} × {code evals}; measure tests passed, /25 quality, reasoning/answer token split (manual_code_eval.py already records this), wall time, t/s. Cold restart per condition to keep perf numbers clean.
3. **Decide the reporting policy:** reasoning level is currently an uncontrolled confound in cross-model comparisons (always-think LFM vs toggleable Qwen vs completion-only Nemotron). Options: (a) report each model at its default + at off; (b) add reasoning level as a column in results tables; (c) normalize to fixed budget.

### Open questions
- Does the per-request API accept reasoning params in our build (avoids server restarts when sweeping quality-only)? → probe or check llama.cpp docs/source for our version.
- Which levels does each template actually implement (minimal/xhigh may be no-ops on some templates)?
- Interaction with sampling: Qwen3.8 card recommends temp 1.0/top-p 0.95 for thinking mode — if we sweep effort, pin temperature policy first (item 2) to avoid confounds.
- Does `--reasoning-budget 0` differ from `-rea off` on templates that hardcode a think prefix (OLMo injects the open tag as prompt prefix — check_thinking.py)?

## 2. Temperature: should we really benchmark at temp 0?

### The claim
Expert: "0.1/0.2 temp + multiple runs gives a better read of accuracy; otherwise you risk a classic local maxima gradient descent problem."

### Is there gradient descent at inference? No.
Inference is forward-pass only: logits → temperature-scaled softmax → sample. No loss, no gradients, no weight/activation updates. Gradient descent is a training algorithm. The expert's phrase is a metaphor, not a mechanism — but it's pointing at real inference-time phenomena.

### What the metaphor maps to (real mechanisms)
1. **Greedy path lock-in.** temp 0 = argmax per token; the model conditions on its own output, so one bad early token compounds. Known as greedy/beam-search degeneration (Holtzman et al. 2020, "The Curious Case of Neural Text Degeneration"). We have direct evidence in this repo:
   - LFM2.5 Q8_0 Java 0/11: greedy draft had a fatal single-token bug (`sorted[j]` on a List); model re-revised 4 times without catching it (scorecard-claude.md). At temp 0 the failure path is re-entered deterministically.
   - Nemotron Q6+Q8 Python 0/11: identical `from typing import list, dict, tuple` ImportError at both quants — a locked-in failure mode. (Open question: always-wrong distribution vs greedy-path artifact — exactly what multi-run would distinguish.)
   - FINDINGS already notes: "sampling at temperature 0.0 does not guarantee draft stability."
2. **Point estimate vs distribution estimate.** One greedy run measures one path. k runs at temp 0.1–0.2 ≈ Monte Carlo estimate of E[quality] near the mode + a variance estimate. If production/agentic use runs at temp > 0 (Qwen3.8 card: 1.0 thinking / 0.7 non-thinking; LFM2.5 card: 0.1), the deployable quantity is expected quality at those settings — not the greedy path.
3. **temp 0 isn't deterministic on our stack anyway.** FP non-determinism in llama.cpp (Vulkan kernel scheduling, batch shape, parallel reduction order) can flip near-tied logits; quant flips (LFM BF16→Q8_0: Rust 0/11→11/11, Java 11/11→0/11) mix genuine quant effects with path luck. n=1 can't separate them.
4. **Selection overfitting (the steelman of "local maxima").** We're ranking models on single samples; a model can win by luck of its greedy path. Multi-run with variance reporting de-risks the model-selection step itself.

### Where temp 0 is still right
- Throughput / context stress: sampling params don't change t/s meaningfully; keep.
- Comparability: existing repo numbers + public leaderboards are greedy; keeping a temp-0 arm preserves apples-to-apples.
- Cost: k× runs × the full suite is expensive (3 languages + essay + 5 stress probes, cold restart each).

### Proposed protocol (draft for discussion)
1. Keep current temp-0 single run as the screening/comparability arm.
2. Finalists: n=3–5 runs at temp 0.2 (or model-card temp if ≥0.1), fixed seeds per run (request `seed` field / `--seed`) so each run is reproducible; report mean ± min–max of tests passed and rubric score.
3. Check whether the temp-0 run falls inside the multi-run distribution — flags greedy outliers (expect LFM Q8_0 Java to be one).
4. Count degeneration events (repetition loops, constraint violations like word-count overshoot) as a reported metric.
5. Wiring: manual_code_eval.py already has `--temperature`; add `--runs N`, `--seed`, and aggregate scorecard output. Consider logprob-based scoring later for MC-style tasks (not our current evals).

### Open questions
- n needed: with 33 tests across 3 languages, n=3–5 shows variance; n≈10 for a decisive head-to-head. Worth a quick power analysis before committing compute.
- Should the essay arm standardize on model-card temp (LFM used 0.1, older runs used server default 0.8?) — FINDINGS says essay used server defaults for the earlier set. That's a hidden inconsistency across the essay table.
- Interaction with item 1: fix temperature policy before sweeping reasoning effort.
```

Wait — one thing to verify: earlier essay runs "used server defaults" — server default temp is 0.8 per the help output. That's a real hidden inconsistency worth flagging: essay scores in §4 compare models some of which ran at 0.8 default (Nemotron, Qwen3.6 older?) vs LFM at 0.1. Actually §4 table covers Qwen3.8, Qwen3.6, Muse-Glimmer, Nemotron, Ornith — FINDINGS line 6: "essay used server defaults" for the main set, LFM at 0.1. And nemotron.md serve shows `--temp 1.0 --top-p 0.95`, qwen3.8.md shows `--temp 1.0 --top-p 0.95 --top-k 20` (thinking-mode recommended) — so "server defaults" differed per model serve command! Qwen3.8 essay ran at temp 1.0, LFM at 0.1. That's a genuine confound in the essay comparison — excellent material for the TODO. Let me double check what each model doc says about essay temp:
- qwen3.8.md:39-41: sampling flags are Qwen3's recommended thinking-mode values; code evals send 0.0 overriding; "the essay run ..." (truncated — probably "uses server temp 1.0"). 
- nemotron.md:24: `--temp 1.0 --top-p 0.95`.
- lfm2.5: essay at 0.1.
So essay table mixes temp 1.0 (Qwen3.8, Nemotron) vs 0.1 (LFM) vs unknown (Qwen3.6, Muse-Glimmer, Ornith — need to check their docs; muse-glimmer.md and ornith.md probably have serve commands with temp flags). I won't over-assert; I'll flag it as "audit needed" with the two confirmed examples.

Now the version check and full help text — let me run round 2. Also grab manual_code_eval.py payload area and context_stress.py payload area for precise wiring notes.

Actually also worth checking models/ornith.md and models/qwen3.8.md serve commands fully — I have qwen3.8 partial from grep (`--temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0`). ornith.md:36 shows bare `llama serve -hf peculiar-ragdoll/Unsloth-Ornith...` — "bare command with llama.cpp defaults" per line 32. So Ornith essay at 0.8 default. Good — confirmed inconsistency: essays ran at 1.0 (Qwen3.8, Nemotron), 0.8 (Ornith), 0.1 (LFM). Let me quickly check muse-glimmer and qwen3.6 serve commands for temp flags — qwen3.6.md:22/27 bare serve commands (no temp flags) → 0.8. muse-glimmer.md:22 bare → 0.8.

So essay temps: Qwen3.6 0.8, Qwen3.8 1.0, Ornith 0.8, Muse-Glimmer 0.8, Nemotron 1.0, LFM2.5 0.1. Great concrete finding for the TODO: the essay comparison table mixes sampling regimes — nobody noticed because "essay used server defaults" but the server defaults differed per serve command. That's a strong, specific insight to include. (I should double-check muse-glimmer.md and ornith.md to be sure they don't pass temp flags. ornith.md:36 bare confirmed. muse-glimmer.md:22 bare confirmed from the grep launch-mentions output. And qwen3.6 serve commands bare. Good.)

Hmm wait, also gemma4/olmo/mellum2 — not in the §4 essay table (gemma4 and olmo are older/other rounds; mellum2 code-only?). FINDINGS §4 covers the main set. Fine.

Round 2 commands:

```bash
cd /var/home/stpousty/git/local-llm-benchmark
echo "=== llama-server version ==="
llama-server --version 2>&1 | head -3
echo ""
echo "=== --reasoning-effort full help ==="
llama-server --help 2>&1 | grep -A6 -- "--reasoning-effort"
echo ""
echo "=== --reasoning-format full help ==="
llama-server --help 2>&1 | grep -A16 -- "--reasoning-format"
echo ""
echo "=== per-request reasoning keys present in binary? ==="
BIN=$(readlink -f $(which llama-server))
(strings "$BIN" 2>/dev/null || tr -c '[:print:]' '\n' < "$BIN") | grep -x -E "reasoning_effort|chat_template_kwargs|reasoning_budget|enable_thinking|thinking" | sort -u
echo ""
echo "=== manual_code_eval.py payload build ==="
sed -n '40,75p' manual_code_eval.py
sed -n '95,160p' manual_code_eval.py
echo ""
echo "=== context_stress.py payload build ==="
sed -n '45,95p' context_stress.py
echo ""
echo "=== essay temp audit ==="
rg -n "temp|essay" models/muse-glimmer.md models/ornith.md models/qwen3.8.md | head -30
```

Hmm, that's a lot but fine. Actually let me trim: I don't need the full manual_code_eval source; just the payload lines. sed -n '95,115p' is enough plus args. And the essay audit grep.

Then write TODO.md, then run `git status` to show it as a new untracked file (nice callback), and reply.

One more thought on gradient descent analysis — be precise about the softmax/temperature mechanics: temp 0 in llama.cpp = greedy argmax (logits/0 → argmax; implementation-wise llama.cpp treats temp 0 as greedy). Low temp 0.1-0.2 = near-greedy sampling. Also worth noting top_k/top_p defaults: llama-server default top-k 40! So an essay run at "server default" temp 0.8 with top-k 40 — sampling regime quite different from greedy. And the code evals send only temperature: 0.0 in the body — top_k etc. from server defaults apply but with temp 0 sampling collapses to greedy regardless. OK.

Also for the "is temp 0 deterministic" point: llama.cpp with same seed, same batch, same everything is deterministic in principle; but their protocol cold-restarts and the request path/batch may vary; GPU/Vulkan reductions are deterministic per-kernel-config but config can vary with load? To be safe I'll phrase as "near-tied logits + any variation in kernel/batch path can flip argmax; and in practice we've already observed..." — grounded in FINDINGS line 252. Also the scorecard line: "Q8_0's sampling at temperature 0.0 produced a draft with a fatal single-token-level mistake" — hmm, that phrase says sampling at temp 0 — fine.

Also worth including in TODO item 2: the "greedy ≠ best-of" nuance for pass@k — standard practice in code-model evals (HumanEval pass@k with temp 0.2/0.8, n samples) — Codex/HumanEval protocol (Chen et al. 2021) literally samples n≥1 at temp 0.8 for pass@k, temp 0 for pass@1. That's the canonical precedent supporting the expert: multi-sample at moderate temp is the established methodology for code generation evaluation. pass@1 estimated from n samples (unbiased estimator) is standard. Our rubric scoring is richer than pass@k but the same logic applies: estimate expected quality from n samples. Definitely include this citation — it's the strongest "the expert is right in practice" evidence, and it also answers "should we really set temp 0": the field's answer for pass@1 has literally moved to sampling-based estimation.

Let me also think: is there any argument that temp 0 gives a *better* read? Yes: if deployed config is greedy (some agent harnesses use temp 0 for reproducibility — e.g., many coding agents default temp 0!). Actually that's a real counterpoint: agentic coding tools (Aider, Cline, Continue...) often default to temp 0 or low temp for determinism. If the deployment target is greedy, then measuring greedy is measuring the deployment condition. But even then, multi-run at 0.1-0.2 tells you how fragile the greedy path is (variance ≈ sensitivity), which matters for model selection robustness. I'll include this.
