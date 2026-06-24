# Coding Evals

This directory contains coding evaluation tasks for benchmarking local LLM code quality. Each eval tests whether a model can produce correct, clean, idiomatic code in Python, Java, and Rust.

## Workflow

### 1. Run the model

Edit the constants at the top of `manual_code_eval.py` (in the repo root):

```python
MODEL = "Qwen3.6-35B-A3B-UD-Q4_K_M"
PROMPT_FILE = "evals/bubble-sort/python/prompt.md"
OUTPUT_DIR = "evals/bubble-sort/python/qwen-q4"
```

Then run it (model must be serving via Ramalama on the configured HOST/port):

```bash
python3 manual_code_eval.py
```

This produces two files in OUTPUT_DIR:
- `{model}.md` — full request/response trace (reasoning, response, timings)
- The code file with the correct name for the language (e.g., `bubble_sort.py`)

The code filename is auto-detected from the language directory in PROMPT_FILE's path, using the `LANG_CODE_FILENAMES` mapping in `manual_code_eval.py`.

### 2. Run tests and generate scorecard

No extra configuration needed — the script reads MODEL, OUTPUT_DIR, and PROMPT_FILE from `manual_code_eval.py`:

```bash
python3 run_tests.py
```

This script:
1. Copies the test file(s) into the model's output directory
2. Runs the tests (Python runs directly; Java and Rust run via Docker containers)
3. Parses pass/fail counts from the test output
4. Generates `scorecard.md` with test results pre-filled and code quality scores blank
5. Cleans up all test artifacts (test files, compiled classes, build directories)

After cleanup, the model directory contains only:
- The trace `.md`
- The code file
- `scorecard.md`

### 3. Score code quality

Open the model's `scorecard.md` and score each of the five dimensions (1–5) by reading the model's code against the eval's `rubric.md`. See `scorecard_example.md` in each eval for guidance on how to score.

## Docker Requirements

Java and Rust tests run in Docker containers (Python runs natively). The images used are:
- **Java:** `eclipse-temurin:21`
- **Rust:** `rust:1-slim`

These are pulled automatically on first run.

## Eval Structure

Each eval lives in its own directory under `evals/` with a companion `.md` file at the top level:

```
evals/
  README.md                        # This file
  bubble-sort.md                   # Eval overview and test case documentation
  bubble-sort/
    rubric.md                      # Code quality scoring rubric (5 dimensions, 1-5 each)
    scorecard_example.md           # Filled-in example showing how to score
    reference-impl/                # Verified reference implementations
      bubble_sort.py
      BubbleSortTasks.java
      lib.rs
    python/
      prompt.md                    # Prompt given to the model
      test_bubble_sort.py          # Test suite (model never sees this)
      <model-name>/               # One subdirectory per model run
        {model}.md                 #   Full trace
        bubble_sort.py             #   Model's code
        scorecard.md               #   Test results + quality scores
    java/
      prompt.md
      BubbleSortTasksTest.java
      <model-name>/
        {model}.md
        BubbleSortTasks.java
        scorecard.md
    rust/
      prompt.md
      Cargo.toml                   # Needed for cargo test
      src/lib.rs                   # Stub (model replaces this)
      tests/test_bubble_sort.rs
      <model-name>/
        {model}.md
        lib.rs
        scorecard.md
```

## Scoring

Each eval has two scoring axes:

1. **Correctness** — automated, binary: how many tests pass out of the total
2. **Code quality** — human-scored against a rubric with five dimensions:
   - **Naming** (1–5): descriptive names, language conventions
   - **Documentation** (1–5): docstring explaining behavior, parameters, edge cases
   - **Language Idiom** (1–5): idiomatic patterns for the target language
   - **Structure** (1–5): clean separation of logic, reasonable length
   - **Edge Cases** (1–5): graceful handling without over-engineering

Total quality score: 25 points. See each eval's `rubric.md` for detailed criteria per score level.

## How to Create a New Eval

### Design principles

These principles guided the design of the existing evals and should be followed for new ones:

