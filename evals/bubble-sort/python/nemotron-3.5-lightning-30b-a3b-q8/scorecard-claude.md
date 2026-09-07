# Scorecard: NVIDIA-Nemotron-3.5-Lightning-30B-A3B-UD-Q8_K_XL

## Test Results

- **Tests passed:** 0 / 11
- **Tests failed:** 11

**The generated module does not import** — the *same* failure as this model's Q6 run. Line 3 is
`from typing import list, dict, tuple`, but `typing` doesn't export those lowercase names (and the import
is redundant under PEP 585). Importing `bubble_sort.py` raises `ImportError` before any test runs, so all
11 tests error out. That the identical mistake appears at both Q6 and Q8 indicates it is a **model trait,
not a quantization artifact**.

## Code Quality (see rubric.md for criteria)

| Dimension | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| Naming | 4 | Clear snake_case: `bubble_sort_tasks`, `_should_swap`, `sorted_tasks`, `swap_count`. Comparison locals `pri_a`/`pri_b`/`ca`/`cb` are terse but symmetric; `i`/`j`/`n` conventional. |
| Documentation | 5 | Module docstring, an exhaustive function docstring (rules, args, return, constraints), and helpful inline comments on each branch of `_should_swap`. |
| Language Idiom | 1 | **Fatal:** `from typing import list, dict, tuple` is invalid and unimportable — the same disqualifying idiom error as the Q6 run. |
| Structure | 3 | The nested `_should_swap` predicate and the sort loop are clean, but the demo/usage code (lines 80-92) sits at **module top level** rather than under an `if __name__ == "__main__"` guard, so it would execute on import. The Q6 run guarded its demo correctly; this one regressed. |
| Edge Cases | 4 | The *logic* is correct and complete — empty/single fall out of the loop bounds, nulls sort last with a `created_at` fallback, and equality uses `>` (no spurious-swap bug). Docked one point because the import failure means none of it executes. |
| **Total** | **17 / 25 (code does not run — 0/11 tests)** | |

### Evaluation

- **Evaluator:** Claude
- **Date:** 2026-09-06

## Overall Notes

Functionally a failure (**0/11**), caused by the identical invalid `from typing import list, dict, tuple`
line seen in the Q6 run — strong evidence this is a consistent model behavior rather than a quant effect.
As at Q6, the surrounding code is otherwise good (thorough docs, correct algorithm including the
equal-`created_at` tiebreak), but here the demo block is left unguarded at module scope, dropping Structure
to 3 and the total below the Q6 Python run (19/25). Generation was fast (~47.2 t/s) with a large reasoning
trace (3,814 reasoning tokens for a 1,071-token answer).
