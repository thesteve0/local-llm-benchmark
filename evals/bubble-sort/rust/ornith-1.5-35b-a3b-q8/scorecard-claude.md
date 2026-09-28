# Scorecard: Ornith-1.5-35B-A3B-UD-Q8_K_XL

## Test Results

- **Tests passed:** 11 / 11
- **Tests failed:** 0

> **Note on test execution:** `run_tests.py` does not support Rust (documented limitation in
> `evals/README.md`); tests were run manually via `docker run --rm -v <dir>:/work -w /work
> rust:1-slim cargo test`, using the hidden `tests/test_bubble_sort.rs` suite. The model's own
> internal `#[cfg(test)] mod tests` (7 tests) and one doc-test also passed but aren't part of the
> graded 11.
>
> **Note on extraction:** `manual_code_eval.py`'s `extract_code()` joins *every* fenced code block
> in the response, but this response contained three separate blocks — an illustrative `Cargo.toml`
> snippet, the actual `src/lib.rs`, and a closing `cargo test`/`cargo clippy` usage note — which got
> concatenated into a non-compiling `lib.rs`. This is a tooling bug, not a model defect. The `lib.rs`
> in this directory was manually corrected to contain only the model's actual library code (verified
> against the `## Response` section of the trace `.md`) before running/scoring it.

## Code Quality (see rubric.md for criteria)

| Dimension | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| Naming | 5 | Descriptive throughout: `task_comes_before`, `sorted`, `swap_count`, `last` (the shrinking upper bound), conventional `n`/`j` loop counters. |
| Documentation | 5 | Module-level `//!` doc, `///` doc comments on `Task`, both fields, `task_comes_before`, and `bubble_sort_tasks`, including a working doc-test example that compiles and passes. Inline comments explain intent (`// last is the index of the last element still awaiting its final place`), not mechanics. |
| Language Idiom | 5 | Idiomatic `Option` handling via tuple pattern matching (`match (a.priority, b.priority) { ... }`), `#[derive(Clone, Debug, PartialEq)]`, no `.sort()`/`.sort_by()`, borrows (`&Task`) instead of unnecessary clones in the comparator, owned `Vec` returned from `to_vec()`. |
| Structure | 5 | Ordering logic fully isolated in `task_comes_before`; `bubble_sort_tasks` is a standard reducing-bound bubble sort with an early-exit `swapped` flag. No unnecessary `main`/binary — this is a clean library crate, exactly as scoped. |
| Edge Cases | 5 | Empty and single-element slices fall out of the `(0..n).rev()` / `0..last` bounds naturally; both-`None`, one-`None`, and equal-priority-and-timestamp cases are all handled inside `task_comes_before` without special-case branches; equal elements return `false` (no swap), preserving stability. |
| **Total** | **25 / 25** | |

## Evaluation

- **Evaluator:** Claude
- **Date:** 2026-09-27

## Overall Notes

This is the first Rust run in the benchmark set to receive a quality score (prior Rust runs — Mellum2, Qwen3.6 — were only ever test-checked, never rubric-scored). All 11 hidden tests pass, plus the model's own 7 unit tests and 1 doc-test. The implementation is fully idiomatic Rust: `task_comes_before` centralizes every ordering rule via exhaustive `Option` pattern matching, ties are left unswapped (correct stability), and the crate ships with a working doc-test example. No latent issues found in review. The one wrinkle in this run was in tooling, not the model: `manual_code_eval.py` naively concatenates every fenced code block in a response, and this response's answer contained a `Cargo.toml` snippet and a closing usage note as separate blocks alongside the real `lib.rs`, corrupting the saved file. The actual code (recovered from the trace and shown above) is clean and correct.
