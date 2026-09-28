# Scorecard: Ornith-1.5-35B-A3B-UD-Q8_K_XL

## Test Results

- **Tests passed:** 11 / 11
- **Tests failed:** 0

## Code Quality (see rubric.md for criteria)

| Dimension | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| Naming | 5 | Descriptive snake_case throughout: `bubble_sort_tasks`, `_should_swap`, `ordered`, `pass_number`, `swap_count`. No cryptic abbreviations. |
| Documentation | 5 | Module docstring plus full function docstrings on both `_should_swap` and `bubble_sort_tasks` covering the three ordering rules, args, return value, and null/immutability behavior. Inline comments explain intent at each branch (`# Only a lacks a priority -> a belongs at the end.`) rather than restating code. |
| Language Idiom | 5 | Modern `list[dict]`/`tuple[list[dict], int]` type hints, shallow-copy-then-swap pattern, tuple unpacking swap, a guarded `if __name__ == "__main__":` demo block (harmless — doesn't execute on import). |
| Structure | 5 | Comparison logic fully extracted into `_should_swap`, separated from the swap mechanics; textbook bubble sort with the reducing inner range (`n - 1 - pass_number`) and an early-exit `swapped` flag. No unnecessary abstractions. |
| Edge Cases | 5 | Empty and single-element lists fall out of the loop bounds naturally; both-null and single-null priority cases are handled by `_should_swap` without special-case branches; equality (same priority **and** same `created_at`) uses strict `>` comparisons, so exact ties never trigger a spurious swap — no stability bug. |
| **Total** | **25 / 25** | |

## Evaluation

- **Evaluator:** Claude
- **Date:** 2026-09-27

## Overall Notes

All 11 hidden tests pass. `_should_swap` centralizes every ordering rule (both-null → `created_at` fallback, one-null → sorts last, equal priority → `created_at` tiebreak) using strict inequalities throughout, so exact ties are correctly left unswapped — this avoids the stability bug found in the Muse-Glimmer Python run. The implementation is clean, fully idiomatic, and matches the strongest Python runs in this benchmark set (Qwen3.6, Nemotron BF16). No latent issues found in review.
