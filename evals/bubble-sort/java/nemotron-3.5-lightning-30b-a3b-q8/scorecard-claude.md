# Scorecard: NVIDIA-Nemotron-3.5-Lightning-30B-A3B-UD-Q8_K_XL

## Test Results

- **Tests passed:** 11 / 11
- **Tests failed:** 0

## Code Quality (see rubric.md for criteria)

| Dimension | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| Naming | 5 | Descriptive camelCase: `bubbleSortTasks`, `shouldSwap`, `SortResult`, `Task`, `swapCount`, `swapped`, and clear `aNull`/`bNull` flags. `temp`/`n` conventional. |
| Documentation | 5 | Thorough Javadoc — class, both records, both methods with `@param`/`@return`, an HTML `<ul>` of the ordering rules, plus inline comments on each `shouldSwap` branch. |
| Language Idiom | 3 | Records, generics, accessor methods (`a.priority()` — more idiomatic than the Q6 run's direct field access), `List.of()` in the demo. **But** line 73 compares two `Integer` objects with `!=` (`a.priority() != b.priority()`), i.e. reference equality rather than value equality — a classic Java pitfall. It should unbox (`!=` on `int`) or use `Integer.compare`/`.equals`. Also carries an extraneous `main`. |
| Structure | 5 | Clean split: `bubbleSortTasks` owns copy/loop, `shouldSwap` isolates the rules, `SortResult` models the return. Textbook bubble sort with early exit. |
| Edge Cases | 3 | Empty and single-element lists fall out naturally; nulls sort last with a `createdAt` fallback. **Two flaws:** (1) The `!=` reference comparison on line 73 means two *equal* priorities held in distinct `Integer` objects (values ≥ 128, outside the Integer cache) skip the `createdAt` tiebreaker and return "no swap" — wrong order that the test suite misses because all its priorities are small cached values. (2) A null *input list* throws NPE at `new ArrayList<>(tasks)` — the Q6 run guarded this and returned an empty result. |
| **Total** | **21 / 25** | |

### Evaluation

- **Evaluator:** Claude
- **Date:** 2026-09-06

## Overall Notes

Passes all 11 tests and is well documented, but a notch below this model's own Q6 Java run (24/25). The
Q8 version actually improves on one point — it reads record components via accessor methods rather than
direct field access — yet regresses on correctness: it compares nullable priorities with `!=`, which is
reference equality on boxed `Integer`, so equal priorities outside the −128..127 cache would skip the
`createdAt` tiebreaker. The tests only use small priorities, so the bug stays latent and all 11 pass. It
also drops the null-input guard the Q6 run had. Same fast MoE generation (~47.2 t/s) with a large
reasoning trace (3,735 reasoning tokens for a 997-token answer).
