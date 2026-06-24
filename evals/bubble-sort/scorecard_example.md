# Scorecard Example — How to Score Code Quality

This is a filled-in example showing how to evaluate a model's code output against the rubric (`rubric.md`). Use this as a reference when scoring real model submissions.

The `run_tests.py` script auto-generates a blank scorecard with test results pre-filled. Your job is to read the model's code and fill in the five quality scores.

---

## Example: Fictional Model — Python

### Test Results (auto-filled by run_tests.py)

- **Tests passed:** 10 / 11
- **Tests failed:** 1

### Code Quality

| Dimension | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| Naming | 4 | Good names overall (`swap_count`, `should_swap`). Minor: used `t` as a loop variable instead of `task`. |
| Documentation | 3 | Has a docstring but only says "Sorts tasks using bubble sort." Doesn't explain the priority-descending/created_at-ascending rules or None handling. |
| Language Idiom | 5 | Proper type hints, list comprehension for the copy, tuple return. Fully idiomatic Python. |
| Structure | 4 | Comparison logic is in a separate `should_swap` helper — clean. Minor: the helper is nested inside the main function, which is fine but a module-level function would be slightly cleaner. |
| Edge Cases | 4 | All edge cases pass, but has an explicit `if len(tasks) <= 1: return` guard that isn't needed — the loop naturally handles it. |
| **Total** | **20 / 25** | |

### Evaluation

- **Evaluator:** Jane Smith
- **Date:** 2026-06-20

### Overall Notes

Solid implementation. The main weakness is documentation — the docstring doesn't explain the sorting rules, which matters for a function with non-obvious behavior (priority descending, None to end). A reader would have to read the comparison logic to understand what the function does.

---

## Scoring Tips

1. **Read the code before looking at test results.** Form your quality impression independently, then check if test failures reveal issues you missed.

2. **Score relative to the rubric, not to perfection.** A score of 5 means "a practitioner would approve this in code review without changes to this dimension." It doesn't mean the code is the best possible implementation.

3. **Language idiom varies.** What's idiomatic in Python (type hints, list comprehensions) is different from Java (records, generics) and Rust (match expressions, Option handling). Score based on the conventions of the language being used.

4. **Edge cases: prefer generality over guards.** A bubble sort that naturally handles empty lists through its loop structure (5) is better than one with an explicit early-return check (4), because the guard suggests the author wasn't confident the main logic would work.

5. **Document the "why" in your notes.** Future you (or someone else reviewing the benchmark results) needs to understand why you gave a 3 vs a 4. One sentence per dimension is enough.

6. **Be consistent across models.** If you dock one model for no docstring, dock them all. The rubric criteria are your anchor — refer back to it when in doubt.
