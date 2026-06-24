# Eval: Bubble Sort with Custom Comparator

## Overview

Tests whether a model can implement bubble sort for structured records with a multi-field comparator, null handling, and swap counting. The algorithm is trivial — the signal comes from handling the comparator logic correctly and writing clean, idiomatic code.

Models are evaluated on two axes:
1. **Correctness** — do the 11 automated tests pass?
2. **Code quality** — scored against a 5-dimension rubric (see `bubble-sort/rubric.md`)

## The Task

Sort a list of Task records using bubble sort.

Each task has three fields:
- `name` (string)
- `priority` (integer or null)
- `created_at` (integer, unix timestamp)

**Sorting rules:**
1. Primary: `priority` descending (higher first)
2. Tiebreaker: `created_at` ascending (earlier first)
3. Null priority always sorts to the end, ordered by `created_at` ascending among themselves

**Additional requirements:**
- Must use bubble sort — no built-in sort functions
- Return both the sorted list and the total number of swaps performed
- Must not modify the original input

## Languages

The same task is given in Python, Java, and Rust, expressed idiomatically for each language. Prompts are in `bubble-sort/<language>/prompt.md`.

| Language | Model writes | Test command |
|----------|-------------|-------------|
| Python | `bubble_sort.py` | `python3 -m unittest test_bubble_sort -v` |
| Java | `BubbleSortTasks.java` | `javac *.java && java BubbleSortTasksTest` |
| Rust | `src/lib.rs` | `cargo test` |

## Running an Eval

1. Give the model the contents of the appropriate `prompt.md`
2. Create a subdirectory for the model under the language directory (e.g., `python/qwen-q8/`)
3. Save the model's output into that subdirectory with the expected filename
4. Copy the test file into the subdirectory and run the test command from there
5. Record pass/fail count (11 tests total)
6. Score code quality using `bubble-sort/rubric.md` (5 dimensions, 1–5 each, 25 max)

### Example: testing Qwen Q8 on Python

```bash
mkdir -p evals/bubble-sort/python/qwen-q8
# save model output as evals/bubble-sort/python/qwen-q8/bubble_sort.py
cp evals/bubble-sort/python/test_bubble_sort.py evals/bubble-sort/python/qwen-q8/
cd evals/bubble-sort/python/qwen-q8
python3 -m unittest test_bubble_sort -v
```

## Test Cases

| # | Test | What it checks |
|---|------|---------------|
| 1 | Empty list | Returns `([], 0)` |
| 2 | Single element | Returns unchanged, 0 swaps |
| 3 | Already sorted | Recognizes no work needed, 0 swaps |
| 4 | Reverse sorted | Full reorder, 3 swaps |
| 5 | Tiebreaker | Same priority, sorts by `created_at` ascending |
| 6 | Null to end | Null priority after all non-null |
| 7 | Multiple nulls | Nulls ordered by `created_at` among themselves |
| 8 | Mixed (5 tasks) | Priorities, ties, and nulls combined — 5 swaps |
| 9 | All same priority | Pure tiebreaker sorting |
| 10 | Null after lowest | Null sorts after priority=1 |
| 11 | Input unmodified | Original list/slice is not mutated |

## Code Quality Rubric (summary)

Full rubric with scoring details is in `bubble-sort/rubric.md`.

| Dimension | What to look for |
|-----------|-----------------|
| Naming (1–5) | Descriptive names, language conventions (snake_case / camelCase) |
| Documentation (1–5) | Docstring explaining sorting rules, params, return value |
| Idiom (1–5) | Language-appropriate patterns (type hints, records, Option handling) |
| Structure (1–5) | Comparison logic cleanly separated, reasonable function length |
| Edge Cases (1–5) | Handles empty/single/all-null without unnecessary special-casing |

## File Layout

```
evals/bubble-sort/
  rubric.md                        # Detailed scoring rubric
  reference-impl/                  # Verified reference implementations
    bubble_sort.py
    BubbleSortTasks.java
    lib.rs
  python/
    prompt.md                      # Prompt to give the model
    test_bubble_sort.py            # 11 unittest tests (model never sees this)
    <model-name>/                  # One subdirectory per model run
      bubble_sort.py               #   Model's output
      test_bubble_sort.py          #   Copy of test file
  java/
    prompt.md
    BubbleSortTasksTest.java       # 11 tests via main() — no JUnit needed
    <model-name>/
      BubbleSortTasks.java
      BubbleSortTasksTest.java
  rust/
    prompt.md
    Cargo.toml
    src/lib.rs                     # Stub — model replaces this file
    tests/test_bubble_sort.rs      # 11 integration tests
    <model-name>/                  # Full Cargo project copy per model
```

## Design Rationale

**Why bubble sort?** Simple enough that anyone can verify correctness by reading the code. The interesting signal is in the comparator logic, null handling, and code style — not the algorithm.

**Why the twist (multi-field sort, nulls, swap count)?** Plain bubble sort is heavily represented in LLM training data. The custom comparator forces original work and gives richer signal on the code quality axis.

**Why swap count?** It's deterministic (equals the number of inversions in the input), so we can assert exact values. It also tests whether the model integrates the counting cleanly into the sort loop rather than bolting it on awkwardly.
