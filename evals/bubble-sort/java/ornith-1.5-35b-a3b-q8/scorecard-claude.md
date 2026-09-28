# Scorecard: Ornith-1.5-35B-A3B-UD-Q8_K_XL

## Test Results

- **Tests passed:** 11 / 11
- **Tests failed:** 0

## Code Quality (see rubric.md for criteria)

| Dimension | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| Naming | 5 | Descriptive camelCase throughout: `bubbleSortTasks`, `compare`, `swap`, `priorityCompare`, `swapCount`, `createdAt`. |
| Documentation | 5 | Full Javadoc on the class, both records, and every method, including the null-handling and ordering rules. Inline comments explain the business rules at each branch of `compare`, not just restate the code. |
| Language Idiom | 4 | `record` types for `Task`/`SortResult`, a proper 3-way `Integer.compare`/`Long.compare` comparator (avoids the boxed-`Integer` relational-operator pitfall seen in the Nemotron Java runs), and `List.of` in the demo. One non-idiomatic addition: an unrequested `public static void main` demo method (the prompt asked only for the `bubbleSortTasks` method) — the same deduction applied to the Nemotron BF16 Java run. |
| Structure | 5 | Comparison and swap logic cleanly separated into private `compare`/`swap` helpers; the public method stays a standard reducing-bound bubble sort with an early-exit flag. |
| Edge Cases | 5 | Empty and single-element lists fall out of the loop bounds naturally; both-null and single-null priorities are handled by `compare` without special-casing; equal priority **and** `createdAt` returns `0` (no spurious swap). Also defensively treats a `null` input list as empty, beyond what the spec required, with no cost to correctness. |
| **Total** | **24 / 25** | |

## Evaluation

- **Evaluator:** Claude
- **Date:** 2026-09-27

## Overall Notes

All 11 hidden tests pass. This is one of the strongest Java runs in the set: proper `record`-based `Task`/`SortResult`, a correct 3-way comparator using `Integer.compare`/`Long.compare` (sidestepping the boxed-`Integer` bug seen elsewhere), and fully documented null/tie handling. The only deduction is the same one applied consistently across this benchmark: an unnecessary demo `main` method that the prompt didn't ask for.
