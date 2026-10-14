# Scorecard: LFM2.5-24B-A2B-Q8_0 — Java (claude review)

## Test Results

- **Tests passed:** 0 / 11 — **compile failure** (45 errors, cascading from the generated lib)
- **Root cause:** the model used **array indexing on a `List`** — `if (isOutOfOrder(sorted[j], sorted[j + 1]))` — instead of `sorted.get(j)`. `List<Task>` indexed with `[]` is invalid Java; the lib fails to compile, so every test fails with cascading errors (including errors in the test file, e.g. `variable r of type SortResult`).
- **Extraction verified:** the final code block in the trace (block 4 of 4, 110 lines) matches `BubbleSortTasks.java` byte-for-byte. The model iterated across 4 code drafts (in its thinking trace) and the `sorted[j]` mistake survived into the final answer — genuine model bug, not a tooling regression. Mirrors the Nemotron-30B-A3B fatal-but-good-code treatment.

## Code Quality (see rubric.md for criteria)

| Dimension | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| Naming | 4 | Clean camelCase throughout (`bubbleSortTasks`, `isOutOfOrder`, `swapCount`); minor generic `temp` swap variable. |
| Documentation | 5 | Full Javadoc on class and methods: sorting rules as an HTML list, `@param`/`@return`, explicit null-priority rule ("placed at the end, ordered by createdAt ascending"), `@link SortResult`. Inline comments explain business rules at the point of implementation. |
| Language Idiom | 2 | Otherwise idiomatic (generics, `List` API, static nested classes) — but the single `sorted[j]` array-indexing line is a Python/JS idiom translated into Java and it breaks compilation. |
| Structure | 5 | Comparison logic cleanly separated into `isOutOfOrder` helper; reasonable length; no unnecessary abstractions. |
| Edge Case Handling | 5 | All-null and null-vs-null priority handled via 3-way logic; empty/single lists fall out of loop bounds naturally; input list copied so original is unmodified. |
| **Total** | **21 / 25** | |

## Notes

- The sorting **logic is correct** (priority descending with `Integer.compare(b.priority, a.priority)`, tie-break `createdAt` ascending, null-priority-to-end via explicit 3-way branches, early exit on `!swapped`, `n - i - 1` bound, shallow copy). Had the one indexing line been `sorted.get(j)`/`sorted.get(j + 1)`, this would likely have passed all 11 tests and scored 24–25/25 like the BF16 Java run.
- Static nested classes (`Task`, `SortResult`) instead of records this time — acceptable per rubric, slightly less idiomatic than the BF16 run's records.
- Contrast with BF16 run (11/11, 24/25): Q8_0's sampling at temperature 0.0 produced a draft with a fatal single-token-level mistake the model failed to catch across 4 self-revisions.
