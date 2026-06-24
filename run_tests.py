#!/usr/bin/env python3

import glob
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from manual_code_eval import MODEL, OUTPUT_DIR, PROMPT_FILE, LANG_CODE_FILENAMES

REPO_ROOT = Path(__file__).parent

LANG_TEST_FILES = {
    "python": ["test_bubble_sort.py"],
    "java": ["BubbleSortTasksTest.java"],
    "rust": ["Cargo.toml"],
}


def detect_language(prompt_path: str) -> str:
    match = re.search(r'/(\w+)/prompt\.md$', prompt_path)
    if not match:
        raise ValueError(f"Cannot detect language from prompt path: {prompt_path}")
    return match.group(1).lower()


def get_eval_dir(prompt_path: str) -> Path:
    """Get the language-level eval directory (e.g., evals/bubble-sort/python/)."""
    return REPO_ROOT / Path(prompt_path).parent


def count_expected_tests(lang: str, eval_dir: Path) -> int:
    """Count the number of tests defined in the test file."""
    if lang == "python":
        text = (eval_dir / "test_bubble_sort.py").read_text()
        return len(re.findall(r'def test_', text))
    elif lang == "java":
        text = (eval_dir / "BubbleSortTasksTest.java").read_text()
        return len(re.findall(r'startTest\("', text))
    elif lang == "rust":
        text = (eval_dir / "tests" / "test_bubble_sort.rs").read_text()
        return len(re.findall(r'#\[test\]', text))
    return 0


def copy_test_files(lang: str, eval_dir: Path, out_dir: Path):
    if lang == "python":
        shutil.copy2(eval_dir / "test_bubble_sort.py", out_dir)
    elif lang == "java":
        shutil.copy2(eval_dir / "BubbleSortTasksTest.java", out_dir)
    elif lang == "rust":
        shutil.copy2(eval_dir / "Cargo.toml", out_dir)
        src_dir = out_dir / "src"
        src_dir.mkdir(exist_ok=True)
        shutil.copy2(out_dir / "lib.rs", src_dir / "lib.rs")
        tests_dir = out_dir / "tests"
        tests_dir.mkdir(exist_ok=True)
        shutil.copy2(eval_dir / "tests" / "test_bubble_sort.rs", tests_dir)


def run_tests(lang: str, out_dir: Path) -> tuple[str, int]:
    """Run tests and return (output_text, return_code)."""
    if lang == "python":
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "test_bubble_sort", "-v"],
            cwd=out_dir, capture_output=True, text=True, timeout=60,
        )
        return result.stderr + result.stdout, result.returncode
    elif lang == "java":
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{out_dir}:/work", "-w", "/work",
             "eclipse-temurin:21", "sh", "-c", "javac *.java && java BubbleSortTasksTest"],
            capture_output=True, text=True, timeout=120,
        )
        return result.stdout + result.stderr, result.returncode
    elif lang == "rust":
        result = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{out_dir}:/work", "-w", "/work",
             "rust:1-slim", "sh", "-c", "cargo test 2>&1"],
            capture_output=True, text=True, timeout=180,
        )
        return result.stdout + result.stderr, result.returncode
    else:
        raise ValueError(f"Unknown language: {lang}")


def parse_results(lang: str, output: str) -> tuple[int, int]:
    """Parse test output and return (passed, failed)."""
    if lang == "python":
        ran = re.search(r'Ran (\d+) test', output)
        total = int(ran.group(1)) if ran else 0
        failures = len(re.findall(r'^(?:FAIL|ERROR):', output, re.MULTILINE))
        if "OK" in output.split("Ran")[-1] if "Ran" in output else "":
            return total, 0
        return total - failures, failures
    elif lang == "java":
        match = re.search(r'Results: (\d+) passed, (\d+) failed', output)
        if match:
            return int(match.group(1)), int(match.group(2))
        return 0, 0
    elif lang == "rust":
        matches = re.findall(r'test result: \w+\. (\d+) passed; (\d+) failed', output)
        passed = sum(int(m[0]) for m in matches)
        failed = sum(int(m[1]) for m in matches)
        return passed, failed
    return 0, 0


def cleanup(lang: str, out_dir: Path):
    if lang == "python":
        (out_dir / "test_bubble_sort.py").unlink(missing_ok=True)
        for f in out_dir.glob("__pycache__"):
            shutil.rmtree(f, ignore_errors=True)
    elif lang == "java":
        (out_dir / "BubbleSortTasksTest.java").unlink(missing_ok=True)
        for f in out_dir.glob("*.class"):
            f.unlink(missing_ok=True)
    elif lang == "rust":
        (out_dir / "Cargo.toml").unlink(missing_ok=True)
        (out_dir / "Cargo.lock").unlink(missing_ok=True)
        shutil.rmtree(out_dir / "src", ignore_errors=True)
        shutil.rmtree(out_dir / "tests", ignore_errors=True)
        shutil.rmtree(out_dir / "target", ignore_errors=True)


def write_scorecard(out_dir: Path, model: str, passed: int, failed: int, total: int):
    out_path = out_dir / "scorecard.md"
    content = f"""# Scorecard: {model}

## Test Results

- **Tests passed:** {passed} / {total}
- **Tests failed:** {failed}

## Code Quality (see rubric.md for criteria)

| Dimension | Score (1-5) | Notes |
|-----------|:-----------:|-------|
| Naming | | |
| Documentation | | |
| Language Idiom | | |
| Structure | | |
| Edge Cases | | |
| **Total** | **/ 25** | |

## Evaluation

- **Evaluator:**
- **Date:**

## Overall Notes

"""
    out_path.write_text(content)
    print(f"Scorecard written to: {out_path}")


def main():
    out_dir = (REPO_ROOT / OUTPUT_DIR).resolve()
    lang = detect_language(PROMPT_FILE)
    eval_dir = get_eval_dir(PROMPT_FILE)
    code_filename = LANG_CODE_FILENAMES[lang]

    print(f"Model      : {MODEL}")
    print(f"Language   : {lang}")
    print(f"Output dir : {out_dir}")
    print(f"Code file  : {code_filename}")

    code_file = out_dir / code_filename
    if not code_file.exists():
        print(f"\nERROR: Code file not found: {code_file}")
        print("Run manual_code_eval.py first to generate the model output.")
        sys.exit(1)

    print("\n--- Copying test files ---")
    copy_test_files(lang, eval_dir, out_dir)

    print("\n--- Running tests ---")
    output, returncode = run_tests(lang, out_dir)
    print(output)

    expected_total = count_expected_tests(lang, eval_dir)
    passed, failed = parse_results(lang, output)
    total = max(expected_total, passed + failed)
    print(f"\n--- Results: {passed} passed, {total - passed} failed (of {total} tests) ---")

    print("\n--- Writing scorecard ---")
    write_scorecard(out_dir, MODEL, passed, total - passed, total)

    print("\n--- Cleaning up test artifacts ---")
    cleanup(lang, out_dir)

    print("Done.")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