1. **Deterministic, automatable correctness testing.** Tests must produce unambiguous pass/fail results. No subjective judgment in the test suite — save that for the code quality rubric.
2. **Dodge training data.** Use a twist on familiar algorithms or a custom format/spec so models can't copy-paste from memorized solutions. The twist should be simple enough for a human to verify.
3. **Same task, three languages.** The core problem is identical across Python, Java, and Rust. Only the syntax and idioms differ. This lets you compare model capability across languages.
4. **Precise, succinct prompts.** Each prompt specifies the exact function signature, data types, sorting rules (or equivalent spec), and constraints. One example input/output pair is included. No ambiguity.
5. **Test infrastructure the model never sees.** The model gets only the prompt. Test files, reference implementations, and rubrics are hidden. For future agentic evals, keep test infrastructure isolated from the model's working directory.

### Step-by-step

1. **Choose a task** that is simple enough for a human to verify but has a twist that forces original work (custom comparator, unusual data format, specific edge case handling). The algorithm itself should not be the challenge — the signal comes from the comparator logic, data handling, and code quality.

2. **Define the spec precisely:**
   - Exact function/method signatures for each language
   - Input/output data types
   - All behavioral rules (sorting order, null handling, etc.)
   - Constraints (no built-in sort, must return X, must not modify input, etc.)
   - One example input/output pair

3. **Create the directory structure:**
   ```
   evals/
     new-eval.md                   # Overview, test case table, design rationale
     new-eval/
       rubric.md                   # Can reuse the standard 5-dimension rubric
       scorecard_example.md        # Filled-in example with scoring commentary
       reference-impl/             # Your verified implementations
       python/
         prompt.md                 # The exact prompt for Python
         test_*.py                 # unittest test suite
       java/
         prompt.md
         *Test.java                # Standalone test with main() (no JUnit)
       rust/
         prompt.md
         Cargo.toml
         src/lib.rs                # Stub with todo!()
         tests/test_*.rs           # Integration tests
   ```

4. **Write prompts** — one per language, specifying the exact signature and types for that language. Keep them under ~200 words. Include one example.

5. **Write test suites** — design test cases covering:
   - Base cases (empty, single element)
   - Happy path (already correct, needs full reorder)
   - Edge cases (nulls, ties, all-same values)
   - A comprehensive mixed case
   - Input immutability check
   - Any deterministic metric (like swap count) that lets you assert exact values

6. **Write reference implementations** — one per language. These prove the test suite is correct. Verify all tests pass:
   - Python: `python3 -m unittest test_* -v`
   - Java: `docker run --rm -v "$(pwd):/work" -w /work eclipse-temurin:21 sh -c "javac *.java && java *Test"`
   - Rust: `docker run --rm -v "$(pwd):/work" -w /work rust:1-slim sh -c "cargo test"`

7. **Move reference implementations** to `reference-impl/` and restore stubs. The reference implementations are for verification, not gold-standard code quality.

8. **Update `manual_code_eval.py`** — add entries to `LANG_CODE_FILENAMES` if the new eval uses different output filenames. Currently this mapping is global, not per-eval. If you add a second eval with different filenames, this will need refactoring (e.g., reading the filename from the prompt or a config file).

9. **Update `run_tests.py`** — the test file copying, test execution, and cleanup logic is currently hardcoded for the bubble-sort eval's specific filenames. A new eval will need its own entries in `copy_test_files()`, `run_tests()`, and `cleanup()`. This is a known limitation that should be generalized when adding the second eval.

10. **Add `.gitignore` files** for each language directory to exclude build artifacts (`__pycache__/`, `*.class`, `target/`).

### Known limitations to address when adding a second eval

- `LANG_CODE_FILENAMES` in `manual_code_eval.py` is a flat language→filename mapping. A second eval with different filenames (e.g., `parser.py` instead of `bubble_sort.py`) will conflict. Solution: make the mapping eval-aware, or read the filename from the prompt file.
- `run_tests.py` hardcodes test file names and Docker commands for bubble-sort. Generalize to read test configuration from the eval directory.
- Both scripts use module-level constants. Consider moving to CLI arguments or a config file per eval as the number of evals grows.
